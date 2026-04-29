from packtools.sps.models.basenotes import Fn
from packtools.sps.models.article_and_subarticles import Fulltext
from packtools.sps.models.fn import FulltextFnGroups


class XMLFns:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    def article_fn_groups_notes(self):
        yield from FulltextFnGroups(self.xml_tree.find(".")).items

    def sub_article_fn_groups_notes(self):
        for sub_article in self.xml_tree.xpath(".//sub-article"):
            yield from FulltextFnGroups(sub_article).items

    @property
    def fn_edited_by(self):
        for item in self.xml_tree.xpath(". | .//sub-article"):
            fulltext = Fulltext(item)
            for node in fulltext.node.xpath("*//fn[@fn-type='edited-by']"):
                data = fulltext.attribs_parent_prefixed
                data.update(Fn(node).data)
                yield data
