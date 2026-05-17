variable "region" {
  description = "AWS region"
  default     = "eu-west-1"
}

variable "instance_type" {
  description = "EC2 instance type"
  default     = "t2.micro"
}

variable "ami_id" {
  description = "Ubuntu 22.04 AMI ID"
  default     = "ami-0694d931cee176e7d"
}

variable "key_name" {
  description = "SSH key pair name in AWS"
}

variable "project_name" {
  description = "Project name used for tagging"
  default     = "linkscope"
}