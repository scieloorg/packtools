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

    @property
    def label(self):
        _label = ''
        try:
            fc = self.node.getchildren()[0]
            if fc.tag == 'label':
                _label = fc.text
        except IndexError:
            ...
        finally:
            return _label


    @property
    def text(self):
        return '\n'.join([t for t in self.node.itertext()])
