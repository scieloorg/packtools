import unittest
from pathlib import Path
from unittest.mock import patch

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH

from packtools.sps.formats.pdf.pipeline import docx as docx_pipe
from packtools.sps.formats.pdf.renderer import docx as docx_renderer
from packtools.sps.formats.pdf import enum as pdf_enum
from packtools.sps.utils import xml_utils

WML_NS = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

FIXTURES_DIR = Path(__file__).resolve().parents[4] / "fixtures" / "pdf"


def _docx_with_layout_styles():
    """A fresh Document carrying the named styles the footer/cite-as pipes rely on."""
    return docx_renderer.builder.init_docx({"base_layout": str(FIXTURES_DIR / "layout.docx")})


class TestPipelineDocx(unittest.TestCase):

    def _start_page_number(self, section):
        pg_num_type = section._sectPr.find(f'{WML_NS}pgNumType')
        return pg_num_type.get(f'{WML_NS}start')

    def _pipeline_docx(self, xml_filename):
        xml_tree = xml_utils.get_xml_tree(str(FIXTURES_DIR / xml_filename))
        data = {"base_layout": str(FIXTURES_DIR / "layout.docx"), "assets_dir": str(FIXTURES_DIR)}
        return docx_pipe.pipeline_docx(xml_tree, data)

    def test_start_page_number_uses_fpage_when_present(self):
        docx = self._pipeline_docx("a1.xml")
        self.assertEqual(self._start_page_number(docx.sections[0]), '271')

    def test_start_page_number_defaults_to_one_without_fpage(self):
        docx = self._pipeline_docx("a4.xml")
        self.assertEqual(self._start_page_number(docx.sections[0]), '1')


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

    def test_paragraph_lives_in_the_left_cell_of_a_header_table(self):
        returned_para = docx_pipe.docx_journal_title_pipe(self.docx, 'Acta Amazonica')
        header = docx_renderer.section.get_first_page_header(self.docx)
        table = header.tables[-1]
        cell_para = table.rows[0].cells[0].paragraphs[0]
        # python-docx builds a fresh Paragraph wrapper on each access, so
        # compare the underlying XML element (identity) rather than the
        # wrapper objects themselves.
        self.assertIs(returned_para._p, cell_para._p)

    def test_left_column_gets_the_configured_share_of_content_width(self):
        docx_pipe.docx_journal_title_pipe(self.docx, 'Acta Amazonica')
        header = docx_renderer.section.get_first_page_header(self.docx)
        table = header.tables[-1]
        content_width = int(docx_pipe._content_width())
        expected_left = int(content_width * docx_pipe._JOURNAL_TITLE_DOI_SPLIT)
        # Column widths round-trip through python-docx's internal Length
        # representation with a little rounding noise.
        self.assertAlmostEqual(table.columns[0].width, expected_left, delta=500)


class TestDocxDoiPipe(unittest.TestCase):
    """
    Regression: the DOI used to be tab-appended after the journal title in
    the same paragraph, relying on a tab stop to reach the right margin. A
    tab stop only sets where a run *starts*, not where it wraps - when the
    journal title's own second line (see _format_journal_title_two_lines)
    was already long, there was no room left on that line for the DOI, and
    it wrapped onto a line of its own instead of landing flush right. The
    DOI now gets its own column in a 2-column header table, right-aligned
    within it, independent of how much text is in the journal title's cell.
    """

    def setUp(self):
        self.docx = Document()
        self.docx.styles.add_style('SCL Journal Title Char', WD_STYLE_TYPE.CHARACTER)
        self.docx.styles.add_style('SCL Header Paragraph Char', WD_STYLE_TYPE.CHARACTER)

    def _doi_cell_paragraph(self):
        header = docx_renderer.section.get_first_page_header(self.docx)
        return header.tables[-1].rows[0].cells[1].paragraphs[0]

    def test_doi_run_has_no_leading_tab(self):
        docx_pipe.docx_doi_pipe(self.docx, '10.1590/example')
        para = self._doi_cell_paragraph()
        self.assertEqual(para.runs[-1].text, 'http://dx.doi.org/10.1590/example')

    def test_doi_paragraph_is_right_aligned(self):
        docx_pipe.docx_doi_pipe(self.docx, '10.1590/example')
        para = self._doi_cell_paragraph()
        self.assertEqual(para.alignment, WD_ALIGN_PARAGRAPH.RIGHT)

    def test_reuses_the_table_journal_title_pipe_already_created(self):
        docx_pipe.docx_journal_title_pipe(self.docx, 'Urbe. Revista Brasileira de Gestão Urbana')
        docx_pipe.docx_doi_pipe(self.docx, '10.1590/example')
        header = docx_renderer.section.get_first_page_header(self.docx)
        self.assertEqual(len(header.tables), 1)
        journal_para = header.tables[0].rows[0].cells[0].paragraphs[0]
        self.assertEqual(journal_para.runs[0].text, 'Urbe.\nRevista Brasileira de Gestão Urbana')
        doi_para = header.tables[0].rows[0].cells[1].paragraphs[0]
        self.assertEqual(doi_para.runs[-1].text, 'http://dx.doi.org/10.1590/example')

    def test_works_standalone_without_journal_title_pipe(self):
        # docx_doi_pipe creates its own table when none exists yet, rather
        # than assuming docx_journal_title_pipe always runs first.
        docx_pipe.docx_doi_pipe(self.docx, '10.1590/example')
        header = docx_renderer.section.get_first_page_header(self.docx)
        self.assertEqual(len(header.tables), 1)

    def test_right_aligns_a_caller_supplied_paragraph_too(self):
        # Regression: the right-alignment used to be set only on the branch
        # that creates its own cell, so a caller passing an existing
        # `paragraph` got the DOI added without any alignment at all.
        para = self.docx.add_paragraph()
        docx_pipe.docx_doi_pipe(self.docx, '10.1590/example', paragraph=para)
        self.assertEqual(para.alignment, WD_ALIGN_PARAGRAPH.RIGHT)
        self.assertEqual(para.runs[-1].text, 'http://dx.doi.org/10.1590/example')


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
    """
    Regression tests for issue #1322: the Keywords/Palavras-chave paragraph
    had no space-after of its own, so the section title immediately
    following it (space-before=0) collapsed onto it with almost no gap.
    """

    def setUp(self):
        self.docx = Document()
        self.docx.styles.add_style('SCL Paragraph Keywords', WD_STYLE_TYPE.PARAGRAPH)
        self.docx.styles.add_style('SCL Paragraph Keywords Header Char', WD_STYLE_TYPE.CHARACTER)
        self.docx.styles.add_style('SCL Paragraph Keywords Char', WD_STYLE_TYPE.CHARACTER)

    def test_paragraph_has_space_after(self):
        docx_pipe.docx_keyworks_pipe(self.docx, 'Keywords:', 'one, two, three')
        para = self.docx.paragraphs[-1]
        self.assertGreater(para.paragraph_format.space_after.pt, 0)

    def test_title_and_content_runs(self):
        docx_pipe.docx_keyworks_pipe(self.docx, 'Keywords:', 'one, two, three')
        para = self.docx.paragraphs[-1]
        self.assertEqual(para.runs[0].text, 'Keywords: ')
        self.assertEqual(para.runs[1].text, 'one, two, three')


class TestDocxCiteAsPipe(unittest.TestCase):

    def test_uses_fpage_lpage_range_when_present(self):
        docx = _docx_with_layout_styles()
        footer_data = {'volume': '10', 'issue': '2', 'year': '2023',
                       'fpage': 123, 'lpage': 130, 'location_label': '123-130'}
        docx_pipe.docx_cite_as_pipe(docx, 'Author AB. ', 'Journal Title', footer_data)

        footer = docx_renderer.section.get_first_page_footer(docx)
        para = docx_renderer.text.get_first_paragraph(footer)
        self.assertIn('10: 123-130.', para.text)

    def test_uses_elocation_id_when_fpage_is_absent(self):
        docx = _docx_with_layout_styles()
        footer_data = {'volume': '33', 'issue': '3', 'year': '2024',
                       'fpage': '', 'lpage': '', 'location_label': 'e282794'}
        docx_pipe.docx_cite_as_pipe(docx, 'Author AB. ', 'Journal Title', footer_data)

        footer = docx_renderer.section.get_first_page_footer(docx)
        para = docx_renderer.text.get_first_paragraph(footer)
        self.assertIn('33: e282794.', para.text)
        self.assertNotIn('-.', para.text)


class TestDocxSecondHeaderPipe(unittest.TestCase):
    """
    Regression: the running header used to be a single paragraph with the
    article title appended after a tab character. A tab stop only
    positions where a run starts, not where it wraps, so a long article
    title overflowed past the journal title instead of wrapping under
    itself. It's now a borderless 2-column table, each column getting half
    of the content width, with the article title right-aligned in its own
    column - independently bounded wrapping.
    """

    def setUp(self):
        self.docx = Document()
        self.docx.styles.add_style('SCL Header Paragraph', WD_STYLE_TYPE.PARAGRAPH)
        self.docx.styles.add_style('SCL Header Paragraph Char', WD_STYLE_TYPE.CHARACTER)
        self.docx.styles.add_style('SCL Journal Title Char', WD_STYLE_TYPE.CHARACTER)

    def _second_header_table(self):
        header = docx_pipe.docx_renderer.section.get_default_header(self.docx)
        return header.tables[-1]

    def _journal_paragraph(self):
        return self._second_header_table().rows[0].cells[0].paragraphs[0]

    def _title_paragraph(self):
        return self._second_header_table().rows[0].cells[1].paragraphs[0]

    def test_journal_title_is_not_split_into_lines(self):
        # Regression: the running header used to reuse the masthead's
        # _format_journal_title_two_lines() treatment, which is sized for
        # the large first-page title and pushed titles that already fit
        # the masthead in two lines into three lines in this narrower,
        # smaller-font running header column instead.
        docx_pipe.docx_second_header_pipe(self.docx, 'Brazilian Journal of Biology', 'Some Article Title')
        self.assertEqual(self._journal_paragraph().runs[0].text, 'Brazilian Journal of Biology')

    def test_journal_title_uses_the_small_header_style_not_the_masthead_style(self):
        docx_pipe.docx_second_header_pipe(self.docx, 'Acta Amazonica', 'Some Article Title')
        self.assertEqual(self._journal_paragraph().runs[0].style.name, 'SCL Header Paragraph Char')

    def test_article_title_is_in_its_own_cell(self):
        docx_pipe.docx_second_header_pipe(self.docx, 'Acta Amazonica', 'Some Article Title')
        self.assertEqual(self._title_paragraph().runs[0].text, 'Some Article Title')

    def test_article_title_is_right_aligned(self):
        docx_pipe.docx_second_header_pipe(self.docx, 'Acta Amazonica', 'Some Article Title')
        self.assertEqual(self._title_paragraph().alignment, WD_ALIGN_PARAGRAPH.RIGHT)

    def test_columns_split_content_width_evenly(self):
        docx_pipe.docx_second_header_pipe(self.docx, 'Acta Amazonica', 'Some Article Title')
        table = self._second_header_table()
        self.assertEqual(table.columns[0].width, table.columns[1].width)

    def test_table_keeps_the_borderless_default_style(self):
        # No style is assigned explicitly, so it stays 'Normal Table' -
        # the borderless default any new python-docx table gets.
        docx_pipe.docx_second_header_pipe(self.docx, 'Acta Amazonica', 'Some Article Title')
        table = self._second_header_table()
        self.assertEqual(table.style.name, 'Normal Table')


class TestDocxSecondFooterPipe(unittest.TestCase):

    def test_uses_fpage_lpage_range_when_present(self):
        docx = _docx_with_layout_styles()
        footer_data = {'volume': '10', 'issue': '2', 'year': '2023',
                       'fpage': 123, 'lpage': 130, 'location_label': '123-130'}
        docx_pipe.docx_second_footer_pipe(docx, footer_data)

        footer = docx_renderer.section.get_second_footer(docx)
        para = footer.paragraphs[0]
        self.assertIn('VOL. 10 (2) 2023: 123-130', para.text)

    def test_uses_elocation_id_when_fpage_is_absent(self):
        docx = _docx_with_layout_styles()
        footer_data = {'volume': '33', 'issue': '3', 'year': '2024',
                       'fpage': '', 'lpage': '', 'location_label': 'e282794'}
        docx_pipe.docx_second_footer_pipe(docx, footer_data)

        footer = docx_renderer.section.get_second_footer(docx)
        para = footer.paragraphs[0]
        self.assertIn('VOL. 33 (3) 2024: e282794', para.text)
        self.assertNotIn(': -', para.text)

    def test_omits_issue_parentheses_when_issue_is_absent(self):
        docx = _docx_with_layout_styles()
        footer_data = {'volume': '86', 'issue': '', 'year': '2026',
                       'fpage': '', 'lpage': '', 'location_label': 'e301043'}
        docx_pipe.docx_second_footer_pipe(docx, footer_data)

        footer = docx_renderer.section.get_second_footer(docx)
        para = footer.paragraphs[0]
        self.assertIn('VOL. 86 2026: e301043', para.text)
        self.assertNotIn('()', para.text)


class TestDocxPageVolIssueYearPipe(unittest.TestCase):

    def test_uses_fpage_lpage_range_when_present(self):
        docx = _docx_with_layout_styles()
        footer_data = {'volume': '10', 'issue': '2', 'year': '2023',
                       'fpage': 123, 'lpage': 130, 'location_label': '123-130'}
        docx_pipe.docx_page_vol_issue_year_pipe(docx, footer_data)

        footer = docx_renderer.section.get_first_page_footer(docx)
        para = footer.paragraphs[-1]
        self.assertIn('VOL. 10 (2) 2023: 123-130', para.text)

    def test_uses_elocation_id_when_fpage_is_absent(self):
        docx = _docx_with_layout_styles()
        footer_data = {'volume': '33', 'issue': '3', 'year': '2024',
                       'fpage': '', 'lpage': '', 'location_label': 'e282794'}
        docx_pipe.docx_page_vol_issue_year_pipe(docx, footer_data)

        footer = docx_renderer.section.get_first_page_footer(docx)
        para = footer.paragraphs[-1]
        self.assertIn('VOL. 33 (3) 2024: e282794', para.text)
        self.assertNotIn(': -', para.text)

    def test_omits_issue_parentheses_when_issue_is_absent(self):
        docx = _docx_with_layout_styles()
        footer_data = {'volume': '86', 'issue': '', 'year': '2026',
                       'fpage': '', 'lpage': '', 'location_label': 'e301043'}
        docx_pipe.docx_page_vol_issue_year_pipe(docx, footer_data)

        footer = docx_renderer.section.get_first_page_footer(docx)
        para = footer.paragraphs[-1]
        self.assertIn('VOL. 86 2026: e301043', para.text)
        self.assertNotIn('()', para.text)


class TestDocxBodyPipe(unittest.TestCase):
    """
    Item 04 of the pdf_generator backlog: a body paragraph is now a list
    of style-tagged segments (see xml_utils.get_segments_from_node)
    instead of a single string, and each segment must become its own
    run with matching bold/italic/superscript/subscript formatting.
    """

    def _segment(self, text, **flags):
        seg = {'type': 'text', 'text': text, 'italic': False, 'bold': False, 'superscript': False, 'subscript': False}
        seg.update(flags)
        return seg

    def test_paragraph_emits_one_run_per_segment_with_matching_style(self):
        docx = _docx_with_layout_styles()
        body_data = [{
            'level': 2,
            'title': None,
            'paragraphs': [[
                self._segment('A '),
                self._segment('Genus species', italic=True),
                self._segment(' seen'),
                self._segment('1', superscript=True),
                self._segment('.'),
            ]],
            'tables': [],
            'figures': [],
        }]
        docx_pipe.docx_body_pipe(docx, body_data)

        para = docx.paragraphs[-1]
        self.assertEqual([r.text for r in para.runs], ['A ', 'Genus species', ' seen', '1', '.'])
        self.assertIsNone(para.runs[0].italic)
        self.assertTrue(para.runs[1].italic)
        self.assertIsNone(para.runs[2].italic)
        self.assertTrue(para.runs[3].font.superscript)
        self.assertIsNone(para.runs[4].font.superscript)

    def test_superscript_and_subscript_segments_in_the_same_paragraph(self):
        # Regression: python-docx backs superscript/subscript with the
        # same OOXML w:vertAlign element, so unconditionally assigning
        # both on every run (even the falsy one, as None) clears
        # whichever was set first instead of leaving it alone.
        docx = _docx_with_layout_styles()
        body_data = [{
            'level': 2,
            'title': None,
            'paragraphs': [[
                self._segment('1', superscript=True),
                self._segment(' and '),
                self._segment('2', subscript=True),
            ]],
            'tables': [],
            'figures': [],
        }]
        docx_pipe.docx_body_pipe(docx, body_data)

        runs = docx.paragraphs[-1].runs
        self.assertTrue(runs[0].font.superscript)
        self.assertTrue(runs[2].font.subscript)

    def test_unstyled_segment_does_not_force_run_bold_false(self):
        # An explicit False on run.bold overrides the style's own default
        # instead of inheriting it; a segment with no style must leave
        # the run's bold/italic/superscript/subscript unset (None).
        docx = _docx_with_layout_styles()
        body_data = [{
            'level': 2,
            'title': None,
            'paragraphs': [[self._segment('Plain text.')]],
            'tables': [],
            'figures': [],
        }]
        docx_pipe.docx_body_pipe(docx, body_data)

        run = docx.paragraphs[-1].runs[0]
        self.assertIsNone(run.bold)
        self.assertIsNone(run.italic)
        self.assertIsNone(run.font.superscript)
        self.assertIsNone(run.font.subscript)


class TestDocxReferencesPipe(unittest.TestCase):
    """
    Regression: SCL Paragraph Reference uses the same font size as body
    text and has no line_spacing of its own, so a reference wrapping to
    multiple lines rendered with the same loose spacing as a body
    paragraph. Line spacing is now set explicitly on each reference
    paragraph.
    """

    def test_reference_has_single_line_spacing(self):
        docx = _docx_with_layout_styles()
        docx_pipe.docx_references_pipe(docx, references=['Author A. Title B. Journal C. 2020.'])
        para = docx.paragraphs[-1]
        self.assertEqual(para.paragraph_format.line_spacing, 1.0)


class TestDocxAcknowledgmentsPipe(unittest.TestCase):
    # TODO
    ...


class TestDocxSupplementaryMaterialPipe(unittest.TestCase):

    def test_footer_has_no_leading_pipe(self):
        docx = _docx_with_layout_styles()
        footer_data = {'volume': '53', 'issue': '4', 'year': '2023',
                       'fpage': 271, 'lpage': 280, 'location_label': '271-280'}
        docx_pipe.docx_supplementary_material_pipe(
            docx, footer_data, {'title': 'Supplementary Material', 'elements': []}
        )

        footer = docx.sections[-1].footer
        para = footer.paragraphs[-1]
        self.assertEqual(para.text, 'VOL. 53 (4) 2023: 271-280')

    def test_uses_elocation_id_when_fpage_is_absent(self):
        docx = _docx_with_layout_styles()
        footer_data = {'volume': '33', 'issue': '3', 'year': '2024',
                       'fpage': '', 'lpage': '', 'location_label': 'e282794'}
        docx_pipe.docx_supplementary_material_pipe(
            docx, footer_data, {'title': 'Supplementary Material', 'elements': []}
        )

        footer = docx.sections[-1].footer
        para = footer.paragraphs[-1]
        self.assertEqual(para.text, 'VOL. 33 (3) 2024: e282794')

    def test_omits_issue_parentheses_when_issue_is_absent(self):
        docx = _docx_with_layout_styles()
        footer_data = {'volume': '86', 'issue': '', 'year': '2026',
                       'fpage': '', 'lpage': '', 'location_label': 'e301043'}
        docx_pipe.docx_supplementary_material_pipe(
            docx, footer_data, {'title': 'Supplementary Material', 'elements': []}
        )

        footer = docx.sections[-1].footer
        para = footer.paragraphs[-1]
        self.assertEqual(para.text, 'VOL. 86 2026: e301043')


class TestFormatVolIssueYear(unittest.TestCase):

    def test_keeps_both_when_present(self):
        footer_data = {'volume': '10', 'issue': '2', 'year': '2023', 'location_label': '123-130'}
        self.assertEqual(docx_pipe._format_vol_issue_year(footer_data), 'VOL. 10 (2) 2023: 123-130')

    def test_omits_issue_parentheses_when_issue_is_absent(self):
        footer_data = {'volume': '86', 'issue': '', 'year': '2026', 'location_label': 'e301043'}
        self.assertEqual(docx_pipe._format_vol_issue_year(footer_data), 'VOL. 86 2026: e301043')

    def test_omits_vol_label_when_volume_is_absent(self):
        footer_data = {'volume': '', 'issue': '67', 'year': '2023', 'location_label': 'e236720'}
        self.assertEqual(docx_pipe._format_vol_issue_year(footer_data), '(67) 2023: e236720')


class TestAddTwoColumnHeaderTable(unittest.TestCase):

    def test_default_split_is_even(self):
        docx = Document()
        header = docx_renderer.section.get_first_page_header(docx)
        left_cell, right_cell = docx_pipe._add_two_column_header_table(header)
        table = header.tables[-1]
        self.assertEqual(table.columns[0].width, table.columns[1].width)

    def test_custom_ratio_splits_unevenly(self):
        docx = Document()
        header = docx_renderer.section.get_first_page_header(docx)
        docx_pipe._add_two_column_header_table(header, left_ratio=0.65)
        table = header.tables[-1]
        content_width = int(docx_pipe._content_width())
        self.assertAlmostEqual(table.columns[0].width, int(content_width * 0.65), delta=500)
        self.assertAlmostEqual(
            table.columns[1].width, content_width - int(content_width * 0.65), delta=500
        )

    def test_table_keeps_the_borderless_default_style(self):
        docx = Document()
        header = docx_renderer.section.get_first_page_header(docx)
        docx_pipe._add_two_column_header_table(header)
        table = header.tables[-1]
        self.assertEqual(table.style.name, 'Normal Table')

    def test_removes_the_auto_created_empty_placeholder_paragraph(self):
        # python-docx auto-creates one empty paragraph the first time a
        # header's body is accessed; add_table() appends after it rather
        # than replacing it, so left alone it reserves a blank line's
        # worth of vertical space above the table.
        docx = Document()
        header = docx_renderer.section.get_first_page_header(docx)
        docx_pipe._add_two_column_header_table(header)
        self.assertEqual(len(header.paragraphs), 0)

    def test_keeps_a_placeholder_paragraph_that_already_has_text(self):
        docx = Document()
        header = docx_renderer.section.get_first_page_header(docx)
        header.paragraphs[0].add_run('not actually empty')
        docx_pipe._add_two_column_header_table(header)
        self.assertEqual(len(header.paragraphs), 1)
        self.assertEqual(header.paragraphs[0].text, 'not actually empty')

    def test_zeroes_left_and_right_cell_margins(self):
        # The OOXML default (108 twips = 5.4pt) offsets a header table's
        # content from the flush-left/flush-right text used everywhere
        # else in the document, since a plain paragraph has no such margin.
        docx = Document()
        header = docx_renderer.section.get_first_page_header(docx)
        docx_pipe._add_two_column_header_table(header)
        table = header.tables[-1]
        tblCellMar = table._tbl.tblPr.find(docx_pipe.qn('w:tblCellMar'))
        self.assertIsNotNone(tblCellMar)
        left = tblCellMar.find(docx_pipe.qn('w:left'))
        right = tblCellMar.find(docx_pipe.qn('w:right'))
        self.assertEqual(left.get(docx_pipe.qn('w:w')), '0')
        self.assertEqual(right.get(docx_pipe.qn('w:w')), '0')


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
