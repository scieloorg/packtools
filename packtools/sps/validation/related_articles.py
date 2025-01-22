from packtools.sps.models.related_articles import Fulltext
from packtools.sps.validation.utils import (
    build_response,
    is_valid_url_format,
    validate_doi_format,
)


class RelatedArticlesValidation:
    def __init__(self, xmltree, params=None):
        self.validator = FulltextValidation(Fulltext(xmltree.find(".")), params)
        self.params = params or {}
        self.error_level = self.params.get("error_level", "ERROR")

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
            Dictionary with validation parameters:
            {
                'correspondence_list': [...],
                'ext_link_types': ['doi', 'uri'],
                'requires_related_article': ['correction', 'retraction', ...],
                'requirement_error_level': 'ERROR',
                'type_error_level': 'ERROR',
                'ext_link_type_error_level': 'ERROR',
                'uri_error_level': 'ERROR',
                'uri_format_error_level': 'ERROR',
                'doi_error_level': 'ERROR',
                'doi_format_error_level': 'ERROR',
                'id_error_level': 'ERROR'
            }
        """
        self.related_article = related_article
        self.article_type = related_article.get(
            "original_article_type"
        ) or related_article.get("parent_article_type")
        self.related_article_type = related_article.get("related-article-type")

        self.params = params or {}
        self.valid_ext_link_types = self.params.get("ext_link_types", ["doi", "uri"])
        _related = self.params.get("article-types-and-related-article-types", {}).get(
            self.article_type, {}
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

    def validate_type(self):
        """Validate if related article type matches main article type"""
        expected_values = (
            self.required_related_article_types + self.acceptable_related_article_types
        )

        obtained_type = self.related_article.get("related-article-type")

        if not expected_values:
            return build_response(
                title="Related article type",
                parent=self.related_article,
                item="related-article",
                sub_item="related-article-type",
                validation_type="match",
                is_valid=False,
                expected=expected_values,
                obtained=obtained_type,
                advice=f"The article-type: {self.article_type} does not match the related-article-type: "
                f"{obtained_type}, provide one of the following items: {expected_values}",
                data=self.related_article,
                error_level=self._get_error_level("type"),
            )

        is_valid = obtained_type in expected_values
        if not is_valid:
            return build_response(
                title="Related article type",
                parent=self.related_article,
                item="related-article",
                sub_item="related-article-type",
                validation_type="match",
                is_valid=is_valid,
                expected=expected_values,
                obtained=obtained_type,
                advice=f"The article-type: {self.article_type} does not match the related-article-type: "
                f"{obtained_type}, provide one of the following items: {expected_values}",
                data=self.related_article,
                error_level=self._get_error_level("type"),
            )

    def validate_ext_link_type(self):
        """Validate if related article has valid ext-link-type"""
        ext_link_type = self.related_article.get("ext-link-type")
        is_valid = ext_link_type in self.valid_ext_link_types

        if not is_valid:
            return build_response(
                title="Related article ext-link-type",
                parent=self.related_article,
                item="related-article",
                sub_item="ext-link-type",
                validation_type="match",
                is_valid=is_valid,
                expected=self.valid_ext_link_types,
                obtained=ext_link_type,
                advice=f'The ext-link-type should be one of {self.valid_ext_link_types} for related article with id="{self.related_article.get("id")}"',
                data=self.related_article,
                error_level=self._get_error_level("ext_link_type"),
            )

    def validate_uri(self):
        """Validate if related article has valid link (URI)"""
        ext_link_type = self.related_article.get("ext-link-type")
        if not ext_link_type == "uri":
            return

        link = self.related_article.get("href")
        if not link:
            return build_response(
                title="Related article link",
                parent=self.related_article,
                item="related-article",
                sub_item="xlink:href",
                validation_type="exist",
                is_valid=False,
                expected=f'A valid {ext_link_type.upper() if ext_link_type else "link"}',
                obtained=link,
                advice=f'Provide a valid {ext_link_type.upper() if ext_link_type else "link"} for <related-article '
                f'id="{self.related_article.get("id")}" />',
                data=self.related_article,
                error_level=self._get_error_level("uri"),
            )

        is_valid = is_valid_url_format(link)
        expected = "A valid URI format (e.g., http://example.com)"

        if not is_valid:
            return build_response(
                title="Related article link",
                parent=self.related_article,
                item="related-article",
                sub_item="xlink:href",
                validation_type="format",
                is_valid=is_valid,
                expected=expected,
                obtained=link,
                advice=(
                    None
                    if is_valid
                    else f"Invalid {ext_link_type.upper()} format for link: {link}"
                ),
                data=self.related_article,
                error_level=self._get_error_level("uri_format"),
            )

    def validate_doi(self):
        """Validate if related article has valid DOI"""
        ext_link_type = self.related_article.get("ext-link-type")
        if not ext_link_type == "doi":
            return

        link = self.related_article.get("href")
        if not link:
            return build_response(
                title="Related article doi",
                parent=self.related_article,
                item="related-article",
                sub_item="xlink:href",
                validation_type="exist",
                is_valid=False,
                expected=f'A valid {ext_link_type.upper() if ext_link_type else "link"}',
                obtained=link,
                advice=f'Provide a valid {ext_link_type.upper() if ext_link_type else "link"} for <related-article '
                f'id="{self.related_article.get("id")}" />',
                data=self.related_article,
                error_level=self.params.get("doi_error_level"),
            )

        valid = validate_doi_format(link)
        is_valid = valid and valid.get("valido")
        expected = "A valid DOI"

        if not is_valid:
            return build_response(
                title="Related article doi",
                parent=self.related_article,
                item="related-article",
                sub_item="xlink:href",
                validation_type="format",
                is_valid=is_valid,
                expected=expected,
                obtained=link,
                advice=(
                    None
                    if is_valid
                    else f"Invalid {ext_link_type.upper()} format for link: {link}"
                ),
                data=self.related_article,
                error_level=self.params.get("doi_format_error_level"),
            )

    def validate_id_presence(self):
        """Validate if related article has an ID"""
        related_id = self.related_article.get("id")
        is_valid = related_id is not None and related_id.strip() != ""
        expected = "A non-empty ID"

        if not is_valid:
            return build_response(
                title="Related article id",
                parent=self.related_article,
                item="related-article",
                sub_item="id",
                validation_type="exist",
                is_valid=is_valid,
                expected=expected,
                obtained=related_id,
                advice="Each related-article element must have a unique id attribute",
                data=self.related_article,
                error_level=self._get_error_level("id"),
            )

    def validate(self):
        """Run all validations"""
        validations = [
            self.validate_type(),
            self.validate_ext_link_type(),
            self.validate_doi() or self.validate_uri(),
            self.validate_id_presence(),
        ]
        return [v for v in validations if v is not None]


class FulltextValidation:
    """Validates related articles in a Fulltext instance"""

    def __init__(self, fulltext, params=None):
        """
        Initialize with a Fulltext instance and validation parameters

        Parameters
        ----------
        fulltext : Fulltext
            Fulltext instance to validate
        params : dict, optional
            Dictionary with validation parameters
        """
        self.fulltext = fulltext
        self.params = params or {}
        self._set_article_rules()

    def _set_article_rules(self):
        """Set article rules from params"""
        article_rules = self.params.get("article-types-and-related-article-types", {})
        article_config = article_rules.get(
            self.fulltext.parent_data["parent_article_type"], {}
        )
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
            for related in self.fulltext.related_articles
        }

        # Check if any required type is missing
        missing_types = set(self.required_types) - found_types

        if missing_types:
            error_level = self._get_error_level("requirement")
            return build_response(
                title="Required related articles",
                parent=self.fulltext.parent_data,
                item="related-article",
                sub_item=None,
                validation_type="match",
                is_valid=False,
                expected=self.required_types,
                obtained=list(found_types),
                advice=f'Article type "{self.fulltext.parent_data["parent_article_type"]}" '
                f"requires related articles of types: {list(missing_types)}",
                data={
                    "article_type": self.fulltext.parent_data["parent_article_type"],
                    "missing_types": list(missing_types),
                },
                error_level=error_level,
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
        for related in self.fulltext.related_articles:
            validator = RelatedArticleValidation(related, self.params)
            yield from validator.validate()

        # Validate each sub-article
        for subtext in self.fulltext.fulltexts:
            validator = FulltextValidation(subtext, self.params)
            yield from validator.validate()


class RelatedArticlesFulltextValidation(FulltextValidation):
    ...
