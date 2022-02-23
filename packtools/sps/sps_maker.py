from packtools.sps.models import packages, sps_package
from packtools.sps.libs import async_download, reqs
from packtools.sps.utils import file_utils
from packtools.sps import exceptions


FILE_PATHS_REQUIRED_KEYS = ['xml', 'assets', 'renditions']


def get_names_and_packages(path):
    return packages.explore_source(path)

