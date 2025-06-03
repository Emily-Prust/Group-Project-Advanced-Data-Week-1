# `/terraform`

Create a `terraform.tfvars` file locally, and populate it with:

- AWS_ACCESS_KEY - AWS IAM access key
- AWS_SECRET_KEY - The corresponding secret key for the above IAM user

Note: `terraform init` has been run.

## Resources provisioned

`main.tf` will provision the following resources:

- An ECR Repository for the image for the ETL pipeline: `c17-allum-ecr-pipeline-terraform`

## Provisioning Resources

To provision resources run the following commands:

`terraform plan`
`terraform apply`