from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context

class SupplementaryMaterial:
    def __init__(self, node):
        self.node = node
        self._parent_node = node.getparent()

    @property
    def id(self):
        return self.node.get("id")

    @property
    def parent(self):
        return self._parent_node.tag if self._parent_node is not None else None

    @property
    def sec_type(self):
        return self._parent_node.get("sec-type")

    @property
    def label(self):
        return self.node.findtext("label")

    @property
    def caption_title(self):
        return self.node.findtext("caption/title")

    @property
    def media_node(self):
        node = self.node.findall("media") or self.node.findall("graphic")
        return node[0] if node else None

    @property
    def mimetype(self):
        return self.media_node.get("mimetype") if self.media_node is not None else None

    @property
    def mime_subtype(self):
        return self.media_node.get("mime-subtype") if self.media_node is not None else None

    @property
    def xlink_href(self):
        return self.media_node.get("{http://www.w3.org/1999/xlink}href") if self.media_node is not None else None

    @property
    def media_type(self):
        return self.media_node.tag if self.media_node is not None else None

    @property
    def data(self):
        return {
            "id": self.id,
            "parent_tag": self.parent,
            "parent_attrib_type": self.sec_type,
            "label": self.label,
            "caption_title": self.caption_title,
            "mimetype": self.mimetype,
            "mime_subtype": self.mime_subtype,
            "xlink_href": self.xlink_href,
            "media_type": self.media_type,
            "media_node": self.media_node
        }


class ArticleSupplementaryMaterials:
    def __init__(self, xml_tree):
        """
        Extrai todos os <supplementary-material> e <sec sec-type="supplementary-material"> dentro do artigo.

        Args:
            xml_tree: Objeto XML representando o artigo
        """
        self.xml_tree = xml_tree

    def data(self):
        """Itera sobre os <supplementary-material> e retorna os dados extraídos."""
        for node, lang, article_type, parent, parent_id in get_parent_context(self.xml_tree):
            for supp_node in node.xpath(".//supplementary-material"):
                supp_data = SupplementaryMaterial(supp_node).data
                yield put_parent_context(supp_data, lang, article_type, parent, parent_id)
