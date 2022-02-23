import os
import shutil
import logging
import tempfile
import re
from datetime import datetime
from zipfile import ZipFile

logger = logging.getLogger(__name__)


def is_folder(source):
    return os.path.isdir(source)


def is_zipfile(source):
    return os.path.isfile(source) and source.endswith(".zip")


def xml_files_list(path):
    """
    Return the XML files found in `path`
    """
    return (f for f in os.listdir(path) if f.endswith(".xml"))


def files_list(path):
    """
    Return the files in `path`
    """
    return os.listdir(path)


def read_file(path, encoding="utf-8", mode="r"):
    with open(path, mode=mode, encoding=encoding) as f:
        text = f.read()
    return text


def read_from_zipfile(zip_path, filename):
    with ZipFile(zip_path) as zf:
        return zf.read(filename)


def xml_files_list_from_zipfile(zip_path):
    with ZipFile(zip_path) as zf:
        xmls_filenames = [
            xml_filename
            for xml_filename in zf.namelist()
            if os.path.splitext(xml_filename)[-1] == ".xml"
        ]
    return xmls_filenames


def files_list_from_zipfile(zip_path):
    """
    Return the files in `zip_path`

    Example:

    ```
    [
        '2318-0889-tinf-33-0421/2318-0889-tinf-33-e200069.pdf',
        '2318-0889-tinf-33-0421/2318-0889-tinf-33-e200069.xml',
        '2318-0889-tinf-33-0421/2318-0889-tinf-33-e200071.pdf',
        '2318-0889-tinf-33-0421/2318-0889-tinf-33-e200071.xml',
        '2318-0889-tinf-33-0421/2318-0889-tinf-33-e200071-gf01.tif',
        '2318-0889-tinf-33-0421/2318-0889-tinf-33-e200071-gf02.tif',
        '2318-0889-tinf-33-0421/2318-0889-tinf-33-e200071-gf03.tif',
        '2318-0889-tinf-33-0421/2318-0889-tinf-33-e200071-gf04.tif',
    ]
    ```
    """
    with ZipFile(zip_path) as zf:
        return zf.namelist()


def write_file(path, source, mode="w"):
    dirname = os.path.dirname(path)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    logger.debug("Gravando arquivo: %s", path)
    if "b" in mode:
        with open(path, mode) as f:
            f.write(source)
        return

    with open(path, mode, encoding="utf-8") as f:
        f.write(source)


def create_zip_file(files, zip_name, zip_folder=None):
    zip_folder = zip_folder or tempfile.mkdtemp()

    zip_path = os.path.join(zip_folder, zip_name)
    with ZipFile(zip_path, 'w') as myzip:
        for f in files:
            myzip.write(f, os.path.basename(f))
    return zip_path


def delete_folder(path):
    try:
        shutil.rmtree(path)
    except:
        pass


def date_now_as_folder_name():
    # >>> datetime.now().isoformat()
    # >>> '2021-08-11T17:54:50.556715'
    return datetime.utcnow().isoformat().replace(":", "")


def create_temp_file(filename, content=None, mode='w'):
    file_path = tempfile.mkdtemp()
    file_path = os.path.join(file_path, filename)
    write_file(file_path, content or '', mode)
    return file_path


def size(file_path):
    return os.path.getsize(file_path)


def get_prefix_by_xml_filename(xml_filename):
    """
    Obtém o prefixo associado a um arquivo xml

    Parameters
    ----------
    xml_filename : str
        Nome de arquivo xml

    Returns
    -------
    str
        Prefixo associado ao arquivo xml
    """
    file, ext = os.path.splitext(xml_filename)
    return file


def get_file_role(file_path, prefix, pdf_langs):
    """
    Obtém o papel/função de um arquivo (xml, renditions ou assets) no contexto de um documento

    Parameters
    ----------
    file_path : str
        Nome de um arquivo
    prefix: str
        Prefixo associado ao arquivo
    pdf_langs: list
        Idiomas dos PDFs do documento

    Returns
    -------
    str
        Papel/função de arquivo (xml, rendition ou assets) no contexto de um documento
    """
    file, ext = os.path.splitext(file_path)

    if ext == '.xml':
        return 'xml'
    elif ext == '.pdf':
        if file == prefix:
            return 'renditions'

        for lang in pdf_langs:
            if file == f'{prefix}-{lang}':
                return 'renditions'
    return 'assets'


def extract_issn_from_zip_uri(zip_uri):
    """
    Extrai código ISSN a partir do endereço de um arquivo zip

    Parameters
    ----------
    zip_uri : str
        Endereço de um arquivo zip

    Returns
    -------
    str
        ISSN
    """
    match = re.search(r'.*/ingress/packages/(\d{4}-\d{4})/.*.zip', zip_uri)
    if match:
        return match.group(1)
