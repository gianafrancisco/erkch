

data "aws_subnet_ids" "subnets" {
  vpc_id = var.vpc_id
}

module "iam" {
  source      = "../../modules/iam"
  tags        = var.tags
  region      = var.region
}

module "load_balancer" {
  source      = "../../modules/load_balancer"
  vpc_id      = var.vpc_id
  app         = var.app
  tags        = var.tags
  protocols   = {
    "8080" = "HTTP"
  }
}

module "dns" {
  source      = "../../modules/dns"
  dns_record  = "eureka-api"
  dns_name    = module.load_balancer.dns_name
  tags        = var.tags
}

module "services" {
  source         = "../../modules/ecs"
  tags           = var.tags
  vpc_id         = var.vpc_id
  region         = var.region
  app            = var.app
  services       = {
   "api" = {
      "image"              = "docker.io/fgiana/eureka-api:latest"
      "name"               = "api"
      "desired_count"      = 1
      "port"               = 8080
      "protocol"           = "tcp"
      "target_group_arn"   = module.load_balancer.target_groups["8080"].arn
      "task_role_arn"     = module.iam.task_role_arn
    }
  } 
}
