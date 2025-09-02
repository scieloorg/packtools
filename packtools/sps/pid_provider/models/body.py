
class Body:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def main_body(self):
        return self.xmltree.find(".//body")

    @property
    def main_body_texts(self):
        for node in self.main_body.xpath("*"):
            yield " ".join([item for item in node.xpath(".//text()") if item.strip()])
