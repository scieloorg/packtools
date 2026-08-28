import os
import tempfile
import unittest

from docx import Document
from docx.shared import Cm
from PIL import Image

from packtools.sps.formats.pdf.renderer.docx.figure import (
    _infer_image_dpi,
    _natural_width_capped,
    add_figure,
    decide_figure_layout,
)
from packtools.sps.formats.pdf import enum as pdf_enum


class TestDecideFigureLayoutUnits(unittest.TestCase):
    """
    Regression test for a units bug: single_col_width degrades from a Cm
    object to a raw EMU number under python-docx's Length arithmetic (it has
    no operator overloads that preserve units), so comparing it directly
    against width_in_cm (a real centimeter float) compared cm against EMU -
    a ~360000x scale mismatch that made the full-width branch unreachable
    for any real image, regardless of size.
    """

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)

    def _make_png(self, px_width, px_height=200, dpi=96):
        path = os.path.join(self.tmpdir.name, f"img_{px_width}.png")
        Image.new("RGB", (px_width, px_height), color="white").save(
            path, format="PNG", dpi=(dpi, dpi)
        )
        return path

    def test_wide_image_gets_full_width_layout(self):
        # ~18.5cm at 96 DPI - wider than a single column (~8.2cm) by far more
        # than the 1.1 threshold, on an A4/2-column default page.
        img_path = self._make_png(px_width=698)
        docx = Document()
        fig = {"href": img_path, "label": "Figure 1"}
        self.assertEqual(
            decide_figure_layout(docx, fig), pdf_enum.SINGLE_COLUMN_PAGE_LABEL
        )

    def test_narrow_image_stays_within_column(self):
        # ~2.6cm at 96 DPI - well under the single-column width.
        img_path = self._make_png(px_width=100)
        docx = Document()
        fig = {"href": img_path, "label": "Figure 1"}
        self.assertEqual(
            decide_figure_layout(docx, fig), pdf_enum.DOUBLE_COLUMN_PAGE_LABEL
        )

    def test_untagged_image_uses_print_resolution_fallback(self):
        # An image with no DPI tag at all must fall back to print
        # resolution, not screen resolution.
        img_path = self._make_png(px_width=700)
        with Image.open(img_path) as im:
            im.info.pop("dpi", None)
            im.save(img_path)  # re-save without the dpi tag
        docx = Document()
        fig = {"href": img_path, "label": "Graph 1"}
        self.assertEqual(
            decide_figure_layout(docx, fig), pdf_enum.DOUBLE_COLUMN_PAGE_LABEL
        )

    def test_layout_dpi_override_replaces_embedded_dpi(self):
        # 'layout_dpi_override' must take precedence over the image's own
        # embedded DPI.
        img_path = self._make_png(px_width=612, dpi=72)
        docx = Document()
        fig = {"href": img_path, "label": "Graph 1", "layout_dpi_override": 300.0}
        self.assertEqual(
            decide_figure_layout(docx, fig), pdf_enum.DOUBLE_COLUMN_PAGE_LABEL
        )


class TestNaturalWidthCapped(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)

    def _make_png(self, px_width=200, px_height=100, dpi=None):
        path = os.path.join(self.tmpdir.name, "img.png")
        im = Image.new("RGB", (px_width, px_height), color="white")
        if dpi:
            im.save(path, format="PNG", dpi=(dpi, dpi))
        else:
            im.save(path, format="PNG")
        return path

    def test_natural_width_shrinks_to_ceiling_when_larger(self):
        img_path = self._make_png(px_width=4000, dpi=96)
        ceiling = Cm(10)
        result = _natural_width_capped(img_path, ceiling)
        self.assertEqual(result, ceiling)

    def test_natural_width_kept_when_smaller_than_ceiling(self):
        img_path = self._make_png(px_width=200, dpi=96)
        ceiling = Cm(10)
        result = _natural_width_capped(img_path, ceiling)
        expected = Cm((200 / 96) * 2.54)
        # PNG's pHYs chunk stores pixels-per-meter (integer), so the DPI read
        # back after a save/load round-trip is a close approximation, not
        # bit-exact - allow a small tolerance instead of exact EMU equality.
        self.assertAlmostEqual(int(result), int(expected), delta=5000)
        self.assertLess(result, ceiling)

    def test_missing_file_falls_back_to_ceiling(self):
        ceiling = Cm(10)
        result = _natural_width_capped("/no/such/file.png", ceiling)
        self.assertEqual(result, ceiling)


class TestAddFigureInsertedWidth(unittest.TestCase):
    """
    Regression test for the DPI mismatch between _infer_image_dpi (used to
    decide the figure's width) and python-docx's own DPI reading (used when
    add_picture() is called without an explicit width, defaulting to 72 DPI
    vs _infer_image_dpi's 96 DPI fallback - a ~33% size difference).
    """

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)

    def test_inserted_picture_width_matches_infer_image_dpi_not_python_docx_default(self):
        img_path = os.path.join(self.tmpdir.name, "no_dpi.png")
        Image.new("RGB", (200, 100), color="white").save(img_path, format="PNG")

        docx = Document()
        figure_data = {"href": img_path, "label": "Figure 1", "caption": "test"}
        add_figure(docx, figure_data)

        self.assertEqual(len(docx.inline_shapes), 1)
        inserted_width = docx.inline_shapes[0].width

        with Image.open(img_path) as im:
            dpi = _infer_image_dpi(im)
        expected_width = int(Cm((200 / dpi) * 2.54))

        self.assertEqual(inserted_width, expected_width)

        # python-docx's own (unfixed) default would have produced 96/72 = 1.333x
        # this width instead - assert we are NOT that value.
        python_docx_default_width = int(Cm((200 / 72) * 2.54))
        self.assertNotEqual(inserted_width, python_docx_default_width)


if __name__ == "__main__":
    unittest.main()
