# coding: utf-8
from __future__ import print_function, unicode_literals
import argparse
import sys
import pkg_resources
import logging

from lxml import etree

import packtools
from packtools import catalogs

LOGGER = logging.getLogger(__name__)


class XMLError(Exception):
    """ Represents errors that would block HTMLGenerator instance from
    being created.
    """


def get_htmlgenerator(
    xmlpath, no_network, no_checks, css, print_css, js,
    math_elem_preference, math_js,
    permlink,
    url_article_page, url_download_ris,
    gs_abstract,
    output_style,
    xslt,
):
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
            print_css=print_css, js=js,
            math_elem_preference=math_elem_preference, math_js=math_js,
            permlink=permlink,
            url_article_page=url_article_page,
            url_download_ris=url_download_ris,
            gs_abstract=gs_abstract,
            output_style=output_style,
            xslt=xslt,
            )
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
    parser.add_argument('--gs_abstract', default=False,
                        action='store_true',
                        help='Abstract for Google Scholar')
    parser.add_argument('--output_style', default='',
                        help='Output styles: website or html')
    parser.add_argument('--xslt', default='3.0',
                        choices=['2.0', '3.0'],
                        help='XSLT Version',
                        )
    parser.add_argument('--css', default=catalogs.HTML_GEN_DEFAULT_CSS_PATH,
                        help='URL or full path of the CSS file to use with generated htmls')
    parser.add_argument('--math_js', default='https://cdn.jsdelivr.net/npm/mathjax@3.0.0/es5/tex-mml-svg.js',
                        help='URL Math renderer')
    parser.add_argument('--math_elem_preference', default='mml:math',
                        choices=['text-math', 'mml:math'],
                        help='Math element preference')
    parser.add_argument('--print_css', default=catalogs.HTML_GEN_DEFAULT_PRINT_CSS_PATH,
                        help='URL or full path of the CSS (media: print) file to use with generated htmls')
    parser.add_argument('--js', default=catalogs.HTML_GEN_DEFAULT_JS_PATH,
                        help='URL or full path of the JS file to use with generated htmls')
    parser.add_argument('--permlink', default='',
                        help='Permanente URL to access the article')
    parser.add_argument('--url_article_page', default='',
                        help='OPAC URL to access the article')
    parser.add_argument('--url_download_ris', default='',
                        help='URL to download RIS file (how to cite this article)')
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
                args.css, args.print_css, args.js,
                args.math_elem_preference, args.math_js,
                args.permlink, args.url_article_page, args.url_download_ris,
                args.gs_abstract,
                args.output_style,
                args.xslt,
            )
            LOGGER.debug('HTMLGenerator repr: %s' % repr(html_generator))
        except XMLError as e:
            LOGGER.debug(e)
            LOGGER.warning('Error generating %s. Skipping. Run with DEBUG for more info.', xml)
            continue

        try:
            abstract_suffix = args.gs_abstract and '.abstract' or ''
            for lang, trans_result in html_generator:
                fname, fext = xml.rsplit('.', 1)
                out_fname = '.'.join([fname, lang + abstract_suffix, 'html'])

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
