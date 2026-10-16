output "server_ids" {
  value       = module.web_server.server_ids
  description = "Map of server name to instance ID"
}

output "web_urls" {
  value       = { for name, inst in module.web_server.instances : name => "http://${inst.public_dns}" }
  description = "Ready-to-click URL for each web server"
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

output "server_summary" {
  description = "Map of server name to its public DNS"
  value = {
    for name, inst in module.web_server.instances :
    name => inst.public_dns
  }
}

output "frontend_servers" {
  description = "Names of frontend servers only"
  value = [
    for name, cfg in var.servers : name
    if cfg.role == "frontend"
  ]
}

output "all_private_ips" {
  description = "Splat over all instances"
  value       = values(module.web_server.instances)[*].private_ip
}
