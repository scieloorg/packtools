# coding=utf-8
import os
from tempfile import TemporaryDirectory

from packtools import XMLValidator, etree, XML
from packtools.domain import SchematronValidator, PyValidator
from gettext import gettext as _


IS_PACKTOOLS_INSTALLED = False
try:
    from packtools.catalogs import XML_CATALOG
    os.environ['XML_CATALOG_FILES'] = XML_CATALOG
    IS_PACKTOOLS_INSTALLED = True
except Exception as e:
    os.environ['XML_CATALOG_FILES'] = ''


DEFAULT_VERSIONS = {
    '-//NLM//DTD Journal Publishing DTD v3.0 20080202//EN': {
        "sps_versions": [
            None,
            'sps-1.0',
            'sps-1.1',
        ],
        "url": "https://dtd.nlm.nih.gov/publishing/3.0/journalpublishing3.dtd",
    },
    '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.0 20120330//EN': {
        "sps_versions": [
            'sps-1.2',
            'sps-1.3',
            'sps-1.4',
            'sps-1.5',
            'sps-1.6',
            'sps-1.7',
            'sps-1.8',
        ],
        "url": "https://jats.nlm.nih.gov/publishing/1.0/JATS-journalpublishing1.dtd",
    },
    '-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20151215//EN': {
        "sps_versions": [
            'sps-1.7',
            'sps-1.8',
            'sps-1.9',
        ],
        "url": "https://jats.nlm.nih.gov/publishing/1.1/JATS-journalpublishing1.dtd",
    },
    "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.3 20210610//EN": {
        "sps_versions": [
            'sps-1.10',
        ],
        "url": "https://jats.nlm.nih.gov/publishing/1.3/JATS-journalpublishing1-3.dtd",
    },
}


class StructureValidator:

    def __init__(self, xml_with_pre, VERSIONS=None):
        self.xml_with_pre = xml_with_pre
        self.VERSIONS = VERSIONS
        sps_version = self.xml_with_pre.sps_version
        auto_loaded_sch_label = u'@' + sps_version
        self.style_validators = [
            SchematronValidator.from_catalog(
                sps_version,
                label=auto_loaded_sch_label),
            PyValidator(label=auto_loaded_sch_label),
            # the python based validation pipeline
        ]

        with TemporaryDirectory() as targetdir:
            filename = "a.xml"
            target = os.path.join(targetdir, filename)
            with open(target, 'w') as fp:
                fp.write(self.xml_with_pre.tostring())
            # saved optimised
            with open(target, "rb") as fp:
                self.xml_validator = XMLValidator.parse(XML(fp))

    def validate_doctype(self, VERSIONS=None):
        VERSIONS = VERSIONS or self.VERSIONS or DEFAULT_VERSIONS
        try:
            dtd_version = VERSIONS[self.xml_with_pre.public_id]
        except KeyError:
            yield {
                "result": "error",
                "message": _('Unknown {}: {}').format(
                    'PUBLIC ID',
                    self.xml_with_pre.public_id,
                )
            }
            return

        if self.xml_with_pre.sps_version not in dtd_version["sps_versions"]:
            yield {
                "result": "error",
                "message": _('Unmatched {}: {}. Expected one of {}').format(
                    'sps version',
                    self.xml_with_pre.sps_version,
                    dtd_version["sps_versions"],
                )
            }

        try:
            system_id = self.xml_with_pre.system_id.split("://")[1]
            if system_id not in dtd_version['url']:
                yield {
                    "result": "error",
                    "message": _('Unmatched {}: {}. Expected {}').format(
                        'SYSTEM ID',
                        self.xml_with_pre.system_id,
                        dtd_version['url'],
                    )
                }
        except (AttributeError, ValueError, TypeError, IndexError):
            yield {
                "result": "error",
                "message": _('Unmatched {}: {}. Expected {}').format(
                    'SYSTEM ID',
                    self.xml_with_pre.system_id,
                    dtd_version['url'],
                )
            }

    def annotate_errors(self):
        return etree.tostring(
            self.xml_validator.annotate_errors(),
            pretty_print=True,
            encoding='utf-8',
            xml_declaration=True,
        ).decode("utf-8")

    def validate_dtd(self):
        try:
            dtd_is_valid, dtd_errors = self.xml_validator.validate()
        except Exception as e:
            dtd_is_valid, dtd_errors = False, [str(e)]
        return {"dtd_is_valid": dtd_is_valid, "dtd_errors": dtd_errors}

    def validate_style(self):
        try:
            style_is_valid, style_errors = self.xml_validator.validate_style()
        except Exception as e:
            style_is_valid, style_errors = False, [str(e)]
        return {"style_is_valid": style_is_valid, "style_errors": style_errors}

    def validate(self):
        dtd_validation_result = self.validate_dtd()
        style_validation_result = self.validate_style()
        d = {
            "is_valid": bool(
                dtd_validation_result["dtd_is_valid"] and
                style_validation_result["style_is_valid"]),
            "errors_number": (
                len(dtd_validation_result["dtd_errors"]) +
                len(style_validation_result["style_errors"])
            ),
            "doctype_validation_result": list(self.validate_doctype()),
        }
        d.update(dtd_validation_result)
        d.update(style_validation_result)
        return d
