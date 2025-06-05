# `/terraform/pipeline_archived_data`

All terraform files to provision the resources for the archived data pipeline are here.

## Set up

Create a `terraform.tfvars` file locally, and populate it with:

- ACCESS_KEY - AWS IAM access key.
- SECRET_KEY - The corresponding secret key for the above IAM user.

## Resources provisioned

#### IAM Role & Policies:
- Permissions for CloudWatch Logs.

#### Lambda Function:
- `c17-allum-lambda-archived-terraform`.
- Retrieves oldest one hour of data and removes it from the database before uploading to S3.
- Scheduled to run every hour via EventBridge.
- Runs the latest image from `c17-allum-ecr-archived-terraform`.

## Provisioning Resources

To provision resources run the following commands:

`terraform plan`  
`terraform apply`