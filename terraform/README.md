# `/terraform`

All terraform files for the project are inside this folder.

## Folders

- `/ECR` will provision necessary ECR's for the project.
- `/pipeline_live_data` will provision resources for the live data pipeline.
- `/pipeline_archived_data` will provision resources for the archived data pipeline.
- `/dashboard` will provision resources for the dashboard.

## Set up

Run terraform apply in `/ECR` first as the resources in `/pipeline_live_data`, `/pipeline_archived_data`, `/dashboard` will rely on the ECR's provisioned there.