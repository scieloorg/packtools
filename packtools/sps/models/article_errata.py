"""
<fn-group>
    <fn fn-type="other">
        <label>Additions and Corrections</label>
        <p>On page 10, where it was read:</p>
        <p>“Joao da Silva”</p>
        <p>Now reads:</p>
        <p>“João da Silva Santos”</p>
    </fn>
</fn-group>
"""


class ArticleErrata:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def article_errata(self):
        _errata = []

        for node in self.xmltree.xpath(".//fn-group//fn[@fn-type='other']"):
            _errata.append(Erratum(node))

        return _errata


class Erratum:
    def __init__(self, node):
        self.node = node
