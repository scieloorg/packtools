import unittest
from xml.etree.ElementTree import Element, SubElement
from packtools.sps.models.media import Media  # Ajuste o caminho conforme sua estrutura


class TestMedia(unittest.TestCase):

    def setUp(self):
        """Configuração inicial dos elementos XML para cada teste."""

        # Criando um elemento <media> completo, com label, caption, attrib e long-desc
        self.media_complete = Element("media", {
            "id": "media1",
            "mimetype": "video",
            "mime-subtype": "mp4",
            "{http://www.w3.org/1999/xlink}href": "1234-5678-scie-58-e1043-md1.mp4"
        })

        label = SubElement(self.media_complete, "label")
        label.text = "Video 1"

        caption = SubElement(self.media_complete, "caption")
        title = SubElement(caption, "title")
        title.text = "Vídeo: malesuada vehicula"

        attrib = SubElement(self.media_complete, "attrib")
        attrib.text = "Fonte: consectetur adipiscing elit"

        long_desc = SubElement(self.media_complete, "long-desc")
        long_desc.text = "Descrição detalhada do objeto (acima de 120 caracteres)"

        # Criando um <media> sem label e caption
        self.media_no_label_caption = Element("media", {
            "id": "media2",
            "mimetype": "audio",
            "mime-subtype": "mp3",
            "{http://www.w3.org/1999/xlink}href": "1234-5678-scie-58-e1043-md2.mp3"
        })

        # Criando um <media> sem mimetype e mime-subtype
        self.media_no_mime = Element("media", {
            "id": "media3",
            "{http://www.w3.org/1999/xlink}href": "1234-5678-scie-58-e1043-md3.ogg"
        })

        # Criando um <media> sem xlink:href
        self.media_no_xlink = Element("media", {
            "id": "media4",
            "mimetype": "image",
            "mime-subtype": "png"
        })

    def test_media_xlink_href(self):
        """Testa se xlink_href do Media é extraído corretamente."""
        resource = Media(self.media_complete)
        self.assertEqual(resource.xlink_href, "1234-5678-scie-58-e1043-md1.mp4")

    def test_media_id(self):
        """Testa se o ID do Media é extraído corretamente."""
        resource = Media(self.media_complete)
        self.assertEqual(resource.id, "media1")

    def test_media_mimetype_and_mime_subtype(self):
        """Testa se mimetype e mime_subtype são extraídos corretamente do Media."""
        resource = Media(self.media_complete)
        self.assertEqual(resource.mimetype, "video")
        self.assertEqual(resource.mime_subtype, "mp4")

    def test_media_label_and_caption(self):
        """Testa se label e caption são extraídos corretamente do Media."""
        resource = Media(self.media_complete)
        self.assertEqual(resource.label, "Video 1")
        self.assertEqual(resource.caption, "Vídeo: malesuada vehicula")

    def test_media_attrib_extraction(self):
        """Testa se attrib (fonte) é extraído corretamente do Media."""
        resource = Media(self.media_complete)
        self.assertEqual(resource.attrib, "Fonte: consectetur adipiscing elit")

    def test_media_long_desc(self):
        """Testa se long-desc é extraído corretamente do Media."""
        resource = Media(self.media_complete)
        self.assertEqual(resource.data.get("long_desc"), "Descrição detalhada do objeto (acima de 120 caracteres)")

    def test_media_data_output(self):
        """Testa se a propriedade data de Media retorna o dicionário esperado."""
        resource = Media(self.media_complete)
        expected_data = {
            "xlink_href": "1234-5678-scie-58-e1043-md1.mp4",
            "id": "media1",
            "mimetype": "video",
            "mime_subtype": "mp4",
            "alt_text": None,
            "long_desc": "Descrição detalhada do objeto (acima de 120 caracteres)",
            "transcript": None,
            "content_type": None,
            "speakers": None,
            "tag": "media",
            "label": "Video 1",
            "caption": "Vídeo: malesuada vehicula",
            "attrib": "Fonte: consectetur adipiscing elit",
        }
        self.assertDictEqual(resource.data, expected_data)

    def test_media_no_label_caption(self):
        """Testa o comportamento quando <media> não contém label nem caption."""
        resource = Media(self.media_no_label_caption)
        self.assertIsNone(resource.label)
        self.assertIsNone(resource.caption)

    def test_media_no_mimetype_and_mime_subtype(self):
        """Testa o comportamento quando mimetype e mime-subtype não estão presentes."""
        resource = Media(self.media_no_mime)
        self.assertIsNone(resource.mimetype)
        self.assertIsNone(resource.mime_subtype)

    def test_media_no_xlink_href(self):
        """Testa o comportamento quando <media> não contém xlink:href."""
        resource = Media(self.media_no_xlink)
        self.assertIsNone(resource.xlink_href)

    def test_media_no_id(self):
        """Testa o comportamento quando a tag <media> não contém id."""
        media_no_id = Element("media", {
            "mimetype": "video",
            "mime-subtype": "mp4",
            "{http://www.w3.org/1999/xlink}href": "video.mp4"
        })

        resource = Media(media_no_id)
        self.assertIsNone(resource.id)


if __name__ == "__main__":
    unittest.main()
