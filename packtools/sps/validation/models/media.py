from packtools.sps.models.media import Media, InlineMedia
from packtools.sps.models.visual_resource_base import XmlVisualResource


class XmlMedias(XmlVisualResource):
    def __init__(self, xmltree):
        resource_types = [("*[name()!='supplementary-material']/media", Media), ("inline-media", InlineMedia)]
        super().__init__(xmltree, resource_types=resource_types)
