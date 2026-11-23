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

# Same pipeline as ci-cd-bitbucket-azure-aws.py, but QA and Prod are drawn as a single
# environment: the branch only decides WHICH environment gets deployed, via a trigger.
full_name = str(Path(__file__).resolve().parents[1] / "examples" / "ci-cd-bitbucket-azure-aws-unified")

graph_attr = {"splines": "ortho", "nodesep": "0.55", "ranksep": "0.70"}

trigger_attrs = {
    "shape": "diamond",
    "style": "filled",
    "fillcolor": "#FFF4D6",
    "color": "#E0A800",
    "fixedsize": "false",
    "labelloc": "c",
    "width": "2.2",
    "height": "1.4",
    "fontsize": "12",
}

with Diagram("CI/CD — Bitbucket → Azure DevOps → AWS (unified env)", filename=full_name, show=False, direction="LR", graph_attr=graph_attr):
    # Bitbucket has no icon in this library; Git icon + label is a common stand-in.
    bitbucket = Git("Bitbucket\n(develop / master)")

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

        # Branch-based trigger: selects the target environment for the same deploy flow.
        trigger = Node(
            "Branch trigger\n\ndevelop → QA\nmaster → Prod",
            **trigger_attrs,
        )
        release >> trigger

    bitbucket >> build >> release

    with Cluster("Deploy — environment (QA | Prod)"):
        env_tf = Terraform("terraform apply\n(-var-file=<env>.tfvars)")
        with Cluster("AWS <env>"):
            alb = ELB("ALB")
            ecs_svc = ElasticContainerServiceService("ECS service")
            ecs = ECS("ECS cluster")
            asg = EC2AutoScaling("Auto Scaling")
            lt = Node("Launch\ntemplate")
            ec2 = EC2("EC2")
            cw = Cloudwatch("CloudWatch")

            alb >> ecs_svc >> ecs
            ecs_svc >> registry
            lt >> asg >> ec2
            ecs_svc >> cw

        env_tf >> ecs_svc
        env_tf >> asg

    trigger >> Edge(label="env = qa | prod", style="bold", color="#E0A800") >> env_tf
