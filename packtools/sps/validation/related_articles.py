from packtools.sps.models import (
    related_articles,
    article_and_subarticles
)

from packtools.sps.validation.exceptions import ValidationRelatedArticleException


class RelatedArticlesValidation:
    def __init__(self, xmltree):
        self.related_articles = [related for related in related_articles.RelatedItems(xmltree).related_articles]
        self.article_type = article_and_subarticles.ArticleAndSubArticles(xmltree).main_article_type

    def related_articles_matches_article_type_validation(self, correspondence_list=None):
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

        article_type_match = {}
        for item in correspondence_list:
            if isinstance(item, dict) and item.get('article-type') == self.article_type:
                article_type_match = item
                break

        if article_type_match:
            for related_article in self.related_articles:
                validated = related_article.get('related-article-type') in article_type_match.get('related-article-types') or []
                yield {
                        'title': 'Related article type validation',
                        'xpath': './article[@article-type] .//related-article[@related-article-type]',
                        'validation_type': 'match',
                        'response': 'OK' if validated else 'ERROR',
                        'expected_value': article_type_match.get('related-article-types'),
                        'got_value': related_article.get('related-article-type'),
                        'message': 'Got {}, expected {}'.format(
                            related_article.get('related-article-type'),
                            'one of the following items: {}'.format(article_type_match.get('related-article-types'))
                        ),
                        'advice': None if validated else 'The article-type: {} does not match the '
                                                         'related-article-type: {}, provide '
                                                         'one of the following items: {}'.format(
                            self.article_type,
                            related_article.get('related-article-type'),
                            article_type_match.get('related-article-types')
                        )
                    }

    def related_articles_doi(self):
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
            expected_value = doi if doi else 'A valid DOI or URI for related-article/@xlink:href'
            yield {
                    'title': 'Related article doi validation',
                    'xpath': './/related-article/@xlink:href',
                    'validation_type': 'exist',
                    'response': 'OK' if doi else 'ERROR',
                    'expected_value': expected_value,
                    'got_value': doi,
                    'message': 'Got {}, expected {}'.format(doi, expected_value[0].lower() + expected_value[1:]),
                    'advice': None if doi else 'Provide a valid DOI for the related-article {} which ID is {}'
                    .format(related_article.get('related-article-type'), related_article.get('id'))
                }

