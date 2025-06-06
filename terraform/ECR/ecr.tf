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
    encryption_type = "AES256"
  }
}

# ECR Repository for dashboard image

resource "aws_ecr_repository" "dashboard-td-image-repo" {
  name                 = "c17-allum-ecr-dashboard-terraform"
  image_tag_mutability = "MUTABLE"

  encryption_configuration {
    encryption_type = "AES256"
  }
}

# ECR Repository for archived data image

resource "aws_ecr_repository" "archived-lambda-image-repo" {
  name                 = "c17-allum-ecr-archived-terraform"
  image_tag_mutability = "MUTABLE"

  encryption_configuration {
    encryption_type = "AES256"
  }
}

# ECR Repository for sensor errors image

resource "aws_ecr_repository" "sensor-errors-lambda-image-repo" {
  name                 = "c17-allum-ecr-sensor-errors-terraform"
  image_tag_mutability = "MUTABLE"

  encryption_configuration {
    encryption_type = "AES256"
  }
}

# ECR Repository for measurement errors image

resource "aws_ecr_repository" "measurement-errors-lambda-image-repo" {
  name                 = "c17-allum-ecr-measurement-errors-terraform"
  image_tag_mutability = "MUTABLE"

  encryption_configuration {
    encryption_type = "AES256"
  }
}