from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles


class ArticleLangValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree).data
        self.main_article_type = ArticleAndSubArticles(self.xmltree).main_article_type

    def validate_language(self, language_codes):
        """
        Params
        ------
        list: Default values to languages

        Returns
        -------
        list: dicts as:
        {
            'title': 'Article element lang attribute validation',
            'xpath': './article/@xml:lang',
            'validation_type': 'value in list',
            'response': 'OK',
            'expected_value': ['en'],
            'got_value': 'en',
            'message': 'Got en, expected ['en']',
            'advice': 'XML research-article has en as language, expected ['en']'
        }
        """
        if language_codes:
            for article in self.articles:
                lang = article.get('lang')
                item = {
                    'title': 'Article element lang attribute validation',
                    'xpath': './article/@xml:lang' if article.get('article_type') == self.main_article_type else './/sub-article/@xml:lang',
                    'validation_type': 'value in list',
                    'response': 'OK' if lang in language_codes else 'ERROR',
                    'expected_value': language_codes,
                    'got_value': lang,
                    'message': 'Got {}, expected one item of this list: {}'.format(lang, " | ".join(language_codes)),
                    'advice': 'XML {} has {} as language, expected one item of this list: {}'.format(article.get('article_type'), lang, " | ".join(language_codes))
                }
                yield item
