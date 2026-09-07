from pathlib import Path
from diagrams import Diagram, Cluster, Edge, Node
from diagrams.aws.management import (
    Organizations,
    OrganizationsAccount,
    OrganizationsOrganizationalUnit,
    ControlTower,
)
from diagrams.aws.security import SingleSignOn, IAM

full_name = str(Path(__file__).resolve().parents[1] / "examples" / "landing-zone")

with Diagram(full_name, show=False, direction="TB"):
    sso = SingleSignOn("IAM Identity Center\n(SSO)")
    iam = IAM("IAM / federation")

    with Cluster("AWS Organizations"):
        org = Organizations("Organization")
        ct = ControlTower("Control Tower\n(optional)")
        mgmt = OrganizationsAccount("Management\naccount")

        org >> mgmt
        ct >> org

        with Cluster("OU — Workloads"):
            ou = OrganizationsOrganizationalUnit("Workloads OU")
            scp = Node("SCPs\n(deny risky APIs)")
            ou >> scp

            with Cluster("Accounts"):
                dev = OrganizationsAccount("dev")
                qa = OrganizationsAccount("qa")
                prod = OrganizationsAccount("prod")

            ou >> [dev, qa, prod]

        org >> ou

    sso >> Edge(label="SSO into accounts") >> [dev, qa, prod]
    sso >> iam
    iam >> mgmt