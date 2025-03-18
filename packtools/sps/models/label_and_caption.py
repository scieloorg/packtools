class LabelAndCaption:
    def __init__(self, node):
        self.node = node
        self.label = self.node.findtext("label")
        self.attrib = node.findtext("attrib")

    @property
    def caption(self):
        caption_element = self.node.find("caption")
        if caption_element is not None:
            return "".join(caption_element.itertext()).strip()
        return None

    @property
    def data(self):
        return {
            "label": self.label,
            "caption": self.caption,
            "attrib": self.attrib if self.attrib else None,  # Inclui fonte, se existir
        }
