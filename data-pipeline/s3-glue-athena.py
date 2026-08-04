from pathlib import Path
from diagrams import Diagram, Cluster, Edge
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Glue, GlueDataCatalog, Athena, Redshift
from diagrams.aws.compute import Lambda
from diagrams.aws.general import User

full_name = str(Path(__file__).resolve().parents[1] / "examples" / "data-pipeline")

with Diagram(full_name, show=False, direction="LR"):
    producers = User("Producers\n(apps / batch jobs)")

    with Cluster("Ingest"):
        raw = S3("S3 raw\n(landing zone)")

    with Cluster("Transform"):
        glue = Glue("AWS Glue\n(ETL jobs)")
        catalog = GlueDataCatalog("Data Catalog")
        fn = Lambda("Lambda\n(light transforms)")
        glue >> catalog
        fn >> catalog

    with Cluster("Serve"):
        curated = S3("S3 curated\n(Parquet)")
        athena = Athena("Athena")
        redshift = Redshift("Redshift\n(optional warehouse)")
        analysts = User("Analysts")

    producers >> raw
    raw >> Edge(label="batch") >> glue
    raw >> Edge(label="event", style="dashed") >> fn
    glue >> curated
    fn >> curated
    curated >> athena
    curated >> Edge(label="COPY", style="dashed") >> redshift
    catalog >> athena
    athena >> analysts
    redshift >> analysts
