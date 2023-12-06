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
                    'message': 'Got corrected-article, expected one of the following items: corrected-article',
                    'advice': None
                }, ...
            ]
        """
        if not correspondence_dictionary:
            raise ValidationRelatedArticleException("Function requires a dictionary with article types and related article types")
        result = []
        for related_article in self.related_articles:
            validated = self.article_type in correspondence_dictionary and correspondence_dictionary.get(self.article_type) == related_article.get('related-article-type')
            result.append(
                {
                    'title': 'Related article type validation',
                    'xpath': './article[@article-type] .//related-article[@related-article-type]',
                    'validation_type': 'match',
                    'response': 'OK' if validated else 'ERROR',
                    'expected_value': 'A valid match such as the following: {}'.format(
                        ' or '.join([f'({article}, {related})' for article, related in correspondence_dictionary.items()])
                    ),
                    'got_value': 'article-type: {}, related-article-type: {}'.format(
                        self.article_type,
                        related_article.get('related-article-type')
                    ),
                    'message': 'Got {}, expected {}'.format(
                        f'({self.article_type}, {related_article.get("related-article-type")})',
                        f' or '.join([f'({article}, {related})' for article, related in correspondence_dictionary.items()])
                    ),
                    'advice': None if validated else 'Consider replacing the article-type and related-article-type '
                                                     'with a tuple from the following list: {}'.format(
                        f' or '.join([f'({article}, {related})' for article, related in correspondence_dictionary.items()])
                    )
                }
            )
        return result

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
                    'xpath': './/related-article[@ext-link-type="doi"]',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': '10.1590/1808-057x202090350',
                    'got_value': '10.1590/1808-057x202090350',
                    'message': 'Got 10.1590/1808-057x202090350, expected 10.1590/1808-057x202090350',
                    'advice': None
                },...
            ]
        """
        result = []
        for related_article in self.related_articles:
            if related_article.get('ext-link-type') == 'doi':
                doi = related_article.get('href')
                expected_value = doi if doi else 'A valid DOI for related-article'
                result.append(
                    {
                        'title': 'Related article doi validation',
                        'xpath': './/related-article[@ext-link-type="doi"]',
                        'validation_type': 'exist',
                        'response': 'OK' if doi else 'ERROR',
                        'expected_value': expected_value,
                        'got_value': doi,
                        'message': 'Got {}, expected {}'.format(doi, expected_value),
                        'advice': None if doi else 'Provide a valid DOI for the related-article {} whith ID {}'
                        .format(related_article.get('related-article-type'), related_article.get('id'))
                    }
                )
        return result
