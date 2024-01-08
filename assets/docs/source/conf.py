# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
import sphinx_rtd_theme
import mock

current_dir = os.path.dirname(__file__)
target_dir = os.path.abspath(os.path.join(current_dir, "../../"))
sys.path.insert(0, target_dir)

# -- Project info ------------------------------------------------------------
project = 'Proyecto itc_etl'
copyright = '2023, Edosoft'
author = 'Edosoft'
release = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
                'sphinx_rtd_theme', # Necesario para cargar el estilo del documento bonito 'rtd theme'
                'sphinx.ext.napoleon', # Incluir docstrings estilo NumPy y estilo Google
                'sphinx.ext.autodoc', # Incluir docstrings
                'sphinx.ext.autosectionlabel', # Incluir referencias a secciones utilizando títulos
                'sphinx.ext.doctest', # Comprueba snippets dentro de la documentación
                'sphinx.ext.todo', # Incluir objetos todo
                'sphinx.ext.coverage', # Genera estadísticas acerca del funcionamiento del programa (visible en la consola)
                'sphinx.ext.mathjax', # Permite que el hmtl o el pdf output contenga fórmulas matemáticas legibles
                'sphinx.ext.ifconfig', # Necesaria para activar ciertas configuraciones 
                'sphinx.ext.viewcode', # Incluir links que redirigen hacia el código fuente
                #'sphinx.ext.intersphinx', # Incluir links hacia otros proyectos de documentación
                'sphinx.ext.duration', # Contador del tiempo que tarda en generar cada output (visible en la consola)
                #'sphinx.ext.autosummary', # Genera automáticamente archivos .rst. En este proyecto se ha hecho de forma manual.
            ]

# Generar el path relativo dónde se podrán guardar templates.
templates_path = ['_templates']

# Idioma de los comentarios
language = 'es'

# Lista de patrones a ignorar. Relativa al path de origen.
exclude_patterns = [*'__init__.py',
]

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# En caso de ser necesarios 'fake imports' (suelen ser problemas con las versiones de Python o las versiones de las librerías)
autodoc_mock_imports = ['proteus']