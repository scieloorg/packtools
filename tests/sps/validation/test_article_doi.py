import unittest

from packtools.sps.utils.xml_utils import get_xml_tree

from packtools.sps.validation.article_doi import ArticleDoiValidation


class ArticleDoiTest(unittest.TestCase):
    def test_validate_article_has_doi(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
            <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
            <article-id pub-id-type="other">00303</article-id>
            </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleDoiValidation(xml_tree).validate_main_article_doi_exists()
        expected = {
            'title': 'Article DOI element',
            'xpath': './article-id[@pub-id-type="doi"]',
            'validation_type': 'exist',
            'response': 'OK',
            'expected_value': 'article DOI',
            'got_value': '10.1590/1518-8345.2927.3231',
            'message': 'Got 10.1590/1518-8345.2927.3231 expected a DOI',
            'advice': None
        }
        self.assertDictEqual(obtained, expected)

