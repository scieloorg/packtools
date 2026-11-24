"""Nomes de estilo: papel do bloco/run (definido na extração) -> estilo SCL do layout.docx."""

STYLES = {
    "body": "SCL Paragraph",
    "heading2": "SCL Section Title",
    "heading3": "SCL Subsection Title",
    "formula": "SCL Formula",
    "reference": "SCL Paragraph Reference",
    "abstract": "SCL Paragraph Abstract",
    "abstract_title": "SCL Abstract Title",
    "table_caption": "SCL Table Heading",
    "figure_caption": "SCL Figure Caption",
    "article_title": "SCL Article Title",
    "article_category": "SCL Article Category",
    "author": "SCL Author",
    "author_char": "SCL Author Char",
    "affiliation": "SCL Affiliation",
    "affiliation_char": "SCL Affiliation Char",
    "keywords": "SCL Paragraph Keywords",
    "keywords_title_char": "SCL Paragraph Keywords Header Char",
    "keywords_char": "SCL Paragraph Keywords Char",
    "journal_title_char": "SCL Journal Title Char",
    "header": "SCL Header Paragraph",
    "header_char": "SCL Header Paragraph Char",
    "footer": "SCL Footer",
    "cite_as": "SCL Paragraph Cite As",
    "cite_as_char": "SCL Paragraph Cite As Char",
    "cite_as_label_char": "SCL Paragraph Cite As Footer Char",
    "cite_as_journal_char": "SCL Paragraph Cite As Journal Title Char",
}

# Entrelinha do texto corrido quando o estilo do corpo no layout.docx não
# define uma: múltiplo da linha simples da fonte. Sem isso, o corpo herdava o
# 1,15 do modelo do python-docx (12,5 pt com Noto Serif 8 pt). Com 1,22,
# a entrelinha vai a cerca de 13,3 pt, a mediana dos PDFs canônicos de um
# artigo por periódico do corpus de teste.
BODY_LINE_SPACING = 1.22
