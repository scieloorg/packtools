from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context


class Media:
    def __init__(self, node):
        self.node = node

    @property
    def mimetype(self):
        return self.node.get("mimetype")

    @property
    def mime_subtype(self):
        return self.node.get("mime-subtype")

    @property
    def xlink_href(self):
        return self.node.get("{http://www.w3.org/1999/xlink}href")

    @property
    def data(self):
        return {
            "mimetype": self.mimetype,
            "mime_subtype": self.mime_subtype,
            "xlink_href": self.xlink_href,
        }


class ArticleMedias:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    def data(self):
        for node, lang, article_type, parent, parent_id in get_parent_context(
            self.xml_tree
        ):
            for media_node in node.xpath(".//media"):
                media_data = Media(media_node).data
                yield put_parent_context(
                    media_data, lang, article_type, parent, parent_id
                )
