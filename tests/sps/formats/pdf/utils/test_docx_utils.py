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
