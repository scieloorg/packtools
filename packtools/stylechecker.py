import re
import copy
from lxml import etree


SCHEMAS = {'http://static.scielo.org/sps/schema/SciELO-journalpublishing1.xsd': '/Users/gustavofonseca/prj/github/packtools/packtools/sps_xsd/sps.xsd'}
EXPOSE_ELEMENTNAME_PATTERN = re.compile(r"'.*'")


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
                return elem

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
                raise ValueError('Could not locate the erratic element %s at line %s.' % (element_name, error.line))

            notice_element = etree.Element('SPS-ERROR')
            notice_element.text = error.message
            err_element.addprevious(notice_element)

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

