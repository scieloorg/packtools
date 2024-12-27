import unittest
from lxml import etree as ET
from packtools.sps.formats.sps_xml.history import build_history


class TestBuildHistory(unittest.TestCase):
    def test_build_history(self):
        data = [
            {
                "date_type": "received",
                "day": "15",
                "month": "03",
                "year": "2013"
            },
            {
                "date_type": "rev-recd",
                "day": "06",
                "month": "11",
                "year": "2013"
            }
        ]
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

    def test_build_history_date_type_None(self):
        data = [
            {
                "date_type": None,
                "year": "2013"
            }
        ]
        with self.assertRaises(ValueError) as e:
            build_history(data)
        self.assertEqual(str(e.exception), "date_type is required")

    def test_build_history_day_or_month_None(self):
        data = [
            {
                "date_type": "received",
                "day": None,
                "month": None,
                "year": "2013"
            }
        ]
        expected_xml_str = (
            '<history>'
            '<date date-type="received">'
            '<year>2013</year>'
            '</date>'
            '</history>'
        )
        history_elem = build_history(data)
        generated_xml_str = ET.tostring(history_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_history_year_None(self):
        data = [
            {
                "date_type": "received",
                "year": None
            }
        ]
        with self.assertRaises(ValueError) as e:
            build_history(data)
        self.assertEqual(str(e.exception), "year is required")

    def test_build_history_order(self):
        data = [
            {
                "date_type": "received",
                "year": "2013",
                "month": "03",
                "day": "15"
            }
        ]
        expected_xml_str = (
            '<history>'
            '<date date-type="received">'
            '<day>15</day>'
            '<month>03</month>'
            '<year>2013</year>'
            '</date>'
            '</history>'
        )
        history_elem = build_history(data)
        generated_xml_str = ET.tostring(history_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())
