import os
import shutil
import tempfile
import unittest
from unittest.mock import patch

from packtools.sps.formats.pdf.utils import file_utils
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
        with self.assertRaises(FileNotFoundError):
            convert_docx_to_pdf(self.docx_path, libreoffice_binary=None)
        mock_run.assert_not_called()


class TestConvertDocxToPdfRelativeOutputPath(unittest.TestCase):
    """
    Regression test for issue #773: os.path.dirname("doc.docx") is "" when
    docx_path has no directory component (e.g. CLI -o doc.pdf), and
    os.makedirs("") raises FileNotFoundError.
    """

    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self._cwd = os.getcwd()
        os.chdir(self.tmpdir.name)
        self.addCleanup(os.chdir, self._cwd)

        self.docx_path = "doc.docx"
        with open(self.docx_path, "wb") as f:
            f.write(b"")
        self.pdf_path = "doc.pdf"

    def _touch_pdf(self, *args, **kwargs):
        with open(self.pdf_path, "wb") as f:
            f.write(b"")

    @patch("packtools.sps.formats.pdf.utils.file_utils.subprocess.run")
    def test_docx_path_without_directory_component_does_not_raise(self, mock_run):
        mock_run.side_effect = self._touch_pdf
        result = convert_docx_to_pdf(self.docx_path, libreoffice_binary="/usr/bin/soffice")
        self.assertEqual(os.path.normpath(result), self.pdf_path)


class TestPatchBaseSize(unittest.TestCase):
    """
    LibreOffice ignores w:sz/w:rFonts on OOXML formula runs and renders every
    <m:oMath> at its own internal BaseSize (12pt by default), overflowing the
    column when the body text is smaller (8pt). See issue #1385.
    """

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmpdir, ignore_errors=True)
        self.registry_path = os.path.join(self.tmpdir, "registrymodifications.xcu")
        with open(self.registry_path, "w", encoding="utf-8") as f:
            f.write('<?xml version="1.0"?><oor:items xmlns:oor="x"></oor:items>')

    def test_adds_base_size_item_when_missing(self):
        file_utils._patch_base_size(self.registry_path, 8)

        with open(self.registry_path, encoding="utf-8") as f:
            content = f.read()
        self.assertIn("<value>8</value>", content)
        self.assertEqual(content.count("BaseSize"), 1)

    def test_is_idempotent(self):
        file_utils._patch_base_size(self.registry_path, 8)
        file_utils._patch_base_size(self.registry_path, 8)

        with open(self.registry_path, encoding="utf-8") as f:
            content = f.read()
        self.assertEqual(content.count("BaseSize"), 1)


class TestProfileEnvArg(unittest.TestCase):
    """
    _profile_env_arg is best-effort: any failure (missing binary support,
    permissions, a mocked subprocess.run in tests that never creates real
    profile files, ...) must fall back to (None, None) instead of raising,
    so a cosmetic formula-sizing fix never breaks PDF generation.
    """

    @patch("packtools.sps.formats.pdf.utils.file_utils._ensure_seed_profile", side_effect=OSError("boom"))
    def test_returns_none_on_failure(self, mock_ensure):
        env_arg, profile_dir = file_utils._profile_env_arg("/usr/bin/soffice")
        self.assertIsNone(env_arg)
        self.assertIsNone(profile_dir)

    def test_returns_env_arg_pointing_to_a_private_copy_of_the_seed_profile(self):
        seed_dir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, seed_dir, ignore_errors=True)
        with open(os.path.join(seed_dir, "marker"), "w") as f:
            f.write("seed")

        with patch("packtools.sps.formats.pdf.utils.file_utils._ensure_seed_profile", return_value=seed_dir):
            env_arg, call_profile_dir = file_utils._profile_env_arg("/usr/bin/soffice")
        self.addCleanup(shutil.rmtree, call_profile_dir, ignore_errors=True)

        self.assertEqual(env_arg, f"-env:UserInstallation=file://{call_profile_dir}")
        self.assertNotEqual(call_profile_dir, seed_dir)
        self.assertTrue(os.path.exists(os.path.join(call_profile_dir, "marker")))


class TestConvertDocxToPdfProfileInjection(unittest.TestCase):
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
    @patch("packtools.sps.formats.pdf.utils.file_utils._profile_env_arg")
    def test_env_arg_is_inserted_right_after_binary_and_profile_dir_is_cleaned_up(
        self, mock_profile_env_arg, mock_run
    ):
        call_profile_dir = tempfile.mkdtemp()
        mock_profile_env_arg.return_value = (
            f"-env:UserInstallation=file://{call_profile_dir}", call_profile_dir
        )
        mock_run.side_effect = self._touch_pdf

        convert_docx_to_pdf(self.docx_path, libreoffice_binary="/usr/bin/soffice")

        command = mock_run.call_args[0][0]
        self.assertEqual(command[0], "/usr/bin/soffice")
        self.assertEqual(command[1], f"-env:UserInstallation=file://{call_profile_dir}")
        self.assertFalse(os.path.isdir(call_profile_dir))

    @patch("packtools.sps.formats.pdf.utils.file_utils.subprocess.run")
    @patch("packtools.sps.formats.pdf.utils.file_utils._profile_env_arg", return_value=(None, None))
    def test_no_env_arg_when_profile_setup_fails(self, mock_profile_env_arg, mock_run):
        mock_run.side_effect = self._touch_pdf

        convert_docx_to_pdf(self.docx_path, libreoffice_binary="/usr/bin/soffice")

        command = mock_run.call_args[0][0]
        self.assertEqual(
            command,
            ["/usr/bin/soffice", "--headless", "--convert-to", "pdf", self.docx_path, "--outdir", self.tmpdir.name],
        )


if __name__ == "__main__":
    unittest.main()
