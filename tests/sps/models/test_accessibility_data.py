import unittest
from lxml import etree
from packtools.sps.models.accessibility_data import AccessibilityData, Transcript, XMLAccessibilityData


class TestAccessibilityData(unittest.TestCase):

    def setUp(self):
        """Cria um XML de teste antes de cada teste."""
        xml_content = """
        <body>
            <media xmlns:xlink="http://www.w3.org/1999/xlink" mimetype="video" mime-subtype="mp4" xlink:href="1234-5678.mp4">
                <alt-text content-type="machine-generated">Breve descrição do vídeo</alt-text>
                <long-desc content-type="machine-generated">Descrição detalhada do vídeo contendo mais de 120 caracteres. Isso garante que a extração esteja correta e seja útil para acessibilidade.</long-desc>
                <xref ref-type="sec" rid="TR1"/>
            </media>
            <sec sec-type="transcript" id="TR1">
                <speech>
                    <speaker>Gabriel</speaker>
                    <p>Olá, este é um vídeo demonstrativo.</p>
                </speech>
                <speech>
                    <speaker>Denise</speaker>
                    <p>Sim, estamos explicando como funciona.</p>
                </speech>
            </sec>
        </body>
        """
        self.xml_node = etree.fromstring(xml_content)
        self.xml_data = list(XMLAccessibilityData(self.xml_node).data)

    def test_alt_text(self):
        """Testa a extração do <alt-text>."""
        self.assertEqual(self.xml_data[0]["alt_text"], "Breve descrição do vídeo")
        self.assertEqual(self.xml_data[0]["alt_text_xml"], '<alt-text content-type="machine-generated">Breve descrição do vídeo</alt-text>')

    def test_long_desc(self):
        """Testa a extração do <long-desc>."""
        expected_text = (
            "Descrição detalhada do vídeo contendo mais de 120 caracteres. "
            "Isso garante que a extração esteja correta e seja útil para acessibilidade."
        )
        self.assertEqual(self.xml_data[0]["long_desc"], expected_text)
        self.assertEqual(
            self.xml_data[0]["long_desc_xml"],
            '<long-desc content-type="machine-generated">Descrição detalhada do vídeo contendo mais de 120 '
            'caracteres. Isso garante que a extração esteja correta e seja útil para acessibilidade.</long-desc>')

    def test_transcript(self):
        """Testa a extração da transcrição <sec sec-type="transcript">."""
        transcript = self.xml_data[0]["transcript"]
        self.assertIsNotNone(transcript)
        self.assertIn("Gabriel", transcript)
        self.assertIn("Denise", transcript)

    def test_get_content_type(self):
        """Testa a obtenção do atributo @content-type."""
        self.assertEqual(self.xml_data[0]["long_desc_content_type"], "machine-generated")
        self.assertEqual(self.xml_data[0]["alt_text_content_type"], "machine-generated")

    def test_get_speaker_data(self):
        """Testa a extração de diálogos com <speaker> e <speech>."""
        expected_data = [
            {"speaker": "Gabriel", "speech": "Olá, este é um vídeo demonstrativo."},
            {"speaker": "Denise", "speech": "Sim, estamos explicando como funciona."},
        ]
        self.assertEqual(list(self.xml_data[0]["speakers"]), expected_data)

    def test_extract_data(self):
        """Testa a extração completa dos dados de acessibilidade."""
        extracted = self.xml_data[0]
        self.assertEqual(extracted["tag"], "sec")
        self.assertEqual(extracted["transcript_id"], "TR1")


if __name__ == "__main__":
    unittest.main()
