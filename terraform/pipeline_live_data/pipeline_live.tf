provider "aws" {
  region     = var.REGION
  access_key = var.ACCESS_KEY
  secret_key = var.SECRET_KEY
}

# ECR Repository and image for pipeline lambda

data "aws_ecr_repository" "pipeline-lambda-image-repo" {
  name = "c17-allum-ecr-pipeline-terraform"
}

data "aws_ecr_image" "pipeline-lambda-image-version" {
  repository_name = data.aws_ecr_repository.pipeline-lambda-image-repo.name
  image_tag       = "latest"
}

# ECR Repository and image for sensor errors lambda

data "aws_ecr_repository" "sensor-errors-lambda-image-repo" {
  name = "c17-allum-ecr-sensor-errors-terraform"
}

data "aws_ecr_image" "sensor-errors-lambda-image-version" {
  repository_name = data.aws_ecr_repository.sensor-errors-lambda-image-repo.name
  image_tag       = "latest"
}

# ECR Repository and image for measurement errors lambda

data "aws_ecr_repository" "measurement-errors-lambda-image-repo" {
  name = "c17-allum-ecr-measurement-errors-terraform"
}

data "aws_ecr_image" "measurement-errors-lambda-image-version" {
  repository_name = data.aws_ecr_repository.measurement-errors-lambda-image-repo.name
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
    resources = ["arn:aws:logs:eu-west-2:${var.ACCOUNT_ID}:*"]
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

# Lambdas
# TODO: add environment variables

resource "aws_lambda_function" "pipeline-lambda" {
  function_name = "c17-allum-lambda-pipeline-terraform"
  description   = "Runs the ETL Pipeline every minute. Triggered by an EventBridge."
  role          = aws_iam_role.lambda-role.arn
  package_type  = "Image"
  image_uri     = data.aws_ecr_image.pipeline-lambda-image-version.image_uri
  timeout       = 900
}

resource "aws_lambda_function" "sensor-errors-lambda" {
  function_name = "c17-allum-lambda-sensor-errors-terraform"
  description   = "Check for sensor errors every minute. Triggered by an EventBridge."
  role          = aws_iam_role.lambda-role.arn
  package_type  = "Image"
  image_uri     = data.aws_ecr_image.sensor-errors-lambda-image-version.image_uri
  timeout       = 900
}

resource "aws_lambda_function" "measurement-errors-lambda" {
  function_name = "c17-allum-lambda-measurement-errors-terraform"
  description   = "Check for measurement errors every minute. Triggered by an EventBridge."
  role          = aws_iam_role.lambda-role.arn
  package_type  = "Image"
  image_uri     = data.aws_ecr_image.measurement-errors-lambda-image-version.image_uri
  timeout       = 900
}

# SNS

resource "aws_sns_topic" "alerts" {
  name = "c17-allum-sns-pipeline-alerts"
}

resource "aws_sns_topic_subscription" "email-sub" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.EMAIL
}
