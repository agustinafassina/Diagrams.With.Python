from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.network import VPC
from diagrams.aws.storage import S3

folder_name = "ec2-backup-with-s3"
file_name = "backup"
full_name = f"{folder_name}/{file_name}"

with Diagram(full_name, show=True):
    with Cluster("Region: sa-east-1"):

        vpc = VPC("VPC")
        ec2_instance = EC2("MongoDB in EC2 instance")
        s3_bucket_name = S3("Backup S3")

        # Connections
        vpc >> ec2_instance
        ec2_instance >> s3_bucket_name