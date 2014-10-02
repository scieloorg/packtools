#coding:utf-8
from __future__ import print_function
import argparse
import pkg_resources

from lxml import etree

import packtools


def main():
    """
    Creates a SciELO PS package based on a given XML file.
    """

    packtools_version = pkg_resources.get_distribution('packtools').version

    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('XML', nargs='+',
                        help='Filesystem path to the XML file.')
    parser.add_argument('--version', action='version', version=packtools_version)

    args = parser.parse_args()

    for xml in args.XML:
        try:
            packer = packtools.XMLPacker(xml)
        except IOError:
            print('Error reading %s. Make sure it is a valid file-path.' % xml)
        except etree.XMLSyntaxError as e:
            print('Error reading %s. Syntax error: %s' % (xml, e))
        else:
            outfile = packer.abs_filepath.replace('.xml', '.zip')
            try:
                packer.pack(outfile)
            except ValueError as e:
                print('Error:', e)
            else:
                print('Created:', outfile)


if __name__ == '__main__':
    main()

