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
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def footnotes(self):
        for fn_node in self.xmltree.xpath(".//fn"):
            # identifica se o fn_node pertence a article ou sub-article
            parent = fn_node.getparent()
            while parent is not None and parent.tag not in ['article', 'sub-article']:
                parent = parent.getparent()

            # obtem os dados de fn_node
            fn = Footnote(fn_node)
            fn_data = fn.data

            fn_data["parent"] = parent.tag if parent is not None else parent
            fn_data["parent_id"] = parent.get("id") if parent is not None else parent
            yield fn_data
