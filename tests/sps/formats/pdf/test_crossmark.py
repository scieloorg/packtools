"""
Tests for packtools.sps.formats.pdf.crossmark
"""

import io
import os
import csv
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.pagesizes import A4, letter

from packtools.sps.formats.pdf.crossmark import (
    _compute_logo_rect,
    _get_logo_height,
    _build_xmp_packet,
    _merge_xmp_packet,
    _create_logo_overlay,
    add_crossmark,
    _DEFAULT_LOGO,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _make_simple_pdf(pagesize=letter, num_pages=1):
    """Return a BytesIO containing a minimal PDF with `num_pages` pages."""
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=pagesize)
    for i in range(num_pages):
        c.drawString(72, 500, f"Page {i + 1}")
        if i < num_pages - 1:
            c.showPage()
    c.save()
    buf.seek(0)
    return buf


def _write_temp_pdf(tmp_dir, pagesize=letter, num_pages=1, filename="test.pdf"):
    """Write a minimal PDF to *tmp_dir* and return its path."""
    path = os.path.join(tmp_dir, filename)
    buf = _make_simple_pdf(pagesize=pagesize, num_pages=num_pages)
    with open(path, "wb") as f:
        f.write(buf.read())
    return path


# ---------------------------------------------------------------------------
# Unit tests: _compute_logo_rect
# ---------------------------------------------------------------------------

class TestComputeLogoRect(unittest.TestCase):

    def test_top_right(self):
        x, y = _compute_logo_rect(612, 792, "top-right", 150, 40, margin=20)
        self.assertAlmostEqual(x, 612 - 150 - 20)
        self.assertAlmostEqual(y, 792 - 40 - 20)

    def test_top_left(self):
        x, y = _compute_logo_rect(612, 792, "top-left", 150, 40, margin=20)
        self.assertAlmostEqual(x, 20)
        self.assertAlmostEqual(y, 792 - 40 - 20)

    def test_bottom_right(self):
        x, y = _compute_logo_rect(612, 792, "bottom-right", 150, 40, margin=20)
        self.assertAlmostEqual(x, 612 - 150 - 20)
        self.assertAlmostEqual(y, 20)

    def test_bottom_left(self):
        x, y = _compute_logo_rect(612, 792, "bottom-left", 150, 40, margin=20)
        self.assertAlmostEqual(x, 20)
        self.assertAlmostEqual(y, 20)

    def test_unknown_position_defaults_to_top_right(self):
        x, y = _compute_logo_rect(612, 792, "unknown", 150, 40, margin=20)
        self.assertAlmostEqual(x, 612 - 150 - 20)
        self.assertAlmostEqual(y, 792 - 40 - 20)


# ---------------------------------------------------------------------------
# Unit tests: _get_logo_height
# ---------------------------------------------------------------------------

class TestGetLogoHeight(unittest.TestCase):

    def test_with_default_logo(self):
        h = _get_logo_height(_DEFAULT_LOGO, 200)
        self.assertGreater(h, 0)

    def test_fallback_on_missing_file(self):
        h = _get_logo_height("/nonexistent/logo.png", 200)
        # Fallback: width / 4.0
        self.assertAlmostEqual(h, 50.0)


# ---------------------------------------------------------------------------
# Unit tests: _build_xmp_packet
# ---------------------------------------------------------------------------

class TestBuildXmpPacket(unittest.TestCase):

    def setUp(self):
        self.doi = "10.1590/s0100-12345"
        self.date_stamp = "2026-01-15"
        self.xmp = _build_xmp_packet(self.doi, self.date_stamp).decode("utf-8")

    def test_contains_xpacket_begin(self):
        self.assertIn("<?xpacket begin=", self.xmp)

    def test_contains_xpacket_end(self):
        self.assertIn("<?xpacket end=", self.xmp)

    def test_contains_doi_identifier(self):
        self.assertIn(f"doi:{self.doi}", self.xmp)

    def test_contains_prism_doi(self):
        self.assertIn(f"<prism:doi>{self.doi}</prism:doi>", self.xmp)

    def test_contains_prism_url(self):
        self.assertIn(f"https://doi.org/{self.doi}", self.xmp)

    def test_contains_crossmark_major_version_date(self):
        self.assertIn(
            f"<crossmark:MajorVersionDate>{self.date_stamp}</crossmark:MajorVersionDate>",
            self.xmp,
        )

    def test_contains_crossmark_doi(self):
        self.assertIn(f"<crossmark:DOI>{self.doi}</crossmark:DOI>", self.xmp)

    def test_contains_pdfx_doi(self):
        self.assertIn(f"<pdfx:doi>{self.doi}</pdfx:doi>", self.xmp)

    def test_contains_pdfx_crossmark_date(self):
        self.assertIn(
            f"<pdfx:CrossmarkMajorVersionDate>{self.date_stamp}</pdfx:CrossmarkMajorVersionDate>",
            self.xmp,
        )


# ---------------------------------------------------------------------------
# Unit tests: _merge_xmp_packet
# ---------------------------------------------------------------------------

class TestMergeXmpPacket(unittest.TestCase):

    def test_merge_with_no_existing_returns_fresh_packet(self):
        result = _merge_xmp_packet(None, "10.1234/test", "2026-01-01")
        self.assertIn("10.1234/test", result.decode("utf-8"))

    def test_merge_with_invalid_xml_returns_fresh_packet(self):
        result = _merge_xmp_packet(b"<not valid xml>>>", "10.1234/test", "2026-01-01")
        self.assertIn("10.1234/test", result.decode("utf-8"))

    def test_merge_preserves_existing_fields(self):
        existing = b"""<?xpacket begin='\xef\xbb\xbf' id='W5M0MpCehiHzreSzNTczkc9d'?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about=""
        xmlns:dc="http://purl.org/dc/elements/1.1/">
      <dc:title>My Article</dc:title>
    </rdf:Description>
  </rdf:RDF>
</x:xmpmeta>
<?xpacket end='w'?>"""
        result = _merge_xmp_packet(existing, "10.1590/abc", "2026-02-01")
        text = result.decode("utf-8")
        # Existing field preserved
        self.assertIn("My Article", text)
        # New fields added
        self.assertIn("10.1590/abc", text)

    def test_merge_updates_existing_crossmark_field(self):
        existing = b"""<?xpacket begin='\xef\xbb\xbf' id='W5M0MpCehiHzreSzNTczkc9d'?>
<x:xmpmeta xmlns:x="adobe:ns:meta/">
  <rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">
    <rdf:Description rdf:about=""
        xmlns:crossmark="http://crossref.org/crossmark/1.0/">
      <crossmark:DOI>10.OLD/doi</crossmark:DOI>
    </rdf:Description>
  </rdf:RDF>
</x:xmpmeta>
<?xpacket end='w'?>"""
        result = _merge_xmp_packet(existing, "10.NEW/doi", "2026-01-01")
        text = result.decode("utf-8")
        self.assertIn("10.NEW/doi", text)
        self.assertNotIn("10.OLD/doi", text)


# ---------------------------------------------------------------------------
# Integration tests: add_crossmark
# ---------------------------------------------------------------------------

class TestAddCrossmark(unittest.TestCase):

    DOI = "10.1590/s0100-12345"
    DATE_STAMP = "2026-01-15"

    def test_basic_single_page_pdf(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_pdf = _write_temp_pdf(tmp, filename="input.pdf")
            output_pdf = os.path.join(tmp, "output.pdf")

            add_crossmark(input_pdf, output_pdf, self.DOI, self.DATE_STAMP)

            self.assertTrue(os.path.exists(output_pdf))
            self.assertGreater(os.path.getsize(output_pdf), 0)

    def test_output_has_same_page_count(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_pdf = _write_temp_pdf(tmp, num_pages=3, filename="input.pdf")
            output_pdf = os.path.join(tmp, "output.pdf")

            add_crossmark(input_pdf, output_pdf, self.DOI, self.DATE_STAMP)

            reader = PdfReader(output_pdf)
            self.assertEqual(len(reader.pages), 3)

    def test_output_contains_uri_annotation(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_pdf = _write_temp_pdf(tmp, filename="input.pdf")
            output_pdf = os.path.join(tmp, "output.pdf")

            add_crossmark(input_pdf, output_pdf, self.DOI, self.DATE_STAMP)

            reader = PdfReader(output_pdf)
            first_page = reader.pages[0]
            annots = first_page.get("/Annots")
            self.assertIsNotNone(annots, "No annotations found on first page")

            # Find the URI annotation with crossmark URL
            found_uri = False
            for annot_ref in annots:
                annot = annot_ref.get_object()
                action = annot.get("/A")
                if action:
                    uri = str(action.get("/URI", ""))
                    if uri.startswith("https://crossmark.crossref.org/"):
                        found_uri = True
                        break
            self.assertTrue(found_uri, "Crossmark URI annotation not found")

    def test_crossmark_url_contains_doi(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_pdf = _write_temp_pdf(tmp, filename="input.pdf")
            output_pdf = os.path.join(tmp, "output.pdf")

            add_crossmark(input_pdf, output_pdf, self.DOI, self.DATE_STAMP)

            reader = PdfReader(output_pdf)
            first_page = reader.pages[0]
            annots = first_page.get("/Annots")

            for annot_ref in annots:
                annot = annot_ref.get_object()
                action = annot.get("/A")
                if action:
                    uri = str(action.get("/URI", ""))
                    if uri.startswith("https://crossmark.crossref.org/"):
                        self.assertIn(self.DOI, uri)
                        self.assertIn(self.DATE_STAMP, uri)
                        return

            self.fail("Crossmark URI annotation not found")

    def test_output_contains_xmp_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_pdf = _write_temp_pdf(tmp, filename="input.pdf")
            output_pdf = os.path.join(tmp, "output.pdf")

            add_crossmark(input_pdf, output_pdf, self.DOI, self.DATE_STAMP)

            reader = PdfReader(output_pdf)
            meta_ref = reader.root_object.get("/Metadata")
            self.assertIsNotNone(meta_ref, "XMP metadata stream not found in PDF")

            xmp_text = meta_ref.get_object().get_data().decode("utf-8")
            self.assertIn(self.DOI, xmp_text)
            self.assertIn(self.DATE_STAMP, xmp_text)

    def test_xmp_contains_all_required_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_pdf = _write_temp_pdf(tmp, filename="input.pdf")
            output_pdf = os.path.join(tmp, "output.pdf")

            add_crossmark(input_pdf, output_pdf, self.DOI, self.DATE_STAMP)

            reader = PdfReader(output_pdf)
            xmp_text = (
                reader.root_object["/Metadata"].get_object().get_data().decode("utf-8")
            )

            expected_fragments = [
                f"doi:{self.DOI}",                  # dc:identifier
                f"<prism:doi>{self.DOI}</prism:doi>",
                f"https://doi.org/{self.DOI}",       # prism:url
                f"<crossmark:DOI>{self.DOI}</crossmark:DOI>",
                f"<pdfx:doi>{self.DOI}</pdfx:doi>",
                self.DATE_STAMP,
            ]
            for fragment in expected_fragments:
                self.assertIn(fragment, xmp_text, f"Missing fragment: {fragment}")

    def test_a4_pdf(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_pdf = _write_temp_pdf(tmp, pagesize=A4, filename="a4.pdf")
            output_pdf = os.path.join(tmp, "a4_cm.pdf")

            add_crossmark(input_pdf, output_pdf, self.DOI, self.DATE_STAMP)

            reader = PdfReader(output_pdf)
            self.assertEqual(len(reader.pages), 1)

    def test_position_top_left(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_pdf = _write_temp_pdf(tmp, filename="input.pdf")
            output_pdf = os.path.join(tmp, "output.pdf")

            add_crossmark(
                input_pdf, output_pdf, self.DOI, self.DATE_STAMP, position="top-left"
            )
            self.assertTrue(os.path.exists(output_pdf))

    def test_custom_width(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_pdf = _write_temp_pdf(tmp, filename="input.pdf")
            output_pdf = os.path.join(tmp, "output.pdf")

            add_crossmark(
                input_pdf, output_pdf, self.DOI, self.DATE_STAMP, width=100
            )
            self.assertTrue(os.path.exists(output_pdf))

    def test_missing_input_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(FileNotFoundError):
                add_crossmark(
                    "/nonexistent/input.pdf",
                    os.path.join(tmp, "out.pdf"),
                    self.DOI,
                    self.DATE_STAMP,
                )

    def test_missing_logo_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_pdf = _write_temp_pdf(tmp, filename="input.pdf")
            with self.assertRaises(FileNotFoundError):
                add_crossmark(
                    input_pdf,
                    os.path.join(tmp, "out.pdf"),
                    self.DOI,
                    self.DATE_STAMP,
                    logo_path="/nonexistent/logo.png",
                )

    def test_empty_doi_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_pdf = _write_temp_pdf(tmp, filename="input.pdf")
            with self.assertRaises(ValueError):
                add_crossmark(
                    input_pdf,
                    os.path.join(tmp, "out.pdf"),
                    "",
                    self.DATE_STAMP,
                )

    def test_empty_date_stamp_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_pdf = _write_temp_pdf(tmp, filename="input.pdf")
            with self.assertRaises(ValueError):
                add_crossmark(
                    input_pdf,
                    os.path.join(tmp, "out.pdf"),
                    self.DOI,
                    "",
                )

    def test_output_directory_created_if_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_pdf = _write_temp_pdf(tmp, filename="input.pdf")
            output_pdf = os.path.join(tmp, "subdir", "output.pdf")

            add_crossmark(input_pdf, output_pdf, self.DOI, self.DATE_STAMP)
            self.assertTrue(os.path.exists(output_pdf))


# ---------------------------------------------------------------------------
# CLI tests
# ---------------------------------------------------------------------------

class TestCLIMain(unittest.TestCase):

    DOI = "10.1590/s0100-12345"
    DATE_STAMP = "2026-01-15"

    def test_single_file_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_pdf = _write_temp_pdf(tmp, filename="input.pdf")
            output_pdf = os.path.join(tmp, "output.pdf")

            import sys
            from packtools.sps.formats.pdf.crossmark import main

            with patch.object(
                sys,
                "argv",
                [
                    "crossmark_pdf",
                    "--input", input_pdf,
                    "--output", output_pdf,
                    "--doi", self.DOI,
                    "--date-stamp", self.DATE_STAMP,
                ],
            ):
                main()

            self.assertTrue(os.path.exists(output_pdf))

    def test_single_file_default_output_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            input_pdf = _write_temp_pdf(tmp, filename="article.pdf")
            expected_output = os.path.join(tmp, "article_cm.pdf")

            import sys
            from packtools.sps.formats.pdf.crossmark import main

            with patch.object(
                sys,
                "argv",
                [
                    "crossmark_pdf",
                    "--input", input_pdf,
                    "--doi", self.DOI,
                    "--date-stamp", self.DATE_STAMP,
                ],
            ):
                main()

            self.assertTrue(os.path.exists(expected_output))

    def test_batch_csv_mode(self):
        with tempfile.TemporaryDirectory() as tmp:
            input1 = _write_temp_pdf(tmp, filename="a1.pdf")
            input2 = _write_temp_pdf(tmp, filename="a2.pdf")
            out1 = os.path.join(tmp, "a1_cm.pdf")
            out2 = os.path.join(tmp, "a2_cm.pdf")

            csv_path = os.path.join(tmp, "batch.csv")
            with open(csv_path, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["doi", "input_pdf", "date_stamp", "output_pdf"])
                w.writerow([self.DOI, input1, self.DATE_STAMP, out1])
                w.writerow(["10.1590/other", input2, "2025-06-01", out2])

            import sys
            from packtools.sps.formats.pdf.crossmark import main

            with patch.object(sys, "argv", ["crossmark_pdf", "--csv", csv_path]):
                main()

            self.assertTrue(os.path.exists(out1))
            self.assertTrue(os.path.exists(out2))

    def test_batch_csv_mode_default_output_name(self):
        with tempfile.TemporaryDirectory() as tmp:
            input1 = _write_temp_pdf(tmp, filename="a1.pdf")
            expected_out = os.path.join(tmp, "a1_cm.pdf")

            csv_path = os.path.join(tmp, "batch.csv")
            with open(csv_path, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["doi", "input_pdf", "date_stamp"])
                w.writerow([self.DOI, input1, self.DATE_STAMP])

            import sys
            from packtools.sps.formats.pdf.crossmark import main

            with patch.object(sys, "argv", ["crossmark_pdf", "--csv", csv_path]):
                main()

            self.assertTrue(os.path.exists(expected_out))

    def test_batch_csv_skips_rows_with_missing_fields(self):
        with tempfile.TemporaryDirectory() as tmp:
            csv_path = os.path.join(tmp, "batch.csv")
            with open(csv_path, "w", newline="") as f:
                w = csv.writer(f)
                w.writerow(["doi", "input_pdf", "date_stamp"])
                # Row with missing doi -> should be skipped
                w.writerow(["", os.path.join(tmp, "a1.pdf"), self.DATE_STAMP])

            import sys
            from packtools.sps.formats.pdf.crossmark import main

            # Should not raise
            with patch.object(sys, "argv", ["crossmark_pdf", "--csv", csv_path]):
                main()


if __name__ == "__main__":
    unittest.main()
