import unittest
from lxml import etree
from packtools.sps.validation.supplementary_material import (
    SupplementaryMaterialValidation,
    XmlSupplementaryMaterialValidation,
)
from packtools.sps.models.supplementary_material import XmlSupplementaryMaterials
from packtools.sps.validation.xml_validator_rules import get_default_rules
from packtools.sps.validation.media import MediaValidation
from packtools.sps.validation.graphic import GraphicValidation


class TestSupplementaryMaterialValidation(unittest.TestCase):
    def setUp(self):
        # Regras customizadas (override), com valores deliberadamente
        # diferentes dos defaults reais de visual_resource_base_rules/
        # graphic_rules (CRITICAL/ERROR trocados), para deixar explícito
        # que este fixture testa o cenário de sobreposição de regras, e
        # não os valores pré-estabelecidos (esses são cobertos em
        # test_media_rules_and_graphic_rules_default_to_pre_established_sps_values).
        self.params = {
            "sec_type_error_level": "CRITICAL",
            "position_error_level": "CRITICAL",
            "label_error_level": "CRITICAL",
            "app_group_error_level": "CRITICAL",
            "inline_error_level": "CRITICAL",
            "parent_suppl_mat_expected": ["app-group", "app"],
            "media_rules": {
                "media_attributes_error_level": "ERROR",
                "xlink_href_error_level": "ERROR",
                "valid_extension": ["mp3", "mp4", "zip", "pdf", "xlsx", "docx", "pptx"],
                "mime_types_and_subtypes": [
                    {"mimetype": "video", "mime-subtype": "mp4"},
                    {"mimetype": "audio", "mime-subtype": "mp3"},
                    {"mimetype": "application", "mime-subtype": "zip"},
                    {"mimetype": "application", "mime-subtype": "pdf"},
                    {"mimetype": "application", "mime-subtype": "xlsx"},
                    {"mimetype": "application", "mime-subtype": "docx"},
                    {"mimetype": "application", "mime-subtype": "pptx"}
                ],
                "mime_type_error_level": "CRITICAL",
                "alt_text_exist_error_level": "CRITICAL",
                "alt_text_content_error_level": "CRITICAL",
                "long_desc_exist_error_level": "CRITICAL",
                "long_desc_content_error_level": "CRITICAL",
                "transcript_error_level": "CRITICAL",
                "content_type_error_level": "CRITICAL",
                "speaker_speech_error_level": "CRITICAL",
                "structure_error_level": "CRITICAL",
                "content_types": ["machine-generated"],
            },
            "graphic_rules": {
                "media_attributes_error_level": "CRITICAL",
                "xlink_href_error_level": "CRITICAL",
                "valid_extension": ["jpg", "jpeg", "png", "tif", "tiff", "svg"],
                "svg_error_level": "CRITICAL",
            },
        }

    def test_validate_sec_type(self):
        """Fails when sec-type != 'supplementary-material'."""
        xml_tree = etree.fromstring(
            """
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
        """
        )
        supplementary_data = list(XmlSupplementaryMaterials(xml_tree).items)
        validator = SupplementaryMaterialValidation(
            supplementary_data[0], self.params
        )
        results = validator.validate_sec_type()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(
            results["advice"],
            'In <sec sec-type="None"><supplementary-material> replace "None" with "supplementary-material".',
        )

    def test_validate_label(self):
        """Fails when supplementary material lacks an label element."""
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <supplementary-material />
                    </sec>
                </body>
            </article>
        """
        )
        supplementary_data = list(XmlSupplementaryMaterials(xml_tree).items)
        validator = SupplementaryMaterialValidation(
            supplementary_data[0], self.params
        )
        results = validator.validate_label()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(
            results["advice"],
            "Add label in <supplementary-material>: <supplementary-material><label>. Consult SPS documentation for more detail.",
        )

    def test_validate_position_failure(self):
        """Fails when supplementary material is not at the end of <body> or inside <back>."""
        xml_tree = etree.fromstring(
            """
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
        """
        )
        validator = XmlSupplementaryMaterialValidation(
            xml_tree, self.params
        )
        results = validator.validate_position()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(
            results["advice"],
            "The supplementary materials section must be at the end of <body> or inside <back>.",
        )

    def test_validate_supplementary_material_not_in_app_group(self):
        """Verifies that <supplementary-material> does not occur inside <app-group> or <app>."""
        xml_tree = etree.fromstring(
            """
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
        """
        )
        supplementary_data = list(XmlSupplementaryMaterials(xml_tree).items)
        validator = SupplementaryMaterialValidation(
            supplementary_data[0], self.params
        )
        results = validator.validate_not_in_app_group()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(
            results["advice"],
            "Do not use <supplementary-material> inside <app-group> or <app>.",
        )

    def test_validate_prohibited_inline_supplementary_material(self):
        """Verifies that <inline-supplementary-material> is not used."""
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <inline-supplementary-material id="supp1">
                        <label>Invalid Inline Supplementary Material</label>
                    </inline-supplementary-material>
                </body>
            </article>
        """
        )

        validator = XmlSupplementaryMaterialValidation(xml_tree, self.params)
        results = validator.validate_prohibited_inline()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(
            results["advice"],
            "The use of <inline-supplementary-material> is prohibited.",
        )

    def test_validate_full_workflow(self):
        """Test the complete validation workflow for supplementary material."""
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <supplementary-material id="supp1" xlink:href="file.pdf">
                            <label>Supplementary Material</label>
                            <media mimetype="application" mime-subtype="pdf" xlink:href="file.pdf"/>
                        </supplementary-material>
                    </sec>
                </body>
            </article>
            """
        )
        validator = XmlSupplementaryMaterialValidation(xml_tree, self.params)
        results = list(validator.validate())

        self.assertEqual(len(results), 20)  # Validações executadas
        titles = [result["title"] for result in results]
        self.assertIn("mime type and subtype", titles)
        self.assertIn("@id", titles)
        self.assertIn("@xlink:href validation", titles)
        self.assertIn("<alt-text>", titles)
        self.assertIn("<long-desc>", titles)
        self.assertIn("Transcript validation", titles)
        self.assertIn("<speaker> and <speech> validation", titles)
        self.assertIn("structure", titles)
        self.assertIn("@id", titles)
        self.assertIn("@xlink:href validation", titles)
        self.assertIn("<alt-text>", titles)
        self.assertIn("<long-desc>", titles)
        self.assertIn("Transcript validation", titles)
        self.assertIn("<speaker> and <speech> validation", titles)
        self.assertIn("structure", titles)
        self.assertIn("@sec-type", titles)
        self.assertIn("label", titles)
        self.assertIn("Prohibition of <supplementary-material> inside <app-group> and <app>", titles)
        self.assertIn("Prohibition of inline-supplementary-material", titles)
        self.assertIn("Position of supplementary materials", titles)

    def test_media_rules_and_graphic_rules_are_overridable(self):
        """
        Regras customizadas (media_rules/graphic_rules) passadas pelo chamador
        devem ser efetivamente usadas por MediaValidation/GraphicValidation,
        e não os valores default de visual_resource_base_rules/graphic_rules.
        """
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <supplementary-material id="supp1">
                            <label>Supplementary Material</label>
                            <media id="m1" mimetype="application" mime-subtype="pdf" xlink:href="filenoext"/>
                        </supplementary-material>
                    </sec>
                </body>
            </article>
            """
        )
        supplementary_data = list(XmlSupplementaryMaterials(xml_tree).items)[0]

        media_result = MediaValidation(
            supplementary_data, self.params["media_rules"]
        ).validate_xlink_href()
        graphic_result = GraphicValidation(
            supplementary_data, self.params["graphic_rules"]
        ).validate_xlink_href()

        # self.params usa valores deliberadamente diferentes dos defaults reais
        # (ERROR para media, CRITICAL para graphic — trocados em relação ao SPS)
        self.assertEqual(media_result["response"], "ERROR")
        self.assertEqual(graphic_result["response"], "CRITICAL")

    def test_media_rules_and_graphic_rules_default_to_pre_established_sps_values(self):
        """
        Quando nenhuma regra customizada é passada, get_default_rules() fornece
        as regras pré-estabelecidas (SPS): CRITICAL para <media>, ERROR para
        <graphic>, conforme visual_resource_base_rules.json/graphic_rules.json.
        """
        default_rules = get_default_rules()
        media_rules = default_rules["visual_resource_base_rules"]
        graphic_rules = default_rules["graphic_rules"]

        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <supplementary-material id="supp1">
                            <label>Supplementary Material</label>
                            <media id="m1" mimetype="application" mime-subtype="pdf" xlink:href="filenoext"/>
                        </supplementary-material>
                    </sec>
                </body>
            </article>
            """
        )
        supplementary_data = list(XmlSupplementaryMaterials(xml_tree).items)[0]

        media_result = MediaValidation(supplementary_data, media_rules).validate_xlink_href()
        graphic_result = GraphicValidation(supplementary_data, graphic_rules).validate_xlink_href()

        self.assertEqual(media_result["response"], "CRITICAL")
        self.assertEqual(graphic_result["response"], "ERROR")


if __name__ == "__main__":
    unittest.main()
