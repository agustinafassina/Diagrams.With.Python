from diagrams import Diagram, Cluster, Node
from diagrams.aws.compute import ECS, ECR, Fargate
from diagrams.aws.network import VPC
from diagrams.onprem.container import Docker
from diagrams.aws.management import Cloudwatch

file_name = "diagram"

with Diagram(file_name, show=True):
    with Cluster("Region: us-west-1"):

        vpc = VPC("VPC")
        ecs_cluster = ECS("Ecs cluster")
        fargate = Fargate("Fargate Service")
        task_def = Node("Task definition")
        ecr = ECR("Docker image repository")
        docker = Docker("docker-image:latest")
        cw = Cloudwatch("tf-dev-app-logs")

        # Connections
        vpc >> ecs_cluster
        ecs_cluster >> fargate
        fargate >> task_def
        task_def >> docker
        task_def >> cw
        docker >> ecr