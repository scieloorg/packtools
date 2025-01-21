from packtools.sps.models.related_articles import RelatedItems
from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles
from packtools.sps.validation.exceptions import ValidationRelatedArticleException
from packtools.sps.validation.utils import build_response


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
        self.error_level = self.params.get('error_level', 'ERROR')

    def validate_related_article_types(self):
        """
        Validate if article type matches related article types from correspondence list.

        Returns
        -------
        generator
            Yields validation results for each related article
        """
        correspondence_list = self.params.get('correspondence_list')
        if not correspondence_list:
            raise ValidationRelatedArticleException(
                "Validation requires 'correspondence_list' parameter with article type and related article types"
            )

        expected_values = None
        for item in correspondence_list:
            if isinstance(item, dict) and item.get('article-type') == self.article_type:
                expected_values = item['related-article-types']
                break

        if expected_values:
            for related_article in self.related_articles:
                obtained_type = related_article.get('related-article-type')
                is_valid = obtained_type in expected_values

                yield build_response(
                    title='Related article type validation',
                    parent=related_article,
                    item='related-article',
                    sub_item='related-article-type',
                    validation_type='match',
                    is_valid=is_valid,
                    expected=expected_values,
                    obtained=obtained_type,
                    advice=f"The article-type: {self.article_type} does not match the related-article-type: "
                          f"{obtained_type}, provide one of the following items: {expected_values}",
                    data=related_article,
                    error_level=self.error_level
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
            doi = related_article.get('href')
            is_valid = doi is not None
            expected = doi if doi else 'A valid DOI or URI for related-article/@xlink:href'

            yield build_response(
                title='Related article doi validation',
                parent=related_article,
                item='related-article',
                sub_item='xlink:href',
                validation_type='exist',
                is_valid=is_valid,
                expected=expected,
                obtained=doi,
                advice=f'Provide a valid DOI for <related-article ext-link-type="doi" '
                      f'id="{related_article.get("id")}" related-article-type='
                      f'"{related_article.get("related-article-type")}" />',
                data=related_article,
                error_level=self.error_level
            )