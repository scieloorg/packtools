
class ArticleCitations:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def article_citations(self):
        _citations = []
        for node in self.xmltree.xpath("./back/ref-list//ref"):
            label = get_label(node)
            source = get_source(node)
            author = get_author(node)
            volume = get_volume(node)
            issue = get_issue(node)
            fpage = get_fpage(node)
            year = get_year(node)
            article_title = get_article_title(node)

            tags = [
                ('label', label),
                ('source', source),
                ('author', author),
                ('volume', volume),
                ('issue', issue),
                ('fpage', fpage),
                ('year', year),
                ('article_title', article_title)
            ]

            d = dict()
            for name, value in tags:
                if value is not None:
                    try:
                        d[name] = value.text
                    except AttributeError:
                        d[name] = value
            _citations.append(d)
        return _citations
