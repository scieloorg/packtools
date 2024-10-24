import unittest
import xml.etree.ElementTree as ET
from packtools.sps.formats.sps_xml.history import build_history


class TestBuildHistory(unittest.TestCase):
    def test_build_history(self):
        data = {
            "received": {
                "day": "15",
                "month": "03",
                "year": "2013"
            },
            "rev-recd": {
                "day": "06",
                "month": "11",
                "year": "2013"
            }
        }
        expected_xml_str = (
            '<history>'
            '<date date-type="received">'
            '<day>15</day>'
            '<month>03</month>'
            '<year>2013</year>'
            '</date>'
            '<date date-type="rev-recd">'
            '<day>06</day>'
            '<month>11</month>'
            '<year>2013</year>'
            '</date>'
            '</history>'
        )
        history_elem = build_history(data)
        generated_xml_str = ET.tostring(history_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_history_None(self):
        data = {
            "received": None,
            "rev-recd": {
                "day": None,
                "month": None,
                "year": None
            }
        }

        expected_xml_str = (
            '<history />'
        )
        history_elem = build_history(data)
        generated_xml_str = ET.tostring(history_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())
