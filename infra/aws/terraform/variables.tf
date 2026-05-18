variable "aws_region" {
  description = "AWS region for EKS"
  type        = string
  default     = "eu-east-1"
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "telco-cloud-eks"
}

variable "vpc_cidr" {
  description = "VPC CIDR"
  type        = string
  default     = "10.10.0.0/16"
}
