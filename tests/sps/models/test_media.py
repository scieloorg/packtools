import unittest
from lxml.etree import Element, SubElement
from packtools.sps.models.media import Media, InlineMedia, XmlMedias


class TestMedia(unittest.TestCase):

    def setUp(self):
        """Configuração inicial dos elementos XML para cada teste."""

        # Criando um artigo XML com <media> e <inline-media>
        self.article = Element("article")

        # Criando sub-artigo para validar extração por ArticleAndSubArticles
        self.sub_article = SubElement(self.article, "sub-article", {"id": "sub1"})

        # Adicionando <media> ao sub-artigo
        self.media1 = SubElement(
            self.sub_article,
            "media",
            {
                "id": "media1",
                "mimetype": "video",
                "mime-subtype": "mp4",
                "{http://www.w3.org/1999/xlink}href": "video1.mp4",
            },
        )

        self.media2 = SubElement(
            self.sub_article,
            "media",
            {
                "id": "media2",
                "mimetype": "audio",
                "mime-subtype": "mp3",
                "{http://www.w3.org/1999/xlink}href": "audio1.mp3",
            },
        )

        # Criando parágrafo com <inline-media>
        paragraph = SubElement(self.sub_article, "p")
        self.inline_media = SubElement(
            paragraph,
            "inline-media",
            {
                "mimetype": "application",
                "mime-subtype": "pdf",
                "{http://www.w3.org/1999/xlink}href": "document1.pdf",
            },
        )

        # Criando um XML sem mídias para testar comportamento vazio
        self.article_no_media = Element("article")

    def test_media_xlink_href(self):
        """Testa se xlink_href do Media é extraído corretamente."""
        resource = Media(self.media1)
        self.assertEqual(resource.xlink_href, "video1.mp4")

    def test_media_mimetype_and_mime_subtype(self):
        """Testa se mimetype e mime_subtype são extraídos corretamente do Media."""
        resource = Media(self.media1)
        self.assertEqual(resource.mimetype, "video")
        self.assertEqual(resource.mime_subtype, "mp4")

    def test_media_data_output(self):
        """Testa se a propriedade data de Media retorna um dicionário esperado."""
        resource = Media(self.media1)
        expected_data = {
            "xlink_href": "video1.mp4",
            "id": "media1",
            "mimetype": "video",
            "mime_subtype": "mp4",
        }
        self.assertTrue(expected_data.items() <= resource.data.items())

    def test_inline_media_xlink_href(self):
        """Testa se xlink_href do InlineMedia é extraído corretamente."""
        resource = InlineMedia(self.inline_media)
        self.assertEqual(resource.xlink_href, "document1.pdf")

    def test_inline_media_mimetype_and_mime_subtype(self):
        """Testa se mimetype e mime_subtype são extraídos corretamente do InlineMedia."""
        resource = InlineMedia(self.inline_media)
        self.assertEqual(resource.mimetype, "application")
        self.assertEqual(resource.mime_subtype, "pdf")

    def test_inline_media_data_output(self):
        """Testa se a propriedade data de InlineMedia retorna um dicionário esperado."""
        resource = InlineMedia(self.inline_media)
        expected_data = {
            "xlink_href": "document1.pdf",
            "mimetype": "application",
            "mime_subtype": "pdf",
        }
        self.assertTrue(expected_data.items() <= resource.data.items())

    def test_xmlmedia_generates_data(self):
        """Testa se XmlMedia gera corretamente um iterador de dicionários."""
        xml_media = XmlMedias(self.article)
        data_list = list(xml_media.data())

        # Deve haver 3 elementos (2 <media> + 1 <inline-media>)
        self.assertEqual(len(data_list), 3)

        expected_media1 = {
            "xlink_href": "video1.mp4",
            "mimetype": "video",
            "mime_subtype": "mp4",
        }
        expected_media2 = {
            "xlink_href": "audio1.mp3",
            "mimetype": "audio",
            "mime_subtype": "mp3",
        }
        expected_inline_media = {
            "xlink_href": "document1.pdf",
            "mimetype": "application",
            "mime_subtype": "pdf",
        }
        self.assertTrue(expected_media1.items() <= data_list[0].items())
        self.assertTrue(expected_media2.items() <= data_list[1].items())
        self.assertTrue(expected_inline_media.items() <= data_list[2].items())

    def test_xmlmedia_handles_no_media(self):
        """Testa o comportamento quando o XML não contém mídias."""
        xml_media = XmlMedias(self.article_no_media)
        data_list = list(xml_media.data())

        # Não há mídia no XML, o iterador deve ser vazio
        self.assertEqual(len(data_list), 0)


if __name__ == "__main__":
    unittest.main()
