# `/terraform/pipeline_archived_data`

All terraform files to provision the resources for the archived data pipeline are here.

## Set up

Create a `terraform.tfvars` file locally, and populate it with:

- ACCESS_KEY - AWS IAM access key.
- SECRET_KEY - The corresponding secret key for the above IAM user.
- ACCOUNT_ID - AWS Account ID.

## Resources provisioned

#### S3 Bucket:
- `c17-allum-s3-archived-data`.
- Stores archived data.

#### IAM Role & Policies:
- Permissions for CloudWatch Logs.
- Permissions for Lambda to write to S3.

#### Lambda Function:
- `c17-allum-lambda-archived-terraform`.
- Retrieves oldest one hour of data and removes it from the database before uploading to S3.
- Scheduled to run every hour via EventBridge.
- Runs the latest image from `c17-allum-ecr-archived-terraform`.

#### Eventbridge:
- Triggers the Lambda function every hour.

## To Do

- Add environment variables to the lambda resource once known.
- Lambda may need `vpc_config` block to access RDS.
- S3 may need `aws_s3_bucket_policy` resource to allow lambda write access.

## Provisioning Resources

To provision resources run the following commands:

`terraform plan`  
`terraform apply`