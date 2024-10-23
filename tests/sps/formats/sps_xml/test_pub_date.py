import unittest
import xml.etree.ElementTree as ET
from packtools.sps.formats.sps_xml.pub_date import build_pub_dates


class TestBuildPubDate(unittest.TestCase):
    def test_build_pub_dates(self):
        data = {
            "pub": {
                "day": "01",
                "month": "01",
                "year": "2024"
            },
            "collection": {
                "season": "Jan-Fev",
                "year": "2024"
            }
        }
        expected_xml_str = [
            (
                '<pub-date publication-format="electronic" date-type="pub">'
                '<day>01</day>'
                '<month>01</month>'
                '<year>2024</year>'
                '</pub-date>'
            ),
            (
                '<pub-date publication-format="electronic" date-type="collection">'
                '<season>Jan-Fev</season>'
                '<year>2024</year>'
                '</pub-date>'
            )
        ]
        for item, pub_date_elem in enumerate(build_pub_dates(data)):
            generated_xml_str = ET.tostring(pub_date_elem, encoding="unicode", method="xml")
            with self.subTest(item):
                self.assertEqual(generated_xml_str.strip(), expected_xml_str[item].strip())

    def test_build_pub_dates_None(self):
        data = {
            "pub": {
                "day": None,
                "month": None,
                "year": None
            },
            "collection": None
        }

        pub_date_elem = list(build_pub_dates(data))
        self.assertEqual(len(pub_date_elem), 0)
