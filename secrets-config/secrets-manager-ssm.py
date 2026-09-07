from pathlib import Path
from diagrams import Diagram, Cluster, Edge, Node
from diagrams.aws.security import SecretsManager, IAMRole
from diagrams.aws.management import ParameterStore
from diagrams.aws.compute import ECS, ElasticContainerServiceService, ElasticContainerServiceTask
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.onprem.iac import Terraform

full_name = str(Path(__file__).resolve().parents[1] / "examples" / "secrets-config")

with Diagram(full_name, show=False, direction="LR"):
    tf = Terraform("Terraform\n(creates secrets\n+ parameters)")

    with Cluster("Config store"):
        secrets = SecretsManager("Secrets Manager\n(DB password, API keys)")
        params = ParameterStore("SSM Parameter Store\n(/app/env, feature flags)")

    tf >> secrets
    tf >> params

    with Cluster("Compute"):
        role = IAMRole("Task execution\n+ task role")
        task = ElasticContainerServiceTask("Task definition\ninjects secrets/params")
        svc = ElasticContainerServiceService("ECS service")
        ecs = ECS("ECS cluster")
        alb = ELB("ALB")

        role >> task
        task >> svc >> ecs
        alb >> svc

    secrets >> Edge(label="valueFrom") >> task
    params >> Edge(label="valueFrom") >> task

    with Cluster("Data"):
        rds = RDS("RDS")
        note = Node("App reads DSN\nat runtime only")

    svc >> Edge(label="uses secret") >> rds
    rds >> note
