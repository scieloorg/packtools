from lxml import etree as ET


def get_label(node):
    try:
        return node.find('./label').text[:-1]
    except AttributeError:
        return


def get_source(node):
    return node.find('./element-citation/source')


def get_main_author(node):
    surname = node.find('./element-citation/person-group/name/surname')
    given_name = node.find('./element-citation/person-group/name/given-names')
    if surname is not None and given_name is not None:
        return " ".join([surname.text, given_name.text])
    else:
        return None


def get_all_authors(node):
    result = []
    authors = node.xpath('./element-citation/person-group//name')
    for author in authors:
        surname = author.find('surname')
        given_name = author.find('given-names')
        if surname is not None and given_name is not None:
            result.append(" ".join([surname.text, given_name.text]))
    return result


def get_volume(node):
    return node.find('./element-citation/volume')


def get_issue(node):
    return node.find('./element-citation/issue')


def get_fpage(node):
    return node.find('./element-citation/fpage')


def get_lpage(node):
    return node.find('./element-citation/lpage')


def get_year(node):
    return node.find('./element-citation/year')


def get_article_title(node):
    return node.find('./element-citation/article-title')


def get_mixed_citation(node):
    return node.find('./mixed-citation')


class ArticleCitations:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def article_citations(self):
        _citations = []
        for node in self.xmltree.xpath("./back/ref-list//ref"):
            tags = [
                ('label', get_label(node)),
                ('source', get_source(node)),
                ('main_author', get_main_author(node)),
                ('all_authors', get_all_authors(node)),
                ('volume', get_volume(node)),
                ('issue', get_issue(node)),
                ('fpage', get_fpage(node)),
                ('lpage', get_lpage(node)),
                ('year', get_year(node)),
                ('article_title', get_article_title(node)),
                ('mixed_citation', ET.tostring(get_mixed_citation(node), encoding=str, method='text').strip()),
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
