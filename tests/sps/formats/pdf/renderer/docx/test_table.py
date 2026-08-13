import unittest

from packtools.sps.formats.pdf import enum as pdf_enum
from packtools.sps.formats.pdf.layout_config import LayoutConfig, PageProfile
from packtools.sps.formats.pdf.renderer.docx import table as table_renderer


class TestComputeTableWidth(unittest.TestCase):

    def test_full_page_width_layout_ignores_layout_config(self):
        table_data = {"layout": pdf_enum.SINGLE_COLUMN_PAGE_LABEL}
        content_width, table_width, layout = table_renderer._compute_table_width(
            pdf_enum.PAGE_ATTRIBUTES, table_data
        )
        self.assertEqual(table_width, content_width)
        self.assertEqual(layout, pdf_enum.SINGLE_COLUMN_PAGE_LABEL)

    def test_within_column_without_layout_config_matches_legacy_formula(self):
        table_data = {"layout": pdf_enum.DOUBLE_COLUMN_PAGE_LABEL}
        _, table_width, _ = table_renderer._compute_table_width(pdf_enum.PAGE_ATTRIBUTES, table_data)
        _, legacy_width, _ = table_renderer._compute_table_width(pdf_enum.PAGE_ATTRIBUTES, table_data)
        self.assertEqual(table_width, legacy_width)

    def test_within_column_with_one_column_layout_config_uses_full_content_width(self):
        # The bug found and fixed while calibrating a real 1-column journal
        # (Anuário Antropológico): the legacy formula always halves the
        # content width, which is wrong when the journal only has 1 column.
        profile = PageProfile(default_column_count=1)
        cfg = LayoutConfig(profile=profile)
        table_data = {"layout": pdf_enum.DOUBLE_COLUMN_PAGE_LABEL}
        content_width, table_width, _ = table_renderer._compute_table_width(
            pdf_enum.PAGE_ATTRIBUTES, table_data, layout_config=cfg
        )
        self.assertAlmostEqual(table_width.pt, profile.content_width_pt, places=1)

    def test_within_column_with_two_column_layout_config_uses_column_width(self):
        profile = PageProfile(default_column_count=2)
        cfg = LayoutConfig(profile=profile)
        table_data = {"layout": pdf_enum.DOUBLE_COLUMN_PAGE_LABEL}
        _, table_width, _ = table_renderer._compute_table_width(
            pdf_enum.PAGE_ATTRIBUTES, table_data, layout_config=cfg
        )
        self.assertAlmostEqual(table_width.pt, profile.column_width_pt(2), places=1)


if __name__ == "__main__":
    unittest.main()
