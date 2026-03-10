# docs/source/conf.py — Sphinx configuration template
# Replace <PROJECT_NAME>, <AUTHOR>, <VERSION> with actual values.

project = "<PROJECT_NAME>"
author = "<AUTHOR>"
release = "<VERSION>"
copyright = "2026, <AUTHOR>"

# -- Extensions ---------------------------------------------------------------
extensions = [
    "sphinx.ext.autodoc",           # pull docstrings from source code
    "sphinx.ext.napoleon",          # parse Google-style docstrings
    "sphinx_autodoc_typehints",     # render type hints in documentation
    "sphinx.ext.viewcode",          # add [source] links to generated HTML
    "sphinx.ext.intersphinx",       # cross-reference external projects
    "myst_parser",                  # support .md files alongside .rst
]

# -- Napoleon (Google-style) --------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False

# -- Type hints ----------------------------------------------------------------
autodoc_typehints = "description"
always_document_param_types = True

# -- Theme ---------------------------------------------------------------------
html_theme = "sphinx_rtd_theme"

# -- Intersphinx targets -------------------------------------------------------
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pandas": ("https://pandas.pydata.org/docs/", None),
    "snowflake-connector-python": (
        "https://docs.snowflake.com/en/developer-guide/python-connector/python-connector-api",
        None,
    ),
}

# -- Source parsers ------------------------------------------------------------
source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
