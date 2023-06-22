from lxml import etree as ET


def get_label(node):
    try:
        return node.find('./label').text[:-1]
    except AttributeError:
        return


def get_source(node):
    return node.find('./element-citation/source')


def get_main_author(node):
    main_author = {}
    if node.find('./element-citation/person-group/name/surname') is not None:
        main_author['surname'] = node.find('./element-citation/person-group/name/surname').text
    if node.find('./element-citation/person-group/name/given-names') is not None:
        main_author['given_name'] = node.find('./element-citation/person-group/name/given-names').text
    if node.find('./element-citation/person-group/name/prefix') is not None:
        main_author['prefix'] = node.find('./element-citation/person-group/name/prefix').text
    if node.find('./element-citation/person-group/name/suffix') is not None:
        main_author['suffix'] = node.find('./element-citation/person-group/name/suffix').text

    return main_author


def get_all_authors(node):
    result = []
    authors = node.xpath('./element-citation/person-group//name')
    for author in authors:
        d = {}
        if author.find('surname') is not None:
            d['surname'] = author.find('surname').text
        if author.find('given-names') is not None:
            d['given_name'] = author.find('given-names').text
        if author.find('prefix') is not None:
            d['prefix'] = author.find('prefix').text
        if author.find('suffix') is not None:
            d['suffix'] = author.find('suffix').text
        result.append(d)
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
