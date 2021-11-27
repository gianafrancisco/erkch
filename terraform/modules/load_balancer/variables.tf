variable "vpc_id" {
  type = string
}

variable "app" {
  type = string
}

variable "tags" {
    type = map(string)
}

variable "protocols" {
  type = map(string)
  default = {
    "8080" = "HTTP"
  }
}