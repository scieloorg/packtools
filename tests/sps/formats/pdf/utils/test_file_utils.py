import os
import shutil
import signal
import subprocess
import tempfile
import time
import unittest
import zipfile
from unittest.mock import patch
from urllib.parse import unquote, urlparse

from docx.oxml.ns import nsmap
from lxml import etree

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

    @patch("packtools.sps.formats.pdf.utils.file_utils._run_command")
    def test_explicit_binary_is_respected(self, mock_run):
        mock_run.side_effect = self._touch_pdf
        convert_docx_to_pdf(self.docx_path, libreoffice_binary="/custom/soffice")
        self.assertEqual(mock_run.call_args[0][0][0], "/custom/soffice")

    @patch("packtools.sps.formats.pdf.utils.file_utils._run_command")
    @patch("packtools.sps.formats.pdf.utils.file_utils.shutil.which")
    def test_autodetects_libreoffice_when_binary_omitted(self, mock_which, mock_run):
        mock_which.side_effect = lambda name: "/usr/bin/libreoffice" if name == "libreoffice" else None
        mock_run.side_effect = self._touch_pdf
        convert_docx_to_pdf(self.docx_path, libreoffice_binary=None)
        self.assertEqual(mock_run.call_args[0][0][0], "/usr/bin/libreoffice")

    @patch("packtools.sps.formats.pdf.utils.file_utils._run_command")
    @patch("packtools.sps.formats.pdf.utils.file_utils.shutil.which")
    def test_falls_back_to_soffice_when_libreoffice_missing(self, mock_which, mock_run):
        mock_which.side_effect = lambda name: "/usr/bin/soffice" if name == "soffice" else None
        mock_run.side_effect = self._touch_pdf
        convert_docx_to_pdf(self.docx_path, libreoffice_binary=None)
        self.assertEqual(mock_run.call_args[0][0][0], "/usr/bin/soffice")

    @patch("packtools.sps.formats.pdf.utils.file_utils._run_command")
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

    @patch("packtools.sps.formats.pdf.utils.file_utils._run_command")
    def test_docx_path_without_directory_component_does_not_raise(self, mock_run):
        mock_run.side_effect = self._touch_pdf
        result = convert_docx_to_pdf(self.docx_path, libreoffice_binary="/usr/bin/soffice")
        self.assertEqual(os.path.normpath(result), self.pdf_path)


def _docx_with_body_size(path, half_points):
    """Minimal DOCX whose "SCL Paragraph" style has the given w:sz (half-points), or none when None."""
    sz = f'<w:sz w:val="{half_points}"/>' if half_points is not None else ""
    styles = (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f'<w:styles xmlns:w="{nsmap["w"]}">'
        '<w:style w:type="paragraph" w:styleId="SCLParagraph"><w:name w:val="SCL Paragraph"/>'
        f'<w:rPr>{sz}</w:rPr></w:style></w:styles>'
    )
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("word/styles.xml", styles)
    return path


class TestBodyFontSizePt(unittest.TestCase):
    """
    LibreOffice ignores w:sz/w:rFonts on OOXML formula runs and renders every
    <m:oMath> at its own internal BaseSize (12pt by default), overflowing the
    column when the body text is smaller. The size to use comes from the body
    style of the converted DOCX itself. See issue #1385.
    """

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.tmpdir, ignore_errors=True)
        self.docx_path = os.path.join(self.tmpdir, "doc.docx")

    def test_reads_size_in_points_from_body_style(self):
        _docx_with_body_size(self.docx_path, 20)
        self.assertEqual(file_utils._body_font_size_pt(self.docx_path), 10)

    def test_reads_size_from_the_real_layout_template(self):
        layout = os.path.join(os.path.dirname(__file__), "..", "..", "..", "..", "fixtures", "pdf", "layout.docx")
        self.assertEqual(file_utils._body_font_size_pt(layout), 8)

    def test_returns_none_when_style_has_no_size(self):
        _docx_with_body_size(self.docx_path, None)
        self.assertIsNone(file_utils._body_font_size_pt(self.docx_path))

    def test_returns_none_when_file_is_missing(self):
        self.assertIsNone(file_utils._body_font_size_pt(self.docx_path))

    def test_returns_none_when_file_is_not_a_docx(self):
        with open(self.docx_path, "wb") as f:
            f.write(b"")
        self.assertIsNone(file_utils._body_font_size_pt(self.docx_path))


class TestCreateMathProfile(unittest.TestCase):
    def test_profile_holds_only_the_math_base_size(self):
        profile_dir = file_utils._create_math_profile(8)
        self.addCleanup(shutil.rmtree, profile_dir, ignore_errors=True)

        registry = os.path.join(profile_dir, "user", "registrymodifications.xcu")
        root = etree.parse(registry).getroot()
        props = root.xpath("//prop[@*[local-name()='name']='BaseSize']/value/text()")
        self.assertEqual(props, ["8"])
        self.assertEqual(os.listdir(profile_dir), ["user"])

    def test_profile_dir_is_removed_when_writing_fails(self):
        created = []
        real_mkdtemp = tempfile.mkdtemp

        def tracking_mkdtemp(*args, **kwargs):
            created.append(real_mkdtemp(*args, **kwargs))
            return created[-1]

        with patch("packtools.sps.formats.pdf.utils.file_utils.tempfile.mkdtemp", side_effect=tracking_mkdtemp), \
                patch("builtins.open", side_effect=OSError("disk full")):
            with self.assertRaises(OSError):
                file_utils._create_math_profile(8)

        self.assertEqual(len(created), 1)
        self.assertFalse(os.path.exists(created[0]))


class TestConvertDocxToPdfProfile(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.docx_path = _docx_with_body_size(os.path.join(self.tmpdir.name, "doc.docx"), 16)
        self.pdf_path = os.path.join(self.tmpdir.name, "doc.pdf")

    def _touch_pdf(self, *args, **kwargs):
        with open(self.pdf_path, "wb") as f:
            f.write(b"")

    @staticmethod
    def _profile_dir_from(command):
        return unquote(urlparse(command[1].split("=", 1)[1]).path)

    @patch("packtools.sps.formats.pdf.utils.file_utils._run_command")
    def test_private_profile_with_body_size_is_used_and_cleaned_up(self, mock_run):
        seen = {}

        def run(command, **kwargs):
            profile_dir = self._profile_dir_from(command)
            with open(os.path.join(profile_dir, "user", "registrymodifications.xcu"), encoding="utf-8") as f:
                seen["registry"] = f.read()
            seen["profile_dir"] = profile_dir
            self._touch_pdf()

        mock_run.side_effect = run

        convert_docx_to_pdf(self.docx_path, libreoffice_binary="/usr/bin/soffice")

        command = mock_run.call_args[0][0]
        self.assertEqual(command[0], "/usr/bin/soffice")
        self.assertTrue(command[1].startswith("-env:UserInstallation=file:///"))
        self.assertIn("<value>8</value>", seen["registry"])
        self.assertFalse(os.path.exists(seen["profile_dir"]))

    @patch("packtools.sps.formats.pdf.utils.file_utils._run_command")
    def test_no_profile_when_body_size_is_unknown(self, mock_run):
        _docx_with_body_size(self.docx_path, None)
        mock_run.side_effect = self._touch_pdf

        convert_docx_to_pdf(self.docx_path, libreoffice_binary="/usr/bin/soffice")

        self.assertEqual(
            mock_run.call_args[0][0],
            ["/usr/bin/soffice", "--headless", "--convert-to", "pdf", self.docx_path, "--outdir", self.tmpdir.name],
        )

    @patch("packtools.sps.formats.pdf.utils.file_utils._create_math_profile", side_effect=OSError("boom"))
    @patch("packtools.sps.formats.pdf.utils.file_utils._run_command")
    def test_conversion_proceeds_without_profile_when_profile_creation_fails(self, mock_run, mock_create):
        mock_run.side_effect = self._touch_pdf

        convert_docx_to_pdf(self.docx_path, libreoffice_binary="/usr/bin/soffice")

        self.assertNotIn("-env:UserInstallation", " ".join(mock_run.call_args[0][0]))

    @patch("packtools.sps.formats.pdf.utils.file_utils._run_command")
    def test_retries_with_default_profile_when_conversion_with_private_profile_fails(self, mock_run):
        profile_dirs = []

        def run(command, **kwargs):
            if "-env:UserInstallation" in command[1]:
                profile_dirs.append(self._profile_dir_from(command))
                raise subprocess.CalledProcessError(1, command)
            self._touch_pdf()

        mock_run.side_effect = run

        result = convert_docx_to_pdf(self.docx_path, libreoffice_binary="/usr/bin/soffice")

        self.assertEqual(result, self.pdf_path)
        self.assertEqual(mock_run.call_count, 2)
        self.assertNotIn("-env:UserInstallation", " ".join(mock_run.call_args[0][0]))
        self.assertFalse(os.path.exists(profile_dirs[0]))

    @patch("packtools.sps.formats.pdf.utils.file_utils._run_command")
    def test_raises_when_conversion_fails_with_and_without_profile(self, mock_run):
        mock_run.side_effect = lambda command, **kwargs: (_ for _ in ()).throw(
            subprocess.CalledProcessError(1, command)
        )

        with self.assertRaises(subprocess.CalledProcessError):
            convert_docx_to_pdf(self.docx_path, libreoffice_binary="/usr/bin/soffice")

        self.assertEqual(mock_run.call_count, 2)

    @patch("packtools.sps.formats.pdf.utils.file_utils._run_command")
    def test_does_not_retry_when_there_was_no_profile(self, mock_run):
        _docx_with_body_size(self.docx_path, None)
        mock_run.side_effect = lambda command, **kwargs: (_ for _ in ()).throw(
            subprocess.CalledProcessError(1, command)
        )

        with self.assertRaises(subprocess.CalledProcessError):
            convert_docx_to_pdf(self.docx_path, libreoffice_binary="/usr/bin/soffice")

        self.assertEqual(mock_run.call_count, 1)


@unittest.skipUnless(hasattr(os, "killpg"), "grupo de processos só em POSIX")
class TestRunCommand(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)

    @staticmethod
    def _is_alive(pid):
        # espera o init recolher o processo morto
        for _ in range(50):
            try:
                os.kill(pid, 0)
            except ProcessLookupError:
                return False
            time.sleep(0.05)
        return True

    def test_timeout_kills_child_processes_too(self):
        # como o oosplash, que lança o soffice.bin e fica esperando
        pid_file = os.path.join(self.tmpdir.name, "child.pid")
        command = ["sh", "-c", f"sleep 60 & echo $! > {pid_file}; wait"]

        with self.assertRaises(subprocess.TimeoutExpired):
            file_utils._run_command(command, timeout=1)

        with open(pid_file) as f:
            child_pid = int(f.read())
        self.assertFalse(self._is_alive(child_pid))

    def test_interruption_kills_process_group(self):
        # em sessão própria, o Ctrl+C do terminal não chega ao LibreOffice
        with patch("packtools.sps.formats.pdf.utils.file_utils.subprocess.Popen") as mock_popen, \
                patch("packtools.sps.formats.pdf.utils.file_utils.os.killpg") as mock_killpg:
            process = mock_popen.return_value
            process.pid = 4321
            process.wait.side_effect = [KeyboardInterrupt, 0]

            with self.assertRaises(KeyboardInterrupt):
                file_utils._run_command(["soffice"], timeout=10)

        mock_killpg.assert_called_once_with(4321, signal.SIGKILL)

    def test_nonzero_exit_raises_called_process_error(self):
        with self.assertRaises(subprocess.CalledProcessError) as ctx:
            file_utils._run_command(["sh", "-c", "exit 3"], timeout=10)
        self.assertEqual(ctx.exception.returncode, 3)


class TestConvertDocxToPdfTimeout(unittest.TestCase):
    def setUp(self):
        self.tmpdir = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmpdir.cleanup)
        self.docx_path = _docx_with_body_size(os.path.join(self.tmpdir.name, "doc.docx"), 16)
        self.lock_path = os.path.join(self.tmpdir.name, ".~lock.doc.pdf#")

    @patch("packtools.sps.formats.pdf.utils.file_utils._run_command")
    def test_default_timeout_is_passed_to_libreoffice_run(self, mock_run):
        mock_run.side_effect = lambda command, **kwargs: open(
            os.path.join(self.tmpdir.name, "doc.pdf"), "wb").close()

        convert_docx_to_pdf(self.docx_path, libreoffice_binary="/usr/bin/soffice")

        self.assertEqual(mock_run.call_args[1]["timeout"], file_utils.DEFAULT_CONVERSION_TIMEOUT)

    @patch("packtools.sps.formats.pdf.utils.file_utils._run_command")
    def test_timeout_raises_without_retry_and_removes_lock_file(self, mock_run):
        profile_dirs = []

        def run(command, **kwargs):
            profile_dirs.append(TestConvertDocxToPdfProfile._profile_dir_from(command))
            open(self.lock_path, "w").close()
            raise subprocess.TimeoutExpired(command, kwargs["timeout"])

        mock_run.side_effect = run

        with self.assertRaises(file_utils.ConversionTimeoutError):
            convert_docx_to_pdf(self.docx_path, libreoffice_binary="/usr/bin/soffice", timeout=5)

        self.assertEqual(mock_run.call_count, 1)
        self.assertFalse(os.path.exists(self.lock_path))
        self.assertFalse(os.path.exists(profile_dirs[0]))

    @patch("packtools.sps.formats.pdf.utils.file_utils._run_command")
    def test_interruption_removes_lock_file_and_propagates(self, mock_run):
        def run(command, **kwargs):
            open(self.lock_path, "w").close()
            raise KeyboardInterrupt

        mock_run.side_effect = run

        with self.assertRaises(KeyboardInterrupt):
            convert_docx_to_pdf(self.docx_path, libreoffice_binary="/usr/bin/soffice")

        self.assertEqual(mock_run.call_count, 1)
        self.assertFalse(os.path.exists(self.lock_path))

    def test_timeout_error_is_a_runtime_error(self):
        # quem já trata RuntimeError continua funcionando
        self.assertTrue(issubclass(file_utils.ConversionTimeoutError, RuntimeError))


if __name__ == "__main__":
    unittest.main()
