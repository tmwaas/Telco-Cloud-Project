module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  version         = "~> 20.0"
  cluster_name    = var.cluster_name
  cluster_version = "1.29"
  subnet_ids      = [aws_subnet.public_a.id, aws_subnet.public_b.id]
  vpc_id          = aws_vpc.this.id
  eks_managed_node_groups = {
    default = { min_size=2, max_size=3, desired_size=2, instance_types=["t3.large"] }
  }
}
output "cluster_name" { value = module.eks.cluster_name }
output "cluster_endpoint" { value = module.eks.cluster_endpoint }
