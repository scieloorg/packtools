import unittest
import xml.etree.ElementTree as ET
from packtools.sps.formats.sps_xml.author_notes import build_author_notes


class TestBuildAuthorNotesCorrespId(unittest.TestCase):
    def test_build_author_notes_corresp_id(self):
        data = {
            "corresp_id": "c01",
        }
        expected_xml_str = (
            '<author-notes>'
            '<corresp id="c01" />'
            '</author-notes>'
        )
        author_notes_elem = build_author_notes(data)
        generated_xml_str = ET.tostring(author_notes_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_author_notes_corresp_id_None(self):
        data = {
            "corresp_id": None
        }
        expected_xml_str = (
            '<author-notes />'
        )
        author_notes_elem = build_author_notes(data)
        generated_xml_str = ET.tostring(author_notes_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildAuthorNotesCorrespLabel(unittest.TestCase):
    def test_build_author_notes_corresp_label(self):
        data = {
            "corresp_label": "*",
        }
        expected_xml_str = (
            '<author-notes>'
            '<corresp />'
            '</author-notes>'
        )
        author_notes_elem = build_author_notes(data)
        generated_xml_str = ET.tostring(author_notes_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_author_notes_corresp_label_None(self):
        data = {
            "corresp_label": None
        }
        expected_xml_str = (
            '<author-notes />'
        )
        author_notes_elem = build_author_notes(data)
        generated_xml_str = ET.tostring(author_notes_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildAuthorNotesCorrespText(unittest.TestCase):
    def test_build_author_notes_corresp_text(self):
        data = {
            "corresp_text": "Correspondence Dr. Edmundo Figueira Departamento de Fisioterapia, Universidade FISP - Hogwarts,  Brasil."
        }
        expected_xml_str = (
            '<author-notes>'
            '<corresp>'
            'Correspondence Dr. Edmundo Figueira Departamento de Fisioterapia, Universidade FISP - Hogwarts,  Brasil.'
            '</corresp>'
            '</author-notes>'
        )
        author_notes_elem = build_author_notes(data)
        generated_xml_str = ET.tostring(author_notes_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_author_notes_corresp_text_None(self):
        data = {
            "corresp_text": None
        }
        expected_xml_str = (
            '<author-notes />'
        )
        author_notes_elem = build_author_notes(data)
        generated_xml_str = ET.tostring(author_notes_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildAuthorNotesCorrespEmail(unittest.TestCase):
    def test_build_author_notes_corresp_email(self):
        data = {
            "corresp_email": "contato@foo.com"
        }
        expected_xml_str = (
            '<author-notes>'
            '<corresp>'
            '<email>contato@foo.com</email>'
            '</corresp>'
            '</author-notes>'
        )
        author_notes_elem = build_author_notes(data)
        generated_xml_str = ET.tostring(author_notes_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_author_notes_corresp_email_None(self):
        data = {
            "corresp_email": None
        }
        expected_xml_str = (
            '<author-notes />'
        )
        author_notes_elem = build_author_notes(data)
        generated_xml_str = ET.tostring(author_notes_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildAuthorNotesFootnotes(unittest.TestCase):
    def test_build_author_notes_fn(self):
        data = {
            "fns": {
                "conflict": "Não há conflito de interesse entre os autores do artigo.",
                "equal": "Todos os autores tiveram contribuição igualitária na criação do artigo."
            }
        }
        expected_xml_str = (
            '<author-notes>'
            '<fn fn-type="conflict">'
            '<p>Não há conflito de interesse entre os autores do artigo.</p>'
            '</fn>'
            '<fn fn-type="equal">'
            '<p>Todos os autores tiveram contribuição igualitária na criação do artigo.</p>'
            '</fn>'
            '</author-notes>'
        )
        author_notes_elem = build_author_notes(data)
        generated_xml_str = ET.tostring(author_notes_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_author_notes_fn_None(self):
        data = {
            "fns": {
                "conflict": None,
                "equal": None
            }
        }
        expected_xml_str = (
            '<author-notes />'
        )
        author_notes_elem = build_author_notes(data)
        generated_xml_str = ET.tostring(author_notes_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())
