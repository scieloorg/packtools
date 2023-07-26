from unittest import TestCase

from lxml import etree

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


class NodeTextTest(TestCase):

    def test_node_text_with_sublevels(self):
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<bold><italic>São</italic> Paulo</bold> <i>Paulo</i>"
        result = xml_utils.node_text(xmltree.find(".//city"))
        self.assertEqual(expected, result)


class NodeTextWithoutXrefTest(TestCase):

    def test_node_text_without_xref_with_sublevels(self):
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i><xref rid="fn1">1</xref>, <xref rid="fn2">2</xref></city>
            </root>
            """
        )
        expected = "<bold><italic>São</italic> Paulo</bold> <i>Paulo</i>"
        result = xml_utils.node_text_without_xref(xmltree.find(".//city"))
        self.assertEqual(expected, result)

    def test_node_text_without_xref_with_sublevels_keeps_xref_tail(self):
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i><xref rid="fn1">*</xref> texto para manter</city>
            </root>
            """
        )
        expected = "<bold><italic>São</italic> Paulo</bold> <i>Paulo</i> texto para manter"
        result = xml_utils.node_text_without_xref(xmltree.find(".//city"))
        self.assertEqual(expected, result)
