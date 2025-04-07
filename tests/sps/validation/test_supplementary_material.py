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
            "inline_error_level": "CRITICAL",
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
        supplementary_node = xml_tree.xpath(".//media")
        validator = SupplementaryMaterialValidation(
            supplementary_data[0], self.params, supplementary_node
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


if __name__ == "__main__":
    unittest.main()
