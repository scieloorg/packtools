import unittest
import xml.etree.ElementTree as ET
from packtools.sps.formats.sps_xml.ack import build_ack


class TestBuildAck(unittest.TestCase):
    def test_build_ack(self):
        data = {
            "title": "Agradecimentos",
            "paragraphs": ["Texto de agradecimento"]
        }
        expected_xml_str = (
            '<ack>'
            '<title>Agradecimentos</title>'
            '<p>Texto de agradecimento</p>'
            '</ack>'
        )
        ack_elem = build_ack(data)
        generated_xml_str = ET.tostring(ack_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_ack_title_None(self):
        data = {
            "title": None,
            "paragraphs": ["Texto de agradecimento"]
        }
        expected_xml_str = (
            '<ack>'
            '<p>Texto de agradecimento</p>'
            '</ack>'
        )
        ack_elem = build_ack(data)
        generated_xml_str = ET.tostring(ack_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_ack_paragraph_None(self):
        data = {
            "title": "Agradecimentos",
            "paragraphs": None
        }
        expected_xml_str = (
            '<ack>'
            '<title>Agradecimentos</title>'
            '</ack>'
        )
        ack_elem = build_ack(data)
        generated_xml_str = ET.tostring(ack_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())
