# Jenkins ECR AWS Deployment

## Objective

Automate application deployment using Jenkins,
Docker, GitHub, Amazon ECR and AWS EC2.

## Technology Stack

- Python Flask
- Git and GitHub
- Jenkins
- Docker
- Amazon ECR
- AWS EC2

## Application Port

5000

## Endpoints

/       - Home page
/health - Application health check

## CI/CD Workflow

Developer
    |
GitHub
    |
Jenkins
    |
Build and Test
    |
Docker Image Build
    |
Amazon ECR
    |
AWS EC2 Deployment
    |
Live Application
