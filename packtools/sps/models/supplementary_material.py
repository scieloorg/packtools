from packtools.sps.models.graphic import Graphic
from packtools.sps.models.label_and_caption import LabelAndCaption
from packtools.sps.models.article_and_subarticles import Fulltext
from packtools.sps.models.media import Media


class SupplementaryMaterial(LabelAndCaption):
    def __init__(self, node):
        super().__init__(node)
        self.id = node.get("id")
        self._parent_node = node.getparent()
        media_nodes = node.xpath("./media")
        graphic_nodes = node.xpath("./graphic")
        self.media = None
        self.graphic = None
        self.media_node = None
        self.graphic_node = None
        if media_nodes:
            self.media_node = media_nodes[0]
            self.media = Media(self.media_node)
            self.graphic_node = None
            self.graphic = None
        elif graphic_nodes:
            self.media_node = None
            self.media = None
            self.graphic_node = graphic_nodes[0]
            self.graphic = Graphic(self.graphic_node)

    def __getattr__(self, name):
        if self.media is not None and hasattr(self.media, name):
            return getattr(self.media, name)

        if self.graphic is not None and hasattr(self.graphic, name):
            return getattr(self.graphic, name)



        raise AttributeError(f"SupplementaryMaterial has no attribute {name}")

    @property
    def parent_tag(self):
        return self._parent_node.tag if self._parent_node is not None else None

    @property
    def sec_type(self):
        return self._parent_node.get("sec-type") if self.parent_tag == "sec" else None

    @property
    def xml(self):
        if self.id:
            return f'<supplementary-material id="{self.id}">'
        else:
            return "<supplementary-material>"

    @property
    def data(self):
        base_data = super().data.copy()
        base_data.update(self.media.data if self.media else {})
        base_data.update(self.graphic.data if self.graphic else {})
        base_data.update(
            {
                "id": self.id,
                "parent_suppl_mat": self.parent_tag,
                "sec_type": self.sec_type,
                "visual_elem": "media" if self.media else "graphic",
            }
        )

        return base_data


class XmlSupplementaryMaterials:
    def __init__(self, xml_tree):
        """
        Extrai todos os <supplementary-material> e <sec sec-type="supplementary-material"> dentro do artigo.

        Args:
            xml_tree: Objeto XML representando o artigo
        """
        self.xml_tree = xml_tree

    @property
    def items_by_id(self):
        """
        De acordo com o SPS 1.10, não é permitido o uso de <inline-supplementary-material>, assim, o modelo não
        considera esse elemento, apesar de ele poder existir.
        """
        supp_dict = {}
        for node in self.xml_tree.xpath(". | sub-article"):
            node_id = node.get("id") if node.get("id") else "main_article"
            supp_dict.setdefault(node_id, [])
            full_text = Fulltext(node)
            for supp_node in full_text.node.xpath(".//supplementary-material"):
                supp_data = SupplementaryMaterial(supp_node).data
                supp_data.update(full_text.attribs_parent_prefixed)
                supp_dict[node_id].append(supp_data)
        return supp_dict

    @property
    def items(self):
        for item in self.items_by_id.values():
            yield from item
