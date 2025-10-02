from packtools.sps.formats.pdf import enum as pdf_enum
from packtools.sps.formats.pdf.pipeline import xml as xml_pipe
from packtools.sps.formats.pdf.renderer import docx as docx_renderer
from packtools.sps.formats.pdf.utils import xml_utils


def pipeline_docx(xml_tree, data):
    """
    Create a DOCX document from an XML tree and additional data.

    Args:
        xml_tree: The XML tree containing the article data.
        data: Additional data for the DOCX generation.

    Returns:
        A DOCX Document object.
    """
    docx = docx_renderer.builder.init_docx(data)

    # First page header
    journal_title = xml_pipe.extract_journal_title(xml_tree)
    docx_journal_title_pipe(docx, journal_title)

    doi = xml_pipe.extract_doi(xml_tree)
    docx_doi_pipe(docx, doi)

    # First page content
    article_type = xml_pipe.extract_article_type(xml_tree)
    category = xml_pipe.extract_category(xml_tree)
    docx_article_type_and_category_pipe(docx, category, article_type)

    article_title = xml_pipe.extract_article_title(xml_tree)
    docx_article_title_pipe(docx, article_title)

    contrib_data = xml_pipe.extract_contrib_data(xml_tree)
    docx_authors_pipe(docx, contrib_data['authors_names'])
    docx_affiliation_pipe(docx, contrib_data['affiliations'])
    docx_corresponding_pipe(docx, contrib_data['corresponding_author'])

    article_main_language = xml_pipe.extract_article_main_language(xml_tree)
    abstract_data = xml_pipe.extract_abstract_data(xml_tree)
    docx_abstract_pipe(docx, abstract_data['title'], abstract_data['content'])

    keywords_data = xml_pipe.extract_keywords_data(xml_tree, article_main_language)
    docx_keyworks_pipe(docx, keywords_data['title'], keywords_data['keywords'])

    trans_abstract_data = xml_pipe.extract_trans_abstract_data(xml_tree)
    for ta in trans_abstract_data:
        docx_abstract_pipe(docx, ta['title'], ta['content'])
        ta_keywords_data = xml_pipe.extract_keywords_data(xml_tree, ta['lang'])
        docx_keyworks_pipe(docx, ta_keywords_data['title'], ta_keywords_data['keywords'])

    # Next pages header
    docx_second_header_pipe(docx, journal_title, article_title)

    # First page footer
    footer_data = xml_pipe.extract_footer_data(xml_tree)
    cite_as_part_one = xml_pipe.extract_cite_as_part_one(xml_tree) 
    docx_cite_as_pipe(docx, cite_as_part_one, journal_title, footer_data)
    docx_page_vol_issue_year_pipe(docx, footer_data)

    # Next pages footer
    docx_second_footer_pipe(docx, footer_data)
    
    # Main content
    body_data = xml_pipe.extract_body_data(xml_tree)
    docx_body_pipe(docx, body_data)
    
    # Acknowledgments
    acknow_data = xml_pipe.extract_acknowledgment_data(xml_tree)
    docx_acknowledgments_pipe(docx, acknow_data['title'], acknow_data['paragraphs'])

    # References
    references_data = xml_pipe.extract_references_data(xml_tree)
    references = map(xml_utils.get_text_from_mixed_citation_node, references_data['references'])
    docx_references_pipe(docx, references_data['title'], references)

    # Supplementary material
    supplementary_data = xml_pipe.extract_supplementary_data(xml_tree)
    if supplementary_data['elements']:
        docx_supplementary_material_pipe(docx, footer_data, supplementary_data)

    # Setting up sections
    docx_renderer.section.docx_setup_sections(docx)
    
    return docx

def docx_journal_title_pipe(docx, journal_title_text, style_name='SCL Journal Title Char'):
    """
    Adds the journal title text to the first page header of the DOCX document, with each word on a new line.
    
    Args:
        docx (python-docx.Document): The DOCX document object.
        journal_title_text (str): The text of the journal title to be added.
        style_name (str, optional): The name of the style to apply to the journal title text. Defaults to 'SCL Journal Title Char'.
    
    Returns:
        python-docx.Paragraph: The paragraph object containing the journal title text.
    """
    first_page_header = docx_renderer.section.get_first_page_header(docx)
    para = docx_renderer.text.get_first_paragraph(first_page_header)

    left_run = para.add_run(journal_title_text.replace(' ', '\n'))
    left_run.style = docx.styles[style_name]

    return para

def docx_doi_pipe(docx, doi_code, paragraph=None, style_name='SCL Header Paragraph Char'):
    """
    Adds the DOI (Digital Object Identifier) code to the first page header of the DOCX document, with the DOI URL formatted as a tab-indented string.
    
    Args:
        docx (python-docx.Document): The DOCX document object.
        doi_code (str): The DOI code to be added.
        paragraph (python-docx.Paragraph, optional): The paragraph object to add the DOI URL to. If not provided, the first paragraph in the first page header will be used.
        style_name (str, optional): The name of the style to apply to the DOI URL. Defaults to 'SCL Header Paragraph Char'.
    
    Returns:
        None
    """
    doi_url = f"http://dx.doi.org/{doi_code}"

    if paragraph:
        para = paragraph
    else:
        first_page_header = docx_renderer.section.get_first_page_header(docx)
        para = docx_renderer.text.get_first_paragraph(first_page_header)

    r = para.add_run(f'\t{doi_url}')
    r.style = docx.styles[style_name]

def docx_article_type_and_category_pipe(docx, category, article_type='Original Article', style_name='SCL Article Category'):
    """
    Adds the article category and type to the first page header of the DOCX document.
    Args:
        docx (python-docx.Document): The DOCX document object.
        category (str):
    
    Returns:
        None
    """
    article_category_text = ' | '.join([category, article_type])
    article_category_el = docx.add_paragraph(article_category_text)
    article_category_el.style = docx.styles[style_name]

def docx_article_title_pipe(docx, article_title, style_name='SCL Article Title'):
    """
    Adds the article title to the first page header of the DOCX document.

    Args:
        docx (python-docx.Document): The DOCX document object.
        article_title (str): The title of the article to be added.
        style_name (str, optional): The name of the style to apply to the article title. Defaults to 'SCL Article Title'.
    
    Returns:
        None
    """
    article_title_el = docx.add_heading(article_title, level=1)
    article_title_el.style = docx.styles[style_name]

def docx_authors_pipe(docx, authors_names, paragraph_style_name='SCL Author', character_style_name='SCL Author Char'):
    """
    Adds the authors' names to the first page header of the DOCX document, with each name on a new line.

    Args:
        docx (python-docx.Document): The DOCX document object.
        authors_names (list): The list of authors' names to be added.
        paragraph_style_name (str, optional): The name of the style to apply to the paragraph containing the authors' names. Defaults to 'SCL Author'.
        character_style_name (str, optional): The name of the style to apply to the authors' names. Defaults to 'SCL Author Char'.

    Returns:
        None
    """
    docx_renderer.text.add_authors_names_paragraph_with_formatting_sup(
    docx, 
        authors_names,
        paragraph_style_name=paragraph_style_name,
        character_style_name=character_style_name, 
        sup_mark="[^]"
    )

def docx_affiliation_pipe(docx, affiliations, paragraph_style_name='SCL Affiliation', character_style_name='SCL Affiliation Char'):
    """
    Adds the affiliations to the first page header of the DOCX document, with each affiliation on a new line.

    Args:
        docx (python-docx.Document): The DOCX document object.
        affiliations (list): The list of affiliations to be added.
        paragraph_style_name (str, optional): The name of the style to apply to the paragraph containing the affiliations. Defaults to 'SCL Affiliation'.
        character_style_name (str, optional): The name of the style to apply to the affiliations. Defaults to 'SCL Affiliation Char'.

    Returns:
        None
    """
    for aff in affiliations:
        docx_renderer.text.add_text_paragraph_with_formatting_sup(
            docx, 
            aff, 
            paragraph_style_name=paragraph_style_name,
            character_style_name=character_style_name, 
            sup_mark="[^]"
        )

def docx_corresponding_pipe(docx, corresponding, paragraph_style_name='SCL Affiliation', character_style_name='SCL Affiliation Char'):
    """
    Adds the corresponding author to the first page header of the DOCX document.

    Args:
        docx (python-docx.Document): The DOCX document object.
        corresponding (str): The corresponding author to be added.
        paragraph_style_name (str, optional): The name of the style to apply to the paragraph containing the corresponding author. Defaults to 'SCL Affiliation'.
        character_style_name (str, optional): The name of the style to apply to the corresponding author. Defaults to 'SCL Affiliation Char'.

    Returns:
        None
    """
    docx_renderer.text.add_text_paragraph_with_formatting_sup(
        docx,
        corresponding,
        paragraph_style_name=paragraph_style_name,
        character_style_name=character_style_name,
        sup_mark="[^]"
    )

def docx_abstract_pipe(docx, abstract_title, abstract_content, title_paragraph_style_name='SCL Abstract Title', content_paragraph_style_name='SCL Paragraph Abstract'):
    """
    Adds the abstract title and content to the first page header of the DOCX document.

    Args:
        docx (python-docx.Document): The DOCX document object.
        abstract_title (str): The title of the abstract to be added.
        abstract_content (str): The content of the abstract to be added.
        title_paragraph_style_name (str, optional): The name of the style to apply to the abstract title. Defaults to 'SCL Abstract Title'.
        content_paragraph_style_name (str, optional): The name of the style to apply to the abstract content. Defaults to 'SCL Paragraph Abstract'.

    Returns:
        None
    """
    abstract_title_el = docx.add_heading(abstract_title, level=2)
    abstract_title_el.style = docx.styles[title_paragraph_style_name]
    abstract_content_el = docx.add_paragraph(abstract_content)
    abstract_content_el.style = docx.styles[content_paragraph_style_name]

def docx_keyworks_pipe(
        docx, 
        keywords_title, 
        keywords_content, 
        keywords_paragraph_style_name='SCL Paragraph Keywords', 
        keywords_header_character_style_name='SCL Paragraph Keywords Header Char',
        keyworks_character_paragraph_style_name='SCL Paragraph Keywords Char'):
    """
    Adds the keywords title and content to the first page header of the DOCX document.

    Args:
        docx (python-docx.Document): The DOCX document object.
        keywords_title (str): The title of the keywords to be added.
        keywords_content (str): The content of the keywords to be added.
        keywords_paragraph_style_name (str, optional): The name of the style to apply to the keywords title. Defaults to 'SCL Paragraph Keywords'.
        keywords_header_character_style_name (str, optional): The name of the style to apply to the keywords title. Defaults to 'SCL Paragraph Keywords Header Char'.
        keyworks_character_paragraph_style_name (str, optional): The name of the style to apply to the keywords content. Defaults to 'SCL Paragraph Keywords Char'.

    Returns:
        None
    """
    para = docx.add_paragraph()
    para.style = docx.styles[keywords_paragraph_style_name]

    r1 = para.add_run(f'{keywords_title} ')
    r1.style = docx.styles[keywords_header_character_style_name]

    r2 = para.add_run(f'{keywords_content}')
    r2.style = docx.styles[keyworks_character_paragraph_style_name]

def docx_cite_as_pipe(
        docx,
        cite_as_part_one,
        journal_title,
        footer_data,
):
    """
    Adds the citation information to the first page footer of the DOCX document.

    Args:
        docx (python-docx.Document): The DOCX document object.
        cite_as_part_one (str): The first part of the citation information to be added.
        journal_title (str): The title of the journal to be added.
        footer_data (dict): The data to be added to the footer.

    Returns:
        None
    """
    cite_as_part_two = f'{footer_data["volume"]}: {footer_data["fpage"]}-{footer_data["lpage"]}'

    footer = docx_renderer.section.get_first_page_footer(docx)
    para = docx_renderer.text.get_first_paragraph(footer)
    para.style = docx.styles['SCL Paragraph Cite As']

    footer_style = docx.styles['SCL Paragraph Cite As Footer Char']
    docx_renderer.style.add_run_with_style(para, 'CITE AS: ', footer_style)

    p1_style = docx.styles['SCL Paragraph Cite As Char']
    docx_renderer.style.add_run_with_style(para, cite_as_part_one, p1_style)

    journal_title_style = docx.styles['SCL Paragraph Cite As Journal Title Char']
    docx_renderer.style.add_run_with_style(para, f'{journal_title} ', journal_title_style)

    p2_style = docx.styles['SCL Paragraph Cite As Char']
    docx_renderer.style.add_run_with_style(para, f'{cite_as_part_two}.', p2_style)

def docx_second_header_pipe(
        docx, 
        journal_title, 
        article_title, 
        paragraph_header_style_name='SCL Header Paragraph',
        character_header_style_name='SCL Header Paragraph Char',
        paragraph_title_style_name='SCL Journal Title Char'
    ):
    """
    Adds the journal title and article title to the second page header of the DOCX document.

    Args:
        docx (python-docx.Document): The DOCX document object.
        journal_title (str): The title of the journal to be added.
        article_title (str): The title of the article to be added.
        paragraph_header_style_name (str, optional): The name of the style to apply to the journal title. Defaults to 'SCL Header Paragraph'.
        character_header_style_name (str, optional): The name of the style to apply to the article title.

    Returns:
        None
    """
    header = docx_renderer.section.get_second_header(docx)
    header.is_linked_to_previous = False
    para = header.add_paragraph()
    para.style = docx.styles[paragraph_header_style_name]

    r1 = para.add_run(journal_title.replace(' ', '\n'))
    r1.style = docx.styles[paragraph_title_style_name]

    r2 = para.add_run(f'\t{article_title}')
    r2.style = docx.styles[character_header_style_name]

def docx_second_footer_pipe(docx, footer_data, paragraph_style_name='SCL Footer'):
    """
    Adds the footer information to the second page footer of the DOCX document.

    Args:
        docx (python-docx.Document): The DOCX document object.
        footer_data (dict): The data to be added to the footer.
        paragraph_style_name (str, optional): The name of the style to apply to the footer. Defaults to 'SCL Footer'.

    Returns:
        None
    """
    footer = docx_renderer.section.get_second_footer(docx)

    para = footer.paragraphs[0]
    para.style = docx.styles[paragraph_style_name]

    page_number_run = para.add_run()

    fld_char_start = OxmlElement('w:fldChar')
    fld_char_start.set(qn('w:fldCharType'), 'begin')
    page_number_run._element.append(fld_char_start)

    instr_text = OxmlElement('w:instrText')
    instr_text.text = "PAGE \\* MERGEFORMAT"
    page_number_run._element.append(instr_text)

    fld_char_end = OxmlElement('w:fldChar')
    fld_char_end.set(qn('w:fldCharType'), 'end')
    page_number_run._element.append(fld_char_end)
    
    para.add_run(f" | VOL. {footer_data['volume']} ({footer_data['issue']}) {footer_data['year']}: {footer_data['fpage']}-{footer_data['lpage']}")

    sect_pr = docx.sections[1]._sectPr
    pg_num_type = OxmlElement('w:pgNumType')

    try:
        current_page_number = int(footer_data['fpage']) + 1
    except ValueError:
        current_page_number = 1

    pg_num_type.set(ns.qn('w:start'), str(current_page_number))
    sect_pr.append(pg_num_type)

def docx_page_vol_issue_year_pipe(docx, footer_data, paragraph_style_name='SCL Footer'):
    """
    Adds the page, volume, issue, and year information to the first page footer of the DOCX document.

    Args:
        docx (python-docx.Document): The DOCX document object.
        footer_data (dict): The data to be added to the footer.
        paragraph_style_name (str, optional): The name of the style to apply to the footer. Defaults to 'SCL Footer'.

    Returns:
        None
    """
    footer = docx_renderer.section.get_first_page_footer(docx)
    para = footer.add_paragraph()

    para.style = docx.styles[paragraph_style_name]
    para.add_run(f"{footer_data['fpage']} | VOL. {footer_data['volume']} ({footer_data['issue']}) {footer_data['year']}: {footer_data['fpage']}-{footer_data['lpage']}")

def docx_body_pipe(docx, body_data):
    """
    Adds the body content to the DOCX document.

    Args:
        docx (python-docx.Document): The DOCX document object.
        body_data (list): The list of body sections to be added.

    Returns:
        None
    """
    section = docx_utils.get_or_create_second_section(docx)
    docx_utils.setup_section_columns(section, 2, pdf_enum.TWO_COLUMNS_SPACING)

    for section in body_data:
        section_style_name = docx_utils.level_to_style(section['level'])
        if section['title'] is not None:
            docx_utils.add_heading_with_formatting(docx, section['title'], section_style_name, section['level'])

            for para in section['paragraphs']:
                docx_utils.add_paragraph_with_formatting(docx, para)

            for table in section['tables']:
                docx_utils.add_table(docx, table)
                # FIXME: enable/disable one-column or two-column page tables
                #   1. enable the one-column mode
                #       single_col_section = docx.add_section(WD_SECTION.CONTINUOUS)
                #       setup_section_columns(single_col_section, 1, 0)
                #   2. add the table itself
                #   3. disable the one-column mode
                #       multi_col_section = docx.add_section(WD_SECTION.CONTINUOUS)
                #       setup_section_columns(multi_col_section, 2, TWO_COLUMNS_SPACING)

def docx_references_pipe(
        docx, 
        title='References', 
        references=[], 
        section_style_name='SCL Section Title', 
        paragraph_style_name='SCL Paragraph Reference',
    ):
    """
    Adds the references section to the DOCX document.

    Args:
        docx (python-docx.Document): The DOCX document object.
        title (str, optional): The title of the references section. Defaults to 'References'.
        references (list, optional): The list of references to be added. Defaults to [].
        section_style_name (str, optional): The name of the style to apply to the section title. Defaults to 'SCL Section Title'.
        paragraph_style_name (str, optional): The name of the style to apply to the reference paragraphs. Defaults to 'SCL Paragraph Reference'.
    
    Returns:
        None
    """
    docx_renderer.text.add_heading_with_formatting(docx, title, section_style_name, 2)
    for reference in references:
        paragraph = docx.add_paragraph(reference)
        paragraph.style = docx.styles[paragraph_style_name]

def docx_acknowledgments_pipe(docx, acknowledgment_title, acknowledgement_paragraphs, paragraph_section_style_name='SCL Section Title'):
    """
    Adds the acknowledgments section to the DOCX document.

    Args:
        docx (python-docx.Document): The DOCX document object.
        acknowledgment_title (str): The title of the acknowledgments section.
        acknowledgement_paragraphs (list): The list of paragraphs to be added to the acknowledgments section.
        paragraph_section_style_name (str, optional): The name of the style to apply to the acknowledgments section title. Defaults to 'SCL Section Title'.

    Returns:
        None
    """
    docx_renderer.text.add_heading_with_formatting(docx, acknowledgment_title, paragraph_section_style_name, 2)

    for text in acknowledgement_paragraphs:
        docx_renderer.text.add_paragraph_with_formatting(docx, text)

def docx_supplementary_material_pipe(docx, footer_data, supplementary_data, section_style_name='SCL Section Title'):
    """
    Adds the supplementary material section to the DOCX document.

    Args:
        docx (python-docx.Document): The DOCX document object.
        footer_data (dict): The data to be added to the footer.
        supplementary_data (dict): The data to be added to the supplementary material section.
        section_style_name (str, optional): The name of the style to apply to the supplementary material section title. Defaults to 'SCL Section Title'.

    Returns:
        None
    """
    section = docx.add_section()

    section.footer.is_linked_to_previous = False
    footer = section.footer

    para = footer.add_paragraph()
    para.style = docx.styles['SCL Footer']
    
    para.add_run(f" | VOL. {footer_data['volume']} ({footer_data['issue']}) {footer_data['year']}: {footer_data['fpage']}-{footer_data['lpage']}")
    
    docx_renderer.section.setup_section_columns(section, 1, pdf_enum.TWO_COLUMNS_SPACING)

    docx_renderer.text.add_heading_with_formatting(docx, supplementary_data['title'], section_style_name, 2)

    for element in supplementary_data['elements']:
        if element['type'] == 'table':
            docx_renderer.table.add_table(docx, element['content'])
        elif element['type'] == 'text':
            docx_renderer.text.add_paragraph_with_formatting(docx, element['content'])


# -----------------
# Private helpers
# -----------------

def _setup_two_column_body_section(docx):
    """Create or get the second section and set it to two columns."""
    section = docx_renderer.section.get_or_create_second_section(docx)
    docx_renderer.section.setup_section_columns(section, 2, pdf_enum.TWO_COLUMNS_SPACING)


def _render_body_section(docx, section_data):
    """Render a single body section including title, paragraphs, tables, and figures."""
    level = section_data.get('level')
    section_style_name = docx_renderer.style.level_to_style(level)

    _render_section_title(docx, section_data.get('title'), section_style_name, level)
    _render_paragraphs(docx, section_data.get('paragraphs', []))
    _render_tables(docx, section_data.get('tables', []))
    _render_figures(docx, section_data.get('figures', []))


def _render_section_title(docx, title, style_name, level):
    """Render section title if present."""
    if title is not None:
        docx_renderer.text.add_heading_with_formatting(docx, title, style_name, level)


def _render_paragraphs(docx, paragraphs):
    """Render a list of paragraphs with the default formatting for body text."""
    for para in paragraphs:
        docx_renderer.text.add_paragraph_with_formatting(docx, para)


def _add_single_column_section(docx):
    """Insert a continuous section break and set a single column layout. Returns the section."""
    single_col_section = docx.add_section(pdf_enum.WD_SECTION.CONTINUOUS)
    docx_renderer.section.setup_section_columns(single_col_section, 1, 0)
    return single_col_section


def _add_two_column_section(docx):
    """Insert a continuous section break and set a two column layout. Returns the section."""
    multi_col_section = docx.add_section(pdf_enum.WD_SECTION.CONTINUOUS)
    docx_renderer.section.setup_section_columns(multi_col_section, 2, pdf_enum.TWO_COLUMNS_SPACING)
    return multi_col_section


def _render_tables(docx, tables):
    """Render tables, switching to single column when required by layout."""
    for table in tables:
        if table.get('layout') == pdf_enum.SINGLE_COLUMN_PAGE_LABEL:
            _add_single_column_section(docx)
            docx_renderer.table.add_table(docx, table, page_attributes=pdf_enum.PAGE_ATTRIBUTES)
            _add_two_column_section(docx)
        else:
            docx_renderer.table.add_table(docx, table, page_attributes=pdf_enum.PAGE_ATTRIBUTES)


def _figure_layout(docx, fig):
    """Resolve and cache figure layout if not provided."""
    layout = fig.get('layout') if isinstance(fig, dict) else None
    if not layout:
        layout = docx_renderer.figure.decide_figure_layout(docx, fig, page_attributes=pdf_enum.PAGE_ATTRIBUTES)
        if isinstance(fig, dict):
            fig['layout'] = layout
    return layout


def _render_figures(docx, figures):
    """Render figures, switching to single column when the layout requires it."""
    for fig in figures:
        layout = _figure_layout(docx, fig)

        if layout == pdf_enum.SINGLE_COLUMN_PAGE_LABEL:
            _add_single_column_section(docx)
            docx_renderer.figure.add_figure(docx, fig, page_attributes=pdf_enum.PAGE_ATTRIBUTES)
            _add_two_column_section(docx)
        else:
            docx_renderer.figure.add_figure(docx, fig, page_attributes=pdf_enum.PAGE_ATTRIBUTES)
