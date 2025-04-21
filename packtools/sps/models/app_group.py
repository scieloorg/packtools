from packtools.sps.models.article_and_subarticles import Fulltext
from packtools.sps.models.label_and_caption import LabelAndCaption
from packtools.sps.models.media import Media
from packtools.sps.models.graphic import Graphic


class App(LabelAndCaption):
    @property
    def id(self):
        return self.node.get("id")

    @property
    def graphics(self):
        """Retorna uma lista de dados de gráficos (<graphic>) dentro do <app>."""
        return [Graphic(graphic).data for graphic in self.node.xpath(".//graphic")]

    @property
    def media(self):
        """Retorna uma lista de dados de mídias (<media>) dentro do <app>."""
        return [Media(media).data for media in self.node.xpath(".//media")]

    @property
    def data(self):
        """Inclui os atributos de LabelAndCaption e adiciona 'id', 'graphics' e 'media'."""
        base_data = super().data or {}
        return {
            **base_data,
            "id": self.id,
            "graphics": self.graphics,
            "media": self.media,
        }


class XmlAppGroup:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    @property
    def data(self):
        for node in self.xml_tree.xpath(".|.//sub-article"):
            full_text = Fulltext(node)

            for app_node in node.xpath("./back//app"):
                app_data = App(app_node).data
                yield {**app_data, **full_text.attribs_parent_prefixed}
