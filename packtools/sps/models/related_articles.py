"""
<related-article ext-link-type="doi" id="A01" related-article-type="commentary-article" xlink:href="10.1590/0101-3173.2022.v45n1.p139">
Referência do artigo comentado: FREITAS, J. H. de. Cinismo e indiferenciación: la huella de Glucksmann en
<italic>El coraje de la verdad</italic>
de Foucault.
<bold>Trans/form/ação</bold>
: revista de Filosofia da Unesp, v. 45, n. 1, p. 139-158, 2022.
</related-article>
"""


class RelatedItems:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def related_articles(self):
        for item in self.xmltree.xpath(".//related-article"):
            d = {}
            for k in item.attrib:
                if k == '{http://www.w3.org/1999/xlink}href':
                    d['href'] = item.attrib.get(k)
                else:
                    d[k] = item.attrib.get(k)
            yield d

    @property
    def related_objects(self):
        # TODO
        pass
