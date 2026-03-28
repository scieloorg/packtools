import unittest
from lxml import etree
from packtools.sps.validation.supplementary_material import (
    SupplementaryMaterialValidation,
    XmlSupplementaryMaterialValidation,
)
from packtools.sps.models.supplementary_material import XmlSupplementaryMaterials


class TestSupplementaryMaterialValidation(unittest.TestCase):
    def setUp(self):
        self.params = {
            "sec_type_error_level": "CRITICAL",
            "position_error_level": "CRITICAL",
            "label_error_level": "CRITICAL",
            "app_group_error_level": "CRITICAL",
            "inline_error_level": "ERROR",
            "id_error_level": "CRITICAL",
            "sec_title_error_level": "CRITICAL",
            "content_error_level": "WARNING",
            "id_uniqueness_error_level": "ERROR",
            "mime_types_and_subtypes": [
                {"mimetype": "video", "mime-subtype": "mp4"},
                {"mimetype": "audio", "mime-subtype": "mp3"},
                {"mimetype": "application", "mime-subtype": "zip"},
                {"mimetype": "application", "mime-subtype": "pdf"},
                {"mimetype": "application", "mime-subtype": "xlsx"}
            ],
            "mime_type_error_level": "CRITICAL",
            "media_attributes_error_level": "CRITICAL",
            "valid_extension": "CRITICAL",
            "xlink_href_error_level": "CRITICAL",
            "alt_text_exist_error_level": "CRITICAL",
            "long_desc_exist_error_level": "CRITICAL",
            "transcript_error_level": "CRITICAL",
            "speaker_speech_error_level": "CRITICAL",
            "structure_error_level": "CRITICAL",
            "parent_suppl_mat_expected": ["app-group", "app"]
        }

    def test_validate_id_present(self):
        """Passes when supplementary material has @id."""
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <supplementary-material id="supp1">
                            <label>Supplementary Material</label>
                            <media mimetype="application" mime-subtype="pdf" xlink:href="file.pdf"/>
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
        result = validator.validate_id()
        self.assertEqual(result["response"], "OK")

    def test_validate_id_missing(self):
        """Fails when supplementary material lacks @id."""
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <supplementary-material>
                            <label>Supplementary Material</label>
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
        result = validator.validate_id()
        self.assertEqual(result["response"], "CRITICAL")
        self.assertIn("@id", result["advice"])

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

    def test_validate_label_missing(self):
        """Fails when supplementary material lacks a label element."""
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

    def test_validate_label_present_with_media(self):
        """Passes when supplementary material has label even with media data merged."""
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <supplementary-material id="supp1">
                            <label>Supplementary Material 1</label>
                            <media mimetype="application" mime-subtype="pdf" xlink:href="file.pdf"/>
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
        results = validator.validate_label()
        self.assertEqual(results["response"], "OK")

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
        self.assertEqual(results["response"], "ERROR")
        self.assertEqual(
            results["advice"],
            "The use of <inline-supplementary-material> is prohibited.",
        )

    def test_validate_sec_title_present(self):
        """Passes when sec has a title element."""
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <title>Supplementary Materials</title>
                        <supplementary-material id="supp1">
                            <label>Supplementary Material 1</label>
                        </supplementary-material>
                    </sec>
                </body>
            </article>
        """
        )
        validator = XmlSupplementaryMaterialValidation(xml_tree, self.params)
        results = list(validator.validate_sec_title())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_validate_sec_title_missing(self):
        """Fails when sec lacks a title element."""
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <supplementary-material id="supp1">
                            <label>Supplementary Material 1</label>
                        </supplementary-material>
                    </sec>
                </body>
            </article>
        """
        )
        validator = XmlSupplementaryMaterialValidation(xml_tree, self.params)
        results = list(validator.validate_sec_title())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")
        self.assertIn("<title>", results[0]["advice"])

    def test_validate_content_present(self):
        """Passes when supplementary material contains media."""
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <supplementary-material id="supp1">
                            <label>Supplementary Material 1</label>
                            <media mimetype="application" mime-subtype="pdf" xlink:href="file.pdf"/>
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
        result = validator.validate_content()
        self.assertEqual(result["response"], "OK")

    def test_validate_content_missing(self):
        """Fails when supplementary material has no graphic or media."""
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <supplementary-material id="supp1">
                            <label>Supplementary Material 1</label>
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
        result = validator.validate_content()
        self.assertEqual(result["response"], "WARNING")
        self.assertIn("<graphic>", result["advice"])

    def test_validate_content_with_graphic(self):
        """Passes when supplementary material contains graphic."""
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <supplementary-material id="supp1">
                            <label>Figure S1</label>
                            <graphic xlink:href="figure-s1.jpg"/>
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
        result = validator.validate_content()
        self.assertEqual(result["response"], "OK")

    def test_validate_id_uniqueness_pass(self):
        """Passes when all supplementary materials have unique @id values."""
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <supplementary-material id="supp1">
                            <label>Supplementary Material 1</label>
                        </supplementary-material>
                        <supplementary-material id="supp2">
                            <label>Supplementary Material 2</label>
                        </supplementary-material>
                    </sec>
                </body>
            </article>
        """
        )
        validator = XmlSupplementaryMaterialValidation(xml_tree, self.params)
        results = list(validator.validate_id_uniqueness())
        self.assertEqual(len(results), 0)

    def test_validate_id_uniqueness_fail(self):
        """Fails when supplementary materials have duplicate @id values."""
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <supplementary-material id="supp1">
                            <label>Supplementary Material 1</label>
                        </supplementary-material>
                        <supplementary-material id="supp1">
                            <label>Supplementary Material 2</label>
                        </supplementary-material>
                    </sec>
                </body>
            </article>
        """
        )
        validator = XmlSupplementaryMaterialValidation(xml_tree, self.params)
        results = list(validator.validate_id_uniqueness())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")
        self.assertIn("supp1", results[0]["advice"])

    def test_validate_full_workflow(self):
        """Test the complete validation workflow for supplementary material."""
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">
                <body>
                    <sec sec-type="supplementary-material">
                        <title>Supplementary Materials</title>
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
        results = [r for r in validator.validate() if r is not None]
        titles = [result["title"] for result in results]
        self.assertIn("supplementary-material @id", titles)
        self.assertIn("label", titles)
        self.assertIn("supplementary-material content", titles)
        self.assertIn("Prohibition of inline-supplementary-material", titles)
        self.assertIn("sec supplementary-material title", titles)


if __name__ == "__main__":
    unittest.main()
