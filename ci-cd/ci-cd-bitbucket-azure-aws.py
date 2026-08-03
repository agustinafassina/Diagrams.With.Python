from pathlib import Path
from diagrams import Diagram, Cluster, Edge, Node
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

full_name = str(Path(__file__).resolve().parents[1] / "examples" / "ci-cd-bitbucket-azure-aws")

graph_attr = {"splines": "ortho", "nodesep": "0.55", "ranksep": "0.70"}

with Diagram(full_name, show=False, direction="LR", graph_attr=graph_attr):
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
        release = Pipelines("Release\n(triggered by build)")
        docgen = Node("Scripts\ndocs from infra")
        scan = Inspector("Image scan\n& reports")
        mail = SES("Email\n(scan reports)")
        s3_docs = S3("S3\n(docs / artifacts)")

        release >> docgen >> s3_docs
        release >> scan >> mail
        registry >> scan

    bitbucket >> build >> release

    with Cluster("QA — develop"):
        qa_tf = Terraform("terraform apply\n(QA)")
        with Cluster("AWS QA"):
            qa_alb = ELB("ALB")
            qa_ecs_svc = ElasticContainerServiceService("ECS service")
            qa_ecs = ECS("ECS cluster")
            qa_asg = EC2AutoScaling("Auto Scaling")
            qa_lt = Node("Launch\ntemplate")
            qa_ec2 = EC2("EC2")
            qa_cw = Cloudwatch("CloudWatch")

            qa_alb >> qa_ecs_svc >> qa_ecs
            qa_ecs_svc >> registry
            qa_lt >> qa_asg >> qa_ec2
            qa_ecs_svc >> qa_cw

        qa_tf >> qa_ecs_svc
        qa_tf >> qa_asg

    with Cluster("Prod — master"):
        prod_tf = Terraform("terraform apply\n(Prod)")
        with Cluster("AWS Prod"):
            prod_alb = ELB("ALB")
            prod_ecs_svc = ElasticContainerServiceService("ECS service")
            prod_ecs = ECS("ECS cluster")
            prod_asg = EC2AutoScaling("Auto Scaling")
            prod_lt = Node("Launch\ntemplate")
            prod_ec2 = EC2("EC2")
            prod_cw = Cloudwatch("CloudWatch")

            prod_alb >> prod_ecs_svc >> prod_ecs
            prod_ecs_svc >> registry
            prod_lt >> prod_asg >> prod_ec2
            prod_ecs_svc >> prod_cw

        prod_tf >> prod_ecs_svc
        prod_tf >> prod_asg

    release >> Edge(label="develop") >> qa_tf
    release >> Edge(label="master") >> prod_tf
