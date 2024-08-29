from unittest import TestCase

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation.errata import ErrataValidation, CorrectedArticleValidation


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
                "title": "errata",
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
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(item, expected[i])

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
                "title": "errata",
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
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(item, expected[i])


class CorrectedArticleValidationTest(TestCase):
    def test_validate_related_article_not_found(self):
        self.maxDiff = None
        self.xml_tree = get_xml_tree(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            </article>

            """
        )
        obtained = list(CorrectedArticleValidation(
            self.xml_tree,
            expected_article_type="correction",
            expected_related_article_type="correction-forward"
        ).validate_related_article())
        expected = [
            {
                "title": "errata",
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
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(item, expected[i])

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
        obtained = list(CorrectedArticleValidation(
            self.xml_tree,
            expected_article_type="correction",
            expected_related_article_type="correction-forward"
        ).validate_related_article())
        expected = [
            {
                "title": "errata",
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
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(item, expected[i])

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
        obtained = list(CorrectedArticleValidation(
            self.xml_tree,
            expected_article_type="correction",
            expected_related_article_type="correction-forward"
        ).validate_related_articles_and_history_dates())
        expected = [
            {
                "title": "errata",
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
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(item, expected[i])
