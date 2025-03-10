from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles
from packtools.sps.models.label_and_caption import LabelAndCaption
from packtools.sps.models.visual_resource_base import VisualResourceBase


class BaseMedia(VisualResourceBase):
    @property
    def mimetype(self):
        return self.node.get("mimetype")

    @property
    def mime_subtype(self):
        return self.node.get("mime-subtype")

    @property
    def data(self):
        base_data = super().data

        media_data = {
            "mimetype": self.mimetype,
            "mime_subtype": self.mime_subtype,
        }

        combined_data = {**base_data, **media_data}
        return combined_data


class Media(BaseMedia, LabelAndCaption):
    def __init__(self, node):
        BaseMedia.__init__(self, node)  # Chama o __init__ de BaseMedia
        LabelAndCaption.__init__(self, node)  # Chama o __init__ de LabelAndCaption

    @property
    def data(self):
        base_data = super().data
        label_caption_data = LabelAndCaption.data.fget(self)

        return {**base_data, **label_caption_data}


class InlineMedia(BaseMedia):
    pass


class XmlMedia:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.article_and_subarticle = ArticleAndSubArticles(xmltree).article_and_sub_articles

    def data(self):
        """Gera dados de mídia e inline-media de cada artigo e sub-artigo."""
        for item in self.article_and_subarticle:
            node_data = getattr(item, "data", {})

            for media_type, media_class in [("media", Media), ("inline-media", InlineMedia)]:
                nodes = item.xpath(f".//{media_type}") or []
                for node in nodes:
                    media_data = media_class(node).data
                    yield {**media_data, **node_data}
