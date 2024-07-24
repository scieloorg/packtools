from itertools import chain

from packtools.sps.validation.utils import format_response
from packtools.sps.validation.exceptions import ValidationAlternativesException
from packtools.sps.models import fig, formula, tablewrap


class AlternativeValidation:
    """
    Represents the validation of alternative elements within a parent element in an XML document.

    **Attributes:**
        alternative_data (dict): Dictionary containing information about the alternative elements.
        obtained_elements (list): List of tags within the <alternatives> element.
        parent_element (str): The parent tag name containing the <alternatives> element.
        expected_elements (list): List of expected child tags within the <alternatives> element.
    """

    def __init__(self, alternative_data, expected_elements):
        """
        Initializes an AlternativeValidation object.

        **Parameters:**
            alternative_data (dict): Dictionary containing information about the alternative elements.
            expected_elements (list): List of expected child tags within the <alternatives> element.
        """
        self.alternative_data = alternative_data
        self.obtained_elements = alternative_data.get("alternative_elements")
        self.parent_element = alternative_data.get("alternative_parent")
        self.expected_elements = expected_elements

    def validate(self, error_level="CRITICAL"):
        """
        Checks whether the alternatives match the tag that contains them.

        **Parameters:**
            error_level (str): The level of error to be used in the validation response.

        **Returns:**
            generator: A generator that yields dictionaries with validation results.
        """
        is_valid = True

        for tag in self.obtained_elements:
            if tag not in self.expected_elements:
                is_valid = False
                break

        yield format_response(
            title="Alternatives validation",
            parent=self.alternative_data.get("parent"),
            parent_id=self.alternative_data.get("parent_id"),
            parent_article_type=self.alternative_data.get("parent_article_type"),
            parent_lang=self.alternative_data.get("parent_lang"),
            item=self.parent_element,
            sub_item="alternatives",
            validation_type="value in list",
            is_valid=is_valid,
            expected=self.expected_elements,
            obtained=self.obtained_elements,
            advice=f'Add {self.expected_elements} as sub-elements of {self.parent_element}/alternatives',
            data=self.alternative_data,
            error_level=error_level
        )


class AlternativesValidation:
    """
    Represents the validation of alternative elements within figures, formulas, and table-wraps in an XML document.

    **Attributes:**
        xml_tree (xml.etree.ElementTree.ElementTree): The parsed XML document representing the article.
        parent_to_children (dict): Dictionary mapping parent tags to their expected child tags within <alternatives>.
        figures (dict): Dictionary of figures grouped by language.
        formulas (dict): Dictionary of formulas grouped by language.
        table_wraps (dict): Dictionary of table-wraps grouped by language.
    """

    def __init__(self, xml_tree, parent_to_children=None):
        """
        Initializes an AlternativesValidation object.

        **Parameters:**
            xml_tree (xml.etree.ElementTree.ElementTree): The parsed XML document representing the article.
            parent_to_children (dict, optional): Dictionary mapping parent tags to their expected child tags within <alternatives>.
        """
        self.xml_tree = xml_tree
        self.parent_to_children = parent_to_children
        self.figures = fig.ArticleFigs(self.xml_tree).items_by_lang or {}
        self.formulas = formula.ArticleFormulas(self.xml_tree).items_by_lang or {}
        self.table_wraps = tablewrap.ArticleTableWraps(self.xml_tree).items_by_lang or {}

    def validate(self, parent_to_children=None):
        """
        Validates the alternative elements within figures, formulas, and table-wraps against the expected children.

        **Parameters:**
            parent_to_children (dict, optional): Dictionary mapping parent tags to their expected child tags within <alternatives>.

        **Yields:**
            dict: A dictionary with validation results for each alternative element.
        """
        parent_to_children = parent_to_children or self.parent_to_children

        for lang, alternative in chain(self.figures.items(), self.formulas.items(), self.table_wraps.items()):
            parent_element = alternative.get("alternative_parent")
            if not parent_to_children:
                raise ValidationAlternativesException(f"The element '{parent_element}' is not configured to use 'alternatives'."
                                                      " Provide alternatives parent and children")
            expected_elements = parent_to_children.get(parent_element)
            if expected_elements is None:
                raise ValidationAlternativesException(f"The element '{parent_element}' is not configured to use 'alternatives'."
                                                      " Provide alternatives parent and children")
            yield from AlternativeValidation(alternative, expected_elements).validate()
