Installing Packtools
====================

Packtools works with CPython > 3.9. 
Please, read `lxml's installation instructions <http://lxml.de/installation.html>`_ 
to make sure it is installed correctly.


Pypi (recommended)
------------------

.. code-block:: bash

    $ pip install packtools


Source code (development version)
---------------------------------

.. code-block:: bash

    $ git clone https://github.com/scieloorg/packtools.git
    $ cd packtools 
    $ python setup.py install


Installing on Windows
--------------------


Requirements
````````````

* What is the Windows version?
* What is the Python version?
* Is the architecture 32 or 64 bits?
* The packages *lxml* and *packtools* can be downloaded at 
  `PyPi <https://pypi.python.org/pypi>`_.


For example, if you want to install packtools on a  *64 bits Windows 10* machine
running *Python 2.7.3* you should download and install `lxml-3.7.3.win-amd64-py2.7.exe <https://pypi.python.org/packages/b7/8d/e43df2f52f032090d2d0d9139dd5db84b2831172380cd884f421b1f3cf6c/lxml-3.7.3.win-amd64-py2.7.exe#md5=72bc82b8205d22aa888c38fa9b9dd239>`_ and `packtools-2.0.1-py2.py3-none-any.whl <https://pypi.python.org/packages/a7/5f/ec82f6cbb541f93d07f95aea8061553bde3a42d2405bdff2ff654c6ba1a1/packtools-2.0.1-py2.py3-none-any.whl#md5=0a83c0c388204da0fbf5ce1003ebaee7>`_. While *lxml* comes with a double-click graphic installer,
*packtools* will require the following command at the command prompt:

.. code-block:: bash

    $ pip install path/to/packtools-2.0.1-py2.py3-none-any.whl

You can test the installation executing:

.. code-block:: bash

    $ stylechecker -h

