from pathlib import Path
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.network import VPC, InternetGateway, NATGateway, PublicSubnet, PrivateSubnet, ELB
from diagrams.aws.compute import ECS, ElasticContainerServiceService
from diagrams.aws.database import RDS

full_name = str(Path(__file__).resolve().parents[1] / "examples" / "networking-vpc")

with Diagram(full_name, show=False, direction="TB"):
    igw = InternetGateway("Internet Gateway")

    with Cluster("VPC 10.0.0.0/16"):
        with Cluster("Public subnets"):
            pub_a = PublicSubnet("public-a\n10.0.0.0/24")
            pub_b = PublicSubnet("public-b\n10.0.1.0/24")
            alb = ELB("Application\nLoad Balancer")
            nat = NATGateway("NAT Gateway")
            pub_a >> alb
            pub_b >> alb
            pub_a >> nat

        with Cluster("Private subnets — app"):
            priv_app_a = PrivateSubnet("private-app-a\n10.0.10.0/24")
            priv_app_b = PrivateSubnet("private-app-b\n10.0.11.0/24")
            ecs = ECS("ECS cluster")
            svc = ElasticContainerServiceService("ECS service")
            priv_app_a >> svc
            priv_app_b >> svc
            svc >> ecs

        with Cluster("Private subnets — data"):
            priv_db_a = PrivateSubnet("private-db-a\n10.0.20.0/24")
            priv_db_b = PrivateSubnet("private-db-b\n10.0.21.0/24")
            rds = RDS("RDS\n(Multi-AZ)")
            priv_db_a >> rds
            priv_db_b >> rds

    igw >> Edge(label="inbound HTTPS") >> alb
    alb >> Edge(label="to private") >> svc
    svc >> Edge(label="SQL") >> rds
    nat >> Edge(label="egress\n(updates, ECR)", style="dashed") >> igw
    svc >> Edge(label="via NAT", style="dashed") >> nat