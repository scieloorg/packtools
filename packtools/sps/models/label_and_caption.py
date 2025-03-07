class LabelAndCaption:
    def __init__(self, node):
        self.node = node
        self.id = node.get("id")
        self.label = node.findtext("label")

    @property
    def caption(self):
        caption_element = self.node.find(".//caption")
        if caption_element is not None:
            return caption_element.xpath("string()").strip()

    @property
    def data(self):
        return {
            "id": self.id,
            "label": self.label,
            "caption": self.caption
        }

    @property
    def xml(self):
        if self.id:
            return f'<{self.node.tag} id="{self.id}">'
        return f'<{self.node.tag}>'
