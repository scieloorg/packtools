import unittest

from docx.shared import Cm

from packtools.sps.formats.pdf.renderer.docx.figure import _compute_single_column_width
from packtools.sps.formats.pdf import enum as pdf_enum


class TestComputeSingleColumnWidth(unittest.TestCase):
    """
    Regression tests: column width must honor 'default_column_count' from
    page_attributes instead of always dividing by a hardcoded 2, so a
    1-column body doesn't get its figures/tables sized as if there were
    two columns.
    """

    def _page_attributes(self, default_column_count):
        attrs = dict(pdf_enum.PAGE_ATTRIBUTES)
        attrs['default_column_count'] = default_column_count
        return attrs

    def test_two_columns_matches_legacy_formula(self):
        attrs = self._page_attributes(2)
        content_width = attrs['page_width'] - attrs['left_margin'] - attrs['right_margin']
        spacing_cm = Cm(pdf_enum.TWO_COLUMNS_SPACING / 567.0)
        expected = (content_width - spacing_cm) / 2
        self.assertEqual(_compute_single_column_width(attrs), expected)

    def test_one_column_equals_full_content_width(self):
        attrs = self._page_attributes(1)
        content_width = attrs['page_width'] - attrs['left_margin'] - attrs['right_margin']
        self.assertEqual(_compute_single_column_width(attrs), content_width)

    def test_missing_key_defaults_to_two_columns(self):
        attrs = dict(pdf_enum.PAGE_ATTRIBUTES)
        attrs.pop('default_column_count', None)
        two_col_attrs = self._page_attributes(2)
        self.assertEqual(
            _compute_single_column_width(attrs),
            _compute_single_column_width(two_col_attrs),
        )


if __name__ == "__main__":
    unittest.main()
