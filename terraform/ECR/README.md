# `/terraform/ECR`

All terraform files to provision the ECR's are here.

## Set up

Create a `terraform.tfvars` file locally, and populate it with:

- ACCESS_KEY - AWS IAM access key.
- SECRET_KEY - The corresponding secret key for the above IAM user.

## Resources provisioned

#### ECR Repository: 
- `c17-allum-ecr-pipeline-terraform`.
- Stores the container image used by the ETL Lambda function.

#### ECR Repository:
- `c17-allum-ecr-dashboard-terraform`.
- Stores the container image for the Streamlit dashboard.

#### ECR Repository:
- `c17-allum-ecr-archived-terraform`.
- Stores the container image for the archived data Lambda.

#### ECR Repository:
- `c17-allum-ecr-sensor-errors-terraform`.
- Stores the container image for the sensor errors Lambda.

#### ECR Repository:
- `c17-allum-ecr-measurement-errors-terraform`.
- Stores the container image for the measurement errors Lambda.

## Provisioning Resources

To provision resources run the following commands:

`terraform plan`  
`terraform apply`