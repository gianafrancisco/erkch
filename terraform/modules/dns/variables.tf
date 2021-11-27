variable "dns_record" {
  type = string
  default = "eureka-api"
}

variable "dns_name" {
  type = string
}

variable "zone" {
  type = string
  default = "gianafrancisco.com.ar."
}

variable "tags" {
    type = map(string)
}