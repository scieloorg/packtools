"""
Validation for related-article elements according to SPS 1.10 specification.

Implements validations for related article elements to ensure:
- Mandatory attributes are present (@related-article-type, @id, @ext-link-type, @xlink:href)
- Attribute values are in allowed lists
- Preference for DOI over URI is followed
- Attribute order follows specification

Reference: https://docs.google.com/document/d/1GTv4Inc2LS_AXY-ToHT3HmO66UT0VAHWJNOIqzBNSgA/edit?tab=t.0#heading=h.relatedarticle
"""
import gettext

from packtools.sps.models.related_articles import FulltextRelatedArticles
from packtools.sps.validation.utils import (
    build_response,
    is_valid_url_format,
    validate_doi_format,
)

_ = gettext.gettext

ALLOWED_RELATED_ARTICLE_TYPES = [
    "corrected-article",
    "correction-forward",
    "retracted-article",
    "retraction-forward",
    "partial-retraction",
    "addended-article",
    "addendum",
    "expression-of-concern",
    "object-of-concern",
    "commentary-article",
    "commentary",
    "reply",
    "letter",
    "reviewed-article",
    "reviewer-report",
    "preprint",
    "peer-reviewed-material",
]

ALLOWED_EXT_LINK_TYPES = ["doi", "uri"]

URI_ALLOWED_RELATED_ARTICLE_TYPES = ["reviewer-report", "preprint"]


class XMLRelatedArticlesValidation:
    def __init__(self, xmltree, params=None):
        self.validator = FulltextRelatedArticlesValidation(xmltree.find("."), params)
        self.params = params or {}

    def validate(self):
        yield from self.validator.validate()


class RelatedArticleValidation:
    """Validates a single related-article element"""

    def __init__(self, related_article, params=None):
        """
        Parameters
        ----------
        related_article : dict
            Dictionary with related article data including parent_article_type
        params : dict, optional
            Dictionary with validation parameters
        """
        self.related_article = related_article
        self.original_article_type = related_article["original_article_type"]
        self.related_article_type = related_article.get("related-article-type")

        self.params = params or {}
        self.valid_ext_link_types = self.params.get("ext_link_types", ALLOWED_EXT_LINK_TYPES)
        _related = self.params.get("article-types-and-related-article-types", {}).get(
            self.original_article_type, {}
        )
        self.required_related_article_types = (
            _related.get("required_related_article_types") or []
        )
        self.acceptable_related_article_types = (
            _related.get("acceptable_related_article_types") or []
        )

    def _get_error_level(self, validation_type):
        """
        Get error level for specific validation type from params

        Parameters
        ----------
        validation_type : str
            Type of validation being performed

        Returns
        -------
        str
            Error level for the validation type
        """
        error_level_key = f"{validation_type}_error_level"
        return self.params.get(error_level_key, "CRITICAL")

    def validate_related_article_type_presence(self):
        """
        Validate presence of @related-article-type attribute (CRITICAL).

        SPS Rule: @related-article-type is mandatory in all <related-article> elements.

        Returns
        -------
        dict or None
            Validation result if attribute is missing or empty, None if valid
        """
        error_level = self._get_error_level("related_article_type_presence")
        obtained = self.related_article.get("related-article-type")
        is_valid = obtained is not None and obtained.strip() != ""

        advice_text = _(
            'Add @related-article-type attribute to <related-article>.'
            ' Valid values: {allowed_values}'
        )
        advice_params = {
            "allowed_values": ", ".join(ALLOWED_RELATED_ARTICLE_TYPES),
        }

        if not is_valid:
            return build_response(
                title="Related article type presence",
                parent=self.related_article,
                item="related-article",
                sub_item="@related-article-type",
                validation_type="exist",
                is_valid=is_valid,
                expected="@related-article-type attribute present",
                obtained=obtained,
                advice=advice_text.format(**advice_params),
                data=self.related_article,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_ext_link_type_presence(self):
        """
        Validate presence of @ext-link-type attribute (CRITICAL).

        SPS Rule: @ext-link-type is mandatory in all <related-article> elements.

        Returns
        -------
        dict or None
            Validation result if attribute is missing or empty, None if valid
        """
        error_level = self._get_error_level("ext_link_type_presence")
        obtained = self.related_article.get("ext-link-type")
        is_valid = obtained is not None and obtained.strip() != ""

        advice_text = _(
            'Add @ext-link-type attribute to <related-article>.'
            ' Valid values: {allowed_values}'
        )
        advice_params = {
            "allowed_values": ", ".join(ALLOWED_EXT_LINK_TYPES),
        }

        if not is_valid:
            return build_response(
                title="Related article ext-link-type presence",
                parent=self.related_article,
                item="related-article",
                sub_item="@ext-link-type",
                validation_type="exist",
                is_valid=is_valid,
                expected="@ext-link-type attribute present",
                obtained=obtained,
                advice=advice_text.format(**advice_params),
                data=self.related_article,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_related_article_type_value(self):
        """
        Validate @related-article-type value is in allowed list (ERROR).

        SPS Rule: @related-article-type must be one of the allowed values.
        Comparison is case-sensitive.

        Returns
        -------
        dict or None
            Validation result if value is invalid, None if valid or attribute missing
        """
        obtained = self.related_article.get("related-article-type")
        if not obtained or not obtained.strip():
            return None

        error_level = self._get_error_level("related_article_type_value")
        is_valid = obtained in ALLOWED_RELATED_ARTICLE_TYPES

        advice_text = _(
            'Value "{obtained}" is not allowed for @related-article-type.'
            ' Valid values: {allowed_values}'
        )
        advice_params = {
            "obtained": obtained,
            "allowed_values": ", ".join(ALLOWED_RELATED_ARTICLE_TYPES),
        }

        if not is_valid:
            return build_response(
                title="Related article type value",
                parent=self.related_article,
                item="related-article",
                sub_item="@related-article-type",
                validation_type="value in list",
                is_valid=is_valid,
                expected=ALLOWED_RELATED_ARTICLE_TYPES,
                obtained=obtained,
                advice=advice_text.format(**advice_params),
                data=self.related_article,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_xlink_href_presence(self):
        """
        Validate presence of @xlink:href attribute (ERROR).

        SPS Rule: @xlink:href is mandatory in all <related-article> elements.

        Returns
        -------
        dict or None
            Validation result if attribute is missing or empty, None if valid
        """
        error_level = self._get_error_level("xlink_href_presence")
        obtained = self.related_article.get("href")
        is_valid = obtained is not None and obtained.strip() != ""

        advice_text = _(
            'Add @xlink:href attribute to <related-article>.'
            ' Provide a valid DOI or URI.'
        )
        advice_params = {}

        if not is_valid:
            return build_response(
                title="Related article xlink:href presence",
                parent=self.related_article,
                item="related-article",
                sub_item="@xlink:href",
                validation_type="exist",
                is_valid=is_valid,
                expected="@xlink:href attribute present",
                obtained=obtained,
                advice=advice_text.format(**advice_params),
                data=self.related_article,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_ext_link_type_value(self):
        """
        Validate @ext-link-type value is in allowed list (ERROR).

        SPS Rule: @ext-link-type must be "doi" or "uri".
        Comparison is case-sensitive.

        Returns
        -------
        dict or None
            Validation result if value is invalid, None if valid or attribute missing
        """
        obtained = self.related_article.get("ext-link-type")
        if not obtained or not obtained.strip():
            return None

        error_level = self._get_error_level("ext_link_type_value")
        is_valid = obtained in ALLOWED_EXT_LINK_TYPES

        advice_text = _(
            'Value "{obtained}" is not allowed for @ext-link-type.'
            ' Valid values: {allowed_values}'
        )
        advice_params = {
            "obtained": obtained,
            "allowed_values": ", ".join(ALLOWED_EXT_LINK_TYPES),
        }

        if not is_valid:
            return build_response(
                title="Related article ext-link-type value",
                parent=self.related_article,
                item="related-article",
                sub_item="@ext-link-type",
                validation_type="value in list",
                is_valid=is_valid,
                expected=ALLOWED_EXT_LINK_TYPES,
                obtained=obtained,
                advice=advice_text.format(**advice_params),
                data=self.related_article,
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_doi_preference(self):
        """
        Validate preference for DOI over URI (WARNING).

        SPS Rule: @ext-link-type should be "doi" by default. Only
        "reviewer-report" and "preprint" types are allowed to use "uri".
        For all other types, using "uri" produces a WARNING.

        Returns
        -------
        dict or None
            Validation result if uri is used when doi should be preferred,
            None if valid or not applicable
        """
        ext_link_type = self.related_article.get("ext-link-type")
        related_type = self.related_article.get("related-article-type")

        if ext_link_type != "uri":
            return None

        if related_type in URI_ALLOWED_RELATED_ARTICLE_TYPES:
            return None

        error_level = self._get_error_level("doi_preference")

        advice_text = _(
            'For @related-article-type="{related_type}", use @ext-link-type="doi".'
            ' Value "uri" is only recommended for: {uri_types}'
        )
        advice_params = {
            "related_type": related_type or "",
            "uri_types": ", ".join(URI_ALLOWED_RELATED_ARTICLE_TYPES),
        }

        return build_response(
            title="Related article doi preference",
            parent=self.related_article,
            item="related-article",
            sub_item="@ext-link-type",
            validation_type="value",
            is_valid=False,
            expected="doi",
            obtained=ext_link_type,
            advice=advice_text.format(**advice_params),
            data=self.related_article,
            error_level=error_level,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_type(self):
        """Validate if related article type matches main article type"""
        expected_values = (
            self.required_related_article_types + self.acceptable_related_article_types
        )

        obtained_type = self.related_article.get("related-article-type")

        if not expected_values:
            advice_text = _(
                'The article-type "{article_type}" does not match the'
                ' related-article-type "{obtained_type}".'
                ' Provide one of: {expected_values}'
            )
            advice_params = {
                "article_type": self.original_article_type,
                "obtained_type": obtained_type or "",
                "expected_values": str(expected_values),
            }
            return build_response(
                title="Related article type",
                parent=self.related_article,
                item="related-article",
                sub_item="related-article-type",
                validation_type="match",
                is_valid=False,
                expected=expected_values,
                obtained=obtained_type,
                advice=advice_text.format(**advice_params),
                data=self.related_article,
                error_level=self._get_error_level("type"),
                advice_text=advice_text,
                advice_params=advice_params,
            )

        is_valid = obtained_type in expected_values
        if not is_valid:
            advice_text = _(
                'The article-type "{article_type}" does not match the'
                ' related-article-type "{obtained_type}".'
                ' Provide one of: {expected_values}'
            )
            advice_params = {
                "article_type": self.original_article_type,
                "obtained_type": obtained_type or "",
                "expected_values": str(expected_values),
            }
            return build_response(
                title="Related article type",
                parent=self.related_article,
                item="related-article",
                sub_item="related-article-type",
                validation_type="match",
                is_valid=is_valid,
                expected=expected_values,
                obtained=obtained_type,
                advice=advice_text.format(**advice_params),
                data=self.related_article,
                error_level=self._get_error_level("type"),
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_ext_link_type(self):
        """Validate if related article has valid ext-link-type"""
        ext_link_type = self.related_article.get("ext-link-type")
        is_valid = ext_link_type in self.valid_ext_link_types

        if not is_valid:
            advice_text = _(
                'The @ext-link-type should be one of {allowed_values}'
                ' for related article with id="{related_id}"'
            )
            advice_params = {
                "allowed_values": str(self.valid_ext_link_types),
                "related_id": self.related_article.get("id") or "",
            }
            return build_response(
                title="Related article ext-link-type",
                parent=self.related_article,
                item="related-article",
                sub_item="ext-link-type",
                validation_type="match",
                is_valid=is_valid,
                expected=self.valid_ext_link_types,
                obtained=ext_link_type,
                advice=advice_text.format(**advice_params),
                data=self.related_article,
                error_level=self._get_error_level("ext_link_type"),
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_uri(self):
        """Validate if related article has valid link (URI)"""
        ext_link_type = self.related_article.get("ext-link-type")
        if not ext_link_type == "uri":
            return

        link = self.related_article.get("href")
        if not link:
            advice_text = _(
                'Provide a valid {link_type} for <related-article'
                ' id="{related_id}" />'
            )
            advice_params = {
                "link_type": ext_link_type.upper() if ext_link_type else "link",
                "related_id": self.related_article.get("id") or "",
            }
            return build_response(
                title="Related article link",
                parent=self.related_article,
                item="related-article",
                sub_item="xlink:href",
                validation_type="exist",
                is_valid=False,
                expected=f'A valid {ext_link_type.upper() if ext_link_type else "link"}',
                obtained=link,
                advice=advice_text.format(**advice_params),
                data=self.related_article,
                error_level=self._get_error_level("uri"),
                advice_text=advice_text,
                advice_params=advice_params,
            )

        is_valid = is_valid_url_format(link)
        expected = "A valid URI format (e.g., http://example.com)"

        if not is_valid:
            advice_text = _(
                'Invalid {link_type} format for link: {link}'
            )
            advice_params = {
                "link_type": ext_link_type.upper(),
                "link": link,
            }
            return build_response(
                title="Related article link",
                parent=self.related_article,
                item="related-article",
                sub_item="xlink:href",
                validation_type="format",
                is_valid=is_valid,
                expected=expected,
                obtained=link,
                advice=advice_text.format(**advice_params),
                data=self.related_article,
                error_level=self._get_error_level("uri_format"),
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_doi(self):
        """Validate if related article has valid DOI"""
        ext_link_type = self.related_article.get("ext-link-type")
        if not ext_link_type == "doi":
            return

        link = self.related_article.get("href")
        if not link:
            advice_text = _(
                'Provide a valid {link_type} for <related-article'
                ' id="{related_id}" />'
            )
            advice_params = {
                "link_type": ext_link_type.upper() if ext_link_type else "link",
                "related_id": self.related_article.get("id") or "",
            }
            return build_response(
                title="Related article doi",
                parent=self.related_article,
                item="related-article",
                sub_item="xlink:href",
                validation_type="exist",
                is_valid=False,
                expected=f'A valid {ext_link_type.upper() if ext_link_type else "link"}',
                obtained=link,
                advice=advice_text.format(**advice_params),
                data=self.related_article,
                error_level=self.params.get("doi_error_level"),
                advice_text=advice_text,
                advice_params=advice_params,
            )

        valid = validate_doi_format(link)
        is_valid = valid and valid.get("valido")
        expected = "A valid DOI"

        if not is_valid:
            advice_text = _(
                'Invalid {link_type} format for link: {link}'
            )
            advice_params = {
                "link_type": ext_link_type.upper(),
                "link": link,
            }
            return build_response(
                title="Related article doi",
                parent=self.related_article,
                item="related-article",
                sub_item="xlink:href",
                validation_type="format",
                is_valid=is_valid,
                expected=expected,
                obtained=link,
                advice=advice_text.format(**advice_params),
                data=self.related_article,
                error_level=self.params.get("doi_format_error_level"),
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_id_presence(self):
        """
        Validate presence of @id attribute (CRITICAL).

        SPS Rule: @id is mandatory in all <related-article> elements.

        Returns
        -------
        dict or None
            Validation result if attribute is missing or empty, None if valid
        """
        related_id = self.related_article.get("id")
        is_valid = related_id is not None and related_id.strip() != ""

        if not is_valid:
            advice_text = _(
                'Add @id attribute to <related-article>.'
                ' The @id must be a non-empty unique identifier.'
            )
            advice_params = {}
            return build_response(
                title="Related article id",
                parent=self.related_article,
                item="related-article",
                sub_item="id",
                validation_type="exist",
                is_valid=is_valid,
                expected="A non-empty ID",
                obtained=related_id,
                advice=advice_text.format(**advice_params),
                data=self.related_article,
                error_level=self._get_error_level("id"),
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_attrib_order(self):
        """
        Recommend attribute order (INFO).

        SPS Rule: Attributes should follow the order:
        @related-article-type, @id, @xlink:href, @ext-link-type

        Returns
        -------
        dict or None
            Validation result if order is wrong, None if correct or not configured
        """
        expected_order = self.params.get("attrib_order")
        if not expected_order:
            return

        order = self.related_article.get("attribs")
        if not order:
            return

        if list(order) != list(expected_order):
            advice_text = _(
                'Set related-article attributes in this order: {expected_order}'
            )
            advice_params = {
                "expected_order": str(expected_order),
            }
            return build_response(
                title="Related article attribute order",
                parent=self.related_article,
                item="related-article",
                sub_item="attributes",
                validation_type="value",
                is_valid=False,
                expected=expected_order,
                obtained=list(order),
                advice=advice_text.format(**advice_params),
                data=self.related_article,
                error_level=self.params.get("attrib_order_error_level", "INFO"),
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate(self):
        """Run all validations"""
        validations = [
            self.validate_related_article_type_presence(),
            self.validate_ext_link_type_presence(),
            self.validate_related_article_type_value(),
            self.validate_ext_link_type_value(),
            self.validate_xlink_href_presence(),
            self.validate_doi_preference(),
            self.validate_attrib_order(),
            self.validate_type(),
            self.validate_ext_link_type(),
            self.validate_doi() or self.validate_uri(),
            self.validate_id_presence(),
        ]
        return [v for v in validations if v is not None]


class FulltextRelatedArticlesValidation:
    """Validates related articles in a FulltextRelatedArticles instance"""

    def __init__(self, node, params=None):
        """
        Initialize with a FulltextRelatedArticles instance and validation parameters

        Parameters
        ----------
        fulltext : FulltextRelatedArticles
            FulltextRelatedArticles instance to validate
        params : dict, optional
            Dictionary with validation parameters
        """
        self.obj = FulltextRelatedArticles(node)
        self.params = params or {}
        self._set_article_rules()

    def _set_article_rules(self):
        """Set article rules from params"""
        article_rules = self.params.get("article-types-and-related-article-types", {})
        original_article_type = self.obj.original_article_type
        article_config = article_rules.get(original_article_type) or {}
        self.required_types = article_config.get("required_related_article_types", [])
        self.acceptable_types = article_config.get(
            "acceptable_related_article_types", []
        )

    def _get_error_level(self, validation_type):
        """Get error level for specific validation type"""
        error_level_key = f"{validation_type}_error_level"
        return self.params.get(error_level_key, "CRITICAL")

    def validate_presence_of_required_related_articles(self):
        """
        Validate if required related articles are present

        Returns
        -------
        dict or None
            Validation result if article type requires related articles,
            None otherwise
        """
        if not self.required_types:
            return None

        # Get all related-article-types present in the document
        found_types = {
            related.get("related-article-type")
            for related in self.obj.related_articles
        }

        # Check if any required type is missing
        missing_types = set(self.required_types) - found_types

        if missing_types:
            error_level = self._get_error_level("requirement")
            advice_text = _(
                'Article type "{article_type}" requires related articles'
                ' of types: {missing_types}'
            )
            advice_params = {
                "article_type": self.obj.original_article_type,
                "missing_types": str(list(missing_types)),
            }
            return build_response(
                title="Required related articles",
                parent=self.obj.parent_data,
                item="related-article",
                sub_item=None,
                validation_type="match",
                is_valid=False,
                expected=self.required_types,
                obtained=list(found_types),
                advice=advice_text.format(**advice_params),
                data={
                    "article_type": self.obj.original_article_type,
                    "missing_types": list(missing_types),
                },
                error_level=error_level,
                advice_text=advice_text,
                advice_params=advice_params,
            )

        return None

    def validate(self):
        """
        Validate each related article

        Returns
        -------
        list
            List of validation results
        """
        # First check if required related articles are present
        if presence_result := self.validate_presence_of_required_related_articles():
            yield presence_result

        # Then validate each related article
        for related in self.obj.related_articles:
            validator = RelatedArticleValidation(related, self.params)
            yield from validator.validate()

        # Validate each sub-article
        for subtext in self.obj.fulltexts:
            validator = FulltextRelatedArticlesValidation(subtext.node, self.params)
            yield from validator.validate()
