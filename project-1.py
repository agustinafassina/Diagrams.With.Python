from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS

with Diagram("project-1", show=True):
    with Cluster("AWS"):
        ec2_instance = EC2("EC2 Instance")
        database = RDS("Database")
        ec2_instance >> database