"""
CI/CD: Bitbucket → Azure DevOps (build + release) → AWS.
Build: Docker image to ECR; Terraform in pipeline. Release: branch → QA/Prod,
terraform apply, infra docs, image scan reports, email (SES).
"""
from diagrams import Diagram, Cluster, Node
from diagrams.onprem.vcs import Git
from diagrams.onprem.container import Docker
from diagrams.onprem.iac import Terraform
from diagrams.azure.devops import Pipelines
from diagrams.aws.compute import ECR, ECS, EC2, ElasticContainerServiceService, EC2AutoScaling
from diagrams.aws.storage import S3
from diagrams.aws.network import ELB
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import Inspector
from diagrams.aws.engagement import SES

folder_name = "examples"
file_name = "ci-cd-bitbucket-azure-aws"
full_name = f"{folder_name}/{file_name}"

with Diagram(full_name, show=False, direction="LR"):
    # Bitbucket has no icon in this library; Git icon + label is a common stand-in.
    bitbucket = Git("Bitbucket")

    with Cluster("Azure DevOps — Build"):
        build = Pipelines("CI pipeline")
        docker = Docker("docker build")
        tf_ci = Terraform("Terraform (IaC)")
        build >> docker
        build >> tf_ci

    registry = ECR("Amazon ECR")
    docker >> registry

    with Cluster("Azure DevOps — Release"):
        release = Pipelines("Release (triggered by build)")
        branch_env = Node("Branch → environment\ndevelop → QA\nmaster → Prod")
        tf_cd = Terraform("terraform apply")
        docgen = Node("Scripts\ndocumentation\nfrom infra")
        scan = Inspector("Image scan\n& reports")
        mail = SES("Email\n(scan reports)")

        release >> branch_env >> tf_cd
        release >> docgen
        release >> scan >> mail

    bitbucket >> build
    build >> release
    registry >> scan

    with Cluster("AWS (runtime)"):
        alb = ELB("Load balancer")
        ecs_svc = ElasticContainerServiceService("ECS service")
        ecs_cluster = ECS("ECS cluster")
        asg = EC2AutoScaling("Auto Scaling")
        lt = Node("Launch\ntemplate")
        ec2 = EC2("EC2")
        cw = Cloudwatch("CloudWatch")
        s3_docs = S3("S3 (docs / artifacts)")

        alb >> ecs_svc >> ecs_cluster
        ecs_svc >> registry
        asg >> ec2
        lt >> asg
        ecs_svc >> cw

    tf_cd >> ecs_svc
    tf_cd >> asg
    docgen >> s3_docs
