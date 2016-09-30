# coding:utf-8
"""The domain-specific adapters.

An adapter is an object that provides domain-specific apis for another object,
called adaptee.

Examples are: XMLValidator and XMLPacker objects, which provide SciELO PS
validation behaviour and packaging functionality, respectively.
"""
from __future__ import unicode_literals
import logging
from copy import deepcopy
import os
try:
    import reprlib
except ImportError:
    import repr as reprlib

from lxml import etree, isoschematron

from . import utils, catalogs, checks, style_errors, exceptions


__all__ = ['XMLValidator', 'HTMLGenerator']


LOGGER = logging.getLogger(__name__)


# As a general rule, only the latest 2 versions are supported simultaneously.
CURRENTLY_SUPPORTED_VERSIONS = os.environ.get(
    'PACKTOOLS_SUPPORTED_SPS_VERSIONS', 'sps-1.4:sps-1.5').split(':')

ALLOWED_PUBLIC_IDS = (
    '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN',
)

# doctype public ids for sps <= 1.1
ALLOWED_PUBLIC_IDS_LEGACY = (
    '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN',
    '-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN',
)


def _get_public_ids(sps_version):
    """Returns the set of allowed public ids for the XML based on its version.
    """
    if sps_version in ['pre-sps', 'sps-1.1']:
        return frozenset(ALLOWED_PUBLIC_IDS_LEGACY)
    else:
        return frozenset(ALLOWED_PUBLIC_IDS)


def _init_sps_version(xml_et, supported_versions=None):
    """Returns the SPS spec version for `xml_et` or raises ValueError.

    It also checks if the version is currently supported.

    :param xml_et: etree instance.
    :param supported_versions: (optional) the default value is set by env var `PACKTOOLS_SUPPORTED_SPS_VERSIONS`.
    """
    if supported_versions is None:
        supported_versions = CURRENTLY_SUPPORTED_VERSIONS

    doc_root = xml_et.getroot()
    version_from_xml = doc_root.attrib.get('specific-use', None)
    if version_from_xml is None:
        raise exceptions.XMLSPSVersionError('Missing SPS version at /article/@specific-use')

    if version_from_xml not in supported_versions:
        raise exceptions.XMLSPSVersionError('%s is not currently supported' % version_from_xml)
    else:
        return version_from_xml


def Schematron(file):
    with open(file, mode='rb') as fp:
        xmlschema_doc = etree.parse(fp)

    return isoschematron.Schematron(xmlschema_doc)


def StdSchematron(schema_name):
    """Returns an instance of `isoschematron.Schematron`.

    A standard schematron is one bundled with packtools.
    The returned instance is cached due to performance reasons.

    :param schema_name: The logical name of schematron file in the package `catalogs`.
    """
    cache = utils.setdefault(StdSchematron, 'cache', lambda: {})

    if schema_name in cache:
        return cache[schema_name]
    else:
        try:
            schematron = Schematron(catalogs.SCHEMAS[schema_name])
        except KeyError:
            raise ValueError('Unknown schema %s' % (schema_name,))

        cache[schema_name] = schematron
        return schematron


def XSLT(xslt_name):
    """Returns an instance of `etree.XSLT`.

    The returned instance is cached due to performance reasons.
    """
    cache = utils.setdefault(XSLT, 'cache', lambda: {})

    if xslt_name in cache:
        return cache[xslt_name]
    else:
        try:
            xslt_doc = etree.parse(catalogs.XSLTS[xslt_name])
        except KeyError:
            raise ValueError('Unknown xslt %s' % (xslt_name,))

        xslt = etree.XSLT(xslt_doc)
        cache[xslt_name] = xslt
        return xslt


#--------------------------------
# adapters for etree._ElementTree
#--------------------------------
class XMLValidator(object):
    """Adapter that performs SPS validations.

    SPS validation stages are:
      - JATS 1.0 or PMC 3.0 (as bound by the doctype declaration or passed
        explicitly)
      - SciELO Style - ISO Schematron
      - SciELO Style - Python based pipeline

    :param file: etree._ElementTree instance.
    :param sps_version: the version of the SPS that will be the basis for validation.
    :param dtd: (optional) etree.DTD instance. If not provided, we try the external DTD.
    :param extra_schematron: (optional) extra schematron schema.
    """
    def __init__(self, file, sps_version, dtd=None, extra_schematron=None):
        assert isinstance(file, etree._ElementTree)

        self.lxml = file
        self.sps_version = sps_version
        self.allowed_public_ids = _get_public_ids(self.sps_version)
        self.doctype = self.lxml.docinfo.doctype
        self.dtd = dtd or self.lxml.docinfo.externalDTD
        self.source_url = self.lxml.docinfo.URL
        self.public_id = self.lxml.docinfo.public_id
        self.encoding = self.lxml.docinfo.encoding

        # Load schematron schema based on sps version. Can raise ValueError
        self.schematron = StdSchematron(self.sps_version)

        # Load user-provided schematron schema
        if extra_schematron:
            self.extra_schematron = Schematron(extra_schematron)
        else:
            self.extra_schematron = None

        # Load python based validation pipeline
        self.ppl = checks.StyleCheckingPipeline()

        # Cache of validation results
        self._validation_errors = {'dtd': (), 'style': ()}

    @classmethod
    def parse(cls, file, no_doctype=False, sps_version=None,
            supported_sps_versions=None, **kwargs):
        """Factory of XMLValidator instances.

        If `file` is not an etree instance, it will be parsed using
        :func:`XML`.

        If the DOCTYPE is declared, its public id is validated against a white list,
        declared by ``allowed_public_ids`` class variable. The system id is ignored.
        By default, the allowed values are:

          - SciELO PS >= 1.2:
            - ``-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN``
          - SciELO PS 1.1:
            - ``-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN``
            - ``-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN``

        :param file: Path to the XML file, URL, etree or file-object.
        :param no_doctype: (optional) if missing DOCTYPE declaration is accepted.
        :param sps_version: (optional) force the style validation against a SPS version.
        :param supported_sps_versions: (optional) list of supported versions. the
               only way to bypass this restriction is by using the arg `sps_version`.
        """
        if isinstance(file, etree._ElementTree):
            et = file
        else:
            et = utils.XML(file)

        # can raise exception
        sps_version = sps_version or _init_sps_version(et, supported_sps_versions)

        allowed_public_ids = _get_public_ids(sps_version)

        # DOCTYPE declaration must be present by default. This behaviour can
        # be changed by the `no_doctype` arg.
        doctype = et.docinfo.doctype
        if not doctype and not no_doctype:
            raise exceptions.XMLDoctypeError('Missing DOCTYPE declaration')

        # if there exists a DOCTYPE declaration, ensure its PUBLIC-ID is
        # supported.
        public_id = et.docinfo.public_id
        if doctype and public_id not in allowed_public_ids:
            raise exceptions.XMLDoctypeError('Unsuported DOCTYPE public id')

        return cls(et, sps_version, **kwargs)

    def validate(self):
        """Validate the source XML against JATS DTD.

        Returns a tuple comprising the validation status and the errors list.
        """
        if len(self._validation_errors['dtd']) == 0:
            if self.dtd is None:
                raise exceptions.UndefinedDTDError('The DTD/XSD could not be loaded')

            def make_error_log():
                return [style_errors.SchemaStyleError(err) for err in self.dtd.error_log]

            result = self.dtd.validate(self.lxml)
            errors = make_error_log()
            self._validation_errors['dtd'] = result, errors

        return self._validation_errors['dtd']

    def _validate_sch(self):
        """Validate the source XML against SPS-Style Schematron.

        Returns a tuple comprising the validation status and the errors list.
        """
        def make_error_log(schematron):
            err_log = schematron.error_log
            return [style_errors.SchematronStyleError(err) for err in err_log]

        result = self.schematron.validate(self.lxml)
        errors = make_error_log(self.schematron)

        if self.extra_schematron:
            extra_result = self.extra_schematron.validate(self.lxml)  # run
            result = result and extra_result
            errors += make_error_log(self.extra_schematron)

        return result, errors

    def validate_style(self):
        """Validate the source XML against SPS-Style Tagging guidelines.

        Returns a tuple comprising the validation status and the errors list.
        """
        if len(self._validation_errors['style']) == 0:
            def make_error_log():
                errors = next(self.ppl.run(self.lxml, rewrap=True))
                errors += self._validate_sch()[1]
                return errors

            errors = make_error_log()
            result = not bool(errors)
            self._validation_errors['style'] = result, errors

        return self._validation_errors['style']

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

        except exceptions.UndefinedDTDError:
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

        if status is True:
            return mutating_xml

        err_pairs = []
        for error in errors:
            try:
                err_element = error.get_apparent_element(mutating_xml)
            except ValueError:
                LOGGER.info('Could not locate the element name in: %s', error.message)
                err_element = mutating_xml.getroot()

            err_pairs.append((err_element, error.message))

        for el, em in err_pairs:
            self._annotate_error(el, em)

        return mutating_xml

    def __repr__(self):
        arg_names = [u'lxml', u'sps_version', u'dtd']
        arg_values = [reprlib.repr(getattr(self, arg)) for arg in arg_names]
        arg_names[0] = u'file'

        args = zip(arg_names, arg_values)
        attrib_args = (u'{}={}'.format(name, value) for name, value in args)

        return '<XMLValidator object at 0x%x (%s)>' % (
                id(self), u', '.join(attrib_args))

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

    @property
    def assets(self):
        """Lists all static assets referenced by the XML.
        """
        return utils.get_static_assets(self.lxml)

    def lookup_assets(self, base):
        """Look for each asset in `base`, and returns a list of tuples
        with the asset name and its presence status.

        :param base: any container that implements membership tests, i.e.
                     it must support the ``in`` operator.
        """
        return [(asset, asset in base) for asset in self.assets]


class HTMLGenerator(object):
    """Adapter that generates HTML from SPS XML.

    Basic usage:

    .. code-block:: python

        from lxml import etree

        xml = etree.parse('valid-sps-file.xml')
        generator = HTMLGenerator(xml)

        html = generator.generate('pt')
        html_string = etree.tostring(html, encoding='unicode', method='html')


    :param file: etree._ElementTree instance.
    :param xslt: (optional) etree.XSLT instance. If not provided, the default XSLT is used.
    :param css: (optional) URI for a CSS file.
    """
    def __init__(self, file, xslt=None, css=None):
        assert isinstance(file, etree._ElementTree)

        self.lxml = file
        self.xslt = xslt or XSLT('root-html-1.2.xslt')
        self.css = css

    @classmethod
    def parse(cls, file, valid_only=True, **kwargs):
        """Factory of HTMLGenerator instances.

        If `file` is not an etree instance, it will be parsed using
        :func:`XML`.

        :param file: Path to the XML file, URL, etree or file-object.
        :param valid_only: (optional) prevents the generation of HTML for invalid XMLs.
        """
        if isinstance(file, etree._ElementTree):
            et = file
        else:
            et = utils.XML(file)

        if valid_only:
            is_valid, _ = XMLValidator.parse(et).validate_all()
            if not is_valid:
                raise ValueError('The XML is not valid according to SPS rules')

        return cls(et, **kwargs)

    @property
    def languages(self):
        """The language of the main document plus all translations.
        """
        return self.lxml.xpath(
            '/article/@xml:lang | //sub-article[@article-type="translation"]/@xml:lang')

    @property
    def language(self):
        """The language of the main document.
        """
        try:
            return self.lxml.xpath('/article/@xml:lang')[0]
        except IndexError:
            return None

    def _is_aop(self):
        """ Has the document been published ahead-of-print?
        """
        volume = self.lxml.findtext('front/article-meta/volume')
        number = self.lxml.findtext('front/article-meta/issue')

        return volume == '00' and number == '00'

    def _get_issue_label(self):
        volume = self.lxml.findtext('front/article-meta/volume')
        number = self.lxml.findtext('front/article-meta/issue')

        return 'vol.%s n.%s' % (volume, number)

    def _get_bibliographic_legend(self):
        return '[#BIBLIOGRAPHIC LEGEND#]'

        issue = 'ahead of print' if self._is_aop() else self._get_issue_label()

        abrev_title = self.lxml.findtext(
            'front/journal-meta/journal-title-group/abbrev-journal-title[@abbrev-type="publisher"]')
        city = '[#CITY#]'

        pubdate = self.lxml.xpath(
            '/article/front/article-meta/pub-date[@pub-type="epub-ppub" or @pub-type="epub"][1]')[0]
        pubtype = 'Epub' if pubdate.xpath('@pub-type')[0] == 'epub' else ''
        day = pubdate.findtext('day')
        month = pubdate.findtext('month')
        year = pubdate.findtext('year')
        dates = ' '.join([month, year]) if month else year

        parts = [abrev_title, issue, city, pubtype, dates]

        return ' '.join([part for part in parts if part])

    def __iter__(self):
        """Iterates thru all languages and generates the HTML for each one.
        """
        for lang in self.languages:
            res_html = self.generate(lang)
            yield lang, res_html

    def generate(self, lang):
        """Generates the HTML in the language ``lang``.

        :param lang: 2-digit ISO 639-1 text string.
        """
        main_language = self.language
        if main_language is None:
            raise exceptions.HTMLGenerationError('Main document language is '
                                                 'undefined.')

        if lang not in self.languages:
            raise ValueError('Unknown language "%s"' % lang)

        is_translation = lang != main_language
        return self.xslt(
                self.lxml,
                article_lang=etree.XSLT.strparam(lang),
                is_translation=etree.XSLT.strparam(str(is_translation)),
                bibliographic_legend=etree.XSLT.strparam(self._get_bibliographic_legend()),
                issue_label=etree.XSLT.strparam(self._get_issue_label()),
                styles_css_path=etree.XSLT.strparam(self.css or ''),
        )

