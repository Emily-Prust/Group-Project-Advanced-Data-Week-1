provider "aws" {
  region     = var.AWS_REGION
  access_key = var.AWS_ACCESS_KEY
  secret_key = var.AWS_SECRET_KEY
}


# ECR Repository for pipeline image

resource "aws_ecr_repository" "pipeline-lambda-image-repo" {
  name                 = "c17-allum-ecr-pipeline-terraform"
  image_tag_mutability = "MUTABLE"

  encryption_configuration {
    encryption_type = "AES256"
  }
}

# Image for lambda to run

data "aws_ecr_image" "pipeline-lambda-image-version" {
  repository_name = aws_ecr_repository.pipeline-lambda-image-repo.name
  image_tag       = "latest"
}

# Permissions for lambda

data "aws_iam_policy_document" "pipeline-lambda-role-trust-policy-doc" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = [
      "sts:AssumeRole"
    ]
  }
}

data "aws_iam_policy_document" "pipeline-lambda-role-permissions-policy-doc" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["arn:aws:logs:eu-west-2:129033205317:*"]
  }
}

resource "aws_iam_role" "pipeline-lambda-role" {
  name               = "c17-allum-lambda-pipeline-terraform-role"
  assume_role_policy = data.aws_iam_policy_document.pipeline-lambda-role-trust-policy-doc.json
}

resource "aws_iam_policy" "pipeline-lambda-role-permissions-policy" {
  name   = "c17-allum-lambda-pipeline-permissions-policy"
  policy = data.aws_iam_policy_document.pipeline-lambda-role-permissions-policy-doc.json
}


resource "aws_iam_role_policy_attachment" "pipeline-lambda-role-policy-connection" {
  role       = aws_iam_role.pipeline-lambda-role.name
  policy_arn = aws_iam_policy.pipeline-lambda-role-permissions-policy.arn
}

# Lambda
# TODO: add environment variables

resource "aws_lambda_function" "pipeline-lambda" {
  function_name = "c17-allum-lambda-pipeline-terraform"
  description   = "Runs the ETL Pipeline every minute. Triggered by an EventBridge."
  role          = aws_iam_role.pipeline-lambda-role.arn
  package_type  = "Image"
  image_uri     = data.aws_ecr_image.pipeline-lambda-image-version.image_uri
  timeout       = 900
}

# remove