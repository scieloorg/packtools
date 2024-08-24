import xml.etree.ElementTree as ET
from packtools.sps.utils.xml_utils import put_parent_context, node_plain_text


class TableWrap:
    """
    Represents a <table-wrap> element within an XML document.
    """

    def __init__(self, element):
        """
        Initializes a TableWrap object.

        Parameters:
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
        Returns the text content of the <caption> element within the table-wrap.

        Returns:
            str: The text content of the <caption> element, or an empty string if the element is not found.
        """
        caption_element = self.element.find(".//caption")
        if caption_element is not None:
            return ET.tostring(caption_element, encoding='unicode', method='text').strip()
        return ""

    @property
    def footnote(self):
        """
        Returns the text content of the <table-wrap-foot> element.

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
        Returns the ID of the first <fn> element within the <table-wrap-foot>.

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
        Returns the label of the first <fn> element within the <table-wrap-foot>.

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
        Returns a list of tags within the <alternatives> element.

        Returns:
            list of str: A list of tag names of the elements within the <alternatives> element,
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
    def __init__(self, node):
        """
        Initializes a TableWrappers object.

        Parameters:
            node (xml.etree.ElementTree.Element): The XML node containing table-wrap elements.
        """
        self.node = node

    def table_wrappers(self):
        """
        Yields TableWrap objects for each <table-wrap> element within the provided node.

        Yields:
            dict: A dictionary containing table-wrap data with context from the parent node.
        """
        parent = self.node.tag
        parent_id = self.node.get("id")

        if parent == "article":
            root = self.node.xpath(".")[0]
            path = "./front//table-wrap | ./body//table-wrap | ./back//table-wrap"
        else:
            root = self.node
            path = ".//table-wrap"

        lang = root.get("{http://www.w3.org/XML/1998/namespace}lang")
        article_type = root.get("article-type")

        for table in root.xpath(path):
            data = TableWrap(table).data
            yield put_parent_context(data, lang, article_type, parent, parent_id)


class ArticleTableWrappers:
    """
    Represents an article with its associated table wrappers, grouped by language.

    Attributes:
        xml_tree (xml.etree.ElementTree.ElementTree): The parsed XML document representing the article.
    """

    def __init__(self, xml_tree):
        """
        Initializes an ArticleTableWrappers object.

        Parameters:
            xml_tree (xml.etree.ElementTree.ElementTree): The parsed XML document representing the article.
        """
        self.xml_tree = xml_tree

    @property
    def get_all_table_wrappers(self):
        """
        Yields dictionaries containing information about table wrappers grouped by language.

        Iterates through parent contexts (article or sub-article elements) in the XML document
        and generates data for associated table wrappers using the `TableWrappers` class.

        Yields:
            dict: A dictionary containing information about table wrappers within the given language context,
                  including language, article type, parent, parent ID, and table wrapper data.
        """
        yield from self.get_article_table_wrappers
        yield from self.get_sub_article_translation_table_wrappers
        yield from self.get_sub_article_non_translation_table_wrappers

    @property
    def get_article_table_wrappers(self):
        """
        Yields data for table wrappers associated directly with the main article.

        Yields:
            dict: A dictionary containing table wrapper data where the parent context is the main article.
        """
        yield from TableWrappers(self.xml_tree).table_wrappers()

    @property
    def get_sub_article_translation_table_wrappers(self):
        """
        Yields data for table wrappers within sub-articles of type 'translation'.

        Yields:
            dict: A dictionary containing table wrapper data where the parent context is a sub-article of type 'translation'.
        """
        for node in self.xml_tree.xpath(".//sub-article[@article-type='translation']"):
            yield from TableWrappers(node).table_wrappers()

    @property
    def get_sub_article_non_translation_table_wrappers(self):
        """
        Yields data for table wrappers within sub-articles that are not of type 'translation'.

        Yields:
            dict: A dictionary containing table wrapper data where the parent context is a sub-article that is not of type 'translation'.
        """
        for node in self.xml_tree.xpath(".//sub-article[@article-type!='translation']"):
            yield from TableWrappers(node).table_wrappers()
