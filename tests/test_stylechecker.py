#coding: utf-8
import unittest
from StringIO import StringIO
from tempfile import NamedTemporaryFile

from lxml import etree

from packtools import stylechecker


# valid: <a><b></b></a>
# invalid: anything else
sample_xsd = StringIO('''\
<xsd:schema xmlns:xsd="http://www.w3.org/2001/XMLSchema">
<xsd:element name="a" type="AType"/>
<xsd:complexType name="AType">
  <xsd:sequence>
    <xsd:element name="b" type="xsd:string" />
  </xsd:sequence>
</xsd:complexType>
</xsd:schema>
''')


def setup_tmpfile(method):
    def wrapper(self):
        valid_tmpfile = NamedTemporaryFile()
        valid_tmpfile.write(b'<a><b>bar</b></a>')
        valid_tmpfile.seek(0)
        self.valid_tmpfile = valid_tmpfile

        method(self)

        self.valid_tmpfile.close()
    return wrapper


class XMLTests(unittest.TestCase):

    @setup_tmpfile
    def test_initializes_with_filepath(self):
        self.assertTrue(stylechecker.XML(self.valid_tmpfile.name))

    def test_initializes_with_etree(self):
        fp = StringIO(b'<a><b>bar</b></a>')
        et = etree.parse(fp)

        self.assertTrue(stylechecker.XML(et))

    def test_validation(self):
        fp = etree.parse(StringIO(b'<a><b>bar</b></a>'))
        xml = stylechecker.XML(fp)
        xml.xmlschema = etree.XMLSchema(etree.parse(sample_xsd))

        result, errors = xml.validate()
        self.assertTrue(result)
        self.assertFalse(errors)

    def test_invalid(self):
        fp = etree.parse(StringIO(b'<a><c>bar</c></a>'))
        xml = stylechecker.XML(fp)
        xml.xmlschema = etree.XMLSchema(etree.parse(sample_xsd))

        result, _ = xml.validate()
        self.assertFalse(result)

    def test_invalid_errors(self):
        # Default lxml error log.
        fp = etree.parse(StringIO(b'<a><c>bar</c></a>'))
        xml = stylechecker.XML(fp)
        xml.xmlschema = etree.XMLSchema(etree.parse(sample_xsd))

        _, errors = xml.validate()
        self.assertIsInstance(errors, etree._ListErrorLog)

    def test_find(self):
        fp = etree.parse(StringIO(b'<a>\n<b>bar</b>\n</a>'))
        xml = stylechecker.XML(fp)
        xml.xmlschema = etree.XMLSchema(etree.parse(sample_xsd))

        elem = xml.find('b', 2)
        self.assertEqual(elem.tag, 'b')
        self.assertEqual(elem.sourceline, 2)

    def test_find_root_element(self):
        fp = etree.parse(StringIO(b'<a>\n<b>bar</b>\n</a>'))
        xml = stylechecker.XML(fp)
        xml.xmlschema = etree.XMLSchema(etree.parse(sample_xsd))

        elem = xml.find('a', 1)
        self.assertEqual(elem.tag, 'a')
        self.assertEqual(elem.sourceline, 1)

    def test_find_missing(self):
        fp = etree.parse(StringIO(b'<a>\n<b>bar</b>\n</a>'))
        xml = stylechecker.XML(fp)
        xml.xmlschema = etree.XMLSchema(etree.parse(sample_xsd))

        self.assertIsNone(xml.find('c', 2))

    def test_annotate_errors(self):
        fp = etree.parse(StringIO(b'<a><c>bar</c></a>'))
        xml = stylechecker.XML(fp)
        xml.xmlschema = etree.XMLSchema(etree.parse(sample_xsd))

        xml.annotate_errors()
        self.assertIn("<SPS-ERROR>Element 'c': This element is not expected. Expected is ( b ).</SPS-ERROR>", str(xml))

    def test_annotate_errors(self):
        fp = etree.parse(StringIO(b'<a><c>bar</c></a>'))
        xml = stylechecker.XML(fp)
        xml.xmlschema = etree.XMLSchema(etree.parse(sample_xsd))

        xml.annotate_errors()
        xml_text = xml.read()

        self.assertIn("<SPS-ERROR>Element 'c': This element is not expected. Expected is ( b ).</SPS-ERROR>", xml_text)
        self.assertTrue(isinstance(xml_text, unicode))


class ElementNamePatternTests(unittest.TestCase):
    pattern = stylechecker.EXPOSE_ELEMENTNAME_PATTERN

    def test_case1(self):
        message = "Element 'article', attribute 'dtd-version': [facet 'enumeration'] The value '3.0' is not an element of the set {'1.0'}."
        self.assertEqual(self.pattern.search(message).group(0), "'article'")


    def test_case2(self):
        message = "Element 'article', attribute 'dtd-version': '3.0' is not a valid value of the local atomic type."
        self.assertEqual(self.pattern.search(message).group(0), "'article'")

    def test_case3(self):
        message = "Element 'author-notes': This element is not expected. Expected is one of ( label, title, ack, app-group, bio, fn-group, glossary, ref-list, notes, sec )."
        self.assertEqual(self.pattern.search(message).group(0), "'author-notes'")

    def test_case4(self):
        message = "Element 'journal-title-group': This element is not expected. Expected is ( journal-id )."
        self.assertEqual(self.pattern.search(message).group(0), "'journal-title-group'")

    def test_case5(self):
        message = "Element 'contrib-group': This element is not expected. Expected is one of ( article-id, article-categories, title-group )."
        self.assertEqual(self.pattern.search(message).group(0), "'contrib-group'")

