from packtools.sps.models.visual_resource_base import VisualResourceBase, XmlVisualResource


class Graphic(VisualResourceBase):
    pass

class InlineGraphic(Graphic):
    pass

class XmlGraphic(XmlVisualResource):
    RESOURCE_TYPES = [("graphic", Graphic), ("inline-graphic", InlineGraphic)]
