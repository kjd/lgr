=====================
The idntables toolkit
=====================

This toolkit provides elements for the manipulation of Internationalised
Domain Names (IDNA) strings, with a particular focus on the processing of
strings in conjunction with tables which describe eligible code points
as well as alternate (variant) code points. These tables, often known as
either "IDN tables" or "variant tables" represent the basis of registration
policy for most domain registries that offer IDN registrations.

Installation
============

``idntables`` can be installed simply using the ``pip`` tool:

.. code-block:: text

    $ pip install idntables

Alternatively, you can unpack the archive and run ``python setup.py install``.

Sample usage
============

The most common usage of an IDN table is to perform a validation of a string
against the rules of the table. The library allows you to load a table and
check a domain name. Either the A-label (encoded form) or U-label (presentation
form) of a domain name is accepted:

.. code-block:: pycon

	>>> import idntables
	>>> table = idntables.load('simplified-chinese.xml')
	>>> "例子" in table
	True
	>>> "xn--fsqu00a" in table
	True
	>>> "xn--invalid" in table
	False
	
Additionally, if there are variants in a table, those variants can be computed:

	>>> for variant in table.variants('xn--fiqz9s'):
	...     print variant.ulabel, variant.alabel
	... 
	中國 xn--fiqz9s
	中国 xn--fiqs8s
	中囯 xn--fiq66s
	中圀 xn--fiqy8s

The library provides operations that allow a table to be constructed also:

.. code-block:: pycon

	>>> table = idntables.IDNTable()
	>>> table
	<idntables.tables.IDNTable object at 0x10d327bd0>
	>>> len(table)
	0
	>>> table.add('a-z')
	>>> len(table)
	26
	>>> "foo" in table
	True
	>>> table.addvariant('i', '1')
	>>> table.addvariant('o', '0')
	>>> list(table.variants("moi"))
	['moi', 'mo1', 'm0i', 'm01']
	>>> table.save('sample.xml')

Set operations can be performed on multiple tables in order to merge and
perform other comparisons of the tables:

.. code-block:: pycon

	>>> table1 = idntables.IDNTable()
	>>> table2 = idntables.IDNTable()
	>>> table1.add('a-z')
	>>> table2.add('b-y')
	>>> table3 = table1 - table2
	>>> len(table3)
	2

The "|" and "+" operators perform a union operation on two tables. The "-"
operator subtracts the entries in one table from another. The "&" operator
results in the intersection of the two tables (resulting in a table that
only contains entries that are in both tables.)

Command Line Tool
=================

The application provides a command-line utility called ``idntables`` that provide convenient access to many of the functions of the library.

For example, you can quickly test a label's validity to a given table:

.. code-block:: console

	$ idntables test xn--zckzah sample.xml
	Does not match table sample.xml: Codepoint U+30C6 at position 1 not allowed per table

Or you compute the variants for a given label and table:

.. code-block:: console

	$ idntables variants xn--fiqz9s sample.xml
	xn--fiqz9s
	xn--fiqs8s
	xn--fiq66s
	xn--fiqy8s

There are a number of other functions for merging and analysing tables:

.. code-block:: console

	$ idntables list <table>
	$ idntables info <table>
	$ idntables diff <table1> <table2>
	$ idntables merge <table1> <table2> <table3> > <mergedtable>
	$ idntables merge <table1> <table2> --output <mergedtable>


API Reference
=============

.. toctree::
   :maxdepth: 2

   api/core
   api/tables
   api/codepoints
   api/idna
   api/etree

