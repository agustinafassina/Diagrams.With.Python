from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS

folder_name = "examples"
file_name = "rds-ec2"
full_name = f"{folder_name}/{file_name}"

with Diagram(full_name, show=True):
    with Cluster("AWS"):
        ec2_instance = EC2("EC2 Instance")
        database = RDS("Database")
        ec2_instance >> database