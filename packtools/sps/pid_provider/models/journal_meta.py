"""
<journal-meta>
    <journal-id journal-id-type="publisher-id">tinf</journal-id>
    <journal-id journal-id-type="nlm-ta">Rev Saude Publica</journal-id>
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
        return self.xmltree.findtext('.//journal-meta//issn[@pub-type="epub"]') or ""

    @property
    def ppub(self):
        return self.xmltree.findtext('.//journal-meta//issn[@pub-type="ppub"]') or ""


class Acronym:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def text(self):
        return self.xmltree.findtext(
            './/journal-meta//journal-id[@journal-id-type="publisher-id"]'
        )


class Title:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def data(self):
        _data = []

        _data.append(
            {
                "type": "main",
                "value": self.journal_title,
            }
        )
        _data.append(
            {
                "type": "abbreviated",
                "value": self.abbreviated_journal_title,
            }
        )

        return _data

    @property
    def abbreviated_journal_title(self):
        return self.xmltree.findtext(
            './/journal-meta//journal-title-group//abbrev-journal-title[@abbrev-type="publisher"]'
        )

    @property
    def journal_title(self):
        return self.xmltree.findtext(
            ".//journal-meta//journal-title-group//journal-title"
        )


class Publisher:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def publishers_names(self):
        names = []
        for node in self.xmltree.xpath(".//journal-meta//publisher//publisher-name"):
            names.append(node.text)
        return names


class JournalID:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def nlm_ta(self):
        return self.xmltree.findtext(
            './/journal-meta//journal-id[@journal-id-type="nlm-ta"]'
        )
