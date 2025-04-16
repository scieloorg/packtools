import unittest
from lxml.etree import Element, SubElement
from packtools.sps.models.visual_resource_base import VisualResourceBase


class TestVisualResourceBase(unittest.TestCase):

    def setUp(self):
        """Configuração inicial dos elementos XML para cada teste."""

        # Criando o primeiro material suplementar (vídeo)
        self.supplementary_material_1 = Element(
            "supplementary-material", {"id": "suppl1"}
        )

        label_1 = SubElement(self.supplementary_material_1, "label")
        label_1.text = "Supplementary material 1"

        caption_1 = SubElement(self.supplementary_material_1, "caption")
        title_1 = SubElement(caption_1, "title")
        title_1.text = "Video 1"

        self.media_1 = SubElement(
            self.supplementary_material_1,
            "media",
            {
                "id": "media1",
                "mimetype": "video",
                "mime-subtype": "mp4",
                "{http://www.w3.org/1999/xlink}href": "1234-5678-scie-58-e1043-md1.mp4",
            },
        )

        # Criando o segundo material suplementar (planilha)
        self.supplementary_material_2 = Element(
            "supplementary-material", {"id": "suppl3"}
        )

        label_2 = SubElement(self.supplementary_material_2, "label")
        label_2.text = "Supplementary material 3"

        caption_2 = SubElement(self.supplementary_material_2, "caption")
        title_2 = SubElement(caption_2, "title")
        title_2.text = "Spreadsheet 1"

        self.media_2 = SubElement(
            self.supplementary_material_2,
            "media",
            {
                "id": "media2",
                "mimetype": "application",
                "mime-subtype": "xlsx",
                "{http://www.w3.org/1999/xlink}href": "1234-5678-scie-58-e1043-md2.xlsx",
            },
        )

        # Criando um elemento media sem id e sem xlink_href
        self.media_without_id = Element(
            "media", {"mimetype": "image", "mime-subtype": "png"}
        )

        # Criando um elemento media sem atributos para verificar valores padrão
        self.media_empty = Element("media")

    def test_xlink_href(self):
        """Verifica se o xlink:href é extraído corretamente da tag <media>."""
        resource_1 = VisualResourceBase(self.media_1)
        self.assertEqual(resource_1.xlink_href, "1234-5678-scie-58-e1043-md1.mp4")

        resource_2 = VisualResourceBase(self.media_2)
        self.assertEqual(resource_2.xlink_href, "1234-5678-scie-58-e1043-md2.xlsx")

    def test_id(self):
        """Verifica se o ID é extraído corretamente da tag <media>."""
        resource_1 = VisualResourceBase(self.media_1)
        self.assertEqual(resource_1.id, "media1")

        resource_2 = VisualResourceBase(self.media_2)
        self.assertEqual(resource_2.id, "media2")

        resource_no_id = VisualResourceBase(self.media_without_id)
        self.assertIsNone(resource_no_id.id)  # Deve ser None se não houver id

        resource_empty = VisualResourceBase(self.media_empty)
        self.assertIsNone(resource_empty.id)  # Nenhum atributo presente

    def test_accessibility_data(self):
        """Verifica se os dados de acessibilidade são extraídos corretamente."""
        resource_1 = VisualResourceBase(self.media_1)
        self.assertIsNone(
            resource_1.accessibility.alt_text
        )  # Sem <alt-text>, deve ser None

        resource_2 = VisualResourceBase(self.media_2)
        self.assertIsNone(resource_2.accessibility.alt_text)

    def test_data_output(self):
        self.maxDiff = None
        """Testa se a propriedade data retorna o dicionário esperado."""
        resource_1 = VisualResourceBase(self.media_1)
        expected_data_1 = {
            "xlink_href": "1234-5678-scie-58-e1043-md1.mp4",
            "id": "media1",
            "tag": "media",
            "xml": '<media xmlns:ns0="http://www.w3.org/1999/xlink" id="media1" mimetype="video" mime-subtype="mp4" '
                   'ns0:href="1234-5678-scie-58-e1043-md1.mp4"/>',
            "xref_sec_rid": None
        }
        self.assertDictEqual(resource_1.data, expected_data_1)

        resource_2 = VisualResourceBase(self.media_2)
        expected_data_2 = {
            "xlink_href": "1234-5678-scie-58-e1043-md2.xlsx",
            "id": "media2",
            "tag": "media",
            "xml": '<media xmlns:ns0="http://www.w3.org/1999/xlink" id="media2" mimetype="application" mime-subtype="xlsx" '
                   'ns0:href="1234-5678-scie-58-e1043-md2.xlsx"/>',
            "xref_sec_rid": None,
        }
        self.assertDictEqual(resource_2.data, expected_data_2)

    def test_missing_xlink_href(self):
        """Testa o comportamento quando a tag <media> não contém xlink:href."""
        resource = VisualResourceBase(self.media_without_id)
        self.assertIsNone(resource.xlink_href)  # Deve ser None se não houver o atributo

        resource_empty = VisualResourceBase(self.media_empty)
        self.assertIsNone(resource_empty.xlink_href)  # Nenhum atributo presente

    def test_missing_id(self):
        """Testa o comportamento quando a tag <media> não contém id."""
        resource = VisualResourceBase(self.media_without_id)
        self.assertIsNone(resource.id)  # Deve ser None se não houver o atributo

        resource_empty = VisualResourceBase(self.media_empty)
        self.assertIsNone(resource_empty.id)  # Nenhum atributo presente


if __name__ == "__main__":
    unittest.main()
