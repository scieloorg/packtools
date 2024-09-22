from unittest import TestCase

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation.errata import ErrataValidation, ArticleCorrectedValidation, ArticleRetractedInFullValidation, ArticlePartiallyRetractedValidation


class ErrataValidationTest(TestCase):
    def test_validate_related_article_not_found(self):
        self.maxDiff = None
        self.xml_tree = get_xml_tree(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            </article>

            """
        )
        obtained = list(ErrataValidation(
            self.xml_tree,
            expected_article_type="correction",
            expected_related_article_type="corrected-article"
        ).validate_related_article())
        expected = [
            {
                "title": "validation matching 'correction' and 'corrected-article'",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "correction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": 'at least one <related-article related-article-type="corrected-article">',
                "got_value": None,
                "message": f'Got None, expected at least one <related-article related-article-type="corrected-article">',
                "advice": 'provide <related-article related-article-type="corrected-article">',
                "data": None,
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
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <related-article ext-link-type="doi" id="RA1" related-article-type="corrected-article" xlink:href="10.5935/abc.20160032"/>
            <related-article ext-link-type="doi" id="RA2" related-article-type="commentary" xlink:href="10.5935/abc.20150051"/>
            </front>
            </article>

            """
        )
        obtained = list(ErrataValidation(
            self.xml_tree,
            expected_article_type="correction",
            expected_related_article_type="corrected-article"
        ).validate_related_article())
        expected = [
            {
                "title": "validation matching 'correction' and 'corrected-article'",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "correction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "match",
                "response": "OK",
                "expected_value": 'at least one <related-article related-article-type="corrected-article">',
                "got_value": '<related-article ext-link-type="doi" id="RA1" related-article-type="corrected-article" xlink:href="10.5935/abc.20160032"/>',
                "message": f'Got <related-article ext-link-type="doi" id="RA1" related-article-type="corrected-article" xlink:href="10.5935/abc.20160032"/>, '
                           f'expected at least one <related-article related-article-type="corrected-article">',
                "advice": None,
                "data": {
                    'ext-link-type': 'doi',
                    'href': '10.5935/abc.20160032',
                    'id': 'RA1',
                    'parent': 'article',
                    'parent_article_type': 'correction',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'related-article-type': 'corrected-article'
                },
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


class ArticleCorrectedValidationTest(TestCase):
    def test_validate_related_article_not_found(self):
        self.maxDiff = None
        self.xml_tree = get_xml_tree(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            </article>

            """
        )
        obtained = list(ArticleCorrectedValidation(
            self.xml_tree,
            expected_article_type="correction",
            expected_related_article_type="correction-forward"
        ).validate_related_article())
        expected = [
            {
                "title": "validation matching 'correction' and 'correction-forward'",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "correction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": 'at least one <related-article related-article-type="correction-forward">',
                "got_value": None,
                "message": f'Got None, expected at least one <related-article related-article-type="correction-forward">',
                "advice": 'provide <related-article related-article-type="correction-forward">',
                "data": None,
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
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <related-article ext-link-type="doi" id="RA1" related-article-type="correction-forward" xlink:href="10.5935/abc.20160032"/>
            <related-article ext-link-type="doi" id="RA2" related-article-type="commentary" xlink:href="10.5935/abc.20150051"/>
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
            </front>
            </article>
            """
        )
        obtained = list(ArticleCorrectedValidation(
            self.xml_tree,
            expected_article_type="correction",
            expected_related_article_type="correction-forward"
        ).validate_related_article())
        expected = [
            {
                "title": "validation matching 'correction' and 'correction-forward'",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "correction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "match",
                "response": "OK",
                "expected_value": 'at least one <related-article related-article-type="correction-forward">',
                "got_value": '<related-article ext-link-type="doi" id="RA1" related-article-type="correction-forward" xlink:href="10.5935/abc.20160032"/>',
                "message": f'Got <related-article ext-link-type="doi" id="RA1" related-article-type="correction-forward" xlink:href="10.5935/abc.20160032"/>, '
                           f'expected at least one <related-article related-article-type="correction-forward">',
                "advice": None,
                "data": {
                    'ext-link-type': 'doi',
                    'href': '10.5935/abc.20160032',
                    'id': 'RA1',
                    'parent': 'article',
                    'parent_article_type': 'correction',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'related-article-type': 'correction-forward'
                },
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
            <related-article ext-link-type="doi" id="RA1" related-article-type="correction-forward" xlink:href="10.5935/abc.20160032"/>
            <related-article ext-link-type="doi" id="RA2" related-article-type="correction-forward" xlink:href="10.5935/abc.20150051"/>
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
            </front>
            </article>
            """
        )
        obtained = list(ArticleCorrectedValidation(
            self.xml_tree,
            expected_article_type="correction",
            expected_related_article_type="correction-forward"
        ).validate_history_dates())
        expected = [
            {
                "title": "validation related and corrected dates count",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "correction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": 'equal numbers of <related-article type="correction-forward"> and <date type="corrected">',
                "got_value": '2 <related-article type="correction-forward"> and 1 <date type="corrected">',
                "message": 'Got 2 <related-article type="correction-forward"> and 1 <date type="corrected">, '
                           'expected equal numbers of <related-article type="correction-forward"> and <date '
                           'type="corrected">',
                "advice": 'for each <related-article type="correction-forward">, there must be a corresponding <date type="corrected"> in <history>',
                "data": [
                    {
                        'parent': 'article',
                        'parent_article_type': 'correction',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'article_date': None,
                        'collection_date': None,
                        'history': {
                            'accepted': {'day': '06', 'month': '06', 'type': 'accepted', 'year': '1998'},
                            'corrected': {'day': '01', 'month': '06', 'type': 'corrected', 'year': '2012'},
                            'received': {'day': '05', 'month': '01', 'type': 'received', 'year': '1998'},
                            'rev-recd': {'day': '24', 'month': '05', 'type': 'rev-recd', 'year': '1998'},
                            'rev-request': {'day': '14', 'month': '03', 'type': 'rev-request', 'year': '1998'}
                        },
                    }
                ]
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
        obtained = list(ArticleRetractedInFullValidation(
            self.xml_tree,
            expected_article_type="retraction",
            expected_related_article_type="retracted-article"
        ).validate_related_article())
        expected = [
            {
                "title": "validation matching 'retraction' and 'retracted-article'",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "retraction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": 'at least one <related-article related-article-type="retracted-article">',
                "got_value": None,
                "message": f'Got None, expected at least one <related-article related-article-type="retracted-article">',
                'advice': 'provide <related-article related-article-type="retracted-article">',
                "data": None,
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
            article-type="retraction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <related-article ext-link-type="doi" id="RA1" related-article-type="retracted-article" xlink:href="10.5935/abc.20160032"/>
            <related-article ext-link-type="doi" id="RA2" related-article-type="commentary" xlink:href="10.5935/abc.20150051"/>
            </front>
            </article>

            """
        )
        obtained = list(ArticleRetractedInFullValidation(
            self.xml_tree,
            expected_article_type="retraction",
            expected_related_article_type="retracted-article"
        ).validate_related_article())
        expected = [
            {
                "title": "validation matching 'retraction' and 'retracted-article'",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "retraction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "match",
                "response": "OK",
                "expected_value": 'at least one <related-article related-article-type="retracted-article">',
                "got_value": '<related-article ext-link-type="doi" id="RA1" related-article-type="retracted-article" xlink:href="10.5935/abc.20160032"/>',
                "message": f'Got <related-article ext-link-type="doi" id="RA1" related-article-type="retracted-article" xlink:href="10.5935/abc.20160032"/>, '
                           f'expected at least one <related-article related-article-type="retracted-article">',
                "advice": None,
                "data": {
                    'ext-link-type': 'doi',
                    'href': '10.5935/abc.20160032',
                    'id': 'RA1',
                    'parent': 'article',
                    'parent_article_type': 'retraction',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'related-article-type': 'retracted-article'
                },
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
            <related-article ext-link-type="doi" id="RA1" related-article-type="retracted-article" xlink:href="10.5935/abc.20160032"/>
            <related-article ext-link-type="doi" id="RA2" related-article-type="retracted-article" xlink:href="10.5935/abc.20150051"/>
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
            <date date-type="retracted">
            <day>01</day>
            <month>06</month>
            <year>2012</year>
            </date>
            </history>
            </front>
            </article>
            """
        )
        obtained = list(ArticleRetractedInFullValidation(
            self.xml_tree,
            expected_article_type="retraction",
            expected_related_article_type="retracted-article"
        ).validate_history_dates())
        expected = [
            {
                "title": "validation related and corrected dates count",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "retraction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": 'equal numbers of <related-article type="retracted-article"> and <date type="retracted">',
                "got_value": '2 <related-article type="retracted-article"> and 1 <date type="retracted">',
                "message": 'Got 2 <related-article type="retracted-article"> and 1 <date type="retracted">, '
                           'expected equal numbers of <related-article type="retracted-article"> and <date '
                           'type="retracted">',
                "advice": 'for each <related-article type="retracted-article">, there must be a corresponding <date type="retracted"> in <history>',
                "data": [
                    {
                        'parent': 'article',
                        'parent_article_type': 'retraction',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'article_date': None,
                        'collection_date': None,
                        'history': {
                            'accepted': {'day': '06', 'month': '06', 'type': 'accepted', 'year': '1998'},
                            'retracted': {'day': '01', 'month': '06', 'type': 'retracted', 'year': '2012'},
                            'received': {'day': '05', 'month': '01', 'type': 'received', 'year': '1998'},
                            'rev-recd': {'day': '24', 'month': '05', 'type': 'rev-recd', 'year': '1998'},
                            'rev-request': {'day': '14', 'month': '03', 'type': 'rev-request', 'year': '1998'}
                        },
                    }
                ]
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
            article-type="retraction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            </article>

            """
        )
        obtained = list(ArticlePartiallyRetractedValidation(
            self.xml_tree,
            expected_article_type="retraction",
            expected_related_article_type="partial-retraction"
        ).validate_related_article())
        expected = [
            {
                "title": "validation matching 'retraction' and 'partial-retraction'",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "retraction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": 'at least one <related-article related-article-type="partial-retraction">',
                "got_value": None,
                "message": f'Got None, expected at least one <related-article related-article-type="partial-retraction">',
                'advice': 'provide <related-article related-article-type="partial-retraction">',
                "data": None,
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
            article-type="retraction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <related-article ext-link-type="doi" id="RA1" related-article-type="partial-retraction" xlink:href="10.5935/abc.20160032"/>
            <related-article ext-link-type="doi" id="RA2" related-article-type="commentary" xlink:href="10.5935/abc.20150051"/>
            </front>
            </article>

            """
        )
        obtained = list(ArticleRetractedInFullValidation(
            self.xml_tree,
            expected_article_type="retraction",
            expected_related_article_type="partial-retraction"
        ).validate_related_article())
        expected = [
            {
                "title": "validation matching 'retraction' and 'retracted-article'",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "retraction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "match",
                "response": "OK",
                "expected_value": 'at least one <related-article related-article-type="partial-retraction">',
                "got_value": '<related-article ext-link-type="doi" id="RA1" related-article-type="partial-retraction" xlink:href="10.5935/abc.20160032"/>',
                "message": f'Got <related-article ext-link-type="doi" id="RA1" related-article-type="partial-retraction" xlink:href="10.5935/abc.20160032"/>, '
                           f'expected at least one <related-article related-article-type="partial-retraction">',
                "advice": None,
                "data": {
                    'ext-link-type': 'doi',
                    'href': '10.5935/abc.20160032',
                    'id': 'RA1',
                    'parent': 'article',
                    'parent_article_type': 'retraction',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'related-article-type': 'partial-retraction'
                },
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
            <related-article ext-link-type="doi" id="RA1" related-article-type="partial-retraction" xlink:href="10.5935/abc.20160032"/>
            <related-article ext-link-type="doi" id="RA2" related-article-type="partial-retraction" xlink:href="10.5935/abc.20150051"/>
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
            <date date-type="retracted">
            <day>01</day>
            <month>06</month>
            <year>2012</year>
            </date>
            </history>
            </front>
            </article>
            """
        )
        obtained = list(ArticlePartiallyRetractedValidation(
            self.xml_tree,
            expected_article_type="retraction",
            expected_related_article_type="partial-retraction"
        ).validate_history_dates())
        expected = [
            {
                "title": "validation related and corrected dates count",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "retraction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": 'equal numbers of <related-article type="partial-retraction"> and <date type="retracted">',
                "got_value": '2 <related-article type="partial-retraction"> and 1 <date type="retracted">',
                "message": 'Got 2 <related-article type="partial-retraction"> and 1 <date type="retracted">, '
                           'expected equal numbers of <related-article type="partial-retraction"> and <date '
                           'type="retracted">',
                "advice": 'for each <related-article type="partial-retraction">, there must be a corresponding <date type="retracted"> in <history>',
                "data": [
                    {
                        'parent': 'article',
                        'parent_article_type': 'retraction',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'article_date': None,
                        'collection_date': None,
                        'history': {
                            'accepted': {'day': '06', 'month': '06', 'type': 'accepted', 'year': '1998'},
                            'retracted': {'day': '01', 'month': '06', 'type': 'retracted', 'year': '2012'},
                            'received': {'day': '05', 'month': '01', 'type': 'received', 'year': '1998'},
                            'rev-recd': {'day': '24', 'month': '05', 'type': 'rev-recd', 'year': '1998'},
                            'rev-request': {'day': '14', 'month': '03', 'type': 'rev-request', 'year': '1998'}
                        },
                    }
                ]
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])
