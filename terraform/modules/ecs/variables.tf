variable "vpc_id" {
    type = string
}

variable "app" {
  type = string
}

variable "region" {
    type = string
}

variable "tags" {
    type = map(string)
}

variable "services" {
    type = map(object({
        image            = string
        name             = string
        desired_count    = number
        port             = number
        protocol         = string
        target_group_arn = string
        task_role_arn    = string
  }))
}