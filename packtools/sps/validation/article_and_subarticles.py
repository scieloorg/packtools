from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles
from packtools.sps.validation.exceptions import AffiliationValidationValidateLanguageCodeException


class ArticleLangValidation:
    def __init__(self, xmltree, language_codes_list=None):
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree).data
        self.language_codes_list = language_codes_list

    def validate_language(self, language_codes_list=None):
        """
        Params
        ------
            xml: ElementTree

        Returns
        -------
        list: dicts as:
        {
            'title': 'Article element lang attribute validation',
            'xpath': './article/@xml:lang',
            'validation_type': 'value in list',
            'response': 'OK',
            'expected_value': ['pt', 'en', 'es'],
            'got_value': 'en',
            'message': 'Got en, to research-article whose id is main, expected one item of this list: pt | en | es',
            'advice': 'XML research-article has en as language, to research-article whose id is main, expected one item
            of this list: pt | en | es'
        }
        """

        if language_codes:
            for article in self.articles:
                article_lang = article.get('lang')
                article_type = article.get('article_type')
                article_id = article.get('article_id')

                if article_id == 'main':
                    msg = '<article article-type={} xml:lang={}>'.format(article_type, article_lang)
                else:
                    msg = '<sub-article article-type={} id={} xml:lang={}>'.format(article_type, article_id, article_lang)

                item = {
                    'title': 'Article element lang attribute validation',
                    'xpath': './article/@xml:lang' if article_id == 'main' else './/sub-article/@xml:lang',
                    'validation_type': 'value in list',
                    'response': 'OK' if article_lang in language_codes else 'ERROR',
                    'expected_value': language_codes,
                    'got_value': article_lang,
                    'message': 'Got {} expected one item of this list: {}'.format(msg, " | ".join(language_codes)),
                    'advice': '{} has {} as language, expected one item of this list: {}'.format(msg, article_lang, " | ".join(language_codes))
                }
                yield item