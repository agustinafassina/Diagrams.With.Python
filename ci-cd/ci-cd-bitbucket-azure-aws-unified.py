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
from diagrams.onprem.security import Trivy
from diagrams.saas.security import Sonarqube

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

    # The trigger runs a Bitbucket pipeline with the scan tests; only if it passes
    # does the flow continue to the deploy.
    with Cluster("Bitbucket Pipelines — Scan tests"):
        bb_pipeline = Git("bitbucket-pipelines.yml\n(custom: scan-tests)")
        sast = Sonarqube("SAST / code quality")
        image_scan = Trivy("Image & IaC scan")
        gate = Node(
            "Quality gate\n\nscans OK?",
            **{**trigger_attrs, "fillcolor": "#E3F6E5", "color": "#2E9E44"},
        )
        blocked = Node(
            "Deploy blocked\n(notify team)",
            shape="box",
            style="rounded,filled",
            fillcolor="#FDE2E1",
            color="#D93025",
            fixedsize="false",
            labelloc="c",
            fontsize="12",
        )

        bb_pipeline >> sast >> gate
        bb_pipeline >> image_scan >> gate
        registry >> Edge(style="dashed") >> image_scan
        gate >> Edge(xlabel="fail", fontcolor="#D93025", color="#D93025") >> blocked

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

    # xlabel: with splines=ortho, regular edge labels drift away from their edge.
    trigger >> Edge(xlabel="run scans\n(env = qa | prod)", fontcolor="#B08400", style="bold", color="#E0A800") >> bb_pipeline
    gate >> Edge(xlabel="pass", fontcolor="#2E9E44", style="bold", color="#2E9E44") >> env_tf
