output "instance_id" {
  value       = module.web_server.instance_id
  description = "ID of the web server instance"
}

output "public_ip" {
  value       = module.web_server.public_ip
  description = "Public IPv4 address of the web server"
}

output "public_dns" {
  value       = module.web_server.public_dns
  description = "Public DNS hostname of the web server"
}

output "web_url" {
  value       = "http://${module.web_server.public_dns}"
  description = "Ready-to-click URL for the web server"
}

output "security_group_id" {
  value       = module.web_server.security_group_id
  description = "ID of the web security group"
}

output "admin_password" {
  value       = var.admin_password
  description = "Demonstration of a sensitive output"
  sensitive   = true
}
