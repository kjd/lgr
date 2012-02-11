ElementTree
===========

The :mod:`idntables.etree` module is an import helper, which will import the best
available ElementTree implementation available on the system.

By preference, if LXML is installed, the :mod:`ElementTree` provided by that library will
be used. LXML provides support for XML schema validation, which can be used by the
discretionary validation functions for the IDN tables.

If LXML is not installed, then any custom installed ElementTree is imported.

Finally, if neither is available, the built-in version is imported which is available
in Python 2.5 or higher.

Sample Usage
------------

.. code-block:: python

	from idntables.etree import etree

