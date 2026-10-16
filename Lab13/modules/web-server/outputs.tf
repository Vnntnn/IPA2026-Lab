output "instance_id" {
  value       = aws_instance.web.id
  description = "ID of the created instance"
}

output "public_ip" {
  value       = aws_instance.web.public_ip
  description = "Public IPv4 address"
}

output "public_dns" {
  value       = aws_instance.web.public_dns
  description = "Public DNS hostname"
}

output "security_group_id" {
  value       = aws_security_group.web.id
  description = "ID of the created security group"
}
