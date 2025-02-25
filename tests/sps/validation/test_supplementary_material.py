import unittest
from lxml import etree
from packtools.sps.validation.supplementary_material import SupplementaryMaterialValidation, ArticleSupplementaryMaterialValidation
from packtools.sps.models.supplementary_material import ArticleSupplementaryMaterials


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

    def test_validate_supplementary_material_structure(self):
        """Verifies if supplementary materials are inside <sec sec-type='supplementary-material'>."""
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
        article_supps = list(ArticleSupplementaryMaterials(xml_tree).data())
        validator = SupplementaryMaterialValidation(article_supps[0], xml_tree, self.params)
        results = validator.validate_supplementary_material_structure()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "Supplementary materials must be inside <sec sec-type='supplementary-material'>.")

    def test_validate_supplementary_material_id_attribute(self):
        """Verifies if supplementary materials contain the ID attribute."""
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
        article_supps = list(ArticleSupplementaryMaterials(xml_tree).data())
        validator = SupplementaryMaterialValidation(article_supps[0], xml_tree, self.params)
        results = validator.validate_supplementary_material_id()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], 'Add supplementary material with id="" in <supplementary-material>: '
                                            '<supplementary-material id="">. Consult SPS documentation for more detail.')

    def test_validate_supplementary_material_language(self):
        """Verifies if the language of supplementary materials matches the article's language."""
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
        article_supps = list(ArticleSupplementaryMaterials(xml_tree).data())
        validator = SupplementaryMaterialValidation(article_supps[0], xml_tree, self.params)
        results = validator.validate_supplementary_material_language()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"],
                         f'The language of the supplementary material (pt) differs from the language of the article (en).')

    def test_validate_supplementary_material_position(self):
        """Verifica se a seção de materiais suplementares está na última posição do <body> ou dentro de <back>."""
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
        article_supps = list(ArticleSupplementaryMaterials(xml_tree).data())
        validator = SupplementaryMaterialValidation(article_supps[0], xml_tree, self.params)
        results = validator.validate_supplementary_material_position()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "The supplementary materials section must be at the end of <body> or inside <back>.")

    def test_validate_supplementary_material_format(self):
        """Verifies if the supplementary material type matches the correct markup."""
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
        article_supps = list(ArticleSupplementaryMaterials(xml_tree).data())
        validator = SupplementaryMaterialValidation(article_supps[0], xml_tree, self.params)
        results = validator.validate_supplementary_material_format()
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
        article_supps = list(ArticleSupplementaryMaterials(xml_tree).data())
        validator = SupplementaryMaterialValidation(article_supps[0], xml_tree, self.params)
        results = validator.validate_supplementary_material_not_in_app_group()
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
        results = validator.validate_prohibited_inline_supplementary_material()
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
        article_supps = list(ArticleSupplementaryMaterials(xml_tree).data())
        validator = SupplementaryMaterialValidation(article_supps[0], xml_tree, self.params)
        results = validator.validate_sec_type_supplementary_material()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"],
                         "Every section containing <supplementary-material> must have sec-type='supplementary-material'.")

    def test_validate_media_attributes(self):
        """Verifies that <media> contains the mandatory attributes @id, @mime-type, @mime-subtype, and @xlink:href."""
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <supplementary-material id="supp1">
                            <label>Supplementary Material</label>
                            <media id="m1" mimetype="video" mime-subtype="mp4" xlink:href="video.mp4"/>
                        </supplementary-material>
                    </sec>
                </body>
            </article>
        ''')
        article_supps = list(ArticleSupplementaryMaterials(xml_tree).data())
        validator = SupplementaryMaterialValidation(article_supps[0], xml_tree, self.params)
        results = validator.validate_media_attributes()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "Each <media> must contain the attributes id, mime-type, mime-subtype, and xlink:href.")

    def test_validate_accessibility_requirements(self):
        """Verifies that images and media contain a description in <alt-text> or <long-desc>."""
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <supplementary-material id="supp1">
                            <label>Supplementary Material</label>
                            <media id="m1" mimetype="video" mime-subtype="mp4" xlink:href="video.mp4">
                                <alt-text>Descriptive text for accessibility</alt-text>
                            </media>
                        </supplementary-material>
                    </sec>
                </body>
            </article>
        ''')
        article_supps = list(ArticleSupplementaryMaterials(xml_tree).data())
        validator = SupplementaryMaterialValidation(article_supps[0], xml_tree, self.params)
        results = validator.validate_accessibility_requirements()
        self.assertEqual(results["response"], "OK")
        self.assertIsNone(results["advice"])


if __name__ == "__main__":
    unittest.main()