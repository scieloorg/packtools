from ..utils import xml_utils
"""
<custom-meta-group>
<custom-meta>
<meta-name>peer-review-recommendation</meta-name>
<meta-value>accept</meta-value>
</custom-meta>
</custom-meta-group>
"""


class CustomMetaGroup:
    def __init__(self, main_node):
        self.main_node = main_node

    @property
    def custom_meta(self):
        for item in self.main_node.xpath('.//custom-meta-group//custom-meta'):
            yield CustomMeta(item)

    @property
    def data(self):
        return [item.data for item in self.custom_meta]


class CustomMeta:
    def __init__(self, custom_meta_node):
        self.custom_meta_node = custom_meta_node

    @property
    def meta_name(self):
        return self.custom_meta_node.findtext('meta-name')

    @property
    def meta_value(self):
        return self.custom_meta_node.findtext('meta-value')

    @property
    def data(self):
        return {
            "meta-name": self.meta_name,
            "meta-value": self.meta_value
        }


class PeerReview(CustomMetaGroup):
    pass
