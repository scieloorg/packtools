import xml.etree.ElementTree as ET

from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context, node_plain_text


class TableWrap:
    """
    Represents a table wrap element within an XML document.

    **Parameters:**
        element (xml.etree.ElementTree.Element): The XML element representing the table wrap.

    **Attributes:**
        element (xml.etree.ElementTree.Element): The internal representation of the parsed XML element.
    """

    def __init__(self, element):
        """
        Initializes a TableWrap object.

        **Parameters:**
            element (xml.etree.ElementTree.Element): The XML element representing the table wrap.
        """
        self.element = element

    @property
    def table_wrap_id(self):
        """
        Returns the ID of the table wrap from the 'id' attribute of the element.

        Returns:
            str: The ID of the table wrap, or None if the 'id' attribute is not found.
        """
        return self.element.get("id")

    @property
    def label(self):
        """
        Returns the label of the table wrap.

        Returns:
            str: The text content of the <label> element, or None if the element is not found.
        """
        return self.element.findtext("label")

    @property
    def caption(self):
        """
        Returns the text content of the caption element within the table-wrap.

        Returns:
            str: The concatenated text content of the <caption> element,
                 or an empty string if the element is not found.
        """
        caption_element = self.element.find(".//caption")
        if caption_element is not None:
            return ET.tostring(caption_element, encoding='unicode', method='text').strip()
        return ""

    @property
    def footnote(self):
        """
        Returns the text content of the table-wrap-foot element.

        Returns:
            str: The concatenated text content of the <table-wrap-foot> element,
                 or an empty string if the element is not found.
        """
        footnote_element = self.element.find('.//table-wrap-foot')
        if footnote_element is not None:
            return node_plain_text(footnote_element)
        return ""

    @property
    def footnote_id(self):
        """
        Returns the ID of the first fn element within the table-wrap-foot.

        Returns:
            str: The ID of the first <fn> element, or None if the element or attribute is not found.
        """
        footnote_element = self.element.find('.//table-wrap-foot')
        if footnote_element is not None:
            fn_element = footnote_element.find('.//fn')
            if fn_element is not None:
                return fn_element.get("id")
        return None

    @property
    def footnote_label(self):
        """
        Returns the label of the first fn element within the table-wrap-foot.

        Returns:
            str: The text content of the <label> element within the first <fn> element,
                 or None if the element is not found.
        """
        footnote_element = self.element.find('.//table-wrap-foot')
        if footnote_element is not None:
            return footnote_element.findtext('.//fn//label')
        return None

    @property
    def alternative_elements(self):
        """
        Returns a list of tags within the alternatives element.

        Returns:
            list: A list of tag names of the elements within the <alternatives> element,
                  or an empty list if the element is not found.
        """
        alternative_elements = self.element.find('.//alternatives')
        if alternative_elements is not None:
            return [child.tag for child in alternative_elements]
        return []

    @property
    def data(self):
        """
        Returns a dictionary containing the table wrap's data.

        Returns:
            dict: A dictionary with keys 'table_wrap_id', 'label', 'caption',
                  'footnote', 'footnote_id', 'footnote_label', and 'alternative_elements',
                  containing the respective data of the table wrap.
        """
        return {
            "alternative_parent": "table-wrap",
            "table_wrap_id": self.table_wrap_id,
            "label": self.label,
            "caption": self.caption,
            "footnote": self.footnote,
            "footnote_id": self.footnote_id,
            "footnote_label": self.footnote_label,
            "alternative_elements": self.alternative_elements
        }


class ArticleTableWraps:
    """
    Represents an article with its associated table wraps, grouped by language.

    **Parameters:**
        xml_tree (xml.etree.ElementTree.ElementTree): The parsed XML document representing the article.

    **Attributes:**
        xml_tree (xml.etree.ElementTree.ElementTree): The internal representation of the parsed XML document.
    """

    def __init__(self, xml_tree):
        """
        Initializes an ArticleTableWraps object.

        **Parameters:**
            xml_tree (xml.etree.ElementTree.ElementTree): The parsed XML document representing the article.
        """
        self.xml_tree = xml_tree

    @property
    def items_by_lang(self):
        """
        Returns a dictionary containing information about table wraps grouped by language.

        Iterates through parent contexts (article or sub-article elements) in the XML document
        and creates `Parent` objects. For each parent context, it yields data for associated table wraps
        using the `parent.items` generator.

        Returns:
            dict: A dictionary where keys are languages and values are generators that yield dictionaries
                  containing information about table wraps within that language context.
        """
        langs = {}
        for node, lang, article_type, parent_context, parent_id in get_parent_context(self.xml_tree):
            for item in node.xpath(".//table-wrap"):
                table_wrap = TableWrap(item)
                data = table_wrap.data
                data["node"] = table_wrap
                langs.setdefault(lang, [])
                langs[lang].append(
                    put_parent_context(data, lang, article_type, parent_context, parent_id)
                )

        if langs:
            return langs
