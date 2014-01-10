"""
This library provides the ability to generate, manipulate and check against
"Label Generation Rulesets", which are formal descriptions of which code points
are available for registration by domain name registries. These tables can also
specify contextual rules, as well as rules for generating sets of labels derived
from nominated code point variants.
"""

import sys
from setuptools import setup, find_packages

def main():

    python_version = sys.version_info[:2]
    python_3 = sys.version_info[0] == 3

    if python_3:
        raise SystemExit("Sorry, Python 2.x only")
    if python_version < (2,5):
        raise SystemExit("Sorry, Python 2.5 or newer required")

    from lgr import __version__

    arguments = {
        'name': 'lgr',
        'packages': find_packages(),
        'provides': ['lgr'],
        'version': __version__,
        'entry_points': {
            'console_scripts': [
                'lgr = lgr.commandline:main',
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

        'description': 'Label Generation Ruleset Toolkit',
        'long_description': __doc__,
        'author': 'Kim Davies',
        'author_email': 'kim.davies@icann.org',
        'license': 'BSD-like',
        'url': 'https://github.com/kjd/lgr',
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
