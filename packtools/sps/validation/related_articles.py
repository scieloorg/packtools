import re

from packtools.sps.models import article_and_subarticles
from packtools.sps.models.v2 import related_articles

from packtools.sps.validation.exceptions import ValidationRelatedArticleException
from packtools.sps.validation.utils import format_response


class RelatedArticlesValidation:
    def __init__(self, xmltree):
        self.related_articles = [related for related in related_articles.RelatedArticles(xmltree).related_articles()]
        self.article_type = article_and_subarticles.ArticleAndSubArticles(xmltree).main_article_type

    def related_articles_matches_article_type_validation(self, correspondence_list=None, error_level="ERROR"):
        """
        Check whether the article type attribute of the article matches the options provided in a standard list.

        XML input
        ---------
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="correction-forward" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
        <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" xlink:href="10.1590/1808-057x202090350"/>
        </article>

        Params
        ------
        correspondence_list : list of dict, such as:
            [
                {
                    'article-type': 'correction',
                    'related-article-types': ['corrected-article']
                },
                {
                    'article-type': 'retraction',
                    'related-article-types': ['retracted-article']
                }, ...
            ]

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Related article type validation',
                    'xpath': './article[@article-type] .//related-article[@related-article-type]',
                    'validation_type': 'match',
                    'response': 'OK',
                    'expected_value': ['corrected-article'],
                    'got_value': 'corrected-article',
                    'message': 'Got corrected-article, expected one of the following items: ['corrected-article'],
                    'advice': None
                }, ...
            ]
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
        Checks if there is a DOI for related articles.

        XML input
        ---------
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="correction-forward" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
        <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" xlink:href="10.1590/1808-057x202090350"/>
        </article>

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'Related article doi validation',
                    'xpath': './/related-article/@xLink:href',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': '10.1590/1808-057x202090350',
                    'got_value': '10.1590/1808-057x202090350',
                    'message': 'Got 10.1590/1808-057x202090350, expected 10.1590/1808-057x202090350',
                    'advice': None
                },...
            ]
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

    def attrib_order_in_related_article_tag(self, error_level="ERROR"):
        pattern = r'<related-article\s+(?:xmlns:xlink="http://www\.w3\.org/1999/xlink"\s+)?related-article-type="[' \
                  r'^"]*"\s+id="[^"]*"\s+ext-link-type="doi"\s+xlink:href="[^"]*"\s*/?>'

        for related_article in self.related_articles:
            full_tag = related_article.get('full_tag')
            if not re.match(pattern, full_tag):
                yield format_response(
                    title='attrib order in related article tag',
                    parent=related_article.get("parent"),
                    parent_id=related_article.get("parent_id"),
                    parent_article_type=related_article.get("parent_article_type"),
                    parent_lang=related_article.get("parent_lang"),
                    item='related-article',
                    sub_item=None,
                    validation_type='match',
                    is_valid=False,
                    expected='<related-article related-article-type="TYPE" id="ID" xlink:href="HREF" ext-link-type="doi">',
                    obtained=full_tag,
                    advice='provide the attributes in the specified order',
                    data=related_article,
                    error_level=error_level
                )
