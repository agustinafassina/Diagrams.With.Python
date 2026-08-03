import json
from pathlib import Path
from diagrams import Diagram, Cluster, Node
from diagrams.aws.compute import EC2, ECS, Lambda, AutoScaling
from diagrams.aws.network import ELB, Route53, APIGateway
from diagrams.aws.database import RDS
from diagrams.aws.security import IAMRole, WAF
from diagrams.aws.management import Cloudwatch
from diagrams.aws.storage import S3
from diagrams.onprem.container import Docker

here = Path(__file__).resolve().parent
with open(here / "config.json") as f:
    config = json.load(f)

region_name = config['region']
components = config['components']
roles = components['roles']
security_groups = components['security_groups']
file_name = str(here / "with-dockers-diagram")

with Diagram(file_name, show=True):
    with Cluster(f"Region: {region_name}"):
        vpc = Cluster("VPC")
        with vpc:
            route53 = Route53(components['route53'])
            gateway = APIGateway(components['api_gateway'])
            lambda_name = Lambda(components['lambda_name'])
            load_balancer = ELB(components['load_balancer'])
            ecs_service = ECS(components['ecs_service'])
            ec2_instance = EC2(components['ec2_instance'])
            database = RDS(components['database'])
            cloudwatch = Cloudwatch(components['cloudwatch'])
            ec2_role = IAMRole(roles['ec2_role'])
            ecs_role = IAMRole(roles['ecs_role'])
            rds_sg = Node(security_groups['rds_sg'])
            ec2_sg = Node(security_groups['ec2_sg'])
            lambda_logs = Cloudwatch("Lambda Logs")
            gateway_logs = Cloudwatch("API Gateway Logs")
            auto_scaling = AutoScaling("Auto Scaling Group")
            waf = WAF(components.get('waf', 'WAF'))
            s3_bucket_ec2 = S3(components.get('s3_bucket_ec2', 'S3 Bucket'))
            s3_bucket_backup = S3(components.get('s3_bucket_backup', 'S3 Bucket'))
            docker_one = Docker("Docker1")
            docker_one_logs = Cloudwatch("Docker log1")
            docker_two = Docker("Docker2")
            docker_two_logs = Cloudwatch("Docker log2")
            docker_three = Docker("Docker3")
            docker_three_logs = Cloudwatch("Docker log3")

            route53 >> gateway
            gateway >> gateway_logs
            gateway >> lambda_name
            lambda_name >> lambda_logs
            gateway >> load_balancer
            load_balancer >> waf
            load_balancer >> ecs_service
            ecs_service >> ec2_instance
            ec2_instance >> auto_scaling
            ec2_instance >> database
            ec2_instance >> ec2_role
            ecs_service >> ecs_role
            database >> rds_sg
            ec2_instance >> ec2_sg
            ec2_instance >> s3_bucket_ec2
            database >> cloudwatch
            database >> s3_bucket_backup

            ecs_service >> docker_one
            docker_one >> docker_one_logs
            ecs_service >> docker_two
            docker_two >> docker_two_logs
            ecs_service >> docker_three
            docker_three >> docker_three_logs