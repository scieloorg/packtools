import unittest

from lxml import etree

from packtools.sps.formats.pdf import enum as pdf_enum
from packtools.sps.formats.pdf.extract import tables
from packtools.sps.formats.pdf.layout import table_layout


def _layout(xml_str, override=None):
    data = tables.read_table_wrap(etree.fromstring(xml_str))
    return table_layout.determine_table_layout(data, override=override)


def _row(n):
    return '<tr>' + ''.join(f'<td>{i}</td>' for i in range(n)) + '</tr>'


class TestDetermineTableLayout(unittest.TestCase):

    def test_single_long_cell_forces_single_column(self):
        long_text = "x" * 500
        xml_str = f"<table-wrap><table><tbody><tr><td>{long_text}</td></tr></tbody></table></table-wrap>"
        self.assertEqual(_layout(xml_str), pdf_enum.SINGLE_COLUMN_PAGE_LABEL)

    def test_moderately_long_cell_stays_double_column(self):
        moderate_text = "x" * 150
        xml_str = f"<table-wrap><table><tbody><tr><td>{moderate_text}</td></tr></tbody></table></table-wrap>"
        self.assertEqual(_layout(xml_str), pdf_enum.DOUBLE_COLUMN_PAGE_LABEL)

    def test_more_than_four_columns_forces_single_column(self):
        xml_str = f"<table-wrap><table><tbody>{_row(5)}</tbody></table></table-wrap>"
        self.assertEqual(_layout(xml_str), pdf_enum.SINGLE_COLUMN_PAGE_LABEL)

    def test_four_columns_stays_double_column(self):
        xml_str = f"<table-wrap><table><tbody>{_row(4)}</tbody></table></table-wrap>"
        self.assertEqual(_layout(xml_str), pdf_enum.DOUBLE_COLUMN_PAGE_LABEL)

    def test_colspan_counts_towards_columns(self):
        xml_str = (
            '<table-wrap><table><thead><tr><th colspan="5">Wide header</th></tr></thead>'
            f'<tbody>{_row(2)}</tbody></table></table-wrap>'
        )
        self.assertEqual(_layout(xml_str), pdf_enum.SINGLE_COLUMN_PAGE_LABEL)

    def test_later_wide_panel_decides_the_whole_wrap(self):
        xml_str = (
            f'<table-wrap><table><tbody>{_row(2)}</tbody></table>'
            f'<table><tbody>{_row(6)}</tbody></table></table-wrap>'
        )
        self.assertEqual(_layout(xml_str), pdf_enum.SINGLE_COLUMN_PAGE_LABEL)

    def test_long_cell_outside_header_and_body_grids_still_counts(self):
        long_text = "x" * 500
        xml_str = (
            f'<table-wrap><table><tbody>{_row(2)}</tbody>'
            f'<tfoot><tr><td>{long_text}</td></tr></tfoot></table></table-wrap>'
        )
        self.assertEqual(_layout(xml_str), pdf_enum.SINGLE_COLUMN_PAGE_LABEL)

    def test_override_wins(self):
        xml_str = f"<table-wrap><table><tbody>{_row(6)}</tbody></table></table-wrap>"
        self.assertEqual(
            _layout(xml_str, override=pdf_enum.DOUBLE_COLUMN_PAGE_LABEL),
            pdf_enum.DOUBLE_COLUMN_PAGE_LABEL,
        )

    def test_invalid_override_is_ignored(self):
        xml_str = f"<table-wrap><table><tbody>{_row(6)}</tbody></table></table-wrap>"
        self.assertEqual(_layout(xml_str, override='bogus'), pdf_enum.SINGLE_COLUMN_PAGE_LABEL)

    def test_empty_wrap_is_double_column(self):
        self.assertEqual(_layout('<table-wrap/>'), pdf_enum.DOUBLE_COLUMN_PAGE_LABEL)


class TestCalculateColumnWidths(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(table_layout.calculate_column_widths([], []), [])

    def test_min_and_max_width(self):
        widths = table_layout.calculate_column_widths([['a', 'b' * 100]], [])
        self.assertEqual(widths, [50, 200])

    def test_scales_down_when_total_is_too_wide(self):
        widths = table_layout.calculate_column_widths([], [['b' * 100] * 3])
        self.assertEqual(widths, [166, 166, 166])


class TestCalculateColumnWidthsEdgeCases(unittest.TestCase):

    def test_rows_without_cells(self):
        self.assertEqual(table_layout.calculate_column_widths([[]], [[]]), [])

    def test_headers_only(self):
        self.assertEqual(table_layout.calculate_column_widths([['a', 'b']], []), [50, 50])

    def test_empty_cells_get_min_width(self):
        self.assertEqual(table_layout.calculate_column_widths([], [['', 'x']]), [50, 50])


class TestEstimateTextWidth(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(table_layout._estimate_text_width(''), 0)

    def test_character_weights(self):
        # 'A' 1.2 + '1' 1.0 + 'i' 0.5 + 'm' 1.5 + 'a' 1.0 = 5.2
        self.assertEqual(table_layout._estimate_text_width('A1ima'), 5)

    def test_collapses_whitespace(self):
        self.assertEqual(table_layout._estimate_text_width('  a   b  '), 3)


if __name__ == '__main__':
    unittest.main()
