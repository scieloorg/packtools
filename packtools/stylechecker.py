#coding: utf-8
from __future__ import print_function
import os
import argparse
import sys
import pkg_resources

from lxml import etree

import packtools


PY2 = sys.version_info[0] == 2


def config_xml_catalog(func):
    """Wraps the execution of ``func``, setting-up and tearing-down the
    ``XML_CATALOG_FILES`` environment variable for the current process.
    """
    def wrapper(*args, **kwargs):
        os.environ['XML_CATALOG_FILES'] = packtools.catalogs.XML_CATALOG
        _return = func(*args, **kwargs)
        del(os.environ['XML_CATALOG_FILES'])
        return _return
    return wrapper


@config_xml_catalog
def main():

    packtools_version = pkg_resources.get_distribution('packtools').version

    parser = argparse.ArgumentParser(description='stylechecker cli utility.')
    parser.add_argument('--annotated', action='store_true')
    parser.add_argument('--nonetwork', action='store_true')
    parser.add_argument('xmlpath',
                        help='Filesystem path or URL to the XML file.')
    parser.add_argument('--version', action='version', version=packtools_version)

    args = parser.parse_args()
    try:
        parsed_xml = packtools.XML(args.xmlpath, no_network=args.nonetwork)

    except IOError:
        sys.exit('Error reading %s. Make sure it is a valid file-path or URL.' % args.xmlpath)

    except etree.XMLSyntaxError as e:
        sys.exit('Error reading %s. Syntax error: %s' % (args.xmlpath, e))

    else:
        try:
            xml = packtools.XMLValidator(parsed_xml)

        except ValueError as e:
            sys.exit('Error reading %s. %s.' % (args.xmlpath, e))

    try:
        # validation may raise TypeError when the DTD lookup fails.
        is_valid, errors = xml.validate()
    except TypeError as e:
        sys.exit('Error validating %s. %s.' % (args.xmlpath, e))

    style_is_valid, style_errors = xml.validate_style()

    if args.annotated:
        err_xml = xml.annotate_errors()

        if PY2:
            bin_stdout = sys.stdout
        else:
            bin_stdout = sys.stdout.buffer

        bin_stdout.write(etree.tostring(err_xml, pretty_print=True,
            encoding='utf-8', xml_declaration=True))

    else:
        if not is_valid:
            print('Invalid XML! Found %s errors:' % len(errors))
            for err in errors:
                print('%s,%s\t%s' % (err.line, err.column, err.message))
        else:
            print('Valid XML! ;)')

        if not style_is_valid:
            print('Invalid SPS Style! Found %s errors:' % len(style_errors))
            for err in style_errors:
                print(err.message)
        else:
            print('Valid SPS Style! ;)')


if __name__ == '__main__':
    main()

