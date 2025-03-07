import unittest
from xml.etree.ElementTree import Element, SubElement
from packtools.sps.models.graphic import Graphic, InlineGraphic


class TestGraphicAndInlineGraphic(unittest.TestCase):

    def setUp(self):
        """Configuração inicial dos elementos XML para cada teste."""

        # Criando um elemento <fig> com <graphic>
        self.fig = Element("fig", {"id": "f2"})

        label = SubElement(self.fig, "label")
        label.text = "Figure 2"

        caption = SubElement(self.fig, "caption")
        title = SubElement(caption, "title")
        title.text = "Título da figura"

        self.graphic = SubElement(self.fig, "graphic", {
            "id": "graphic1",
            "{http://www.w3.org/1999/xlink}href": "1234-5678-scie-58-e1043-gf2.jpg"
        })

        # Criando um parágrafo <p> com <inline-graphic>
        self.paragraph = Element("p")
        self.inline_graphic = SubElement(self.paragraph, "inline-graphic", {
            "id": "inline-graphic1",
            "{http://www.w3.org/1999/xlink}href": "1234-5678-scie-58-e1043-gf17.jpg"
        })

    def test_graphic_xlink_href(self):
        """Testa se xlink_href do Graphic é extraído corretamente."""
        resource = Graphic(self.graphic)
        self.assertEqual(resource.xlink_href, "1234-5678-scie-58-e1043-gf2.jpg")

    def test_inline_graphic_xlink_href(self):
        """Testa se xlink_href do InlineGraphic é extraído corretamente."""
        resource = InlineGraphic(self.inline_graphic)
        self.assertEqual(resource.xlink_href, "1234-5678-scie-58-e1043-gf17.jpg")

    def test_graphic_id(self):
        """Testa se o id do Graphic é extraído corretamente."""
        resource = Graphic(self.graphic)
        self.assertEqual(resource.id, "graphic1")

    def test_inline_graphic_id(self):
        """Testa se o id do InlineGraphic é extraído corretamente."""
        resource = InlineGraphic(self.inline_graphic)
        self.assertEqual(resource.id, "inline-graphic1")

    def test_graphic_data_output(self):
        """Testa se a propriedade data de Graphic retorna o dicionário esperado."""
        resource = Graphic(self.graphic)
        expected_data = {
            "xlink_href": "1234-5678-scie-58-e1043-gf2.jpg",
            "id": "graphic1",
            "alt_text": None,
            "long_desc": None,
            "transcript": None,
            "content_type": None,
            "speakers": None,
            "tag": "graphic",
        }
        self.assertDictEqual(resource.data, expected_data)

    def test_inline_graphic_data_output(self):
        """Testa se a propriedade data de InlineGraphic retorna o dicionário esperado."""
        resource = InlineGraphic(self.inline_graphic)
        expected_data = {
            "xlink_href": "1234-5678-scie-58-e1043-gf17.jpg",
            "id": "inline-graphic1",
            "alt_text": None,
            "long_desc": None,
            "transcript": None,
            "content_type": None,
            "speakers": None,
            "tag": "inline-graphic",
        }
        self.assertDictEqual(resource.data, expected_data)

    def test_missing_xlink_href(self):
        """Testa o comportamento quando a tag <graphic> ou <inline-graphic> não contém xlink:href."""
        graphic_without_href = Element("graphic", {"id": "graphic2"})
        inline_graphic_without_href = Element("inline-graphic", {"id": "inline-graphic2"})

        resource_graphic = Graphic(graphic_without_href)
        self.assertIsNone(resource_graphic.xlink_href)

        resource_inline_graphic = InlineGraphic(inline_graphic_without_href)
        self.assertIsNone(resource_inline_graphic.xlink_href)

    def test_missing_id(self):
        """Testa o comportamento quando a tag <graphic> ou <inline-graphic> não contém id."""
        graphic_without_id = Element("graphic", {"{http://www.w3.org/1999/xlink}href": "image.jpg"})
        inline_graphic_without_id = Element("inline-graphic", {"{http://www.w3.org/1999/xlink}href": "inline-image.jpg"})

        resource_graphic = Graphic(graphic_without_id)
        self.assertIsNone(resource_graphic.id)

        resource_inline_graphic = InlineGraphic(inline_graphic_without_id)
        self.assertIsNone(resource_inline_graphic.id)


if __name__ == "__main__":
    unittest.main()
