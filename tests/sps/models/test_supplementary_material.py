import unittest
from lxml import etree

from packtools.sps.models.supplementary_material import (
    XmlSupplementaryMaterials,
    SupplementaryMaterial,
)


class SupplementaryMaterialTest(unittest.TestCase):
    def setUp(self):
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
            <body>
                <sec sec-type="supplementary-material">
                    <supplementary-material id="supp01">
                        <label>Supplementary Material 1</label>
                        <caption>
                            <title>Video 1</title>
                        </caption>
                        <media mimetype="application" mime-subtype="pdf" xlink:href="supplementary1.pdf"/>
                    </supplementary-material>
                </sec>
            </body>
        </article>
        """
        self.xml_tree = etree.fromstring(xml_str)
        self.supp = SupplementaryMaterial(
            self.xml_tree.xpath(".//supplementary-material")[0]
        )

    def test_id(self):
        self.assertEqual(self.supp.id, "supp01")

    def test_parent(self):
        self.assertEqual(self.supp.parent_tag, "sec")

    def test_sec_type(self):
        self.assertEqual(self.supp.sec_type, "supplementary-material")

    def test_label(self):
        self.assertEqual(self.supp.label, "Supplementary Material 1")

    def test_caption_title(self):
        self.assertEqual(self.supp.caption, "Video 1")

    def test_mimetype(self):
        self.assertEqual(self.supp.mimetype, "application")

    def test_mime_subtype(self):
        self.assertEqual(self.supp.mime_subtype, "pdf")

    def test_xlink_href(self):
        self.assertEqual(self.supp.xlink_href, "supplementary1.pdf")

    def test_xml(self):
        self.assertEqual(self.supp.xml, '<supplementary-material id="supp01">')

    def test_supplementary_material_media_node(self):
        """Verifies that the model correctly extracts the <media> node and its attributes."""
        xml_tree = etree.fromstring(
            """
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
        """
        )

        # Obtém o primeiro material suplementar do XML
        supp_material = SupplementaryMaterial(
            xml_tree.find(".//supplementary-material")
        )

        # Verifica se media_node foi corretamente extraído
        self.assertIsInstance(supp_material.media_node, etree._Element)

        # Verifica se a tag do nó extraído é "media"
        self.assertEqual(supp_material.media_node.tag, "media")

        # Verifica se os atributos foram corretamente extraídos
        self.assertEqual(supp_material.media_node.get("id"), "m1")
        self.assertEqual(supp_material.media_node.get("mimetype"), "video")
        self.assertEqual(supp_material.media_node.get("mime-subtype"), "mp4")
        self.assertEqual(
            supp_material.media_node.get("{http://www.w3.org/1999/xlink}href"),
            "video.mp4",
        )

        # Verifica se contém <alt-text> para acessibilidade
        self.assertIsNotNone(supp_material.media_node.find("alt-text"))
        self.assertEqual(
            supp_material.media_node.findtext("alt-text"),
            "Descriptive text for accessibility",
        )


class XmlSupplementaryMaterialsTest(unittest.TestCase):
    def setUp(self):
        self.xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
            <body>
                <supplementary-material id="supp01">
                    <label>Supplementary Material 1</label>
                    <media mimetype="application" mime-subtype="pdf" xlink:href="supplementary1.pdf"/>
                </supplementary-material>
                <sec sec-type="supplementary-material" id="sec01">
                    <title>Supplementary Section</title>
                    <supplementary-material id="supp02">
                        <label>Supplementary Material 2</label>
                        <graphic xlink:href="supplementary2.jpg"/>
                    </supplementary-material>
                </sec>
            </body>
            <sub-article id="subart01">
                <body>
                    <supplementary-material id="supp03">
                        <label>Supplementary Material 3</label>
                        <graphic xlink:href="supplementary3.jpg"/>
                    </supplementary-material>
                </body>
            </sub-article>
        </article>
        """
        self.xml_tree = etree.fromstring(self.xml_str)
        self.supplementary_materials = XmlSupplementaryMaterials(self.xml_tree)

    def test_items_by_id(self):
        items_by_id = self.supplementary_materials.items_by_id

        # Verifica se os materiais suplementares estão organizados corretamente
        self.assertIn(
            "main_article", items_by_id
        )  # Agora, "main_article" representa o artigo sem @id
        self.assertIn("subart01", items_by_id)  # Subartigo continua com seu próprio @id

        # Verifica se o artigo principal contém dois materiais suplementares
        self.assertEqual(len(items_by_id["main_article"]), 2)

        # Verifica se o subartigo contém um material suplementar
        self.assertEqual(len(items_by_id["subart01"]), 1)

        # Verifica se os IDs dos materiais suplementares estão corretos
        supp_ids_main_article = [item["id"] for item in items_by_id["main_article"]]
        self.assertIn("supp01", supp_ids_main_article)
        self.assertIn("supp02", supp_ids_main_article)

        supp_ids_subarticle = [item["id"] for item in items_by_id["subart01"]]
        self.assertIn("supp03", supp_ids_subarticle)

        # Verifica se os dados do primeiro material suplementar estão corretos
        supp1_data = next(
            item for item in items_by_id["main_article"] if item["id"] == "supp01"
        )
        self.assertEqual(supp1_data["parent_suppl_mat"], "body")
        self.assertEqual(supp1_data["mimetype"], "application")
        self.assertEqual(supp1_data["mime_subtype"], "pdf")
        self.assertEqual(supp1_data["xlink_href"], "supplementary1.pdf")


if __name__ == "__main__":
    unittest.main()
