import os
import tempfile
import unittest

from docx import Document
from PIL import Image

from packtools.sps.formats.pdf.renderer.docx.figure import decide_figure_layout
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


if __name__ == "__main__":
    unittest.main()
