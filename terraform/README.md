# `/terraform`

All terraform files for the project are inside this folder.

## Set up

Create a `terraform.tfvars` file locally, and populate it with:

- ACCESS_KEY - AWS IAM access key.
- SECRET_KEY - The corresponding secret key for the above IAM user.
- VPC_ID - The ID of the VPC you want to use.
- SUBNET_ID_X - The ID's of subnets you want to use.


Note: `terraform init` has been run.

## Resources provisioned

### `pipeline.tf` will provision the following resources relevant to the ETL pipeline:

#### ECR Repository: 
- `c17-allum-ecr-pipeline-terraform`.
- Stores the container image used by the ETL Lambda function.

#### IAM Role & Policies:
- Permissions for CloudWatch Logs.

#### Lambda Function:
- `c17-allum-lambda-pipeline-terraform`.
- Runs the ETL Pipeline.
- Scheduled to run every minute via EventBridge.
- Runs the latest image from `c17-allum-ecr-pipeline-terraform`.

---

### `dashboard.tf` will provision the following resources relevant to the Streamlit Dashboard:

#### ECR Repository:
- `c17-allum-ecr-dashboard-terraform`.
- Stores the container image for the Streamlit dashboard.

#### ECS Task Definition:
- `c17-allum-td-dashboard`.
- Runs a containerized Streamlit dashboard.
- Runs the latest image from `c17-allum-ecr-dashboard-terraform`.
- Logs are sent to CloudWatch.

#### ECS Fargate Service:
- Runs the dashboard as a service.
- Accessible via port `8501`.
- Placed in public subnets.

#### Security Group:
- A security group for the ECS Service.
- Allows incoming HTTP traffic on port 8501 from any IP.
- Allows all outgoing traffic. 

## To Do

- Add environment variables to the lambda resource once known.
- Add environment variables to the task definition once known.

## Provisioning Resources

To provision resources run the following commands:

`terraform plan`  
`terraform apply`