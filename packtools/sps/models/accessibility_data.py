import re

class AccessibilityData:
    def __init__(self, node):
        self.node = node

    def get_alt_text(self):
        """Obtém o texto alternativo (<alt-text>) do XML."""
        alt_text_node = self.node.find("alt-text")
        return alt_text_node.text.strip() if alt_text_node is not None else None

    def get_long_desc(self):
        """Obtém a descrição longa (<long-desc>) do XML."""
        long_desc_node = self.node.find("long-desc")
        if long_desc_node is not None:
            return " ".join(long_desc_node.text.split())  # Remove espaços extras e quebras de linha
        return None

    def get_transcript(self):
        """Obtém todo o texto dentro de <sec sec-type='transcript'>, incluindo <speaker> e <speech>, removendo espaços extras."""
        transcript_node = self.node.find(".//sec[@sec-type='transcript']")
        if transcript_node is not None:
            text = " ".join(transcript_node.itertext()).strip()
            return re.sub(r'\s+', ' ', text)
        return None

    def get_content_type(self):
        """Obtém o atributo @content-type do elemento."""
        return self.node.get("content-type")

    def get_speaker_data(self):
        """Obtém o conteúdo de <speaker> e <speech> dentro da transcrição, se existir."""
        speakers = self.node.findall(".//speaker")
        speech_blocks = self.node.findall(".//speech")

        speaker_data = []
        for speaker, speech in zip(speakers, speech_blocks):
            speaker_data.append({
                "speaker": speaker.text.strip() if speaker is not None else None,
                "speech": speech.text.strip() if speech is not None else None
            })

        return speaker_data if speaker_data else None

    def extract_data(self):
        """Retorna um dicionário com todos os dados extraídos do XML."""
        return {
            "alt_text": self.get_alt_text(),
            "long_desc": self.get_long_desc(),
            "transcript": self.get_transcript(),
            "content_type": self.get_content_type(),
            "speakers": self.get_speaker_data(),
        }
