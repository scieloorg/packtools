from unittest import TestCase

from packtools.sps.utils import xml_utils
from packtools.sps.formats.am import am
from packtools.sps.models.article_citations import ArticleCitations


class AM(TestCase):
    def setUp(self):
        self.xml_tree = xml_utils.get_xml_tree(
            "tests/sps/fixtures/standard_scielo_xml/S0080-62342022000100445_JATS.xml"
        )
        self.citation_data = list(ArticleCitations(self.xml_tree).article_citations)[0]

    def test_code(self):
        self.assertDictEqual(
            {"code": "S0080-62342022000100445"}, am.code(self.xml_tree, dict())
        )

