from pathlib import Path
from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.network import VPC
from diagrams.aws.storage import S3

full_name = str(Path(__file__).resolve().parent / "backup")

with Diagram(full_name, show=True):
    with Cluster("Region: sa-east-1"):

        vpc = VPC("VPC")
        ec2_instance = EC2("MongoDB in EC2 instance")
        s3_bucket_name = S3("Backup S3")

        # Connections
        vpc >> ec2_instance
        ec2_instance >> s3_bucket_name