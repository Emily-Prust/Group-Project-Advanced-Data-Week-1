provider "aws" {
  region     = var.REGION
  access_key = var.ACCESS_KEY
  secret_key = var.SECRET_KEY
}

# ECR Repository for dashboard image

data "aws_ecr_repository" "dashboard-td-image-repo" {
  name = "c17-allum-ecr-dashboard-terraform"
}

# Image for dashboard to run

data "aws_ecr_image" "dashboard-td-image-version" {
  repository_name = data.aws_ecr_repository.dashboard-td-image-repo.name
  image_tag       = "latest"
}

# ECS Cluster

data "aws_ecs_cluster" "ecs-cluster" {
  cluster_name = "c17-ecs-cluster"
}

# Log group

resource "aws_cloudwatch_log_group" "dashboard-log-group" {
  name = "/ecs/c17-allum-dashboard"
}

# S3 bucket

data "aws_s3_bucket" "archived-s3" {
  bucket = "c17-allum-s3-archived-data"
}

# S3 Permissions for ECS

resource "aws_iam_role" "ecs-task-role" {
  name = "c17-allum-ecs-task-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_policy" "s3-access-policy" {
  name        = "c17-allum-s3-access-policy"
  description = "Allow ECS tasks to read from S3."

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket"
        ]
        Resource = [
          "arn:aws:s3:::c17-allum-s3-archived-data",
          "arn:aws:s3:::c17-allum-s3-archived-data/*"
        ]
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_s3_access" {
  role       = aws_iam_role.ecs-task-role.name
  policy_arn = aws_iam_policy.s3-access-policy.arn
}

# Execution Role

resource "aws_iam_role" "ecs-execution-role" {
  name = "c17-allum-ecs-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Principal = {
          Service = "ecs-tasks.amazonaws.com"
        },
        Action = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "ecs_execution_policy" {
  role       = aws_iam_role.ecs-execution-role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"
}


# Dashboard Task Definition
# TODO: add environment variables to task definition

resource "aws_ecs_task_definition" "dashboard-task" {
  family                   = "c17-allum-td-dashboard"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "512"
  task_role_arn            = aws_iam_role.ecs-task-role.arn
  execution_role_arn       = aws_iam_role.ecs-execution-role.arn

  container_definitions = jsonencode([
    {
      name      = "dashboard"
      image     = data.aws_ecr_image.dashboard-td-image-version.image_uri
      cpu       = 256
      memory    = 512
      essential = true

      portMappings = [
        {
          containerPort = 8501
          hostPort      = 8501
        }
      ]

      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = aws_cloudwatch_log_group.dashboard-log-group.name
          awslogs-region        = var.REGION
          awslogs-stream-prefix = "ecs"
        }
      }
      # Add env variables
    }
  ])
}

# VPC and subnets

data "aws_vpc" "c17-vpc" {
  id = var.VPC_ID
}

data "aws_subnet" "public-subnet-1" {
  id = var.SUBNET_ID_1
}

data "aws_subnet" "public-subnet-2" {
  id = var.SUBNET_ID_2
}

data "aws_subnet" "public-subnet-3" {
  id = var.SUBNET_ID_3
}

# ECS Service

resource "aws_ecs_service" "dashboard-service" {
  name             = "c17-allum-ecs-service-dashboard"
  cluster          = data.aws_ecs_cluster.ecs-cluster.id
  task_definition  = aws_ecs_task_definition.dashboard-task.arn
  desired_count    = 1
  launch_type      = "FARGATE"
  platform_version = "LATEST"

  network_configuration {
    subnets          = [data.aws_subnet.public-subnet-1.id, data.aws_subnet.public-subnet-2.id, data.aws_subnet.public-subnet-3.id]
    security_groups  = [aws_security_group.dashboard-sg.id]
    assign_public_ip = true
  }
}

resource "aws_security_group" "dashboard-sg" {
  name        = "c17-allum-sg-dashboard"
  description = "Allow HTTP access to dashboard."
  vpc_id      = data.aws_vpc.c17-vpc.id
}

resource "aws_vpc_security_group_ingress_rule" "dashboard-http-ingress" {
  security_group_id = aws_security_group.dashboard-sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 8501
  to_port           = 8501
  ip_protocol       = "tcp"
  description       = "Allow HTTP access from anywhere"
}

resource "aws_vpc_security_group_egress_rule" "dashboard-all-egress" {
  security_group_id = aws_security_group.dashboard-sg.id
  cidr_ipv4         = "0.0.0.0/0"
  from_port         = 0
  to_port           = 0
  ip_protocol       = "-1"
  description       = "Allow all outbound traffic"
}