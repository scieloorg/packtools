from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context


class CustomMetaGroup:
    def __init__(self, main_node):
        self.main_node = main_node

    @property
    def data(self):
        for node, lang, article_type, parent, parent_id in get_parent_context(self.main_node):
            for item in node.xpath('.//custom-meta-group//custom-meta'):
                custom_meta = CustomMeta(item).data
                yield put_parent_context(custom_meta, lang, article_type, parent, parent_id)


class CustomMeta:
    def __init__(self, custom_meta_node):
        self.custom_meta_node = custom_meta_node

    @property
    def meta_name(self):
        if name := self.custom_meta_node.findtext('.//meta-name'):
            return name

    @property
    def meta_value(self):
        if value := self.custom_meta_node.findtext('.//meta-value'):
            return value

    @property
    def data(self):
        return {
            "meta_name": self.meta_name,
            "meta_value": self.meta_value
        }


class PeerReview(CustomMetaGroup):
    pass
