# coding: utf-8
from __future__ import print_function, unicode_literals
import os
import argparse
import sys
import pkg_resources
import json
import logging
import pathlib

from lxml import etree

import packtools
from packtools import exceptions
from packtools import catalogs

__all__ = ['summarize', 'annotate']


LOGGER = logging.getLogger(__name__)


LOGGER_FMT = '%(asctime)s [%(levelname)s] %(name)s: %(message)s'


EPILOG = """\
Copyright 2013 SciELO <scielo-dev@googlegroups.com>.
Licensed under the terms of the BSD license. Please see LICENSE in the source
code for more information.
"""


ERR_MESSAGE = "Something went wrong while working on {filename}: {details}."


AVAILABLE_SCHEMAS = ', '.join(sorted(['@'+key 
    for key in catalogs.SCH_SCHEMAS.keys()]))


def get_xmlvalidator(xmlpath, no_network, extra_sch):
    """ Get an instance of ``packtools.XMLValidator``.

    :param xmlpath: filesystem or URL to an XML file.
    :param no_network: if the parser might retrieve the DTD from the internet.
    :param extra_sch: list of paths to schematron schemas.
    """ 
    parsed_xml = packtools.XML(xmlpath, no_network=no_network)
    _extra_sch = list(extra_sch)
    if _extra_sch:
        paths = [packtools.utils.resolve_schematron_filepath(path_or_ref)
                 for path_or_ref in _extra_sch]
        schemas = [packtools.utils.get_schematron_from_filepath(path)
                   for path in paths]
        labeled_schemas = zip(schemas, _extra_sch)
    else:
        labeled_schemas = None

    return packtools.XMLValidator.parse(parsed_xml, 
            extra_sch_schemas=labeled_schemas)


def annotate(validator, buff, encoding=None):
    _encoding = encoding or validator.encoding
    err_xml = validator.annotate_errors()

    buff.write(etree.tostring(err_xml, pretty_print=True,
        encoding=_encoding, xml_declaration=True))


def summarize(validator, assets_basedir=None):
    """Produce a summarized result of the validation.
    """
    def _make_err_message(err):
        """ An error message is comprised of the message itself and the
        element sourceline.
        """
        err_msg = {'message': err.message}

        try:
            err_element = err.get_apparent_element(validator.lxml)
        except ValueError:
            LOGGER.info('could not find the element name in message')
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
        'style_errors': {},
        'is_valid': bool(dtd_is_valid and sps_is_valid),
    }

    for sps_error in sps_errors:
        err_group = summary['style_errors'].setdefault(sps_error.label, [])
        err_group.append(_make_err_message(sps_error))

    if assets_basedir:
        LOGGER.info('starting to look for assets')
        summary['assets'] = validator.lookup_assets(assets_basedir)
        LOGGER.info('total assets referenced: %s', len(summary['assets']))

    return summary


def _make_relative_to_base(base, paths):
    for path in paths:
        # pure paths don't access the filesystem
        posix_path = pathlib.PurePosixPath(path)
        try:
            relative_path = posix_path.relative_to(base)
        except ValueError:
            continue

        yield str(relative_path)


def validate_zip_package(filepath):
    """Validates all documents in a zip package.

    Returns a generator object that produces validation reports for each
    XML document. Validation reports are represented as 5-tuples in the form:
    (<filename>, <is_valid>, <validation_errors>, <exc_type>, <exc_value>)
    """
    with packtools.utils.Xray.fromfile(filepath) as xpack:
        xmls = xpack.show_sorted_members().get('xml', [])

        for xml in xmls:
            # useful for looking-up files relative to the xml file
            xml_dirname = os.path.dirname(xml)

            with xpack.get_file(xml) as file:
                try:
                    validator = packtools.XMLValidator.parse(file)

                except exceptions.PacktoolsError as exc:
                    exc_type = type(exc).__name__
                    exc_value = str(exc)
                    summary = None

                else:
                    exc_type = None
                    exc_value = None

                    paths = _make_relative_to_base(xml_dirname,
                            xpack.show_members())
                    summary = summarize(validator, paths)

            yield (xml, summary, exc_type, exc_value)


@packtools.utils.config_xml_catalog
def _main():
    exit_status = 0

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
    parser.add_argument('--loglevel', default='')  # disabled by default
    parser.add_argument('--nocolors', action='store_false',
                        help='prevents the output from being colorized by ANSI escape sequences')
    parser.add_argument('--extrasch', action='append', default=[],
                        help='runs an extra validation using an external schematron schema. built-in schemas are available through the prefix `@`: %s.' % AVAILABLE_SCHEMAS)
    parser.add_argument('--sysinfo', action='store_true',
                        help='show program\'s installation info and exit.')
    parser.add_argument('file', nargs='*',
                        help='filesystem path or URL to the XML')
    args = parser.parse_args()

    # All log messages will be omited if level > 50
    logging.basicConfig(level=getattr(logging, args.loglevel.upper(), 999),
            format=LOGGER_FMT)

    if args.sysinfo:
        print(packtools.utils.prettify(packtools.get_debug_info(), colorize=args.nocolors))
        sys.exit(0)

    print('Please wait, this may take a while...', file=sys.stderr)

    input_args = args.file or sys.stdin
    summary_list = []

    LOGGER.info('running with catalog: %s', catalogs.NAME)

    for xml in packtools.utils.flatten(input_args):
        LOGGER.info('starting validation of "%s"', xml)

        try:
            validator = get_xmlvalidator(xml, args.nonetwork, args.extrasch)

        except (etree.XMLSyntaxError, exceptions.XMLDoctypeError,
                exceptions.XMLSPSVersionError) as exc:
            LOGGER.exception(exc)
            print(ERR_MESSAGE.format(filename=xml, details=exc),
                    file=sys.stderr)
            exit_status = 1
            continue

        if args.annotated:

            fname, fext = xml.rsplit('.', 1)
            out_fname = '.'.join([fname, 'annotated', fext])

            with open(out_fname, 'wb') as fp:
                annotate(validator, fp)

            is_valid, _ = validator.validate_all()
            if is_valid is False:
                exit_status = 1

            print('Annotated XML file: "%s"' % out_fname)

        else:
            # remote XML will not lookup for assets
            if xml.startswith(('http:', 'https:')):
                LOGGER.info('disabling assets lookup since "%s" is a '
                            'remote file', xml)
                assetsdir = ''
                assetsdir_files = []
            else:
                assetsdir = args.assetsdir or os.path.dirname(xml)
                assetsdir_files = os.listdir(assetsdir)  # list of files in dir

            try:
                summary = summarize(validator, assets_basedir=assetsdir_files)
            except TypeError as exc:
                LOGGER.exception(exc)
                LOGGER.info(
                        'error validating "%s". Skipping. '
                        'run with option `--loglevel INFO` for more info',
                        xml)
                continue

            summary['_xml'] = xml

            if args.raw:
                print(json.dumps(summary, sort_keys=True))
            else:
                summary_list.append(summary)

            # set the exit status to 1 if the xml is not valid
            if summary['is_valid'] is False:
                exit_status = 1

        LOGGER.info('finished validating "%s"', xml)

    if summary_list:
        print(packtools.utils.prettify(summary_list, colorize=args.nocolors))

    return exit_status


def main():
    try:
        sys.exit(_main())
    except KeyboardInterrupt:
        LOGGER.info('terminating the program')
        sys.exit(1)
    except Exception as exc:
        LOGGER.exception(exc)
        sys.exit('An unexpected error has occurred: %s' % exc)


if __name__ == '__main__':
    main()

