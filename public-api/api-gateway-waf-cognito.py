from pathlib import Path
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.general import User
from diagrams.aws.security import WAF, Cognito
from diagrams.aws.network import APIGateway
from diagrams.aws.compute import Lambda, ECS, ElasticContainerServiceService
from diagrams.aws.database import RDS

full_name = str(Path(__file__).resolve().parents[1] / "examples" / "public-api")

with Diagram(full_name, show=False, direction="LR"):
    clients = User("Clients\n(apps / partners)")

    with Cluster("Edge"):
        waf = WAF("WAF")
        apigw = APIGateway("API Gateway")
        cognito = Cognito("Cognito\n(JWT / authorizer)")
        waf >> apigw
        cognito >> Edge(label="authorize") >> apigw

    with Cluster("Compute"):
        fn = Lambda("Lambda\n(lightweight routes)")
        svc = ElasticContainerServiceService("ECS service\n(core API)")
        ecs = ECS("ECS cluster")
        svc >> ecs

    with Cluster("Data"):
        rds = RDS("RDS")

    clients >> waf
    apigw >> Edge(label="/v1/light") >> fn
    apigw >> Edge(label="/v1/core") >> svc
    fn >> rds
    svc >> rds
