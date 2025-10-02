from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def add_heading_with_formatting(docx, text, style_name, level):
    """Add a heading with the specified style and level to the document."""
    heading = docx.add_heading(text, level=level)
    heading.style = docx.styles[style_name]
    return heading

def add_paragraph_with_formatting(docx, text, style_name='SCL Paragraph', element=None):
    """Add a paragraph with the specified style to the document or a given element."""
    if element is not None:
        para = element.add_paragraph(text)
    else:
        para = docx.add_paragraph(text)
    para.style = docx.styles[style_name]
    return para

def add_authors_names_paragraph_with_formatting_sup(docx, authors_names, paragraph_style_name, character_style_name, sup_mark="[^]"):
    """Add a paragraph with authors' names, handling superscript markers for affiliations."""
    para = docx.add_paragraph()
    para.style = docx.styles[paragraph_style_name]

    for ind, a in enumerate(authors_names):
        normal_text, sup_text = _split_on_marker(a, sup_mark, reverse=False)

        normal_run = para.add_run(normal_text)
        normal_run.style = docx.styles[character_style_name]

        separator_text = _authors_separator(ind, len(authors_names))

        sup_run = para.add_run(sup_text)
        sup_run.style = docx.styles[character_style_name]
        sup_run.font.superscript = True

        sep_run = para.add_run(separator_text)
        sep_run.style = docx.styles[character_style_name]

    return para

def add_text_paragraph_with_formatting_sup(docx, text, paragraph_style_name, character_style_name, sup_mark="[^]"):
    """Add a paragraph with text, handling superscript markers."""
    para = docx.add_paragraph()
    para.style = docx.styles[paragraph_style_name]

    sup_text, normal_text = _split_on_marker(text, sup_mark, reverse=True)

    sup_run = para.add_run(sup_text)
    sup_run.style = docx.styles[character_style_name]
    sup_run.font.superscript = True

    normal_run = para.add_run(normal_text)
    normal_run.style = docx.styles[character_style_name]

def get_first_paragraph(element):
    """ Get or create the first paragraph in the given element (document, header, footer, cell, etc.)."""
    try:
        return element.paragraphs[0]
    except KeyError:
        element.add_paragraph()
        return element.paragraphs[0]

def add_field_run(paragraph, instruction_text):
    """
    Insert a field code run into the given paragraph.

    Example instruction_text values:
    - "PAGE \\* MERGEFORMAT"
    - "NUMPAGES"
    - "DATE \\@ yyyy"
    """
    run = paragraph.add_run()

    fld_char_begin = OxmlElement('w:fldChar')
    fld_char_begin.set(qn('w:fldCharType'), 'begin')
    run._element.append(fld_char_begin)

    instr_text = OxmlElement('w:instrText')
    instr_text.text = instruction_text
    run._element.append(instr_text)

    fld_char_end = OxmlElement('w:fldChar')
    fld_char_end.set(qn('w:fldCharType'), 'end')
    run._element.append(fld_char_end)

    return run


# -----------------
# Private helpers
# -----------------

def _split_on_marker(text, marker, reverse=False):
    """
    Split text on the first occurrence of marker and return a tuple (before, after).
    - If marker isn't found: returns (text, '') by default.
    - If reverse=True and marker isn't found: returns ('', text) to match
      callers that expect the second part to carry the whole text.
    """
    parts = text.split(marker, 1)
    if len(parts) == 2:
        before, after = parts[0], parts[1]
        return before, after

    if reverse:
        return '', text
    return text, ''

def _authors_separator(index, total):
    """ Return the appropriate separator between authors' names based on their position."""
    if index <= total - 3:
        return ', '
    if index == total - 2:
        return ' and '
    return ''
