import unittest
from unittest.mock import patch

from docx import Document
from docx.enum.style import WD_STYLE_TYPE

from packtools.sps.formats.pdf.pipeline import docx as docx_pipe
from packtools.sps.formats.pdf import enum as pdf_enum


class TestPipelineDocx(unittest.TestCase):
    # TODO
    ...


class TestFormatJournalTitleTwoLines(unittest.TestCase):
    """
    Regression tests for issue #1301: journal titles with more than 2 words
    used to get one word per line (unbounded), pushing the rest of the page-1
    header down. The first word stays on its own line and every remaining
    word is joined onto a single second line, capping the masthead at 2 lines
    regardless of how many words the title has.
    """

    def test_single_word_title_stays_on_one_line(self):
        self.assertEqual(docx_pipe._format_journal_title_two_lines('Biology'), 'Biology')

    def test_two_word_title_keeps_one_word_per_line(self):
        self.assertEqual(
            docx_pipe._format_journal_title_two_lines('Acta Amazonica'),
            'Acta\nAmazonica',
        )

    def test_four_word_title_is_capped_at_two_lines(self):
        self.assertEqual(
            docx_pipe._format_journal_title_two_lines('Brazilian Journal of Biology'),
            'Brazilian\nJournal of Biology',
        )

    def test_five_word_title_is_capped_at_two_lines(self):
        self.assertEqual(
            docx_pipe._format_journal_title_two_lines('Urbe. Revista Brasileira de Gestão Urbana'),
            'Urbe.\nRevista Brasileira de Gestão Urbana',
        )

    def test_empty_title_returns_empty_string(self):
        self.assertEqual(docx_pipe._format_journal_title_two_lines(''), '')


class TestJournalTitlePipe(unittest.TestCase):

    def setUp(self):
        self.docx = Document()
        self.docx.styles.add_style('SCL Journal Title Char', WD_STYLE_TYPE.CHARACTER)

    def test_two_word_title_keeps_one_word_per_line(self):
        para = docx_pipe.docx_journal_title_pipe(self.docx, 'Acta Amazonica')
        self.assertEqual(para.runs[0].text, 'Acta\nAmazonica')

    def test_multi_word_title_is_capped_at_two_lines(self):
        para = docx_pipe.docx_journal_title_pipe(self.docx, 'Brazilian Journal of Biology')
        self.assertEqual(para.runs[0].text, 'Brazilian\nJournal of Biology')

    def test_run_uses_the_given_style(self):
        para = docx_pipe.docx_journal_title_pipe(self.docx, 'Acta Amazonica')
        self.assertEqual(para.runs[0].style.name, 'SCL Journal Title Char')


class TestDocxDoiPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxArticleTypeAndCategoryPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxArticleTitlePipe(unittest.TestCase):
    # TODO
    ...


class TestDocxAuthorsPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxAffiliationPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxCorrespondingPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxAbstractPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxKeyworksPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxCiteAsPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxSecondHeaderPipe(unittest.TestCase):

    def setUp(self):
        self.docx = Document()
        self.docx.styles.add_style('SCL Header Paragraph', WD_STYLE_TYPE.PARAGRAPH)
        self.docx.styles.add_style('SCL Header Paragraph Char', WD_STYLE_TYPE.CHARACTER)
        self.docx.styles.add_style('SCL Journal Title Char', WD_STYLE_TYPE.CHARACTER)

    def _second_header_paragraph(self):
        header = docx_pipe.docx_renderer.section.get_default_header(self.docx)
        return header.paragraphs[-1]

    def test_two_word_title_keeps_one_word_per_line(self):
        docx_pipe.docx_second_header_pipe(self.docx, 'Acta Amazonica', 'Some Article Title')
        para = self._second_header_paragraph()
        self.assertEqual(para.runs[0].text, 'Acta\nAmazonica')

    def test_multi_word_title_is_capped_at_two_lines(self):
        docx_pipe.docx_second_header_pipe(self.docx, 'Brazilian Journal of Biology', 'Some Article Title')
        para = self._second_header_paragraph()
        self.assertEqual(para.runs[0].text, 'Brazilian\nJournal of Biology')

    def test_article_title_is_appended_after_a_tab(self):
        docx_pipe.docx_second_header_pipe(self.docx, 'Acta Amazonica', 'Some Article Title')
        para = self._second_header_paragraph()
        self.assertEqual(para.runs[1].text, '\tSome Article Title')


class TestDocxSecondFooterPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxPageVolIssueYearPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxBodyPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxReferencesPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxAcknowledgmentsPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxSupplementaryMaterialPipe(unittest.TestCase):
    # TODO
    ...


class TestBodyColumnConfiguration(unittest.TestCase):
    """
    Regression tests: body column count (and the count restored after a
    full-width table/figure) must come from PAGE_ATTRIBUTES['default_column_count']
    instead of a hardcoded 2, so a 1-column body isn't forced back to 2
    columns after a full-width table/figure interlude.
    """

    def _cols_num(self, section):
        cols = section._sectPr.find(
            '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}cols'
        )
        return cols.get(
            '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}num'
        )

    def test_body_column_count_defaults_to_two(self):
        with patch.dict(pdf_enum.PAGE_ATTRIBUTES, {}, clear=False):
            pdf_enum.PAGE_ATTRIBUTES.pop('default_column_count', None)
            self.assertEqual(docx_pipe._body_column_count(), 2)

    def test_body_column_count_reads_config(self):
        with patch.dict(pdf_enum.PAGE_ATTRIBUTES, {'default_column_count': 1}):
            self.assertEqual(docx_pipe._body_column_count(), 1)

    def test_setup_body_section_uses_configured_column_count(self):
        docx = Document()
        with patch.dict(pdf_enum.PAGE_ATTRIBUTES, {'default_column_count': 1}):
            docx_pipe._setup_body_section(docx)
        self.assertEqual(self._cols_num(docx.sections[1]), '1')

    def test_setup_body_section_supports_three_columns(self):
        docx = Document()
        with patch.dict(pdf_enum.PAGE_ATTRIBUTES, {'default_column_count': 3}):
            docx_pipe._setup_body_section(docx)
        self.assertEqual(self._cols_num(docx.sections[1]), '3')

    def test_restore_body_column_section_restores_configured_column_count(self):
        docx = Document()
        with patch.dict(pdf_enum.PAGE_ATTRIBUTES, {'default_column_count': 1}):
            section = docx_pipe._restore_body_column_section(docx)
        self.assertEqual(self._cols_num(section), '1')

    def test_restore_body_column_section_supports_three_columns(self):
        docx = Document()
        with patch.dict(pdf_enum.PAGE_ATTRIBUTES, {'default_column_count': 3}):
            section = docx_pipe._restore_body_column_section(docx)
        self.assertEqual(self._cols_num(section), '3')

    def test_render_tables_skips_section_switch_when_body_is_single_column(self):
        docx = Document()
        with patch.dict(pdf_enum.PAGE_ATTRIBUTES, {'default_column_count': 1}), \
             patch('packtools.sps.formats.pdf.pipeline.docx.docx_renderer.table.add_table'):
            sections_before = len(docx.sections)
            docx_pipe._render_tables(docx, [{'layout': pdf_enum.SINGLE_COLUMN_PAGE_LABEL}])
        self.assertEqual(len(docx.sections), sections_before)

    def test_render_tables_switches_section_when_body_has_multiple_columns(self):
        docx = Document()
        with patch.dict(pdf_enum.PAGE_ATTRIBUTES, {'default_column_count': 2}), \
             patch('packtools.sps.formats.pdf.pipeline.docx.docx_renderer.table.add_table'):
            sections_before = len(docx.sections)
            docx_pipe._render_tables(docx, [{'layout': pdf_enum.SINGLE_COLUMN_PAGE_LABEL}])
        self.assertEqual(len(docx.sections), sections_before + 2)

    def test_render_figures_skips_section_switch_when_body_is_single_column(self):
        docx = Document()
        with patch.dict(pdf_enum.PAGE_ATTRIBUTES, {'default_column_count': 1}), \
             patch('packtools.sps.formats.pdf.pipeline.docx.docx_renderer.figure.add_figure'):
            sections_before = len(docx.sections)
            docx_pipe._render_figures(docx, [{'layout': pdf_enum.SINGLE_COLUMN_PAGE_LABEL}])
        self.assertEqual(len(docx.sections), sections_before)

    def test_render_figures_switches_section_when_body_has_multiple_columns(self):
        docx = Document()
        with patch.dict(pdf_enum.PAGE_ATTRIBUTES, {'default_column_count': 2}), \
             patch('packtools.sps.formats.pdf.pipeline.docx.docx_renderer.figure.add_figure'):
            sections_before = len(docx.sections)
            docx_pipe._render_figures(docx, [{'layout': pdf_enum.SINGLE_COLUMN_PAGE_LABEL}])
        self.assertEqual(len(docx.sections), sections_before + 2)


if __name__ == "__main__":
    unittest.main()
