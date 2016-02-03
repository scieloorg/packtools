"""Packtools is a Python library and set of command line utilities which can be
used to handle SciELO Publishing Schema packages and XML files.
"""
import os
import sys
import logging
import platform

from lxml import etree

from .domain import XMLValidator, HTMLGenerator
from .utils import XML
from .version import __version__


__all__ = [
    'XMLValidator',
    'XML',
    '__version__',
    'get_debug_info',
    'HTMLGenerator',
]


# we need to handle this exception in order to use sphinx-doc's autodoc.
try:
    LIBXML_COMPILED_VERSION = '.'.join(
            (str(digit) for digit in etree.LIBXML_COMPILED_VERSION))
except TypeError:
    LIBXML_COMPILED_VERSION = ''

try:
    LIBXML_VERSION = '.'.join(
            (str(digit) for digit in etree.LIBXML_VERSION))
except TypeError:
    LIBXML_VERSION = ''

try:
    LIBXSLT_COMPILED_VERSION = '.'.join(
            (str(digit) for digit in etree.LIBXSLT_COMPILED_VERSION))
except TypeError:
    LIBXSLT_COMPILED_VERSION = ''

try:
    LIBXSLT_VERSION = '.'.join(
            (str(digit) for digit in etree.LIBXSLT_VERSION))
except TypeError:
    LIBXSLT_VERSION = ''

try:
    LXML_VERSION = '.'.join(
            (str(digit) for digit in etree.LXML_VERSION))
except TypeError:
    LXML_VERSION = ''


def get_debug_info():
    """ Returns debug data computed at the time.
    """
    info = {
        'libxml_compiled_version': LIBXML_COMPILED_VERSION,
        'libxml_version': LIBXML_VERSION,
        'libxslt_compiled_version': LIBXSLT_COMPILED_VERSION,
        'libxslt_version': LIBXSLT_VERSION,
        'lxml_version': LXML_VERSION,
        'xml_catalog_files': os.environ.get('XML_CATALOG_FILES', ''),
        'system_path': sys.path,
        'packtools_version': __version__,
        'python_version': platform.python_version(),
    }

    return info


# Setting up a do-nothing handler. We expect the application to define
# the handler for `packtools`.
logging.getLogger(__name__).addHandler(logging.NullHandler())

