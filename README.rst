scielo.packtools
================

Canivete suiço para a inspeção de pacotes SPS.


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
```


Exemplo do resultado da validação:

```bash
$ stylechecker 0034-8910-rsp-48-2-0206.xml
[
  {
    "_xml": "0034-8910-rsp-48-2-0206.xml",
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
```

