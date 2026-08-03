from pathlib import Path
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import Route53, ELB
from diagrams.aws.compute import ECS, ElasticContainerServiceService
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.aws.management import Cloudwatch

full_name = str(Path(__file__).resolve().parents[1] / "examples" / "multi-region-dr")

with Diagram(full_name, show=False, direction="TB"):
    dns = Route53("Route 53\nhealth checks\n+ failover")

    with Cluster("Primary — us-east-1 (active)"):
        with Cluster("VPC primary"):
            p_alb = ELB("ALB")
            p_svc = ElasticContainerServiceService("ECS service")
            p_ecs = ECS("ECS cluster")
            p_rds = RDS("RDS primary")
            p_s3 = S3("S3")
            p_cw = Cloudwatch("CloudWatch")

            p_alb >> p_svc >> p_ecs
            p_svc >> p_rds
            p_svc >> p_cw
            p_svc >> p_s3

    with Cluster("DR — sa-east-1 (standby)"):
        with Cluster("VPC DR"):
            d_alb = ELB("ALB")
            d_svc = ElasticContainerServiceService("ECS service")
            d_ecs = ECS("ECS cluster")
            d_rds = RDS("RDS replica")
            d_s3 = S3("S3 replica")
            d_cw = Cloudwatch("CloudWatch")

            d_alb >> d_svc >> d_ecs
            d_svc >> d_rds
            d_svc >> d_cw
            d_svc >> d_s3

    dns >> Edge(label="active", color="#2F9E44") >> p_alb
    dns >> Edge(label="failover", color="#E03131", style="dashed") >> d_alb

    p_rds >> Edge(label="async replication", style="dashed") >> d_rds
    p_s3 >> Edge(label="CRR", style="dashed") >> d_s3
    p_cw >> Edge(label="alarms → failover", style="dashed") >> dns
