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

*packtools* is shipped with a standard catalog, and can be used basically in 2
ways:

1. Registering packtools' catalog in the super catalog with the appropriate delegates, 
   which can be done by adding the following lines to make the file ``/etc/xml/catalog``
   looks like (this is preferred for production):

.. code-block:: xml

    <?xml version="1.0"?>
    <!DOCTYPE catalog PUBLIC "-//OASIS//DTD Entity Resolution XML Catalog V1.0//EN" "http://www.oasis-open.org/committees/entity/release/1.0/catalog.dtd">
    <catalog xmlns="urn:oasis:names:tc:entity:xmlns:xml:catalog">
        <delegatePublic publicIdStartString="-//NLM//DTD JATS" 
                        catalog="file://<packtools_dir>/packtools/catalogs/scielo-publishing-schema.xml"/>
        <delegatePublic publicIdStartString="-//NLM//DTD Journal" 
                        catalog="file://<packtools_dir>/packtools/catalogs/scielo-publishing-schema.xml"/>
        <delegateSystem systemIdStartString="JATS-journalpublishing1.dtd" 
                        catalog="file://<packtools_dir>/packtools/catalogs/scielo-publishing-schema.xml"/>
        <delegateSystem systemIdStartString="journalpublishing3.dtd" 
                        catalog="file://<packtools_dir>/packtools/catalogs/scielo-publishing-schema.xml"/>
        <delegateSystem systemIdStartString="http://jats.nlm.nih.gov/publishing/"
                        catalog="file://<packtools_dir>/packtools/catalogs/scielo-publishing-schema.xml"/>
    </catalog>

`This shell script <https://github.com/scieloorg/packtools/blob/master/scripts/install_xml_catalog.sh>`_ 
can help you with the task.

2. Setting the environment variable *XML_CATALOG_FILES* with the absolute path to 
``<packtools_dir>/packtools/catalogs/scielo-publishing-schema.xml``. This setup can
also be made by the main Python program, so for these cases a constant pointing to 
the catalog file is also provided.

.. code-block:: python

    import os
    from packtools.catalogs import XML_CATALOG
    os.environ['XML_CATALOG_FILES'] = XML_CATALOG


In some cases where the system's entry-point is a single function, for instance 
the ``main`` function, a special helper decorator can be used, as follows:

.. code-block:: python

    from packtools.utils import config_xml_catalog
    @config_xml_catalog
    def main():
        """At this point the XML Catalog is configured"""


More information at http://xmlsoft.org/catalog.html#Simple


Settings up the logger handler
------------------------------

It is expected that the application using `packtools` defines a logger for 
`packtools`, e.g.:

.. code-block:: python

    import logging
    logging.getLogger('packtools').addHandler(logging.StreamHandler())


See the official `docs <http://docs.python.org/2.7/howto/logging.html#configuring-logging>`_ for more info.


Validation basics
-----------------

The validation of an XML document is performed through instances of 
:class:`packtools.XMLValidator`. The easiest way to get an instance is by running
:meth:`packtools.XMLValidator.parse`, which in addition to accepting absolute or
relative path to file in the local filesystem, URL, etree objects, or
file-objects, it also loads the most appropriate validation schemas to the
document according to its version.

.. code-block:: python

    import packtools
    xmlvalidator = packtools.XMLValidator.parse('path/to/file.xml')


The validation can be performed in two levels: DTD and SciELO Style.
To do this, the :meth:`packtools.XMLValidator.validate` and 
:meth:`packtools.XMLValidator.validate_style` methods are available, respectively.
Full validation can be performed with the :meth:`packtools.XMLValidator.validate_all`
method. All these methods return a *tuple* comprising the validation status and the 
errors list.

.. code-block:: python

    import packtools
    xmlvalidator = packtools.XMLValidator.parse('path/to/file.xml')
    is_valid, errors = xmlvalidator.validate_all()

