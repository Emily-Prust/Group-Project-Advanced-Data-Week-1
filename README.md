# LNHM Plant Health Monitoring | Group Project

## Summary

Liverpool Natural History Museum has an array of sensors setup to monitor the health of a plant, configured with a single API endpoint that reports the current health of a plant.
The outcome is for the museum to be able to monitor the health of the plants over time and to be able to alert the gardeners when there is a problem.
The data will need to be stored in long term storage, and be queryable to create visualisations and alerts.

## Deliverables

- A full E.T.L data pipeline, hosted in the cloud on AWS.
- An RDS that can store the full data for the past 24 hours
- An S3 bucket for storing data older than 24 hours
- A streamlit dashboard for both real-time and historical visualisations of the data.

## Setup

1) To setup the project, navigate to `/terraform` and follow the steps in the README.
2) Navigate to `/database` and follow the steps in the README to create the schema.
3) Navigate to `/pipeline_live_data` and follow the steps in the README to setup the live data pipeline.
4) Navigate to `/pipeline_archived_data` and follow the steps in the README to setup the archived data pipeline.
5) Finally, navigate to `/dashboard` and follow the steps in the README to setup the streamlit dashboard.

## Architecture 

#### System Architecture Diagram
![Architecture Diagram](https://raw.githubusercontent.com/rafsandwich/Group-Project-Advanced-Data-Week-1/main/architecture/Architecture_Diagram.png)

#### Entity Relationship Diagram
![ERD](https://raw.githubusercontent.com/rafsandwich/Group-Project-Advanced-Data-Week-1/refs/heads/main/architecture/ERD_Diagram.png)

Note: these are stored in `/architecture`.
  
## Roles

| Member    | Role                            |
|-----------|---------------------------------|
| Tom       | Data Engineer, Architect        |
| Ibrahim   | Data Engineer, Architect        |
| Emily     | Data Engineer, Quality Assurance|
| Raphael   | Data Engineer, Project Manager  |

## Technology

- Python - boto3, pandas, pyodbc, streamlit, pylint, pytest
- AWS - ECR, ECS, S3, Step Functions, EventBridge, SNS, Lambda Functions, RDS,
- Docker
- Terraform
- Microsoft SQL Server
- Streamlit
- CI/CD
