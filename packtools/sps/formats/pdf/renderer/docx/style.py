from docx.enum.text import WD_PARAGRAPH_ALIGNMENT

from packtools.sps.formats.pdf import enum as pdf_enum

# Nomes dos estilos definidos no layout base (.docx): única fonte dos nomes 'SCL *'.
SCL_ABSTRACT_TITLE = 'SCL Abstract Title'
SCL_AFFILIATION = 'SCL Affiliation'
SCL_AFFILIATION_CHAR = 'SCL Affiliation Char'
SCL_ARTICLE_CATEGORY = 'SCL Article Category'
SCL_ARTICLE_TITLE = 'SCL Article Title'
SCL_AUTHOR = 'SCL Author'
SCL_AUTHOR_CHAR = 'SCL Author Char'
SCL_FIGURE_CAPTION = 'SCL Figure Caption'
SCL_FOOTER = 'SCL Footer'
SCL_FORMULA = 'SCL Formula'
SCL_HEADER_PARAGRAPH = 'SCL Header Paragraph'
SCL_HEADER_PARAGRAPH_CHAR = 'SCL Header Paragraph Char'
SCL_JOURNAL_TITLE_CHAR = 'SCL Journal Title Char'
SCL_PARAGRAPH = 'SCL Paragraph'
SCL_PARAGRAPH_ABSTRACT = 'SCL Paragraph Abstract'
SCL_PARAGRAPH_CITE_AS = 'SCL Paragraph Cite As'
SCL_PARAGRAPH_CITE_AS_CHAR = 'SCL Paragraph Cite As Char'
SCL_PARAGRAPH_CITE_AS_FOOTER_CHAR = 'SCL Paragraph Cite As Footer Char'
SCL_PARAGRAPH_CITE_AS_JOURNAL_TITLE_CHAR = 'SCL Paragraph Cite As Journal Title Char'
SCL_PARAGRAPH_KEYWORDS = 'SCL Paragraph Keywords'
SCL_PARAGRAPH_KEYWORDS_CHAR = 'SCL Paragraph Keywords Char'
SCL_PARAGRAPH_KEYWORDS_HEADER_CHAR = 'SCL Paragraph Keywords Header Char'
SCL_PARAGRAPH_REFERENCE = 'SCL Paragraph Reference'
SCL_SECTION_TITLE = 'SCL Section Title'
SCL_SUBSECTION_TITLE = 'SCL Subsection Title'
SCL_TABLE_HEADING = 'SCL Table Heading'


def copy_styles(source, target):
    for style in source.styles:
        if style.type in (pdf_enum.WD_STYLE_TYPE.PARAGRAPH, pdf_enum.WD_STYLE_TYPE.CHARACTER, pdf_enum.WD_STYLE_TYPE.TABLE):
            new_style = _create_or_replace_style(target, style)
            if style.type != pdf_enum.WD_STYLE_TYPE.TABLE:
                _copy_font_props(style, new_style)
                if style.type == pdf_enum.WD_STYLE_TYPE.PARAGRAPH:
                    _copy_paragraph_format(style, new_style)

def level_to_style(level):
    if level == 2:
        return SCL_SECTION_TITLE
    elif level == 3:
        return SCL_SUBSECTION_TITLE
    else:
        return SCL_PARAGRAPH

def add_run_with_style(element, text, style):
    run = element.add_run(text)
    run.style = style


# -----------------
# Private helpers
# -----------------

def _create_or_replace_style(target, style):
    if style.name in target.styles:
        target.styles[style.name].delete()
    new_style = target.styles.add_style(style.name, style.type)
    new_style.base_style = style.base_style
    new_style.hidden = style.hidden
    new_style.priority = style.priority
    new_style.quick_style = style.quick_style
    new_style.unhide_when_used = style.unhide_when_used
    return new_style

def _copy_font_props(src_style, dst_style):
    if src_style.font.name:
        dst_style.font.name = src_style.font.name
    if src_style.font.size:
        dst_style.font.size = src_style.font.size
    dst_style.font.bold = src_style.font.bold
    dst_style.font.italic = src_style.font.italic
    dst_style.font.underline = src_style.font.underline
    dst_style.font.strike = src_style.font.strike
    dst_style.font.all_caps = src_style.font.all_caps
    if src_style.font.color.rgb:
        dst_style.font.color.rgb = src_style.font.color.rgb
    if src_style.font.color.theme_color:
        dst_style.font.color.theme_color = src_style.font.color.theme_color
    dst_style.font.highlight_color = src_style.font.highlight_color
    dst_style.font.superscript = src_style.font.superscript
    dst_style.font.subscript = src_style.font.subscript

def _copy_paragraph_format(src_style, dst_style):
    try:
        dst_style.paragraph_format.alignment = src_style.paragraph_format.alignment
    except ValueError:
        dst_style.paragraph_format.alignment = WD_PARAGRAPH_ALIGNMENT.JUSTIFY
    pf_dst = dst_style.paragraph_format
    pf_src = src_style.paragraph_format
    pf_dst.left_indent = pf_src.left_indent
    pf_dst.right_indent = pf_src.right_indent
    pf_dst.first_line_indent = pf_src.first_line_indent
    pf_dst.keep_together = pf_src.keep_together
    pf_dst.keep_with_next = pf_src.keep_with_next
    pf_dst.page_break_before = pf_src.page_break_before
    pf_dst.widow_control = pf_src.widow_control
    pf_dst.space_before = pf_src.space_before
    pf_dst.space_after = pf_src.space_after
    pf_dst.line_spacing = pf_src.line_spacing
    pf_dst.line_spacing_rule = pf_src.line_spacing_rule
