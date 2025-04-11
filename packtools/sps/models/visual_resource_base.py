from packtools.sps.models.accessibility_data import AccessibilityData
from packtools.sps.models.article_and_subarticles import Fulltext
from packtools.sps.utils.xml_utils import tostring


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
            "tag": self.node.tag,
            "xlink_href": self.xlink_href,
            "id": self.id,
            "xml": tostring(self.node, xml_declaration=False)
        }
        data.update(
            self.accessibility.data
        )  # Adiciona os dados de acessibilidade extraídos
        return data


class XmlVisualResource:
    def __init__(self, xmltree, resource_types=None):
        self.xmltree = xmltree
        self.resource_types = resource_types if resource_types else []

    @property
    def data(self):
        """Gera dados dos recursos visuais de cada artigo e sub-artigo."""
        for node in self.xmltree.xpath(". | .//sub-article"):
            full_text = Fulltext(node)
            for resource_xpath, resource_class in self.resource_types:
                resource_nodes = full_text.node.xpath(
                    f"./front//{resource_xpath} | ./body//{resource_xpath} | ./back//{resource_xpath}"
                ) or []
                for resource_node in resource_nodes:
                    resource_instance = resource_class(resource_node)
                    resource_data = resource_instance.data
                    yield {**resource_data, **full_text.attribs_parent_prefixed}
