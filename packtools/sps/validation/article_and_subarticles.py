from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles


class ArticleLangValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.articles = ArticleAndSubArticles(self.xmltree).data
        self.main_article_type = ArticleAndSubArticles(self.xmltree).main_article_type

    def validate_language(self, default_values):
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
        if default_values:
            for article in self.articles:
                lang = article.get('lang')
                item = {
                    'title': 'Article element lang attribute validation',
                    'xpath': './article/@xml:lang' if article.get('article_type') == self.main_article_type else './/sub-article/@xml:lang',
                    'validation_type': 'value in list',
                    'response': 'OK' if lang in default_values else 'ERROR',
                    'expected_value': default_values,
                    'got_value': lang,
                    'message': 'Got {}, expected {}'.format(lang, default_values),
                    'advice': 'XML {} has {} as language, expected {}'.format(article.get('article_type'), lang, default_values)
                }
                yield item
