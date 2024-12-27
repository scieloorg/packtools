import unittest
from lxml import etree as ET
from packtools.sps.formats.sps_xml.table_wrap import build_table_wrap


class TestBuildTableExceptions(unittest.TestCase):

    def test_build_table_wrap_without_table(self):
        data = {
            "table-wrap-id": "t01",
            "tables": None
        }
        with self.assertRaises(ValueError) as e:
            build_table_wrap(data)
        self.assertEqual(str(e.exception), "At least one representation of the table is required")

    def test_build_table_wrap_codification_invalid(self):
        data = {
            "table-wrap-id": "t01",
            "tables": [{"formula": "codificação da formula"}]
        }
        with self.assertRaises(ValueError) as e:
            build_table_wrap(data)
        self.assertEqual(str(e.exception), "A valid codification type ('table' or 'graphic') is required.")

    def test_build_table_wrap_without_id(self):
        data = {
            "table-wrap-id": None,
            "tables": [{"table": "codificação da tabela"}]
        }
        with self.assertRaises(ValueError) as e:
            build_table_wrap(data)
        self.assertEqual(str(e.exception), "Attrib table-wrap-id is required")


class TestBuildTableLabel(unittest.TestCase):

    def test_build_table_wrap_label(self):
        data = {
            "table-wrap-id": "t01",
            "label": "Table 1",
            "tables": [{"table": "codificação da tabela"}]
        }
        expected_xml_str = (
            '<table-wrap id="t01">'
            '<label>Table 1</label>'
            '<table>codificação da tabela</table>'
            '</table-wrap>'
        )

        table_elem = build_table_wrap(data)
        generated_xml_str = ET.tostring(table_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_table_wrap_label_None(self):
        data = {
            "table-wrap-id": "t01",
            "label": None,
            "tables": [{"table": "codificação da tabela"}]
        }
        expected_xml_str = (
            '<table-wrap id="t01">'
            '<table>codificação da tabela</table>'
            '</table-wrap>'
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
            "tables": [{"table": "codificação da tabela"}]
        }
        expected_xml_str = (
            '<table-wrap id="t01">'
            '<caption>'
            '<title>Título da tabela</title>'
            '<p>Deaths Among Patients...</p>'
            '</caption>'
            '<table>codificação da tabela</table>'
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
            "tables": [{"table": "codificação da tabela"}]
        }
        expected_xml_str = (
            '<table-wrap id="t01">'
            '<caption>'
            '<p>Deaths Among Patients...</p>'
            '</caption>'
            '<table>codificação da tabela</table>'
            '</table-wrap>'
        )

        table_elem = build_table_wrap(data)
        generated_xml_str = ET.tostring(table_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_table_wrap_caption_p_None(self):
        data = {
            "table-wrap-id": "t01",
            "caption-title": "Título da tabela",
            "caption-p": None,
            "tables": [{"table": "codificação da tabela"}]
        }
        expected_xml_str = (
            '<table-wrap id="t01">'
            '<caption>'
            '<title>Título da tabela</title>'
            '</caption>'
            '<table>codificação da tabela</table>'
            '</table-wrap>'
        )

        table_elem = build_table_wrap(data)
        generated_xml_str = ET.tostring(table_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildTableFootnotes(unittest.TestCase):

    def test_build_table_wrap_footnotes_id(self):
        data = {
            "table-wrap-id": "t01",
            "fns": [{"fn-id": None}],
            "tables": [{"table": "codificação da tabela"}]
        }
        with self.assertRaises(ValueError) as e:
            build_table_wrap(data)
        self.assertEqual(str(e.exception), "fn-id is required")

    def test_build_table_wrap_footnotes_None(self):
        data = {
            "table-wrap-id": "t01",
            "fns": None,
            "tables": [{"table": "codificação da tabela"}]
        }
        expected_xml_str = (
            '<table-wrap id="t01">'
            '<table>codificação da tabela</table>'
            '</table-wrap>'
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
            ],
            "tables": [{"table": "codificação da tabela"}]
        }
        expected_xml_str = (
            '<table-wrap id="t01">'
            '<table-wrap-foot>'
            '<fn id="fn01"/>'
            '</table-wrap-foot>'
            '<table>codificação da tabela</table>'
            '</table-wrap>'
        )

        table_elem = build_table_wrap(data)
        generated_xml_str = ET.tostring(table_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildTableAlternatives(unittest.TestCase):

    def test_build_table_wrap_alternatives(self):
        data = {
            "table-wrap-id": "t01",
            "tables": [
                {
                    "graphic": "nomedaimagemdatabela.svg",
                    "id": "g1"
                },
                {
                    "table": "codificação da tabela"
                }
            ]
        }
        expected_xml_str = (
            '<table-wrap id="t01">'
            '<alternatives>'
            '<graphic xmlns:ns0="http://www.w3.org/1999/xlink" '
            'ns0:href="nomedaimagemdatabela.svg" id="g1"/>'
            '<table>codificação da tabela</table>'
            '</alternatives>'
            '</table-wrap>'
        )

        table_elem = build_table_wrap(data)
        generated_xml_str = ET.tostring(table_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())
