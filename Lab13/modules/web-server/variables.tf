variable "name_prefix" {
  type        = string
  description = "Prefix applied to all resource names"
}

variable "vpc_id" {
  type        = string
  description = "VPC in which to create the security group"
}

variable "subnet_id" {
  type        = string
  description = "Subnet in which to launch the instance"
}

variable "root_volume" {
  type = object({
    size_gb   = number
    type      = string
    encrypted = bool
  })
  default = {
    size_gb   = 8
    type      = "gp3"
    encrypted = true
  }
}

variable "tags" {
  type        = map(string)
  description = "Tags applied to all resources"
  default     = {}
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

variable "ingress_rules" {
  type = list(object({
    description = string
    port        = number
    protocol    = string
    cidr_blocks = list(string)
  }))
  description = "Security group ingress rules to generate"
  default = [
    {
      description = "HTTP"
      port        = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    },
    {
      description = "HTTPS"
      port        = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  ]
}
