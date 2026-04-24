# Diagrams with Python

**[English](#english)** · **[Español](#español)**

---

## English

Collection of infrastructure diagrams built as code with [Diagrams](https://diagrams.mingrammer.com/) (Python). The idea is to keep visuals reproducible and aligned with what you define in tools like Terraform, so documentation stays clear and easy to refresh.

### Diagram examples

<div align="left">
    <img src="examples/project-4.png" alt="AWS diagram example (project-4)" width="380" height="380">
    <img src="examples/project-json.png" alt="AWS diagram from JSON config" width="380" height="380">
</div>
<div align="left">
    <img src="examples/ci-cd-bitbucket-azure-aws.png" alt="CI/CD Bitbucket Azure DevOps AWS" width="520">
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
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS / Linux: source .venv/bin/activate
pip install -r requirements.txt
```

### How to run

Always run scripts from the **repository root** so paths such as `config.json` and `examples/` resolve correctly.

```bash
python project-4.py
# Writes: examples/project-4.png
```

Other entry points work the same way (`json-read.py`, `diagram-terra.py`, `ci-cd-bitbucket-azure-aws.py`, scripts under subfolders, etc.). Each script sets its own output path (usually under `examples/`).

Besides the PNG, Diagrams may leave a **Graphviz source file** next to it (same base name, often without a `.dot` extension). You can delete those files and regenerate them by running the script again.

### Tips

- In `Diagram(...)`, `show=True` opens the image with the default viewer after generation; use `show=False` to only write the file.
- Getting started and layout options: [Diagrams — Getting started](https://diagrams.mingrammer.com/docs/getting-started/installation). AWS node catalog: [AWS nodes](https://diagrams.mingrammer.com/docs/nodes/aws).

**Version:** 0.2.0

---

## Español

Conjunto de diagramas de infraestructura definidos como código con [Diagrams](https://diagrams.mingrammer.com/) en Python. El objetivo es que los gráficos sean reproducibles y coherentes con lo que definís en Terraform (u otras fuentes), para documentar de forma clara y actualizable.

### Ejemplos de diagramas

<div align="left">
    <img src="examples/project-4.png" alt="Ejemplo de diagrama AWS (project-4)" width="380" height="380">
    <img src="examples/project-json.png" alt="Diagrama AWS desde JSON" width="380" height="380">
</div>
<div align="left">
    <img src="examples/ci-cd-bitbucket-azure-aws.png" alt="CI/CD Bitbucket Azure DevOps AWS" width="520">
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
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS / Linux: source .venv/bin/activate
pip install -r requirements.txt
```

### Cómo ejecutar

Ejecutá los scripts siempre desde la **raíz del repositorio**, así `config.json` y la carpeta `examples/` se resuelven bien.

```bash
python project-4.py
# Genera: examples/project-4.png
```

El resto se corre igual (`json-read.py`, `diagram-terra.py`, `ci-cd-bitbucket-azure-aws.py`, los de subcarpetas, etc.). Cada script define su salida (casi siempre bajo `examples/`).

Además del PNG, Diagrams puede dejar el **fuente Graphviz** al lado (mismo nombre, a veces sin extensión `.dot`). Podés borrarlo y regenerarlo volviendo a ejecutar el script.

### Comentarios y recomendaciones

- En `Diagram(...)`, `show=True` abre la imagen con el visor predeterminado al terminar; con `show=False` solo se guarda el archivo.
- Intro e instalación: [Diagrams — Getting started](https://diagrams.mingrammer.com/docs/getting-started/installation). Catálogo de nodos AWS: [AWS nodes](https://diagrams.mingrammer.com/docs/nodes/aws).

**Versión:** 0.2.0

©️ License
By Agustina Fassina