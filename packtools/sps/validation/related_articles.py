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
        self.related_articles = list(RelatedArticles(xml_tree).related_articles())
        self.article_type = article_and_subarticles.ArticleAndSubArticles(xml_tree).main_article_type
        self.history_events = list(article_dates.ArticleDates(xml_tree).history_dates_dict)

    def related_articles_matches_article_type_validation(self, correspondence_list=None, error_level="ERROR"):
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
        if not correspondence_list:
            raise ValidationRelatedArticleException("Function requires a list of dictionary with article type and related article types")

        expected_values_for_related_article_type = None
        for item in correspondence_list:
            if isinstance(item, dict) and item.get('article-type') == self.article_type:
                expected_values_for_related_article_type = item['related-article-types']
                break

        if expected_values_for_related_article_type:
            for related_article in self.related_articles:
                obtained_related_article = related_article.get('related-article-type')
                is_valid = obtained_related_article in expected_values_for_related_article_type
                yield format_response(
                    title='Related article type validation',
                    parent=related_article.get("parent"),
                    parent_id=related_article.get("parent_id"),
                    parent_article_type=related_article.get("parent_article_type"),
                    parent_lang=related_article.get("parent_lang"),
                    item='related-article',
                    sub_item='related-article-type',
                    validation_type='match',
                    is_valid=is_valid,
                    expected=expected_values_for_related_article_type,
                    obtained=obtained_related_article,
                    advice=f"The article-type: {self.article_type} does not match the related-article-type: "
                           f"{obtained_related_article}, provide one of the following items: "
                           f"{expected_values_for_related_article_type}",
                    data=related_article,
                    error_level=error_level
                )

    def related_articles_doi(self, error_level="ERROR"):
    """
    Class to validate individual related article elements within the XML structure.
    """
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

        for related_article in self.related_articles:
            doi = related_article.get('href')
            is_valid = doi is not None
            expected_value = doi if doi else 'A valid DOI or URI for related-article/@xlink:href'
            yield format_response(
                title='Related article doi validation',
                parent=related_article.get("parent"),
                parent_id=related_article.get("parent_id"),
                parent_article_type=related_article.get("parent_article_type"),
                parent_lang=related_article.get("parent_lang"),
                item='related-article',
                sub_item='xlink:href',
                validation_type='exist',
                is_valid=is_valid,
                expected=expected_value,
                obtained=doi,
                advice=f'Provide a valid DOI for <related-article ext-link-type="doi" id="{related_article.get("id")}" '
                       f'related-article-type="{related_article.get("related-article-type")}" /> ',
                data=related_article,
                error_level=error_level
            )

    def related_article_attributes_validation(self, error_level="ERROR"):
        for related_article in self.related_articles:
            for attrib in ("related-article-type", "id", "href", "ext-link-type"):
                if not related_article[attrib]:
                    yield format_response(
                        title='Related article attributes validation',
                        parent=related_article.get("parent"),
                        parent_id=related_article.get("parent_id"),
                        parent_article_type=related_article.get("parent_article_type"),
                        parent_lang=related_article.get("parent_lang"),
                        item='related-article',
                        sub_item=f'@{attrib}',
                        validation_type='exist',
                        is_valid=False,
                        expected=f"a value for @{attrib}",
                        obtained=None,
                        advice=f"Provide a value for @{attrib}",
                        data=related_article,
                        error_level=error_level
                    )
