import unittest
from lxml import etree

from packtools.sps.validation.tablewrap import TableWrapValidation


class TableWrapValidationTest(unittest.TestCase):
    def test_tablewrap_validation_no_tablewrap_elements(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<p>Some text content without table wraps.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(TableWrapValidation(xmltree).validate_tablewrap_existence())

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

    def test_tablewrap_validation_with_tablewrap_elements(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            '<caption>Table caption</caption>'
            "<alternatives>"
            '<graphic xlink:href="image1-lowres.png" mime-subtype="low-resolution"/>'
            '<graphic xlink:href="image1-highres.png" mime-subtype="high-resolution"/>'
            "</alternatives>"
            "</table-wrap>"
            "</body>"
            '<sub-article article-type="translation" xml:lang="en">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1:</label>"
            "<caption>Table caption</caption>"
            "<alternatives>"
            '<graphic xlink:href="image1-lowres.png" mime-subtype="low-resolution"/>'
            '<graphic xlink:href="image1-highres.png" mime-subtype="high-resolution"/>'
            "</alternatives>"
            "</table-wrap>"
            "</body>"
            "</sub-article>"
            "</article>"
        )
        obtained = list(TableWrapValidation(xmltree).validate_tablewrap_existence())

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
                "response": "OK",
                'expected_value': '<table-wrap> element',
                'got_value': '<table-wrap xmlns:xlink="http://www.w3.org/1999/xlink" '
                             'xmlns:mml="http://www.w3.org/1998/Math/MathML" '
                             'id="t01"><label>Table 1</label><caption>Table '
                             'caption</caption><alternatives><graphic '
                             'xlink:href="image1-lowres.png" '
                             'mime-subtype="low-resolution"/><graphic '
                             'xlink:href="image1-highres.png" '
                             'mime-subtype="high-resolution"/></alternatives></table-wrap>',

                'message': 'Got <table-wrap xmlns:xlink="http://www.w3.org/1999/xlink" '
                           'xmlns:mml="http://www.w3.org/1998/Math/MathML" '
                           'id="t01"><label>Table 1</label><caption>Table '
                           'caption</caption><alternatives><graphic '
                           'xlink:href="image1-lowres.png" '
                           'mime-subtype="low-resolution"/><graphic '
                           'xlink:href="image1-highres.png" '
                           'mime-subtype="high-resolution"/></alternatives></table-wrap>, '
                           'expected <table-wrap> element',
                "advice": None,
                "data": {
                    "alternative_parent": "table-wrap",
                    "table_wrap_id": "t01",
                    "label": "Table 1",
                    "caption": "Table caption",
                    "footnote": "",
                    "footnote_id": None,
                    "footnote_label": None,
                    "alternative_elements": ["graphic", "graphic"],
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        # Remover a chave "node" dos dados obtidos
        for item in obtained:
            if item.get("data"):
                item["data"].pop("node", None)

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


if __name__ == "__main__":
    unittest.main()
