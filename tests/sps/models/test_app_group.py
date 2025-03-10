from unittest import TestCase

from lxml import etree

from packtools.sps.models.app_group import App, AppGroup
from packtools.sps.utils import xml_utils


class AppTest(TestCase):
    def setUp(self):
        xml_tree = xml_utils.get_xml_tree('tests/fixtures/htmlgenerator/app_group_supplementary_material/0104-5970-hcsm-27-01-0275.xml')
        self.app = App(xml_tree.xpath(".//app")[0])

    def test_app_id(self):
        self.assertEqual(self.app.id, "app01")

    def test_app_label(self):
        self.assertEqual(self.app.label, "FONTES")

    def test_data(self):
        expected = {
            'attrib': None,
            'caption': None,
            'id': 'app01',
            'label': 'FONTES'
        }
        obtained = self.app.data
        self.assertDictEqual(expected, obtained)


class AppGroupTest(TestCase):
    def setUp(self):
        self.xml_tree = xml_utils.get_xml_tree('tests/fixtures/htmlgenerator/app_group_supplementary_material/0104-5970-hcsm-27-01-0275.xml')

    def test_data(self):
        obtained = list(AppGroup(self.xml_tree).data())
        expected = [
            {
                'id': 'app01',
                'label': 'FONTES',
                'attrib': None,
                'caption': None,
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt'
            },
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])
