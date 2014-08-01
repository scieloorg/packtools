"""Just to ease the access to the files.
"""
import os


_CWD = os.path.dirname(os.path.abspath(__file__))

# Validation schemas: XSD or DTD files.
SCHEMAS = {
    'scielo-style.sch': os.path.join(_CWD, 'scielo-style.sch'),
    'JATS-journalpublishing1.dtd': os.path.join(_CWD, 'jats-publishing-dtd-1.0/JATS-journalpublishing1.dtd'),
    'journalpublishing3.dtd': os.path.join(_CWD, 'pmc-publishing-dtd-3.0/journalpublishing3.dtd'),
}

# XML Catalog - OASIS Standard.
XML_CATALOG = os.path.join(_CWD, 'scielo-publishing-schema.xml')

