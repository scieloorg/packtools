from packtools.sps.models.visual_resource_base import (
    VisualResourceBase,
    XmlVisualResource,
)


class Graphic(VisualResourceBase):
    pass


class InlineGraphic(Graphic):
    pass


class XmlGraphic(XmlVisualResource):
    def __init__(self, xmltree):
        resource_types = [("graphic", Graphic), ("inline-graphic", InlineGraphic)]
        super().__init__(xmltree, resource_types=resource_types)
