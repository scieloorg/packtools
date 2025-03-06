from packtools.sps.utils.xml_utils import tostring
from packtools.sps.models.article_and_subarticles import Fulltext


# https://jats.nlm.nih.gov/publishing/tag-library/1.4/attribute/ref-type.html
ELEMENT_NAME = {
    "table": "table-wrap",
    "bibr": "ref",
}
REF_TYPE = {
    "table-wrap": "table",
    "ref": "bibr",
}


def get_element_name(ref_type):
    try:
        return ELEMENT_NAME[ref_type]
    except KeyError:
        return ref_type


def get_ref_type(element_name):
    try:
        return REF_TYPE[element_name]
    except KeyError:
        return element_name


class Xref:
    """<xref ref-type="aff" rid="aff1">1</xref>"""

    def __init__(self, node):
        self.xref_node = node
        self.xref_type = self.xref_node.get("ref-type")
        self.xref_rid = self.xref_node.get("rid")
        self.xref_text = self.xref_node.text

    @property
    def tag_and_attribs(self):
        items = [
            f"<{self.xref_node.tag} ",
            " ".join(f'{k}="{v}"' for k, v in self.xref_node.attrib.items()),
            ">"
        ]
        return "".join(items)

    @property
    def element_name(self):
        return get_element_name(self.xref_type)

    @property
    def elem_xml(self):
        if self.xref_rid:
            return f'<{self.element_name} id="{self.xref_rid}">'
        return f'<{self.element_name}>'

    @property
    def xml(self):
        return tostring(self.xref_node)

    @property
    def data(self):
        return {
            "ref-type": self.xref_type,
            "rid": self.xref_rid,
            "text": self.xref_text,
            "elem_xml": self.elem_xml,
            "elem_name": self.element_name,
            "content": " ".join(self.xref_node.xpath(".//text()")),
            "tag_and_attribs": self.tag_and_attribs,
        }


class Element:
    """<aff id="aff1"><p>affiliation</p></aff>"""

    def __init__(self, node):
        self.node = node
        self.node_id = self.node.get("id")
        self.node_tag = self.node.tag

    @property
    def tag_id(self):
        if self.node_id:
            return f'<{self.node_tag} id="{self.node_id}">'
        return f'<{self.node_tag}>'

    @property
    def tag_and_attribs(self):
        items = [
            f"<{self.node.tag} ",
            " ".join(f'{k}="{v}"' for k, v in self.node.attrib.items()),
            ">"
        ]
        return "".join(items)

    def xml(self, doctype=None, pretty_print=True, xml_declaration=True):
        return tostring(
            node=self.node,
            doctype=doctype,
            pretty_print=pretty_print,
            xml_declaration=xml_declaration,
        )

    @property
    def ref_type(self):
        return get_ref_type(self.node_tag)

    @property
    def xref_xml(self):
        if self.node_id:
            return f'<xref ref-type="{self.ref_type}" rid="{self.node_id}">'
        return f'<xref ref-type="{self.ref_type}">'

    def __str__(self):
        return tostring(self.node)

    @property
    def data(self):
        return {"tag": self.node_tag, "id": self.node_id, "xref_xml": self.xref_xml, "tag_id": self.tag_id, "tag_and_attribs": self.tag_and_attribs}


class XMLCrossReference:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    def elems_by_id(self, element_name="*", attribs=None):
        elems = {}
        xpaths = []
        if attribs:
            for attr in attribs or []:
                name = attr["name"]
                value = attr["value"]
                xpaths.append(f'.//{element_name}[@{name}="{value}"]')
        else:
            xpaths.append(f'.//{element_name}')

        for node in self.xml_tree.xpath(". | .//sub-article"):
            fulltext = Fulltext(node)
            for item in fulltext.node.xpath("|".join(xpaths)):
                elem = Element(item)
                data = fulltext.attribs_parent_prefixed
                data.update(elem.data)
                e_id = item.get("id")
                elems.setdefault(e_id, [])
                elems[e_id].append(data)
        return elems

    def xrefs_by_rid(self):
        response = {}
        for xref_node in self.xml_tree.xpath(".//xref"):
            xref_data = Xref(xref_node).data
            rid = xref_data.get("rid")
            response.setdefault(rid, [])
            response[rid].append(xref_data)
        return response
