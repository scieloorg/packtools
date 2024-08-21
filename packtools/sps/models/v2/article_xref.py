from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context


class Xref:
    """<xref ref-type="aff" rid="aff1">1</xref>"""

    def __init__(self, node):
        self.xref_node = node
        self.xref_type = self.xref_node.get("ref-type")
        self.xref_rid = self.xref_node.get("rid")
        self.xref_parent = self.xref_node.getparent().tag
        self.xref_text = self.xref_node.text

    @property
    def data(self):
        return {
            "ref-type": self.xref_type,
            "rid": self.xref_rid,
            "text": self.xref_text,
            "parent-tag": self.xref_parent,
        }


class Id:
    """<aff id="aff1"><p>affiliation</p></aff>"""

    def __init__(self, node):
        self.node = node
        self.node_id = self.node.get("id")
        self.node_tag = self.node.tag

    @property
    def data(self):
        return {"tag": self.node_tag, "id": self.node_id}


class Xrefs:
    def __init__(self, node, lang, article_type, parent, parent_id):
        self.node = node
        self.lang = lang
        self.article_type = article_type
        self.parent = parent
        self.parent_id = parent_id

    def xrefs(self):
        for xref_node in self.node.xpath(".//xref"):
            xref_data = Xref(xref_node).data
            yield put_parent_context(
                xref_data, self.lang, self.article_type, self.parent, self.parent_id
            )


class Ids:
    def __init__(self, node, lang, article_type, parent, parent_id):
        self.node = node
        self.lang = lang
        self.article_type = article_type
        self.parent = parent
        self.parent_id = parent_id

    def ids(self):
        for id_node in self.node.xpath(".//*[@id]"):
            id_data = Id(id_node).data
            yield put_parent_context(
                id_data, self.lang, self.article_type, self.parent, self.parent_id
            )


class ArticleXref:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    def all_ids(self):
        for node, lang, article_type, parent, parent_id in get_parent_context(
            self.xml_tree
        ):
            yield from Ids(node, lang, article_type, parent, parent_id).ids()

    def all_xref_rids(self):
        for node, lang, article_type, parent, parent_id in get_parent_context(
            self.xml_tree
        ):
            yield from Xrefs(node, lang, article_type, parent, parent_id).xrefs()

    def article_ids(self):
        for item in self.all_ids():
            if item.get("parent") == "article":
                yield item

    def article_xref_rids(self):
        for item in self.all_xref_rids():
            if item.get("parent") == "article":
                yield item

    def sub_article_translation_ids(self):
        for item in self.all_ids():
            if (
                item.get("parent") == "sub-article"
                and item.get("parent_article_type") == "translation"
            ):
                yield item

    def sub_article_translation_xref_rids(self):
        for item in self.all_xref_rids():
            if (
                item.get("parent") == "sub-article"
                and item.get("parent_article_type") == "translation"
            ):
                yield item

    def sub_article_non_translation_ids(self):
        for item in self.all_ids():
            if (
                item.get("parent") == "sub-article"
                and item.get("parent_article_type") != "translation"
            ):
                yield item

    def sub_article_non_translation_xref_rids(self):
        for item in self.all_xref_rids():
            if (
                item.get("parent") == "sub-article"
                and item.get("parent_article_type") != "translation"
            ):
                yield item
