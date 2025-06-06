# `/terraform/pipeline_live_data`

All terraform files to provision the resources for the live data pipeline are here.

## Set up

Create a `terraform.tfvars` file locally, and populate it with:

- ACCESS_KEY - AWS IAM access key.
- SECRET_KEY - The corresponding secret key for the above IAM user.
- ACCOUNT_ID - AWS Account ID.
- EMAIL - The email to send SNS notifications to. 

## Resources provisioned

#### IAM Role & Policies for Lambdas:
- Permissions for CloudWatch Logs.

#### Lambda Function:
- `c17-allum-lambda-pipeline-terraform`.
- Runs the ETL Pipeline.
- Scheduled to run every minute via EventBridge.
- Runs the latest image from `c17-allum-ecr-pipeline-terraform`.

#### Lambda Function:
- `c17-allum-lambda-sensor-errors-terraform`.
- Checks for plants with sensor errors.
- Scheduled to run every minute via EventBridge.
- Runs the latest image from `c17-allum-ecr-sensor-errors-terraform`.

#### Lambda Function:
- `c17-allum-lambda-pipeline-terraform`.
- Checks for plants with measurement errors.
- Scheduled to run every minute via EventBridge.
- Runs the latest image from `c17-allum-ecr-measurement-errors-terraform`.

#### SNS
- SNS Topic `c17-allum-sns-pipeline-alerts`.
- Will send emails when triggered by a Lambda function.

## To Do

- Add environment variables to the lambda resource once known.
- Lambda may need `vpc_config` block to access RDS.

## Provisioning Resources

To provision resources run the following commands:

`terraform plan`  
`terraform apply`