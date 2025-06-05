provider "aws" {
  region     = var.REGION
  access_key = var.ACCESS_KEY
  secret_key = var.SECRET_KEY
}

# ECR Repository for pipeline image

resource "aws_ecr_repository" "pipeline-lambda-image-repo" {
  name                 = "c17-allum-ecr-pipeline-terraform"
  image_tag_mutability = "MUTABLE"

  encryption_configuration {
    encryption_type = "AES25"
  }
}

#delete

# ECR Repository for dashboard image

resource "aws_ecr_repository" "dashboard-td-image-repo" {
  name                 = "c17-allum-ecr-dashboard-terraform"
  image_tag_mutability = "MUTABLE"

  encryption_configuration {
    encryption_type = "AES256"
  }
}