#coding: utf-8
import re
import logging
from StringIO import StringIO

from lxml import etree

from . import utils


logger = logging.getLogger(__name__)


EXPOSE_ELEMENTNAME_PATTERN = re.compile(r"(?<=Element )'.*?'")


def search_element_name(message):
    """Try to locate in `message` the element name pointed as error.

    :param message: is a lxml error log message.
    """
    match = EXPOSE_ELEMENTNAME_PATTERN.search(message)
    if match is None:
        raise ValueError('Could not locate the element name in %s.' % message)
    else:
        return match.group(0).strip("'")


def search_element(doc, xpath, line=None):
    """Try to locate in `doc` the element expressed as `xpath`.
    """
    for elem in doc.xpath(xpath):
        if line is None:
            return elem

        elif elem.sourceline == line:
            return elem

        else:
            continue

    else:
        raise ValueError("Could not find element '%s'." % xpath)


class StyleError(object):
    """Acts like an interface for SPS style errors.

    A basic implementation of `get_apparent_element` is provided.
    """
    # The sourceline of the apparent element
    line = 0
    column = 0

    # The error message
    message = None

    # The error level. Can be ERROR or WARNING
    level = 'Error'
    level_name = level

    def get_apparent_element(self, doc):
        """The apparent element presenting the error at doc.

        This base implementation tries to discover the element name by
        searching the string pattern `Element 'element name'` on message.
        """
        def get_data():
            tagname = search_element_name(self.message)
            return search_element(doc, '//' + tagname, line=self.line)

        return utils.setdefault(self, '__apparent_element', get_data)


class SchemaStyleError(StyleError):
    """Implements the StyleError interface for Schema error objects.
    """
    def __init__(self, err_object):
        self._err = err_object
        self.message = self._err.message
        self.line = self._err.line

    def get_apparent_element(self, doc):
        def get_data():
            tagname = search_element_name(self.message)
            return search_element(doc, '//' + tagname, line=self.line)

        return utils.setdefault(self, '__apparent_element', get_data)


class SchematronStyleError(StyleError):
    """Implements the StyleError interface for Schematron error objects.
    """
    def __init__(self, err_object):
        self._err = err_object
        self._parsed_message = etree.parse(StringIO(self._err.message.encode('utf-8')))

    @property
    def message(self):
        def get_data():
            try:
                text = re.search(r"<svrl:text>(.*)</svrl:text>", self._err.message, re.DOTALL).group(1)
            except AttributeError:
                raise ValueError('Cannot get the message from %s.' % self._err)

            return text.strip()

        return utils.setdefault(self, '__message', get_data)

    def get_apparent_element(self, doc):
        def get_data():
            try:
                tagname = self._parsed_message.xpath('@location')[0]
            except IndexError:
                raise ValueError('Cannot get the context info from %s.' % self._err.message)

            return search_element(doc, tagname)

        return utils.setdefault(self, '__apparent_element', get_data)

