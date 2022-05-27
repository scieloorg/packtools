# scielo.packtools

Python library and command-line utilities to handle SciELO PS XML files that
runs on python 2.7, 3.3+.


## Build status

[![Build Status](https://travis-ci.com/gustavofonseca/packtools.svg?branch=master)](https://travis-ci.com/gustavofonseca/packtools)

[![Latest Documentation Status](https://readthedocs.org/projects/packtools/badge/?version=latest)](https://packtools.readthedocs.io/en/latest/)


## Installation

``packtools`` depends on [lxml](http://lxml.de/installation.html).


Python Package Index (recommended):

```bash
$ pip install packtools
```

or just:

```bash
pip install -r requirements.txt
```


Pip + git (versão de desenvolvimento):

```bash
$ pip install -e git+git://github.com/scieloorg/packtools.git#egg=packtools
```


Source-code:

```bash
$ git clone https://github.com/scieloorg/packtools.git
$ cd packtools
$ python setup.py install
```

Installation as a web application, where a graphical interface for `stylechecker`
and an HTML previewer is provided:

```bash
$ pip install packtools[webapp]
```

or

```bash
pip install -r requirements.txt && pip install -r optional-requirements.txt
```

## Tests

To run tests execute:

```bash
python setup.py test
```

To run a specific module of tests, type:

```bash
python setup.py test -s tests.test_htmlgenerator
```

## Command line execute

```bash
htmlgenerator example.xml --loglevel=error --nochecks --nonetwork
```

It will generate the result in the same path of the .xml file.

## Running the web application


Configuring the application:

| environment variable | default value                                    |
|----------------------|--------------------------------------------------|
| APP_SETTINGS         | packtools.webapp.config.default.ProductionConfig |


```bash
$ export APP_SETTINGS=packtools.webapp.config.default.ProductionConfig
$ export FLASK_APP=packtools.webapp.app.py
$ flask run
```


## Documentation

http://packtools.readthedocs.org/ (we need help!)


## Use license

Copyright 2013 SciELO <scielo-dev@googlegroups.com>. Licensed under the terms
of the BSD license. Please see LICENSE in the source code for more
information.

https://github.com/scieloorg/packtools/blob/master/LICENSE


## Changelog

https://github.com/scieloorg/packtools/blob/master/HISTORY.md
