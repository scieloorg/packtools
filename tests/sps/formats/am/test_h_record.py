from unittest import TestCase
from unittest.mock import patch
import datetime
from lxml import etree

from packtools.sps.formats.am import h_record


class HRecord(TestCase):

    def test_code(self):
        self.xml_tree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
            <front>
            <article-meta>
            <article-id specific-use="scielo-v2" pub-id-type="publisher-id">S1414-98932020000100118</article-id>
            </article-meta>
            </front>
            </article>
            """
        )
        self.assertDictEqual(
            {"code": "S1414-98932020000100118"}, h_record.code(self.xml_tree, dict())
        )
