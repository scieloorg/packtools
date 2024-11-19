import unittest
import xml.etree.ElementTree as ET
from packtools.sps.formats.sps_xml.back import build_back


class TestBuildBack(unittest.TestCase):
    def test_build_back(self):
        self.maxDiff = None
        node = {
            "ack": [
                ET.fromstring(
                    '<ack>'
                    '<title>Acknowledgments</title>'
                    '<p>Federal University of Rio de Janeiro (UFRJ), School of Medicine,...</p>'
                    '<p>This study was funded by the Hospital Municipal Conde Modesto Leal...</p>'
                    '</ack>'
                )
            ],
            "ref-list": [
                ET.fromstring(
                    '<ref-list>'
                    '<title>References</title>'
                    '<ref id="B1">'
                    '<label>1</label>'
                    '<mixed-citation>Goldberg DS, McGee SJ. Pain as a global public health priority. BMC Public Health. 2011;11:770.</mixed-citation>'
                    '<element-citation publication-type="journal">'
                    '<person-group person-group-type="author">'
                    '<name>'
                    '<surname>Goldberg</surname>'
                    '<given-names>DS</given-names>'
                    '</name>'
                    '</person-group>'
                    '<article-title>Pain as a global public health priority</article-title>'
                    '<source>BMC Public Health</source>'
                    '<volume>11</volume>'
                    '<year>2011</year>'
                    '<fpage>770</fpage>'
                    '</element-citation>'
                    '</ref>'
                    '</ref-list>'
                )
            ]
        }
        expected_xml_str = (
            '<back>'
            '<ack>'
            '<title>Acknowledgments</title>'
            '<p>Federal University of Rio de Janeiro (UFRJ), School of Medicine,...</p>'
            '<p>This study was funded by the Hospital Municipal Conde Modesto Leal...</p>'
            '</ack>'
            '<ref-list>'
            '<title>References</title>'
            '<ref id="B1">'
            '<label>1</label>'
            '<mixed-citation>Goldberg DS, McGee SJ. Pain as a global public health priority. BMC Public Health. 2011;11:770.</mixed-citation>'
            '<element-citation publication-type="journal">'
            '<person-group person-group-type="author">'
            '<name>'
            '<surname>Goldberg</surname>'
            '<given-names>DS</given-names>'
            '</name>'
            '</person-group>'
            '<article-title>Pain as a global public health priority</article-title>'
            '<source>BMC Public Health</source>'
            '<volume>11</volume>'
            '<year>2011</year>'
            '<fpage>770</fpage>'
            '</element-citation>'
            '</ref>'
            '</ref-list>'
            '</back>'
        )
        back_elem = build_back(node)
        generated_xml_str = ET.tostring(back_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_back_None(self):
        node = {}
        with self.assertRaises(ValueError) as e:
            build_back(node)
        self.assertEqual(str(e.exception), "A list of child elements is required.")
