from docx.oxml import OxmlElement
from docx.oxml.ns import qn

from packtools.sps.formats.pdf import enum as pdf_enum


def docx_setup_sections(docx, page_attributes=pdf_enum.PAGE_ATTRIBUTES):
    """
    Apply page attributes to all sections in the document.
    Link headers/footers appropriately: first section first page different, second section onwards link headers/footers.
    """
    for ind, sec in enumerate(docx.sections):
        _apply_header_footer_linking(sec, ind, page_attributes)
        _apply_page_attributes(sec, page_attributes)

def get_first_section(docx):
    """
    Get or create the first section in the document.
    """
    try:
        return docx.sections[0]
    except IndexError:
        docx.add_section()
        return docx.sections[0]

def get_or_create_second_section(docx):
    """
    Get or create the second section in the document.
    """
    while len(docx.sections) < 2:
        docx.add_section()
    return docx.sections[1]

def get_first_page_header(docx):
    """
    Get the first page header of the document.
    """
    section = get_first_section(docx)
    return section.first_page_header

def get_first_page_footer(docx):
    """
    Get the first page footer of the document.
    """
    section = get_first_section(docx)
    return section.first_page_footer

def get_second_header(docx):
    """
    Get the second page header of the document.
    """
    section = get_or_create_second_section(docx)
    return section.header

def get_second_footer(docx):
    """
    Get the second page footer of the document.
    """
    section = get_or_create_second_section(docx)
    return section.footer

def setup_section_columns(section, num_columns, column_spacing):
    """
    Set up the number of columns and spacing for a given section.
    """
    sect_pr = section._sectPr
    cols = _get_or_create_cols(sect_pr)
    cols.set(qn('w:num'), str(num_columns))
    cols.set(qn('w:space'), str(column_spacing))

def add_continuous_single_column_section(docx):
    """Insert a continuous section and set layout to a single column. Returns the section."""
    section = docx.add_section(pdf_enum.WD_SECTION.CONTINUOUS)
    setup_section_columns(section, 1, 0)
    return section

def add_continuous_two_column_section(docx):
    """Insert a continuous section and set layout to two columns with default spacing. Returns the section."""
    section = docx.add_section(pdf_enum.WD_SECTION.CONTINUOUS)
    setup_section_columns(section, 2, pdf_enum.TWO_COLUMNS_SPACING)
    return section

def set_start_page_number(section, start_number: int):
    """
    Set the starting page number for the given section.
    """
    sect_pr = section._sectPr
    pg_num_type = sect_pr.find(qn('w:pgNumType'))
    if pg_num_type is None:
        pg_num_type = OxmlElement('w:pgNumType')
        sect_pr.append(pg_num_type)
    pg_num_type.set(qn('w:start'), str(start_number))


# -----------------
# Private helpers
# -----------------

def _apply_header_footer_linking(sec, index, page_attributes):
    """ Apply header/footer linking rules based on section index."""
    if index == 0:
        sec.different_first_page_header_footer = page_attributes.get('different_first_page_header_footer')
    elif index == 1:
        sec.header.is_linked_to_previous = False

def _apply_page_attributes(sec, page_attributes):
    """Apply page attributes from the given dictionary to the section."""
    sec.top_margin = page_attributes.get('top_margin')
    sec.left_margin = page_attributes.get('left_margin')
    sec.right_margin = page_attributes.get('right_margin')
    sec.bottom_margin = page_attributes.get('bottom_margin')
    sec.header_distance = page_attributes.get('header_distance')
    sec.footer_distance = page_attributes.get('footer_distance')
    sec.gutter = page_attributes.get('gutter')
    sec.orientation = page_attributes.get('orientation')
    sec.page_height = page_attributes.get('page_height')
    sec.page_width = page_attributes.get('page_width')

def _get_or_create_cols(sect_pr):
    """Get or create the <w:cols> element in the section properties."""
    cols = sect_pr.find(qn('w:cols'))
    if cols is None:
        cols = OxmlElement('w:cols')
        sect_pr.append(cols)
    return cols
