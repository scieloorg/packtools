# coding: utf-8
from __future__ import print_function, unicode_literals
import os
import argparse
import sys
import pkg_resources
import logging

from lxml import etree

import packtools


LOGGER = logging.getLogger(__name__)
HERE = os.path.dirname(os.path.abspath(__file__))

DEFAULT_CSS_PATH = os.path.join(HERE, 'catalogs/htmlgenerator/static/scielo-article.css')
DEFAULT_PRINT_CSS_PATH = os.path.join(HERE, 'catalogs/htmlgenerator/static/scielo-print.css')
DEFAULT_JS_PATH = os.path.join(HERE, 'catalogs/htmlgenerator/static/scielo-article.js')


class XMLError(Exception):
    """ Represents errors that would block HTMLGenerator instance from
    being created.
    """


def get_htmlgenerator(xmlpath, no_network, no_checks, css, print_css, js):
    try:
        parsed_xml = packtools.XML(xmlpath, no_network=no_network)
    except IOError as e:
        raise XMLError('Error reading %s. Make sure it is a valid file-path or URL.' % xmlpath)
    except etree.XMLSyntaxError as e:
        raise XMLError('Error reading %s. Syntax error: %s' % (xmlpath, e))

    try:
        valid_only = not no_checks
        generator = packtools.HTMLGenerator.parse(
            parsed_xml, valid_only=valid_only, css=css,
            print_css=print_css, js=js)
    except ValueError as e:
        raise XMLError('Error reading %s. %s.' % (xmlpath, e))

    return generator


@packtools.utils.config_xml_catalog
def main():

    packtools_version = pkg_resources.get_distribution('packtools').version

    parser = argparse.ArgumentParser(description='HTML generator cli utility')
    parser.add_argument('--nonetwork', action='store_true',
                        help='prevents the retrieval of the DTD through the network')
    parser.add_argument('--nochecks', action='store_true',
                        help='prevents the validation against SciELO PS spec')
    parser.add_argument('--css', default=DEFAULT_CSS_PATH,
                        help='URL or full path of the CSS file to use with generated htmls')
    parser.add_argument('--print_css', default=DEFAULT_PRINT_CSS_PATH,
                        help='URL or full path of the CSS (media: print) file to use with generated htmls')
    parser.add_argument('--js', default=DEFAULT_JS_PATH,
                        help='URL or full path of the JS file to use with generated htmls')
    parser.add_argument('XML', nargs='+',
                        help='filesystem path or URL to the XML')
    parser.add_argument('--version', action='version', version=packtools_version)
    parser.add_argument('--loglevel', default='WARNING')
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.loglevel.upper()))

    print('Please wait, this may take a while...', file=sys.stderr)

    for xml in packtools.utils.flatten(args.XML):
        LOGGER.info('starting generation of %s' % (xml,))

        try:
            html_generator = get_htmlgenerator(
                xml, args.nonetwork, args.nochecks,
                args.css, args.print_css, args.js)
            LOGGER.debug('HTMLGenerator repr: %s' % repr(html_generator))
        except XMLError as e:
            LOGGER.debug(e)
            LOGGER.warning('Error generating %s. Skipping. Run with DEBUG for more info.', xml)
            continue

        try:
            for lang, trans_result in html_generator:
                fname, fext = xml.rsplit('.', 1)
                out_fname = '.'.join([fname, lang, 'html'])

                with open(out_fname, 'wb') as fp:
                    fp.write(etree.tostring(trans_result, pretty_print=True,
                                            encoding='utf-8', method='html',
                                            doctype=u"<!DOCTYPE html>"))

                print('Generated HTML file:', out_fname)
        except TypeError as e:
            LOGGER.debug(e)
            LOGGER.warning('Error generating %s. Skipping. Run with DEBUG for more info.', xml)
            continue

        LOGGER.info('finished generating %s' % (xml,))


if __name__ == '__main__':
    main()
