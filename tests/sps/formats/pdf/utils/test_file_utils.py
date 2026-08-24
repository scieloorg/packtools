import os
import tempfile
import unittest
from unittest.mock import patch

from packtools.sps.formats.pdf.utils.file_utils import convert_docx_to_pdf


class TestConvertDocxToPdfBinaryResolution(unittest.TestCase):
    """
    Regression test for a bug where the CLI always passed an explicit
    libreoffice_binary argument (None, when --libreoffice-binary was
    omitted) that shadowed this function's own default, breaking the
    subprocess call with a TypeError instead of converting the file.
    """

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.docx_path = os.path.join(self.tmpdir.name, "doc.docx")
        with open(self.docx_path, "wb") as f:
            f.write(b"")
        self.pdf_path = os.path.join(self.tmpdir.name, "doc.pdf")

    def _touch_pdf(self, *args, **kwargs):
        with open(self.pdf_path, "wb") as f:
            f.write(b"")

    @patch("packtools.sps.formats.pdf.utils.file_utils.subprocess.run")
    def test_explicit_binary_is_respected(self, mock_run):
        mock_run.side_effect = self._touch_pdf
        convert_docx_to_pdf(self.docx_path, libreoffice_binary="/custom/soffice")
        self.assertEqual(mock_run.call_args[0][0][0], "/custom/soffice")

    @patch("packtools.sps.formats.pdf.utils.file_utils.subprocess.run")
    @patch("packtools.sps.formats.pdf.utils.file_utils.shutil.which")
    def test_autodetects_libreoffice_when_binary_omitted(self, mock_which, mock_run):
        mock_which.side_effect = lambda name: "/usr/bin/libreoffice" if name == "libreoffice" else None
        mock_run.side_effect = self._touch_pdf
        convert_docx_to_pdf(self.docx_path, libreoffice_binary=None)
        self.assertEqual(mock_run.call_args[0][0][0], "/usr/bin/libreoffice")

    @patch("packtools.sps.formats.pdf.utils.file_utils.subprocess.run")
    @patch("packtools.sps.formats.pdf.utils.file_utils.shutil.which")
    def test_falls_back_to_soffice_when_libreoffice_missing(self, mock_which, mock_run):
        mock_which.side_effect = lambda name: "/usr/bin/soffice" if name == "soffice" else None
        mock_run.side_effect = self._touch_pdf
        convert_docx_to_pdf(self.docx_path, libreoffice_binary=None)
        self.assertEqual(mock_run.call_args[0][0][0], "/usr/bin/soffice")

    @patch("packtools.sps.formats.pdf.utils.file_utils.subprocess.run")
    @patch("packtools.sps.formats.pdf.utils.file_utils.shutil.which", return_value=None)
    def test_raises_clear_error_when_no_binary_found(self, mock_which, mock_run):
        with self.assertRaises(RuntimeError):
            convert_docx_to_pdf(self.docx_path, libreoffice_binary=None)
        mock_run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
