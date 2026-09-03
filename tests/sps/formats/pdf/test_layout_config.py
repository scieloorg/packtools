import json
import tempfile
import unittest
from pathlib import Path

from docx.enum.section import WD_ORIENT, WD_SECTION

from packtools.sps.formats.pdf import layout_config


class TestLoadPageAttributes(unittest.TestCase):
    """
    Regression tests for the JSON-backed replacement of the legacy hardcoded
    PAGE_ATTRIBUTES dict. Length values are compared with a tolerance of a
    few EMU: converting through a decimal pt value in JSON can't guarantee
    perfect round-trip precision from the original Cm() literals, and a
    handful of EMU (1/914400 inch) has no visible or functional effect.
    """

    def setUp(self):
        self.attrs = layout_config.load_page_attributes()

    def _assert_close(self, actual, expected, tolerance_emu=5):
        self.assertLessEqual(abs(int(actual) - int(expected)), tolerance_emu)

    def test_matches_legacy_hardcoded_values(self):
        from docx.shared import Cm

        self._assert_close(self.attrs['top_margin'], Cm(3.5))
        self._assert_close(self.attrs['left_margin'], Cm(2))
        self._assert_close(self.attrs['right_margin'], Cm(2))
        self._assert_close(self.attrs['bottom_margin'], Cm(2))
        self._assert_close(self.attrs['header_distance'], Cm(1))
        self._assert_close(self.attrs['footer_distance'], Cm(1))
        self._assert_close(self.attrs['gutter'], Cm(0))
        self._assert_close(self.attrs['page_width'], Cm(21.0))
        self._assert_close(self.attrs['page_height'], Cm(29.7))
        self.assertEqual(self.attrs['orientation'], WD_ORIENT.PORTRAIT)
        self.assertEqual(self.attrs['different_first_page_header_footer'], True)
        self.assertEqual(self.attrs['start_type'], WD_SECTION.CONTINUOUS)
        self.assertEqual(self.attrs['default_column_count'], 2)

    def test_load_column_spacing_twips_matches_legacy_constant(self):
        self.assertEqual(layout_config.load_column_spacing_twips(), 300)

    def test_custom_path_overrides_default(self):
        custom = {
            "schema_version": 1,
            "page": {
                "page_width_pt": 400.0,
                "page_height_pt": 600.0,
                "orientation": "landscape",
                "top_margin_pt": 10.0,
                "left_margin_pt": 10.0,
                "right_margin_pt": 10.0,
                "bottom_margin_pt": 10.0,
                "header_distance_pt": 5.0,
                "footer_distance_pt": 5.0,
                "gutter_pt": 0,
                "different_first_page_header_footer": False,
                "body_start_type": "new_page",
                "default_column_count": 1,
                "column_spacing_pt": 0,
            },
        }
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "custom.json"
            path.write_text(json.dumps(custom))

            attrs = layout_config.load_page_attributes(path)
            self.assertEqual(attrs['orientation'], WD_ORIENT.LANDSCAPE)
            self.assertEqual(attrs['start_type'], WD_SECTION.NEW_PAGE)
            self.assertEqual(attrs['default_column_count'], 1)
            self.assertEqual(attrs['different_first_page_header_footer'], False)

            self.assertEqual(layout_config.load_column_spacing_twips(path), 0)


if __name__ == "__main__":
    unittest.main()
