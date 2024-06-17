class Tablewrap:
    """
    Represents a tablewrap element within an XML document (assuming this is the intended purpose).

    **Parameters:**
        node (xml.etree.ElementTree.Element): The XML element representing the tablewrap.

    **Attributes:**
        node (xml.etree.ElementTree.Element): The internal representation of the parsed XML element.
    """

    def __init__(self, node):
        """
        Initializes a Tablewrap object.

        **Parameters:**
            node (xml.etree.ElementTree.Element): The XML element representing the tablewrap.
        """
        self.node = node

    @property
    def id(self):
        """
        Returns the ID of the tablewrap from the 'id' attribute of the node.

        Returns:
            str: The ID of the tablewrap, or None if the 'id' attribute is not found.
        """
        return self.node.get("id")

    @property
    def data(self):
        """
        Returns a dictionary containing the tablewrap's data.

        Currently, this only includes the 'tablewrap_id'.

        **Note:** This property currently lacks information beyond the ID. You might want to
        consider adding other relevant attributes like 'graphic', 'label', 'caption', or 'alternatives'
        as indicated in the existing TODO comment.

        Returns:
            dict: A dictionary with the key 'tablewrap_id' and the value being the tablewrap's ID.
        """
        # TODO: Add other attributes to the data dictionary (graphic, label, caption, alternatives...)
        return {"tablewrap_id": self.id}


class Parent:
    """
    Represents a parent element (article or sub-article) in the context of tablewraps.

    **Parameters:**
        node (xml.etree.ElementTree.Element): The XML element representing the parent.
        lang (str): The language associated with the parent element (extracted from the 'xml:lang' attribute).
        article_type (str): The type of article (extracted from the 'article-type' attribute).
        parent (str): The name of the parent element (either "article" or "sub-article").
        parent_id (str): The ID of the parent element.

    **Attributes:**
        parent_node (xml.etree.ElementTree.Element): The internal representation of the parsed XML element representing the parent.
        lang (str): The language associated with the parent.
        article_type (str): The type of article associated with the parent.
        parent_name (str): The name of the parent element ("article" or "sub-article").
        parent_id (str): The ID of the parent element.
    """

    def __init__(self, node, lang, article_type, parent, parent_id):
        """
        Initializes a Parent object.

        **Parameters:**
            node (xml.etree.ElementTree.Element): The XML element representing the parent.
            lang (str): The language associated with the parent element (extracted from the 'xml:lang' attribute).
            article_type (str): The type of article (extracted from the 'article-type' attribute).
            parent (str): The name of the parent element (either "article" or "sub-article").
            parent_id (str): The ID of the parent element.
        """
        self.parent_node = node
        self.lang = lang
        self.article_type = article_type
        self.parent_name = parent
        self.parent_id = parent_id

    @property
    def data(self):
        """
        Returns a dictionary containing the parent's information.

        Returns:
            dict: A dictionary with keys 'parent', 'parent_id', 'parent_lang', and 'parent_article_type'.
        """
        return {
            "parent": self.parent_name,
            "parent_id": self.parent_id,
            "parent_lang": self.lang,
            "parent_article_type": self.article_type,
        }

    @property
    def items(self):
        """
        Yields dictionaries containing combined data for tablewraps within the parent's context.

        Iterates through child nodes that are 'table-wrap' elements and creates `Tablewrap` objects.
        For each tablewrap, it yields a dictionary containing combined data:
          - The tablewrap's data (currently just 'tablewrap_id').
          - The parent's information.

        Yields:
            dict: A dictionary containing information about a tablewrap within the parent's context.
        """
        parent_data = self.data
        for node in self.parent_node.xpath(
            ".//table-wrap"
        ):  # Look for 'table-wrap' elements
            tablewrap = Tablewrap(node)  # Assuming Tablewrap class exists
            data = tablewrap.data
            data.update(parent_data)
            yield data


class ArticleTablewraps:
    """
    Represents an article with its associated tablewraps, grouped by language.

    **Parameters:**
        xmltree (xml.etree.ElementTree.ElementTree): The parsed XML document representing the article.

    **Attributes:**
        xmltree (xml.etree.ElementTree.ElementTree): The internal representation of the parsed XML document.
    """

    def __init__(self, xmltree):
        """
        Initializes an ArticleTablewraps object.

        **Parameters:**
            xmltree (xml.etree.ElementTree.ElementTree): The parsed XML document representing the article.
        """
        self.xmltree = xmltree

    @property
    def items_by_lang(self):
        """
        Returns a dictionary containing information about tablewraps grouped by language.

        Iterates through parent contexts (article or sub-article elements) in the XML document
        and creates `Parent` objects. For each parent context, it yields data for associated tablewraps
        using the `parent.items` generator.

        Returns:
            dict: A dictionary where keys are languages and values are generators that yield dictionaries
                  containing information about tablewraps within that language context.
        """
        langs = {}
        for (
            parent_node,
            lang,
            article_type,
            parent_name,
            parent_id,
        ) in self._get_parent_context:
            parent = Parent(parent_node, lang, article_type, parent_name, parent_id)
            langs[lang] = parent.items
        return langs

    @property
    def _get_parent_context(self):
        """
        Yields information about parent contexts (article or sub-article elements) in the XML document.

        1. Extracts information from the main element (e.g., language and article type).
        2. Iterates through article-meta and sub-article elements.
        3. For each element, extracts its type ("article" or "sub-article"), ID, language (if specified),
           and article type (if specified). Defaults to values from the main element if not found locally.
        4. Yields a tuple containing the parent node, language, article type, parent name, and parent ID.

        Yields:
            tuple: A tuple containing information for each parent context:
                   (parent_node, lang, article_type, parent_name, parent_id)
        """
        main = self.xmltree.xpath(".")[0]
        main_lang = main.get("{http://www.w3.org/XML/1998/namespace}lang")
        main_article_type = main.get("article-type")
        for node in self.xmltree.xpath(".//article-meta | .//sub-article"):
            parent = "sub-article" if node.tag == "sub-article" else "article"
            parent_id = node.get("id")
            lang = node.get("{http://www.w3.org/XML/1998/namespace}lang") or main_lang
            article_type = node.get("article-type") or main_article_type
            yield node, lang, article_type, parent, parent_id
