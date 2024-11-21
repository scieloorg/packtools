import unittest
import xml.etree.ElementTree as ET
from packtools.sps.formats.sps_xml.fig import build_fig


class TestBuildFig(unittest.TestCase):

    def test_build_fig_without_id(self):
        data = {
            "fig-id": None,
        }
        with self.assertRaises(ValueError) as e:
            build_fig(data)
        self.assertEqual(str(e.exception), "Attrib id is required")


class TestBuildFigType(unittest.TestCase):

    def test_build_fig_type(self):
        data = {"fig-id": "f01", "fig-type": "map"}
        expected_xml_str = '<fig id="f01" fig-type="map" />'
        fig_elem = build_fig(data)
        generated_xml_str = ET.tostring(fig_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildFigLabel(unittest.TestCase):

    def test_build_fig_label(self):
        data = {"fig-id": "f01", "fig-type": "map", "label": "Figure 1"}
        expected_xml_str = (
            '<fig id="f01" fig-type="map">' "<label>Figure 1</label>" "</fig>"
        )
        fig_elem = build_fig(data)
        generated_xml_str = ET.tostring(fig_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildFigCaption(unittest.TestCase):

    def test_build_fig_caption_without_title(self):
        data = {"fig-id": "f01", "caption-p": ["Deaths Among Patients..."]}
        expected_xml_str = (
            '<fig id="f01">'
            "<caption>"
            "<p>Deaths Among Patients...</p>"
            "</caption>"
            "</fig>"
        )
        fig_elem = build_fig(data)
        generated_xml_str = ET.tostring(fig_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_fig_caption_without_paragraphs(self):
        data = {
            "fig-id": "f01",
            "caption-title": "Título de figura",
        }
        expected_xml_str = (
            '<fig id="f01">'
            "<caption>"
            "<title>Título de figura</title>"
            "</caption>"
            "</fig>"
        )
        fig_elem = build_fig(data)
        generated_xml_str = ET.tostring(fig_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildFigXlink(unittest.TestCase):

    def test_build_fig_xlink(self):
        data = {
            "fig-id": "f01",
            "graphic": "1234-5678-zwy-12-04-0123-gf02.tif",
        }
        expected_xml_str = (
            '<fig id="f01">'
            '<graphic xlink:href="1234-5678-zwy-12-04-0123-gf02.tif" />'
            "</fig>"
        )
        fig_elem = build_fig(data)
        generated_xml_str = ET.tostring(fig_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildFigAttrib(unittest.TestCase):

    def test_build_fig_attrib(self):
        data = {"fig-id": "f01", "attrib": "Fonte: IBGE (2018)"}
        expected_xml_str = (
            '<fig id="f01">' "<attrib>Fonte: IBGE (2018)</attrib>" "</fig>"
        )
        fig_elem = build_fig(data)
        generated_xml_str = ET.tostring(fig_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())
