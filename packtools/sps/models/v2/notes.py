from packtools.sps.utils.xml_utils import process_subtags, put_parent_context


class Fn:
    def __init__(self, fn_node):
        self.fn_node = fn_node
        self.fn_id = self.fn_node.get("id")
        self.fn_type = self.fn_node.get("fn-type")
        self.fn_label = self.fn_node.findtext("label")
        self.fn_text = process_subtags(self.fn_node)

    def data(self):
        return {
            "fn_id": self.fn_id,
            "fn_type": self.fn_type,
            "fn_label": self.fn_label,
            "fn_text": self.fn_text
        }


class Fns:
    def __init__(self, node):
        self.node = node

    def fns(self):
        for fn_node in self.node.xpath(".//fn"):
            fn = Fn(fn_node)
            yield fn.data()


class FnGroup:
    def __init__(self, node):
        self.node = node

    def fn_group(self):
        for data in Fns(self.node).fns():
            data["fn_parent"] = "fn-group"
            yield data


class FnGroups:
    def __init__(self, node):
        self.node = node
        self.parent = node.tag
        self.parent_id = node.get("id")
        self.parent_lang = node.get("{http://www.w3.org/XML/1998/namespace}lang")
        self.parent_article_type = self.node.get("article-type")

    def fn_groups(self):
        for fn_group in self.node.xpath(".//fn-group"):
            data = {
                "fns": [fn for fn in FnGroup(fn_group).fn_group()]
            }
            yield put_parent_context(data, self.parent_lang, self.parent_article_type, self.parent, self.parent_id)


class AuthorNote:
    def __init__(self, node):
        self.node = node

    def author_note(self):
        for data in Fns(self.node).fns():
            data["fn_parent"] = "author-notes"
            yield data


class AuthorNotes:
    def __init__(self, node):
        self.node = node
        self.parent = node.tag
        self.parent_id = node.get("id")
        self.parent_lang = node.get("{http://www.w3.org/XML/1998/namespace}lang")
        self.parent_article_type = self.node.get("article-type")

    def author_notes(self):
        for author_note in self.node.xpath(".//author-notes"):
            data = {
                "corresp": process_subtags(author_note.find("corresp")),
                "corresp_label": process_subtags(author_note.find("corresp/label")),
                "fns": [fn for fn in AuthorNote(author_note).author_note()]
            }
            yield put_parent_context(data, self.parent_lang, self.parent_article_type, self.parent, self.parent_id)


class ArticleNotes:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    def article_author_notes(self):
        yield from AuthorNotes(self.xml_tree.find(".")).author_notes()

    def article_fn_groups_notes(self):
        yield from FnGroups(self.xml_tree.find(".")).fn_groups()

    def article_notes(self):
        yield from self.article_fn_groups_notes()
        yield from self.article_author_notes()

    def sub_article_author_notes(self):
        for sub_article in self.xml_tree.xpath(".//sub-article"):
            yield from AuthorNotes(sub_article).author_notes()

    def sub_article_fn_groups_notes(self):
        for sub_article in self.xml_tree.xpath(".//sub-article"):
            yield from FnGroups(sub_article).fn_groups()

    def sub_article_notes(self):
        yield from self.sub_article_fn_groups_notes()
        yield from self.sub_article_author_notes()

    def all_notes(self):
        yield from self.article_notes()
        yield from self.sub_article_notes()
