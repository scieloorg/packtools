class Footnote:
    def __init__(self, node):
        self.node = node

    @property
    def fn_id(self):
        return self.node.get("id")

    @property
    def fn_type(self):
        return self.node.get("fn-type")

    @property
    def fn_parent(self):
        return self.node.getparent().tag

    @property
    def data(self):
        return {
            "fn_id": self.fn_id,
            "fn_type": self.fn_type,
            "fn_parent": self.fn_parent
        }


class Footnotes:
    def __init__(self, node):
        self.node = node

    @property
    def footnotes(self):
        for fn_node in self.node.xpath(".//fn"):
            fn = Footnote(fn_node)
            fn_data = fn.data

            parent_id = self.node.get("id")
            fn_data["parent"] = "sub-article" if parent_id is not None else "article"
            fn_data["parent_id"] = parent_id
            yield fn_data


class ArticleFootnotes:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def article_footnotes(self):
        for node in self.xmltree.xpath("./front | ./body | ./back | .//sub-article"):
            yield from Footnotes(node).footnotes
