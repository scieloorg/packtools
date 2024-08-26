from packtools.sps.utils.xml_utils import put_parent_context, tostring


class Fig:
    def __init__(self, element):
        self.element = element

    def str_main_tag(self):
        return f'<fig fig-type="{self.fig_type}" id="{self.fig_id}">'

    def __str__(self):
        return tostring(self.element)

    def xml(self):
        return tostring(node=self.element, doctype=None, pretty_print=True, xml_declaration=True)

    @property
    def fig_id(self):
        return self.element.get("id")

    @property
    def fig_type(self):
        return self.element.get("fig-type")

    @property
    def label(self):
        return self.element.findtext("label")

    @property
    def graphic_href(self):
        graphic_element = self.element.find(".//graphic")
        if graphic_element is not None:
            return graphic_element.get("{http://www.w3.org/1999/xlink}href")
        return None

    @property
    def caption_text(self):
        caption_element = self.element.find(".//caption")
        if caption_element is not None:
            return caption_element.xpath("string()").strip()
        return ""

    @property
    def source_attrib(self):
        return self.element.findtext("attrib")

    @property
    def alternative_elements(self):
        alternative_elements = self.element.find(".//alternatives")
        if alternative_elements is not None:
            return [child.tag for child in alternative_elements]
        return []

    @property
    def data(self):
        return {
            "alternative_parent": "fig",
            "fig_id": self.fig_id,
            "fig_type": self.fig_type,
            "label": self.label,
            "graphic_href": self.graphic_href,
            "caption_text": self.caption_text,
            "source_attrib": self.source_attrib,
            "alternative_elements": self.alternative_elements,
        }


class Figs:
    def __init__(self, node):
        """
        Initializes the Figs class with an XML node.

        Parameters:
        node : lxml.etree._Element
            The XML node (element) that contains one or more <fig> elements.
            This can be the root of an `xml_tree` or a node representing a `sub-article`.
        """
        self.node = node

    def figs(self):
        parent = self.node.tag
        parent_id = self.node.get("id")

        if parent == "article":
            root = self.node.xpath(".")[0]
            path = "./front//fig | ./body//fig | ./back//fig"
        else:
            root = self.node
            path = ".//fig"

        lang = root.get("{http://www.w3.org/XML/1998/namespace}lang")
        article_type = root.get("article-type")

        for fig in root.xpath(path):
            data = Fig(fig).data
            yield put_parent_context(data, lang, article_type, parent, parent_id)


class ArticleFigs:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    @property
    def get_all_figs(self):
        yield from self.get_article_figs
        yield from self.get_sub_article_translation_figs
        yield from self.get_sub_article_non_translation_figs

    @property
    def get_article_figs(self):
        yield from Figs(self.xml_tree).figs()

    @property
    def get_sub_article_translation_figs(self):
        for node in self.xml_tree.xpath(".//sub-article[@article-type='translation']"):
            yield from Figs(node).figs()

    @property
    def get_sub_article_non_translation_figs(self):
        for node in self.xml_tree.xpath(".//sub-article[@article-type!='translation']"):
            yield from Figs(node).figs()
