from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, ECS
from diagrams.aws.network import ELB, Route53
from diagrams.aws.database import RDS

with Diagram("project-3", show=True):
    with Cluster("Region: us-east-1"):
        vpc = Cluster("VPC")

        with vpc:
            route53 = Route53("Route 53")
            load_balancer = ELB("Load Balancer")
            ecs_service = ECS("ECS Service")
            ec2_instance = EC2("EC2 Instance")
            database = RDS("Database")

            # Connections
            route53 >> load_balancer
            load_balancer >> ecs_service
            ecs_service >> ec2_instance
            ec2_instance >> database