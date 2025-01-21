from packtools.sps.models.related_articles import RelatedItems
from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles
from packtools.sps.validation.exceptions import ValidationRelatedArticleException
from packtools.sps.validation.utils import (
    build_response,
    is_valid_url_format,
    validate_doi_format,
)


class RelatedArticlesValidation:
    def __init__(self, xmltree, params=None):
        """Initialize with xmltree and validation parameters

        Parameters
        ----------
        xmltree : etree
            XML tree to be validated
        params : dict, optional
            Dictionary containing validation parameters:
            {
                'correspondence_list': [
                    {
                        'article-type': 'correction',
                        'related-article-types': ['corrected-article']
                    },
                    {
                        'article-type': 'retraction',
                        'related-article-types': ['retracted-article']
                    }
                ],
                'error_level': 'ERROR'  # Default error level for validations
            }
        """
        self.related_articles = [
            related for related in RelatedItems(xmltree).related_articles
        ]
        self.article_type = ArticleAndSubArticles(xmltree).main_article_type
        self.params = params or {}
        self.error_level = self.params.get("error_level", "ERROR")

    def validate_related_article_types(self):
        """
        Validate if article type matches related article types from correspondence list.

        Returns
        -------
        generator
            Yields validation results for each related article
        """
        correspondence_list = self.params.get("correspondence_list")
        if not correspondence_list:
            raise ValidationRelatedArticleException(
                "Validation requires 'correspondence_list' parameter with article type and related article types"
            )

        expected_values = None
        for item in correspondence_list:
            if isinstance(item, dict) and item.get("article-type") == self.article_type:
                expected_values = item["related-article-types"]
                break

        if expected_values:
            for related_article in self.related_articles:
                obtained_type = related_article.get("related-article-type")
                is_valid = obtained_type in expected_values

                yield build_response(
                    title="Related article type validation",
                    parent=related_article,
                    item="related-article",
                    sub_item="related-article-type",
                    validation_type="match",
                    is_valid=is_valid,
                    expected=expected_values,
                    obtained=obtained_type,
                    advice=f"The article-type: {self.article_type} does not match the related-article-type: "
                    f"{obtained_type}, provide one of the following items: {expected_values}",
                    data=related_article,
                    error_level=self.error_level,
                )

    def validate_related_article_doi(self):
        """
        Validate if related articles have DOIs.

        Returns
        -------
        generator
            Yields validation results for each related article's DOI
        """
        for related_article in self.related_articles:
            doi = related_article.get("href")
            is_valid = doi is not None
            expected = (
                doi if doi else "A valid DOI or URI for related-article/@xlink:href"
            )

            yield build_response(
                title="Related article doi validation",
                parent=related_article,
                item="related-article",
                sub_item="xlink:href",
                validation_type="exist",
                is_valid=is_valid,
                expected=expected,
                obtained=doi,
                advice=f'Provide a valid DOI for <related-article ext-link-type="doi" '
                f'id="{related_article.get("id")}" related-article-type='
                f'"{related_article.get("related-article-type")}" />',
                data=related_article,
                error_level=self.error_level,
            )


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
                title="Related article type validation",
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

        return build_response(
            title="Related article type validation",
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

        return build_response(
            title="Related article ext-link-type validation",
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
                title="Related article link validation",
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

        return build_response(
            title="Related article link validation",
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
                title="Related article doi validation",
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

        return build_response(
            title="Related article doi validation",
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

        return build_response(
            title="Related article id validation",
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
