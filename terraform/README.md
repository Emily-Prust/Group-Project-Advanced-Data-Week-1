# `/terraform`

All terraform files for the project are inside this folder.

## Folders

- `/ECR` will provision necessary ECR's for the project.
- `/pipeline_live_data` will provision resources for the live data pipeline.
- `/pipeline_archived_data` will provision resources for the archived data pipeline.
- `/dashboard` will provision resources for the dashboard.

## Set Up

Order to run terraform apply:
1. `/ECR`
2. `/pipeline_live_data`
3. `/pipeline_archived_data`
4. `/dashboard`

## To Do

Make a bash script to run apply in all folders to create all resources.