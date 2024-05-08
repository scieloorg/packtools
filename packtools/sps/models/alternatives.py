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
        for alternative in Alternatives(self.article_body).alternatives():
            alternative_data = alternative.data
            alternative_data["parent"] = "article"
            alternative_data["parent_id"] = None
            yield alternative_data

    def sub_article_alternatives(self):
        for sub_article, parent_id in self.sub_article_bodies():
            for alternative in Alternatives(sub_article).alternatives():
                alternative_data = alternative.data
                alternative_data["parent"] = "sub-article"
                alternative_data["parent_id"] = parent_id
                yield alternative_data

    def alternatives(self):
        yield from self.article_alternatives()
        yield from self.sub_article_alternatives()
