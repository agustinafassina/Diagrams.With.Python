# Diagrams with python
This repository contains several diagrams generated with Python, designed to create visual diagrams automatically through code. The goal is to facilitate the reproduction and visual documentation of our infrastructure, enabling us to replicate what is defined in Terraform and convert it into clear, up-to-date diagrams.

### Structure
└─ .gitignore  <br>
└─ config.json <br>
└─ json-read.py <br>
└─ project-1.py <br>
└─ project-2.py <br>
└─ project-3.py <br>
└─ project-4.py <br>
└─ project-5.py <br>
└─ README.md

### How to use this repository?

From root:

```
python project1.py
# Result: project-1.png
```

### Comments and recomendations
- Make sure you have the necessary dependencies installed for the visualization (such as Graphviz and its Python libraries).
- In the diagram: 'show=True' will automatically open a preview of the generated diagram using the default image viewer.# Setting it to 'False' will generate the diagram without opening it automatically.

#### Repository version
v 0.1.0
