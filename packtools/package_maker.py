import argparse
import logging

from packtools.sps.utils import file_utils
from packtools.sps import sps_maker


LOGGER = logging.getLogger(__name__)


def generate_paths_dict(xml_path, assets_paths, renditions_paths):
    return {
        'xml': xml_path or '', 
        'assets': assets_paths or [], 
        'renditions': renditions_paths or [],
    }


def generate_uris_dict(xml_uri, renditions_uris):
    uris_dict = {
        'xml': xml_uri or '', 
        'renditions': [],
    }

    for ru in renditions_uris:
        ru_dict = _get_rendition_dict(ru)
        uris_dict['renditions'].append(ru_dict)

    return uris_dict


def _get_rendition_dict(rendition_uri_or_path):
    return {
        'uri': rendition_uri_or_path,
        'name': file_utils.get_filename(rendition_uri_or_path),
    }
