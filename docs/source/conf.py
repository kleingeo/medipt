# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

# import ImageProcessingTools
import sys
import os
sys.path.insert(0, os.path.abspath('../..'))
import medipt


project = 'MedIPT'
copyright = '2023, Geoff Klein'
author = 'Geoff Klein'
# from importlib.metadata import version as get_version
# # release = get_version("medipt")
# release = get_version(root='..', relative_to=__file__)
# # for example take major/minor
version = medipt.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = []

templates_path = ['_templates']
extensions = [
    'sphinx.ext.napoleon',
    'sphinx.ext.autodoc',
    'sphinx_autodoc_typehints',
    'sphinx.ext.autosummary',
    'sphinx.ext.intersphinx',
    'sphinx.ext.mathjax',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages'
]

autodoc_typehints = "description"
# build the templated autosummary files
autosummary_generate = True
autodoc_mock_imports = ['torch']

master_doc = "index"

intersphinx_mapping = {
    'python': ('https://docs.python.org/', None),
    'numpy': ('http://docs.scipy.org/doc/numpy', None),
    'SimpleITK': ('https://simpleitk.readthedocs.io/en/master/', None),
}


exclude_patterns = ['old_data_loader/*']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = []

html_baseurl = 'medipt.org'

html_title = 'MedIPT'
