import os
import pathlib
import shutil
import subprocess
import tempfile
import zipfile

from docx.oxml.ns import nsmap
from lxml import etree


class DirectoryRemovalError(Exception):
    ...


# LibreOffice ignora w:sz/w:rFonts de zonas de matemática OOXML e usa seu
# próprio BaseSize (padrão 12pt), estourando a coluna quando o corpo do
# artigo usa um tamanho menor. O tamanho vem do estilo do corpo do próprio
# DOCX convertido. Ver issue #1385.
_BODY_STYLE_NAME = "SCL Paragraph"
_MATH_CONFIG_XML = (
    '<?xml version="1.0" encoding="UTF-8"?>'
    '<oor:items xmlns:oor="http://openoffice.org/2001/registry"'
    ' xmlns:xs="http://www.w3.org/2001/XMLSchema"'
    ' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">'
    '<item oor:path="/org.openoffice.Office.Math/StandardFormat">'
    '<prop oor:name="BaseSize" oor:op="fuse"><value>{size}</value></prop>'
    '</item></oor:items>'
)


def _body_font_size_pt(docx_path):
    """
    Returns the font size, in whole points, of the body text style
    (_BODY_STYLE_NAME) of a DOCX, or None when it can't be read.
    """
    try:
        with zipfile.ZipFile(docx_path) as zf:
            styles_xml = zf.read("word/styles.xml")
        root = etree.fromstring(styles_xml, etree.XMLParser(resolve_entities=False, no_network=True))
    except (OSError, KeyError, zipfile.BadZipFile, etree.XMLSyntaxError):
        return None

    half_points = root.xpath(
        "string(//w:style[w:name/@w:val=$name]/w:rPr/w:sz/@w:val)",
        namespaces={"w": nsmap["w"]}, name=_BODY_STYLE_NAME,
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
        with open(os.path.join(user_dir, "registrymodifications.xcu"), "w", encoding="utf-8") as f:
            f.write(_MATH_CONFIG_XML.format(size=size_pt))
    except OSError:
        shutil.rmtree(profile_dir, ignore_errors=True)
        raise
    return profile_dir


def _run_conversion(binary, docx_path, output_dir, profile_dir=None):
    command = [binary]
    if profile_dir:
        command.append(f"-env:UserInstallation={pathlib.Path(profile_dir).as_uri()}")
    command += ["--headless", "--convert-to", "pdf", docx_path, "--outdir", output_dir]
    subprocess.run(command, check=True)


def convert_docx_to_pdf(docx_path, libreoffice_binary=None):
    """
    Converts a DOCX file to PDF format using LibreOffice in headless mode.
    The function runs a subprocess to call LibreOffice, specifying the input DOCX file
    and the output directory for the generated PDF file. Formulas are sized to the
    body text by running LibreOffice with a private profile; if that conversion
    fails, it is retried with the default profile.
    Args:
        docx_path (str): The path to the DOCX file to be converted.
        libreoffice_binary (str): The path to the LibreOffice binary. If not provided,
            it is autodetected on PATH (tries "libreoffice", then "soffice").
    Raises:
        FileNotFoundError: If no LibreOffice binary is found.
        RuntimeError: If the PDF file was not created successfully.
    Returns:
        str: The path to the generated PDF file.
    """
    binary = libreoffice_binary or shutil.which("libreoffice") or shutil.which("soffice")
    if not binary:
        raise FileNotFoundError(
            "LibreOffice binary ('libreoffice' or 'soffice') was not found on PATH. "
            "Install LibreOffice, or pass libreoffice_binary (CLI: --libreoffice-binary) "
            "with the path to the executable."
        )

    output_dir = os.path.dirname(docx_path) or "."
    if output_dir != ".":
        os.makedirs(output_dir, exist_ok=True)

    profile_dir = None
    base_size = _body_font_size_pt(docx_path)
    if base_size:
        try:
            profile_dir = _create_math_profile(base_size)
        except OSError:
            profile_dir = None

    try:
        try:
            _run_conversion(binary, docx_path, output_dir, profile_dir)
        except subprocess.CalledProcessError:
            if not profile_dir:
                raise
            _run_conversion(binary, docx_path, output_dir)
    finally:
        if profile_dir:
            shutil.rmtree(profile_dir, ignore_errors=True)

    base_name = os.path.basename(docx_path)
    f_name, f_ext = os.path.splitext(base_name)
    pdf_path = os.path.join(output_dir, f"{f_name}.pdf")

    if not os.path.exists(pdf_path):
        raise RuntimeError(f"PDF file was not created: {pdf_path}")

    return pdf_path

def unzip_docx(path, prefix="scl_xml2pdf"):
    """
    Extracts contents of a DOCX file into a temporary directory. 
    Creates a new temporary directory with the specified prefix, extracts all files from the DOCX archive into it, 
    and returns the path to the temporary directory containing the extracted files.

    Args:
        path (str): The path to the DOCX file to extract.
        prefix (str): The prefix to use for the temporary directory.

    Returns:
        str: The path to the temporary directory containing the extracted files
    """
    temp_docx_source_dir = tempfile.mkdtemp(prefix=prefix)

    with zipfile.ZipFile(path, 'r') as zf:
        zf.extractall(temp_docx_source_dir)

    return temp_docx_source_dir

def embed_docx(source_dir, prefix="scl_xml2pdf", suffix=".docx"):
    """
    Creates a DOCX file by compressing all files from the source directory into a ZIP archive with .docx extension. 
    After successful compression, removes the source directory and returns the path to the newly created DOCX file.

    Args:
        source_dir (str): The path to the directory containing the files to compress.
        prefix (str): The prefix to use for the temporary DOCX file.
        suffix (str): The suffix to use for the temporary DOCX file.

    Returns:
        str: The path to the newly created DOCX file.
    """
    temp_docx_path = tempfile.mktemp(prefix=prefix, suffix=suffix)
    with zipfile.ZipFile(temp_docx_path, 'w') as zf:
        for root, _, files in os.walk(source_dir):
            for f in files:
                fpath_absolute = os.path.join(root, f)
                fpath_rel = os.path.relpath(fpath_absolute, source_dir)
                zf.write(fpath_absolute, arcname=fpath_rel)
    
    try:
        shutil.rmtree(source_dir)
    except OSError:
        raise DirectoryRemovalError(f'Unable to delete temporary directory: {source_dir}')
    return temp_docx_path

def resolve_asset_path(href, assets_dir=None):
    """
    Resolve a resource path given a href-like string and an optional assets directory.

    Behavior:
    - If href is http(s), return as-is.
    - If href is an absolute filesystem path, return as-is.
    - If assets_dir is provided and contains the relative file, return the joined path.
    - Otherwise return the href unchanged (caller may handle it later).
    """
    if not href:
        return None
    
    href = str(href)
    if href.startswith('http://') or href.startswith('https://'):
        return href

    if os.path.isabs(href):
        return href

    if assets_dir:
        candidate = os.path.join(assets_dir, href)
        if os.path.exists(candidate):
            return candidate

    return href
