.. _cli:

Command-line tools
==================

stylechecker
------------

packbuilder
-----------

Builds a SciELO PS package for each XML file passed as argument.

Usage:

.. code-block:: bash

    $ packbuilder 0034-8910-rsp-48-2-0192.xml
    Created 0034-8910-rsp-48-2-0192.zip


Multiple XML files can also be passed:

.. code-block:: bash

    $ packbuilder 0034-8910-rsp-48-2-0192.xml 0034-8910-rsp-48-2-0193.xml
    Created 0034-8910-rsp-48-2-0192.zip
    Created 0034-8910-rsp-48-2-0193.zip

