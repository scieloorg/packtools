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

    def validate_specific_use(self, specific_use_list=None):
        """
        Params
        ------
            xml: ElementTree

        Returns
        -------
        list: dicts as:
        {
            'title': 'Article element specific-use attribute validation',
            'xpath': './article/specific-use',
            'validation_type': 'value in list',
            'response': 'OK',
            'expected_value': ['sps-1.9', 'preprint', 'special-issue'],
            'got_value': 'sps-1.9',
            'message': 'Got sps-1.9 expected one item of this list: sps-1.9 | preprint | special-issue',
            'advice': 'XML research-article has None as specific-use expected one item of this list: sps-1.9 | preprint | special-issue'
        }
        """

        specific_use_list = specific_use_list or self.specific_use_list
        if not specific_use_list:
            raise ArticleValidationValidateSpecificUseException("Function requires list of specific uses")

        article_specific_use = self.articles.main_specific_use
        validated = article_specific_use in specific_use_list

        return {
            'title': 'Article element specific-use attribute validation',
            'xpath': './article/specific-use',
            'validation_type': 'value in list',
            'response': 'OK' if validated else 'ERROR',
            'expected_value': specific_use_list,
            'got_value': article_specific_use,
            'message': 'Got {} expected one item of this list: {}'.format(article_specific_use, " | "
                                                                          .join(specific_use_list)),
            'advice': None if validated else 'XML {} has {} as specific-use, expected one item of this list: {}'
            .format(self.articles.main_article_type, article_specific_use, " | ".join(specific_use_list))
        }

    def validate_dtd_version(self, dtd_version_list=None):
        """
        Params
        ------
            xml: ElementTree

        Returns
        -------
        list: dicts as:
        {
            'title': 'Article element dtd-version attribute validation',
            'xpath': './article/dtd-version',
            'validation_type': 'value in list',
            'response': 'OK',
            'expected_value': ['1.1', '1.2', '1.3'],
            'got_value': '1.1',
            'message': 'Got 1.1 expected one item of this list: 1.1 | 1.2 | 1.3',
            'advice': 'XML research-article has 1.1 as dtd-version expected one item of this list: 1.1 | 1.2 | 1.3'
        }
        """

        dtd_version_list = dtd_version_list or self.dtd_version_list
        if not dtd_version_list:
            raise ArticleValidationValidateDtdVersionException("Function requires list of dtd versions")

        article_dtd_version = self.articles.main_dtd_version
        validated = article_dtd_version in dtd_version_list

        return {
            'title': 'Article element dtd-version attribute validation',
            'xpath': './article/dtd-version',
            'validation_type': 'value in list',
            'response': 'OK' if validated else 'ERROR',
            'expected_value': dtd_version_list,
            'got_value': article_dtd_version,
            'message': 'Got {} expected one item of this list: {}'.format(article_dtd_version, " | "
                                                                          .join(dtd_version_list)),
            'advice': None if validated else 'XML {} has {} as dtd-version, expected one item of this list: {}'
            .format(self.articles.main_article_type, article_dtd_version, " | ".join(dtd_version_list))
        }

    def validate(self, data):
        """
        Função que executa as validações da classe ArticleValidation.

        Returns:
            dict: Um dicionário contendo os resultados das validações realizadas.

        """
        return {
            'article_lang_validation': self.validate_language(data['language_codes_list']),
            'article_specific_use_validation': self.validate_specific_use(data['specific_use_list'])
        }
