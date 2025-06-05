provider "aws" {
  region     = var.REGION
  access_key = var.ACCESS_KEY
  secret_key = var.SECRET_KEY
}

# ECR Repository for pipeline image

data "aws_ecr_repository" "pipeline-lambda-image-repo" {
  name = "c17-allum-ecr-pipeline-terraform"
}

# Image for lambda to run

data "aws_ecr_image" "pipeline-lambda-image-version" {
  repository_name = data.aws_ecr_repository.pipeline-lambda-image-repo.name
  image_tag       = "latest"
}

# Permissions for lambda

data "aws_iam_policy_document" "lambda-role-trust-policy-doc" {
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

data "aws_iam_policy_document" "lambda-role-permissions-policy-doc" {
  statement {
    effect = "Allow"
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = ["arn:aws:logs:eu-west-2:129033205317:*"]
  }

  statement {
    effect = "Allow"
    actions = [
      "rds-data:*"
    ]
    resources = []
  }

  statement {
    effect = "Allow"
    actions = [
      "sns:Publish"
    ]
    resources = []
  }
}

resource "aws_iam_role" "lambda-role" {
  name               = "c17-allum-lambda-terraform-role"
  assume_role_policy = data.aws_iam_policy_document.lambda-role-trust-policy-doc.json
}

resource "aws_iam_policy" "lambda-role-permissions-policy" {
  name   = "c17-allum-lambda-permissions-policy"
  policy = data.aws_iam_policy_document.lambda-role-permissions-policy-doc.json
}


resource "aws_iam_role_policy_attachment" "lambda-role-policy-connection" {
  role       = aws_iam_role.lambda-role.name
  policy_arn = aws_iam_policy.lambda-role-permissions-policy.arn
}

# Lambda
# TODO: add environment variables

resource "aws_lambda_function" "pipeline-lambda" {
  function_name = "c17-allum-lambda-pipeline-terraform"
  description   = "Runs the ETL Pipeline every minute. Triggered by an EventBridge."
  role          = aws_iam_role.lambda-role.arn
  package_type  = "Image"
  image_uri     = data.aws_ecr_image.pipeline-lambda-image-version.image_uri
  timeout       = 900
}