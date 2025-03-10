import unittest
from lxml import etree
from packtools.sps.models.accessibility_data import AccessibilityData


class TestAccessibilityData(unittest.TestCase):

    def setUp(self):
        """Cria um XML de teste antes de cada teste."""
        xml_content = """
        <media xmlns:xlink="http://www.w3.org/1999/xlink" 
           mimetype="video" mime-subtype="mp4" xlink:href="1234-5678.mp4" content-type="machine-generated">
        <alt-text>Breve descrição do vídeo</alt-text>
        <long-desc>Descrição detalhada do vídeo contendo mais de 120 caracteres. Isso garante que 
        a extração esteja correta e seja útil para acessibilidade.</long-desc>
        <sec sec-type="transcript">
            <speaker>Gabriel</speaker>
            <speech>Olá, este é um vídeo demonstrativo.</speech>
            <speaker>Denise</speaker>
            <speech>Sim, estamos explicando como funciona.</speech>
        </sec>
    </media>
        """
        self.xml_node = etree.fromstring(xml_content)
        self.accessibility_data = AccessibilityData(self.xml_node)

    def test_alt_text(self):
        """Testa a extração do <alt-text>."""
        self.assertEqual(self.accessibility_data.alt_text, "Breve descrição do vídeo")

    def test_long_desc(self):
        """Testa a extração do <long-desc>."""
        expected_text = ("Descrição detalhada do vídeo contendo mais de 120 caracteres. Isso garante que "
                         "a extração esteja correta e seja útil para acessibilidade.")
        self.assertEqual(self.accessibility_data.long_desc, expected_text)

    def test_transcript(self):
        """Testa a extração da transcrição <sec sec-type="transcript">."""
        transcript = self.accessibility_data.transcript
        self.assertIsNotNone(transcript)
        self.assertIn("Gabriel", transcript)
        self.assertIn("Denise", transcript)

    def test_get_content_type(self):
        """Testa a obtenção do atributo @content-type."""
        self.assertEqual(self.accessibility_data.content_type, "machine-generated")

    def test_get_speaker_data(self):
        """Testa a extração de diálogos com <speaker> e <speech>."""
        expected_data = [
            {"speaker": "Gabriel", "speech": "Olá, este é um vídeo demonstrativo."},
            {"speaker": "Denise", "speech": "Sim, estamos explicando como funciona."}
        ]
        self.assertEqual(self.accessibility_data.speaker_data, expected_data)

    def test_extract_data(self):
        """Testa a extração completa dos dados de acessibilidade."""
        extracted = self.accessibility_data.data

        self.assertEqual(extracted["alt_text"], "Breve descrição do vídeo")
        self.assertIn("Descrição detalhada do vídeo", extracted["long_desc"])
        self.assertIn("Gabriel", extracted["transcript"])
        self.assertEqual(extracted["content_type"], "machine-generated")
        self.assertEqual(extracted["speakers"], [
            {"speaker": "Gabriel", "speech": "Olá, este é um vídeo demonstrativo."},
            {"speaker": "Denise", "speech": "Sim, estamos explicando como funciona."}
        ])


if __name__ == "__main__":
    unittest.main()
