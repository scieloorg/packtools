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
        yield {
            "alternative_parent": self.parent,
            "alternative_childrens": list(self.children)
        }


class Alternatives:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def alternatives(self):
        for alternative in self.xmltree.xpath(".//alternatives"):
            for ancestor in alternative.iterancestors():
                if ancestor.tag == "sub-article":
                    parent = ancestor.tag
                    parent_id = ancestor.get("id")
                    break
            else:
                parent = "article"
                parent_id = None
            alternative_data = Alternative(alternative)
            yield {
                "parent": parent,
                "parent_id": parent_id,
                "alternative_parent": alternative_data.parent,
                "alternative_children": list(alternative_data.children)
            }
