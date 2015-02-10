.. Packtools documentation master file, created by
   sphinx-quickstart on Fri Sep  5 16:18:09 2014.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

packtools
=========

Release v\ |version|.
This software is licensed under `BSD License <http://opensource.org/licenses/BSD-2-Clause>`_.

----

Packtools is a Python library and set of command line utilities which can be 
used to handle :term:`SciELO Publishing Schema` packages and XML files.


stylechecker command line utility
---------------------------------

.. code-block:: bash

    $ stylechecker -h
    usage: stylechecker [-h] [--annotated] [--nonetwork] [--assetsdir ASSETSDIR]
                        [--version]
                        XML [XML ...]

    stylechecker cli utility

    positional arguments:
      XML                   filesystem path or URL to the XML

    optional arguments:
      -h, --help            show this help message and exit
      --annotated           reproduces the XML with notes at elements that have
                            errors
      --nonetwork           prevents the retrieval of the DTD through the network
      --assetsdir ASSETSDIR
                            lookup, at the given directory, for each asset
                            referenced by the XML
      --version             show program's version number and exit
    

    $ stylechecker 0034-8910-rsp-48-2-0206.xml
    [
      {
        "_xml": "0034-8910-rsp-48-2-0206.xml",
        "assets": [],
        "dtd_errors": [
          "Value \"foo\" for attribute ref-type of xref is not among the enumerated set"
        ],
        "is_valid": false,
        "sps_errors": [
          "Element 'abstract': Unexpected attribute xml:lang.",
          "Element 'article-title': Unexpected attribute xml:lang.",
          "Element 'counts': Missing element or wrong value in equation-count.",
          "Element 'xref', attribute ref-type: Invalid value \"foo\".",
          "Element 'person-group': Missing attribute person-group-type.",
          "Element 'fn': Missing attribute fn-type.",
          "Element 'article': Missing SPS version at the attribute specific-use."
        ]
      }
    ]


For better outputs, stylechecker makes use of `Pygments <https://pypi.python.org/pypi/Pygments/>`_ 
whenever it is available.


Using packtools as a library
----------------------------

.. code-block:: python

    >>> pack = packtools.SPSPackage('rsp-v47n4-04.zip')
    >>>
    >>> pack.meta
    {'article_title': u'Casos aut\xf3ctones de esquistossomose mans\xf4nica em crian\xe7as de Recife, PE',
     'issue_number': '04',
     'issue_volume': '47',
     'issue_year': '2013',
     'journal_eissn': '1518-8787',
     'journal_pissn': '0034-8910',
     'journal_title': u'Revista de Sa\xfade P\xfablica'}
    >>>
    >>> pack.list_members_by_type()
    {'pdf': ['0034-8910-rsp-47-04-0684.pdf', 'en_0034-8910-rsp-47-04-0684.pdf'],
     'tif': ['0034-8910-rsp-47-04-0684-gf02.tif', '0034-8910-rsp-47-04-0684-gf01.tif'],
     'xml': ['0034-8910-rsp-47-04-0684.xml']}
    >>>
    >>> pack.get_member('0034-8910-rsp-47-04-0684-gf02.tif')
    <zipfile.ZipExtFile object at 0x10e652a50>
    >>>
    >>> pack.xml_validator
    <XMLValidator xml=<lxml.etree._ElementTree object at 0x10e650200> valid=False>


User guide
----------

Step-by-step guide to use the features provided by **packtools**. 

.. toctree::
   :maxdepth: 2

   install
   quickstart


API documentation
-----------------

If you are looking for information about the library internals,
this if for you.

.. toctree::
   :maxdepth: 2

   api

