import re
import os
import logging
import itertools

from lxml import etree

from packtools.utils import setdefault
from packtools.checks import StyleCheckingPipeline


HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMAS = {
    'SciELO-journalpublishing1.xsd': os.path.join(HERE, 'sps_xsd', 'sps.xsd'),
}
EXPOSE_ELEMENTNAME_PATTERN = re.compile(r"(?<=Element )'.*?'")

logger = logging.getLogger(__name__)


def XMLSchema(schema_name):
    with open(SCHEMAS[schema_name]) as fp:
        xmlschema_doc = etree.parse(fp)

    xmlschema = etree.XMLSchema(xmlschema_doc)
    return xmlschema


def search_element_name(message):
    """Try to locate in `message` the element name pointed as error.

    :param message: is a lxml error log message.
    """
    match = EXPOSE_ELEMENTNAME_PATTERN.search(message)
    if match is None:
        raise ValueError('Could not locate the element name in %s.' % message)
    else:
        return match.group(0).strip("'")


class XML(object):
    def __init__(self, file):
        """Represents an XML under validation.

        The XML can be retrieved given its filesystem path,
        an URL, a file-object or an etree instance.

        The XML is validated against the JATS Publishing tag set
        and the SPS Style.

        :param file: Path to the XML file, URL or etree.
        """
        if isinstance(file, etree._ElementTree):
            self.lxml = file
        else:
            self.lxml = etree.parse(file)

        self.xmlschema = XMLSchema('SciELO-journalpublishing1.xsd')
        self.ppl = StyleCheckingPipeline()

    def find_element(self, tagname, lineno=None, fallback=True):
        """Find an element given a tagname and a line number.

        If no element is found than the return value is None.
        :param tagname: string of the tag name.
        :param lineno: int if the line it appears on the original source file.
        :param fallback: fallback to root element when `element` is not found.
        """
        for elem in self.lxml.findall('//' + tagname):
            if lineno is None:
                return elem

            elif elem.sourceline == lineno:
                logger.debug('method *find*: hit a regular element: %s.' % tagname)
                return elem

            else:
                continue
        else:
            root = self.lxml.getroot()
            if fallback:
                return root
            elif root.tag == tagname:
                logger.debug('method *find*: hit a root element.')
                return root
            else:
                raise ValueError("Could not find element '%s'." % tagname)

    def validate(self):
        """Validate the source XML against the JATS Publishing Schema.

        Returns a tuple comprising the validation status and the errors list.
        """
        result = setdefault(self, '__validation_result', lambda: self.xmlschema.validate(self.lxml))
        errors = setdefault(self, '__validation_errors', lambda: self.xmlschema.error_log)
        return result, errors

    def validate_style(self):
        """Validate the source XML against the SPS Tagging guidelines.

        Returns a tuple comprising the validation status and the errors list.
        """
        errors = next(self.ppl.run(self.lxml, rewrap=True))
        result = not bool(errors)
        return result, errors

    def _annotate_error(self, element, error):
        """Add an annotation prior to `element`, with `error` as the content.

        The annotation is a <SPS-ERROR> element added prior to `element`.
        If `element` is the root element, then the error is annotated as comment.
        :param element: etree instance to be annotated.
        :param error: string of the error.
        """
        notice_element = etree.Element('SPS-ERROR')
        notice_element.text = error
        try:
            element.addprevious(notice_element)
        except TypeError:
            # In case of a root element, a comment if added.
            element.addprevious(etree.Comment('SPS-ERROR: %s' % error))

    def annotate_errors(self):
        """Add notes on all elements that have errors.

        The errors list is generated as a result of calling both :meth:`validate` and
        :meth:`validate_style` methods.
        """
        v_result, v_errors = self.validate()
        s_result, s_errors = self.validate_style()

        if not v_result and not s_result:
            return None

        for error in itertools.chain(v_errors, s_errors):
            try:
                element_name = search_element_name(error.message)
            except ValueError:
                # could not find the element name
                logger.info('Could not locate the element name in: %s' % error.message)
                continue

            if error.line is None:
                err_element = self.find_element(element_name)
            else:
                err_element = self.find_element(element_name, lineno=error.line)

            self._annotate_error(err_element, error.message)

    def __str__(self):
        return etree.tostring(self.lxml, pretty_print=True,
            encoding='utf-8', xml_declaration=True)

    def __unicode__(self):
        return str(self).decode('utf-8')

    def __repr__(self):
        return '<packtools.stylechecker.XML xml=%s valid=%s>' % (self.lxml, self.validate()[0])

    def read(self):
        """
        Read the XML contents as text.
        """
        return unicode(self)


def main():
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='stylechecker cli utility.')
    parser.add_argument('--annotated', action='store_true')
    parser.add_argument('xmlpath', help='Filesystem path or URL to the XML file.')

    args = parser.parse_args()
    xml = XML(args.xmlpath)

    is_valid, errors = xml.validate()
    style_is_valid, style_errors = xml.validate_style()

    if args.annotated:
        xml.annotate_errors()
        sys.stdout.write(str(xml))

    else:
        if not is_valid:
            print 'Invalid XML! Found %s errors:' % len(errors)
            for err in errors:
                print '%s,%s\t%s' % (err.line, err.column, err.message)
        else:
            print 'Valid XML! ;)'

        if not style_is_valid:
            print 'Invalid SPS Style! Found %s errors:' % len(style_errors)
            for err in style_errors:
                print err.message
        else:
            print 'Valid SPS Style! ;)'

if __name__ == '__main__':
    main()

