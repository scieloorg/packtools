class LabelAndCaption:
    def __init__(self, node):
        self.node = node
        self.label = self.node.findtext("label")
        self.attrib = node.findtext("attrib")

    @property
    def caption(self):
        """Garante que a captura de caption sempre funcione"""
        caption_element = self.node.find("caption")
        if caption_element is not None:
            return "".join(caption_element.itertext()).strip()  # Melhor que XPath "string()"
        return None

    @property
    def data(self):
        """Garante que label, caption e attrib sejam extraídos corretamente"""
        return {
            "label": self.label,
            "caption": self.caption,
            "attrib": self.attrib if self.attrib else None,  # Inclui fonte, se existir
        }
