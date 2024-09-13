import unittest

from lxml import etree

from packtools.sps.validation.related_articles import RelatedArticlesValidation


class RelatedArticlesValidationTest(unittest.TestCase):

    def test_related_articles_matches_article_type_validation_match(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <article-meta>
            <front>
            <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" xlink:href="10.1590/1808-057x202090350"/>
            </front>
            </article-meta>
            </article>

            """
        )
        obtained = list(RelatedArticlesValidation(xmltree).related_articles_matches_article_type_validation(
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
        ))

        expected = [
            {
                'title': 'Related article type validation',
                'parent': 'article',
                'parent_article_type': 'correction',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'related-article',
                'sub_item': 'related-article-type',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': ['corrected-article'],
                'got_value': 'corrected-article',
                'message': "Got corrected-article, expected ['corrected-article']",
                'advice': None,
                'data': {
                    'parent': 'article',
                    'parent_article_type': 'correction',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'ext-link-type': 'doi',
                    'href': '10.1590/1808-057x202090350',
                    'id': 'ra1',
                    'related-article-type': 'corrected-article',
                    'text': ''
                }
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_related_articles_matches_article_type_validation_not_match(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="retraction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <article-meta>
            <front>
            <related-article ext-link-type="doi" id="ra1" related-article-type="retraction-forward" xlink:href="10.1590/1808-057x202090350"/>
            </front>
            </article-meta>
            </article>

            """
        )
        obtained = list(RelatedArticlesValidation(xmltree).related_articles_matches_article_type_validation(
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
        ))

        expected = [
            {
                'title': 'Related article type validation',
                'parent': 'article',
                'parent_article_type': 'retraction',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'related-article',
                'sub_item': 'related-article-type',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': ['retracted-article', 'article-retracted'],
                'got_value': 'retraction-forward',
                'message': "Got retraction-forward, expected ['retracted-article', 'article-retracted']",
                'advice': "The article-type: retraction does not match the related-article-type: retraction-forward, "
                          "provide one of the following items: ['retracted-article', 'article-retracted']",
                'data': {
                    'parent': 'article',
                    'parent_article_type': 'retraction',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'ext-link-type': 'doi',
                    'href': '10.1590/1808-057x202090350',
                    'id': 'ra1',
                    'related-article-type': 'retraction-forward',
                    'text': ''
                }
            }
        ]

        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_related_articles_has_doi(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="correction-forward" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <article-meta>
            <front>
            <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" xlink:href="10.1590/1808-057x202090350"/>
            </front>
            </article-meta>
            </article>

            """
        )
        obtained = list(RelatedArticlesValidation(xmltree).related_articles_doi())

        expected = [
            {
                'title': 'Related article doi validation',
                'parent': 'article',
                'parent_article_type': 'correction-forward',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'related-article',
                'sub_item': 'xlink:href',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '10.1590/1808-057x202090350',
                'got_value': '10.1590/1808-057x202090350',
                'message': 'Got 10.1590/1808-057x202090350, expected 10.1590/1808-057x202090350',
                'advice': None,
                'data': {
                    'parent': 'article',
                    'parent_article_type': 'correction-forward',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'ext-link-type': 'doi',
                    'href': '10.1590/1808-057x202090350',
                    'id': 'ra1',
                    'related-article-type': 'corrected-article',
                    'text': ''
                }
            }
        ]

        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_related_articles_does_not_have_doi(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="correction-forward" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <article-meta>
            <front>
            <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" />
            </front>
            </article-meta>
            </article>

            """
        )
        obtained = list(RelatedArticlesValidation(xmltree).related_articles_doi())

        expected = [
            {
                'title': 'Related article doi validation',
                'parent': 'article',
                'parent_article_type': 'correction-forward',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'related-article',
                'sub_item': 'xlink:href',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'A valid DOI or URI for related-article/@xlink:href',
                'got_value': None,
                'message': 'Got None, expected A valid DOI or URI for related-article/@xlink:href',
                'advice': 'Provide a valid DOI for <related-article ext-link-type="doi" id="ra1" '
                          'related-article-type="corrected-article" /> ',
                'data': {
                    'parent': 'article',
                    'parent_article_type': 'correction-forward',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'ext-link-type': 'doi',
                    'id': 'ra1',
                    'related-article-type': 'corrected-article',
                    'text': '',
                    'href': None
                }
            }
        ]

        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_related_articles_attribute_validation(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <article-meta>
            <front>
            <related-article related-article-type="corrected-article"/>
            </front>
            </article-meta>
            </article>

            """
        )
        obtained = list(RelatedArticlesValidation(xmltree).related_article_attributes_validation())

        expected = [
            {
                'title': 'Related article type validation',
                'parent': 'article',
                'parent_article_type': 'correction',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'related-article',
                'sub_item': '@id',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'a value for @id',
                'got_value': None,
                'message': 'Got None, expected a value for @id',
                'advice': 'Provide a value for @id',
                'data': {
                    'parent': 'article',
                    'parent_article_type': 'correction',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'ext-link-type': None,
                    'href': None,
                    'id': None,
                    'related-article-type': 'corrected-article',
                    'text': ''
                }
            },
            {
                'title': 'Related article type validation',
                'parent': 'article',
                'parent_article_type': 'correction',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'related-article',
                'sub_item': '@href',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'a value for @href',
                'got_value': None,
                'message': 'Got None, expected a value for @href',
                'advice': 'Provide a value for @href',
                'data': {
                    'parent': 'article',
                    'parent_article_type': 'correction',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'ext-link-type': None,
                    'href': None,
                    'id': None,
                    'related-article-type': 'corrected-article',
                    'text': ''
                }
            },
            {
                'title': 'Related article type validation',
                'parent': 'article',
                'parent_article_type': 'correction',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'related-article',
                'sub_item': '@ext-link-type',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'a value for @ext-link-type',
                'got_value': None,
                'message': 'Got None, expected a value for @ext-link-type',
                'advice': 'Provide a value for @ext-link-type',
                'data': {
                    'parent': 'article',
                    'parent_article_type': 'correction',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'ext-link-type': None,
                    'href': None,
                    'id': None,
                    'related-article-type': 'corrected-article',
                    'text': ''
                }
            }
        ]
        self.assertEqual(len(obtained), 3)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_related_articles_matches_history_date_validation_success(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <article-meta>
            <front>
            <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" xlink:href="10.1590/1808-057x202090350"/>
            </front>
            <history>
            <date date-type="received">
            <day>05</day>
            <month>01</month>
            <year>1998</year>
            </date>
            <date date-type="rev-request">
            <day>14</day>
            <month>03</month>
            <year>1998</year>
            </date>
            <date date-type="rev-recd">
            <day>24</day>
            <month>05</month>
            <year>1998</year>
            </date>
            <date date-type="accepted">
            <day>06</day>
            <month>06</month>
            <year>1998</year>
            </date>
            <date date-type="corrected">
            <day>01</day>
            <month>06</month>
            <year>2012</year>
            </date>
            </history>
            </article-meta>
            </article>

            """
        )
        obtained = list(RelatedArticlesValidation(xmltree).related_articles_matches_history_date_validation(
            {
                "correction": "corrected",
                "retraction": "retracted"
            }
        ))

        expected = [
            {
                'title': 'Related article type validation',
                'parent': 'article',
                'parent_article_type': 'correction',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'date',
                'sub_item': '@date-type',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'corrected',
                'got_value': ['received', 'rev-request', 'rev-recd', 'accepted', 'corrected'],
                'message': "Got ['received', 'rev-request', 'rev-recd', 'accepted', 'corrected'], expected corrected",
                'advice': None,
                'data': {
                    'parent': 'article',
                    'parent_article_type': 'correction',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'ext-link-type': 'doi',
                    'href': '10.1590/1808-057x202090350',
                    'id': 'ra1',
                    'related-article-type': 'corrected-article',
                    'text': ''
                }
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_related_articles_matches_history_date_validation_fail(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <article-meta>
            <front>
            <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" xlink:href="10.1590/1808-057x202090350"/>
            </front>
            <history>
            <date date-type="received">
            <day>05</day>
            <month>01</month>
            <year>1998</year>
            </date>
            <date date-type="rev-request">
            <day>14</day>
            <month>03</month>
            <year>1998</year>
            </date>
            <date date-type="rev-recd">
            <day>24</day>
            <month>05</month>
            <year>1998</year>
            </date>
            <date date-type="accepted">
            <day>06</day>
            <month>06</month>
            <year>1998</year>
            </date>
            </history>
            </article-meta>
            </article>

            """
        )
        obtained = list(RelatedArticlesValidation(xmltree).related_articles_matches_history_date_validation(
            {
                "correction": "corrected",
                "retraction": "retracted"
            }
        ))

        expected = [
            {
                'title': 'Related article type validation',
                'parent': 'article',
                'parent_article_type': 'correction',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'date',
                'sub_item': '@date-type',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'corrected',
                'got_value': ['received', 'rev-request', 'rev-recd', 'accepted'],
                'message': "Got ['received', 'rev-request', 'rev-recd', 'accepted'], expected corrected",
                'advice': 'Provide corrected event in <history>',
                'data': {
                    'parent': 'article',
                    'parent_article_type': 'correction',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'ext-link-type': 'doi',
                    'href': '10.1590/1808-057x202090350',
                    'id': 'ra1',
                    'related-article-type': 'corrected-article',
                    'text': ''
                }
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)


if __name__ == '__main__':
    unittest.main()
