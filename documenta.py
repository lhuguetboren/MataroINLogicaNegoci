
import os
import pydoc

# Lista de módulos de tu proyecto
# Lista de módulos de tu proyecto
modules = [
    "app",
    "buscador_aloj",
    "CalculosNegocios",
    "config",
    "generate_keys",
    "models",
    "pila",
    "reserva",
    "security",
    "securityUsers",
    "socket_1",
    "usuarios"
]
# Crear directorio para almacenar la documentación si no existe
docs_dir = "docs"
if not os.path.exists(docs_dir):
    os.makedirs(docs_dir)

# Generar documentación para cada módulo
for module in modules:
    # Generar el archivo HTML
    module_doc = pydoc.HTMLDoc().document(pydoc.safeimport(module))
    # Guardar el archivo HTML en el directorio docs
    with open(os.path.join(docs_dir, f"{module}.html"), "w", encoding='utf-8') as f:
        f.write(module_doc)

# Crear un archivo index.html que enlace a toda la documentación
index_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Documentation</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .container {
            width: 80%;
            margin: auto;
            padding: 20px;
        }
        h1 {
            text-align: center;
        }
        ul {
            list-style-type: none;
            padding: 0;
        }
        li {
            margin: 10px 0;
        }
        a {
            text-decoration: none;
            color: #007BFF;
        }
        a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Project Documentation</h1>
        <ul>
"""

for module in modules:
    index_content += f'            <li><a href="{module}.html">{module}</a></li>\n'

index_content += """
        </ul>
    </div>
</body>
</html>
"""

# Guardar el archivo index.html en el directorio docs
with open(os.path.join(docs_dir, "index.html"), "w", encoding='utf-8') as f:
    f.write(index_content)

print("Documentación generada en el directorio 'docs'.")
