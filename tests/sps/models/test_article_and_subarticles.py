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
        data = open('tests/samples/article-abstract-en-sub-articles-pt-es.xml').read()
        xmltree = xml_utils.get_xml_tree(data)

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
        data = open('tests/samples/article-abstract-en-sub-articles-pt-es.xml').read()
        xmltree = xml_utils.get_xml_tree(data)

        expected = ['research-article', 'translation', 'translation']
        obtained = [d['article_type'] for d in ArticleAndSubArticles(xmltree).data]

        self.assertListEqual(expected, obtained)
