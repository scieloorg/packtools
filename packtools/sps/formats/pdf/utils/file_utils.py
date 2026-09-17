import os
import shutil
import subprocess
import tempfile
import zipfile


class DirectoryRemovalError(Exception):
    ...


# LibreOffice ignora w:sz/w:rFonts de zonas de matemática OOXML e usa seu
# próprio BaseSize (padrão 12pt), estourando a coluna quando o corpo do
# artigo (estilo "SCL Paragraph") usa um tamanho menor. Ver issue #1385.
_FORMULA_BASE_SIZE_PT = 8
_BASE_SIZE_ITEM_XML = (
    '<item oor:path="/org.openoffice.Office.Math/StandardFormat">'
    '<prop oor:name="BaseSize" oor:op="fuse"><value>{size}</value></prop>'
    '</item>'
)


def _seed_profile_dir():
    return os.path.join(tempfile.gettempdir(), "packtools_lo_profile_seed")


def _patch_base_size(registry_path, size):
    with open(registry_path, "r", encoding="utf-8") as f:
        content = f.read()

    marker = f'<value>{size}</value></prop></item>'
    if '"BaseSize"' in content and marker in content:
        return

    item = _BASE_SIZE_ITEM_XML.format(size=size)
    content = content.replace("</oor:items>", item + "</oor:items>")
    with open(registry_path, "w", encoding="utf-8") as f:
        f.write(content)


def _ensure_seed_profile(binary):
    """
    Returns a cached LibreOffice user profile with Math BaseSize patched to
    _FORMULA_BASE_SIZE_PT, bootstrapping it on first use.
    """
    profile_dir = _seed_profile_dir()
    registry_path = os.path.join(profile_dir, "user", "registrymodifications.xcu")

    if not os.path.exists(registry_path):
        staging_dir = tempfile.mkdtemp(prefix="packtools_lo_profile_seed_staging_")
        subprocess.run([
            binary, "--headless", "--terminate_after_init",
            f"-env:UserInstallation=file://{staging_dir}",
        ], check=True)
        try:
            os.rename(staging_dir, profile_dir)
        except OSError:
            # perfil já criado por uma chamada concorrente; descarta o nosso
            shutil.rmtree(staging_dir, ignore_errors=True)

    _patch_base_size(registry_path, _FORMULA_BASE_SIZE_PT)
    return profile_dir


def _profile_env_arg(binary):
    """
    Best-effort: returns (env_arg, profile_dir_to_clean_up) for a private,
    per-call copy of the BaseSize-patched profile, or (None, None) if
    anything goes wrong (missing binary support, permissions, mocked
    subprocess in tests, etc.) so callers can fall back to plain conversion.
    """
    try:
        seed_profile = _ensure_seed_profile(binary)
        call_profile_dir = tempfile.mkdtemp(prefix="packtools_lo_profile_")
        shutil.copytree(seed_profile, call_profile_dir, dirs_exist_ok=True)
        return f"-env:UserInstallation=file://{call_profile_dir}", call_profile_dir
    except OSError:
        return None, None


def convert_docx_to_pdf(docx_path, libreoffice_binary=None):
    """
    Converts a DOCX file to PDF format using LibreOffice in headless mode.
    The function runs a subprocess to call LibreOffice, specifying the input DOCX file
    and the output directory for the generated PDF file.
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

    env_arg, call_profile_dir = _profile_env_arg(binary)
    command = [binary]
    if env_arg:
        command.append(env_arg)
    command += ['--headless', '--convert-to', 'pdf', docx_path, '--outdir', output_dir]

    try:
        subprocess.run(command, check=True)
    finally:
        if call_profile_dir:
            shutil.rmtree(call_profile_dir, ignore_errors=True)

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
