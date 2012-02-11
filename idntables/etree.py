try:
	from lxml.etree import *
	have_lxml = True
except ImportError:
	have_lxml = False
	try:
		from elementtree.ElementTree import *
	except ImportError:
		from xml.etree.ElementTree import *
