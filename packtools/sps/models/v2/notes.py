from packtools.sps.utils.xml_utils import process_subtags, put_parent_context


class BaseNoteGroup:
    def __init__(self, fn_parent_node):
        self.fn_parent_node = fn_parent_node

    @property
    def fns(self):
        for fn_node in self.fn_parent_node.xpath(".//fn"):
            fn = Fn(fn_node)
            data = fn.data
            data["fn_parent"] = self.fn_parent_node.tag
            yield data

    @property
    def data(self):
        return {
            "fns": list(self.fns)
        }


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
        for fn_parent_node in self.article_or_sub_article_node.xpath(f".//{self.fn_parent_tag_name}"):
            data = self.NoteGroupClass(fn_parent_node).data
            yield put_parent_context(data, self.parent_lang, self.parent_article_type, self.parent, self.parent_id)


class Fn:
    def __init__(self, node):
        self.node = node
        self.id = self.node.get("id")
        self.type = self.node.get("fn-type")
        self.label = self.node.findtext("label")
        self.text = process_subtags(self.node)
        self.bold = self.node.findtext("bold")

    @property
    def data(self):
        return {
            "fn_id": self.id,
            "fn_type": self.type,
            "fn_label": self.label,
            "fn_text": self.text,
            "fn_bold": self.bold
        }


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
            **super().data,
            "label": self.label,
            "title": self.title
        }


class FnGroups(BaseNoteGroups):
    def __init__(self, article_or_sub_article_node):
        super().__init__(article_or_sub_article_node, "fn-group", FnGroup)


class AuthorNote(BaseNoteGroup):

    @property
    def corresp(self):
        return process_subtags(self.fn_parent_node.find("corresp"))

    @property
    def corresp_label(self):
        return process_subtags(self.fn_parent_node.find("corresp/label"))

    @property
    def data(self):
        return {
            **super().data,
            "corresp": self.corresp,
            "corresp_label": self.corresp_label
        }


class AuthorNotes(BaseNoteGroups):
    def __init__(self, article_or_sub_article_node):
        super().__init__(article_or_sub_article_node, "author-notes", AuthorNote)


class ArticleNotes:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    def article_author_notes(self):
        yield from AuthorNotes(self.xml_tree.find(".")).items

    def article_fn_groups_notes(self):
        yield from FnGroups(self.xml_tree.find(".")).items

    def article_notes(self):
        yield from self.article_fn_groups_notes()
        yield from self.article_author_notes()

    def sub_article_author_notes(self):
        for sub_article in self.xml_tree.xpath(".//sub-article"):
            yield from AuthorNotes(sub_article).items

    def sub_article_fn_groups_notes(self):
        for sub_article in self.xml_tree.xpath(".//sub-article"):
            yield from FnGroups(sub_article).items

    def sub_article_notes(self):
        yield from self.sub_article_fn_groups_notes()
        yield from self.sub_article_author_notes()

    def all_notes(self):
        yield from self.article_notes()
        yield from self.sub_article_notes()
