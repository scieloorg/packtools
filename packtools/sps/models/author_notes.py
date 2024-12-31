from packtools.sps.models.basenotes import BaseNoteGroup, BaseNoteGroups


class AuthorNote(BaseNoteGroup):

    @property
    def corresp(self):
        return process_subtags(self.fn_parent_node.find("corresp"))

    @property
    def corresp_label(self):
        return process_subtags(self.fn_parent_node.find("corresp/label"))

    @property
    def corresp_title(self):
        return process_subtags(self.fn_parent_node.find("corresp/title"))

    @property
    def corresp_bold(self):
        return process_subtags(self.fn_parent_node.find("corresp/bold"))

    @property
    def data(self):
        data = super().data
        data.update({
            "corresp": self.corresp,
            "corresp_label": self.corresp_label,
            "corresp_title": self.corresp_title,
            "corresp_bold": self.corresp_bold,
         })
        return data


class AuthorNotes(BaseNoteGroups):
    def __init__(self, article_or_sub_article_node):
        super().__init__(article_or_sub_article_node, "author-notes", AuthorNote)


class ArticleAuthorNotes:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    def article_author_notes(self):
        yield from AuthorNotes(self.xml_tree.find(".")).items

    def sub_article_author_notes(self):
        for sub_article in self.xml_tree.xpath(".//sub-article"):
            yield from AuthorNotes(sub_article).items
