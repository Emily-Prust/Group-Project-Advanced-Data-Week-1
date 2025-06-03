provider "aws" {
    region = var.AWS_REGION
    access_key = var.AWS_ACCESS_KEY
    secret_key = var.AWS_SECRET_KEY
}

resource "aws_ecr_repository" "pipeline-lambda-repo" {
    name = "c17-allum-ecr-pipeline-terraform"
    image_tag_mutability = "MUTABLE"

    encryption_configuration {
        encryption_type = "AES256"
    }
}