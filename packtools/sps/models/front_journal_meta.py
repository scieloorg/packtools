"""
<journal-meta>
    <journal-id journal-id-type="publisher-id">tinf</journal-id>
    <journal-title-group>
        <journal-title>Transinformação</journal-title>
        <abbrev-journal-title abbrev-type="publisher">Transinformação</abbrev-journal-title>
    </journal-title-group>
    <issn pub-type="ppub">0103-3786</issn>
    <issn pub-type="epub">2318-0889</issn>
    <publisher>
        <publisher-name>Pontifícia Universidade Católica de Campinas</publisher-name>
    </publisher>
</journal-meta>
"""


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
 