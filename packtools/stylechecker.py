# coding: utf-8
from __future__ import print_function, unicode_literals
import os
import argparse
import sys
import pkg_resources
import json
import logging

from lxml import etree
# import pygments if here
try:
    import pygments     # NOQA
    from pygments.lexers import get_lexer_for_mimetype
    from pygments.formatters import TerminalFormatter
except ImportError:
    pygments = False    # NOQA

import packtools
from packtools import exceptions


LOGGER = logging.getLogger(__name__)


EPILOG = """\
Copyright 2013 SciELO <scielo-dev@googlegroups.com>.
Licensed under the terms of the BSD license. Please see LICENSE in the source
code for more information.
"""


ERR_MESSAGE = "Something went wrong while working on {filename}: {details}."


def prettify(jsonobj, colorize=True):
    """ Prettify JSON output.

    On windows, bypass pygments colorization.

    Function copied from Circus process manager:
    https://github.com/circus-tent/circus/blob/master/circus/circusctl.py
    """

    json_str = json.dumps(jsonobj, indent=2, sort_keys=True)
    if colorize and pygments and not sys.platform.startswith('win'):
        LOGGER.info('using pygments to highlight the output')
        try:
            lexer = get_lexer_for_mimetype("application/json")
            return pygments.highlight(json_str, lexer, TerminalFormatter())
        except Exception as e:
            LOGGER.debug(e)
            pass

    return json_str


def get_xmlvalidator(xmlpath, no_network, extra_sch):
    parsed_xml = packtools.XML(xmlpath, no_network=no_network)
    return packtools.XMLValidator.parse(parsed_xml, extra_schematron=extra_sch)


def summarize(validator, assets_basedir=None):

    def _make_err_message(err):
        """ An error message is comprised of the message itself and the
        element sourceline.
        """
        err_msg = {'message': err.message}

        try:
            err_element = err.get_apparent_element(validator.lxml)
        except ValueError:
            LOGGER.info('Could not locate the element name in: %s' % err.message)
            err_element = None

        if err_element is not None:
            err_msg['apparent_line'] = err_element.sourceline
        else:
            err_msg['apparent_line'] = None

        return err_msg


    dtd_is_valid, dtd_errors = validator.validate()
    sps_is_valid, sps_errors = validator.validate_style()

    summary = {
        'dtd_errors': [_make_err_message(err) for err in dtd_errors],
        'sps_errors': [_make_err_message(err) for err in sps_errors],
    }

    if assets_basedir:
        LOGGER.info('looking for assets in %s' % (assets_basedir,))
        summary['assets'] = validator.lookup_assets(assets_basedir)
        LOGGER.info('total assets referenced: %s' % (len(summary['assets']),))

    return summary


@packtools.utils.config_xml_catalog
def _main():

    packtools_version = pkg_resources.get_distribution('packtools').version

    parser = argparse.ArgumentParser(
            description='SciELO PS stylechecker command line utility.',
            epilog=EPILOG)

    mutex_group = parser.add_mutually_exclusive_group()
    mutex_group.add_argument('--annotated', action='store_true',
                             help='reproduces the XML with notes at elements that have errors')
    mutex_group.add_argument('--raw', action='store_true',
                             help='each result is encoded as json, without any formatting, and written to stdout in a single line.')

    parser.add_argument('--nonetwork', action='store_true',
                        help='prevents the retrieval of the DTD through the network')
    parser.add_argument('--assetsdir', default=None,
                        help='lookup, at the given directory, for each asset referenced by the XML. current working directory will be used by default.')
    parser.add_argument('--version', action='version', version=packtools_version)
    parser.add_argument('--loglevel', default='ERROR')
    parser.add_argument('--nocolors', action='store_false',
                        help='prevents the output from being colorized by ANSI escape sequences')
    parser.add_argument('--extrasch', default=None,
                        help='runs an extra validation using an external schematron schema.')
    parser.add_argument('--sysinfo', action='store_true',
                        help='show program\'s installation info and exit.')
    parser.add_argument('XML', nargs='*',
                        help='filesystem path or URL to the XML')
    args = parser.parse_args()

    logging.basicConfig(level=getattr(logging, args.loglevel.upper()))

    if args.sysinfo:
        print(prettify(packtools.get_debug_info(), colorize=args.nocolors))
        sys.exit(0)

    print('Please wait, this may take a while...', file=sys.stderr)

    input_args = args.XML or sys.stdin
    summary_list = []

    for xml in packtools.utils.flatten(input_args):
        LOGGER.info('starting validation of %s' % (xml,))

        try:
            xml_validator = get_xmlvalidator(xml, args.nonetwork, args.extrasch)

        except (etree.XMLSyntaxError, exceptions.XMLDoctypeError,
                exceptions.XMLSPSVersionError) as exc:
            LOGGER.debug(exc)
            print(ERR_MESSAGE.format(filename=xml, details=exc),
                    file=sys.stderr)
            continue

        if args.annotated:
            err_xml = xml_validator.annotate_errors()

            fname, fext = xml.rsplit('.', 1)
            out_fname = '.'.join([fname, 'annotated', fext])

            with open(out_fname, 'wb') as fp:
                fp.write(etree.tostring(err_xml, pretty_print=True,
                            encoding='utf-8', xml_declaration=True))

            print('Annotated XML file:', out_fname)

        else:
            try:
                # remote XML will not lookup for assets
                if xml.startswith(('http:', 'https:')):
                    assets_basedir = None
                else:
                    assets_basedir = args.assetsdir or os.path.dirname(xml)

                summary = summarize(xml_validator, assets_basedir=assets_basedir)
            except TypeError as exc:
                LOGGER.debug(exc)
                LOGGER.warning(
                        'Error validating %s. Skipping. Run with DEBUG for more info.',
                        xml)
                continue

            summary['_xml'] = xml
            summary['is_valid'] = bool(
                    xml_validator.validate()[0] and
                    xml_validator.validate_style()[0])

            if args.raw:
                print(json.dumps(summary, sort_keys=True))
            else:
                summary_list.append(summary)

        LOGGER.info('finished validating %s' % (xml,))

    if summary_list:
        print(prettify(summary_list, colorize=args.nocolors))


def main():
    try:
        _main()
    except KeyboardInterrupt:
        LOGGER.debug('The program is terminating due to SIGTERM.')
        pass


if __name__ == '__main__':
    main()

