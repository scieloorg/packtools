from packtools.sps.models.basenotes import BaseNoteGroup, BaseNoteGroups
from packtools.sps.utils.xml_utils import process_subtags


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


class FulltextAuthorNotes(BaseNoteGroups):
    def __init__(self, node):
        super().__init__(node, "author-notes", AuthorNotes)

    @property
    def corresp_data(self):
        xpath = f"front//{self.fn_parent_tag_name} | front-stub//{self.fn_parent_tag_name}"

        for fn_parent_node in self.node.xpath(xpath):
            data = self.NoteGroupClass(fn_parent_node).corresp_data
            data.update(self.attribs_parent_prefixed)
            yield data


class XMLAuthorNotes:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    def article_author_notes(self):
        group = FulltextAuthorNotes(self.xml_tree.find("."))
        return {"corresp_data": list(group.corresp_data), "fns": list(group.items)}

    def sub_article_author_notes(self):
        for sub_article in self.xml_tree.xpath(".//sub-article"):
            group = FulltextAuthorNotes(sub_article)
            yield {"corresp_data": list(group.corresp_data), "fns": list(group.items)}
