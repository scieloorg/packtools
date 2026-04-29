from packtools.sps.models.article_and_subarticles import Fulltext
from packtools.sps.models.supplementary_material import SupplementaryMaterial


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
        for node in self.xml_tree.xpath(". | .//sub-article"):
            node_id = node.get("id") if node.get("id") else "main_article"
            supp_dict.setdefault(node_id, [])
            full_text = Fulltext(node)
            for supp_node in full_text.node.xpath(
                    "./front-stub//supplementary-material | ./front//supplementary-material | ./body//supplementary-material | ./back//supplementary-material"
            ) or []:
                supp_data = SupplementaryMaterial(supp_node).data
                supp_data.update(full_text.attribs_parent_prefixed)
                supp_dict[node_id].append(supp_data)
        return supp_dict

    @property
    def items(self):
        for item in self.items_by_id.values():
            yield from item
