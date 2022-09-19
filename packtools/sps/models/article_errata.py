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


class ArticleWithErrataNotes:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    def footnotes(self, fn_types=None):
        _errata = []

        if not fn_types:
            xpath_pattern = ".//fn-group//fn[@fn-type='other']"
        else:
            xpath_pattern = "|".join([".//fn-group//fn[@fn-type='{0}']".format(i) for i in fn_types])

        for node in self.xmltree.xpath(xpath_pattern):
            _errata.append(Footnote(node))

        return _errata


class Footnote:
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
