from zipfile import ZipFile

import os


def get_files_list(file_path):
    with ZipFile(file_path, 'r') as zip_content:
        return zip_content.namelist()


def get_files_list_filtered(file_path, extensions):
    files = get_files_list(file_path)
    if not isinstance(extensions, list) or len(extensions) == 0:
        return files
    else:
        for f in files.copy():
            basename = os.path.basename(f)
            _, ext = os.path.splitext(basename)
            if ext not in extensions:
                files.remove(f)
        return files


def get_file_content_from_zip(file_name, zip_path):
    with ZipFile(zip_path, 'r') as zip_content:
        return zip_content.read(file_name)
