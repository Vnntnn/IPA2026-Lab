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

variable "instance_type" {
  type        = string
  description = "EC2 instance size"
  default     = "t3.micro"
}

variable "allowed_http_cidrs" {
  type        = list(string)
  description = "CIDR blocks permitted to reach port 80"
  default     = ["0.0.0.0/0"]
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
