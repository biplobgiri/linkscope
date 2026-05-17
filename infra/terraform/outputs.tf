output "server_ip" {
  description = "Public IP of the LinkScope server"
  value       = aws_instance.linkscope.public_ip
}

output "ssh_command" {
  description = "SSH command to connect to the server"
  value       = "ssh -i ~/.ssh/id_rsa ubuntu@${aws_instance.linkscope.public_ip}"
}

output "app_url" {
  description = "URL to access the app"
  value       = "http://${aws_instance.linkscope.public_ip}"
}

output "grafana_url" {
  description = "URL to access Grafana"
  value       = "http://${aws_instance.linkscope.public_ip}:3000"
}