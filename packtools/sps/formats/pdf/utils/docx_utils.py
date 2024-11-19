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
def get_first_section(docx):
    """
    Gets the first section of the given docx document.

    Args:
        docx (python-docx.Document): The docx document to get the first section from.

    Returns:
        python-docx.Section: The first section of the docx document.
    """
    try:
        return docx.sections[0]
    except IndexError:
        docx.add_section()
        return docx.sections[0]

def get_or_create_second_section(docx):
    """
    Get or create the second section of a DOCX document.

    If the document has only one section, a new section is added.
    Returns the second section of the document.

    Parameters:
    docx (Document): A python-docx Document object.

    Returns:
    Section: The second section of the DOCX document.
    """
    while len(docx.sections) < 2:
        docx.add_section()
    return docx.sections[1]

def get_first_page_header(docx):
    """
    Retrieves the first page header from the first section of a DOCX document.

    Args:
        docx: A DOCX document object.

    Returns:
        The first page header of the first section of the DOCX document.
    """
    section = get_first_section(docx)
    return section.first_page_header

def get_first_page_footer(docx):
    """
    Retrieves the first page footer from the first section of a DOCX document.

    Args:
        docx: A DOCX document object.

    Returns:
        The first page footer of the first section of the DOCX document.
    """
    section = get_first_section(docx)
    return section.first_page_footer

def get_second_header(docx):
    """
    Retrieves the header of the second section in a DOCX document.

    Args:
        docx (Document): A python-docx Document object representing the DOCX file.

    Returns:
        Header: The header of the second section in the DOCX document.
    """
    section = get_or_create_second_section(docx)
    return section.header

def get_second_footer(docx):
    """
    Retrieves the footer of the second section in a DOCX document.

    Args:
        docx (docx.Document): The DOCX document object.

    Returns:
        docx.section.SectionFooter: The footer of the second section in the DOCX document.
    """
    section = get_or_create_second_section(docx)
    return section.footer

def get_first_paragraph(element):
    """
    Retrieves the first paragraph from a given document element.

    Args:
        element: A document element that contains paragraphs.

    Returns:
        The first paragraph of the given element.
    """
    try:
        return element.paragraphs[0]
    except KeyError:
        element.add_paragraph()
        return element.paragraphs[0]
