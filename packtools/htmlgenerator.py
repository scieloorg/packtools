# coding: utf-8
from __future__ import print_function, unicode_literals
import argparse
import sys
import logging
import os

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
    bootstrap_css,
    article_css,
    design_system_static_img_path,
):

    if xslt == "3.0":
        if bootstrap_css and article_css and os.path.isfile(css):
            css = os.path.dirname(css)
        if not design_system_static_img_path:
            design_system_static_img_path = (
                os.path.join(
                    os.path.dirname(os.path.dirname(bootstrap_css)),
                    "img"
                )
            )

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
            bootstrap_css=bootstrap_css,
            article_css=article_css,
            design_system_static_img_path=design_system_static_img_path,
            )
    except ValueError as e:
        raise XMLError('Error reading %s. %s.' % (xmlpath, e))

    return generator


@packtools.utils.config_xml_catalog
def main():

    packtools_version = packtools.pkg_resources_fixer.get_version('packtools')

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
    parser.add_argument('--xslt', default=None,
                        choices=['2.0', '3.0'],
                        help='XSLT Version',
                        )
    parser.add_argument('--css', default=catalogs.HTML_GEN_DEFAULT_CSS_PATH,
                        help='URL or full path of the CSS file to use with generated htmls')
    parser.add_argument('--print_css', default=catalogs.HTML_GEN_DEFAULT_PRINT_CSS_PATH,
                        help='URL or full path of the CSS (media: print) file to use with generated htmls')
    parser.add_argument('--bootstrap_css', default=catalogs.HTML_GEN_BOOTSTRAP_CSS_PATH,
                        help='URL or full path of the CSS file to use with generated htmls')
    parser.add_argument('--article_css', default=catalogs.HTML_GEN_ARTICLE_CSS_PATH,
                        help='URL or full path of the CSS file to use with generated htmls')
    parser.add_argument('--design_system_static_img_path',
                        help='URL or full path of the Design System Images')

    parser.add_argument('--math_js', default='https://cdn.jsdelivr.net/npm/mathjax@3.0.0/es5/tex-mml-svg.js',
                        help='URL Math renderer')
    parser.add_argument('--math_elem_preference', default='mml:math',
                        choices=['text-math', 'mml:math'],
                        help='Math element preference')
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

    if args.xslt:
        xslt_versions = [args.xslt]
    else:
        xslt_versions = ["2.0", "3.0"]
    for xml in packtools.utils.flatten(args.XML):
        LOGGER.info('starting generation of %s' % (xml,))

        for xslt_version in xslt_versions:
            generate_html_files(args, xslt_version, xml)

        LOGGER.info('finished generating %s' % (xml,))


def generate_html_files(config, xslt_version, xml):
    try:
        html_generator = get_htmlgenerator(
            xml, config.nonetwork, config.nochecks,
            config.css, config.print_css, config.js,
            config.math_elem_preference, config.math_js,
            config.permlink, config.url_article_page, config.url_download_ris,
            config.gs_abstract,
            config.output_style,
            xslt_version,
            config.bootstrap_css,
            config.article_css,
            config.design_system_static_img_path,
        )
        LOGGER.debug('HTMLGenerator repr: %s' % repr(html_generator))
    except XMLError as e:
        LOGGER.debug(e)
        LOGGER.warning('Error generating %s. Skipping. Run with DEBUG for more info.', xml)
        return

    try:
        abstract_suffix = config.gs_abstract and '.abstract' or ''
        version = xslt_version.replace(".", "_")
        for lang, trans_result in html_generator:
            # nome do arquivo a ser criado
            fname, fext = xml.rsplit('.', 1)
            if xslt_version == "2.0":
                name_parts = [fname, lang + abstract_suffix, 'html']
            else:
                name_parts = [fname, lang + abstract_suffix, version, 'html']
            out_fname = '.'.join(name_parts)

            # criação do arquivo
            with open(out_fname, 'wb') as fp:
                fp.write(etree.tostring(trans_result, pretty_print=True,
                                        encoding='utf-8', method='html',
                                        doctype=u"<!DOCTYPE html>"))

            print('Generated HTML file:', out_fname)
    except TypeError as e:
        LOGGER.debug(e)
        LOGGER.warning('Error generating %s. Skipping. Run with DEBUG for more info.', xml)
        return


if __name__ == '__main__':
    main()
