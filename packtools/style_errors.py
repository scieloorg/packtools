# coding:utf-8
"""Adapters for XML errors.

An adapter is an object that provides domain-specific apis for another object,
called adaptee.
"""
from __future__ import unicode_literals
import io
import re
import logging

from lxml import etree


LOGGER = logging.getLogger(__name__)


EXPOSE_ELEMENTNAME_PATTERN = re.compile(r"(?<=Element )'.*?'")


def search_element_name(message):
    """Try to locate in `message` the element name pointed as error.

    :param message: is a lxml error log message.
    """
    match = EXPOSE_ELEMENTNAME_PATTERN.search(message)
    if match is None:
        LOGGER.info('cannot find the element name in message')
        LOGGER.debug('failed regexp was %s on message "%s"', 
                EXPOSE_ELEMENTNAME_PATTERN.pattern, message)
        raise ValueError('cannot find the element name in message')

    else:
        element_name = match.group(0).strip("'")
        LOGGER.info('found element name "%s" in message', element_name)

        return element_name


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

    # raise ValueError if the element could not be located.
    LOGGER.info('could not find element "%s"', xpath)
    raise ValueError('could not find element "%s"' % xpath)


#--------------------------------
# adapters for XML style errors
#--------------------------------
class StyleErrorBase(object):
    """Acts like an interface for SPS style errors.

    A basic implementation of `get_apparent_element` is provided.
    """
    line = message = level = None
    label = u''

    def get_apparent_element(self, doc):
        """The apparent element presenting the error at doc.

        This base implementation tries to discover the element name by
        searching the string pattern `Element 'element name'` on message.
        """
        return NotImplemented


class StyleError(StyleErrorBase):
    """ SciELO-style errors raised by the validation pipeline.
    """
    level = u'Style Error'

    def get_apparent_element(self, doc):
        """The apparent element presenting the error at doc.

        This base implementation tries to discover the element name by
        searching the string pattern `Element 'element name'` on message.
        """
        tagname = search_element_name(self.message)
        return search_element(doc, '//' + tagname, line=self.line)


class SchemaStyleError(StyleErrorBase):
    """ DTD errors.
    """
    level = u'DTD Error'

    def __init__(self, err_object, label=u''):
        self._err = err_object
        self.message = self._err.message
        self.line = self._err.line
        self.label = label

    def get_apparent_element(self, doc):
        for elem in doc.iter():
            if elem.sourceline == self.line:
                return elem

        LOGGER.info("cannot find element at the line %s", self.line)
        raise ValueError("cannot find element at the line %s" % self.line)


class SchematronStyleError(StyleErrorBase):
    """ SciELO-style errors raised by schematron validation.
    """
    level = u'Style Error'

    def __init__(self, err_object, label=u''):
        self._err = err_object
        self.label = label

        byte_string = io.BytesIO(self._err.message.encode('utf-8'))
        self._parsed_message = etree.parse(byte_string)

    @property
    def message(self):
        search_res = re.search(r"<svrl:text>(.*)</svrl:text>",
                self._err.message, re.DOTALL)
        try:
            text = search_res.group(1)
        except AttributeError:
            raise ValueError('cannot get message')

        return text.strip()

    def get_apparent_element(self, doc):
        query_res = self._parsed_message.xpath('@location')
        try:
            tagname = query_res[0]
        except IndexError:
            raise ValueError('cannot get context info')

        return search_element(doc, tagname)

