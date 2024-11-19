import unittest

from lxml import etree

from packtools.sps.formats.pdf.utils import xml_utils


class TestGetTextFromNode(unittest.TestCase):

    def test_get_text_from_node_with_xref_and_italic(self):
        xmltree = etree.fromstring(
            '<p>Start <xref ref-type="bibr">Text <italic>Emphasized</italic> more</xref> end.</p>'
        )
        expected = 'Start Text Emphasized more end.'
        result = xml_utils.get_text_from_node(xmltree)
        self.assertEqual(expected, result)

    def test_get_text_from_node_empty_elements(self):
        xmltree = etree.fromstring(
            '<p><xref ref-type="bibr"></xref><italic></italic></p>'
        )
        expected = ''
        result = xml_utils.get_text_from_node(xmltree)
        self.assertEqual(result, expected)

    def test_get_text_from_node_nested_elements(self):
        xmltree = etree.fromstring(
            '<p>This part is <bold>bold text only</bold>, and this part is both <bold><italic>bold and italic</italic></bold> text.</p>'
        )
        expected = 'This part is bold text only, and this part is both bold and italic text.'
        result = xml_utils.get_text_from_node(xmltree)
        self.assertEqual(expected, result)

    def test_get_text_from_node_semicolon_formatting(self):
        xmltree = etree.fromstring(
            '<p>Text; with; semicolons</p>'
        )
        expected = 'Text; with; semicolons'
        result = xml_utils.get_text_from_node(xmltree)
        self.assertEqual(expected, result)

    def test_get_text_from_node_mixed_content(self):
        xmltree = etree.fromstring(
            '<p>Start <xref ref-type="bibr">1</xref> middle <italic>emphasized</italic> end.</p>'
        )
        expected = 'Start 1 middle emphasized end.'
        result = xml_utils.get_text_from_node(xmltree)
        self.assertEqual(expected, result)

    def test_get_text_from_node_multiple_xref_italic(self):
        xmltree = etree.fromstring(
            '<p><xref ref-type="bibr">1<italic>st</italic> ref</xref> and <xref ref-type="bibr">2<italic>nd</italic> ref</xref></p>'
        )
        expected = '1st ref and 2nd ref'
        result = xml_utils.get_text_from_node(xmltree)
        self.assertEqual(expected, result)

