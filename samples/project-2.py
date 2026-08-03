from pathlib import Path
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.network import VPC
from diagrams.aws.database import RDS

full_name = str(Path(__file__).resolve().parents[1] / "examples" / "project-2")

with Diagram(full_name, show=True):
    with Cluster("Region: us-east-1"):

        vpc = VPC("VPC")
        ec2_instance = EC2("EC2 Instance")
        database = RDS("Database")

        # Connections
        vpc >> ec2_instance
        ec2_instance >> database