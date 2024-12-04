import itertools

from packtools.sps.utils.xml_utils import put_parent_context, tostring


# https://jats.nlm.nih.gov/publishing/tag-library/1.4/attribute/ref-type.html
ELEMENT_NAME = {
    "table": "table-wrap",
    "bibr": "ref",
}

def get_element_name(ref_type):
    try:
        return ELEMENT_NAME[ref_type]
    except KeyError:
        return ref_type


class Xref:
    """<xref ref-type="aff" rid="aff1">1</xref>"""

    def __init__(self, node):
        self.xref_node = node
        self.xref_type = self.xref_node.get("ref-type")
        self.xref_rid = self.xref_node.get("rid")
        self.xref_text = self.xref_node.text

    @property
    def data(self):
        return {
            "ref-type": self.xref_type,
            "rid": self.xref_rid,
            "text": self.xref_text,
            "element_name": get_element_name(self.xref_type)
        }


class Id:
    """<aff id="aff1"><p>affiliation</p></aff>"""

    def __init__(self, node):
        self.node = node
        self.node_id = self.node.get("id")
        self.node_tag = self.node.tag
        self.str_main_tag = f'<{self.node_tag} id="{self.node_id}">'

    def xml(self, doctype=None, pretty_print=True, xml_declaration=True):
        return tostring(
            node=self.node,
            doctype=doctype,
            pretty_print=pretty_print,
            xml_declaration=xml_declaration,
        )

    def __str__(self):
        return tostring(self.node)

    @property
    def data(self):
        return {"tag": self.node_tag, "id": self.node_id}


class Ids:
    def __init__(self, node):
        """
        Initializes the Ids class with an XML node.

        Parameters:
        node : lxml.etree._Element
            The XML node (element) that contains one or more <node @id> elements.
            This can be the root of an `xml_tree` or a node representing a `sub-article`.
        """
        self.node = node
        self.parent = self.node.tag
        self.parent_id = self.node.get("id")
        self.article_type = node.get("article-type")
        self.lang = self.node.get("{http://www.w3.org/XML/1998/namespace}lang")

    def ids(self, element_name="*"):
        if self.parent == "article":
            path = f"./front//{element_name}[@id] | ./body//{element_name}[@id] | ./back//{element_name}[@id]"
        else:
            path = f".//{element_name}[@id]"

        for id_node in self.node.xpath(path):
            id_data = Id(id_node).data

            yield put_parent_context(
                id_data, self.lang, self.article_type, self.parent, self.parent_id
            )


class ArticleXref:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    def all_ids(self, element_name):
        response = {}
        for item in itertools.chain(
            self.article_ids(element_name),
            self.sub_article_translation_ids(element_name),
            self.sub_article_non_translation_ids(element_name),
        ):
            id = item.get("id")
            response.setdefault(id, [])
            response[id].append(item)
        return response

    def all_xref_rids(self):
        response = {}
        for xref_node in self.xml_tree.xpath(".//xref"):
            xref_data = Xref(xref_node).data
            rid = xref_data.get("rid")
            response.setdefault(rid, [])
            response[rid].append(xref_data)
        return response

    def article_ids(self, element_name):
        yield from Ids(self.xml_tree.find(".")).ids(element_name)

    def sub_article_translation_ids(self, element_name):
        for node in self.xml_tree.xpath(".//sub-article[@article-type='translation']"):
            yield from Ids(node).ids(element_name)

    def sub_article_non_translation_ids(self, element_name):
        for node in self.xml_tree.xpath(".//sub-article[@article-type!='translation']"):
            yield from Ids(node).ids(element_name)
