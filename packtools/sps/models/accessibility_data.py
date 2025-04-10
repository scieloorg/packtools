import re


class XMLAccessibilityData:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def transcripts(self):
        if not hasattr(self, '_transcripts') or not self._transcripts:
            self._transcripts = {}
            for item in self.xmltree.xpath(".//sec[@sec-type='transcript']"):
                transcript = Transcript(item)
                self._transcripts[transcript.transcript_id] = transcript.data
        return self._transcripts

    @property
    def data(self):
        xpaths = [
            ".//*[alt-text]",
            ".//*[long-desc]",
            "graphic",
            "inline-graphic",
            "media",
            "inline-media",
        ]
        for item in self.xmltree.xpath("|".join(xpaths)):
            model = AccessibilityData(item)
            model.transcript_data = self.transcripts.get(model.xref_sec_rid)
            yield model.data


class AccessibilityData:
    def __init__(self, node):
        self.node = node
        self.transcript_data = None

    @property
    def xref_sec_rid(self):
        """Obtém o texto alternativo (<alt-text>) do XML."""
        try:
            return self.node.xpath('xref[@ref-type="sec"]')[0].get("rid")
        except:
            return None
            
    @property
    def alt_text(self):
        """Obtém o texto alternativo (<alt-text>) do XML."""
        try:
            alt_text_node = self.node.find("alt-text")
            return {
                "alt_text": alt_text_node.text,
                "alt_text_content_type": alt_text_node.get("content-type")
            }
        except:
            return None

    @property
    def long_desc(self):
        """Obtém a descrição longa (<long-desc>) do XML, removendo espaços extras."""
        try:
            long_desc_node = self.node.find("long-desc")
            return {
                "long_desc": long_desc_node.text,
                "long_desc_content_type": long_desc_node.get("content-type")
            }
        except:
            return None

    @property
    def data(self):
        """Retorna um dicionário com todos os dados extraídos do XML."""
        d = {
            "tag": self.node.tag,
            "xref_sec_rid": self.xref_sec_rid,
        }
        d.update(self.long_desc)
        d.update(self.alt_text)
        d.update(self.transcript_data or {})
        return d


class Transcript:
    def __init__(self, node):
        self.node = node

    @property
    def transcript_id(self):
        """Obtém o texto alternativo (<alt-text>) do XML."""
        return self.node.get("id")

    @property
    def transcript(self):
        """Obtém o texto dentro de <sec sec-type='transcript'>, removendo espaços extras."""
        text = " ".join(self.node.itertext()).strip()
        return re.sub(r"\s+", " ", text) if text else None

    @property
    def speaker_data(self):
        """Obtém os dados de <speaker> e <speech> dentro de transcrição."""
        for speech in self.node.xpath("speech"):
            yield {
                "speaker": speech.findtext("speaker"),
                "speech": " ".join(speech.xpath("p//text()"))
            }

    @property
    def data(self):
        """Retorna um dicionário com todos os dados extraídos do XML."""
        return {
            "id": self.id,
            "transcript": self.transcript,
            "speakers": self.speaker_data,
            "tag": self.node.tag,
        }