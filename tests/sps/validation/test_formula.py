import unittest
from lxml import etree

from packtools.sps.validation.formula import FormulaValidation


class FormulaValidationTest(unittest.TestCase):
    def test_formula_validation_no_formula_elements(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<p>Some text content without formulas.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(FormulaValidation(xmltree).validate_formula_existence())

        expected = [
            {
                "title": "validation of <formula> elements",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "formula",
                "sub_item": None,
                "validation_type": "exist",
                "response": "WARNING",
                "expected_value": "<formula> element",
                "got_value": None,
                "message": "Got None, expected <formula> element",
                "advice": "Include <formula> elements to properly represent mathematical expressions in the content.",
                "data": None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_formula_validation_with_disp_formula_elements(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<disp-formula id="d01">'
            "<label>Formula 1</label>"
            "<alternatives>"
            '<graphic xlink:href="image1-lowres.png" mime-subtype="low-resolution"/>'
            '<graphic xlink:href="image1-highres.png" mime-subtype="high-resolution"/>'
            "</alternatives>"
            "</disp-formula>"
            "</body>"
            "</article>"
        )
        obtained = list(FormulaValidation(xmltree).validate_formula_existence())

        expected = [
            {
                "title": "validation of <formula> elements",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "disp-formula",
                "sub_item": None,
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "d01",
                "got_value": "d01",
                "message": "Got d01, expected d01",
                "advice": None,
                "data": {
                    "alternative_parent": "disp-formula",
                    "formula_id": "d01",
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

    def test_formula_validation_with_inline_formula_elements(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<inline-formula id="i01">'
            "<label>Formula 1</label>"
            "<alternatives>"
            '<graphic xlink:href="image1-lowres.png" mime-subtype="low-resolution"/>'
            '<graphic xlink:href="image1-highres.png" mime-subtype="high-resolution"/>'
            "</alternatives>"
            "</inline-formula>"
            "</body>"
            "</article>"
        )
        obtained = list(FormulaValidation(xmltree).validate_formula_existence())

        expected = [
            {
                "title": "validation of <formula> elements",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "inline-formula",
                "sub_item": None,
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "i01",
                "got_value": "i01",
                "message": "Got i01, expected i01",
                "advice": None,
                "data": {
                    "alternative_parent": "inline-formula",
                    "formula_id": "i01",
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
