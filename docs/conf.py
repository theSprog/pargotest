#!/usr/bin/env python3

import os
import sys
from pathlib import Path

# -- Path setup --------------------------------------------------------------
# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

# Get project root directory
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# -- Project information -----------------------------------------------------
project = 'two'
copyright = '2025, Your Name'
author = 'Your Name'
version = '0.0.1'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
extensions = [
    'breathe',
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.mathjax',
    'sphinx.ext.ifconfig',
    'sphinx.ext.githubpages',
    'myst_parser',  # For Markdown support
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The master toctree document.
master_doc = 'index'

# The suffix(es) of source filenames.
source_suffix = {
    '.rst': None,
    '.md': 'myst_parser',
}

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'canonical_url': '',
    'analytics_id': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom CSS files
html_css_files = [
    'custom.css',
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

# -- Breathe configuration ---------------------------------------------------
breathe_projects = {
    project: os.path.join(os.path.dirname(__file__), '_build/doxygen/xml')
}
breathe_default_project = project
breathe_default_members = ('members', 'undoc-members')
breathe_show_define_initializer = True
breathe_show_enumvalue_initializer = True

# -- Napoleon settings -------------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# -- Intersphinx mapping -----------------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'sphinx': ('https://www.sphinx-doc.org/en/master/', None),
}

# -- MyST Parser configuration -----------------------------------------------
myst_enable_extensions = [
    'amsmath',
    'colon_fence',
    'deflist',
    'dollarmath',
    'fieldlist',
    'html_admonition',
    'html_image',
    'linkify',
    'replacements',
    'smartquotes',
    'strikethrough',
    'substitution',
    'tasklist',
]

# -- Custom configuration ----------------------------------------------------
# Custom roles
rst_prolog = """
.. role:: cpp(code)
   :language: cpp
   :class: highlight

.. role:: bash(code)
   :language: bash
   :class: highlight
"""

# Version info for conditional content
version_info = tuple(map(int, version.split('.')))

# -- LaTeX output options ----------------------------------------------------
latex_elements = {
    'papersize': 'letterpaper',
    'pointsize': '10pt',
    'preamble': '',
    'fncychap': '',
    'printindex': '',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, f'{project}.tex', f'{project} Documentation', author, 'manual'),
]

# -- Manual page output ------------------------------------------------------
# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, project.lower(), f'{project} Documentation', [author], 1)
]

# -- Texinfo output ----------------------------------------------------------
# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, project, f'{project} Documentation', author, project,
     'One line description of project.', 'Miscellaneous'),
]

# -- Extension configuration -------------------------------------------------
def setup(app):
    """Custom setup function."""
    app.add_css_file('custom.css')
    
    # Add custom directives or modify behavior here
    pass

# -- External links ----------------------------------------------------------
extlinks = {
    'github': ('https://github.com/yourusername/yourproject/%s', 'GitHub %s'),
    'issue': ('https://github.com/yourusername/yourproject/issues/%s', 'issue %s'),
    'pr': ('https://github.com/yourusername/yourproject/pull/%s', 'PR %s'),
}

# -- Autodoc configuration ---------------------------------------------------
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}

# -- HTML context ------------------------------------------------------------
html_context = {
    'display_github': True,
    'github_user': 'yourusername',
    'github_repo': 'yourproject',
    'github_version': 'main',
    'conf_py_path': '/docs/',
}

# Language for content autogenerated by Sphinx
language = 'en'

# A boolean that decides whether module names are prepended to all object names
add_module_names = False

# A boolean that decides whether parentheses are appended to function and method names
add_function_parentheses = True

# The default language to highlight source code in
highlight_language = 'cpp'