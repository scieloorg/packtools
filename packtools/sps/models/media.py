from packtools.sps.models.article_and_subarticles import Fulltext
from packtools.sps.models.accessibility_data import AccessibilityData


class Media:
    def __init__(self, node):
        self.node = node
        self.accessibility = AccessibilityData(node)

    @property
    def mimetype(self):
        return self.node.get("mimetype")

    @property
    def mime_subtype(self):
        return self.node.get("mime-subtype")

    @property
    def media_type(self):
        return self.node.tag if self.node is not None else None

    @property
    def xlink_href(self):
        return self.node.get("{http://www.w3.org/1999/xlink}href")

    @property
    def data(self):
        """Combina os dados de mídia com os dados de acessibilidade extraídos do XML."""
        data = {
            "mimetype": self.mimetype,
            "mime_subtype": self.mime_subtype,
            "media_type": self.media_type,
            "xlink_href": self.xlink_href,
        }
        data.update(self.accessibility.data)  # Adiciona os dados de acessibilidade extraídos
        return data


class XmlMedias:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    @property
    def items(self):
        media_list = []
        # TODO sub-article está sendo considerado em duplicidade
        for node in self.xml_tree.xpath(". | sub-article"):
            full_text = Fulltext(node)
            for media_node in full_text.node.xpath(".//media | .//graphic"):
                media_data = Media(media_node).data
                media_data.update(full_text.attribs_parent_prefixed)
                media_list.append(media_data)
        return media_list
