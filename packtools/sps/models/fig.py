from packtools.sps.utils.xml_utils import put_parent_context, tostring


class Fig:
    def __init__(self, element):
        self.element = element

    def str_main_tag(self):
        return f'<fig fig-type="{self.fig_type}" id="{self.fig_id}">'

    def __str__(self):
        return tostring(self.element, xml_declaration=False)

    def xml(self, pretty_print=True):
        return tostring(node=self.element, doctype=None, pretty_print=pretty_print, xml_declaration=False)

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
    def file_extension(self):
        file_name = self.graphic_href

        if file_name and "." in file_name:
            return file_name.split(".")[-1]
        return None


    @property
    def data(self):
        return {
            "alternative_parent": "fig",
            "id": self.fig_id,
            "type": self.fig_type,
            "label": self.label,
            "graphic": self.graphic_href,
            "caption": self.caption_text,
            "source_attrib": self.source_attrib,
            "alternatives": self.alternative_elements,
            "file_extension": self.file_extension
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
        self.parent = self.node.tag
        self.parent_id = self.node.get("id")
        self.lang = self.node.get("{http://www.w3.org/XML/1998/namespace}lang")
        self.article_type = self.node.get("article-type")

    def figs(self):
        if self.parent == "article":
            path = "./front//fig | ./body//fig | ./back//fig"
        else:
            path = ".//fig"

        for fig in self.node.xpath(path):
            data = Fig(fig).data
            yield put_parent_context(data, self.lang, self.article_type, self.parent, self.parent_id)


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
        yield from Figs(self.xml_tree.find(".")).figs()

    @property
    def get_sub_article_translation_figs(self):
        for node in self.xml_tree.xpath(".//sub-article[@article-type='translation']"):
            yield from Figs(node).figs()

    @property
    def get_sub_article_non_translation_figs(self):
        for node in self.xml_tree.xpath(".//sub-article[@article-type!='translation']"):
            yield from Figs(node).figs()
