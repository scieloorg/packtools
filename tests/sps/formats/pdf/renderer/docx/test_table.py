import unittest

from docx import Document
from docx.shared import Cm

from packtools.sps.formats.pdf.renderer.docx.table import (
    _compute_table_width,
    _add_caption_paragraph,
    _determine_num_cols,
    add_table,
)
from packtools.sps.formats.pdf import enum as pdf_enum


class TestComputeTableWidth(unittest.TestCase):
    """
    Regression tests: within-column table width must honor
    'default_column_count' from page_attributes instead of always dividing
    by a hardcoded 2.
    """

    def _page_attributes(self, default_column_count):
        attrs = dict(pdf_enum.PAGE_ATTRIBUTES)
        attrs['default_column_count'] = default_column_count
        return attrs

    def test_two_columns_matches_legacy_formula(self):
        attrs = self._page_attributes(2)
        content_width, table_width, layout = _compute_table_width(attrs, {})
        spacing_cm = Cm(pdf_enum.TWO_COLUMNS_SPACING / 567.0)
        expected = (content_width - spacing_cm) // 2
        self.assertEqual(table_width, expected)
        self.assertEqual(layout, pdf_enum.DOUBLE_COLUMN_PAGE_LABEL)

    def test_one_column_equals_full_content_width(self):
        attrs = self._page_attributes(1)
        content_width, table_width, _ = _compute_table_width(attrs, {})
        self.assertEqual(table_width, content_width)

    def test_three_columns_uses_generic_formula(self):
        attrs = self._page_attributes(3)
        content_width, table_width, layout = _compute_table_width(attrs, {})
        spacing_cm = Cm(pdf_enum.TWO_COLUMNS_SPACING / 567.0)
        expected = (content_width - 2 * spacing_cm) // 3
        self.assertEqual(table_width, expected)
        self.assertEqual(layout, pdf_enum.DOUBLE_COLUMN_PAGE_LABEL)

    def test_single_column_layout_override_ignores_column_count(self):
        attrs = self._page_attributes(1)
        content_width, table_width, layout = _compute_table_width(
            attrs, {'layout': pdf_enum.SINGLE_COLUMN_PAGE_LABEL}
        )
        self.assertEqual(table_width, content_width)
        self.assertEqual(layout, pdf_enum.SINGLE_COLUMN_PAGE_LABEL)


class TestAddCaptionParagraph(unittest.TestCase):
    """
    Regression: the caption paragraph's own style (SCL Table Heading) has no
    line_spacing, so it fell back to the same loose spacing as body text -
    only the smaller caption font size made it look somewhat tighter. Line
    spacing is now set explicitly, independent of whether the named style
    resolves.
    """

    def test_caption_has_single_line_spacing(self):
        docx = Document()
        p = _add_caption_paragraph(
            docx, {'label': 'Table 1', 'title': 'A caption'}, 'SCL Table Heading'
        )
        self.assertEqual(p.paragraph_format.line_spacing, 1.0)

    def test_line_spacing_set_even_when_named_style_is_missing(self):
        docx = Document()
        p = _add_caption_paragraph(
            docx, {'label': 'Table 1', 'title': 'A caption'}, 'Does Not Exist'
        )
        self.assertEqual(p.paragraph_format.line_spacing, 1.0)


class TestAddTableFoot(unittest.TestCase):
    """
    Regression tests: <table-wrap-foot> notes extracted into table_data['foot']
    must be rendered as paragraphs below the table, they were previously
    dropped silently since nothing in the renderer read that key.
    """

    def _table_data(self, foot):
        return {
            'label': 'Table 1',
            'title': 'Sample',
            'headers': [['Col1']],
            'rows': [['Data1']],
            'layout': pdf_enum.DOUBLE_COLUMN_PAGE_LABEL,
            'column_widths': [50],
            'header_spans': [[{'colspan': 1, 'rowspan': 1, 'text': 'Col1'}]],
            'row_spans': [[{'colspan': 1, 'rowspan': 1, 'text': 'Data1'}]],
            'foot': foot,
        }

    def test_foot_notes_are_rendered_as_paragraphs(self):
        docx = Document()
        add_table(docx, self._table_data(['Source: Authors.', '* p < 0.05.']))
        body_text = [p.text for p in docx.paragraphs]
        self.assertIn('Source: Authors.', body_text)
        self.assertIn('* p < 0.05.', body_text)

    def test_no_foot_notes_adds_no_extra_paragraphs(self):
        docx = Document()
        add_table(docx, self._table_data([]))
        body_text = [p.text for p in docx.paragraphs]
        self.assertNotIn('Source: Authors.', body_text)


class TestDetermineNumColsHeaderBodyMismatch(unittest.TestCase):
    """
    Regression for issue #1371: thead and tbody get their column count
    computed independently (each section's own _calculate_max_columns), so
    a real table whose header genuinely has fewer columns than its body -
    with no colspan explaining the gap - used to size the DOCX table to
    the header's (smaller) column count. _apply_body_spans then indexed
    past the end of each row's cells for the extra body columns, crashing
    with IndexError. _determine_num_cols must take the max across both.
    """

    def _span_row(self, n):
        return [{'colspan': 1, 'rowspan': 1, 'text': f'c{i}'} for i in range(n)]

    def test_body_wider_than_header_uses_body_width(self):
        header_spans = [self._span_row(2)]
        row_spans = [self._span_row(3)]
        num_cols = _determine_num_cols([], [], header_spans, row_spans)
        self.assertEqual(num_cols, 3)

    def test_header_wider_than_body_uses_header_width(self):
        header_spans = [self._span_row(4)]
        row_spans = [self._span_row(2)]
        num_cols = _determine_num_cols([], [], header_spans, row_spans)
        self.assertEqual(num_cols, 4)

    def test_no_spans_falls_back_to_widest_of_headers_and_rows(self):
        headers = [['H1', 'H2']]
        rows = [['A', 'B', 'C']]
        num_cols = _determine_num_cols(headers, rows, [], [])
        self.assertEqual(num_cols, 3)


class TestAddTableHeaderBodyColumnMismatch(unittest.TestCase):
    """
    End-to-end regression for issue #1371, using the real shape
    extract_table_data returns: a 2-column thead and a 3-column tbody
    (no colspan on either), as seen in real corpus data (a structured
    report-style table). add_table must not raise, and the resulting DOCX
    table must have enough columns for every body cell.
    """

    def _table_data(self):
        return {
            'label': 'Table 1',
            'title': 'Header/body column count mismatch',
            'headers': [['', 'H1']],
            'rows': [['row-label', 'A', 'B']],
            'layout': pdf_enum.DOUBLE_COLUMN_PAGE_LABEL,
            'column_widths': [],
            'header_spans': [[
                {'colspan': 1, 'rowspan': 1, 'text': ''},
                {'colspan': 1, 'rowspan': 1, 'text': 'H1'},
            ]],
            'row_spans': [[
                {'colspan': 1, 'rowspan': 1, 'text': 'row-label'},
                {'colspan': 1, 'rowspan': 1, 'text': 'A'},
                {'colspan': 1, 'rowspan': 1, 'text': 'B'},
            ]],
            'foot': [],
        }

    def test_does_not_raise(self):
        docx = Document()
        add_table(docx, self._table_data())
        self.assertEqual(len(docx.tables), 1)

    def test_table_has_enough_columns_for_body(self):
        docx = Document()
        add_table(docx, self._table_data())
        table = docx.tables[0]
        self.assertEqual(len(table.columns), 3)
        self.assertEqual(table.rows[-1].cells[2].text, 'B')


if __name__ == "__main__":
    unittest.main()
