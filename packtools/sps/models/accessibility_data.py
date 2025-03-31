import re


class AccessibilityData:
    def __init__(self, node):
        self.node = node

    @property
    def alt_text(self):
        """Obtém o texto alternativo (<alt-text>) do XML."""
        if self.node is not None:
            alt_text_node = self.node.find("alt-text")
            return (
                alt_text_node.text.strip()
                if alt_text_node is not None and alt_text_node.text
                else None
            )

    @property
    def long_desc(self):
        """Obtém a descrição longa (<long-desc>) do XML, removendo espaços extras."""
        if self.node is not None:
            long_desc_node = self.node.find("long-desc")
            if long_desc_node is not None and long_desc_node.text:
                return " ".join(long_desc_node.text.split())  # Remove espaços extras
            return None

    @property
    def transcript(self):
        """Obtém o texto dentro de <sec sec-type='transcript'>, removendo espaços extras."""
        if self.node is not None:
            transcript_node = self.node.find(".//sec[@sec-type='transcript']")
            if transcript_node is not None:
                text = " ".join(transcript_node.itertext()).strip()
                return re.sub(r"\s+", " ", text) if text else None
            return None

    @property
    def content_type(self):
        """Obtém o atributo @content-type do elemento."""
        if self.node is not None:
            return self.node.get("content-type")

    @property
    def speaker_data(self):
        """Obtém os dados de <speaker> e <speech> dentro de transcrição."""
        if self.node is not None:
            transcript_node = self.node.find(".//sec[@sec-type='transcript']")
            if transcript_node is None:
                return None

            speakers = []
            current_speaker = None

            for element in transcript_node:
                if element.tag == "speaker" and element.text:
                    current_speaker = element.text.strip()
                elif element.tag == "speech" and element.text:
                    speakers.append(
                        {
                            "speaker": current_speaker,
                            "speech": " ".join(element.text.split()),
                        }
                    )

            return speakers if speakers else None

    @property
    def data(self):
        """Retorna um dicionário com todos os dados extraídos do XML."""
        return {
            "alt_text": self.alt_text,
            "long_desc": self.long_desc,
            "transcript": self.transcript,
            "content_type": self.content_type,
            "speakers": self.speaker_data,
            "tag": self.node.tag,
        }
