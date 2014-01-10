===============
The lgr toolkit
===============

This toolkit provides elements for the manipulation of Internationalised
Domain Names (IDNA) strings, with a particular focus on the processing of
strings in conjunction with rulesets which describe eligible code points
as well as alternate (variant) code points. These rulesets, often known as
either "IDN tables" or "variant tables" represent the basis of registration
policy for most domain registries that offer IDN registrations.

Installation
============

``lgr`` can be installed simply using the ``pip`` tool:

.. code-block:: text

    $ pip install lgr

Alternatively, you can unpack the archive and run ``python setup.py install``.

Sample usage
============

The most common usage of an IDN ruleset is to perform a validation of a string
against the rules of the ruleset. The library allows you to load a ruleset and
check a domain name. Either the A-label (encoded form) or U-label (presentation
form) of a domain name is accepted:

.. code-block:: pycon

	>>> import lgr
	>>> ruleset = lgr.load('simplified-chinese.xml')
	>>> "例子" in ruleset
	True
	>>> "xn--fsqu00a" in ruleset
	True
	>>> "xn--invalid" in ruleset
	False
	
Additionally, if there are variants in a ruleset, those variants can be computed:

	>>> for variant in ruleset.variants('xn--fiqz9s'):
	...     print variant.ulabel, variant.alabel
	... 
	中國 xn--fiqz9s
	中国 xn--fiqs8s
	中囯 xn--fiq66s
	中圀 xn--fiqy8s

The library provides operations that allow a ruleset to be constructed also:

.. code-block:: pycon

	>>> ruleset = lgr.Ruleset()
	>>> ruleset
	<lgr.rulesets.Ruleset object at 0x10d327bd0>
	>>> len(ruleset)
	0
	>>> ruleset.add('a-z')
	>>> len(ruleset)
	26
	>>> "foo" in ruleset
	True
	>>> ruleset.addvariant('i', '1')
	>>> ruleset.addvariant('o', '0')
	>>> list(ruleset.variants("moi"))
	['moi', 'mo1', 'm0i', 'm01']
	>>> ruleset.save('sample.xml')

Set operations can be performed on multiple rulesets in order to merge and
perform other comparisons of the rulesets:

.. code-block:: pycon

	>>> ruleset1 = lgr.Ruleset()
	>>> ruleset2 = lgr.Ruleset()
	>>> ruleset1.add('a-z')
	>>> ruleset2.add('b-y')
	>>> ruleset3 = ruleset1 - ruleset2
	>>> len(ruleset3)
	2

The "|" and "+" operators perform a union operation on two rulesets. The "-"
operator subtracts the entries in one ruleset from another. The "&" operator
results in the intersection of the two rulesets (resulting in a ruleset that
only contains entries that are in both rulesets.)

Command Line Tool
=================

The application provides a command-line utility called ``lgr`` that provide convenient access to many of the functions of the library.

For example, you can quickly test a label's validity to a given ruleset:

.. code-block:: console

	$ lgr test xn--zckzah sample.xml
	Does not match ruleset sample.xml: Codepoint U+30C6 at position 1 not allowed per ruleset

Or you compute the variants for a given label and ruleset:

.. code-block:: console

	$ lgr variants xn--fiqz9s sample.xml
	xn--fiqz9s
	xn--fiqs8s
	xn--fiq66s
	xn--fiqy8s

There are a number of other functions for merging and analysing rulesets:

.. code-block:: console

	$ lgr list <ruleset>
	$ lgr info <ruleset>
	$ lgr diff <ruleset1> <ruleset2>
	$ lgr merge <ruleset1> <ruleset2> <ruleset3> > <mergedruleset>
	$ lgr merge <ruleset1> <ruleset2> --output <mergedruleset>


API Reference
=============

.. toctree::
   :maxdepth: 2

   api/core
   api/rulesets
   api/codepoints
   api/idna
   api/etree

