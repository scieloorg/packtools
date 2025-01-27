from packtools.sps.utils.xml_utils import process_subtags, put_parent_context


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


class BaseNoteGroups:
    def __init__(self, article_or_sub_article_node, fn_parent_tag_name, NoteGroupClass):
        self.article_or_sub_article_node = article_or_sub_article_node
        self.fn_parent_tag_name = fn_parent_tag_name
        self.parent = article_or_sub_article_node.tag
        self.parent_id = article_or_sub_article_node.get("id")
        self.parent_lang = article_or_sub_article_node.get("{http://www.w3.org/XML/1998/namespace}lang")
        self.parent_article_type = article_or_sub_article_node.get("article-type")
        self.NoteGroupClass = NoteGroupClass

    @property
    def items(self):
        if self.parent == "article":
            xpath = f".//front//{self.fn_parent_tag_name} | .//body//{self.fn_parent_tag_name} | .//back//{self.fn_parent_tag_name}"
        else:
            xpath = f".//{self.fn_parent_tag_name}"

        for fn_parent_node in self.article_or_sub_article_node.xpath(xpath):
            for data in self.NoteGroupClass(fn_parent_node).items:
                yield put_parent_context(
                    data,
                    self.parent_lang,
                    self.parent_article_type,
                    self.parent,
                    self.parent_id,
                )


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
