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

*stylechecker* command-line utility example:

.. code-block:: bash

    $ stylechecker -h
    usage: stylechecker [-h] [--annotated] [--nonetwork] [--version] xmlpath
    
    stylechecker cli utility.
    
    positional arguments:
      xmlpath      Filesystem path or URL to the XML file.
    
    optional arguments:
      -h, --help   show this help message and exit
      --annotated
      --nonetwork
      --version    show program's version number and exit
    
    $ stylechecker "http://192.168.1.162:7000/api/v1/article?code=S1516-635X2014000100012&format=xmlrsps"
    Valid XML! ;)
    Invalid SPS Style! Found 3 errors:
    Element 'journal-meta': Missing element journal-id of type "nlm-ta" or "publisher-id".
    Element 'journal-title-group': Missing element abbrev-journal-title of type "publisher".
    Element 'journal-meta': Missing element issn of type "epub".


Lib usage example:

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

