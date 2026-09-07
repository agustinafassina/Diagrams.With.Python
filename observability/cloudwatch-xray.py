from pathlib import Path
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import ECS, ElasticContainerServiceService
from diagrams.aws.network import ELB
from diagrams.aws.management import Cloudwatch, CloudwatchAlarm, CloudwatchLogs
from diagrams.aws.devtools import XRay
from diagrams.aws.integration import SNS
from diagrams.aws.engagement import SES
from diagrams.aws.general import User

full_name = str(Path(__file__).resolve().parents[1] / "examples" / "observability")

with Diagram(full_name, show=False, direction="LR"):
    users = User("Operators")

    with Cluster("Workload"):
        alb = ELB("ALB")
        svc = ElasticContainerServiceService("ECS service")
        ecs = ECS("ECS cluster")
        alb >> svc >> ecs

    with Cluster("Telemetry"):
        logs = CloudwatchLogs("Log groups")
        metrics = Cloudwatch("Metrics")
        xray = XRay("X-Ray\n(tracing)")
        dash = Cloudwatch("Dashboard")

    with Cluster("Alerting"):
        alarm = CloudwatchAlarm("Alarms\n(CPU, 5xx, latency)")
        sns = SNS("SNS topic")
        mail = SES("Email\n(notifications)")

    svc >> logs
    svc >> metrics
    svc >> xray
    logs >> dash
    metrics >> dash
    xray >> dash

    metrics >> alarm
    logs >> Edge(label="metric filters", style="dashed") >> alarm
    alarm >> sns >> mail
    dash >> users
    mail >> users
