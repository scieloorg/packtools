
def _get_texts(node):
    texts = []
    if node.text:
        texts.append(node.text.strip())
    for child in node.getchildren():
        text = _get_texts(child).strip()
        if text:
            texts.append(text)
    if node.tail:
        texts.append(node.tail.strip())
    return " ".join(texts)


class Body:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def main_body(self):
        return self.xmltree.find(".//body")

    @property
    def main_body_texts(self):
        for node in self.main_body.xpath("*"):
            yield _get_texts(node)
