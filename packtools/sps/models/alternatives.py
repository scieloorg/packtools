class Alternative:
    def __init__(self, node):
        self.node = node

    @property
    def parent(self):
        return self.node.getparent().tag

    @property
    def children(self):
        for children in self.node.getchildren():
            yield children.tag

    @property
    def data(self):
        return {
            "alternative_parent": self.parent,
            "alternative_children": list(self.children)
        }


class Alternatives:
    def __init__(self, node):
        self.node = node

    def alternatives(self):
        for alternative in self.node.xpath(".//alternatives"):
            yield Alternative(alternative)


class ArticleAlternatives:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    def article_alternatives(self):
        article_type = self.xmltree.find(".").get("article-type")
        for article_node in self.xmltree.xpath("./front | ./body | ./back"):
            for alternative in Alternatives(article_node).alternatives():
                alternative_data = alternative.data
                alternative_data["parent"] = "article"
                alternative_data["parent_id"] = None
                alternative_data["parent_article_type"] = article_type
                yield alternative_data

    def sub_article_alternatives(self):
        for sub_article_node in self.xmltree.xpath(".//sub-article"):
            for alternative in Alternatives(sub_article_node).alternatives():
                alternative_data = alternative.data
                alternative_data["parent"] = "sub-article"
                alternative_data["parent_id"] = sub_article_node.get("id")
                alternative_data["parent_article_type"] = sub_article_node.get("article-type")
                yield alternative_data

    def alternatives(self):
        yield from self.article_alternatives()
        yield from self.sub_article_alternatives()
