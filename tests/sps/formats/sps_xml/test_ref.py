import unittest
import xml.etree.ElementTree as ET
from packtools.sps.formats.sps_xml.ref import build_ref


class TestBuildRefAttribsRequired(unittest.TestCase):
    def test_build_ref_attribs_required(self):
        data = {
            "ref_id": "B1",
            "publication_type": "journal",
        }
        expected_xml_str = (
            '<ref id="B1">'
            '<element-citation publication-type="journal" />'
            '</ref>'
        )
        ref_elem = build_ref(data)
        generated_xml_str = ET.tostring(ref_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_ref_id_None(self):
        data = {
            "ref_id": None,
            "publication_type": "journal",
        }

        with self.assertRaises(ValueError) as e:
            build_ref(data)
        self.assertEqual(str(e.exception), "attribute id is required")

    def test_build_ref_publication_type_None(self):
        data = {
            "ref_id": "B1",
            "publication_type": None
        }

        with self.assertRaises(ValueError) as e:
            build_ref(data)
        self.assertEqual(str(e.exception), "attribute publication type is required")


class TestBuildRefSubElements(unittest.TestCase):
    def test_build_ref_sub_elements(self):
        data = {
            "ref_id": "B1",
            "label": "1",
            "mixed_citation": "Aires M, Paz AA, Perosa CT. Situação de saúde...",
            "publication_type": "journal",
            "article_title": "Situação de saúde e grau de...",
            "source": "Rev Gaucha Enferm",
            "year": "2009",
            "volume": "30",
            "issue": "3",
            "fpage": "192",
            "lpage": "199"
        }
        expected_xml_str = (
            '<ref id="B1">'
            '<element-citation publication-type="journal" />'
            '<label>1</label>'
            '<mixed_citation>Aires M, Paz AA, Perosa CT. Situação de saúde...</mixed_citation>'
            '<article_title>Situação de saúde e grau de...</article_title>'
            '<source>Rev Gaucha Enferm</source>'
            '<year>2009</year>'
            '<volume>30</volume>'
            '<issue>3</issue>'
            '<fpage>192</fpage>'
            '<lpage>199</lpage>'
            '</ref>'
        )
        ref_elem = build_ref(data)
        generated_xml_str = ET.tostring(ref_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_ref_sub_elements_None(self):
        data = {
            "ref_id": "B1",
            "publication_type": "journal",
            "label": None,
            "mixed_citation": None,
            "article_title": None,
            "source": None
        }
        expected_xml_str = (
            '<ref id="B1">'
            '<element-citation publication-type="journal" />'
            '</ref>'
        )
        ref_elem = build_ref(data)
        generated_xml_str = ET.tostring(ref_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())
