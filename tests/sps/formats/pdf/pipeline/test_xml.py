import unittest

from lxml import etree

from packtools.sps.formats.pdf.pipeline import xml as xml_pipe


class TestExtractArticleMainLanguage(unittest.TestCase):

    def test_extract_article_main_language_with_valid_lang(self):
        xmltree = etree.fromstring(
            '<article xmlns:xml="http://www.w3.org/XML/1998/namespace" xml:lang="en">'
            '<front><article-meta></article-meta></front>'
            '</article>'
        )
        expected = "en"
        result = xml_pipe.extract_article_main_language(xmltree)
        self.assertEqual(expected, result)

    def test_extract_article_main_language_without_lang(self):
        xmltree = etree.fromstring(
            '<article xmlns:xml="http://www.w3.org/XML/1998/namespace">'
            '<front><article-meta></article-meta></front>'
            '</article>'
        )
        result = xml_pipe.extract_article_main_language(xmltree)
        self.assertIsNone(result)

    def test_extract_article_main_language_with_custom_namespace(self):
        xmltree = etree.fromstring(
            '<article xmlns:custom="http://custom.namespace" custom:lang="pt">'
            '<front><article-meta></article-meta></front>'
            '</article>'
        )
        expected = "pt"
        result = xml_pipe.extract_article_main_language(
            xmltree, 
            namespaces={'xml': 'http://custom.namespace'}
        )
        self.assertEqual(expected, result)

    def test_extract_article_main_language_with_multiple_langs(self):
        xmltree = etree.fromstring(
            '<article xmlns:xml="http://www.w3.org/XML/1998/namespace" xml:lang="es">'
            '<front xml:lang="en"><article-meta></article-meta></front>'
            '</article>'
        )
        expected = "es"
        result = xml_pipe.extract_article_main_language(xmltree)
        self.assertEqual(expected, result)
