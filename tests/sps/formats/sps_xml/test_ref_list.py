import unittest
from lxml import etree as ET
from packtools.sps.formats.sps_xml.ref_list import build_ref_list


class TestBuildRefList(unittest.TestCase):
    def test_build_ref_list_by_node(self):
        self.maxDiff = None
        data = {
           "title": "References",
           "ref-list-node": [
               ET.fromstring(
                   '<ref id="B1">'
                   '<label>1</label>'
                   '<element-citation publication-type="journal" />'
                   '</ref>'
               ),
               ET.fromstring(
                   '<ref id="B2">'
                   '<label>2</label>'
                   '<element-citation publication-type="journal" />'
                   '</ref>'
               )
           ]
        }
        expected_xml_str = (
            '<ref-list>'
            '<title>References</title>'
            '<ref id="B1">'
            '<label>1</label>'
            '<element-citation publication-type="journal"/>'
            '</ref>'
            '<ref id="B2"><label>2</label>'
            '<element-citation publication-type="journal"/>'
            '</ref>'
            '</ref-list>'
        )
        ref_list_elem = build_ref_list(data)
        generated_xml_str = ET.tostring(ref_list_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_ref_list_by_dict(self):
        self.maxDiff = None
        data = {
           "title": "References",
           "ref-list-dict": [
               {
                   "ref-id": "B1",
                   "label": "1",
                   "publication-type": "journal"
               },
               {
                   "ref-id": "B2",
                   "label": "2",
                   "publication-type": "journal",
               }
           ]
        }
        expected_xml_str = (
            '<ref-list>'
            '<title>References</title>'
            '<ref id="B1">'
            '<label>1</label>'
            '<element-citation publication-type="journal"/>'
            '</ref>'
            '<ref id="B2">'
            '<label>2</label>'
            '<element-citation publication-type="journal"/>'
            '</ref>'
            '</ref-list>'
        )
        ref_list_elem = build_ref_list(data)
        generated_xml_str = ET.tostring(ref_list_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_ref_list_None(self):
        data = {
           "title": "References"
        }
        with self.assertRaises(ValueError) as e:
            build_ref_list(data)
        self.assertEqual(str(e.exception), "A list of references is required")

    def test_build_ref_list_title_None(self):
        data = {
           "title": None
        }
        with self.assertRaises(ValueError) as e:
            build_ref_list(data)
        self.assertEqual(str(e.exception), "Title is required")