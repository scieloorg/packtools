import unittest

from docx.shared import Cm

from packtools.sps.formats.pdf.renderer.docx.table import _compute_table_width
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


if __name__ == "__main__":
    unittest.main()
