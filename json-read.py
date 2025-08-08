import json
from diagrams import Diagram, Cluster, Node
from diagrams.aws.compute import EC2, ECS
from diagrams.aws.network import ELB, Route53
from diagrams.aws.database import RDS
from diagrams.aws.security import IAMRole
from diagrams.aws.management import Cloudwatch

with open('config.json') as f:
    config = json.load(f)

region_name = config['region']
components = config['components']
roles = components['roles']
security_groups = components['security_groups']
file_name = "examples/project-json"

with Diagram(file_name, show=True):
    with Cluster(f"Region: {region_name}"):
        vpc = Cluster("VPC")
        with vpc:
            route53 = Route53(components['route53'])
            load_balancer = ELB(components['load_balancer'])
            ecs_service = ECS(components['ecs_service'])
            ec2_instance = EC2(components['ec2_instance'])
            database = RDS(components['database'])
            cloudwatch = Cloudwatch(components['cloudwatch'])
            ec2_role = IAMRole(roles['ec2_role'])
            ecs_role = IAMRole(roles['ecs_role'])
            rds_sg = Node(security_groups['rds_sg'])
            ec2_sg = Node(security_groups['ec2_sg'])

            route53 >> load_balancer
            load_balancer >> ecs_service
            ecs_service >> ec2_instance
            ec2_instance >> database
            ec2_instance >> ec2_role
            ecs_service >> ecs_role
            database >> rds_sg
            ec2_instance >> ec2_sg
            database >> cloudwatch