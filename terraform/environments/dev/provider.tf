terraform {
  required_providers {
    aws = {
      version = "~> 3.37"
    }
  }
  required_version = ">= 0.12.26"
}

provider "aws" {
  region  = var.region
  profile = var.app
}