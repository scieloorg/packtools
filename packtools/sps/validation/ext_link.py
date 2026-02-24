"""
Validation for ext-link elements according to SPS 1.10 specification.

Implements validations for external link elements to ensure:
- Mandatory attributes are present (@ext-link-type, @xlink:href)
- URL format is valid (starts with http:// or https://)
- ext-link-type values are in allowed list
- Link text is descriptive (accessibility)
- @xlink:title is present when text is generic or URL

Reference: https://docs.google.com/document/d/1GTv4Inc2LS_AXY-ToHT3HmO66UT0VAHWJNOIqzBNSgA/edit?tab=t.0#heading=h.n2z5yrri2aba
"""
import re
import gettext

from packtools.sps.models.ext_link import ArticleExtLinks
from packtools.sps.validation.utils import build_response

_ = gettext.gettext


class ExtLinkValidation:
    """
    Validates ext-link elements in scientific article XML.

    Validates presence of mandatory attributes, URL format, allowed values,
    and accessibility requirements (descriptive text).
    """

    GENERIC_PHRASES = [
        "leia mais",
        "clique aqui",
        "acesse",
        "veja mais",
        "saiba mais",
        "click here",
        "read more",
        "see more",
        "learn more",
        "more info",
        "mais informações",
    ]

    ALLOWED_EXT_LINK_TYPES = [
        "uri",
        "doi",
        "pmid",
        "pmcid",
        "clinical-trial",
    ]

    def __init__(self, xmltree, params=None):
        """
        Initialize validation with XML tree and optional parameters.

        Parameters
        ----------
        xmltree : lxml.etree._Element
            The root element of the XML document
        params : dict, optional
            Configuration parameters including error levels
        """
        self.params = params or {}
        self.params.setdefault("ext_link_type_error_level", "CRITICAL")
        self.params.setdefault("xlink_href_error_level", "CRITICAL")
        self.params.setdefault("xlink_href_format_error_level", "ERROR")
        self.params.setdefault("ext_link_type_value_error_level", "ERROR")
        self.params.setdefault("descriptive_text_error_level", "WARNING")
        self.params.setdefault("xlink_title_error_level", "WARNING")

        self.xmltree = xmltree
        # ArticleExtLinks.ext_links uses cached_property: XML is parsed only
        # once regardless of how many validation methods are called.
        self.ext_links_model = ArticleExtLinks(xmltree)

    def validate_ext_link_type_presence(self, error_level=None):
        """
        Validate presence of @ext-link-type attribute (CRITICAL).

        SPS Rule: @ext-link-type is mandatory in all <ext-link> elements.

        Parameters
        ----------
        error_level : str, optional
            Override default error level (default: "CRITICAL")

        Yields
        ------
        dict
            Validation result for each ext-link
        """
        error_level = error_level or self.params.get("ext_link_type_error_level", "CRITICAL")

        for ext_link in self.ext_links_model.ext_links:
            ext_link_type = ext_link.get("ext_link_type")
            text = ext_link.get("text", "")[:50]

            is_valid = bool(ext_link_type)

            advice_text = _(
                'Add @ext-link-type attribute to <ext-link> with text "{text}".'
                " Valid values: {allowed_values}"
            )
            advice_params = {
                "text": text,
                "allowed_values": ", ".join(self.ALLOWED_EXT_LINK_TYPES),
            }

            parent = {
                "parent": ext_link.get("parent"),
                "parent_id": ext_link.get("parent_id"),
                "parent_article_type": ext_link.get("parent_article_type"),
                "parent_lang": ext_link.get("parent_lang"),
            }

            yield build_response(
                title="@ext-link-type attribute",
                parent=parent,
                item="ext-link",
                sub_item="@ext-link-type",
                validation_type="exist",
                is_valid=is_valid,
                expected="@ext-link-type attribute present",
                obtained=ext_link_type,
                advice=advice_text.format(**advice_params),
                data=ext_link,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_xlink_href_presence(self, error_level=None):
        """
        Validate presence of @xlink:href attribute (CRITICAL).

        SPS Rule: @xlink:href is mandatory in all <ext-link> elements.

        Parameters
        ----------
        error_level : str, optional
            Override default error level (default: "CRITICAL")

        Yields
        ------
        dict
            Validation result for each ext-link
        """
        error_level = error_level or self.params.get("xlink_href_error_level", "CRITICAL")

        for ext_link in self.ext_links_model.ext_links:
            xlink_href = ext_link.get("xlink_href")
            text = ext_link.get("text", "")[:50]

            is_valid = bool(xlink_href)

            advice_text = _(
                'Add @xlink:href attribute to <ext-link> with text "{text}"'
            )
            advice_params = {"text": text}

            parent = {
                "parent": ext_link.get("parent"),
                "parent_id": ext_link.get("parent_id"),
                "parent_article_type": ext_link.get("parent_article_type"),
                "parent_lang": ext_link.get("parent_lang"),
            }

            yield build_response(
                title="@xlink:href attribute",
                parent=parent,
                item="ext-link",
                sub_item="@xlink:href",
                validation_type="exist",
                is_valid=is_valid,
                expected="@xlink:href attribute present",
                obtained=xlink_href,
                advice=advice_text.format(**advice_params),
                data=ext_link,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_xlink_href_format(self, error_level=None):
        """
        Validate @xlink:href URL format (ERROR).

        SPS Rule: @xlink:href must be a complete URL starting with http:// or https://

        Parameters
        ----------
        error_level : str, optional
            Override default error level (default: "ERROR")

        Yields
        ------
        dict
            Validation result for each ext-link with xlink:href present
        """
        error_level = error_level or self.params.get("xlink_href_format_error_level", "ERROR")

        for ext_link in self.ext_links_model.ext_links:
            xlink_href = ext_link.get("xlink_href")

            # Skip if xlink:href is absent (handled by validate_xlink_href_presence)
            if not xlink_href:
                continue

            is_valid = bool(re.match(r'^https?://', xlink_href, re.IGNORECASE))

            advice_text = _(
                'URL in @xlink:href="{xlink_href}" must start with http:// or https://'
            )
            advice_params = {"xlink_href": xlink_href}

            parent = {
                "parent": ext_link.get("parent"),
                "parent_id": ext_link.get("parent_id"),
                "parent_article_type": ext_link.get("parent_article_type"),
                "parent_lang": ext_link.get("parent_lang"),
            }

            yield build_response(
                title="@xlink:href URL format",
                parent=parent,
                item="ext-link",
                sub_item="@xlink:href",
                validation_type="format",
                is_valid=is_valid,
                expected="URL starting with http:// or https://",
                obtained=xlink_href,
                advice=advice_text.format(**advice_params),
                data=ext_link,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_ext_link_type_value(self, error_level=None):
        """
        Validate @ext-link-type value is in allowed list (ERROR).

        SPS Rule: @ext-link-type must be one of: uri, doi, pmid, pmcid, clinical-trial

        Parameters
        ----------
        error_level : str, optional
            Override default error level (default: "ERROR")

        Yields
        ------
        dict
            Validation result for each ext-link with @ext-link-type present
        """
        error_level = error_level or self.params.get("ext_link_type_value_error_level", "ERROR")

        for ext_link in self.ext_links_model.ext_links:
            ext_link_type = ext_link.get("ext_link_type")

            # Skip if absent (handled by validate_ext_link_type_presence)
            if not ext_link_type:
                continue

            is_valid = ext_link_type in self.ALLOWED_EXT_LINK_TYPES

            advice_text = _(
                'Replace @ext-link-type="{ext_link_type}" with one of: {allowed_values}'
            )
            advice_params = {
                "ext_link_type": ext_link_type,
                "allowed_values": ", ".join(self.ALLOWED_EXT_LINK_TYPES),
            }

            parent = {
                "parent": ext_link.get("parent"),
                "parent_id": ext_link.get("parent_id"),
                "parent_article_type": ext_link.get("parent_article_type"),
                "parent_lang": ext_link.get("parent_lang"),
            }

            yield build_response(
                title="@ext-link-type value",
                parent=parent,
                item="ext-link",
                sub_item="@ext-link-type",
                validation_type="value in list",
                is_valid=is_valid,
                expected=", ".join(self.ALLOWED_EXT_LINK_TYPES),
                obtained=ext_link_type,
                advice=advice_text.format(**advice_params),
                data=ext_link,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_descriptive_text(self, error_level=None):
        """
        Validate link text is descriptive, not generic (WARNING).

        SPS Rule: Text should not be generic phrases like "click here", "read more", etc.
        Validation is case-insensitive.

        Note: Only yields results when text IS generic. No result means text is acceptable.

        Parameters
        ----------
        error_level : str, optional
            Override default error level (default: "WARNING")

        Yields
        ------
        dict
            Validation result for each ext-link with generic text
        """
        error_level = error_level or self.params.get("descriptive_text_error_level", "WARNING")

        for ext_link in self.ext_links_model.ext_links:
            text = ext_link.get("text", "").strip()

            if not text:
                continue

            is_generic = any(phrase in text.lower() for phrase in self.GENERIC_PHRASES)

            if not is_generic:
                continue

            advice_text = _(
                'Replace generic text "{text}" in <ext-link> with descriptive text,'
                " or add @xlink:title attribute"
            )
            advice_params = {"text": text}

            parent = {
                "parent": ext_link.get("parent"),
                "parent_id": ext_link.get("parent_id"),
                "parent_article_type": ext_link.get("parent_article_type"),
                "parent_lang": ext_link.get("parent_lang"),
            }

            yield build_response(
                title="descriptive link text",
                parent=parent,
                item="ext-link",
                sub_item="text()",
                validation_type="value",
                is_valid=False,
                expected="descriptive text (not generic)",
                obtained=text,
                advice=advice_text.format(**advice_params),
                data=ext_link,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_xlink_title_when_generic(self, error_level=None):
        """
        Validate @xlink:title presence when text is generic or URL (WARNING).

        SPS Rule: When text is generic or is the URL itself, @xlink:title should
        be present with a description of the link destination.

        Note: Only yields results when @xlink:title is missing and text is
        generic or matches the URL exactly.

        Parameters
        ----------
        error_level : str, optional
            Override default error level (default: "WARNING")

        Yields
        ------
        dict
            Validation result for ext-links with generic/URL text missing @xlink:title
        """
        error_level = error_level or self.params.get("xlink_title_error_level", "WARNING")

        for ext_link in self.ext_links_model.ext_links:
            text = ext_link.get("text", "").strip()
            xlink_href = ext_link.get("xlink_href", "")
            xlink_title = ext_link.get("xlink_title")

            if not text:
                continue

            is_generic = any(phrase in text.lower() for phrase in self.GENERIC_PHRASES)

            # Exact match only — substring check causes false positives, e.g.
            # text="Nature" would match inside xlink:href="https://www.nature.com".
            is_url_text = bool(xlink_href) and text.strip() == xlink_href.strip()

            if not (is_generic or is_url_text):
                continue

            if xlink_title:
                continue

            # Two separate translatable strings avoid interpolating hard-coded
            # English words ("generic", "URL") into translated messages,
            # which was the original i18n bug (Copilot observation).
            if is_generic:
                advice_text = _(
                    'Add @xlink:title attribute to <ext-link> with generic text'
                    ' "{text}" to describe the link destination'
                )
            else:
                advice_text = _(
                    'Add @xlink:title attribute to <ext-link> where the text is'
                    ' the URL "{text}" to describe the link destination'
                )

            advice_params = {"text": text}

            parent = {
                "parent": ext_link.get("parent"),
                "parent_id": ext_link.get("parent_id"),
                "parent_article_type": ext_link.get("parent_article_type"),
                "parent_lang": ext_link.get("parent_lang"),
            }

            yield build_response(
                title="@xlink:title for generic/URL text",
                parent=parent,
                item="ext-link",
                sub_item="@xlink:title",
                validation_type="exist",
                is_valid=False,
                expected="@xlink:title attribute when text is generic or URL",
                obtained=xlink_title,
                advice=advice_text.format(**advice_params),
                data=ext_link,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )
