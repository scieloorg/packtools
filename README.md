scielo.packtools
================

Canivete suiço para a inspeção de pacotes SPS e rSPS.


Instalação
----------

Pip + git:

```bash
pip install -e git+git://github.com/scieloorg/packtools.git#egg=packtools
```

Repositório de códigos (versão de desenvolvimento):

```bash
git clone https://github.com/scieloorg/packtools.git
cd packtools 
python setup.py install
```


Utilitário `stylechecker`
-------------------------

Após a instalação, o programa `stylechecker` deverá estar disponível no seu emulador de terminal. 
Esse programa realiza a validação de um determinado XML no formato SPS contra o seu XML Schema, e 
apresenta uma lista dos erros encontrados. Também é possível *anotar* os erros encontrados em uma
cópia do XML em validação, por meio do argumento opcional `--annotated`.

```bash
$ stylechecker -h
usage: stylechecker [-h] [--annotated] xmlpath

stylechecker cli utility.

positional arguments:
  xmlpath      Filesystema path or URL to the XML file.

optional arguments:
  -h, --help   show this help message and exit
  --annotated
```

Obs.: Para validar XMLs disponíveis via http, é necessário delimitar a URL com aspas ou apóstrofo. e.g.: 

```bash
$ stylechecker "http://192.168.1.162:7000/api/v1/article?code=S1516-635X2014000100012&format=xmlrsps"
Valid XML! ;)
```

