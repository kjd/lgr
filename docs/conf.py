import sys, os
sys.path.append(os.path.abspath('_themes'))

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

if on_rtd:
	html_theme = 'default'
else:
	html_theme = 'icann'
html_theme_path = ['_themes']
extensions = ['sphinx.ext.coverage']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'idntables'
copyright = u'2012 Kim Davies'
version = '0.1'
release = '0.1'
exclude_patterns = ['_build']
pygments_style = 'sphinx'
html_static_path = ['_static']
html_show_sourcelink = False
html_show_sphinx = False
html_show_copyright = False
htmlhelp_basename = 'idntablesdoc'
latex_elements = {
}
latex_documents = [
  ('index', 'idntables.tex', u'idntables Documentation',
   u'Kim Davies', 'manual'),
]
man_pages = [
    ('index', 'idntables', u'idntables Documentation',
     [u'Kim Davies'], 1)
]
texinfo_documents = [
  ('index', 'idntables', u'idntables Documentation',
   u'Kim Davies', 'idntables', 'IDN Table Toolkit',
   'Miscellaneous'),
]
