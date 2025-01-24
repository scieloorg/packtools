from packtools.sps.models.basenotes import BaseNoteGroup, BaseNoteGroups


class FnGroup(BaseNoteGroup):

    @property
    def label(self):
        return self.fn_parent_node.findtext("label")

    @property
    def title(self):
        return self.fn_parent_node.findtext("title")

    @property
    def data(self):
        return {
            "label": self.label,
            "title": self.title,
            "fns": list(self.items),
        }


class FnGroups(BaseNoteGroups):
    def __init__(self, article_or_sub_article_node):
        super().__init__(article_or_sub_article_node, "fn-group", FnGroup)


class ArticleFns:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    def article_fn_groups_notes(self):
        yield from FnGroups(self.xml_tree.find(".")).items

    def sub_article_fn_groups_notes(self):
        for sub_article in self.xml_tree.xpath(".//sub-article"):
            yield from FnGroups(sub_article).items
