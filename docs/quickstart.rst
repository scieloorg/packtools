Tutorial
========

.. _xml-catalog-configuration:

XML Catalog configuration
-------------------------

An XML Catalog is a lookup mechanism which can be used to prevent network
requests from being performed while loading external DTDs.

For performance and safety, instances of ``stylechecker.XMLValidator`` do not perform 
network connections, so we strongly recommend that you set up an XML catalog, 
which translates public ids to local file URIs.

*packtools* is shipped with a standard catalog. To use it, simply set the
environment variable *XML_CATALOG_FILES* with the absolute path to 
``<packtools_dir>/packtools/catalogs/scielo-publishing-schema.xml``. This setup can
also be made by the main Python program, so for these cases a constant pointing to 
the catalog file is also provided.

.. code-block:: python

    >>> import os
    >>> from packtools.catalogs import XML_CATALOG
    >>> os.environ['XML_CATALOG_FILES'] = XML_CATALOG


More information at http://xmlsoft.org/catalog.html#Simple


Step-by-step tutorial
---------------------

