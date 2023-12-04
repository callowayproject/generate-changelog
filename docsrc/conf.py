"""
Sphinx configuration.
"""
import os
import sys
from datetime import date

sys.path.insert(0, os.path.abspath(".."))

import generate_changelog  # noqa: E402

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
autodoc_class_signature = "separated"
autodoc_member_order = "bysource"
autodoc_typehints = "description"
autodoc_type_aliases = {
    "StrOrCallable": "generate_changelog.configuration.StrOrCallable",
    "IntOrCallable": "generate_changelog.configuration.IntOrCallable",
}

autosummary_generate = True

napoleon_attr_annotations = True
napoleon_include_special_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_init_with_doc = True
# napolean_use_param = True

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
    "fieldlist",
]
myst_heading_anchors = 2
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "gitpython": ("https://gitpython.readthedocs.io/en/stable/", None),
}

templates_path = ["_templates"]
source_suffix = [".rst", ".md"]
master_doc = "index"
language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"
todo_include_todos = False


# -- Options for HTML output -------------------------------------------

html_theme = "furo"
html_static_path = ["_static"]
html_css_files = [
    "css/custom.css",
]
html_theme_options = {
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/coordt/generate-changelog",
            "html": (
                '<svg stroke="currentColor" fill="currentColor" stroke-width="0" viewBox="0 0 16 16">'
                '<path fill-rule="evenodd" d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 '
                "0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-"
                ".01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31"
                "-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 "
                "1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95."
                "29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0 0 16 8c0-4.42-3.58-"
                '8-8-8z"></path></svg>'
            ),
            "class": "",
        },
    ],
}
html_title = f"Generate Changelog {release}"
