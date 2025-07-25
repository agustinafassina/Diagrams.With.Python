from diagrams import Diagram, Cluster, Node
from diagrams.aws.compute import EC2, ECS
from diagrams.aws.network import ELB, Route53
from diagrams.aws.database import RDS
from diagrams.aws.security import IAMRole, ACM
from diagrams.aws.management import Cloudwatch
from diagrams.aws.engagement import SES

with Diagram("project-5", show=True):
    with Cluster("Region: us-east-1"):
        vpc = Cluster("VPC")
        with vpc:
            route53 = Route53("Route 53")
            load_balancer = ELB("Load Balancer")
            ecs_service = ECS("ECS Service")
            ec2_instance = EC2("EC2 Instance")
            database = RDS("Database")
            cloudwatch = Cloudwatch("CloudWatch")

            # IAM roles
            ec2_role = IAMRole("EC2 Role")
            ecs_role = IAMRole("ECS Role")

            # Security Groups
            rds_sg = Node("Security Group")
            ec2_sg = Node("Security Group")
            ecs_sg = Node("Security Group")

            # Relationships
            route53 >> load_balancer
            load_balancer >> ecs_service
            load_balancer >> ACM("Certificate Manager")
            ecs_service >> ec2_instance
            ec2_instance >> database

            # Associating IAM roles and security groups
            ec2_instance >> ec2_role
            ecs_service >> ecs_role
            database >> rds_sg
            ec2_instance >> ec2_sg
            ecs_service >> ecs_sg

            # Monitoring
            database >> cloudwatch
            ses = SES("SES Email")
            cloudwatch >> ses