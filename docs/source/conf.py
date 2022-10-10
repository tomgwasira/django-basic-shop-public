# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import django

# -- Sphinx Django setup -----------------------------------------------------
django_basic_shop_dir = os.path.realpath(
    os.path.join(os.path.dirname(__file__), "../..")
)
sys.path.append(django_basic_shop_dir)
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

# -- Project information -----------------------------------------------------
project = "Django Online Shop"
copyright = "2021, Thomas Gwasira"
author = "Thomas Gwasira"
release = "0.1.0"


# -- General configuration ---------------------------------------------------
extensions = [
    "sphinx.ext.doctest",
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.todo",
]

# Turn on sphinx.ext.autosummary
autosummary_generate = True

# Prevent full paths to classes and functions
# add_module_names = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = "alabaster" # default theme
html_permalinks_icon = "<span>#</span>"
html_theme = "sphinx_rtd_theme"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]
