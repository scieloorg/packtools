def get_label(node):
    return node.find('./label').text[:-1]


def get_source(node):
    return node.find('./element-citation/source')


def get_author(node):
    surname = node.find('./element-citation/person-group/name/surname')
    given_name = node.find('./element-citation/person-group/name/given-names')
    if surname is not None and given_name is not None:
        return " ".join([surname.text, given_name.text])
    else:
        return None


def get_volume(node):
    return node.find('./element-citation/volume')


def get_issue(node):
    return node.find('./element-citation/issue')


def get_fpage(node):
    return node.find('./element-citation/fpage')


def get_year(node):
    return node.find('./element-citation/year')


def get_article_title(node):
    return node.find('./element-citation/article-title')


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
