from packtools.sps.models import packages, sps_package
from packtools.sps.libs import async_download, reqs
from packtools.sps.utils import file_utils
from packtools.sps import exceptions


FILE_PATHS_REQUIRED_KEYS = ['xml', 'assets', 'renditions']


def get_names_and_packages(path):
    return packages.explore_source(path)


def make_package_from_paths(paths, zip_folder=None):
    _check_keys_and_files(paths)

    package_metadata = {}
    xml_sps = _get_xml_sps_from_path(paths['xml'])

    package_metadata['xml'] = _get_xml_uri_and_name(xml_sps, paths['xml'])
    package_metadata['renditions'] = paths['renditions']
    package_metadata['assets'] = paths['assets']

    zip_filename = _get_zip_filename(xml_sps)
    package_metadata['temp-zipfile'] = _zip_files_from_paths(zip_filename, xml_sps, paths, zip_folder)

    return package_metadata

