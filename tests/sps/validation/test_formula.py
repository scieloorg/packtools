import unittest
from lxml import etree

from packtools.sps.validation.formula import ArticleDispFormulaValidation, ArticleInlineFormulaValidation


class ArticleFormulaValidationTest(unittest.TestCase):
    def test_validate_absent_disp_formula(self):
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
            ArticleDispFormulaValidation(
                xml_tree=xml_tree, rules={"absent_error_level": "WARNING"}
            ).validate()
        )

        expected = [
            {
                "title": "disp-formula",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "disp-formula",
                "sub_item": None,
                "validation_type": "exist",
                "response": "WARNING",
                "expected_value": "disp-formula",
                "got_value": None,
                "message": "Got None, expected disp-formula",
                "advice": "Add <disp-formula> elements to properly represent mathematical expressions in the content.",
                "data": None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_absent_inline_formula(self):
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
            ArticleInlineFormulaValidation(
                xml_tree=xml_tree, rules={"absent_error_level": "WARNING"}
            ).validate()
        )

        expected = [
            {
                "title": "inline-formula",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "inline-formula",
                "sub_item": None,
                "validation_type": "exist",
                "response": "WARNING",
                "expected_value": "inline-formula",
                "got_value": None,
                "message": "Got None, expected inline-formula",
                "advice": "Add <inline-formula> elements to properly represent mathematical expressions in the content.",
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
            '<mml:math id="e03">'
            "<mml:mrow>"
            "<mml:msup>"
            '<mml:mover accent="true">'
            "<mml:mi>σ</mml:mi>"
            "<mml:mo>ˆ</mml:mo>"
            "</mml:mover>"
            "<mml:mn>2</mml:mn>"
            "</mml:msup>"
            "</mml:mrow>"
            "</mml:math>"
            '<graphic xlink:href="image1-lowres.png" mime-subtype="low-resolution"/>'
            '<graphic xlink:href="image1-highres.png" mime-subtype="high-resolution"/>'
            "</alternatives>"
            "</disp-formula>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleDispFormulaValidation(
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
                    "id": None,
                    "label": "Formula 1",
                    "alternative_elements": ['{http://www.w3.org/1998/Math/MathML}math', "graphic", "graphic"],
                    "graphic": ["image1-lowres.png", "image1-highres.png"],
                    "mml_math": 'σˆ2',
                    "tex_math": None,
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

    def test_validate_without_label_in_disp_formula(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<disp-formula id='e10'>"
            "<alternatives>"
            '<mml:math id="e03">'
            "<mml:mrow>"
            "<mml:msup>"
            '<mml:mover accent="true">'
            "<mml:mi>σ</mml:mi>"
            "<mml:mo>ˆ</mml:mo>"
            "</mml:mover>"
            "<mml:mn>2</mml:mn>"
            "</mml:msup>"
            "</mml:mrow>"
            "</mml:math>"
            '<graphic xlink:href="image1-lowres.png" mime-subtype="low-resolution"/>'
            '<graphic xlink:href="image1-highres.png" mime-subtype="high-resolution"/>'
            "</alternatives>"
            "</disp-formula>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleDispFormulaValidation(
                    xml_tree=xml_tree, rules={"label_error_level": "WARNING"}
            ).validate()
        )

        expected = [
            {
                "title": "label",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "label",
                "sub_item": None,
                "validation_type": "exist",
                "response": "WARNING",
                "expected_value": "label",
                "got_value": None,
                "message": "Got None, expected label",
                "advice": "Identify the label",
                "data": {
                    "alternative_parent": "disp-formula",
                    "id": "e10",
                    "label": None,
                    "alternative_elements": ['{http://www.w3.org/1998/Math/MathML}math', "graphic", "graphic"],
                    "graphic": ["image1-lowres.png", "image1-highres.png"],
                    "mml_math": 'σˆ2',
                    "tex_math": None,
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

    def test_validate_without_codification_in_disp_formula(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<disp-formula id='e10'>"
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
            ArticleDispFormulaValidation(
                    xml_tree=xml_tree, rules={"codification_error_level": "CRITICAL"}
            ).validate()
        )

        expected = [
            {
                "title": "mml:math or tex-math",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "mml:math or tex-math",
                "sub_item": None,
                "validation_type": "exist",
                "response": "CRITICAL",
                "expected_value": "mml:math or tex-math",
                "got_value": None,
                "message": "Got None, expected mml:math or tex-math",
                "advice": "Identify the mml:math or tex-math",
                "data": {
                    "alternative_parent": "disp-formula",
                    "id": "e10",
                    "label": "Formula 1",
                    "alternative_elements": ["graphic", "graphic"],
                    "graphic": ["image1-lowres.png", "image1-highres.png"],
                    "mml_math": None,
                    "tex_math": None,
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

    def test_validate_without_codification_in_inline_formula(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<inline-formula id='e10'>"
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
            ArticleInlineFormulaValidation(
                xml_tree=xml_tree, rules={"codification_error_level": "CRITICAL"}
            ).validate()
        )

        expected = [
            {
                "title": "mml:math or tex-math",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "mml:math or tex-math",
                "sub_item": None,
                "validation_type": "exist",
                "response": "CRITICAL",
                "expected_value": "mml:math or tex-math",
                "got_value": None,
                "message": "Got None, expected mml:math or tex-math",
                "advice": "Identify the mml:math or tex-math",
                "data": {
                    "alternative_parent": "inline-formula",
                    "id": "e10",
                    "label": "Formula 1",
                    "alternative_elements": ["graphic", "graphic"],
                    "graphic": ["image1-lowres.png", "image1-highres.png"],
                    "mml_math": None,
                    "tex_math": None,
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

    def test_validate_alternatives_required_in_disp_formula(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<disp-formula id='e10'>"
            "<label>Formula 1</label>"
            '<mml:math id="e03">'
            "<mml:mrow>"
            "<mml:msup>"
            '<mml:mover accent="true">'
            "<mml:mi>σ</mml:mi>"
            "<mml:mo>ˆ</mml:mo>"
            "</mml:mover>"
            "<mml:mn>2</mml:mn>"
            "</mml:msup>"
            "</mml:mrow>"
            "</mml:math>"
            '<graphic xlink:href="image1-lowres.png" mime-subtype="low-resolution"/>'
            "</disp-formula>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleDispFormulaValidation(
                    xml_tree=xml_tree, rules={"alternatives_error_level": "CRITICAL"}
            ).validate()
        )

        expected = [
            {
                "title": "alternatives",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "alternatives",
                "sub_item": None,
                "validation_type": "exist",
                "response": "CRITICAL",
                "expected_value": "alternatives",
                "got_value": None,
                "message": "Got None, expected alternatives",
                "advice": "Identify the alternatives",
                "data": {
                    "alternative_parent": "disp-formula",
                    "id": "e10",
                    "label": "Formula 1",
                    "alternative_elements": [],
                    "graphic": ["image1-lowres.png"],
                    "mml_math": 'σˆ2',
                    "tex_math": None,
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

    def test_validate_alternatives_not_required_in_disp_formula(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<disp-formula id='e10'>"
            "<label>Formula 1</label>"
            "<alternatives>"
            '<mml:math id="e03">'
            "<mml:mrow>"
            "<mml:msup>"
            '<mml:mover accent="true">'
            "<mml:mi>σ</mml:mi>"
            "<mml:mo>ˆ</mml:mo>"
            "</mml:mover>"
            "<mml:mn>2</mml:mn>"
            "</mml:msup>"
            "</mml:mrow>"
            "</mml:math>"
            "</alternatives>"
            "</disp-formula>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleDispFormulaValidation(
                    xml_tree=xml_tree, rules={"alternatives_error_level": "CRITICAL"}
            ).validate()
        )

        expected = [
            {
                "title": "alternatives",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "alternatives",
                "sub_item": None,
                "validation_type": "exist",
                "response": "CRITICAL",
                "expected_value": None,
                "got_value": "alternatives",
                "message": "Got alternatives, expected None",
                "advice": "Remove the alternatives",
                "data": {
                    "alternative_parent": "disp-formula",
                    "id": "e10",
                    "label": "Formula 1",
                    "alternative_elements": ['{http://www.w3.org/1998/Math/MathML}math'],
                    "graphic": [],
                    "mml_math": 'σˆ2',
                    "tex_math": None,
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
