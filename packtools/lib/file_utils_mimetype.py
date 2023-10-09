import os
import mimetypes


def is_valid_file(file_path, check_mimetype=False):
    if os.path.exists(file_path):
        if check_mimetype:
            if get_mimetype(file_path) not in ('text/plain', 'application/xml'):
                return False

        return True

    return False


def get_mimetype(file_path):
    return mimetypes.guess_type(file_path, strict=True)
