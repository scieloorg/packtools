
class ArticleCitations:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def article_citations(self):
        _citations = []
        for node in self.xmltree.xpath("./back/ref-list//ref"):
            d = dict(
                label=node.xpath('./label')[0].text[:-1],
                journal_title=node.xpath('./element-citation/source')[0].text,
                author=" ".join([node.xpath('./element-citation/person-group/name/surname')[0].text,
                                node.xpath('./element-citation/person-group/name/given-names')[0].text]),
                volume=node.xpath('./element-citation/volume')[0].text,
                first_page=node.xpath('./element-citation/fpage')[0].text,
                cYear=node.xpath('./element-citation/year')[0].text,
                article_title=node.xpath('./element-citation/article-title')[0].text
            )
            _citations.append(d)
        return _citations
