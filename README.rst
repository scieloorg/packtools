scielo.packtools
================

Python library and command-line utilities to handle SciELO PS XML files that
runs on python 2.7, 3.3+.


Build status
------------

.. image:: https://travis-ci.org/scieloorg/packtools.svg?branch=master
    :target: https://travis-ci.org/scieloorg/packtools
    :alt: master Travis CI Status

.. image:: https://readthedocs.org/projects/packtools/badge/?version=latest
        :target: https://packtools.readthedocs.io/en/latest/
        :alt: Latest Documentation Status


Installation
------------

``packtools`` depends on `lxml <http://lxml.de/installation.html>`_.


Python Package Index (recommended):

.. code-block:: bash

    $ pip install packtools


Pip + git (versão de desenvolvimento):

.. code-block:: bash

    $ pip install -e git+git://github.com/scieloorg/packtools.git#egg=packtools


Source-code:

.. code-block:: bash

    $ git clone https://github.com/scieloorg/packtools.git
    $ cd packtools
    $ python setup.py install


Installation as a web application, where a graphical interface for `stylechecker`
and an HTML previewer is provided:

.. code-block:: bash

    $ pip install packtools[webapp]


Running the web application
---------------------------


Configuring the application::

+----------------------+--------------------------------------------------+
| environment variable | default value                                    |
+======================+==================================================+
| APP_SETTINGS         | packtools.webapp.config.default.ProductionConfig |
+----------------------+--------------------------------------------------+


.. code-block:: bash

    $ export APP_SETTINGS=packtools.webapp.config.default.ProductionConfig
    $ export FLASK_APP=packtools.webapp.app.py
    $ flask run


Documentation
-------------

http://packtools.readthedocs.org/ (we need help!)


Use license
-----------

Copyright 2013 SciELO <scielo-dev@googlegroups.com>. Licensed under the terms
of the BSD license. Please see LICENSE in the source code for more
information.

https://github.com/scieloorg/packtools/blob/master/LICENSE


Changelog
---------
https://github.com/scieloorg/packtools/blob/master/HISTORY.rst
