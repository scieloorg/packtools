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
            fn_data["parent"] = "sub-article" if self.node.tag == "sub-article" else "article"
            fn_data["parent_id"] = parent_id
            yield fn_data


class ArticleFootnotes:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def article_footnotes(self):
        main_node = self.xmltree.xpath(".")[0]
        main_lang = main_node.get("{http://www.w3.org/XML/1998/namespace}lang")
        main_article_type = main_node.get("article-type")
        for node in self.xmltree.xpath("./front | ./body | ./back | .//sub-article"):
            node_lang = node.get("{http://www.w3.org/XML/1998/namespace}lang") or main_lang
            node_article_type = node.get("article-type") or main_article_type
            for fn in Footnotes(node).footnotes:
                fn["parent_lang"] = node_lang
                fn["parent_article_type"] = node_article_type
                yield fn
