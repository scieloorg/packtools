import unittest

from lxml import etree

from packtools.sps.validation.related_articles import RelatedArticlesValidation


class RelatedArticlesValidationTest(unittest.TestCase):

    def test_related_articles_matches_article_type_validation_match(self):
        self.maxDiff =  None
        xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="correction-forward" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            
            <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" xlink:href="10.1590/1808-057x202090350"/>
            
            </article>

            """
        )
        obtained = RelatedArticlesValidation(xmltree).related_articles_matches_article_type_validation(
            {
                'correction-forward': 'corrected-article',
                'retracted-article': 'retraction-forward'
            }
        )

        expected = [
            {
                'title': 'Related article type validation',
                'xpath': './article[@article-type] .//related-article[@related-article-type]',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'A valid match such as the following: (correction-forward, corrected-article) or ('
                                  'retracted-article, retraction-forward)',
                'got_value': 'article-type: correction-forward, related-article-type: corrected-article',
                'message': 'Got (correction-forward, corrected-article), expected (correction-forward, '
                           'corrected-article) or (retracted-article, retraction-forward)',
                'advice': None
            }
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_related_articles_matches_article_type_validation_not_match(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="correction-forward" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">

            <related-article ext-link-type="doi" id="ra1" related-article-type="retraction-forward" xlink:href="10.1590/1808-057x202090350"/>

            </article>

            """
        )
        obtained = RelatedArticlesValidation(xmltree).related_articles_matches_article_type_validation(
            {
                'correction-forward': 'corrected-article',
                'retracted-article': 'retraction-forward'
            }
        )

        expected = [
            {
                'title': 'Related article type validation',
                'xpath': './article[@article-type] .//related-article[@related-article-type]',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': 'A valid match such as the following: (correction-forward, corrected-article) or ('
                                  'retracted-article, retraction-forward)',
                'got_value': 'article-type: correction-forward, related-article-type: retraction-forward',
                'message': 'Got (correction-forward, retraction-forward), expected (correction-forward, '
                           'corrected-article) or (retracted-article, retraction-forward)',
                'advice': 'Consider replacing the article-type and related-article-type with a tuple from the '
                          'following list: (correction-forward, corrected-article) or (retracted-article, '
                          'retraction-forward)'
            }
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

