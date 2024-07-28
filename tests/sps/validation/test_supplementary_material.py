import unittest
from lxml import etree

from packtools.sps.validation.supplementary_material import (
    SupplementaryMaterialValidation,
)


class SupplementaryMaterialValidationTest(unittest.TestCase):
    def test_supplementary_material_validation_no_elements(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<p>Some text content without supplementary materials.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(
            SupplementaryMaterialValidation(
                xmltree
            ).validate_supplementary_material_existence()
        )

        expected = [
            {
                "title": "validation of <supplementary-material> elements",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "supplementary-material",
                "sub_item": None,
                "validation_type": "exist",
                "response": "WARNING",
                "expected_value": "<supplementary-material> element",
                "got_value": None,
                "message": "Got None, expected <supplementary-material> element",
                "advice": "Consider adding a <supplementary-material> element to provide additional data or materials related to the article.",
                "data": None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_supplementary_material_validation_with_elements(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<supplementary-material id="supp01" mimetype="application" mime-subtype="pdf" xlink:href="supplementary1.pdf">'
            "<label>Supplementary Material 1</label>"
            "</supplementary-material>"
            '<inline-supplementary-material id="supp02" mimetype="text" mime-subtype="plain" xlink:href="inline-supplementary1.txt">'
            "<label>Inline Supplementary Material 1</label>"
            "</inline-supplementary-material>"
            "</body>"
            "</article>"
        )
        obtained = list(
            SupplementaryMaterialValidation(
                xmltree
            ).validate_supplementary_material_existence()
        )

        expected = [
            {
                "title": "validation of <supplementary-material> elements",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "supplementary-material",
                "sub_item": None,
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "supp01",
                "got_value": "supp01",
                "message": "Got supp01, expected supp01",
                "advice": None,
                "data": {
                    "supplementary_material_id": "supp01",
                    "supplementary_material_label": "Supplementary Material 1",
                    "mimetype": "application",
                    "mime_subtype": "pdf",
                    "xlink_href": "supplementary1.pdf",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            },
            {
                "title": "validation of <supplementary-material> elements",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "supplementary-material",
                "sub_item": None,
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "supp02",
                "got_value": "supp02",
                "message": "Got supp02, expected supp02",
                "advice": None,
                "data": {
                    "supplementary_material_id": "supp02",
                    "supplementary_material_label": "Inline Supplementary Material 1",
                    "mimetype": "text",
                    "mime_subtype": "plain",
                    "xlink_href": "inline-supplementary1.txt",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


if __name__ == "__main__":
    unittest.main()
