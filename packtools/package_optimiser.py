# coding: utf-8
import os
import argparse
import logging
import sys

import packtools

LOGGER = logging.getLogger(__name__)


@packtools.utils.config_xml_catalog
def main():

    packtools_version = packtools.pkg_resources_fixer.get_version("packtools")

    parser = argparse.ArgumentParser(description="WEB Images generator CLI utility")
    parser.add_argument("SPPackage", help="SP Package Zip file path.")
    parser.add_argument(
        "New_SPPackage", nargs="?", default='', help="Optimised SP Package Zip file path."
    )
    parser.add_argument(
        '--preservefiles',
        action='store_true',
        help='preserve extracted and optimised files in aux directory',
    )
    parser.add_argument(
        '--stopiferror',
        action='store_true',
        help='stop execution if an error occurs',
    )
    parser.add_argument("--version", action="version", version=packtools_version)
    parser.add_argument("--loglevel", default="WARNING")
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.loglevel.upper()))

    print("Please wait, this may take a while...", file=sys.stderr)

    if len(args.New_SPPackage) > 0:
        new_package_file_path = args.New_SPPackage
    else:
        new_package_file_path = os.path.splitext(args.SPPackage)[0] + "_optimised.zip"

    package = packtools.SPPackage.from_file(
        args.SPPackage,
        os.path.splitext(args.SPPackage)[0],
        stop_if_error=args.stopiferror,
    )
    package.optimise(
        new_package_file_path=new_package_file_path, preserve_files=args.preservefiles
    )


if __name__ == "__main__":
    main()
