import unittest
from lxml.etree import Element, SubElement
from packtools.sps.models.graphic import Graphic, InlineGraphic, XmlGraphic


class TestGraphic(unittest.TestCase):

    def setUp(self):
        """Configuração inicial dos elementos XML para cada teste."""

        # Criando um artigo XML com <graphic> e <inline-graphic>
        self.article = Element("article")

        # Criando sub-artigo para validar extração por ArticleAndSubArticles
        self.sub_article = SubElement(self.article, "sub-article", {"id": "sub1"})

        # Adicionando <graphic> ao sub-artigo
        self.graphic1 = SubElement(
            self.sub_article,
            "graphic",
            {"id": "graphic1", "{http://www.w3.org/1999/xlink}href": "image1.png"},
        )

        self.graphic2 = SubElement(
            self.sub_article,
            "graphic",
            {"id": "graphic2", "{http://www.w3.org/1999/xlink}href": "image2.jpg"},
        )

        # Criando parágrafo com <inline-graphic>
        paragraph = SubElement(self.sub_article, "p")
        self.inline_graphic = SubElement(
            paragraph,
            "inline-graphic",
            {"{http://www.w3.org/1999/xlink}href": "icon.svg"},
        )

        # Criando um XML sem gráficos para testar comportamento vazio
        self.article_no_graphic = Element("article")

    def test_graphic_xlink_href(self):
        """Testa se xlink_href do Graphic é extraído corretamente."""
        resource = Graphic(self.graphic1)
        self.assertEqual(resource.xlink_href, "image1.png")

    def test_graphic_data_output(self):
        """Testa se a propriedade data de Graphic retorna um dicionário esperado."""
        resource = Graphic(self.graphic1)
        expected_data = {
            "xlink_href": "image1.png",
            "id": "graphic1",
        }
        self.assertTrue(expected_data.items() <= resource.data.items())

    def test_inline_graphic_xlink_href(self):
        """Testa se xlink_href do InlineGraphic é extraído corretamente."""
        resource = InlineGraphic(self.inline_graphic)
        self.assertEqual(resource.xlink_href, "icon.svg")

    def test_inline_graphic_data_output(self):
        """Testa se a propriedade data de InlineGraphic retorna um dicionário esperado."""
        resource = InlineGraphic(self.inline_graphic)
        expected_data = {
            "xlink_href": "icon.svg",
        }
        self.assertTrue(expected_data.items() <= resource.data.items())

    def test_xmlgraphic_generates_data(self):
        """Testa se XmlGraphic gera corretamente um iterador de dicionários."""
        xml_graphic = XmlGraphic(self.article)
        data_list = list(xml_graphic.data())
        # Deve haver 3 elementos (2 <graphic> + 1 <inline-graphic>)
        self.assertEqual(len(data_list), 3)

        expected_graphic1 = {
            "xlink_href": "image1.png",
            "id": "graphic1",
        }
        expected_graphic2 = {
            "xlink_href": "image2.jpg",
            "id": "graphic2",
        }
        expected_inline_graphic = {
            "xlink_href": "icon.svg",
        }
        self.assertTrue(expected_graphic1.items() <= data_list[0].items())
        self.assertTrue(expected_graphic2.items() <= data_list[1].items())
        self.assertTrue(expected_inline_graphic.items() <= data_list[2].items())

    def test_xmlgraphic_handles_no_graphic(self):
        """Testa o comportamento quando o XML não contém gráficos."""
        xml_graphic = XmlGraphic(self.article_no_graphic)
        data_list = list(xml_graphic.data())

        # Não há gráficos no XML, o iterador deve ser vazio
        self.assertEqual(len(data_list), 0)


if __name__ == "__main__":
    unittest.main()
