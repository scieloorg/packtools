import lxml.etree as ET

from packtools.sps.utils.xml_utils import put_parent_context, node_plain_text, tostring


class TableWrap:
    def __init__(self, element):
        self.element = element

    def str_main_tag(self):
        return f'<table-wrap id="{self.table_wrap_id}">'

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
    def table_wrap_id(self):
        return self.element.get("id")

    @property
    def label(self):
        return self.element.findtext("label")

    @property
    def caption(self):
        caption_element = self.element.find(".//caption")
        if caption_element is not None:
            return ET.tostring(
                caption_element, encoding="unicode", method="text"
            ).strip()
        return ""

    @property
    def table_wrap_foot(self):
        table_wrap_foot_elem = self.element.find(".//table-wrap-foot")
        if table_wrap_foot_elem is None:
            return []

        fns = []
        for fn_elem in table_wrap_foot_elem.findall(".//fn"):
            fns.append(
                {
                    "text": node_plain_text(fn_elem),
                    "id": fn_elem.get("id"),
                    "label": fn_elem.findtext(".//label"),
                }
            )
        return fns

    @property
    def alternative_elements(self):
        alternative_elements = self.element.find(".//alternatives")
        if alternative_elements is not None:
            return [child.tag for child in alternative_elements]
        return []

    @property
    def table(self):
        table = self.element.find(".//table")
        if table is not None:
            return tostring(table, xml_declaration=False)
        return None

    @property
    def graphic(self):
        graphic = self.element.find(".//graphic")
        if graphic is not None:
            return graphic.get("{http://www.w3.org/1999/xlink}href")
        return None

    @property
    def data(self):
        return {
            "alternative_parent": "table-wrap",
            "table_wrap_id": self.table_wrap_id,
            "label": self.label,
            "caption": self.caption,
            "footnotes": self.table_wrap_foot,
            "alternative_elements": self.alternative_elements,
            "table": self.table,
            "graphic": self.graphic,
        }


class TableWrappers:
    def __init__(self, node):
        """
        Initializes the TableWrappers class with an XML node.

        Parameters:
        node : lxml.etree._Element
            The XML node (element) that contains one or more <table-wrap> elements.
            This can be the root of an `xml_tree` or a node representing a `sub-article`.
        """
        self.node = node
        self.parent = self.node.tag
        self.parent_id = self.node.get("id")
        self.lang = self.node.get("{http://www.w3.org/XML/1998/namespace}lang")
        self.article_type = self.node.get("article-type")

    def table_wrappers(self):
        if self.parent == "article":
            path = "./front//table-wrap | ./body//table-wrap | ./back//table-wrap"
        else:
            path = ".//table-wrap"

        for table in self.node.xpath(path):
            data = TableWrap(table).data
            yield put_parent_context(
                data, self.lang, self.article_type, self.parent, self.parent_id
            )


class ArticleTableWrappers:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    @property
    def get_all_table_wrappers(self):
        yield from self.get_article_table_wrappers
        yield from self.get_sub_article_translation_table_wrappers
        yield from self.get_sub_article_non_translation_table_wrappers

    @property
    def get_article_table_wrappers(self):
        yield from TableWrappers(self.xml_tree.find(".")).table_wrappers()

    @property
    def get_sub_article_translation_table_wrappers(self):
        for node in self.xml_tree.xpath(".//sub-article[@article-type='translation']"):
            yield from TableWrappers(node).table_wrappers()

    @property
    def get_sub_article_non_translation_table_wrappers(self):
        for node in self.xml_tree.xpath(".//sub-article[@article-type!='translation']"):
            yield from TableWrappers(node).table_wrappers()
