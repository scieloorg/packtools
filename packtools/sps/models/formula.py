import lxml.etree as ET

from packtools.sps.utils.xml_utils import get_parent_context, put_parent_context


class Formula:
    """
    Represents a formula element within an XML document.

    **Attributes:**
        element (xml.etree.ElementTree.Element): The XML element representing the formula.

    **Parameters:**
        element (xml.etree.ElementTree.Element): The XML element representing the formula.
    """

    def __init__(self, element):
        """
        Initializes a Formula object.

        **Parameters:**
            element (xml.etree.ElementTree.Element): The XML element representing the formula.
        """
        self.element = element

    @property
    def formula_id(self):
        """
        Returns the ID of the formula from the 'id' attribute of the element.

        Returns:
            str: The ID of the formula, or None if the 'id' attribute is not found.
        """
        return self.element.get("id")

    @property
    def formula_label(self):
        """
        Returns the label of the formula.

        Returns:
            str: The text content of the <label> element, or None if the element is not found.
        """
        return self.element.findtext("label")

    @property
    def alternative_elements(self):
        """
        Returns a list of tags within the alternatives element.

        Returns:
            list: A list of tag names of the elements within the <alternatives> element,
                  or an empty list if the element is not found.
        """
        alternatives_element = self.element.find('.//alternatives')
        if alternatives_element is not None:
            return [child.tag for child in alternatives_element]
        return []

    @property
    def mml_math(self):
        """
        Returns a list of MathML representations of the formula.

        Returns:
            list: A list of MathML content as strings, or an empty list if no MathML elements are found.
        """
        namespace = "{http://www.w3.org/1998/Math/MathML}"
        return [
            ET.tostring(formula, encoding="unicode", method="text").strip()
            for formula in self.element.findall(f".//{namespace}math")
            if formula is not None and ET.tostring(formula, encoding="unicode", method="text").strip()
        ]

    @property
    def tex_math(self):
        """
        Returns a list of TeX math representations of the formula.

        Returns:
            list: A list of TeX math content as strings, or an empty list if no TeX math elements are found.
        """
        return [
            ET.tostring(formula, encoding="unicode", method="text").strip()
            for formula in self.element.findall(".//tex-math")
            if formula is not None and ET.tostring(formula, encoding="unicode", method="text").strip()
        ]

    @property
    def graphic(self):
        """
        Returns a list of graphics linked to the formula.

        Returns:
            list: A list of hrefs (as strings) from graphic elements, or an empty list if no graphics are found.
        """
        namespace = "{http://www.w3.org/1999/xlink}"
        return [
            formula.get(f"{namespace}href", "").strip()
            for formula in self.element.findall(".//graphic")
            if formula is not None and formula.get(f"{namespace}href") is not None
        ]

    @property
    def data(self):
        """
        Returns a dictionary containing the formula's data.

        Returns:
            dict: A dictionary with keys 'formula_id', 'formula_label', 'alternative_parent', and 'alternative_elements',
                  containing the respective data of the formula.
        """
        alternative_parent = self.element.tag  # 'disp-formula' or 'inline-formula'
        return {
            "alternative_parent": alternative_parent,
            "id": self.formula_id,
            "label": self.formula_label,
            "alternative_elements": self.alternative_elements,
            "mml_math": self.mml_math,
            "tex_math": self.tex_math,
            "graphic": self.graphic
        }


class ArticleFormulas:
    """
    Represents an article with its associated formulas, grouped by language.

    **Parameters:**
        xml_tree (xml.etree.ElementTree.ElementTree): The parsed XML document representing the article.

    **Attributes:**
        xml_tree (xml.etree.ElementTree.ElementTree): The internal representation of the parsed XML document.
    """

    def __init__(self, xml_tree):
        """
        Initializes an ArticleFormulas object.

        **Parameters:**
            xml_tree (xml.etree.ElementTree.ElementTree): The parsed XML document representing the article.
        """
        self.xml_tree = xml_tree

    @property
    def items(self):
        """
        Generator that yields formulas with their respective parent context.

        Yields:
            dict: A dictionary with formula data and parent context details.
        """
        for node, lang, article_type, parent, parent_id in get_parent_context(self.xml_tree):
            for item in node.xpath(".//disp-formula | .//inline-formula"):
                formula = Formula(item)
                data = formula.data
                parent_data = put_parent_context(data, lang, article_type, parent, parent_id)
                yield parent_data

    @property
    def items_by_lang(self):
        """
        Returns a dictionary containing information about formulas grouped by language.

        Iterates through parent contexts (article or sub-article elements) in the XML document
        and creates `Parent` objects. For each parent context, it yields data for associated formulas
        using the `parent.items` generator.

        Returns:
            dict: A dictionary where keys are languages and values are dictionaries
                  containing information about formulas within that language context.
        """
        langs = {}
        for item in self.items:
            lang = item.get("parent_lang")
            langs[lang] = item
        return langs
