"""Just to ease the access to the files.
"""
import os


_CWD = os.path.dirname(os.path.abspath(__file__))

# Validation schemas: XSD or DTD files.
SCH_SCHEMAS = {
    'sps-1.1': os.path.join(_CWD, 'scielo-style-1.1.sch'),
    'sps-1.2': os.path.join(_CWD, 'scielo-style-1.2.sch'),
    'sps-1.3': os.path.join(_CWD, 'scielo-style-1.3.sch'),
    'sps-1.4': os.path.join(_CWD, 'scielo-style-1.4.sch'),
    'sps-1.5': os.path.join(_CWD, 'scielo-style-1.5.sch'),
    'sps-1.6': os.path.join(_CWD, 'scielo-style-1.6.sch'),
    'sps-1.7': os.path.join(_CWD, 'scielo-style-1.7.sch'),
    'sps-1.8': os.path.join(_CWD, 'scielo-style-1.8.sch'),

    # Collection-specific schema
    'scielo-br': os.path.join(_CWD, 'scielo-br.sch'),
}

DTDS = {
    'JATS-journalpublishing1.dtd': os.path.join(
        _CWD, 'jats-publishing-dtd-1.0/JATS-journalpublishing1.dtd'),
    'journalpublishing3.dtd': os.path.join(
        _CWD, 'pmc-publishing-dtd-3.0/journalpublishing3.dtd'),
}

# Python>=3.5 is possible to use the syntax: SCHEMAS = {**SCH_SCHEMAS, **DTDS}
# https://docs.python.org/dev/whatsnew/3.5.html#pep-448-additional-unpacking-generalizations
SCHEMAS = dict(SCH_SCHEMAS)
SCHEMAS.update(DTDS)

# XML Catalog - OASIS Standard.
XML_CATALOG = os.path.join(_CWD, 'scielo-publishing-schema.xml')

XSLTS = {
    'root-html-1.2.xslt': os.path.join(_CWD, 'htmlgenerator/root-html-1.2.xslt'),
    'root-html-2.0.xslt': os.path.join(_CWD, 'htmlgenerator/root-html-2.0.xslt'),
}

ISO3166_CODES = os.path.join(_CWD, 'iso3166-codes.json')

