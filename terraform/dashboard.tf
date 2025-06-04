# ECR Repository for dashboard image

resource "aws_ecr_repository" "dashboard-td-image-repo" {
  name                 = "c17-allum-ecr-dashboard-terraform"
  image_tag_mutability = "MUTABLE"

  encryption_configuration {
    encryption_type = "AES256"
  }
}

# Image for dashboard to run

data "aws_ecr_image" "dashboard-td-image-version" {
  repository_name = aws_ecr_repository.dashboard-td-image-repo
  image_tag       = "latest"
}

# ECS Cluster

data "aws_ecs_cluster" "ecs-cluster" {
  cluster_name = "c17-ecs-cluster"
}

# Dashboard Task Definition

resource "aws_ecs_task_definition" "dashboard-task" {
  family                   = "c17-allum-td-dashboard"
  requires_compatibilities = ["FARGATE"]
  network_mode             = "awsvpc"
  cpu                      = "256"
  memory                   = "512"

  container_definitions = jsonencode([
    {
      name      = "dashboard"
      image     = data.aws_ecr_image.dashboard-td-image-version
      cpu       = 256
      memory    = 512
      essential = true

      portMappings = [
        {
          containerPort = 8501
          hostPort      = 8501
        }
      ]
      
    }
  ])
}