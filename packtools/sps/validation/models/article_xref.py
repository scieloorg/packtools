from packtools.sps.models.v2.article_xref import Xref, Element
from packtools.sps.models.article_and_subarticles import Fulltext


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

    def all_xrefs(self):
        """Returns a list of data dicts for all <xref> elements in the document."""
        result = []
        for xref_node in self.xml_tree.xpath(".//xref"):
            xref = Xref(xref_node)
            data = xref.data
            data["xml"] = xref.xml
            content = (data.get("content") or "").strip()
            data["has_text_content"] = bool(content)
            result.append(data)
        return result

    def all_ids(self):
        """Returns a set of all @id attribute values in the document."""
        ids = set()
        for node in self.xml_tree.xpath(".//*[@id]"):
            id_val = node.get("id")
            if id_val:
                ids.add(id_val)
        return ids

    def transcript_sections(self):
        """Returns a list of @id values for <sec sec-type='transcript'> elements."""
        result = []
        for node in self.xml_tree.xpath('.//sec[@sec-type="transcript"]'):
            sec_id = node.get("id")
            if sec_id:
                result.append(sec_id)
        return result
