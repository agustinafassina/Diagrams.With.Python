from pathlib import Path
from diagrams.onprem.vcs import Git
from diagrams.onprem.iac import Terraform
from diagrams.azure.devops import Pipelines
from diagrams.aws.storage import S3
from diagrams.aws.database import Dynamodb
from diagrams.aws.management import OrganizationsAccount
from diagrams import Diagram, Cluster, Edge, Node

full_name = str(Path(__file__).resolve().parents[1] / "examples" / "gitops-terraform")

with Diagram(full_name, show=False, direction="LR"):
    # Bitbucket has no icon; Git + label is the stand-in used elsewhere in this repo.
    bitbucket = Git("Bitbucket\n(IaC repo)")

    with Cluster("CI/CD"):
        pipeline = Pipelines("Azure DevOps\npipeline")
        tf_plan = Terraform("terraform plan")
        tf_apply = Terraform("terraform apply")
        pipeline >> tf_plan >> tf_apply

    with Cluster("Remote state"):
        state = S3("S3\n(tfstate)")
        lock = Dynamodb("DynamoDB\n(state lock)")
        state >> Edge(label="lock", style="dashed") >> lock

    with Cluster("Target accounts"):
        qa = OrganizationsAccount("qa")
        prod = OrganizationsAccount("prod")
        note = Node("Resources created\nby Terraform")

    bitbucket >> pipeline
    tf_plan >> Edge(label="read/write state") >> state
    tf_apply >> Edge(label="read/write state") >> state
    tf_apply >> Edge(label="develop → qa") >> qa
    tf_apply >> Edge(label="master → prod") >> prod
    qa >> note
    prod >> note