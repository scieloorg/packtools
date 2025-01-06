from unittest import TestCase
import lxml.etree as ET

from packtools.sps.utils import xml_utils
from packtools.sps.formats.scielo_citation_index import SciELOCitationConverter


class SciELOCitationConverterTest(TestCase):
    def setUp(self):
        self.xml_tree = xml_utils.get_xml_tree('tests/sps/fixtures/standard_scielo_xml/S0080-62342022000100445_JATS.xml')

    def test_articles(self):
        self.maxDiff = None
        expected = (
            '<articles '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:schemaLocation="https://raw.githubusercontent.com/scieloorg/articles_meta/master/tests/xsd/scielo_sci/ThomsonReuters_publishing.xsd" '
            'dtd-version="1.1"/>'
        )
        obtained = SciELOCitationConverter(self.xml_tree).create_articles_tag()

        obtained_str = ET.tostring(obtained, encoding="utf-8").decode("utf-8")

        self.assertEqual(expected, obtained_str)

    def test_article(self):
        self.maxDiff = None
        expected = (
            '<article lang_id="en" article-type="research-article"/>'
        )
        obtained = SciELOCitationConverter(self.xml_tree).create_article_tag()

        obtained_str = ET.tostring(obtained, encoding="utf-8").decode("utf-8")

        self.assertEqual(expected, obtained_str)

    def test_article_citation_index(self):
        self.maxDiff = None
        expected = (
            '<articles '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xsi:schemaLocation="https://raw.githubusercontent.com/scieloorg/articles_meta/master/tests/xsd/scielo_sci/ThomsonReuters_publishing.xsd" '
            'dtd-version="1.1">'
            '<article lang_id="en" article-type="research-article"/>'
            '</articles>'
        )
        obtained = SciELOCitationConverter(self.xml_tree).create_article_citation_index()

        obtained_str = ET.tostring(obtained, encoding="utf-8").decode("utf-8")

        self.assertEqual(expected, obtained_str)




