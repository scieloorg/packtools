import re

from packtools.sps.models.v2.related_articles import RelatedArticles
from packtools.sps.models import article_dates
from packtools.sps.validation.exceptions import ValidationRelatedArticleException
from packtools.sps.validation.utils import format_response


class RelatedArticlesValidation:
    """
    Class to validate related articles in an XML tree, ensuring the article type matches
    predefined correspondence rules and other criteria like DOI presence and attribute order.
    """

    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.related_articles = list(RelatedArticles(xml_tree).related_articles())

    def validate(
        self,
        correspondence_dict=None,
        absence_error_level="ERROR",
        match_error_level="ERROR",
        doi_error_level="ERROR",
        order_error_level="ERROR",
        date_error_level="ERROR",
    ):
        """
        Validate related articles in the XML tree against correspondence rules for article types.

        Parameters
        ----------
        correspondence_dict : dict
            Dictionary mapping article types to valid related article types, like:
            "correspondence_dict": {
                "research-article": ["retraction-forward", "partial-retraction", "correction-forward", "addendum"],
                "retraction": ["retracted-article", "retraction-forward"],
                "partial-retraction": ["retracted-article", "partial-retraction"],
                "correction": ["corrected-article"],
                "addendum": ["article"]
            }
        absence_error_level : str, optional
            Error level when related-article is missing (default is "ERROR").
        match_error_level : str, optional
            Error level when related-article type does not match expected type (default is "ERROR").
        doi_error_level : str, optional
            Error level for DOI validation (default is "ERROR").
        order_error_level : str, optional
            Error level for attribute order validation (default is "ERROR").
        date_error_level : str, optional
            Error level for date validation (default is "ERROR").

        Yields
        ------
        dict
            A validation response for each check performed.

        Raises
        ------
        ValidationRelatedArticleException
            If the correspondence_dict is not provided.
        """
        if not correspondence_dict:
            raise ValidationRelatedArticleException(
                "Function requires a dictionary with article type and related article types"
            )

        if not self.related_articles:
            parent_article_type = self.xml_tree.get("article-type")
            yield format_response(
                title="Related article type validation",
                parent="article",
                parent_id=None,
                parent_article_type=parent_article_type,
                parent_lang=self.xml_tree.get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                item="related-article",
                sub_item="related-article-type",
                validation_type="match",
                is_valid=False,
                expected=correspondence_dict[parent_article_type],
                obtained=self.related_articles,
                advice=f"The article-type: {parent_article_type} does not match the related-article-type: "
                f"{correspondence_dict[parent_article_type]}, provide one of the following items: "
                f"{correspondence_dict[parent_article_type]}",
                data=None,
                error_level=absence_error_level,
            )
        else:
            history_events = article_dates.HistoryDates(self.xml_tree).history_dates()
            for related_article in self.related_articles:
                related_article_validation = RelatedArticleValidation(related_article)
                if related_article_types := correspondence_dict.get(
                    related_article.get("parent_article_type")
                ):
                    yield related_article_validation.validate_related_article_matches_article_type(
                        expected_related_article_types=related_article_types,
                        error_level=match_error_level,
                    )
                    yield related_article_validation.validate_related_article_doi(
                        error_level=doi_error_level
                    )
                    yield related_article_validation.validate_attrib_order_in_related_article_tag(
                        error_level=order_error_level
                    )
                    yield related_article_validation.validate_history_date(
                        expected_date_type=None,
                        history_events=history_events,
                        error_level=date_error_level,
                    )


class RelatedArticleValidation:
    """
    Class to validate individual related article elements within the XML structure.
    """

    def __init__(self, related_article_dict):
        """
        Initialize the RelatedArticleValidation class.

        Parameters
        ----------
        related_article_dict : dict
            Dictionary representing the attributes of a related article element in the XML, like:
            {
                'ext-link-type': 'doi',
                'href': '10.1590/s1413-65382620000100001',
                'id': 'RA1',
                'parent': 'article',
                'parent_article_type': 'correction',
                'parent_id': None,
                'parent_lang': 'pt',
                'related-article-type': 'corrected-article',
                'text': '',
                'full_tag': '<related-article id="RA1" related-article-type="corrected-article" ext-link-type="doi" '
                            'xlink:href="10.1590/s1413-65382620000100001"/>',
            }
        """
        self.related_article_dict = related_article_dict

    def validate_related_article_matches_article_type(
        self, expected_related_article_types=None, error_level="ERROR"
    ):
        """
        Validate that the related-article type matches the expected types based on the article type.

        Parameters
        ----------
        expected_related_article_types : list of str, optional
            A list of valid related-article types.
        error_level : str, optional
            The error level for the validation (default is "ERROR").

        Returns
        -------
        dict
            Validation response indicating whether the related-article type matches the expected types.

        Raises
        ------
        ValidationRelatedArticleException
            If the expected_related_article_types is not provided.
        """
        if not expected_related_article_types:
            raise ValidationRelatedArticleException(
                "Function requires a list of expected related article types"
            )

        obtained_related_article = self.related_article_dict.get("related-article-type")
        is_valid = obtained_related_article in expected_related_article_types
        return format_response(
            title="Related article type validation",
            parent=self.related_article_dict.get("parent"),
            parent_id=self.related_article_dict.get("parent_id"),
            parent_article_type=self.related_article_dict.get("parent_article_type"),
            parent_lang=self.related_article_dict.get("parent_lang"),
            item="related-article",
            sub_item="related-article-type",
            validation_type="match",
            is_valid=is_valid,
            expected=expected_related_article_types,
            obtained=obtained_related_article,
            advice=f"The article-type: {self.related_article_dict.get('parent_article_type')} does not match the related-article-type: "
            f"{obtained_related_article}, provide one of the following items: "
            f"{expected_related_article_types}",
            data=self.related_article_dict,
            error_level=error_level,
        )

    def validate_related_article_doi(self, error_level="ERROR"):
        doi = self.related_article_dict.get("href")
        is_valid = doi is not None
        expected_value = (
            doi if doi else "A valid DOI or URI for related-article/@xlink:href"
        )
        return format_response(
            title="Related article doi validation",
            parent=self.related_article_dict.get("parent"),
            parent_id=self.related_article_dict.get("parent_id"),
            parent_article_type=self.related_article_dict.get("parent_article_type"),
            parent_lang=self.related_article_dict.get("parent_lang"),
            item="related-article",
            sub_item="xlink:href",
            validation_type="exist",
            is_valid=is_valid,
            expected=expected_value,
            obtained=doi,
            advice=f'Provide a valid DOI for <related-article ext-link-type="doi" id="{self.related_article_dict.get("id")}" '
            f'related-article-type="{self.related_article_dict.get("related-article-type")}" /> ',
            data=self.related_article_dict,
            error_level=error_level,
        )

    def validate_attrib_order_in_related_article_tag(self, error_level="ERROR"):
        pattern = r'<related-article\s+(?:xmlns:xlink="http://www\.w3\.org/1999/xlink"\s+)?related-article-type="[^"]*"\s+id="[^"]*"\s+ext-link-type="doi"\s+xlink:href="[^"]*"\s*/?>'
        full_tag = self.related_article_dict.get("full_tag")

        if not re.match(pattern, full_tag):
            return format_response(
                title="attrib order in related article tag",
                parent=self.related_article_dict.get("parent"),
                parent_id=self.related_article_dict.get("parent_id"),
                parent_article_type=self.related_article_dict.get(
                    "parent_article_type"
                ),
                parent_lang=self.related_article_dict.get("parent_lang"),
                item="related-article",
                sub_item=None,
                validation_type="match",
                is_valid=False,
                expected='<related-article related-article-type="TYPE" id="ID" xlink:href="HREF" ext-link-type="doi">',
                obtained=full_tag,
                advice="Provide the attributes in the specified order",
                data=self.related_article_dict,
                error_level=error_level,
            )

    def validate_history_date(
        self, expected_date_type, history_events, error_level="ERROR"
    ):
        """
        Validate that the expected history date type exists within the related-article history events.

        Parameters
        ----------
        expected_date_type : str
            The expected date type (e.g., 'received', 'accepted').
        history_events : dict
            Dictionary of historical events and their associated dates, like:
            {
                "accepted": {
                    "day": "06",
                    "month": "06",
                    "type": "accepted",
                    "year": "1998",
                },
                "corrected": {
                    "day": "01",
                    "month": "06",
                    "type": "corrected",
                    "year": "2012",
                },...
            }
        error_level : str, optional
            The error level for the validation (default is "ERROR").

        Returns
        -------
        dict or None
            Validation response indicating whether the expected date type is present, or None if not applicable.
        """
        if not expected_date_type:
            return

        if expected_date_type not in history_events:
            return format_response(
                title="history date",
                parent=self.related_article_dict.get("parent"),
                parent_id=self.related_article_dict.get("parent_id"),
                parent_article_type=self.related_article_dict.get(
                    "parent_article_type"
                ),
                parent_lang=self.related_article_dict.get("parent_lang"),
                item="related-article / date",
                sub_item=f'@related-article-type={self.related_article_dict.get("related-article-type")} / @date-type={expected_date_type}',
                validation_type="exist",
                is_valid=False,
                expected=expected_date_type,
                obtained=history_events,
                advice=f"Provide the publication date of the {expected_date_type}",
                data=history_events,
                error_level=error_level,
            )
