from packtools.sps.models.basenotes import BaseNoteGroup, BaseNoteGroups
from packtools.sps.utils.xml_utils import process_subtags, put_parent_context


class AuthorNotes(BaseNoteGroup):

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
    def corresp_data(self):
        return {
            "corresp": self.corresp,
            "corresp_label": self.corresp_label,
            "corresp_title": self.corresp_title,
            "corresp_bold": self.corresp_bold,
        }


class AuthorNotesNodes(BaseNoteGroups):
    def __init__(self, article_or_sub_article_node):
        super().__init__(article_or_sub_article_node, "author-notes", AuthorNotes)

    @property
    def corresp_data(self):
        if self.parent == "article":
            xpath = f".//front//{self.fn_parent_tag_name} | .//body//{self.fn_parent_tag_name} | .//back//{self.fn_parent_tag_name}"
        else:
            xpath = f".//{self.fn_parent_tag_name}"

        for fn_parent_node in self.article_or_sub_article_node.xpath(xpath):
            data = self.NoteGroupClass(fn_parent_node).corresp_data
            yield put_parent_context(
                data,
                self.parent_lang,
                self.parent_article_type,
                self.parent,
                self.parent_id,
            )


class ArticleAuthorNotes:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    def article_author_notes(self):
        group = AuthorNotesNodes(self.xml_tree.find("."))
        return {"corresp_data": list(group.corresp_data), "fns": list(group.items)}

    def sub_article_author_notes(self):
        for sub_article in self.xml_tree.xpath(".//sub-article"):
            group = AuthorNotesNodes(sub_article)
            yield {"corresp_data": list(group.corresp_data), "fns": list(group.items)}
