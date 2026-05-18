from packtools.sps.models.graphic import Graphic, InlineGraphic
from packtools.sps.models.visual_resource_base import XmlVisualResource


class XmlGraphic(XmlVisualResource):
    def __init__(self, xmltree):
        resource_types = [("graphic", Graphic), ("inline-graphic", InlineGraphic)]
        super().__init__(xmltree, resource_types=resource_types)
