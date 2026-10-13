"""DOCX -> PDF com LibreOffice em modo headless."""

import os
import pathlib
import shutil
import signal
import subprocess
import tempfile
import zipfile

from docx.oxml.ns import nsmap
from lxml import etree
from packtools.sps.formats.pdf.config.styles import STYLES


class ConversionTimeoutError(RuntimeError):
    """O LibreOffice não terminou a conversão dentro do tempo limite."""


# Uma conversão normal leva poucos segundos; o limite evita travar para
# sempre quando o LibreOffice entra em laço. Ver issue #1377.
DEFAULT_CONVERSION_TIMEOUT = 120


# LibreOffice ignora w:sz/w:rFonts de zonas de matemática OOXML e usa seu
# próprio BaseSize (padrão 12pt), estourando a coluna quando o corpo do
# artigo usa um tamanho menor. O tamanho vem do estilo do corpo do próprio
# DOCX convertido. Ver issue #1385.
_BODY_STYLE_NAME = STYLES["body"]
_MATH_CONFIG_XML = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<oor:items xmlns:oor="http://openoffice.org/2001/registry"'
    ' xmlns:xs="http://www.w3.org/2001/XMLSchema"'
    ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
    '<item oor:path="/org.openoffice.Office.Math/StandardFormat">'
    '<prop oor:name="BaseSize" oor:op="fuse"><value>{size}</value></prop>'
    "</item></oor:items>"
)


def _body_font_size_pt(docx_path):
    """
    Returns the font size, in whole points, of the body text style
    (_BODY_STYLE_NAME) of a DOCX, or None when it can't be read.
    """
    try:
        with zipfile.ZipFile(docx_path) as zf:
            styles_xml = zf.read("word/styles.xml")
        root = etree.fromstring(
            styles_xml, etree.XMLParser(resolve_entities=False, no_network=True)
        )
    except (OSError, KeyError, zipfile.BadZipFile, etree.XMLSyntaxError):
        return None

    half_points = root.xpath(
        "string(//w:style[w:name/@w:val=$name]/w:rPr/w:sz/@w:val)",
        namespaces={"w": nsmap["w"]},
        name=_BODY_STYLE_NAME,
    )
    try:
        return round(int(half_points) / 2) or None
    except ValueError:
        return None


def _create_math_profile(size_pt):
    """
    Creates a private LibreOffice user profile whose only setting is the Math
    BaseSize, and returns its directory. LibreOffice fills in the rest on start.
    """
    profile_dir = tempfile.mkdtemp(prefix="packtools_lo_profile_")
    try:
        user_dir = os.path.join(profile_dir, "user")
        os.makedirs(user_dir)
        with open(
            os.path.join(user_dir, "registrymodifications.xcu"), "w", encoding="utf-8"
        ) as f:
            f.write(_MATH_CONFIG_XML.format(size=size_pt))
    except OSError:
        shutil.rmtree(profile_dir, ignore_errors=True)
        raise
    return profile_dir


def _run_command(command, timeout=None):
    """
    Runs command like subprocess.run(check=True), but on timeout (or any
    interruption, such as Ctrl+C) kills its whole process group before
    re-raising.
    """
    # Grupo próprio: o oosplash lança o soffice.bin, e matar só o primeiro deixa o segundo órfão.
    process = subprocess.Popen(command, start_new_session=True)
    try:
        returncode = process.wait(timeout=timeout)
    except BaseException:
        # Fora do grupo do terminal, o Ctrl+C não chega mais ao LibreOffice.
        _kill_process_group(process)
        raise
    if returncode:
        raise subprocess.CalledProcessError(returncode, command)


def _kill_process_group(process):
    """Mata o grupo de processos do LibreOffice (oosplash + soffice.bin); no Windows, só o processo."""
    try:
        os.killpg(process.pid, signal.SIGKILL)
    except (AttributeError, ProcessLookupError):
        # AttributeError: sem os.killpg (Windows)
        process.kill()
    process.wait()


def _run_conversion(binary, docx_path, output_dir, profile_dir=None, timeout=None):
    """Chama o LibreOffice headless para converter docx_path em PDF dentro de output_dir."""
    command = [binary]
    if profile_dir:
        command.append(f"-env:UserInstallation={pathlib.Path(profile_dir).as_uri()}")
    command += ["--headless", "--convert-to", "pdf", docx_path, "--outdir", output_dir]
    _run_command(command, timeout=timeout)


def convert_docx_to_pdf(
    docx_path, libreoffice_binary=None, timeout=DEFAULT_CONVERSION_TIMEOUT
):
    """
    Converts a DOCX file to PDF format using LibreOffice in headless mode.
    The function runs a subprocess to call LibreOffice, specifying the input DOCX file
    and the output directory for the generated PDF file. Formulas are sized to the
    body text by running LibreOffice with a private profile; if that conversion
    fails, it is retried with the default profile. A conversion that exceeds the
    timeout is not retried. Each conversion runs on a copy of the DOCX in its own
    temporary directory, so lock files and partial output left by a killed
    LibreOffice never touch the destination; the PDF is moved next to the DOCX
    only after a successful conversion.
    Args:
        docx_path (str): The path to the DOCX file to be converted.
        libreoffice_binary (str): The path to the LibreOffice binary. If not provided,
            it is autodetected on PATH (tries "libreoffice", then "soffice").
        timeout (float): Maximum seconds for each LibreOffice run; None waits forever.
    Raises:
        FileNotFoundError: If no LibreOffice binary is found.
        ConversionTimeoutError: If LibreOffice does not finish within timeout.
        RuntimeError: If the PDF file was not created successfully.
    Returns:
        str: The path to the generated PDF file.
    """
    binary = (
        libreoffice_binary or shutil.which("libreoffice") or shutil.which("soffice")
    )
    if not binary:
        raise FileNotFoundError(
            "LibreOffice binary ('libreoffice' or 'soffice') was not found on PATH. "
            "Install LibreOffice, or pass libreoffice_binary (CLI: --libreoffice-binary) "
            "with the path to the executable."
        )

    output_dir = os.path.dirname(docx_path) or "."
    if output_dir != ".":
        os.makedirs(output_dir, exist_ok=True)

    base_name = os.path.basename(docx_path)
    f_name, f_ext = os.path.splitext(base_name)
    pdf_path = os.path.join(output_dir, f"{f_name}.pdf")

    # Diretório exclusivo por execução: travas e arquivos parciais deixados por
    # um LibreOffice morto não alcançam outra conversão com o mesmo nome.
    work_dir = tempfile.mkdtemp(prefix="packtools_lo_convert_")
    profile_dir = None
    try:
        base_size = _body_font_size_pt(docx_path)
        if base_size:
            try:
                profile_dir = _create_math_profile(base_size)
            except OSError:
                profile_dir = None

        work_docx_path = os.path.join(work_dir, base_name)
        shutil.copyfile(docx_path, work_docx_path)
        try:
            try:
                _run_conversion(binary, work_docx_path, work_dir, profile_dir, timeout)
            except subprocess.CalledProcessError:
                if not profile_dir:
                    raise
                _run_conversion(binary, work_docx_path, work_dir, timeout=timeout)
        except subprocess.TimeoutExpired:
            raise ConversionTimeoutError(
                f"LibreOffice did not finish converting {docx_path} within {timeout} seconds"
            ) from None

        work_pdf_path = os.path.join(work_dir, f"{f_name}.pdf")
        if not os.path.exists(work_pdf_path):
            raise RuntimeError(f"PDF file was not created: {pdf_path}")
        shutil.move(work_pdf_path, pdf_path)
    finally:
        shutil.rmtree(work_dir, ignore_errors=True)
        if profile_dir:
            shutil.rmtree(profile_dir, ignore_errors=True)

    return pdf_path
