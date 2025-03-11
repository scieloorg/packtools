from packtools.sps.models.accessibility_data import AccessibilityData
from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles, Fulltext


class VisualResourceBase:
    def __init__(self, node):
        self.node = node
        self.accessibility = AccessibilityData(node)

    @property
    def xlink_href(self):
        return self.node.get("{http://www.w3.org/1999/xlink}href")

    @property
    def id(self):
        return self.node.get("id")

    @property
    def data(self):
        data = {
            "xlink_href": self.xlink_href,
            "id": self.id
        }
        data.update(self.accessibility.data)  # Adiciona os dados de acessibilidade extraídos
        return data


class XmlVisualResource:
    RESOURCE_TYPES = []

    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.article_and_subarticles = ArticleAndSubArticles(xmltree).article_and_sub_articles

    def data(self):
        """Gera dados dos recursos visuais de cada artigo e sub-artigo."""
        for node in self.article_and_subarticles:
            full_text = Fulltext(node)

            for resource_type, resource_class in self.RESOURCE_TYPES:
                resource_nodes = node.xpath(f".//{resource_type}") or []
                for resource_node in resource_nodes:
                    resource_instance = resource_class(resource_node)
                    resource_data = resource_instance.data
                    yield {**resource_data, **full_text.attribs_parent_prefixed}
