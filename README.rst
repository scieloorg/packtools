scielo.packtools
================

Canivete suiço para a inspeção de pacotes SPS.

Build status
============

.. image:: https://travis-ci.org/scieloorg/packtools.svg?branch=master
    :target: https://travis-ci.org/scieloorg/packtools


Instalação
----------

Python Package Index (recomendado):

```bash
pip install packtools
```

Pip + git (versão de desenvolvimento):

```bash
pip install -e git+git://github.com/scieloorg/packtools.git#egg=packtools
```

Repositório de códigos (versão de desenvolvimento):

```bash
git clone https://github.com/scieloorg/packtools.git
cd packtools
python setup.py install
```


Configuração do Catálogo XML
----------------------------

Um Catálogo XML é um mecanismo de *lookup* que pode ser utilizado para evitar que requisições de
rede sejam realizadas para carregar DTDs externas.

Por questões de desempenho e segurança, as instâncias de `stylechecker.XML` não realizam
conexões de rede, portanto é extremamente recomendável que seja configurado um Catálogo XML,
que traduz ids públicos para uris de arquivos locais.

O `packtools` já apresenta um catálogo padrão, que para ser utilizado basta definir a
variável de ambiente `XML_CATALOG_FILES` com o caminho absoluto para
`packtools/catalogs/scielo-publishing-schema.xml`.

Mais informações em http://xmlsoft.org/catalog.html#Simple


Utilitário `stylechecker`
-------------------------

Após a instalação, o programa `stylechecker` deverá estar disponível no seu emulador de terminal.
Esse programa realiza a validação de um determinado XML no formato SPS contra a DTD, e
apresenta uma lista dos erros encontrados. Também é possível *anotar* os erros encontrados em uma
cópia do XML em validação, por meio do argumento opcional `--annotated`.

O utilitário `stylechecker` tenta carregar a DTD externa, especificada na declaração DOCTYPE do
XML. Para evitar esse comportamento, utilize a opção `--nonetwork`.

A função *ajuda* pode ser utilizada com a opção `-h`, conforme o exemplo:

```bash
$ stylechecker -h
usage: stylechecker [-h] [--annotated | --raw] [--nonetwork]
                    [--assetsdir ASSETSDIR] [--version] [--loglevel LOGLEVEL]
                    [--nocolors] [--extrasch EXTRASCH]
                    [XML [XML ...]]

SciELO PS stylechecker command line utility.

positional arguments:
  XML                   filesystem path or URL to the XML

optional arguments:
  -h, --help            show this help message and exit
  --annotated           reproduces the XML with notes at elements that have
                        errors
  --raw                 each result is encoded as json, without any
                        formatting, and written to stdout in a single line.
  --nonetwork           prevents the retrieval of the DTD through the network
  --assetsdir ASSETSDIR
                        lookup, at the given directory, for each asset
                        referenced by the XML. current working directory will
                        be used by default.
  --version             show program's version number and exit
  --loglevel LOGLEVEL
  --nocolors            prevents the output from being colorized by ANSI
                        escape sequences
  --extrasch EXTRASCH   runs an extra validation using an external schematron
                        schema.

Copyright 2013 SciELO <scielo-dev@googlegroups.com>. Licensed under the terms
of the BSD license. Please see LICENSE in the source code for more
information.
```

