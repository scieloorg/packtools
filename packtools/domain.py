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

from lxml import etree

from . import utils, catalogs, checks, style_errors, exceptions


__all__ = ['XMLValidator', 'HTMLGenerator']


LOGGER = logging.getLogger(__name__)


# As a general rule, only the latest 2 versions are supported simultaneously.
CURRENTLY_SUPPORTED_VERSIONS = os.environ.get(
    'PACKTOOLS_SUPPORTED_SPS_VERSIONS', 'sps-1.7:sps-1.8').split(':')

ALLOWED_PUBLIC_IDS = (
    '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN',
    '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN',
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
        raise exceptions.XMLSPSVersionError('cannot get the SPS version from /article/@specific-use')

    if version_from_xml not in supported_versions:
        raise exceptions.XMLSPSVersionError('version "%s" is not currently supported' % version_from_xml)
    else:
        return version_from_xml


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
            schema_path = catalogs.SCHEMAS[schema_name]
        except KeyError:
            raise ValueError('unrecognized schema: "%s"' % schema_name)

        schematron = utils.get_schematron_from_filepath(schema_path)
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
            raise ValueError('unrecognized xslt: "%s"' % xslt_name)

        xslt = etree.XSLT(xslt_doc)
        cache[xslt_name] = xslt
        return xslt


#----------------------------------
# validators for etree._ElementTree
#
# a validator is an object that
# provides the method ``validate``,
# with the following signature:
# validate(xmlfile: etree._ElementTree) -> Tuple(bool, list)
#----------------------------------
class PyValidator(object):
    """Style validations implemented in Python.
    """
    def __init__(self, pipeline=checks.StyleCheckingPipeline, label=u''):
        self.ppl = pipeline()
        self.label = label

    def validate(self, xmlfile):
        errors = next(self.ppl.run(xmlfile, rewrap=True))
        for error in errors:
            error.label = self.label

        return bool(errors), errors


class DTDValidator(object):
    """DTD validations.
    """
    def __init__(self, dtd, label=u''):
        self.dtd = dtd
        self.label = label

    def validate(self, xmlfile):
        """Validate xmlfile against the given DTD.

        Returns a tuple comprising the validation status and the errors list.
        """
        result = self.dtd.validate(xmlfile)
        errors = [style_errors.SchemaStyleError(err, label=self.label)
                  for err in self.dtd.error_log]

        return result, errors


class SchematronValidator(object):
    """Style validations implemented in Schematron.
    """
    def __init__(self, sch, label=u''):
        self.sch = sch
        self.label = label

    @classmethod
    def from_catalog(cls, ref, **kwargs):
        """Get an instance based on schema's reference name.

        :param ref: The reference name for the schematron file in
                    :data:`packtools.catalogs.SCH_SCHEMAS`.
        """
        return cls(StdSchematron(ref), **kwargs)

    def validate(self, xmlfile):
        """Validate xmlfile against the given Schematron schema.

        Returns a tuple comprising the validation status and the errors list.
        """
        result = self.sch.validate(xmlfile)
        errors = [style_errors.SchematronStyleError(err, label=self.label)
                  for err in self.sch.error_log]

        return result, errors


def iter_schematronvalidators(iterable):
    """Returns a generator of :class:`packtools.domain.SchematronValidator`.

    :param iterable: an iterable where each item follows one of the forms
                     ``Iterable[isoschematron.Schematron]`` or
                     ``Iterable[Tuple[isoschematron.Schematron, str]]``. The
                     latter sets the label attribute of the validator instance.
    """
    for item in iterable:
        try:
            sch_obj, sch_label = item
        except TypeError:
            sch_obj = item
            sch_label = u''

        validator = SchematronValidator(sch_obj, label=sch_label)
        yield validator


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
    :param style_validators: (optional) list of
                             :class:`packtools.domain.SchematronValidator`
                             objects.
    """
    def __init__(self, file, dtd=None, style_validators=None):
        assert isinstance(file, etree._ElementTree)

        self.lxml = file
        self.doctype = self.lxml.docinfo.doctype

        self.dtd = dtd or self.lxml.docinfo.externalDTD
        self.source_url = self.lxml.docinfo.URL
        self.public_id = self.lxml.docinfo.public_id
        self.encoding = self.lxml.docinfo.encoding

        if style_validators:
            self.style_validators = list(style_validators)
        else:
            self.style_validators = []

    @classmethod
    def parse(cls, file, no_doctype=False, sps_version=None,
            supported_sps_versions=None, extra_sch_schemas=None, **kwargs):
        """Factory of XMLValidator instances.

        If `file` is not an etree instance, it will be parsed using
        :func:`packtools.utils.XML`.

        If the DOCTYPE is declared, its public id is validated against a white list,
        declared by :data:`ALLOWED_PUBLIC_IDS` module variable. The system id is ignored.
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
        :param extra_sch_schemas: (optional) list of extra Schematron schemas.
        """
        try:
            et = utils.XML(file)
        except TypeError:
            # We hope it is an instance of etree.ElementTree. If it is not,
            # it will fail in the next lines.
            et = file

        # can raise exception
        sps_version = sps_version or _init_sps_version(et, supported_sps_versions)

        # get the right Schematron validator based on the value of ``sps_version``
        # and then mix it with the list of schemas supplied by the user.
        LOGGER.info('auto-loading style validations for version "%s"', sps_version)

        auto_loaded_sch_label = u'@' + sps_version
        style_validators = [
                SchematronValidator.from_catalog(sps_version,
                    label=auto_loaded_sch_label),
                PyValidator(label=auto_loaded_sch_label),  # the python based validation pipeline
        ]
        if extra_sch_schemas:
            style_validators += list(
                    iter_schematronvalidators(extra_sch_schemas))

        allowed_public_ids = _get_public_ids(sps_version)

        # DOCTYPE declaration must be present by default. This behaviour can
        # be changed by the `no_doctype` arg.
        LOGGER.info('fetching the DOCTYPE declaration')
        doctype = et.docinfo.doctype
        if not doctype and not no_doctype:
            raise exceptions.XMLDoctypeError(
                    'cannot get the DOCTYPE declaration')

        # if there exists a DOCTYPE declaration, ensure its PUBLIC-ID is
        # supported.
        LOGGER.info('fetching the PUBLIC-ID in DOCTYPE declaration')
        public_id = et.docinfo.public_id
        if doctype and public_id not in allowed_public_ids:
            raise exceptions.XMLDoctypeError('invalid DOCTYPE public id')

        return cls(et, style_validators=style_validators, **kwargs)

    @property
    def sps_version(self):
        doc_root = self.lxml.getroot()
        sps_version = doc_root.attrib.get('specific-use', None)
        return sps_version

    @property
    def dtd_validator(self):
        if self.dtd:
            return DTDValidator(self.dtd)
        else:
            return None

    @utils.cachedmethod
    def validate(self):
        """Validate the source XML against JATS DTD.

        Returns a tuple comprising the validation status and the errors list.
        """
        if self.dtd_validator is None:
            raise exceptions.UndefinedDTDError('cannot validate (DTD is not set)')

        result_tuple = self.dtd_validator.validate(self.lxml)
        return result_tuple

    @utils.cachedmethod
    def validate_style(self):
        """Validate the source XML against SPS-Style Tagging guidelines.

        Returns a tuple comprising the validation status and the errors list.
        """
        errors = []
        for validator in self.style_validators:
            LOGGER.info('running validator "%s"', repr(validator))
            errors += validator.validate(self.lxml)[1]

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
    def __init__(self, file, xslt=None, css=None, print_css=None, js=None, permlink=None, url_article_page=None, url_download_ris=None):
        assert isinstance(file, etree._ElementTree)

        self.lxml = file
        self.xslt = xslt or XSLT('root-html-2.0.xslt')
        self.css = css
        self.print_css = print_css
        self.js = js
        self.permlink = permlink
        self.url_article_page = url_article_page
        self.url_download_ris = url_download_ris

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
                raise ValueError('invalid XML')

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
            raise exceptions.HTMLGenerationError('main document language is '
                                                 'undefined.')

        if lang not in self.languages:
            raise ValueError('unrecognized language: "%s"' % lang)

        is_translation = lang != main_language
        return self.xslt(
                self.lxml,
                article_lang=etree.XSLT.strparam(lang),
                is_translation=etree.XSLT.strparam(str(is_translation)),
                bibliographic_legend=etree.XSLT.strparam(self._get_bibliographic_legend()),
                issue_label=etree.XSLT.strparam(self._get_issue_label()),
                styles_css_path=etree.XSLT.strparam(self.css or ''),
                print_styles_css_path=etree.XSLT.strparam(self.print_css or ''),
                js_path=etree.XSLT.strparam(self.js or ''),
                permlink=etree.XSLT.strparam(self.permlink or ''),
                url_article_page=etree.XSLT.strparam(self.url_article_page or ''),
                url_download_ris=etree.XSLT.strparam(self.url_download_ris or ''),
        )
