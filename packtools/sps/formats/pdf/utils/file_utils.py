import os
import shutil
import subprocess
import tempfile
import zipfile


class DirectoryRemovalError(Exception):
    ...


def convert_docx_to_pdf(docx_path, pdf_path, libreoffice_binary="libreoffice24.2"):
    """
    Convert a DOCX file to PDF using LibreOffice.

    Args:
        docx_path (str): The path to the DOCX file to convert.
        pdf_path (str): The path to the PDF file to create.
        libreoffice_binary (str): The path to the LibreOffice binary to use for conversion.

    Returns:
        str: The path to the created PDF file.
    """
    output_dir = os.path.dirname(pdf_path)
    os.makedirs(output_dir, exist_ok=True)

    subprocess.run([libreoffice_binary, '--headless', '--convert-to', 'pdf', docx_path, '--outdir', output_dir], check=True)
    
    base_name = os.path.basename(docx_path)
    base_name_no_ext = os.path.splitext(base_name)[0]
    temp_pdf_path = os.path.join(output_dir, f"{base_name_no_ext}.pdf")
    os.rename(temp_pdf_path, pdf_path)

    return pdf_path
