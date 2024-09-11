from packtools.sps.utils.xml_utils import process_subtags, put_parent_context


class NoteGroup:
    def __init__(self, node, parent):
        self.node = node
        self.parent = parent

    @property
    def fns(self):
        for fn_node in self.node.xpath(".//fn"):
            fn = Fn(fn_node)
            data = fn.data
            data["fn_parent"] = self.parent
            yield data

    @property
    def data(self):
        return {
            "fns": list(self.fns)
        }


class NoteGroups:
    def __init__(self, node, node_tag):
        self.node = node
        self.node_tag = node_tag
        self.parent = node.tag
        self.parent_id = node.get("id")
        self.parent_lang = node.get("{http://www.w3.org/XML/1998/namespace}lang")
        self.parent_article_type = self.node.get("article-type")

    @property
    def _get_note_class(self):
        if self.node_tag == "fn-group":
            return FnGroup
        elif self.node_tag == "author-notes":
            return AuthorNote
        else:
            raise ValueError(f"Unsupported node tag: {self.node_tag}")

    @property
    def items(self):
        note_class = self._get_note_class
        for group in self.node.xpath(f".//{self.node_tag}"):
            data = note_class(group).data
            yield put_parent_context(data, self.parent_lang, self.parent_article_type, self.parent, self.parent_id)


class Fn:
    def __init__(self, node):
        # footnote node
        self.node = node
        self.id = self.node.get("id")
        self.type = self.node.get("fn-type")
        self.label = self.node.findtext("label")
        self.text = process_subtags(self.node)
        self.has_bold = bool(self.node.findtext("bold"))

    @property
    def data(self):
        return {
            "fn_id": self.id,
            "fn_type": self.type,
            "fn_label": self.label,
            "fn_text": self.text,
            "fn_has_bold": self.has_bold
        }


class FnGroup(NoteGroup):
    def __init__(self, node):
        # footnote group node
        super().__init__(node, "fn-group")

    @property
    def label(self):
        return self.node.findtext("label")

    @property
    def title(self):
        return self.node.findtext("title")

    @property
    def data(self):
        return {
            **super().data,
            "label": self.label,
            "title": self.title
        }


class FnGroups(NoteGroups):
    def __init__(self, node):
        # article or sub-article node
        super().__init__(node, "fn-group")


class AuthorNote(NoteGroup):
    def __init__(self, node):
        # author note node
        super().__init__(node, "author-notes")

    @property
    def corresp(self):
        return process_subtags(self.node.find("corresp"))

    @property
    def corresp_label(self):
        return process_subtags(self.node.find("corresp/label"))

    @property
    def data(self):
        return {
            **super().data,
            "corresp": self.corresp,
            "corresp_label": self.corresp_label
        }


class AuthorNotes(NoteGroups):
    def __init__(self, node):
        # article or sub-article node
        super().__init__(node, "author-notes")


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
