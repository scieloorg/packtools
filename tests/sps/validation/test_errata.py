from unittest import TestCase

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation.related_articles import (
    RelatedArticleValidation,
    RelatedArticlesValidation,
)
from packtools.sps.models.v2.related_articles import RelatedArticles


class ErrataValidationTest(TestCase):
    def test_validate_related_article_not_found(self):
        self.maxDiff = None
        xml_tree = get_xml_tree(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <article-meta />
            </article>

            """
        )

        obtained = list(
            RelatedArticlesValidation(xml_tree).validate(
                correspondence_dict={"correction": ["corrected-article"]}
            )
        )

        expected = [
            {
                "title": "Related article type validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "correction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "related-article-type",
                "validation_type": "match",
                "response": "ERROR",
                "expected_value": ["corrected-article"],
                "got_value": [],
                "message": "Got [], expected ['corrected-article']",
                "advice": "The article-type: correction does not match the related-article-type: ["
                "'corrected-article'], provide one of the following items: ['corrected-article']",
                "data": None,
            }
        ]

        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_related_article_does_not_match(self):
        self.maxDiff = None
        xml_tree = get_xml_tree(
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
        related_article_dict = list(RelatedArticles(xml_tree).related_articles())[0]
        obtained = RelatedArticleValidation(
            related_article_dict
        ).validate_related_article_matches_article_type(
            expected_related_article_types=["corrected-article"]
        )

        expected = {
            "title": "Related article type validation",
            "parent": "article",
            "parent_id": None,
            "parent_article_type": "correction",
            "parent_lang": "en",
            "item": "related-article",
            "sub_item": "related-article-type",
            "validation_type": "match",
            "response": "ERROR",
            "expected_value": ["corrected-article"],
            "got_value": "correction-forward",
            "message": "Got correction-forward, expected ['corrected-article']",
            "advice": "The article-type: correction does not match the "
            "related-article-type: correction-forward, provide one of the "
            "following items: ['corrected-article']",
            "data": {
                "ext-link-type": "doi",
                "href": "10.5935/abc.20160032",
                "id": "RA1",
                "parent": "article",
                "parent_article_type": "correction",
                "parent_id": None,
                "parent_lang": "en",
                "related-article-type": "correction-forward",
                "text": "",
                "full_tag": '<related-article ext-link-type="doi" id="RA1" '
                'related-article-type="correction-forward" '
                'xlink:href="10.5935/abc.20160032"/>',
            },
        }

        self.assertDictEqual(obtained, expected)


class RelatedArticlesTest(TestCase):
    def test_validate_related_article_not_found(self):
        self.maxDiff = None
        xml_tree = get_xml_tree(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            </article>

            """
        )
        obtained = list(
            RelatedArticlesValidation(xml_tree).validate(
                correspondence_dict={"correction": ["corrected-article"]}
            )
        )

        expected = [
            {
                "title": "Related article type validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "correction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "related-article-type",
                "validation_type": "match",
                "response": "ERROR",
                "expected_value": ["corrected-article"],
                "got_value": [],
                "message": "Got [], expected ['corrected-article']",
                "advice": "The article-type: correction does not match the related-article-type: ["
                "'corrected-article'], provide one of the following items: ['corrected-article']",
                "data": None,
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_related_article_does_not_match(self):
        self.maxDiff = None
        xml_tree = get_xml_tree(
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
        related_article_dict = list(RelatedArticles(xml_tree).related_articles())[0]
        obtained = RelatedArticleValidation(
            related_article_dict
        ).validate_related_article_matches_article_type(
            expected_related_article_types=["corrected-article"]
        )

        expected = {
            "title": "Related article type validation",
            "parent": "article",
            "parent_id": None,
            "parent_article_type": "correction",
            "parent_lang": "en",
            "item": "related-article",
            "sub_item": "related-article-type",
            "validation_type": "match",
            "response": "ERROR",
            "expected_value": ["corrected-article"],
            "got_value": "correction-forward",
            "message": "Got correction-forward, expected ['corrected-article']",
            "advice": "The article-type: correction does not match the related-article-type: correction-forward, "
            "provide one of the following items: ['corrected-article']",
            "data": {
                "ext-link-type": "doi",
                "href": "10.5935/abc.20160032",
                "id": "RA1",
                "parent": "article",
                "parent_article_type": "correction",
                "parent_id": None,
                "parent_lang": "en",
                "related-article-type": "correction-forward",
                "text": "",
                "full_tag": '<related-article ext-link-type="doi" id="RA1" '
                'related-article-type="correction-forward" '
                'xlink:href="10.5935/abc.20160032"/>',
            },
        }

        self.assertDictEqual(obtained, expected)

    def test_validate_history_date(self):
        self.maxDiff = None
        xml_tree = get_xml_tree(
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
        related_article_dict = list(RelatedArticles(xml_tree).related_articles())[0]
        obtained = RelatedArticleValidation(related_article_dict).validate_history_date(
            expected_date_type="corrected",
            history_events={
                "received": {
                    "day": "05",
                    "month": "01",
                    "type": "received",
                    "year": "1998",
                }
            },
        )

        expected = {
            "title": "history date",
            "parent": "article",
            "parent_id": None,
            "parent_article_type": "correction",
            "parent_lang": "en",
            "item": "related-article / date",
            "sub_item": "@related-article-type=correction-forward / @date-type=corrected",
            "validation_type": "exist",
            "response": "ERROR",
            "expected_value": "corrected",
            "got_value": {
                "received": {
                    "day": "05",
                    "month": "01",
                    "type": "received",
                    "year": "1998",
                }
            },
            "message": "Got {'received': {'day': '05', 'month': '01', 'type': 'received', 'year': '1998'}}, expected corrected",
            "advice": "Provide the publication date of the corrected",
            "data": {
                "received": {
                    "day": "05",
                    "month": "01",
                    "type": "received",
                    "year": "1998",
                }
            },
        }

        self.assertDictEqual(obtained, expected)


class ArticleRetractedInFullValidationTest(TestCase):
    def test_validate_related_article_not_found(self):
        self.maxDiff = None
        xml_tree = get_xml_tree(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="retraction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            </article>

            """
        )
        obtained = list(
            RelatedArticlesValidation(xml_tree).validate(
                correspondence_dict={"retraction": ["retracted-article"]}
            )
        )

        expected = [
            {
                "title": "Related article type validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "retraction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "related-article-type",
                "validation_type": "match",
                "response": "ERROR",
                "expected_value": ["retracted-article"],
                "got_value": [],
                "message": "Got [], expected ['retracted-article']",
                "advice": "The article-type: retraction does not match the related-article-type: ["
                "'retracted-article'], provide one of the following items: ['retracted-article']",
                "data": None,
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_related_article_does_not_match(self):
        self.maxDiff = None
        xml_tree = get_xml_tree(
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
        related_article_dict = list(RelatedArticles(xml_tree).related_articles())[0]
        obtained = RelatedArticleValidation(
            related_article_dict
        ).validate_related_article_matches_article_type(
            expected_related_article_types=["retracted-article"]
        )

        expected = {
            "title": "Related article type validation",
            "parent": "article",
            "parent_id": None,
            "parent_article_type": "retraction",
            "parent_lang": "en",
            "item": "related-article",
            "sub_item": "related-article-type",
            "validation_type": "match",
            "response": "ERROR",
            "expected_value": ["retracted-article"],
            "got_value": "commentary",
            "message": "Got commentary, expected ['retracted-article']",
            "advice": "The article-type: retraction does not match the related-article-type: commentary, "
            "provide one of the following items: ['retracted-article']",
            "data": {
                "ext-link-type": "doi",
                "href": "10.5935/abc.20150051",
                "id": "RA2",
                "parent": "article",
                "parent_article_type": "retraction",
                "parent_id": None,
                "parent_lang": "en",
                "related-article-type": "commentary",
                "text": "",
                "full_tag": '<related-article ext-link-type="doi" id="RA2" '
                'related-article-type="commentary" '
                'xlink:href="10.5935/abc.20150051"/>',
            },
        }

        self.assertDictEqual(obtained, expected)

    def test_validate_history_date(self):
        self.maxDiff = None
        xml_tree = get_xml_tree(
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
        related_article_dict = list(RelatedArticles(xml_tree).related_articles())[0]
        obtained = RelatedArticleValidation(related_article_dict).validate_history_date(
            expected_date_type="corrected",
            history_events={
                "received": {
                    "day": "05",
                    "month": "01",
                    "type": "received",
                    "year": "1998",
                }
            },
        )

        expected = {
            "title": "history date",
            "parent": "article",
            "parent_id": None,
            "parent_article_type": "retraction",
            "parent_lang": "en",
            "item": "related-article / date",
            "sub_item": "@related-article-type=retraction-forward / @date-type=corrected",
            "validation_type": "exist",
            "response": "ERROR",
            "expected_value": "corrected",
            "got_value": {
                "received": {
                    "day": "05",
                    "month": "01",
                    "type": "received",
                    "year": "1998",
                }
            },
            "message": "Got {'received': {'day': '05', 'month': '01', 'type': 'received', 'year': '1998'}}, expected corrected",
            "advice": "Provide the publication date of the corrected",
            "data": {
                "received": {
                    "day": "05",
                    "month": "01",
                    "type": "received",
                    "year": "1998",
                }
            },
        }

        self.assertDictEqual(obtained, expected)


class ArticlePartiallyRetractedValidationTest(TestCase):
    def test_validate_related_article_not_found(self):
        self.maxDiff = None
        xml_tree = get_xml_tree(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="partial-retraction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            </article>

            """
        )
        obtained = list(
            RelatedArticlesValidation(xml_tree).validate(
                correspondence_dict={"partial-retraction": ["retracted-article"]}
            )
        )

        expected = [
            {
                "title": "Related article type validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "partial-retraction",
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "related-article-type",
                "validation_type": "match",
                "response": "ERROR",
                "expected_value": ["retracted-article"],
                "got_value": [],
                "message": "Got [], expected ['retracted-article']",
                "advice": "The article-type: partial-retraction does not match the related-article-type: ["
                "'retracted-article'], provide one of the following items: ['retracted-article']",
                "data": None,
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_related_article_does_not_match(self):
        self.maxDiff = None
        xml_tree = get_xml_tree(
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
        related_article_dict = list(RelatedArticles(xml_tree).related_articles())[0]
        obtained = RelatedArticleValidation(
            related_article_dict
        ).validate_related_article_matches_article_type(
            expected_related_article_types=["retracted-article"]
        )

        expected = {
            "title": "Related article type validation",
            "parent": "article",
            "parent_id": None,
            "parent_article_type": "partial-retraction",
            "parent_lang": "en",
            "item": "related-article",
            "sub_item": "related-article-type",
            "validation_type": "match",
            "response": "ERROR",
            "expected_value": ["retracted-article"],
            "got_value": "commentary",
            "message": "Got commentary, expected ['retracted-article']",
            "advice": "The article-type: partial-retraction does not match the related-article-type: commentary, "
            "provide one of the following items: ['retracted-article']",
            "data": {
                "ext-link-type": "doi",
                "href": "10.5935/abc.20150051",
                "id": "RA2",
                "parent": "article",
                "parent_article_type": "partial-retraction",
                "parent_id": None,
                "parent_lang": "en",
                "related-article-type": "commentary",
                "text": "",
                "full_tag": '<related-article ext-link-type="doi" id="RA2" '
                'related-article-type="commentary" '
                'xlink:href="10.5935/abc.20150051"/>',
            },
        }

        self.assertDictEqual(obtained, expected)

    def test_validate_count_related_article_count_date(self):
        self.maxDiff = None
        xml_tree = get_xml_tree(
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
        related_article_dict = list(RelatedArticles(xml_tree).related_articles())[0]
        obtained = RelatedArticleValidation(related_article_dict).validate_history_date(
            expected_date_type="retracted",
            history_events={
                "received": {
                    "day": "05",
                    "month": "01",
                    "type": "received",
                    "year": "1998",
                }
            },
        )

        expected = {
            "title": "history date",
            "parent": "article",
            "parent_id": None,
            "parent_article_type": "partial-retraction",
            "parent_lang": "en",
            "item": "related-article / date",
            "sub_item": "@related-article-type=partial-retraction / @date-type=retracted",
            "validation_type": "exist",
            "response": "ERROR",
            "expected_value": "retracted",
            "got_value": {
                "received": {
                    "day": "05",
                    "month": "01",
                    "type": "received",
                    "year": "1998",
                }
            },
            "message": "Got {'received': {'day': '05', 'month': '01', 'type': 'received', 'year': '1998'}}, expected retracted",
            "advice": "Provide the publication date of the retracted",
            "data": {
                "received": {
                    "day": "05",
                    "month": "01",
                    "type": "received",
                    "year": "1998",
                }
            },
        }

        self.assertDictEqual(obtained, expected)
