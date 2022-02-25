import argparse
import logging

from packtools import file_utils
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
        'renditions': renditions_uris or [],
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


def main():
    parser = argparse.ArgumentParser(description="Article package maker CLI utility")
    parser.add_argument('--output_dir', default='.', help='Output directory where the package will be generated')
    parser.add_argument("--loglevel", default="WARNING")

    subparsers = parser.add_subparsers(title='Commands', dest='command')

    uris_parser = subparsers.add_parser('uris', help='Make package from URIs')
    uris_parser.add_argument('--xml', help='XML URI')
    uris_parser.add_argument('--renditions', default=[], nargs='+', help='Renditions URI')

    paths_parser = subparsers.add_parser('paths', help='Make package from files paths')
    paths_parser.add_argument('--xml', help='XML file path', required=True)
    paths_parser.add_argument('--renditions', default=[], nargs='+', help='Renditions file path')
    paths_parser.add_argument('--assets', default=[], nargs='+', help='Assets file path')

    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.loglevel.upper()))

    if args.command == 'uris':
        uris_dict = generate_uris_dict(args.xml, args.renditions)
        sps_maker.make_package_from_uris(
            uris_dict['xml'],
            uris_dict['renditions'],
            args.output_dir,
        )

    elif args.command == 'paths':
        paths_dict = generate_paths_dict(args.xml, args.assets, args.renditions)
        sps_maker.make_package_from_paths(
            paths_dict,
            args.output_dir,
        )

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
