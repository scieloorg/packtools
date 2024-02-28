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

    def test_remove_subtags_keeps_i(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "São Paulo <i>Paulo</i>"
        obtained = xml_utils.remove_subtags(xmltree.find(".//city"), ['i'])
        self.assertEqual(expected, obtained)

    def test_remove_subtags_keeps_bold(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<bold>São Paulo</bold> Paulo"
        obtained = xml_utils.remove_subtags(xmltree.find(".//city"), ['bold'])
        self.assertEqual(expected, obtained)

    def test_remove_subtags_keeps_italic(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<italic>São</italic> Paulo Paulo"
        obtained = xml_utils.remove_subtags(xmltree.find(".//city"), ['italic'])
        self.assertEqual(expected, obtained)

    def test_remove_subtags_keeps_bold_and_italic(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<bold><italic>São</italic> Paulo</bold> Paulo"
        obtained = xml_utils.remove_subtags(xmltree.find(".//city"), ['bold', 'italic'])
        self.assertEqual(expected, obtained)

    def test_remove_subtags_keeps_bold_and_i(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<bold>São Paulo</bold> <i>Paulo</i>"
        obtained = xml_utils.remove_subtags(xmltree.find(".//city"), ['bold', 'i'])
        self.assertEqual(expected, obtained)

    def test_remove_subtags_keeps_italic_and_i(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<italic>São</italic> Paulo <i>Paulo</i>"
        obtained = xml_utils.remove_subtags(xmltree.find(".//city"), ['italic', 'i'])
        self.assertEqual(expected, obtained)

    def test_remove_subtags_keeps_all(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<bold><italic>São</italic> Paulo</bold> <i>Paulo</i>"
        obtained = xml_utils.remove_subtags(xmltree.find(".//city"), ['bold', 'italic', 'i'])
        self.assertEqual(expected, obtained)

    def test_remove_subtags_remove_all(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "São Paulo Paulo"
        obtained = xml_utils.remove_subtags(xmltree.find(".//city"))
        self.assertEqual(expected, obtained)

    def test_convert_xml_to_html(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<b><i>São</i> Paulo</b> Paulo"
        obtained = xml_utils.convert_xml_to_html(
            xmltree.find(".//city"),
            ['italic', 'bold'],
            {'italic': 'i', 'bold': 'b'}
        )
        self.assertEqual(expected, obtained)

    def test_convert_xml_to_html_without_dict(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <root>
            <city><bold><italic>São</italic> Paulo</bold> <i>Paulo</i></city>
            </root>
            """
        )
        expected = "<bold><italic>São</italic> Paulo</bold> Paulo"
        obtained = xml_utils.convert_xml_to_html(
            xmltree.find(".//city"),
            ['italic', 'bold']
        )
        self.assertEqual(expected, obtained)


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
