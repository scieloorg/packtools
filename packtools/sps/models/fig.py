from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context

class Fig:
    """
    Represents a figure element within an XML document.

    Attributes:
        element (xml.etree.ElementTree.Element): The XML element representing the figure.
    """

    def __init__(self, element):
        """
        Initializes a Fig object.

        Parameters:
            element (xml.etree.ElementTree.Element): The XML element representing the figure.
        """
        self.element = element

    @property
    def fig_id(self):
        """
        Returns the ID of the figure from the 'id' attribute of the element.

        Returns:
            str: The ID of the figure, or None if the 'id' attribute is not found.
        """
        return self.element.get("id")

    @property
    def fig_type(self):
        """
        Returns the type of the figure from the 'fig-type' attribute of the element.

        Returns:
            str: The type of the figure, or None if the 'fig-type' attribute is not found.
        """
        return self.element.get("fig-type")

    @property
    def label(self):
        """
        Returns the label of the figure.

        Returns:
            str: The text content of the <label> element, or None if the element is not found.
        """
        return self.element.findtext("label")

    @property
    def graphic_href(self):
        """
        Returns the href of the graphic element within the figure.

        Returns:
            str: The value of the 'xlink:href' attribute of the <graphic> element,
                 or None if the element or attribute is not found.
        """
        graphic_element = self.element.find(".//graphic")
        if graphic_element is not None:
            return graphic_element.get("{http://www.w3.org/1999/xlink}href")
        return None

    @property
    def caption_text(self):
        """
        Returns the text content of the caption element within the figure.

        Returns:
            str: The concatenated text content of the <caption> element,
                 or an empty string if the element is not found.
        """
        caption_element = self.element.find(".//caption")
        if caption_element is not None:
            return caption_element.xpath("string()").strip()
        return ""

    @property
    def source_attrib(self):
        """
        Returns the text content of the attrib element within the figure.

        Returns:
            str: The text content of the <attrib> element, or None if the element is not found.
        """
        return self.element.findtext("attrib")

    @property
    def alternative_elements(self):
        """
        Returns a list of tags within the alternatives element.

        Returns:
            list: A list of tag names of the elements within the <alternatives> element,
                  or an empty list if the element is not found.
        """
        alternative_elements = self.element.find(".//alternatives")
        if alternative_elements is not None:
            return [child.tag for child in alternative_elements]
        return []

    @property
    def data(self):
        """
        Returns a dictionary containing the figure's data.

        Returns:
            dict: A dictionary with keys 'fig_id', 'fig_type', 'label', 'graphic_href',
                  'caption_text', 'source_attrib', and 'alternative_elements',
                  containing the respective data of the figure.
        """
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
    def __init__(self, fig_node):
        self.fig_node = fig_node

    def figs(self):
        for fig in self.fig_node.xpath(".//fig"):
            yield Fig(fig)


class ArticleFigs:
    """
    Represents an article with its associated figures, grouped by language.

    Parameters:
        xml_tree (lxml.etree._ElementTree): The parsed XML document representing the article.
    """

    def __init__(self, xml_tree):
        """
        Initializes an ArticleFigs object.

        Parameters:
            xml_tree (lxml.etree._ElementTree or xml.etree.ElementTree.ElementTree or lxml.etree.Element):
            The parsed XML document representing the article.
        """
        self.xml_tree = xml_tree

    @property
    def article_figs(self):
        """
        Generates information about figures grouped by language within the article.

        Iterates through parent contexts (article or sub-article elements) in the XML document,
        and creates `Parent` objects. For each parent context, it yields data for associated figures
        using the `parent.items` generator.

        Yields:
            dict: A dictionary containing information about figures within the given language context,
                  including language, article type, parent, parent ID, and figure data.
        """
        for node, lang, article_type, parent, parent_id in get_parent_context(
            self.xml_tree
        ):
            for figure in Figs(node).figs():
                data = figure.data
                data["node"] = figure
                yield put_parent_context(data, lang, article_type, parent, parent_id)
