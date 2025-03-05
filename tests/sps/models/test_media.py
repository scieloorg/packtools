import unittest
from lxml import etree

from packtools.sps.models.media import Media, XmlMedias
from packtools.sps.models.accessibility_data import AccessibilityData


class MediaTest(unittest.TestCase):
    def setUp(self):
        """Configura um XML de teste contendo um único elemento <media>."""
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        dtd-version="1.0" article-type="research-article" xml:lang="pt">
            <body>
                <media mimetype="video" mime-subtype="mp4" xlink:href="media1.mp4" content-type="machine-generated">
                    <alt-text>Breve descrição do vídeo</alt-text>
                    <long-desc>Descrição detalhada do vídeo contendo mais de 120 caracteres. Isso garante que a 
                    extração esteja correta e seja útil para acessibilidade.</long-desc>
                    <sec sec-type="transcript">
                        <speaker>Gabriel</speaker>
                        <speech>Olá, este é um vídeo demonstrativo.</speech>
                    </sec>
                </media>
            </body>
        </article>
        """
        self.xml_tree = etree.fromstring(xml_str)
        self.media = Media(self.xml_tree.xpath(".//media")[0])  # Instancia Media com o nó <media>
        self.accessibility = AccessibilityData(self.xml_tree.xpath(".//media")[0])  # Instancia AccessibilityData

    def test_mimetype(self):
        """Testa a extração do atributo mimetype."""
        self.assertEqual(self.media.mimetype, "video")

    def test_mime_subtype(self):
        """Testa a extração do atributo mime-subtype."""
        self.assertEqual(self.media.mime_subtype, "mp4")

    def test_xlink_href(self):
        """Testa a extração do atributo xlink:href."""
        self.assertEqual(self.media.xlink_href, "media1.mp4")

    def test_media_type(self):
        """Testa a extração da tag do elemento mídia."""
        self.assertEqual(self.media.media_type, "media")

    def test_alt_text(self):
        """Testa a extração do <alt-text>."""
        self.assertEqual(self.accessibility.alt_text, "Breve descrição do vídeo")

    def test_long_desc(self):
        """Testa a extração do <long-desc>."""
        expected_text = ("Descrição detalhada do vídeo contendo mais de 120 caracteres. Isso garante que "
                         "a extração esteja correta e seja útil para acessibilidade.")
        self.assertEqual(self.accessibility.long_desc, expected_text)

    def test_transcript(self):
        """Testa a extração da transcrição <sec sec-type='transcript'>."""
        transcript = self.accessibility.transcript
        self.assertIsNotNone(transcript)
        self.assertIn("Gabriel", transcript)
        self.assertIn("Olá, este é um vídeo demonstrativo.", transcript)

    def test_content_type(self):
        """Testa a extração do atributo @content-type."""
        self.assertEqual(self.accessibility.content_type, "machine-generated")

    def test_speaker_data(self):
        """Testa a extração de falantes e discursos dentro de <sec sec-type='transcript'>."""
        expected_data = [
            {"speaker": "Gabriel", "speech": "Olá, este é um vídeo demonstrativo."}
        ]
        self.assertEqual(self.accessibility.speaker_data, expected_data)

    def test_data(self):
        """Testa a extração combinada de todos os dados de mídia e acessibilidade."""
        self.maxDiff = None
        expected = {
            "media_type": "media",
            "mimetype": "video",
            "mime_subtype": "mp4",
            "xlink_href": "media1.mp4",
            "alt_text": "Breve descrição do vídeo",
            "long_desc": ("Descrição detalhada do vídeo contendo mais de 120 caracteres. Isso garante que "
                          "a extração esteja correta e seja útil para acessibilidade."),
            "transcript": "Gabriel Olá, este é um vídeo demonstrativo.",
            "content_type": "machine-generated",
            "speakers": [{"speaker": "Gabriel", "speech": "Olá, este é um vídeo demonstrativo."}]
        }
        obtained = self.media.data
        self.assertDictEqual(expected, obtained)


class XmlMediasTest(unittest.TestCase):
    def setUp(self):
        """Configura um XML contendo mídias tanto no <article> quanto em <sub-article>."""
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        dtd-version="1.0" article-type="research-article" xml:lang="pt">
            <body>
                <media mimetype="video" mime-subtype="mp4" xlink:href="media1.mp4">
                    <label>Media 1</label>
                </media>
                <media mimetype="image" mime-subtype="png" xlink:href="image1.png">
                    <label>Imagem 1</label>
                </media>
            </body>
            <sub-article article-type="translation" xml:lang="en">
                <body>
                    <media mimetype="audio" mime-subtype="mp3" xlink:href="media2.mp3">
                        <label>Media 2</label>
                    </media>
                </body>
            </sub-article>
        </article>
        """
        self.xml_tree = etree.fromstring(xml_str)

    def test_items(self):
        """Testa a extração de todos os elementos <media> no <article> e <sub-article>."""
        obtained = XmlMedias(self.xml_tree).items
        self.assertEqual(len(obtained), 4)

        expected_mimetypes = {"video", "image", "audio"}
        extracted_mimetypes = {media["mimetype"] for media in obtained}
        self.assertEqual(extracted_mimetypes, expected_mimetypes)

        expected_hrefs = {"media1.mp4", "image1.png", "media2.mp3"}
        extracted_hrefs = {media["xlink_href"] for media in obtained}
        self.assertEqual(extracted_hrefs, expected_hrefs)


if __name__ == "__main__":
    unittest.main()
