from unittest import TestCase
from lxml import etree

from packtools.sps.validation.article_ids import ArticleIdsValidation


class ArticleIdValidationTest(TestCase):
    def test_pub_type_id_other_has_five_digits(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
            <front>
            <article-meta>
            <article-id pub-id-type="other">1234</article-id>
            </article-meta>
            </front>
            </article>
            """
        )
        obtained = list(ArticleIdsValidation(xml_tree).pub_type_id_other_has_five_digits())
        expected = [
            {
                "advice": "Provide a value with five digits for <article-id pub-id-type='other'>",
                "data": None,
                "expected_value": "Five digits",
                "got_value": "1234",
                "item": "article-id",
                "message": "Got 1234, expected Five digits",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "response": "ERROR",
                "sub_item": "@pub-id-type='other'",
                "title": "pub-type-id=other has five digits",
                "validation_type": "format",
            }

        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_pub_type_id_other_is_numeric(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
            <front>
            <article-meta>
            <article-id pub-id-type="other">abcd</article-id>
            </article-meta>
            </front>
            </article>
            """
        )
        obtained = list(ArticleIdsValidation(xml_tree).pub_type_id_other_is_numeric())
        expected = [
            {
                "advice": "Provide a numeric value for <article-id pub-id-type='other'>",
                "data": None,
                "expected_value": "numeric value",
                "got_value": "abcd",
                "item": "article-id",
                "message": "Got abcd, expected numeric value",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "response": "ERROR",
                "sub_item": "@pub-id-type='other'",
                "title": "pub-type-id=other is numeric",
                "validation_type": "format",
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)


