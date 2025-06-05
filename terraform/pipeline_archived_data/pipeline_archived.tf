provider "aws" {
  region     = var.REGION
  access_key = var.ACCESS_KEY
  secret_key = var.SECRET_KEY
}

# ECR Repository for archived data image

data "aws_ecr_repository" "archived-lambda-image-repo" {
  name = "c17-allum-ecr-archived-terraform"
}

# Image for lambda to run

data "aws_ecr_image" "archived-lambda-image-version" {
  repository_name = data.aws_ecr_repository.archived-lambda-image-repo.name
  image_tag       = "latest"
}

# Permissions for lambda

data "aws_iam_policy_document" "archived-lambda-role-trust-policy-doc" {
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

data "aws_iam_policy_document" "archived-lambda-role-permissions-policy-doc" {
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
      "s3:PutObject"
    ]
    resources = ["${aws_s3_bucket.archived-s3.arn}/*"]
  }
}

resource "aws_iam_role" "archived-lambda-role" {
  name               = "c17-allum-lambda-archived-terraform-role"
  assume_role_policy = data.aws_iam_policy_document.archived-lambda-role-trust-policy-doc.json
}

resource "aws_iam_policy" "archived-lambda-role-permissions-policy" {
  name   = "c17-allum-lambda-archived-permissions-policy"
  policy = data.aws_iam_policy_document.archived-lambda-role-permissions-policy-doc.json
}


resource "aws_iam_role_policy_attachment" "archived-lambda-role-policy-connection" {
  role       = aws_iam_role.archived-lambda-role.name
  policy_arn = aws_iam_policy.archived-lambda-role-permissions-policy.arn
}

# Lambda
# TODO: add environment variables

resource "aws_lambda_function" "archived-lambda" {
  function_name = "c17-allum-lambda-archived-terraform"
  description   = "Retrieves oldest one hour of data and removes it from the database before uploading to S3. Triggered by an EventBridge."
  role          = aws_iam_role.archived-lambda-role.arn
  package_type  = "Image"
  image_uri     = data.aws_ecr_image.archived-lambda-image-version.image_uri
  timeout       = 900
}

# S3 Bucket

resource "aws_s3_bucket" "archived-s3" {
  bucket = "c17-allum-s3-archived-data"
}

# EventBridge

resource "aws_cloudwatch_event_rule" "hourly-lambda-trigger" {
  name                = "c17-allum-hourly-lambda-trigger"
  description         = "Triggers the archived data lambda every hour."
  schedule_expression = "rate(1 hour)"
}

resource "aws_lambda_permission" "allow-eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.archived-lambda.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.hourly-lambda-trigger.arn
}

resource "aws_cloudwatch_event_target" "trigger-hourly-lambda" {
  arn  = aws_lambda_function.archived-lambda.arn
  rule = aws_cloudwatch_event_rule.hourly-lambda-trigger.name
}