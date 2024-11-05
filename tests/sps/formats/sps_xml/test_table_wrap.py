import unittest
import xml.etree.ElementTree as ET
from packtools.sps.formats.sps_xml.table_wrap import build_table_wrap


class TestBuildTableId(unittest.TestCase):

    def test_build_table_wrap_without_id(self):
        data = {
            "table-wrap-id": None
        }
        with self.assertRaises(ValueError) as e:
            build_table_wrap(data)
        self.assertEqual(str(e.exception), "Attrib table-wrap-id is required")


class TestBuildTableLabel(unittest.TestCase):

    def test_build_table_wrap_label(self):
        data = {
            "table-wrap-id": "t01",
            "label": "Table 1",
        }
        expected_xml_str = (
            '<table-wrap id="t01">'
            '<label>Table 1</label>'
            '</table-wrap>'
        )

        table_elem = build_table_wrap(data)
        generated_xml_str = ET.tostring(table_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_table_wrap_label_None(self):
        data = {
            "table-wrap-id": "t01",
            "label": None
        }
        expected_xml_str = (
            '<table-wrap id="t01" />'
        )

        table_elem = build_table_wrap(data)
        generated_xml_str = ET.tostring(table_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildTableCaption(unittest.TestCase):

    def test_build_table_wrap_caption(self):
        data = {
            "table-wrap-id": "t01",
            "caption-title": "Título da tabela",
            "caption-p": ["Deaths Among Patients..."],
        }
        expected_xml_str = (
            '<table-wrap id="t01">'
            '<caption>'
            '<title>Título da tabela</title>'
            '<p>Deaths Among Patients...</p>'
            '</caption>'
            '</table-wrap>'
        )

        table_elem = build_table_wrap(data)
        generated_xml_str = ET.tostring(table_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_table_wrap_caption_title_None(self):
        data = {
            "table-wrap-id": "t01",
            "caption-title": None,
            "caption-p": ["Deaths Among Patients..."],
        }
        expected_xml_str = (
            '<table-wrap id="t01">'
            '<caption>'
            '<p>Deaths Among Patients...</p>'
            '</caption>'
            '</table-wrap>'
        )

        table_elem = build_table_wrap(data)
        generated_xml_str = ET.tostring(table_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_table_wrap_caption_p_None(self):
        data = {
            "table-wrap-id": "t01",
            "caption-title": "Título da tabela",
            "caption-p": None
        }
        expected_xml_str = (
            '<table-wrap id="t01">'
            '<caption>'
            '<title>Título da tabela</title>'
            '</caption>'
            '</table-wrap>'
        )

        table_elem = build_table_wrap(data)
        generated_xml_str = ET.tostring(table_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildTableFootnotes(unittest.TestCase):

    def test_build_table_wrap_footnotes_id(self):
        data = {
            "table-wrap-id": "t01",
            "fns": [
                {
                    "fn-id": None
                }
            ]
        }
        with self.assertRaises(ValueError) as e:
            build_table_wrap(data)
        self.assertEqual(str(e.exception), "fn-id is required")

    def test_build_table_wrap_footnotes_None(self):
        data = {
            "table-wrap-id": "t01",
            "fns": None
        }
        expected_xml_str = (
            '<table-wrap id="t01" />'
        )

        table_elem = build_table_wrap(data)
        generated_xml_str = ET.tostring(table_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_table_wrap_footnotes_sub_elements_None(self):
        data = {
            "table-wrap-id": "t01",
            "fns": [
                {
                    "fn-id": "fn01",
                    "fn-label": None
                }
            ]
        }
        expected_xml_str = (
            '<table-wrap id="t01">'
            '<table-wrap-foot>'
            '<fn id="fn01" />'
            '</table-wrap-foot>'
            '</table-wrap>'
        )

        table_elem = build_table_wrap(data)
        generated_xml_str = ET.tostring(table_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())
