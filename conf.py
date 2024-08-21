# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('extensions'))

# -- Project information -----------------------------------------------------

project = 'The Haiku Book'
copyright = '2023, Haiku, Inc.'
author = 'Haiku'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = ''

html_short_title = "API Documentation"


# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    #"myst_parser",
    "custom_parser",
    "abigroup",
]

myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "substitution",
    "linkify"
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "bebook_style.BeBookStyle"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'haikumodern'
html_theme_path = ["theme"]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
html_sidebars = { '**': [ 'localtoc.html'] }


# -- Additional configuration ------------------------------------------------

smartquotes = True

html_css_files = [
    'css/code.css',
    #'css/hide.css'
]

pygments_style = "bebook_style.BeBookStyle"

# def setup(app):
#     from sphinx.highlighting import lexers
#     from pygments.lexers import CppLexer
#     from pygments.filters import Filter
#     from pygments.token import Name

#     class ApiFilter(Filter):
#         def __init__(self, **options):
#             Filter.__init__(self, **options)

#             with open("classes.txt") as classes:
#                 self.classes=[]
#                 for line in classes:
#                     self.classes.append(line.strip())

#         def filter(self, lexer, stream):
#             is_arrow=False
#             is_hyphen=False
#             for ttype, value in stream:
#                 if value in self.classes:
#                     ttype = Name.Class
#                 if is_arrow:
#                     if ttype == Name:
#                         ttype = Name.Function
#                     is_arrow=False
#                 if value == '-':
#                     is_hyphen=True
#                 elif value == '>':
#                     if is_hyphen:
#                         is_arrow=True
#                         is_hyphen=False
#                 else:
#                     is_hyphen=False
#                 yield ttype, value
#     class ApiLexer(CppLexer):
#         def __init__(self, **options):
#             CppLexer.__init__(self, **options)
#             self.add_filter(ApiFilter())

#     app.add_lexer('beapi', ApiLexer)

# highlight_language = 'beapi'
