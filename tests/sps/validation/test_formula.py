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
                "advice": "No <disp-formula> found in XML",
                "data": None,
                "msg_text": "Got {obtained}, expected {expected}",
                "msg_params": {"obtained": "None", "expected": "disp-formula"},
                "adv_text": "No <disp-formula> found in XML",
                "adv_params": {},
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
                "advice": "No <inline-formula> found in XML",
                "data": None,
                "msg_text": "Got {obtained}, expected {expected}",
                "msg_params": {"obtained": "None", "expected": "inline-formula"},
                "adv_text": "No <inline-formula> found in XML",
                "adv_params": {},
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
                "advice": 'Add the formula ID with id="" in <disp-formula>: <disp-formula id="">. Consult SPS documentation for more detail.',
                "data": {
                    "alternative_parent": "disp-formula",
                    "id": None,
                    "label": "Formula 1",
                    "alternative_elements": ['{http://www.w3.org/1998/Math/MathML}math', "graphic", "graphic"],
                    "graphic": ["image1-lowres.png", "image1-highres.png"],
                    "mml_math": 'σˆ2',
                    "mml_math_id": "e03",
                    "tex_math": None,
                    "tex_math_id": None,
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
                "msg_text": "Got {obtained}, expected {expected}",
                "msg_params": {"obtained": "None", "expected": "@id"},
                "adv_text": 'Add the formula ID with id="" in <disp-formula>: <disp-formula id="">. Consult SPS documentation for more detail.',
                "adv_params": {},
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_validate_wrong_id_prefix_in_disp_formula(self):
        """Test validation of wrong prefix in disp-formula @id"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<disp-formula id="f10">'
            "<label>Formula 1</label>"
            '<mml:math id="m03">'
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
            "</disp-formula>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleDispFormulaValidation(
                xml_tree=xml_tree, rules={"id_prefix_error_level": "ERROR"}
            ).validate()
        )

        # Deve retornar erro apenas no prefixo (ID existe, mas prefixo errado)
        errors = [item for item in obtained if item["title"] == "@id prefix"]
        self.assertEqual(len(errors), 1)

        error = errors[0]
        self.assertEqual(error["response"], "ERROR")
        self.assertEqual(error["got_value"], "f10")
        self.assertIn('must start with prefix "e"', error["advice"])

    def test_validate_without_mml_math_id_in_disp_formula(self):
        """Test validation of missing @id in mml:math within disp-formula"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<disp-formula id="e10">'
            "<label>Formula 1</label>"
            "<mml:math>"
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
            "</disp-formula>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleDispFormulaValidation(
                xml_tree=xml_tree, rules={"mml_math_id_error_level": "CRITICAL"}
            ).validate()
        )

        # Deve retornar erro no mml:math @id
        errors = [item for item in obtained if item["title"] == "mml:math @id"]
        self.assertEqual(len(errors), 1)

        error = errors[0]
        self.assertEqual(error["response"], "CRITICAL")
        self.assertIsNone(error["got_value"])
        self.assertIn("Add the @id attribute in <mml:math>", error["advice"])

    def test_validate_wrong_mml_math_id_prefix_in_disp_formula(self):
        """Test validation of wrong prefix in mml:math @id within disp-formula"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<disp-formula id="e10">'
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
            "</disp-formula>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleDispFormulaValidation(
                xml_tree=xml_tree, rules={"mml_math_id_prefix_error_level": "ERROR"}
            ).validate()
        )

        # Deve retornar erro no prefixo do mml:math
        errors = [item for item in obtained if item["title"] == "mml:math @id prefix"]
        self.assertEqual(len(errors), 1)

        error = errors[0]
        self.assertEqual(error["response"], "ERROR")
        self.assertEqual(error["got_value"], "e03")
        self.assertIn('must start with prefix "m"', error["advice"])

    def test_validate_without_label_in_disp_formula(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<disp-formula id='e10'>"
            "<alternatives>"
            '<mml:math id="m03">'
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

        # Buscar apenas o erro de label
        errors = [item for item in obtained if item["title"] == "label"]
        self.assertEqual(len(errors), 1)

        error = errors[0]
        self.assertEqual(error["response"], "WARNING")
        self.assertIsNone(error["got_value"])
        self.assertIn("Mark each label with <label>", error["advice"])

    def test_validate_without_codification_in_disp_formula(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<disp-formula id='e10'>"
            "<label>Formula 1</label>"
            '<graphic xlink:href="image1-lowres.png" mime-subtype="low-resolution"/>'
            "</disp-formula>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleDispFormulaValidation(
                xml_tree=xml_tree, rules={"codification_error_level": "CRITICAL"}
            ).validate()
        )

        # Buscar apenas o erro de codificação
        errors = [item for item in obtained if item["title"] == "mml:math or tex-math"]
        self.assertEqual(len(errors), 1)

        error = errors[0]
        self.assertEqual(error["response"], "CRITICAL")
        self.assertIn("not found codification", error["got_value"])
        self.assertIn("Mark each formula codification", error["advice"])

    def test_validate_without_id_in_inline_formula(self):
        """Test validation of missing @id in inline-formula"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<p>Some text with <inline-formula>"
            '<mml:math id="m03">'
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
            "</inline-formula> in text.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleInlineFormulaValidation(
                xml_tree=xml_tree, rules={"id_error_level": "CRITICAL"}
            ).validate()
        )

        # Deve retornar erro de ID ausente
        errors = [item for item in obtained if item["title"] == "@id"]
        self.assertEqual(len(errors), 1)

        error = errors[0]
        self.assertEqual(error["response"], "CRITICAL")
        self.assertIsNone(error["got_value"])
        self.assertIn('Add the formula ID with id=""', error["advice"])

    def test_validate_wrong_id_prefix_in_inline_formula(self):
        """Test validation of wrong prefix in inline-formula @id"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p>Some text with <inline-formula id="f10">'
            '<mml:math id="m03">'
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
            "</inline-formula> in text.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleInlineFormulaValidation(
                xml_tree=xml_tree, rules={"id_prefix_error_level": "ERROR"}
            ).validate()
        )

        # Deve retornar erro no prefixo
        errors = [item for item in obtained if item["title"] == "@id prefix"]
        self.assertEqual(len(errors), 1)

        error = errors[0]
        self.assertEqual(error["response"], "ERROR")
        self.assertEqual(error["got_value"], "f10")
        self.assertIn('must start with prefix "e"', error["advice"])

    def test_validate_without_mml_math_id_in_inline_formula(self):
        """Test validation of missing @id in mml:math within inline-formula"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p>Some text with <inline-formula id="e10">'
            "<mml:math>"
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
            "</inline-formula> in text.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleInlineFormulaValidation(
                xml_tree=xml_tree, rules={"mml_math_id_error_level": "CRITICAL"}
            ).validate()
        )

        # Deve retornar erro no mml:math @id
        errors = [item for item in obtained if item["title"] == "mml:math @id"]
        self.assertEqual(len(errors), 1)

        error = errors[0]
        self.assertEqual(error["response"], "CRITICAL")
        self.assertIsNone(error["got_value"])
        self.assertIn("Add the @id attribute in <mml:math>", error["advice"])

    def test_validate_wrong_mml_math_id_prefix_in_inline_formula(self):
        """Test validation of wrong prefix in mml:math @id within inline-formula"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p>Some text with <inline-formula id="e10">'
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
            "</inline-formula> in text.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleInlineFormulaValidation(
                xml_tree=xml_tree, rules={"mml_math_id_prefix_error_level": "ERROR"}
            ).validate()
        )

        # Deve retornar erro no prefixo do mml:math
        errors = [item for item in obtained if item["title"] == "mml:math @id prefix"]
        self.assertEqual(len(errors), 1)

        error = errors[0]
        self.assertEqual(error["response"], "ERROR")
        self.assertEqual(error["got_value"], "e03")
        self.assertIn('must start with prefix "m"', error["advice"])

    def test_validate_without_codification_in_inline_formula(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p>Some text with <inline-formula id="e10">'
            '<graphic xlink:href="image1-lowres.png" mime-subtype="low-resolution"/>'
            "</inline-formula> in text.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleInlineFormulaValidation(
                xml_tree=xml_tree, rules={"codification_error_level": "CRITICAL"}
            ).validate()
        )

        # Buscar apenas o erro de codificação
        errors = [item for item in obtained if item["title"] == "mml:math or tex-math"]
        self.assertEqual(len(errors), 1)

        error = errors[0]
        self.assertEqual(error["response"], "CRITICAL")
        self.assertIn("not found codification", error["got_value"])
        self.assertIn("Mark each formula codification", error["advice"])

    def test_validate_alternatives_required_in_disp_formula(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<disp-formula id='e10'>"
            "<label>Formula 1</label>"
            '<mml:math id="m03">'
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

        # Buscar apenas o erro de alternatives
        errors = [item for item in obtained if item["title"] == "alternatives"]
        self.assertEqual(len(errors), 1)

        error = errors[0]
        self.assertEqual(error["response"], "CRITICAL")
        self.assertIsNone(error["got_value"])
        self.assertIn("Wrap <tex-math> and <mml:math> with <alternatives>", error["advice"])

    def test_validate_alternatives_not_required_in_disp_formula(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<disp-formula id='e10'>"
            "<label>Formula 1</label>"
            "<alternatives>"
            '<mml:math id="m03">'
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

        # Buscar apenas o erro de alternatives
        errors = [item for item in obtained if item["title"] == "alternatives"]
        self.assertEqual(len(errors), 1)

        error = errors[0]
        self.assertEqual(error["response"], "CRITICAL")
        self.assertEqual(error["got_value"], "alternatives")
        self.assertIn("Remove the <alternatives>", error["advice"])

    def test_validate_mathml_recommendation_in_disp_formula_with_only_tex(self):
        """Test MathML recommendation when disp-formula has only tex-math"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<disp-formula id="e10">'
            "<label>(1)</label>"
            '<tex-math id="tx1">\\[ E = mc^2 \\]</tex-math>'
            "</disp-formula>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleDispFormulaValidation(
                xml_tree=xml_tree, rules={"mathml_error_level": "WARNING"}
            ).validate()
        )

        # Deve retornar aviso recomendando MathML
        warnings = [item for item in obtained if item["title"] == "MathML recommendation"]
        self.assertEqual(len(warnings), 1)

        warning = warnings[0]
        self.assertEqual(warning["response"], "WARNING")
        self.assertEqual(warning["expected_value"], "mml:math")
        self.assertEqual(warning["got_value"], "tex-math")
        self.assertIn("accessibility", warning["advice"])
        self.assertIn("mml:math", warning["advice"])

    def test_validate_mathml_recommendation_in_disp_formula_with_mml(self):
        """Test that no warning is issued when disp-formula has mml:math"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<disp-formula id="e10">'
            "<label>(1)</label>"
            '<mml:math id="m1">'
            "<mml:mrow>"
            "<mml:mi>E</mml:mi><mml:mo>=</mml:mo><mml:mi>m</mml:mi><mml:msup><mml:mi>c</mml:mi><mml:mn>2</mml:mn></mml:msup>"
            "</mml:mrow>"
            "</mml:math>"
            "</disp-formula>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleDispFormulaValidation(
                xml_tree=xml_tree, rules={"mathml_error_level": "WARNING"}
            ).validate()
        )

        # Não deve retornar aviso de MathML
        warnings = [item for item in obtained if item["title"] == "MathML recommendation"]
        self.assertEqual(len(warnings), 0)

    def test_validate_mathml_recommendation_in_disp_formula_with_both(self):
        """Test that no warning is issued when disp-formula has both tex-math and mml:math"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<disp-formula id="e10">'
            "<label>(1)</label>"
            "<alternatives>"
            '<mml:math id="m1">'
            "<mml:mrow>"
            "<mml:mi>E</mml:mi><mml:mo>=</mml:mo><mml:mi>m</mml:mi><mml:msup><mml:mi>c</mml:mi><mml:mn>2</mml:mn></mml:msup>"
            "</mml:mrow>"
            "</mml:math>"
            '<tex-math id="tx1">\\[ E = mc^2 \\]</tex-math>'
            "</alternatives>"
            "</disp-formula>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleDispFormulaValidation(
                xml_tree=xml_tree, rules={"mathml_error_level": "WARNING"}
            ).validate()
        )

        # Não deve retornar aviso de MathML
        warnings = [item for item in obtained if item["title"] == "MathML recommendation"]
        self.assertEqual(len(warnings), 0)

    def test_validate_mathml_recommendation_in_inline_formula_with_only_tex(self):
        """Test MathML recommendation when inline-formula has only tex-math"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p>Some text with <inline-formula id="e10">'
            '<tex-math id="tx1">x^2</tex-math>'
            "</inline-formula> in text.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleInlineFormulaValidation(
                xml_tree=xml_tree, rules={"mathml_error_level": "WARNING"}
            ).validate()
        )

        # Deve retornar aviso recomendando MathML
        warnings = [item for item in obtained if item["title"] == "MathML recommendation"]
        self.assertEqual(len(warnings), 1)

        warning = warnings[0]
        self.assertEqual(warning["response"], "WARNING")
        self.assertEqual(warning["expected_value"], "mml:math")
        self.assertEqual(warning["got_value"], "tex-math")
        self.assertIn("accessibility", warning["advice"])
        self.assertIn("mml:math", warning["advice"])

    def test_validate_mathml_recommendation_in_inline_formula_with_mml(self):
        """Test that no warning is issued when inline-formula has mml:math"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<p>Some text with <inline-formula id="e10">'
            '<mml:math id="m1">'
            "<mml:msup><mml:mi>x</mml:mi><mml:mn>2</mml:mn></mml:msup>"
            "</mml:math>"
            "</inline-formula> in text.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleInlineFormulaValidation(
                xml_tree=xml_tree, rules={"mathml_error_level": "WARNING"}
            ).validate()
        )

        # Não deve retornar aviso de MathML
        warnings = [item for item in obtained if item["title"] == "MathML recommendation"]
        self.assertEqual(len(warnings), 0)

    def test_validate_mathml_recommendation_returns_none_without_codification(self):
        """Test that mathml recommendation returns None when there's no codification at all"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<disp-formula id="e10">'
            "<label>(1)</label>"
            '<graphic xlink:href="formula.png"/>'
            "</disp-formula>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleDispFormulaValidation(
                xml_tree=xml_tree, rules={"mathml_error_level": "WARNING"}
            ).validate()
        )

        # Não deve retornar aviso de MathML (já retornará erro de codificação)
        warnings = [item for item in obtained if item["title"] == "MathML recommendation"]
        self.assertEqual(len(warnings), 0)
