from lxml import etree as ET

from ..utils import xml_utils


def get_label(node):
    text = xml_utils.node_plain_text(node.find('./label'))
    if text is not None and text.endswith('.'):
        text = text[:-1]
    return text


def get_publication_type(node):
    return node.find('./element-citation').get('publication-type')


def get_source(node):
    return xml_utils.node_plain_text(node.find('./element-citation/source'))


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
            if text := xml_utils.node_plain_text(author.find(tag)):
                d[tag] = text
        result.append(d)
    if collab := get_collab(node):
        result.append({'collab': collab})

    return result


def get_collab(node):
    collabs = node.xpath('./element-citation/person-group//collab')
    return [xml_utils.node_plain_text(collab) for collab in collabs]


def get_volume(node):
    return xml_utils.node_plain_text(node.find('./element-citation/volume'))


def get_issue(node):
    return xml_utils.node_plain_text(node.find('./element-citation/issue'))


def get_fpage(node):
    return xml_utils.node_plain_text(node.find('./element-citation/fpage'))


def get_lpage(node):
    return xml_utils.node_plain_text(node.find('./element-citation/lpage'))


def get_year(node):
    return xml_utils.node_plain_text(node.find('./element-citation/year'))


def get_article_title(node):
    return xml_utils.node_plain_text(node.find('./element-citation/article-title'))


def get_mixed_citation(node):
    return xml_utils.node_plain_text(node.find('./mixed-citation'))


def get_citation_ids(node):
    ids = {}
    for pub_id in node.xpath('.//pub-id'):
        ids[pub_id.attrib['pub-id-type']] = xml_utils.node_plain_text(pub_id)
    return ids


def get_elocation_id(node):
    return xml_utils.node_plain_text(node.find('./element-citation/elocation-id'))


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
                ('publication_type', get_publication_type(node)),
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
                ('citation_ids', get_citation_ids(node)),
                ('mixed_citation', get_mixed_citation(node))
            ]
            d = dict()
            for name, value in tags:
                if value is not None and len(value) > 0:
                    try:
                        d[name] = value.text
                    except AttributeError:
                        d[name] = value
            d['author_type'] = 'institutional' if get_collab(node) else 'person'
            yield d
