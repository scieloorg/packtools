import unittest
from lxml import etree as ET
from packtools.sps.formats.sps_xml.abstract import build_abstract, build_visual_abstract, build_trans_abstract, build_highlights


class TestBuildStructuredAbstractTitle(unittest.TestCase):
    def test_build_structured_abstract_title(self):
        data = {
            "title": "Resumo"
        }
        expected_xml_str = (
            '<abstract>'
            '<title>Resumo</title>'
            '</abstract>'
        )
        abstract_elem = build_abstract(data)
        generated_xml_str = ET.tostring(abstract_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_structured_abstract_title_None(self):
        data = {
            "title": None
        }
        with self.assertRaises(ValueError) as e:
            build_abstract(data)
        self.assertEqual(str(e.exception), "title is required")


class TestBuildStructuredAbstractSections(unittest.TestCase):
    def test_build_structured_abstract_sections(self):
        data = {
            "title": "Resumo",
            "secs": [
                {
                    "title": "Objetivo",
                    "p": "Verificar a sensibilidade e especificidade ..."
                },
                {
                    "title": "Métodos",
                    "p": "Durante quatro meses foram selecionados ..."
                }
            ]
        }
        expected_xml_str = (
            '<abstract>'
            '<title>Resumo</title>'
            '<sec>'
            '<title>Objetivo</title>'
            '<p>Verificar a sensibilidade e especificidade ...</p>'
            '</sec>'
            '<sec>'
            '<title>Métodos</title>'
            '<p>Durante quatro meses foram selecionados ...</p>'
            '</sec>'
            '</abstract>'
        )
        abstract_elem = build_abstract(data)
        generated_xml_str = ET.tostring(abstract_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_structured_abstract_sections_None(self):
        data = {
            "title": "Resumo",
            "secs": None
        }
        expected_xml_str = (
            '<abstract>'
            '<title>Resumo</title>'
            '</abstract>'
        )
        abstract_elem = build_abstract(data)
        generated_xml_str = ET.tostring(abstract_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_structured_abstract_sections_attribs_None(self):
        data = {
            "title": "Resumo",
            "secs": [
                {
                    "title": None,
                    "p": None
                },
                {
                    "title": None,
                    "p": None
                }
            ]
        }
        expected_xml_str = (
            '<abstract>'
            '<title>Resumo</title>'
            '</abstract>'
        )
        abstract_elem = build_abstract(data)
        generated_xml_str = ET.tostring(abstract_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildSimpleAbstractTitle(unittest.TestCase):
    def test_build_simple_abstract_title(self):
        data = {
            "title": "Resumo"
        }
        expected_xml_str = (
            '<abstract>'
            '<title>Resumo</title>'
            '</abstract>'
        )
        abstract_elem = build_abstract(data)
        generated_xml_str = ET.tostring(abstract_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_simple_abstract_title_None(self):
        data = {
            "title": None
        }
        with self.assertRaises(ValueError) as e:
            build_abstract(data)
        self.assertEqual(str(e.exception), "title is required")


class TestBuildSimpleAbstractParagraph(unittest.TestCase):
    def test_build_simple_abstract_paragraph(self):
        data = {
            "title": "Resumo",
            "p": "Verificar a sensibilidade e especificidade ..."
        }
        expected_xml_str = (
            '<abstract>'
            '<title>Resumo</title><'
            'p>Verificar a sensibilidade e especificidade ...</p>'
            '</abstract>'
        )
        abstract_elem = build_abstract(data)
        generated_xml_str = ET.tostring(abstract_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_simple_abstract_paragraph_None(self):
        data = {
            "title": "Resumo",
            "p": None
        }
        expected_xml_str = (
            '<abstract>'
            '<title>Resumo</title>'
            '</abstract>'
        )
        abstract_elem = build_abstract(data)
        generated_xml_str = ET.tostring(abstract_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildVisualAbstractTitle(unittest.TestCase):
    def test_build_visual_abstract_title(self):
        data = {
            "title": "Visual Abstract",
            "fig_id": "vf01",
        }
        expected_xml_str = (
            '<abstract abstract-type="graphical">'
            '<title>Visual Abstract</title>'
            '<p>'
            '<fig id="vf01"/>'
            '</p>'
            '</abstract>'
        )
        abstract_elem = build_visual_abstract(data)
        generated_xml_str = ET.tostring(abstract_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_visual_abstract_title_None(self):
        data = {
            "title": None
        }
        with self.assertRaises(ValueError) as e:
            build_visual_abstract(data)
        self.assertEqual(str(e.exception), "title is required")


class TestBuildVisualAbstractCaption(unittest.TestCase):
    def test_build_visual_abstract_caption(self):
        data = {
            "title": "Visual Abstract",
            "fig_id": "vf01",
            "caption": "Título",
        }
        expected_xml_str = (
            '<abstract abstract-type="graphical">'
            '<title>Visual Abstract</title>'
            '<p>'
            '<fig id="vf01">'
            '<caption>'
            '<title>Título</title>'
            '</caption>'
            '</fig>'
            '</p>'
            '</abstract>'
        )
        abstract_elem = build_visual_abstract(data)
        generated_xml_str = ET.tostring(abstract_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_visual_abstract_caption_None(self):
        data = {
            "title": "Visual Abstract",
            "fig_id": "vf01",
            "caption": None
        }
        expected_xml_str = (
            '<abstract abstract-type="graphical">'
            '<title>Visual Abstract</title>'
            '<p>'
            '<fig id="vf01"/>'
            '</p>'
            '</abstract>'
        )
        abstract_elem = build_visual_abstract(data)
        generated_xml_str = ET.tostring(abstract_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildVisualAbstractHref(unittest.TestCase):
    def test_build_visual_abstract_href(self):
        data = {
            "title": "Visual Abstract",
            "fig_id": "vf01",
            "href": "1234-5678-zwy-12-04-0123-vs01.tif"
        }
        expected_xml_str = (
            '<abstract abstract-type="graphical">'
            '<title>Visual Abstract</title>'
            '<p>'
            '<fig id="vf01">'
            '<graphic xmlns:ns0="http://www.w3.org/1999/xlink" ns0:href="1234-5678-zwy-12-04-0123-vs01.tif"/>'
            '</fig>'
            '</p>'
            '</abstract>'
        )
        abstract_elem = build_visual_abstract(data)
        generated_xml_str = ET.tostring(abstract_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_visual_abstract_href_None(self):
        data = {
            "title": "Visual Abstract",
            "fig_id": "vf01",
            "href": None
        }
        expected_xml_str = (
            '<abstract abstract-type="graphical">'
            '<title>Visual Abstract</title>'
            '<p>'
            '<fig id="vf01"/>'
            '</p>'
            '</abstract>'
        )
        abstract_elem = build_visual_abstract(data)
        generated_xml_str = ET.tostring(abstract_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildTransAbstractTitle(unittest.TestCase):
    def test_build_structured_abstract_title(self):
        data = {
            "title": "Resumo",
            "lang": "pt",
            "secs": [
                {
                    "title": "Objetivo",
                    "p": "Verificar a sensibilidade e especificidade ..."
                },
                {
                    "title": "Métodos",
                    "p": "Durante quatro meses foram selecionados ..."
                }
            ]
        }
        expected_xml_str = (
            '<trans-abstract xml:lang="pt">'
            '<title>Resumo</title>'
            '<sec>'
            '<title>Objetivo</title>'
            '<p>Verificar a sensibilidade e especificidade ...</p>'
            '</sec>'
            '<sec>'
            '<title>Métodos</title>'
            '<p>Durante quatro meses foram selecionados ...</p>'
            '</sec>'
            '</trans-abstract>'
        )
        abstract_elem = build_trans_abstract(data)
        generated_xml_str = ET.tostring(abstract_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildHighlightTitle(unittest.TestCase):
    def test_build_highlight_title(self):
        data = {
            "title": "Highlights",
        }
        expected_xml_str = (
            '<abstract abstract-type="key-points">'
            '<title>Highlights</title>'
            '</abstract>'
        )
        abstract_elem = build_highlights(data)
        generated_xml_str = ET.tostring(abstract_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_highlight_title_None(self):
        data = {
            "title": None
        }
        with self.assertRaises(ValueError) as e:
            build_highlights(data)
        self.assertEqual(str(e.exception), "title is required")


class TestBuildHighlightItems(unittest.TestCase):
    def test_build_highlight_items(self):
        data = {
            "title": "Highlights",
            "highlights": [
                "highlight 1",
                "highlight 2",
                "highlight 3",
            ]
        }
        expected_xml_str = (
            '<abstract abstract-type="key-points">'
            '<title>Highlights</title>'
            '<p>highlight 1</p>'
            '<p>highlight 2</p>'
            '<p>highlight 3</p>'
            '</abstract>'
        )
        abstract_elem = build_highlights(data)
        generated_xml_str = ET.tostring(abstract_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_highlight_items_None(self):
        data = {
            "title": "Highlights",
            "highlights": None
        }
        expected_xml_str = (
            '<abstract abstract-type="key-points">'
            '<title>Highlights</title>'
            '</abstract>'
        )
        abstract_elem = build_highlights(data)
        generated_xml_str = ET.tostring(abstract_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())
