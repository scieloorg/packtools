from lxml import etree as ET

from ..utils.xml_utils import get_parent_context, put_parent_context, node_plain_text


def get_label(node):
    text = node_plain_text(node.find("./label"))
    if text is not None and text.endswith("."):
        text = text[:-1]
    return text


def get_publication_type(node):
    return node.find("./element-citation").get("publication-type")


def get_source(node):
    return node_plain_text(node.find("./element-citation/source"))


def get_main_author(node):
    try:
        return get_all_authors(node)[0]
    except IndexError:
        return


def get_all_authors(node):
    tags = ["surname", "given-names", "prefix", "suffix"]
    result = []
    authors = node.xpath("./element-citation/person-group//name")
    for author in authors:
        d = {}
        for tag in tags:
            if text := node_plain_text(author.find(tag)):
                d[tag] = text
        result.append(d)
    if collab := get_collab(node):
        result.append({"collab": collab})

    return result


def get_collab(node):
    collabs = node.xpath("./element-citation/person-group//collab")
    return [node_plain_text(collab) for collab in collabs]


def get_volume(node):
    return node_plain_text(node.find("./element-citation/volume"))


def get_issue(node):
    return node_plain_text(node.find("./element-citation/issue"))


def get_fpage(node):
    return node_plain_text(node.find("./element-citation/fpage"))


def get_lpage(node):
    return node_plain_text(node.find("./element-citation/lpage"))


def get_year(node):
    return node_plain_text(node.find("./element-citation/year"))


def get_article_title(node):
    return node_plain_text(node.find("./element-citation/article-title"))


def get_mixed_citation(node):
    return node_plain_text(node.find("./mixed-citation"))


def get_citation_ids(node):
    ids = {}
    for pub_id in node.xpath(".//pub-id"):
        ids[pub_id.attrib["pub-id-type"]] = node_plain_text(pub_id)
    return ids


def get_elocation_id(node):
    return node_plain_text(node.find("./element-citation/elocation-id"))


def get_ref_id(node):
    return node.get("id")


class ArticleCitations:

    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def article_citations(self):
        for node, lang, article_type, parent, parent_id in get_parent_context(
            self.xmltree
        ):
            for item in node.xpath("./ref-list//ref"):
                tags = [
                    ("ref_id", get_ref_id(item)),
                    ("label", get_label(item)),
                    ("publication_type", get_publication_type(item)),
                    ("source", get_source(item)),
                    ("main_author", get_main_author(item)),
                    ("all_authors", get_all_authors(item)),
                    ("volume", get_volume(item)),
                    ("issue", get_issue(item)),
                    ("fpage", get_fpage(item)),
                    ("lpage", get_lpage(item)),
                    ("elocation_id", get_elocation_id(item)),
                    ("year", get_year(item)),
                    ("article_title", get_article_title(item)),
                    ("citation_ids", get_citation_ids(item)),
                    ("mixed_citation", get_mixed_citation(item)),
                ]
                d = dict()
                for name, value in tags:
                    if value is not None and len(value) > 0:
                        try:
                            d[name] = value.text
                        except AttributeError:
                            d[name] = value
                d["author_type"] = "institutional" if get_collab(item) else "person"
                yield put_parent_context(d, lang, article_type, parent, parent_id)
