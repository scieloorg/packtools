from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles
from packtools.sps.validation.exceptions import (
    AffiliationValidationValidateLanguageCodeException,
    ArticleValidationValidateSpecificUseException,
    ArticleValidationValidateDtdVersionException,
)


class ArticleValidation:
    def __init__(self, xmltree, language_codes_list=None, specific_use_list=None, dtd_version_list=None):
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree)
        self.language_codes_list = language_codes_list
        self.specific_use_list = specific_use_list
        self.dtd_version_list = dtd_version_list

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

        language_codes_list = language_codes_list or self.language_codes_list
        if not language_codes_list:
            raise AffiliationValidationValidateLanguageCodeException("Function requires list of language codes")
        for article in self.articles.data:
            article_lang = article.get('lang')
            article_type = article.get('article_type')
            article_id = article.get('article_id')
            validated = article_lang in language_codes_list

            if article_id == 'main':
                msg = '<article article-type={} xml:lang={}>'.format(article_type, article_lang)
            else:
                msg = '<sub-article article-type={} id={} xml:lang={}>'.format(article_type, article_id, article_lang)

            item = {
                'title': 'Article element lang attribute validation',
                'xpath': './article/@xml:lang' if article_id == 'main' else './/sub-article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'OK' if validated else 'ERROR',
                'expected_value': language_codes_list,
                'got_value': article_lang,
                'message': 'Got {} expected one item of this list: {}'.format(msg, " | ".join(language_codes_list)),
                'advice': None if validated else '{} has {} as language, expected one item of this list: {}'.format(msg, article_lang, " | ".join(language_codes_list))
            }
            yield item

    def validate(self, data):
        """
        Função que executa as validações da classe ArticleLangValidation.

        Returns:
            dict: Um dicionário contendo os resultados das validações realizadas.

        """
        return {
            'article_lang_validation': self.validate_language(data['language_codes_list'])
        }
