import xml.etree.ElementTree as ET

from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context, node_plain_text


class TableWrap:
    """
    Represents a table wrap element within an XML document.

    Parameters:
        element (xml.etree.ElementTree.Element): The XML element representing the table wrap.
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
            str: The text content of the <caption> element,
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


class TableWrappers:
    def __init__(self, node, lang, article_type, parent, parent_id):
        self.node = node
        self.lang = lang
        self.article_type = article_type
        self.parent = parent
        self.parent_id = parent_id

    def table_wrappers(self):
        """
        Yields TableWrap objects for each <table-wrap> element within the provided node.

        Yields:
            TableWrap: An instance of the TableWrap class for each table-wrap element found.
        """
        for table in self.node.xpath(".//table-wrap"):
            data = TableWrap(table).data
            data["node"] = table
            yield put_parent_context(data, self.lang, self.article_type, self.parent, self.parent_id)


class ArticleTableWrappers:
    """
    Represents an article with its associated table wrappers, grouped by language.

    Parameters:
        xml_tree (xml.etree.ElementTree.ElementTree): The parsed XML document representing the article.
    """

    def __init__(self, xml_tree):
        """
        Initializes an ArticleTableWraps object.

        **Parameters:**
            xml_tree (xml.etree.ElementTree.ElementTree): The parsed XML document representing the article.
        """
        self.xml_tree = xml_tree

    @property
    def get_all_table_wrappers(self):
        """
        Returns a dictionary containing information about table wrappers grouped by language.

        Iterates through parent contexts (article or sub-article elements) in the XML document
        and creates `Parent` objects. For each parent context, it yields data for associated table wrappers
        using the `parent.items` generator.

        Returns:
            dict: A dictionary where keys are languages and values are generators that yield dictionaries
                  containing information about table wrappers within that language context.
        """
        for node, lang, article_type, parent_context, parent_id in get_parent_context(self.xml_tree):
            for table_wrap in TableWrappers(node, lang, article_type, parent_context, parent_id).table_wrappers():
                yield table_wrap

    @property
    def get_article_table_wrappers(self):
        for table in self.get_all_table_wrappers:
            if table.get("parent") == "article":
                yield table

    @property
    def get_sub_article_translation_table_wrappers(self):
        for table in self.get_all_table_wrappers:
            if table.get("parent") == "sub-article" and table.get("parent_article_type") == "translation":
                yield table

    @property
    def get_sub_article_non_translation_table_wrappers(self):
        for table in self.get_all_table_wrappers:
            if table.get("parent") == "sub-article" and table.get("parent_article_type") != "translation":
                yield table
