Installing Packtools
====================

Packtools works with CPython > 3.9. 
Please, read `lxml's installation instructions <http://lxml.de/installation.html>`_ 
to make sure it is installed correctly.


Pip + GitHub (recommended)
--------------------------

Check the latest version available at `GitHub releases <https://github.com/scieloorg/packtools/releases>`_ 
and replace the version in the URL below accordingly:

.. code-block:: bash

    $ pip install https://github.com/scieloorg/packtools/archive/refs/tags/4.16.0.zip


Source code (development version)
---------------------------------

.. code-block:: bash

    $ git clone https://github.com/scieloorg/packtools.git
    $ cd packtools 
    $ python setup.py install


You can test the installation executing:

.. code-block:: bash

    $ stylechecker -h

