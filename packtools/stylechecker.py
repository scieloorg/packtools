#coding: utf-8
import logging
from copy import deepcopy
import os

from lxml import etree, isoschematron

from packtools.utils import XML
from packtools.checks import StyleCheckingPipeline
from packtools.adapters import SchematronStyleError, SchemaStyleError
from packtools.catalogs import SCHEMAS, XML_CATALOG


ALLOWED_PUBLIC_IDS = (
    '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN',
    '-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN',
)


logger = logging.getLogger(__name__)


def XMLSchematron(schema_name):
    """Returns an instance of `isoschematron.Schematron`.

    The returned instance is cached due to performance reasons.
    """
    cache = XMLSchematron.func_dict.setdefault('cache', {})

    if schema_name in cache:
        return cache[schema_name]
    else:
        with open(SCHEMAS[schema_name]) as fp:
            xmlschema_doc = etree.parse(fp)

        schematron = isoschematron.Schematron(xmlschema_doc)
        cache[schema_name] = schematron
        return schematron


class XMLValidator(object):
    """Adapter that performs SPS validations.

    If `file` is not an etree instance, it will be parsed using
    :func:`XML`.

    SPS validation stages are:
      - JATS 1.0 or PMC 3.0 (as bound by the doctype declaration or passed
        explicitly)
      - SciELO Style - ISO Schematron
      - SciELO Style - Python based pipeline

    If the DOCTYPE is declared, its public id is validated against a white list,
    declared by ``allowed_public_ids`` class variable. The system id is ignored.
    By default, the allowed values are:

      - ``-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN``
      - ``-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN``

    :param file: Path to the XML file, URL, etree or file-object.
    :param dtd: (optional) etree.DTD instance. If not provided, we try the external DTD.
    :param no_doctype: (optional) if missing DOCTYPE declaration is accepted.
    """
    allowed_public_ids = frozenset(ALLOWED_PUBLIC_IDS)

    def __init__(self, file, dtd=None, no_doctype=False):
        if isinstance(file, etree._ElementTree):
            self.lxml = file
        else:
            self.lxml = XML(file)

        self.dtd = dtd or self.lxml.docinfo.externalDTD
        self.source_url = self.lxml.docinfo.URL

        self.doctype = self.lxml.docinfo.doctype
        if no_doctype is False:
            if not self.doctype:
                raise ValueError('Missing DOCTYPE declaration')

        if self.doctype and self.lxml.docinfo.public_id not in self.allowed_public_ids:
            raise ValueError('Unsuported DOCTYPE public id')

        self.public_id = self.lxml.docinfo.public_id
        self.schematron = XMLSchematron('scielo-style.sch')
        self.ppl = StyleCheckingPipeline()

    def validate(self):
        """Validate the source XML against JATS DTD.

        Returns a tuple comprising the validation status and the errors list.
        """
        if self.dtd is None:
            raise TypeError('The DTD/XSD could not be loaded')

        def make_error_log():
            return [SchemaStyleError(err) for err in self.dtd.error_log]

        result = self.dtd.validate(self.lxml)
        errors = make_error_log()
        return result, errors

    def _validate_sch(self):
        """Validate the source XML against SPS-Style Schematron.

        Returns a tuple comprising the validation status and the errors list.
        """
        def make_error_log():
            err_log = self.schematron.error_log
            return [SchematronStyleError(err) for err in err_log]

        result = self.schematron.validate(self.lxml)
        errors = make_error_log()
        return result, errors

    def validate_style(self):
        """Validate the source XML against SPS-Style Tagging guidelines.

        Returns a tuple comprising the validation status and the errors list.
        """
        def make_error_log():
            errors = next(self.ppl.run(self.lxml, rewrap=True))
            errors += self._validate_sch()[1]
            return errors

        errors = make_error_log()
        result = not bool(errors)
        return result, errors

    def validate_all(self, fail_fast=False):
        """Runs all validations.

        First, the XML is validated against the DTD (calling :meth:`validate`).
        If no DTD is provided and the argument ``fail_fast == True``, a ``TypeError``
        is raised. After that, the XML is validated against the SciELO style
        (calling :meth:`validate_style`).

        :param fail_fast: (optional) raise ``TypeError`` if the DTD has not been loaded.
        """
        try:
            v_result, v_errors = self.validate()

        except TypeError:
            if fail_fast:
                raise
            else:
                v_result = None
                v_errors = []

        s_result, s_errors = self.validate_style()

        val_status = False if s_result is False else v_result
        val_errors = v_errors + s_errors

        return val_status, val_errors

    def _annotate_error(self, element, error):
        """Add an annotation prior to `element`, with `error` as the content.

        The annotation is a comment added prior to `element`.

        :param element: etree instance to be annotated.
        :param error: string of the error.
        """
        notice_element = etree.Element('SPS-ERROR')
        notice_element.text = error
        element.addprevious(etree.Comment('SPS-ERROR: %s' % error))

    def annotate_errors(self, fail_fast=False):
        """Add notes on all elements that have errors.

        The errors list is generated as the result of calling :meth:`validate_all`.
        """
        status, errors = self.validate_all(fail_fast=fail_fast)
        mutating_xml = deepcopy(self.lxml)

        if status == True:
            return mutating_xml

        for error in errors:
            try:
                err_element = error.get_apparent_element(mutating_xml)
            except ValueError:
                logger.info('Could not locate the element name in: %s' % error.message)
                err_element = mutating_xml.getroot()

            self._annotate_error(err_element, error.message)

        return mutating_xml

    def __str__(self):
        return etree.tostring(self.lxml, pretty_print=True,
            encoding='utf-8', xml_declaration=True)

    def __unicode__(self):
        return str(self).decode('utf-8')

    def __repr__(self):
        try:
            is_valid = self.validate_all()[0]
        except TypeError:
            is_valid = None

        return '<%s xml=%s valid=%s>' % (self.__class__.__name__, self.lxml, is_valid)

    def read(self):
        """Read the XML contents as text.
        """
        return unicode(self)

    @property
    def meta(self):
        """Article metadata.
        """
        parsed_xml = self.lxml

        xml_nodes = {
            "journal_title": "front/journal-meta/journal-title-group/journal-title",
            "journal_eissn": "front/journal-meta/issn[@pub-type='epub']",
            "journal_pissn": "front/journal-meta/issn[@pub-type='ppub']",
            "article_title": "front/article-meta/title-group/article-title",
            "issue_year": "front/article-meta/pub-date/year",
            "issue_volume": "front/article-meta/volume",
            "issue_number": "front/article-meta/issue",
        }

        metadata = {'filename': self.source_url}
        for node_k, node_v in xml_nodes.items():
            node = parsed_xml.find(node_v)
            metadata[node_k] = getattr(node, 'text', None)

        return metadata


def config_xml_catalog(func):
    """Wraps the execution of ``func``, setting-up and tearing-down the
    ``XML_CATALOG_FILES`` environment variable for the current process.
    """
    def wrapper(*args, **kwargs):
        os.environ['XML_CATALOG_FILES'] = XML_CATALOG
        _return = func(*args, **kwargs)
        del(os.environ['XML_CATALOG_FILES'])
        return _return
    return wrapper


@config_xml_catalog
def main():
    import argparse
    import sys
    import pkg_resources

    packtools_version = pkg_resources.get_distribution('packtools').version

    parser = argparse.ArgumentParser(description='stylechecker cli utility.')
    parser.add_argument('--annotated', action='store_true')
    parser.add_argument('--nonetwork', action='store_true')
    parser.add_argument('xmlpath',
                        help='Filesystem path or URL to the XML file.')
    parser.add_argument('--version', action='version', version=packtools_version)

    args = parser.parse_args()
    try:
        parsed_xml = XML(args.xmlpath, no_network=args.nonetwork)

    except IOError:
        sys.exit('Error reading %s. Make sure it is a valid file-path or URL.' % args.xmlpath)

    except etree.XMLSyntaxError as e:
        sys.exit('Error reading %s. Syntax error: %s' % (args.xmlpath, e.message))

    else:
        try:
            xml = XMLValidator(parsed_xml)

        except ValueError as e:
            sys.exit('Error reading %s. %s.' % (args.xmlpath, e.message))

    try:
        # validation may raise TypeError when the DTD lookup fails.
        is_valid, errors = xml.validate()
    except TypeError as e:
        sys.exit('Error validating %s. %s.' % (args.xmlpath, e.message))

    style_is_valid, style_errors = xml.validate_style()

    if args.annotated:
        err_xml = xml.annotate_errors()
        sys.stdout.write(etree.tostring(err_xml, pretty_print=True,
            encoding='utf-8', xml_declaration=True))

    else:
        if not is_valid:
            print 'Invalid XML! Found %s errors:' % len(errors)
            for err in errors:
                print '%s,%s\t%s' % (err.line, err.column, err.message)
        else:
            print 'Valid XML! ;)'

        if not style_is_valid:
            print 'Invalid SPS Style! Found %s errors:' % len(style_errors)
            for err in style_errors:
                print err.message
        else:
            print 'Valid SPS Style! ;)'

if __name__ == '__main__':
    main()

