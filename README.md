# Diagrams with Python

**[English](#english)** · **[Español](#español)**

---

## English

Collection of infrastructure diagrams built as code with [Diagrams](https://diagrams.mingrammer.com/) (Python). The idea is to keep visuals reproducible and aligned with what you define in tools like Terraform, so documentation stays clear and easy to refresh.

### Diagram examples

<div align="left">
    <img src="examples/project-4.png" alt="AWS diagram example (project-4)" width="400" height="400">
    <img src="examples/project-json.png" alt="AWS diagram from JSON config" width="400" height="400">
</div>

### Repository layout

| Path | Description |
|------|-------------|
| `requirements.txt` | Pinned Python dependency (`diagrams`) |
| `config.json` | Labels and region used by `json-read.py` |
| `diagram-terra.py` | Larger AWS / Azure DevOps style diagram |
| `ci-cd-bitbucket-azure-aws.py` | Bitbucket → Azure DevOps (build + release) → AWS (ECR, Terraform, ECS, scans, email) |
| `json-read.py` | Diagram driven by `config.json` |
| `project-2.py` … `project-5.py` | Sample AWS topologies |
| `rds-ec2.py` | Small RDS + EC2 example |
| `examples/` | Generated PNG outputs (paths used by the scripts) |
| `big-diagram/` | Extended diagram (`with-gateway.py`, local `config.json`) |
| `ec2-backup-with-s3/` | EC2 backup flow with S3 |
| `ecs-fargate/` | ECS Fargate example |
| `with-docker/` | Docker-related diagram |

### Prerequisites

- Python 3.x  
- [Graphviz](https://graphviz.org/download/) installed on the system (required by Diagrams). On Windows, the installer often leaves `dot` off your `PATH`; add `C:\Program Files\Graphviz\bin` to the user **PATH** and open a new terminal, or run once per session in PowerShell: `$env:Path = "C:\Program Files\Graphviz\bin;" + $env:Path`  
- Python dependencies (pinned in `requirements.txt`):

```bash
pip install -r requirements.txt
```

A virtual environment (for example `.venv`) is recommended.

### How to run

From the repository root:

```bash
python project-4.py
# Writes: examples/project-4.png
```

Other entry points work the same way (`json-read.py`, `diagram-terra.py`, scripts under subfolders, etc.). Output paths are defined inside each script (usually under `examples/`).

### Tips

- In `Diagram(...)`, `show=True` opens the image with the default viewer after generation; use `show=False` to only write the file.
- Official node and layout reference: [Diagrams documentation](https://diagrams.mingrammer.com/docs/nodes/aws).

**Version:** 0.2.0

---

## Español

Conjunto de diagramas de infraestructura definidos como código con [Diagrams](https://diagrams.mingrammer.com/) en Python. El objetivo es que los gráficos sean reproducibles y coherentes con lo que definís en Terraform (u otras fuentes), para documentar de forma clara y actualizable.

### Ejemplos de diagramas

<div align="left">
    <img src="examples/project-4.png" alt="Ejemplo de diagrama AWS (project-4)" width="400" height="400">
    <img src="examples/project-json.png" alt="Diagrama AWS desde JSON" width="400" height="400">
</div>

### Estructura del repositorio

| Ruta | Descripción |
|------|-------------|
| `requirements.txt` | Dependencia Python fijada (`diagrams`) |
| `config.json` | Textos y región usados por `json-read.py` |
| `diagram-terra.py` | Diagrama amplio con enfoque AWS / Azure DevOps |
| `ci-cd-bitbucket-azure-aws.py` | Bitbucket → Azure DevOps (build + release) → AWS (ECR, Terraform, ECS, escaneos, email) |
| `json-read.py` | Diagrama generado a partir de `config.json` |
| `project-2.py` … `project-5.py` | Ejemplos de topologías AWS |
| `rds-ec2.py` | Ejemplo pequeño RDS + EC2 |
| `examples/` | PNG generados (rutas que usan los scripts) |
| `big-diagram/` | Diagrama extendido (`with-gateway.py`, `config.json` local) |
| `ec2-backup-with-s3/` | Flujo de backup EC2 con S3 |
| `ecs-fargate/` | Ejemplo con ECS Fargate |
| `with-docker/` | Diagrama relacionado con Docker |

### Requisitos

- Python 3.x  
- [Graphviz](https://graphviz.org/download/) instalado en el sistema (lo exige la librería Diagrams). En Windows, si aparece `ExecutableNotFound: failed to execute WindowsPath('dot')`, agregá `C:\Program Files\Graphviz\bin` al **PATH** del usuario y abrí una terminal nueva, o en PowerShell por sesión: `$env:Path = "C:\Program Files\Graphviz\bin;" + $env:Path`  
- Dependencias de Python (versiones fijadas en `requirements.txt`):

```bash
pip install -r requirements.txt
```

Se recomienda un entorno virtual (por ejemplo `.venv`).

### Cómo ejecutar

Desde la raíz del repositorio:

```bash
python project-4.py
# Genera: examples/project-4.png
```

El resto de scripts se ejecuta de la misma forma (`json-read.py`, `diagram-terra.py`, los de las subcarpetas, etc.). La ruta de salida está en cada script (normalmente bajo `examples/`).

### Comentarios y recomendaciones

- En `Diagram(...)`, `show=True` abre la imagen con el visor predeterminado al terminar; con `show=False` solo se guarda el archivo.
- Documentación oficial de nodos y diseño: [Diagrams (AWS)](https://diagrams.mingrammer.com/docs/nodes/aws).

**Versión:** 0.2.0
