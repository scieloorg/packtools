from ..utils import xml_utils


class PeerReview:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def meta_names(self):
        for item in self.xmltree.xpath('.//custom-meta-group//custom-meta//meta-name'):
            yield item.text

    @property
    def meta_values(self):
        for item in self.xmltree.xpath('.//custom-meta-group//custom-meta//meta-value'):
            yield item.text
