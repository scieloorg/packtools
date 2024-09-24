from unittest import TestCase

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation.errata import RelatedArticlesValidation


class ErrataValidationTest(TestCase):
    def test_validate_related_article_not_found(self):
        self.maxDiff = None
        self.xml_tree = get_xml_tree(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <article-meta />
            </article>

            """
        )
        obtained = list(RelatedArticlesValidation(
            self.xml_tree,
            correspondence_list=[
                {
                    'article-type': 'correction',
                    'related-article-type': 'corrected-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'correction-forward',
                    'date-type': 'corrected'
                },
                {
                    'article-type': 'retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': 'partial-retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'retraction-forward',
                    'date-type': 'retracted'
                },
                {
                    'article-type': None,
                    'related-article-type': 'partial-retraction',
                    'date-type': 'retracted'
                },
            ]
        ).validate_related_articles())
        expected = [
            {
                "title": "matching 'correction' and 'corrected-article'",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "correction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "match",
                "response": "ERROR",
                "expected_value": 'at least one <related-article related-article-type="corrected-article">',
                "got_value": None,
                "message": f'Got None, expected at least one <related-article related-article-type="corrected-article">',
                "advice": 'provide <related-article related-article-type="corrected-article">',
                "data": [],
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_related_article_does_not_match(self):
        self.maxDiff = None
        self.xml_tree = get_xml_tree(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <related-article ext-link-type="doi" id="RA1" related-article-type="correction-forward" xlink:href="10.5935/abc.20160032"/>
            <related-article ext-link-type="doi" id="RA2" related-article-type="commentary" xlink:href="10.5935/abc.20150051"/>
            </article-meta>
            </front>
            </article>

            """
        )
        obtained = list(RelatedArticlesValidation(
            self.xml_tree,
            correspondence_list=[
                {
                    'article-type': 'correction',
                    'related-article-type': 'corrected-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'correction-forward',
                    'date-type': 'corrected'
                },
                {
                    'article-type': 'retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': 'partial-retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'retraction-forward',
                    'date-type': 'retracted'
                },
                {
                    'article-type': None,
                    'related-article-type': 'partial-retraction',
                    'date-type': 'retracted'
                },
            ]
        ).validate_related_articles())
        expected = [
            {
                "title": "matching 'correction' and 'corrected-article'",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "correction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "match",
                "response": "ERROR",
                "expected_value": 'at least one <related-article related-article-type="corrected-article">',
                "got_value": None,
                "message": 'Got None, expected at least one <related-article related-article-type="corrected-article">',
                "advice": 'provide <related-article related-article-type="corrected-article">',
                "data": [
                    {
                        'ext-link-type': 'doi',
                        'href': '10.5935/abc.20160032',
                        'id': 'RA1',
                        'parent': 'article',
                        'parent_article_type': 'correction',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'related-article-type': 'correction-forward',
                        'text': ''
                    },
                    {
                        'ext-link-type': 'doi',
                        'href': '10.5935/abc.20150051',
                        'id': 'RA2',
                        'parent': 'article',
                        'parent_article_type': 'correction',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'related-article-type': 'commentary',
                        'text': ''
                    }
                ],
            },
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


class RelatedArticlesTest(TestCase):
    def test_validate_related_article_not_found(self):
        self.maxDiff = None
        self.xml_tree = get_xml_tree(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            </article>

            """
        )
        obtained = list(RelatedArticlesValidation(
            self.xml_tree,
            correspondence_list=[
                {
                    'article-type': 'correction',
                    'related-article-type': 'corrected-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'correction-forward',
                    'date-type': 'corrected'
                },
                {
                    'article-type': 'retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': 'partial-retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'retraction-forward',
                    'date-type': 'retracted'
                },
                {
                    'article-type': None,
                    'related-article-type': 'partial-retraction',
                    'date-type': 'retracted'
                },
            ]
        ).validate_related_articles())
        expected = [
            {
                "title": "matching 'correction' and 'corrected-article'",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "correction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "match",
                "response": "ERROR",
                "expected_value": 'at least one <related-article related-article-type="corrected-article">',
                "got_value": None,
                "message": f'Got None, expected at least one <related-article related-article-type="corrected-article">',
                "advice": 'provide <related-article related-article-type="corrected-article">',
                "data": [],
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_related_article_does_not_match(self):
        self.maxDiff = None
        self.xml_tree = get_xml_tree(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <related-article ext-link-type="doi" id="RA1" related-article-type="correction-forward" xlink:href="10.5935/abc.20160032"/>
            <related-article ext-link-type="doi" id="RA2" related-article-type="commentary" xlink:href="10.5935/abc.20150051"/>
            </article-meta>
            </front>
            </article>
            """
        )
        obtained = list(RelatedArticlesValidation(
            self.xml_tree,
            correspondence_list=[
                {
                    'article-type': 'correction',
                    'related-article-type': 'corrected-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'correction-forward',
                    'date-type': 'corrected'
                },
                {
                    'article-type': 'retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': 'partial-retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'retraction-forward',
                    'date-type': 'retracted'
                },
                {
                    'article-type': None,
                    'related-article-type': 'partial-retraction',
                    'date-type': 'retracted'
                },
            ]
        ).validate_related_articles())
        expected = [
            {
                "title": "matching 'correction' and 'corrected-article'",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "correction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "match",
                "response": "ERROR",
                "expected_value": 'at least one <related-article related-article-type="corrected-article">',
                "got_value": None,
                "message": f'Got None, expected at least one <related-article related-article-type="corrected-article">',
                "advice": 'provide <related-article related-article-type="corrected-article">',
                "data": [
                    {
                        'ext-link-type': 'doi',
                        'href': '10.5935/abc.20160032',
                        'id': 'RA1',
                        'parent': 'article',
                        'parent_article_type': 'correction',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'related-article-type': 'correction-forward',
                        'text': ''
                    },
                    {
                        'ext-link-type': 'doi',
                        'href': '10.5935/abc.20150051',
                        'id': 'RA2',
                        'parent': 'article',
                        'parent_article_type': 'correction',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'related-article-type': 'commentary',
                        'text': ''
                    }
                ],
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_count_related_article_count_date(self):
        self.maxDiff = None
        self.xml_tree = get_xml_tree(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <related-article ext-link-type="doi" id="RA1" related-article-type="correction-forward" xlink:href="10.5935/abc.20160032"/>
            <history>
            <date date-type="received">
            <day>05</day>
            <month>01</month>
            <year>1998</year>
            </date>
            </history>
            </article-meta>
            </front>
            </article>
            """
        )
        obtained = list(RelatedArticlesValidation(
            self.xml_tree,
            correspondence_list=[
                {
                    'article-type': 'correction',
                    'related-article-type': 'corrected-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'correction-forward',
                    'date-type': 'corrected'
                },
                {
                    'article-type': 'retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': 'partial-retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'retraction-forward',
                    'date-type': 'retracted'
                },
                {
                    'article-type': None,
                    'related-article-type': 'partial-retraction',
                    'date-type': 'retracted'
                },
            ]
        ).validate_history_events())
        expected = [
            {
                "title": 'exist historical date event for the related-article',
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "correction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": '<date date-type="corrected">',
                "got_value": None,
                "message": 'Got None, expected <date date-type="corrected">',
                'advice': 'provide <date date-type="corrected">',
                "data": {
                    'received': {
                        'day': '05',
                        'month': '01',
                        'type': 'received',
                        'year': '1998'
                    }
                }
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


class ArticleRetractedInFullValidationTest(TestCase):
    def test_validate_related_article_not_found(self):
        self.maxDiff = None
        self.xml_tree = get_xml_tree(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="retraction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            </article>

            """
        )
        obtained = list(RelatedArticlesValidation(
            self.xml_tree,
            correspondence_list=[
                {
                    'article-type': 'correction',
                    'related-article-type': 'corrected-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'correction-forward',
                    'date-type': 'corrected'
                },
                {
                    'article-type': 'retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': 'partial-retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'retraction-forward',
                    'date-type': 'retracted'
                },
                {
                    'article-type': None,
                    'related-article-type': 'partial-retraction',
                    'date-type': 'retracted'
                },
            ]
        ).validate_related_articles())
        expected = [
            {
                "title": "matching 'retraction' and 'retracted-article'",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "retraction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "match",
                "response": "ERROR",
                "expected_value": 'at least one <related-article related-article-type="retracted-article">',
                "got_value": None,
                "message": f'Got None, expected at least one <related-article related-article-type="retracted-article">',
                'advice': 'provide <related-article related-article-type="retracted-article">',
                "data": [],
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_related_article_does_not_match(self):
        self.maxDiff = None
        self.xml_tree = get_xml_tree(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="retraction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <related-article ext-link-type="doi" id="RA2" related-article-type="commentary" xlink:href="10.5935/abc.20150051"/>
            </article-meta>
            </front>
            </article>

            """
        )
        obtained = list(RelatedArticlesValidation(
            self.xml_tree,
            correspondence_list=[
                {
                    'article-type': 'correction',
                    'related-article-type': 'corrected-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'correction-forward',
                    'date-type': 'corrected'
                },
                {
                    'article-type': 'retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': 'partial-retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'retraction-forward',
                    'date-type': 'retracted'
                },
                {
                    'article-type': None,
                    'related-article-type': 'partial-retraction',
                    'date-type': 'retracted'
                },
            ]
        ).validate_related_articles())
        expected = [
            {
                "title": "matching 'retraction' and 'retracted-article'",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "retraction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "match",
                "response": "ERROR",
                "expected_value": 'at least one <related-article related-article-type="retracted-article">',
                "got_value": None,
                "message": f'Got None, expected at least one <related-article related-article-type="retracted-article">',
                "advice": 'provide <related-article related-article-type="retracted-article">',
                "data": [
                    {
                        'ext-link-type': 'doi',
                        'href': '10.5935/abc.20150051',
                        'id': 'RA2',
                        'parent': 'article',
                        'parent_article_type': 'retraction',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'related-article-type': 'commentary',
                        'text': ''
                    }
                ]
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_count_related_article_count_date(self):
        self.maxDiff = None
        self.xml_tree = get_xml_tree(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="retraction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <related-article ext-link-type="doi" id="RA1" related-article-type="retraction-forward" xlink:href="10.5935/abc.20160032"/>
            <history>
            <date date-type="received">
            <day>05</day>
            <month>01</month>
            <year>1998</year>
            </date>
            </history>
            </article-meta>
            </front>
            </article>
            """
        )
        obtained = list(RelatedArticlesValidation(
            self.xml_tree,
            correspondence_list=[
                {
                    'article-type': 'correction',
                    'related-article-type': 'corrected-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'correction-forward',
                    'date-type': 'corrected'
                },
                {
                    'article-type': 'retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': 'partial-retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'retraction-forward',
                    'date-type': 'retracted'
                },
                {
                    'article-type': None,
                    'related-article-type': 'partial-retraction',
                    'date-type': 'retracted'
                },
            ]
        ).validate_history_events())
        expected = [
            {
                "title": 'exist historical date event for the related-article',
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "retraction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": '<date date-type="retracted">',
                "got_value": None,
                "message": 'Got None, expected <date date-type="retracted">',
                "advice": 'provide <date date-type="retracted">',
                "data": {
                    'received': {
                        'day': '05',
                        'month': '01',
                        'type': 'received',
                        'year': '1998'
                    }
                }
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


class ArticlePartiallyRetractedValidationTest(TestCase):
    def test_validate_related_article_not_found(self):
        self.maxDiff = None
        self.xml_tree = get_xml_tree(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="partial-retraction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            </article>

            """
        )
        obtained = list(RelatedArticlesValidation(
            self.xml_tree,
            correspondence_list=[
                {
                    'article-type': 'correction',
                    'related-article-type': 'corrected-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'correction-forward',
                    'date-type': 'corrected'
                },
                {
                    'article-type': 'retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': 'partial-retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'retraction-forward',
                    'date-type': 'retracted'
                },
                {
                    'article-type': None,
                    'related-article-type': 'partial-retraction',
                    'date-type': 'retracted'
                },
            ]
        ).validate_related_articles())
        expected = [
            {
                "title": "matching 'partial-retraction' and 'retracted-article'",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "partial-retraction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "match",
                "response": "ERROR",
                "expected_value": 'at least one <related-article related-article-type="retracted-article">',
                "got_value": None,
                "message": f'Got None, expected at least one <related-article related-article-type="retracted-article">',
                'advice': 'provide <related-article related-article-type="retracted-article">',
                "data": [],
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_related_article_found(self):
        self.maxDiff = None
        self.xml_tree = get_xml_tree(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="partial-retraction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <related-article ext-link-type="doi" id="RA2" related-article-type="commentary" xlink:href="10.5935/abc.20150051"/>
            </article-meta>
            </front>
            </article>

            """
        )
        obtained = list(RelatedArticlesValidation(
            self.xml_tree,
            correspondence_list=[
                {
                    'article-type': 'correction',
                    'related-article-type': 'corrected-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'correction-forward',
                    'date-type': 'corrected'
                },
                {
                    'article-type': 'retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': 'partial-retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'retraction-forward',
                    'date-type': 'retracted'
                },
                {
                    'article-type': None,
                    'related-article-type': 'partial-retraction',
                    'date-type': 'retracted'
                },
            ]
        ).validate_related_articles())
        expected = [
            {
                "title": "matching 'partial-retraction' and 'retracted-article'",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "partial-retraction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "match",
                "response": "ERROR",
                "expected_value": 'at least one <related-article related-article-type="retracted-article">',
                "got_value": None,
                "message": 'Got None, expected at least one <related-article related-article-type="retracted-article">',
                "advice": 'provide <related-article related-article-type="retracted-article">',
                "data": [
                    {
                        'ext-link-type': 'doi',
                        'href': '10.5935/abc.20150051',
                        'id': 'RA2',
                        'parent': 'article',
                        'parent_article_type': 'partial-retraction',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'related-article-type': 'commentary',
                        'text': ''
                    }
                ],
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_count_related_article_count_date(self):
        self.maxDiff = None
        self.xml_tree = get_xml_tree(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="partial-retraction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <related-article ext-link-type="doi" id="RA1" related-article-type="partial-retraction" xlink:href="10.5935/abc.20160032"/>
            <related-article ext-link-type="doi" id="RA2" related-article-type="partial-retraction" xlink:href="10.5935/abc.20150051"/>
            <history>
            <date date-type="received">
            <day>05</day>
            <month>01</month>
            <year>1998</year>
            </date>
            </history>
            </article-meta>
            </front>
            </article>
            """
        )
        obtained = list(RelatedArticlesValidation(
            self.xml_tree,
            correspondence_list=[
                {
                    'article-type': 'correction',
                    'related-article-type': 'corrected-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'correction-forward',
                    'date-type': 'corrected'
                },
                {
                    'article-type': 'retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': 'partial-retraction',
                    'related-article-type': 'retracted-article',
                    'date-type': None
                },
                {
                    'article-type': None,
                    'related-article-type': 'retraction-forward',
                    'date-type': 'retracted'
                },
                {
                    'article-type': None,
                    'related-article-type': 'partial-retraction',
                    'date-type': 'retracted'
                },
            ]
        ).validate_history_events())
        expected = [
            {
                "title": 'exist historical date event for the related-article',
                "parent": "article",
                "parent_id": None,
                "parent_article_type": 'partial-retraction',
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": '<date date-type="retracted">',
                "got_value": None,
                "message": 'Got None, expected <date date-type="retracted">',
                "advice": 'provide <date date-type="retracted">',
                "data": {
                    'received': {
                        'day': '05',
                        'month': '01',
                        'type': 'received',
                        'year': '1998'
                    }
                },
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])
