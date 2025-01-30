# coding: utf-8
import unittest

from lxml import etree

from packtools.sps.utils import xml_utils


class XMLUtilsTest(unittest.TestCase):

    def test_node_plain_text(self):
        xml = etree.fromstring(
            "<root>"
            "<title>Texto 1    <italic>italico</italic> TExto 2"
            "<xref><sup><bold>1</bold></sup></xref> "
            "         "
            "Texto 3</title></root>"
        )
        expected = "Texto 1 italico TExto 2 Texto 3"
        result = xml_utils.node_plain_text(xml.find(".//title"))
        self.assertEqual(expected, result)

    def test_node_text_without_xref(self):
        xml = etree.fromstring(
            "<root>"
            "<title>Texto 1    <italic>italico</italic> TExto 2"
            "<xref><sup><bold>1</bold></sup></xref> Texto 3</title></root>"
        )
        expected = "Texto 1    <italic>italico</italic> TExto 2 Texto 3"
        node = xml.find(".//title")
        result = xml_utils.node_text_without_fn_xref(node)
        self.assertEqual(expected, result)

