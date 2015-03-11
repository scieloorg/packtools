#coding:utf-8
from __future__ import print_function, unicode_literals
import argparse
import pkg_resources
import logging

from lxml import etree

import packtools


logger = logging.getLogger(__name__)


def main():
    """
    Creates a SciELO PS package based on a given XML file.
    """

    packtools_version = pkg_resources.get_distribution('packtools').version

    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('XML', nargs='+',
                        help='filesystem path to the XML file')
    parser.add_argument('--version', action='version', version=packtools_version)
    parser.add_argument('--loglevel', default='WARNING')
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.loglevel))

    for xml in packtools.utils.flatten(args.XML):
        logger.info('started packing %s' % repr(xml))

        try:
            packer = packtools.XMLPacker(xml)
            logger.debug('XMLPacker repr: %s' % packer)
        except IOError as e:
            logger.debug(e)
            print('Error reading %s. Make sure it is a valid file-path.' % xml)
        except etree.XMLSyntaxError as e:
            logger.debug(e)
            print('Error reading %s. Syntax error: %s' % (xml, e))
        else:
            outfile = packer.abs_filepath.replace('.xml', '.zip')
            try:
                packer.pack(outfile)
            except ValueError as e:
                logger.debug(e)
                print('Error:', e)
            else:
                logger.info('package created at %s' % outfile)
                print('Created:', outfile)

        logger.info('finished packing %s' % xml)


if __name__ == '__main__':
    main()

