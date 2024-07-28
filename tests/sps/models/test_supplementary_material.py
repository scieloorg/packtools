import unittest
from lxml import etree

from packtools.sps.models.supplementary_material import (
    SupplementaryMaterial,
    ArticleSupplementaryMaterials,
)


class SupplementaryMaterialTest(unittest.TestCase):
    def setUp(self):
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        dtd-version="1.0" article-type="research-article" xml:lang="pt">
            <body>
                <supplementary-material id="supp01" mimetype="application" mime-subtype="pdf" xlink:href="supplementary1.pdf">
                    <label>Supplementary Material 1</label>
                </supplementary-material>
            </body>
        </article>
        """
        self.xml_tree = etree.fromstring(xml_str)
        self.supplementary_material = SupplementaryMaterial(
            self.xml_tree.xpath(".//supplementary-material")[0]
        )

    def test_supplementary_material_id(self):
        self.assertEqual(
            self.supplementary_material.supplementary_material_id, "supp01"
        )

    def test_supplementary_material_label(self):
        self.assertEqual(
            self.supplementary_material.supplementary_material_label,
            "Supplementary Material 1",
        )

    def test_mimetype(self):
        self.assertEqual(self.supplementary_material.mimetype, "application")

    def test_mime_subtype(self):
        self.assertEqual(self.supplementary_material.mime_subtype, "pdf")

    def test_xlink_href(self):
        self.assertEqual(self.supplementary_material.xlink_href, "supplementary1.pdf")

    def test_data(self):
        expected = {
            "supplementary_material_id": "supp01",
            "supplementary_material_label": "Supplementary Material 1",
            "mimetype": "application",
            "mime_subtype": "pdf",
            "xlink_href": "supplementary1.pdf",
        }
        obtained = self.supplementary_material.data
        self.assertDictEqual(expected, obtained)


class ArticleSupplementaryMaterialsTest(unittest.TestCase):
    def setUp(self):
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        dtd-version="1.0" article-type="research-article" xml:lang="pt">
            <body>
                <supplementary-material id="supp01" mimetype="application" mime-subtype="pdf" xlink:href="supplementary1.pdf">
                    <label>Supplementary Material 1</label>
                </supplementary-material>
                <inline-supplementary-material id="supp02" mimetype="text" mime-subtype="plain" xlink:href="inline-supplementary1.txt">
                    <label>Inline Supplementary Material 1</label>
                </inline-supplementary-material>
            </body>
        </article>
        """
        self.xml_tree = etree.fromstring(xml_str)

    def test_data(self):
        obtained = list(ArticleSupplementaryMaterials(self.xml_tree).data())
        expected = [
            {
                "supplementary_material_id": "supp01",
                "supplementary_material_label": "Supplementary Material 1",
                "mimetype": "application",
                "mime_subtype": "pdf",
                "xlink_href": "supplementary1.pdf",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
            },
            {
                "supplementary_material_id": "supp02",
                "supplementary_material_label": "Inline Supplementary Material 1",
                "mimetype": "text",
                "mime_subtype": "plain",
                "xlink_href": "inline-supplementary1.txt",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
            },
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


if __name__ == "__main__":
    unittest.main()
