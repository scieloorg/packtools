from packtools.sps.models.accessibility_data import AccessibilityData


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
