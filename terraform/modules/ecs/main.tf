data "aws_subnet_ids" "subnets" {
  vpc_id = var.vpc_id
}

data "aws_subnet" "subnet" {
  for_each = data.aws_subnet_ids.subnets.ids
  id       = each.value
}

resource "aws_cloudwatch_log_group" "eureka_api" {
  name = "${var.app}-logs"
  tags = var.tags
}

resource "aws_ecs_cluster" "cluster" {
  name = "${var.app}-cluster"
  tags = var.tags
}

resource "aws_ecs_service" "service" {
  for_each        = var.services
  name            = "${var.app}-${each.value.name}-service"
  cluster         = aws_ecs_cluster.cluster.id
  task_definition = aws_ecs_task_definition.task[each.key].arn
  desired_count   = each.value.desired_count
  launch_type     = "FARGATE"
  # depends_on      = [module.load_balancer]

  load_balancer {
    target_group_arn = each.value.target_group_arn
    container_name   = "${var.app}-${each.value.name}-task"
    container_port   = each.value.port
  }
  network_configuration {
    subnets = data.aws_subnet_ids.subnets.ids
    security_groups = [aws_security_group.security_group[each.key].id]
    assign_public_ip = true
  }
  tags = var.tags

}

resource "aws_ecs_task_definition" "task" {
  for_each = var.services
  family = "${var.app}-${each.value.name}-task"
  requires_compatibilities = ["FARGATE"]
  network_mode = "awsvpc"
  cpu = 256
  memory = 512
  task_role_arn = each.value.task_role_arn
  execution_role_arn = each.value.task_role_arn
  container_definitions = templatefile("${path.module}/task.json", {
             NAME             = "${var.app}-${each.value.name}",
             REGION           = var.region,
             LOGS             = aws_cloudwatch_log_group.eureka_api.name
             IMAGE_REPOSITORY = each.value.image
           })
  tags = var.tags
}

resource "aws_security_group" "security_group" {
  for_each    = var.services
  name        = "${var.app}-${each.value.name}-security_group"
  description = "Allow inbound traffic"
  vpc_id      = var.vpc_id

  ingress {
    description      = ""
    from_port        = each.value.port
    to_port          = each.value.port
    protocol         = each.value.protocol
    cidr_blocks      = [for s in data.aws_subnet.subnet: s.cidr_block]
  }

  egress {
    from_port        = 0
    to_port          = 0
    protocol         = "-1"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
  }

  tags = var.tags
}