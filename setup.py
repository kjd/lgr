"""
This library provides the ability to generate, manipulate and check against
"IDN Tables", which are formal descriptions of which code points are
available for registration by internationalised domain name registries.
These tables can also specify contextual rules, as well as rules for
generating sets of labels derived from nominated code point variants.
"""

import sys
from setuptools import setup, find_packages

version = "0.1"

def main():

	python_version = sys.version_info[:2]
	python_3 = sys.version_info[0] == 3

	if python_3:
		raise SystemExit("Sorry, Python 2.x only")
	if python_version < (2,5):
		raise SystemExit("Sorry, Python 2.5 or newer required")

	arguments = {
		'name': 'idntables',
		'packages': find_packages(),
		'provides': ['idntables'],
		'version': version,
		'entry_points': {
			'console_scripts': [
				'idntables = idntables.commandline:main',
			],
		},
		'install_requires': [
			'setuptools',
			'nose',
		],
		'requires': [
			'argparse',
		],
		'test_suite': 'nose.collector',
		
		'description': 'IDN Table Toolkit',
		'long_description': __doc__,
		'author': 'Kim Davies',
		'author_email': 'kim.davies@icann.org',
		'license': 'BSD-like',
		'url': 'https://github.com/kjd/idntables',
		'classifiers': [
			'Development Status :: 3 - Alpha',
			'Intended Audience :: Developers',
			'Intended Audience :: System Administrators',
			'License :: OSI Approved :: BSD License',
			'Operating System :: OS Independent',
			'Topic :: Internet :: Name Service (DNS)',
			'Topic :: Software Development :: Libraries :: Python Modules',
			'Topic :: Utilities',
		],
	}
	
	setup(**arguments)

if __name__ == '__main__':
	main()
