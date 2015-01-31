#coding: utf-8
from __future__ import print_function
import os
import argparse
import sys
import pkg_resources
import json

from lxml import etree
# import pygments if here
try:
    import pygments     # NOQA
    from pygments.lexers import get_lexer_for_mimetype
    from pygments.formatters import TerminalFormatter
except ImportError:
    pygments = False    # NOQA

import packtools


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


class XMLError(Exception):
    """ Represents errors that would block XMLValidator instance from
    being created.
    """

def prettify(jsonobj):
    """ Prettify JSON output.

    Function copied from Circus process manager:
    https://github.com/circus-tent/circus/blob/master/circus/circusctl.py
    """

    json_str = json.dumps(jsonobj, indent=2, sort_keys=True)
    if pygments:
        try:
            lexer = get_lexer_for_mimetype("application/json")
            return pygments.highlight(json_str, lexer, TerminalFormatter())
        except:
            pass

    return json_str


def get_xmlvalidator(xmlpath, no_network):
    try:
        parsed_xml = packtools.XML(xmlpath, no_network=no_network)
    except IOError:
        raise XMLError('Error reading %s. Make sure it is a valid file-path or URL.' % xmlpath)
    except etree.XMLSyntaxError as e:
        raise XMLError('Error reading %s. Syntax error: %s' % (xmlpath, e))

    try:
        xml = packtools.XMLValidator(parsed_xml)
    except ValueError as e:
        raise XMLError('Error reading %s. %s.' % (xmlpath, e))

    return xml


def summarize(validator, assets_basedir=None):
    dtd_is_valid, dtd_errors = validator.validate()
    sps_is_valid, sps_errors = validator.validate_style()

    summary = {
        'dtd_errors': ['{message}'.format(message=err.message)
                       for err in dtd_errors],
        'sps_errors': ['{message}'.format(message=err.message)
                       for err in sps_errors],
    }

    if assets_basedir:
        summary['assets'] = validator.lookup_assets(assets_basedir)

    return summary


@config_xml_catalog
def main():

    packtools_version = pkg_resources.get_distribution('packtools').version

    parser = argparse.ArgumentParser(description='stylechecker cli utility')
    parser.add_argument('--annotated', action='store_true',
                        help='reproduces the XML with notes at elements that have errors')
    parser.add_argument('--nonetwork', action='store_true',
                        help='prevents the retrieval of the DTD through the network')
    parser.add_argument('--assetsdir', default=None,
                        help='lookup, at the given directory, for each asset referenced by the XML')
    parser.add_argument('XML', nargs='+',
                        help='filesystem path or URL to the XML')
    parser.add_argument('--version', action='version', version=packtools_version)

    args = parser.parse_args()

    if len(args.XML) > 1:
        print('Please wait, this may take a while...')

    summary_list = []
    for xml in args.XML:
        try:
            xml_validator = get_xmlvalidator(xml, args.nonetwork)
        except XMLError as e:
            sys.exit(e)

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
                summary = summarize(xml_validator, assets_basedir=args.assetsdir)
            except TypeError as e:
                sys.exit('Error validating %s. %s.' % (xml_validator, e))

            summary['_xml'] = xml
            summary['is_valid'] = bool(xml_validator.validate()[0] and xml_validator.validate_style()[0])

            summary_list.append(summary)

    if summary_list:
        print(prettify(summary_list))


if __name__ == '__main__':
    main()

