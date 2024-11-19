import unittest

from docx import Document
from docx.shared import RGBColor

from packtools.sps.formats.pdf import enum as pdf_enum
from packtools.sps.formats.pdf.utils import docx_utils


class TestDocxUtils(unittest.TestCase):

    def setUp(self):
        self.doc = Document()
        self.doc.add_section()
        self.first_paragraph_text = 'This is the first paragraph.'
        self.doc.paragraphs[0].text = self.first_paragraph_text

    def test_get_first_section_is_not_none(self):
        first_section = docx_utils.get_first_section(self.doc)
        self.assertIsNotNone(first_section)

    def test_get_or_create_second_section_is_not_none(self):
        second_section = docx_utils.get_or_create_second_section(self.doc)
        self.assertIsNotNone(second_section)

    def test_get_first_page_header_is_not_none(self):
        header = docx_utils.get_first_page_header(self.doc)
        self.assertIsNotNone(header)

    def test_get_second_header_is_not_none(self):
        header = docx_utils.get_second_header(self.doc)
        self.assertIsNotNone(header)

    def test_get_first_page_footer_is_not_none(self):
        footer = docx_utils.get_first_page_footer(self.doc)
        self.assertIsNotNone(footer)

    def test_get_second_footer_is_not_none(self):
        footer = docx_utils.get_second_footer(self.doc)
        self.assertIsNotNone(footer)

    def test_get_first_paragraph(self):
        first_paragraph = docx_utils.get_first_paragraph(self.doc)
        self.assertEqual(self.first_paragraph_text, first_paragraph.text)
