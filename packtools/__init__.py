"""Packtools is a Python library and set of command line utilities which can be
used to handle SciELO Publishing Schema packages and XML files.
"""
import logging

from .xray import SPSPackage
from .domain import XMLValidator, XMLPacker
from .utils import XML
from .version import __version__

# Setting up a do-nothing handler. We expect the application to define
# the handler for `packtools`.
logging.getLogger(__name__).addHandler(logging.NullHandler())

