"""
Sphinx configuration.
"""
import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(".."))

import generate_changelog  # NOQA

project = "generate-changelog"
copyright = f"{date.today():%Y}, Corey Oordt"
author = "Corey Oordt"

version = generate_changelog.__version__
release = generate_changelog.__version__

# -- General configuration ---------------------------------------------

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx.ext.autosectionlabel",
    "sphinx.ext.napoleon",
    "sphinx_autodoc_typehints",
    "sphinx.ext.coverage",
    "sphinx.ext.githubpages",
    "sphinx_click",
]

autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 2

autodoc_default_flags = [
    # Make sure that any autodoc declarations show the right members
    "members",
    "undoc-members",
    "private-members",
]

autosummary_generate = True

napoleon_attr_annotations = True
napoleon_include_special_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_init_with_doc = True
myst_enable_extensions = [
    "amsmath",
    "colon_fence",
    "deflist",
    "dollarmath",
    "linkify",
    "replacements",
    "smartquotes",
    "substitution",
    "tasklist",
]
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "gitpython": ("https://gitpython.readthedocs.io/en/stable/", None),
}

templates_path = ["_templates"]
source_suffix = [".rst", ".md"]
master_doc = "index"
language = None
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"
todo_include_todos = False


# -- Options for HTML output -------------------------------------------

html_theme = "furo"
html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
]
