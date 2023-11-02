from unittest import TestCase

from packtools.sps.utils import xml_utils

from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles


class ArticleAndSubarticlesTest(TestCase):
    def test_main_lang(self):
        data = """<article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en"></article>"""
        xmltree = xml_utils.get_xml_tree(data)

        expected = 'en'
        obtained = ArticleAndSubArticles(xmltree).main_lang

        self.assertEqual(expected, obtained)

    def test_all_lang(self):
        with open('tests/samples/article-abstract-en-sub-articles-pt-es.xml', 'r') as data:
            xmltree = xml_utils.get_xml_tree(data.read())

        expected = ['en', 'pt', 'es']
        obtained = [d['lang'] for d in ArticleAndSubArticles(xmltree).data]

        self.assertListEqual(expected, obtained)

    def test_main_article_type(self):
        data = """<article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en"></article>"""
        xmltree = xml_utils.get_xml_tree(data)

        expected = 'research-article'
        obtained = ArticleAndSubArticles(xmltree).main_article_type

        self.assertEqual(expected, obtained)

    def test_all_article_type(self):
        with open('tests/samples/article-abstract-en-sub-articles-pt-es.xml', 'r') as data:
            xmltree = xml_utils.get_xml_tree(data.read())

        expected = ['research-article', 'translation', 'translation']
        obtained = [d['article_type'] for d in ArticleAndSubArticles(xmltree).data]

        self.assertListEqual(expected, obtained)

    def test_elements_order(self):
        with open('tests/samples/artigo-com-traducao-e-pareceres-traduzidos.xml', 'r') as data:
            xmltree = xml_utils.get_xml_tree(data.read())

        expected = [
            {
                'article_id': 'main',
                'article_type': 'research-article',
                'lang': 'pt',
                'line_number': 2
            },
            {
                'article_id': 's2',
                'article_type': 'reviewer-report',
                'lang': 'pt',
                'line_number': 93
            },
            {
                'article_id': 's3',
                'article_type': 'reviewer-report',
                'lang': 'pt',
                'line_number': 141
            },
            {
                'article_id': 's1',
                'article_type': 'translation',
                'lang': 'en',
                'line_number': 189
            },
            {
                'article_id': 's5',
                'article_type': 'reviewer-report',
                'lang': 'en',
                'line_number': 233
            },
            {
                'article_id': 's6',
                'article_type': 'reviewer-report',
                'lang': 'en',
                'line_number': 271
            }
        ]
        obtained = [d for d in ArticleAndSubArticles(xmltree).data]

        self.assertListEqual(expected, obtained)
