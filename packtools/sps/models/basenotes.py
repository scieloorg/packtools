from packtools.sps.models.article_and_subarticles import Fulltext
from packtools.sps.utils.xml_utils import process_subtags


class BaseNoteGroup:
    def __init__(self, fn_parent_node):
        self.fn_parent_node = fn_parent_node

    @property
    def items(self):
        for fn_node in self.fn_parent_node.xpath(".//fn"):
            fn = Fn(fn_node)
            data = fn.data
            data["fn_parent"] = self.fn_parent_node.tag
            yield data


class BaseNoteGroups(Fulltext):
    def __init__(self, node, fn_parent_tag_name, NoteGroupClass):
        super().__init__(node)
        self.node = node
        self.fn_parent_tag_name = fn_parent_tag_name
        self.NoteGroupClass = NoteGroupClass

    @property
    def items(self):
        xpath = f"front-stub//{self.fn_parent_tag_name} | front//{self.fn_parent_tag_name} | body//{self.fn_parent_tag_name} | back//{self.fn_parent_tag_name}"

        for fn_parent_node in self.node.xpath(xpath):
            for data in self.NoteGroupClass(fn_parent_node).items:
                data.update(self.attribs_parent_prefixed)
                yield data


class Fn:
    def __init__(self, node):
        self.node = node
        self.id = self.node.get("id")
        self.type = self.node.get("fn-type")
        self.label = self.node.findtext("label")
        self.text = process_subtags(self.node)
        self.bold = self.node.findtext("bold")
        self.title = self.node.findtext("title")

    @property
    def data(self):
        return {
            "fn_id": self.id,
            "fn_type": self.type,
            "fn_label": self.label,
            "fn_text": self.text,
            "fn_bold": self.bold,
            "fn_title": self.title
        }
