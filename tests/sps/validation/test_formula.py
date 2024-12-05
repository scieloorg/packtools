import unittest
from lxml import etree

from packtools.sps.validation.formula import ArticleFormulaValidation


class ArticleFormulaValidationTest(unittest.TestCase):
    def test_validate_absent(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<p>Some text content without formulas.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleFormulaValidation(
                xml_tree=xml_tree, rules={"absent_error_level": "WARNING"}
            ).validate()
        )

        expected = [
            {
                "title": "formula",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "formula",
                "sub_item": None,
                "validation_type": "exist",
                "response": "WARNING",
                "expected_value": "formula",
                "got_value": None,
                "message": "Got None, expected formula",
                "advice": "Add <formula> elements to properly represent mathematical expressions in the content.",
                "data": None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_without_id_in_disp_formula(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<disp-formula>"
            "<label>Formula 1</label>"
            "<alternatives>"
            '<graphic xlink:href="image1-lowres.png" mime-subtype="low-resolution"/>'
            '<graphic xlink:href="image1-highres.png" mime-subtype="high-resolution"/>'
            "</alternatives>"
            "</disp-formula>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleFormulaValidation(
                xml_tree=xml_tree, rules={"id_error_level": "CRITICAL"}
            ).validate()
        )

        expected = [
            {
                "title": "@id",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "@id",
                "sub_item": None,
                "validation_type": "exist",
                "response": "CRITICAL",
                "expected_value": "@id",
                "got_value": None,
                "message": "Got None, expected @id",
                "advice": "Identify the @id",
                "data": {
                    "alternative_parent": "disp-formula",
                    "formula_id": None,
                    "formula_label": "Formula 1",
                    "alternative_elements": ["graphic", "graphic"],
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

    def test_validate_without_id_in_inline_formula(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<inline-formula>"
            "<label>Formula 1</label>"
            "<alternatives>"
            '<graphic xlink:href="image1-lowres.png" mime-subtype="low-resolution"/>'
            '<graphic xlink:href="image1-highres.png" mime-subtype="high-resolution"/>'
            "</alternatives>"
            "</inline-formula>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleFormulaValidation(
                xml_tree=xml_tree, rules={"id_error_level": "CRITICAL"}
            ).validate()
        )

        expected = [
            {
                "title": "@id",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "@id",
                "sub_item": None,
                "validation_type": "exist",
                "response": "CRITICAL",
                "expected_value": "@id",
                "got_value": None,
                "message": "Got None, expected @id",
                "advice": "Identify the @id",
                "data": {
                    "alternative_parent": "inline-formula",
                    "formula_id": None,
                    "formula_label": "Formula 1",
                    "alternative_elements": ["graphic", "graphic"],
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
