from packtools.sps.models.accessibility_data import AccessibilityData, Transcript


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
    def misplaced_alt_texts(self):
        """
        Detecta elementos <alt-text> que estão fora dos elementos permitidos.
        Segundo SPS 1.9/1.10, <alt-text> só pode estar dentro de:
        <graphic>, <inline-graphic>, <media>, <inline-media>
        """
        valid_parents = ("graphic", "inline-graphic", "media", "inline-media")
        misplaced = []

        for alt_text in self.xmltree.xpath(".//alt-text"):
            parent = alt_text.getparent()
            if parent is not None and parent.tag not in valid_parents:
                misplaced.append({
                    "tag": "alt-text",
                    "parent_tag": parent.tag,
                    "parent_id": parent.get("id"),
                    "alt_text": alt_text.text,
                    "alt_text_length": len(alt_text.text or ""),
                    "expected_location": valid_parents,
                    "current_location": parent.tag,
                })

        return misplaced

    @property
    def data(self):
        xpaths = [
            ".//graphic",
            ".//inline-graphic",
            ".//media",
            ".//inline-media",
        ]
        for item in self.xmltree.xpath("|".join(xpaths)):
            model = AccessibilityData(item)
            model.transcript_data = self.transcripts.get(model.xref_sec_rid)
            yield model.data

        for misplaced in self.misplaced_alt_texts:
            yield misplaced
