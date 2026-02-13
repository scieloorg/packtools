from packtools.sps.utils.xml_utils import put_parent_context, tostring


class List:
    def __init__(self, element):
        self.element = element

    def __str__(self):
        return tostring(self.element, xml_declaration=False)

    def xml(self, pretty_print=True):
        return tostring(
            node=self.element,
            doctype=None,
            pretty_print=pretty_print,
            xml_declaration=False,
        )

    @property
    def list_type(self):
        """Returns the value of @list-type attribute"""
        return self.element.get("list-type")

    @property
    def title(self):
        """Returns the text content of <title> element if present"""
        return self.element.findtext("title")

    @property
    def list_items(self):
        """Returns all <list-item> elements"""
        return self.element.findall("list-item")

    @property
    def list_items_count(self):
        """Returns the count of <list-item> elements"""
        return len(self.list_items)

    @property
    def has_label_in_items(self):
        """Checks if any <list-item> contains a <label> element"""
        for item in self.list_items:
            if item.find("label") is not None:
                return True
        return False

    @property
    def empty_list_items(self):
        """Returns list of <list-item> elements that have no content"""
        empty_items = []
        for item in self.list_items:
            # Check if list-item has any child elements or text content
            has_content = len(item) > 0 or (item.text and item.text.strip())
            if not has_content:
                empty_items.append(item)
        return empty_items

    @property
    def data(self):
        """Returns a dictionary with list data for validation"""
        return {
            "list_type": self.list_type,
            "title": self.title,
            "list_items_count": self.list_items_count,
            "has_label_in_items": self.has_label_in_items,
            "empty_list_items_count": len(self.empty_list_items),
        }


class Lists:
    def __init__(self, node):
        self.node = node
        self.parent = self.node.tag
        self.parent_id = self.node.get("id")
        self.lang = self.node.get("{http://www.w3.org/XML/1998/namespace}lang")
        self.article_type = self.node.get("article-type")

    def lists(self):
        if self.parent == "article":
            path = "./front//list | ./body//list | ./back//list"
        else:
            path = ".//list"

        for list_element in self.node.xpath(path):
            data = List(list_element).data
            yield put_parent_context(data, self.lang, self.article_type, self.parent, self.parent_id)


class ArticleLists:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    @property
    def get_all_lists(self):
        """Returns all <list> elements in the document"""
        yield from self.get_article_lists
        yield from self.get_sub_article_translation_lists
        yield from self.get_sub_article_non_translation_lists

    @property
    def get_article_lists(self):
        yield from Lists(self.xml_tree.find(".")).lists()

    @property
    def get_sub_article_translation_lists(self):
        for node in self.xml_tree.xpath(".//sub-article[@article-type='translation']"):
            yield from Lists(node).lists()

    @property
    def get_sub_article_non_translation_lists(self):
        for node in self.xml_tree.xpath(".//sub-article[@article-type!='translation']"):
            yield from Lists(node).lists()
