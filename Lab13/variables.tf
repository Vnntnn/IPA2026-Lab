variable "aws_region" {
  type        = string
  description = "AWS region to deploy into"
  default     = "us-east-1"
}

variable "project_name" {
  type        = string
  description = "Short name used as a prefix for all resource names"
  default     = "ipa-lab02"
}

variable "environment" {
  type        = string
  description = "Deployment environment"
  default     = "dev"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "The environment must be one of: dev, staging, prod."
  }
}

variable "instance_type" {
  type        = string
  description = "EC2 instance size"
  default     = "t3.micro"

  validation {
    condition     = can(regex("^t[23]\\.", var.instance_type))
    error_message = "Only t2 and t3 instance families are permitted in this course."
  }
}

variable "instance_count" {
  type        = number
  description = "How many web servers to create"
  default     = 1

  validation {
    condition     = var.instance_count >= 1 && var.instance_count <= 3
    error_message = "instance_count must be between 1 and 3."
  }
}

variable "enable_monitoring" {
  type        = bool
  description = "Enable detailed CloudWatch monitoring"
  default     = false
}

variable "allowed_http_cidrs" {
  type        = list(string)
  description = "CIDR blocks permitted to reach port 80"
  default     = ["0.0.0.0/0"]
}

variable "extra_tags" {
  type        = map(string)
  description = "Additional tags applied to every resource"
  default     = {}
}

variable "root_volume" {
  type = object({
    size_gb   = number
    type      = string
    encrypted = bool
  })
  description = "Root EBS volume configuration"
  default = {
    size_gb   = 8
    type      = "gp3"
    encrypted = true
  }
}

variable "admin_password" {
  type        = string
  description = "Demonstration of a sensitive input - do NOT use in production"
  sensitive   = true
  default     = "ChangeMe123!"
}

variable "access_key" {
  type      = string
  sensitive = true
}

variable "secret_key" {
  type      = string
  sensitive = true
}

variable "token" {
  type      = string
  sensitive = true
}

variable "servers" {
  type = map(object({
    instance_type = string
    role          = string
  }))
  description = "Map of servers to create, keyed by logical name"
  default = {
    web = {
      instance_type = "t3.micro"
      role          = "frontend"
    }
    api = {
      instance_type = "t3.micro"
      role          = "backend"
    }
  }
}
