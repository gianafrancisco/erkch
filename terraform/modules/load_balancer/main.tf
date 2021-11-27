data "aws_subnet_ids" "subnets" {
  vpc_id = var.vpc_id
}

resource "aws_lb" "lb" {
  name               = "${var.app}-load-balancer"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.security_group.id]
  subnets            = data.aws_subnet_ids.subnets.ids
  tags               = var.tags
}

resource "aws_lb_target_group" "tg" {
  for_each = var.protocols
  name     = "${var.app}-target-group"
  port     = each.key
  protocol = each.value
  vpc_id   = var.vpc_id
  target_type = "ip"
  tags     = var.tags

  health_check {
    enabled             = true
    path                = "/health_check"
    healthy_threshold   = 5
    unhealthy_threshold = 2
  }
}

resource "aws_lb_listener" "lb_listener" {
  for_each = var.protocols
  load_balancer_arn = aws_lb.lb.arn
  port              = each.key
  protocol          = each.value

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.tg[each.key].arn
  }
}

resource "aws_security_group" "security_group" {
  name        = "${var.app}-security_group"
  description = "Allow inbound traffic"
  vpc_id      = var.vpc_id

  ingress {
    description      = "8080 to the world"
    from_port        = 8080
    to_port          = 8080
    protocol         = "tcp"
    cidr_blocks      = ["0.0.0.0/0"]
    ipv6_cidr_blocks = ["::/0"]
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