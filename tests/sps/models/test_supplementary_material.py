import unittest
from lxml import etree

from packtools.sps.models.supplementary_material import XmlSupplementaryMaterials, SupplementaryMaterial

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

    def test_media_type(self):
        self.assertEqual(self.supp.media_type, "media")

    def test_xml(self):
        self.assertEqual(self.supp.xml, '<supplementary-material id="supp01">')

    def test_supplementary_material_media_node(self):
        """Verifies that the model correctly extracts the <media> node and its attributes."""
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

        # Obtém o primeiro material suplementar do XML
        supp_material = SupplementaryMaterial(xml_tree.find(".//supplementary-material"))

        # Verifica se media_node foi corretamente extraído
        self.assertIsInstance(supp_material.media_node, etree._Element)

        # Verifica se a tag do nó extraído é "media"
        self.assertEqual(supp_material.media_node.tag, "media")

        # Verifica se os atributos foram corretamente extraídos
        self.assertEqual(supp_material.media_node.get("id"), "m1")
        self.assertEqual(supp_material.media_node.get("mimetype"), "video")
        self.assertEqual(supp_material.media_node.get("mime-subtype"), "mp4")
        self.assertEqual(supp_material.media_node.get("{http://www.w3.org/1999/xlink}href"), "video.mp4")

        # Verifica se contém <alt-text> para acessibilidade
        self.assertIsNotNone(supp_material.media_node.find("alt-text"))
        self.assertEqual(supp_material.media_node.findtext("alt-text"), "Descriptive text for accessibility")


class XmlSupplementaryMaterialsTest(unittest.TestCase):
    def setUp(self):
        xml_str = """
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
        </article>
        """
        self.xml_tree = etree.fromstring(xml_str)

    def test_items(self):
        obtained = list(XmlSupplementaryMaterials(self.xml_tree).items)
        self.assertEqual(len(obtained), 2)

if __name__ == "__main__":
    unittest.main()
