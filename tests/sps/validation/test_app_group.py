import unittest
from lxml import etree

from packtools.sps.validation.app_group import AppValidation


class AppValidationTest(unittest.TestCase):
    def test_app_validation_no_app_elements(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<p>Some text content without apps.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(AppValidation(xmltree).validate_app_existence())

        expected = [
            {
                "title": "validation of <app> elements",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "app-group",
                "sub_item": "app",
                "validation_type": "exist",
                "response": "WARNING",
                "expected_value": "<app> element",
                "got_value": None,
                "message": "Got None, expected <app> element",
                "advice": "Consider adding an <app> element to include additional content such as supplementary materials or appendices.",
                "data": None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_app_validation_with_app_elements(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<app-group>"
            '<app id="app1">'
            "<label>Appendix 1</label>"
            "<p>Some supplementary content.</p>"
            "</app>"
            "<alternatives>"
            '<app id="app1-alt1">'
            "<p>Alternative content for Appendix 1.</p>"
            "</app>"
            "</alternatives>"
            "</app-group>"
            "</body>"
            "</article>"
        )
        obtained = list(AppValidation(xmltree).validate_app_existence())

        expected = [
            {
                "title": "validation of <app> elements",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "app-group",
                "sub_item": "app",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "app1",
                "got_value": "app1",
                "message": "Got app1, expected app1",
                "advice": None,
                "data": {
                    "app_id": "app1",
                    "app_label": "Appendix 1",
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
