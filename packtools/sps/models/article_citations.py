from lxml import etree as ET


def get_label(node):
    try:
        return node.find('./label').text[:-1]
    except AttributeError:
        return


def get_source(node):
    return node.find('./element-citation/source')


def get_main_author(node):
    return get_all_authors(node)[0]


def get_all_authors(node):
    result = []
    authors = node.xpath('./element-citation/person-group//name')
    for author in authors:
        d = {}
        try:
            d['surname'] = author.find('surname').text
        except AttributeError:
            pass
        try:
            d['given_name'] = author.find('given-names').text
        except AttributeError:
            pass
        try:
            d['prefix'] = author.find('prefix').text
        except AttributeError:
            pass
        try:
            d['suffix'] = author.find('suffix').text
        except AttributeError:
            pass
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


def get_citation_ids(node):
    ids = {}
    for pub_id in node.xpath('.//pub-id'):
        ids[pub_id.attrib['pub-id-type']] = pub_id.text
    return ids


def get_elocation_id(node):
    return node.find('./element-citation/elocation-id')


def get_ref_id(node):
    return node.get('id')

class ArticleCitations:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def article_citations(self):
        for node in self.xmltree.xpath("./back/ref-list//ref"):
            tags = [
                ('ref_id', get_ref_id(node)),
                ('label', get_label(node)),
                ('source', get_source(node)),
                ('main_author', get_main_author(node)),
                ('all_authors', get_all_authors(node)),
                ('volume', get_volume(node)),
                ('issue', get_issue(node)),
                ('fpage', get_fpage(node)),
                ('lpage', get_lpage(node)),
                ('elocation_id', get_elocation_id(node)),
                ('year', get_year(node)),
                ('article_title', get_article_title(node)),
                ('mixed_citation', ET.tostring(get_mixed_citation(node), encoding=str, method='text').strip()),
                ('citation_ids', get_citation_ids(node))
            ]

            d = dict()
            for name, value in tags:
                if value is not None:
                    try:
                        d[name] = value.text
                    except AttributeError:
                        d[name] = value
            yield d
