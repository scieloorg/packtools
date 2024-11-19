from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_PARAGRAPH_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

from packtools.sps.formats.pdf import enum as pdf_enum


def init_docx(data):
    """
    Initialize a DOCX document with optional base layout.

    Args:
        data: Additional data for the DOCX generation.

    Returns:
        A DOCX Document object.
    """
    source_layout = data.get('base_layout')
    if not source_layout:
        return Document()

    source_docx = Document(source_layout)
    docx = Document()
    copy_styles(source_docx, docx)

    return docx
