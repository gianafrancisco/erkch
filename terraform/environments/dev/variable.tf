variable "region" {
  default = "us-east-2"
}

variable "app" {
  default = "Eureka"
}

variable "vpc_id" {
  default = "vpc-1b66a172"
}

variable "subnet_id" {
  default = "subnet-e8ad7e81"
}

variable "tags" {
  type = map(string)
  default = {
    "Project"       = "Eureka"
    "Environment"   = "Development"
    "Email"         = "gianafrancisco@gmail.com"
  }
}