
class ISSN:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def data(self):
        return [
            {"type": node.get("pub-type"), "value": node.text}
            for node in self.xmltree.xpath(".//journal-meta/issn")
        ]

    @property
    def epub(self):
        return self.xmltree.findtext('.//journal-meta//issn[@pub-type="epub"]')

    @property
    def ppub(self):
        return self.xmltree.findtext('.//journal-meta//issn[@pub-type="ppub"]')
 