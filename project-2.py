from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.network import VPC
from diagrams.aws.database import RDS

folder_name = "project-2"
file_name = "project-2"
full_name = f"{folder_name}/{file_name}"

with Diagram(full_name, show=True):
    with Cluster("Region: us-east-1"):

        vpc = VPC("VPC")
        ec2_instance = EC2("EC2 Instance")
        database = RDS("Database")

        # Connections
        vpc >> ec2_instance
        ec2_instance >> database