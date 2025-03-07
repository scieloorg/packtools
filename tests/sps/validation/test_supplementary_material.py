import unittest
from lxml import etree
from packtools.sps.validation.supplementary_material import SupplementaryMaterialValidation, ArticleSupplementaryMaterialValidation
from packtools.sps.models.supplementary_material import XmlSupplementaryMaterials


class TestSupplementaryMaterialValidation(unittest.TestCase):
    def setUp(self):
        self.params = {
            "supplementary_material_structure_error_level": "CRITICAL",
            "supplementary_material_attributes_error_level": "CRITICAL",
            "supplementary_material_language_error_level": "CRITICAL",
            "supplementary_material_position_error_level": "CRITICAL",
            "supplementary_material_format_error_level": "CRITICAL",
            "supplementary_material_in_app_group_error_level": "CRITICAL",
            "inline_supplementary_material_error_level": "CRITICAL",
            "supplementary_material_sec_attributes_error_level": "CRITICAL",
            "supplementary_material_midia_attributes_error_level": "CRITICAL",
            "supplementary_material_midia_accessibility_requirements_error_level": "CRITICAL"
        }

    def test_validate_structure_failure(self):
        """Fails when supplementary materials are outside <sec sec-type='supplementary-material'>."""
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec>
                        <supplementary-material id="supp1" xlink:href="file.pdf">
                            <label>Supplementary Material</label>
                            <media mimetype="application" mime-subtype="pdf"/>
                        </supplementary-material>
                    </sec>
                </body>
            </article>
        ''')
        article_supps = list(XmlSupplementaryMaterials(xml_tree).items)
        validator = SupplementaryMaterialValidation(article_supps[0], xml_tree, self.params)
        results = validator.validate_structure()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "Supplementary materials must be inside <sec sec-type='supplementary-material'>.")

    def test_validate_id_failure(self):
        """Fails when supplementary material lacks an ID attribute."""
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <supplementary-material>
                            <p>Missing required attributes.</p>
                        </supplementary-material>
                    </sec>
                </body>
            </article>
        ''')
        article_supps = list(XmlSupplementaryMaterials(xml_tree).items)
        validator = SupplementaryMaterialValidation(article_supps[0], xml_tree, self.params)
        results = validator.validate_id()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], 'Add supplementary material with id="" in <supplementary-material>: <supplementary-material id="">. Consult SPS documentation for more detail.')

    def test_validate_language_failure(self):
        """Fails when the language of the supplementary material does not match the article's language."""
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <supplementary-material id="supp1">
                            <label>Esse rótulo está em português</label>
                        </supplementary-material>
                    </sec>
                </body>
            </article>
        ''')
        article_supps = list(XmlSupplementaryMaterials(xml_tree).items)
        validator = SupplementaryMaterialValidation(article_supps[0], xml_tree, self.params)
        results = validator.validate_language()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "The language of the supplementary material (pt) differs from the language of the article (en).")

    def test_validate_position_failure(self):
        """Fails when supplementary material is not at the end of <body> or inside <back>."""
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec>
                        <title>Some Section</title>
                    </sec>
                    <sec sec-type="supplementary-material">
                        <supplementary-material id="supp1" xlink:href="file.pdf">
                            <label>Supplementary Material</label>
                        </supplementary-material>
                    </sec>
                    <sec>
                        <title>Invalid Last Section</title>
                    </sec>
                </body>
            </article>
        ''')
        article_supps = list(XmlSupplementaryMaterials(xml_tree).items)
        validator = SupplementaryMaterialValidation(article_supps[0], xml_tree, self.params)
        results = validator.validate_position()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"],
                         "The supplementary materials section must be at the end of <body> or inside <back>.")

    def test_validate_format_failure(self):
        """Fails when supplementary material format is incorrect."""
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <supplementary-material id="supp1">
                            <label>Supplementary Material</label>
                            <graphic mimetype="application/pdf" mime-subtype="pdf"/>
                        </supplementary-material>
                    </sec>
                </body>
            </article>
        ''')
        article_supps = list(XmlSupplementaryMaterials(xml_tree).items)
        validator = SupplementaryMaterialValidation(article_supps[0], xml_tree, self.params)
        results = validator.validate_format()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "Incorrect format. Expected: media for application/pdf.")

    def test_validate_supplementary_material_not_in_app_group(self):
        """Verifies that <supplementary-material> does not occur inside <app-group> or <app>."""
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <app-group>
                        <app>
                            <supplementary-material id="supp1">
                                <label>Invalid Supplementary Material</label>
                            </supplementary-material>
                        </app>
                    </app-group>
                </body>
            </article>
        ''')
        article_supps = list(XmlSupplementaryMaterials(xml_tree).items)
        validator = SupplementaryMaterialValidation(article_supps[0], xml_tree, self.params)
        results = validator.validate_not_in_app_group()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "Do not use <supplementary-material> inside <app-group> or <app>.")

    def test_validate_prohibited_inline_supplementary_material(self):
        """Verifies that <inline-supplementary-material> is not used."""
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <inline-supplementary-material id="supp1">
                        <label>Invalid Inline Supplementary Material</label>
                    </inline-supplementary-material>
                </body>
            </article>
        ''')

        validator = SupplementaryMaterialValidation({}, xml_tree, self.params)
        results = validator.validate_prohibited_inline()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "The use of <inline-supplementary-material> is prohibited.")

    def test_validate_sec_type_supplementary_material(self):
        """Verifies that all <sec> containing <supplementary-material> have @sec-type='supplementary-material'."""
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec>
                        <supplementary-material id="supp1">
                            <label>Supplementary Material</label>
                        </supplementary-material>
                    </sec>
                </body>
            </article>
        ''')
        article_supps = list(XmlSupplementaryMaterials(xml_tree).items)
        validator = SupplementaryMaterialValidation(article_supps[0], xml_tree, self.params)
        results = validator.validate_sec_type()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"],
                         "Every section containing <supplementary-material> must have sec-type='supplementary-material'.")

if __name__ == "__main__":
    unittest.main()