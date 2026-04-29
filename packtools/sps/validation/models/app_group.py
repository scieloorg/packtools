from packtools.sps.models.app_group import App
from packtools.sps.models.article_and_subarticles import Fulltext


class XmlAppGroup:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    @property
    def data(self):
        for node in self.xml_tree.xpath(".|.//sub-article"):
            full_text = Fulltext(node)

            for app_node in node.xpath("./back//app"):
                app_data = App(app_node).data
                yield {**app_data, **full_text.attribs_parent_prefixed}
