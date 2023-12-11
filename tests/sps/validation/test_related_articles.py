import unittest

from lxml import etree

from packtools.sps.validation.related_articles import RelatedArticlesValidation


class RelatedArticlesValidationTest(unittest.TestCase):

    def test_related_articles_matches_article_type_validation_match(self):
        self.maxDiff =  None
        xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            
            <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" xlink:href="10.1590/1808-057x202090350"/>
            
            </article>

            """
        )
        obtained = RelatedArticlesValidation(xmltree).related_articles_matches_article_type_validation(
            [
                {
                    'article-type': 'correction',
                    'related-article-types': ['corrected-article']
                },
                {
                    'article-type': 'retraction',
                    'related-article-types': ['retracted-article']
                }
            ]
        )

        expected = [
            {
                'title': 'Related article type validation',
                'xpath': './article[@article-type] .//related-article[@related-article-type]',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': ['corrected-article'],
                'got_value': 'corrected-article',
                'message': "Got corrected-article, expected one of the following items: ['corrected-article']",
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
            article-type="retraction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">

            <related-article ext-link-type="doi" id="ra1" related-article-type="retraction-forward" xlink:href="10.1590/1808-057x202090350"/>

            </article>

            """
        )
        obtained = RelatedArticlesValidation(xmltree).related_articles_matches_article_type_validation(
            [
                {
                    'article-type': 'correction',
                    'related-article-types': ['corrected-article']
                },
                {
                    'article-type': 'retraction',
                    'related-article-types': ['retracted-article', 'article-retracted']
                }
            ]
        )

        expected = [
            {
                'title': 'Related article type validation',
                'xpath': './article[@article-type] .//related-article[@related-article-type]',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': ['retracted-article', 'article-retracted'],
                'got_value': 'retraction-forward',
                'message': "Got retraction-forward, expected one of the following items: ['retracted-article', 'article-retracted']",
                'advice': "The article-type: retraction does not match the related-article-type: retraction-forward, "
                          "provide one of the following items: ['retracted-article', 'article-retracted']"
            }
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_related_articles_has_doi(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="correction-forward" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">

            <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" xlink:href="10.1590/1808-057x202090350"/>

            </article>

            """
        )
        obtained = RelatedArticlesValidation(xmltree).related_articles_doi()

        expected = [
            {
                'title': 'Related article doi validation',
                'xpath': './/related-article/@xlink:href',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '10.1590/1808-057x202090350',
                'got_value': '10.1590/1808-057x202090350',
                'message': 'Got 10.1590/1808-057x202090350, expected 10.1590/1808-057x202090350',
                'advice': None
            }
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_related_articles_does_not_have_doi(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="correction-forward" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">

            <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" />

            </article>

            """
        )
        obtained = RelatedArticlesValidation(xmltree).related_articles_doi()

        expected = [
            {
                'title': 'Related article doi validation',
                'xpath': './/related-article/@xlink:href',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'A valid DOI or URI for related-article/@xlink:href',
                'got_value': None,
                'message': 'Got None, expected a valid DOI or URI for related-article/@xlink:href',
                'advice': 'Provide a valid DOI for <related-article ext-link-type="doi" id="ra1" '
                          'related-article-type="corrected-article" /> '
            }
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)


if __name__ == '__main__':
    unittest.main()
