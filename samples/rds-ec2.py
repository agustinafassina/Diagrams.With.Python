from pathlib import Path
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS

full_name = str(Path(__file__).resolve().parents[1] / "examples" / "rds-ec2")

with Diagram(full_name, show=True):
    with Cluster("AWS"):
        ec2_instance = EC2("EC2 Instance")
        database = RDS("Database")
        ec2_instance >> database