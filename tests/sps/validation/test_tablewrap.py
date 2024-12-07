import unittest
from lxml import etree

from packtools.sps.validation.tablewrap import ArticleTableWrapValidation


class TableWrapValidationTest(unittest.TestCase):
    def test_validate_absent(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<p>Some text content without table wraps.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree, rules={"absent_error_level": "WARNING"}
            ).validate()
        )

        expected = [
            {
                "title": "table-wrap presence",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "table-wrap",
                "sub_item": None,
                "validation_type": "exist",
                "response": "WARNING",
                "expected_value": "<table-wrap> element",
                "got_value": None,
                "message": "Got None, expected <table-wrap> element",
                "advice": "Add <table-wrap> element to properly illustrate the content.",
                "data": None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_id(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<table-wrap>"
            "<label>Table 1</label>"
            "<caption>Table caption</caption>"
            "<table>Table codification</table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree, rules={"id_error_level": "CRITICAL"}
            ).validate()
        )

        expected = [
            {
                "title": "id",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "table-wrap",
                "sub_item": "id",
                "validation_type": "exist",
                "response": "CRITICAL",
                "expected_value": "id",
                "got_value": None,
                "message": "Got None, expected id",
                "advice": "Identify the id",
                "data": {
                    "alternative_parent": "table-wrap",
                    "table_wrap_id": None,
                    "label": "Table 1",
                    "caption": "Table caption",
                    "footnote": "",
                    "footnote_id": None,
                    "footnote_label": None,
                    "alternative_elements": [],
                    "table": "Table codification",
                    "graphic": None,
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_label(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<caption>Table caption</caption>"
            "<table>Table codification</table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={
                    "label_error_level": "CRITICAL",
                },
            ).validate()
        )

        expected = [
            {
                "title": "label",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "table-wrap",
                "sub_item": "label",
                "validation_type": "exist",
                "response": "CRITICAL",
                "expected_value": "label",
                "got_value": None,
                "message": "Got None, expected label",
                "advice": "Identify the label",
                "data": {
                    "alternative_parent": "table-wrap",
                    "table_wrap_id": "t01",
                    "label": None,
                    "caption": "Table caption",
                    "footnote": "",
                    "footnote_id": None,
                    "footnote_label": None,
                    "alternative_elements": [],
                    "table": "Table codification",
                    "graphic": None,
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_caption(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<table>Table codification</table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={
                    "caption_error_level": "CRITICAL",
                },
            ).validate()
        )

        expected = [
            {
                "title": "caption",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "table-wrap",
                "sub_item": "caption",
                "validation_type": "exist",
                "response": "CRITICAL",
                "expected_value": "caption",
                "got_value": None,
                "message": "Got None, expected caption",
                "advice": "Identify the caption",
                "data": {
                    "alternative_parent": "table-wrap",
                    "table_wrap_id": "t01",
                    "label": "Table 1",
                    "caption": "",
                    "footnote": "",
                    "footnote_id": None,
                    "footnote_label": None,
                    "alternative_elements": [],
                    "table": "Table codification",
                    "graphic": None,
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_table(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption>Table caption</caption>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={"table_error_level": "CRITICAL"},
            ).validate()
        )

        expected = [
            {
                "title": "table",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "table-wrap",
                "sub_item": "table",
                "validation_type": "exist",
                "response": "CRITICAL",
                "expected_value": "table",
                "got_value": None,
                "message": "Got None, expected table",
                "advice": "Identify the table",
                "data": {
                    "alternative_parent": "table-wrap",
                    "table_wrap_id": "t01",
                    "label": "Table 1",
                    "caption": "Table caption",
                    "footnote": "",
                    "footnote_id": None,
                    "footnote_label": None,
                    "alternative_elements": [],
                    "graphic": None,
                    "table": None,
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_required_alternatives(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption>Table caption</caption>"
            "<table>table codification</table>"
            '<graphic xlink:href="1980-5381-neco-28-02-579-gt05.svg"/>'
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={"alternatives_error_level": "CRITICAL"},
            ).validate()
        )

        expected = [
            {
                "title": "alternatives",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "table-wrap",
                "sub_item": "alternatives",
                "validation_type": "exist",
                "response": "CRITICAL",
                "expected_value": "alternatives",
                "got_value": None,
                "message": "Got None, expected alternatives",
                "advice": "Identify the alternatives",
                "data": {
                    "alternative_parent": "table-wrap",
                    "table_wrap_id": "t01",
                    "label": "Table 1",
                    "caption": "Table caption",
                    "footnote": "",
                    "footnote_id": None,
                    "footnote_label": None,
                    "alternative_elements": [],
                    "graphic": "1980-5381-neco-28-02-579-gt05.svg",
                    "table": "table codification",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_not_required_alternatives(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption>Table caption</caption>"
            "<alternatives>"
            "<table>table codification</table>"
            "</alternatives>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={"alternatives_error_level": "CRITICAL"},
            ).validate()
        )

        expected = [
            {
                "title": "alternatives",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "table-wrap",
                "sub_item": "alternatives",
                "validation_type": "exist",
                "response": "CRITICAL",
                "expected_value": None,
                "got_value": "alternatives",
                "message": "Got alternatives, expected None",
                "advice": "Remove the alternatives",
                "data": {
                    "alternative_parent": "table-wrap",
                    "table_wrap_id": "t01",
                    "label": "Table 1",
                    "caption": "Table caption",
                    "footnote": "",
                    "footnote_id": None,
                    "footnote_label": None,
                    "alternative_elements": ["table"],
                    "graphic": None,
                    "table": "table codification",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


if __name__ == "__main__":
    unittest.main()
