import os
import shutil
import subprocess
import tempfile
import zipfile


class DirectoryRemovalError(Exception):
    ...


def convert_docx_to_pdf(docx_path, libreoffice_binary="libreoffice"):
    """
    Converts a DOCX file to PDF format using LibreOffice in headless mode.
    The function runs a subprocess to call LibreOffice, specifying the input DOCX file
    and the output directory for the generated PDF file.
    Args:
        docx_path (str): The path to the DOCX file to be converted.
        libreoffice_binary (str): The path to the LibreOffice binary. Defaults to "libreoffice".
    Raises:
        RuntimeError: If the PDF file was not created successfully.
    Returns:
        str: The path to the generated PDF file.
    """

    output_dir = os.path.dirname(docx_path)
    os.makedirs(output_dir, exist_ok=True)

    subprocess.run([
        libreoffice_binary,
        '--headless',
        '--convert-to',
        'pdf',
        docx_path,
        '--outdir',
        output_dir
    ], check=True)

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
