import json
from diagrams import Diagram, Cluster
from diagrams.aws.network import VPC, ELB, Route53, InternetGateway
from diagrams.aws.compute import EC2, ECS, EC2AutoScaling, ElasticContainerServiceService, EC2Ami
from diagrams.aws.management import Cloudwatch
from diagrams.aws.compute import ECR
from diagrams.aws.security import IAMRole, ACM
from diagrams.aws.engagement import SES
from diagrams.azure.devops import Pipelines

# Variables
vpc_name = "Vpc"
region_name = "California"
ec2_name = "im-89adsjkasjdk89123kj"
ami_id = "ami-1234567890abcdef0"
ec2_role_name = "ec2 rolee"
ecs_role_name = "ecs rolee"
ecs_name = "ECS name"
certificate_arn = "SSL"
profile = "examples/diagram-terra"
ecs_services = ["ecs-cluster-ui", "ecs-service-api", "ecs-service-api-2"]

with Diagram(profile, show=False, direction="TB"):
    pipelines = Pipelines("Azure DevOps Pipelines")
    with Cluster("Region: " + region_name):
        vpc = VPC(vpc_name)

        # EC2
        ec2 = EC2(ec2_name)
        vpc >> ec2

        autoscaling = EC2AutoScaling("Auto scaling")
        ec2 >> autoscaling

        ses = SES("SES Email")
        ses >> autoscaling

        ami = EC2Ami(ami_id)
        ec2 >> ami

        # Ec2 rle
        role = IAMRole(ec2_role_name)
        role >> ec2

        # ECS
        ecs = ECS(ecs_name)
        ec2 >> ecs
        role_ecs = IAMRole(ec2_role_name)
        role_ecs >> ecs

        # Load balancer and Ecs
        alb = ELB("Application Load Balancer")
        alb >> ecs
        alb >> ACM(certificate_arn)

        # APi Gateway
        gateway = InternetGateway("Gateway")
        gateway >> alb


        for service in ecs_services:
            nombre_servicio = service['name']
            cloudwatch_name = service['cloudwatch']['name']
            ecr_images = [img['name'] for img in service['ecr']['images']]

            if nombre_servicio != 'ecs-cluster':
                    with Cluster(nombre_servicio):
                        service = ElasticContainerServiceService(nombre_servicio)
                        ecs >> service
                        # CloudWatch Log Group
                        cw = Cloudwatch(cloudwatch_name)
                        service >> cw
                        # ECR Repo(s)
                        for repo_name in ecr_images:
                            ecr = ECR(repo_name)
                            service >> ecr
