variable "aws_region" {
  description = "AWS region for the infrastructure"
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Project name used for tagging and resource naming"
  type        = string
  default     = "ai-ml-aiops-devops"
}

variable "cluster_name" {
  description = "EKS cluster name"
  type        = string
  default     = "ai-ml-aiops-eks"
}