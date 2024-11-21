import unittest
import xml.etree.ElementTree as ET
from packtools.sps.formats.sps_xml.funding_group import build_funding_group


class TestBuildFundingGroup(unittest.TestCase):
    def test_build_funding_group(self):
        data = {
            "award-group": [
                {
                    "funding-source": ["CNPq"],
                    "award-id": ["00001", "00002"]
                },
                {
                    "funding-source": ["CNPq", "FAPESP"],
                    "award-id": ["#09/06953-4"]
                }
            ]
        }
        expected_xml_str = (
            '<funding-group>'
            '<award-group>'
            '<funding-source>CNPq</funding-source>'
            '<award-id>00001</award-id>'
            '<award-id>00002</award-id>'
            '</award-group>'
            '<award-group>'
            '<funding-source>CNPq</funding-source>'
            '<funding-source>FAPESP</funding-source>'
            '<award-id>#09/06953-4</award-id>'
            '</award-group>'
            '</funding-group>'
        )
        fn_group_elem = build_funding_group(data)
        generated_xml_str = ET.tostring(fn_group_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildFundingGroupNone(unittest.TestCase):
    def test_build_funding_group_funding_source_None(self):
        data = {
            "award-group": [
                {
                    "funding-source": None,
                    "award-id": ["00001", "00002"]
                }
            ]
        }
        with self.assertRaises(ValueError) as e:
            build_funding_group(data)

        self.assertEqual(str(e.exception), "At least one funding-source and one award-id are required")

    def test_build_funding_group_award_id_None(self):
        data = {
            "award-group": [
                {
                    "funding-source": ["CNPq"],
                    "award-id": None
                }
            ]
        }
        with self.assertRaises(ValueError) as e:
            build_funding_group(data)

        self.assertEqual(str(e.exception), "At least one funding-source and one award-id are required")

    def test_build_funding_group_award_group_None(self):
        data = {
            "award-group": None
        }

        fn_group_elem = build_funding_group(data)
        self.assertIsNone(fn_group_elem)
