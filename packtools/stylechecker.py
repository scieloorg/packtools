"""
Mensagens de error_log (linha, coluna - mensagem):

4,0 - Element 'article', attribute 'dtd-version': [facet 'enumeration'] The value '3.0' is not an element of the set {'1.0'}.
4,0 - Element 'article', attribute 'dtd-version': '3.0' is not a valid value of the local atomic type.
824,0 - Element 'author-notes': This element is not expected. Expected is one of ( label, title, ack, app-group, bio, fn-group, glossary, ref-list, notes, sec ).
6,0 - Element 'journal-title-group': This element is not expected. Expected is ( journal-id ).
15,0 - Element 'contrib-group': This element is not expected. Expected is one of ( article-id, article-categories, title-group ).
"""
import re
import copy
from lxml import etree
import logging


SCHEMAS = {'http://static.scielo.org/sps/schema/SciELO-journalpublishing1.xsd': '/Users/gustavofonseca/prj/github/packtools/packtools/sps_xsd/sps.xsd'}
EXPOSE_ELEMENTNAME_PATTERN = re.compile(r"(?<=Element )'.*?'")

logger = logging.getLogger(__name__)


def XMLSchema(href):
    with open(SCHEMAS[href]) as fp:
        xmlschema_doc = etree.parse(fp)

    xmlschema = etree.XMLSchema(xmlschema_doc)
    return xmlschema


def setdefault(object, attribute, producer):
    if not hasattr(object, attribute):
        setattr(object, attribute, producer())

    return getattr(object, attribute)


class XML(object):
    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath) as fp:
            self.xml = etree.parse(fp)
        self.xmlschema = XMLSchema('http://static.scielo.org/sps/schema/SciELO-journalpublishing1.xsd')

    def find(self, tagname, lineno):
        for elem in self.xml.findall('//' + tagname):
            if elem.sourceline == lineno:
                logger.debug('method *find*: hit a regular element: %s.' % tagname)
                return elem
        else:
            root = self.xml.getroot()
            if root.tag == tagname:
                logger.debug('method *find*: hit a root element.')
                return root


    def validate(self):
        result = setdefault(self, '_validation_result', lambda: self.xmlschema.validate(self.xml))
        errors = setdefault(self, '_validation_errors', lambda: self.xmlschema.error_log)
        return result, errors

    def annotate_errors(self):
        result, errors = self.validate()

        for error in errors:
            match = EXPOSE_ELEMENTNAME_PATTERN.search(error.message)
            if match is None:
                raise ValueError('Could not locate the element name in %s.' % error.message)
            else:
                element_name = match.group(0).strip("'")

            err_element = self.find(element_name, error.line)
            if err_element is None:
                raise ValueError('Could not locate the erratic element %s at line %s to annotate: %s.' % (element_name, error.line, error.message))

            notice_element = etree.Element('SPS-ERROR')
            notice_element.text = error.message
            try:
                err_element.addprevious(notice_element)
            except TypeError:
                # In case of a root element, a comment if added.
                err_element.addprevious(etree.Comment('SPS-ERROR: %s' % error.message))

    def __str__(self):
        return etree.tostring(self.xml, pretty_print=True,
            encoding='utf-8', xml_declaration=True)


if __name__ == '__main__':
    import sys
    xml_filepath = sys.argv[1]
    xml = XML(xml_filepath)

    is_valid, errors = xml.validate()

    if is_valid:
        print 'XML file is valid.'
    else:
        for err in errors:
            print '%s,%s - %s' % (err.line, err.column, err.message)

        xml.annotate_errors()
        sys.stderr.write(str(xml))

