import tempfile
import unittest
import os

from docx import Document
from docx.shared import Cm, Emu

from packtools.sps.formats.pdf import enum as pdf_enum
from packtools.sps.formats.pdf.layout_config import LayoutConfig, PageProfile
from packtools.sps.formats.pdf.renderer.docx import figure as figure_renderer


class TestComputeSingleColumnWidth(unittest.TestCase):

    def test_without_layout_config_matches_legacy_two_column_formula(self):
        page_attributes = pdf_enum.PAGE_ATTRIBUTES
        result = figure_renderer._compute_single_column_width(page_attributes)
        content_width = figure_renderer._compute_content_width(page_attributes)
        column_spacing = Cm(pdf_enum.TWO_COLUMNS_SPACING / 567.0)
        expected = (content_width - column_spacing) / 2
        self.assertEqual(result, expected)

    def test_with_layout_config_one_column_uses_full_content_width(self):
        # Without layout_config, this journal's actual 1-column layout would
        # still be halved by the legacy formula - the bug found and fixed
        # while calibrating a real 1-column journal (Anuário Antropológico).
        profile = PageProfile(default_column_count=1)
        cfg = LayoutConfig(profile=profile)
        result = figure_renderer._compute_single_column_width({}, layout_config=cfg)
        self.assertAlmostEqual(result.pt, profile.content_width_pt, places=1)

    def test_with_layout_config_two_columns_uses_column_width(self):
        profile = PageProfile(default_column_count=2)
        cfg = LayoutConfig(profile=profile)
        result = figure_renderer._compute_single_column_width({}, layout_config=cfg)
        self.assertAlmostEqual(result.pt, profile.column_width_pt(2), places=1)


class TestNaturalWidthCapped(unittest.TestCase):

    def test_missing_image_falls_back_to_ceiling(self):
        result = figure_renderer._natural_width_capped(None, Cm(10))
        self.assertEqual(result, Cm(10))

    def test_nonexistent_path_falls_back_to_ceiling(self):
        result = figure_renderer._natural_width_capped("/no/such/file.png", Cm(10))
        self.assertEqual(result, Cm(10))


class TestTryInsertPictureUsesExplicitWidth(unittest.TestCase):
    """
    Regression test for a bug caught during review, before the first commit:
    _try_insert_picture used to call add_picture(img_path) with no explicit
    width, letting python-docx infer a size from its own, independent DPI
    reading - which can silently disagree with _infer_image_dpi (the reader
    used to compute content_width in the first place), especially for images
    with no DPI metadata at all (python-docx defaults to 72 DPI; the code in
    this module defaults to 96 DPI - a real, confirmed ~33% size difference).
    """

    def setUp(self):
        try:
            from PIL import Image
        except ImportError:
            self.skipTest("Pillow not available")
        self.tmpdir = tempfile.TemporaryDirectory()
        self.img_path = os.path.join(self.tmpdir.name, "no_dpi_metadata.png")
        # Deliberately saved without a dpi= argument, so the file carries no
        # DPI metadata at all - the exact case where python-docx's and
        # _infer_image_dpi's defaults diverge (72 DPI vs. 96 DPI).
        Image.new("RGB", (300, 200), "blue").save(self.img_path)

    def tearDown(self):
        self.tmpdir.cleanup()

    def test_inserted_width_matches_a_narrower_explicit_content_width(self):
        docx = Document()
        content_width = Emu(1_000_000)  # narrower than python-docx's own ~3.81M EMU estimate
        inserted = figure_renderer._try_insert_picture(docx, self.img_path, content_width, {})
        self.assertTrue(inserted)
        self.assertEqual(docx.inline_shapes[-1].width, content_width)

    def test_inserted_width_matches_a_wider_explicit_content_width(self):
        # This is the case that exposed the bug: with the old code (add_picture
        # called with no width, followed by a scale-down-only fit), a
        # content_width *larger* than python-docx's own ~3.81M EMU estimate for
        # this image was silently ignored - the scale-down-only logic has
        # nothing to do when the target is already larger than the source, so
        # the picture stayed at python-docx's own (possibly wrong) size instead
        # of the caller's explicitly computed one.
        docx = Document()
        content_width = Emu(5_000_000)  # wider than python-docx's own ~3.81M EMU estimate
        inserted = figure_renderer._try_insert_picture(docx, self.img_path, content_width, {})
        self.assertTrue(inserted)
        self.assertEqual(docx.inline_shapes[-1].width, content_width)


if __name__ == "__main__":
    unittest.main()
