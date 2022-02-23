from unittest import TestCase

from packtools.sps.utils import xml_utils


class TestXMLUtils(TestCase):

    def test_node_text_diacritics(self):
        xmltree = xml_utils.get_xml_tree("<root><city>São Paulo</city></root>")
        expected = "São Paulo"
        result = xml_utils.node_text(xmltree.find(".//city"))
        self.assertEqual(expected, result)

    def test_tostring_diacritics_from_root(self):
        xmltree = xml_utils.get_xml_tree("<root><city>São Paulo</city></root>")
        expected = (
            "<?xml version='1.0' encoding='utf-8'?>\n"
            "<root><city>São Paulo</city></root>"
        )
        result = xml_utils.tostring(xmltree)
        self.assertEqual(expected, result)

    def test_tostring_entity_from_root(self):
        xmltree = xml_utils.get_xml_tree(
            "<root><city>S&#227;o Paulo</city></root>")
        expected = (
            "<?xml version='1.0' encoding='utf-8'?>\n"
            "<root><city>São Paulo</city></root>"
        )
        result = xml_utils.tostring(xmltree)
        self.assertEqual(expected, result)
