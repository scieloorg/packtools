from lxml import etree as ET

from ..utils import xml_utils


def _text(node):
    return xml_utils.node_plain_text(node)


def get_label(node):
    text = _text(node.find('./label'))
    if text is not None and text.endswith('.'):
        text = text[:-1]
    return text


def get_source(node):
    return _text(node.find('./element-citation/source'))


def get_main_author(node):
    try:
        return get_all_authors(node)[0]
    except IndexError:
        return


def get_all_authors(node):
    tags = ['surname', 'given-names', 'prefix', 'suffix']
    result = []
    authors = node.xpath('./element-citation/person-group//name')
    for author in authors:
        d = {}
        for tag in tags:
            if text := _text(author.find(tag)):
                d[tag] = text
        result.append(d)

    return result


def get_volume(node):
    return _text(node.find('./element-citation/volume'))


def get_issue(node):
    return _text(node.find('./element-citation/issue'))


def get_fpage(node):
    return _text(node.find('./element-citation/fpage'))


def get_lpage(node):
    return _text(node.find('./element-citation/lpage'))


def get_year(node):
    return _text(node.find('./element-citation/year'))


def get_article_title(node):
    return _text(node.find('./element-citation/article-title'))


def get_mixed_citation(node):
    return _text(node.find('./mixed-citation'))


def get_citation_ids(node):
    ids = {}
    for pub_id in node.xpath('.//pub-id'):
        ids[pub_id.attrib['pub-id-type']] = _text(pub_id)
    return ids


def get_elocation_id(node):
    return _text(node.find('./element-citation/elocation-id'))


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
                ('citation_ids', get_citation_ids(node))
            ]
            mixed_citation = get_mixed_citation(node)
            if mixed_citation is not None:
                tags.append(('mixed_citation', ET.tostring(mixed_citation, encoding=str, method='text').strip()))

            d = dict()
            for name, value in tags:
                if value is not None:
                    try:
                        d[name] = value.text
                    except AttributeError:
                        d[name] = value
            yield d
