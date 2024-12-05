from packtools.sps.models.formula import ArticleFormulas
from packtools.sps.validation.utils import format_response


class ArticleFormulaValidation:
    """
    Validates the presence and attributes of <formula> elements in an XML tree.

    Attributes:
        xml_tree (ElementTree): The XML tree representing the article.
        elements_by_language (dict): A dictionary containing <formula> elements grouped by language.
        rules (dict): Validation rules specifying error levels and expected criteria.
    """
    def __init__(self, xml_tree, rules):
        if not hasattr(xml_tree, "get"):
            raise ValueError("xml_tree must be a valid XML object.")
        if not isinstance(rules, dict):
            raise ValueError("rules must be a dictionary containing error levels.")
        try:
            self.elements_by_language = ArticleFormulas(xml_tree).items_by_lang
        except Exception as e:
            raise RuntimeError(f"Error processing formula: {e}")
        self.xml_tree = xml_tree
        self.rules = rules

    def validate(self):
        """
        Performs validation for <formula> elements in the article.

        Yields:
            dict: Validation results for each <formula> element or the absence of <formula> elements.
        """
        if not self.elements_by_language:
            yield format_response(
                title="formula",
                parent="article",
                parent_id=None,
                parent_article_type=self.xml_tree.get("article-type"),
                parent_lang=self.xml_tree.get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                item="formula",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="formula",
                obtained=None,
                advice="Add <formula> elements to properly represent mathematical expressions in the content.",
                data=None,
                error_level=self.rules["absent_error_level"],
            )
        else:
            for lang, data in self.elements_by_language.items():
                yield from FormulaValidation(data, self.rules).validate()


class FormulaValidation:
    """
    Validates individual <formula> elements and their attributes.

    Attributes:
        data (dict): Data associated with a specific <formula> element or group.
        rules (dict): Validation rules specifying error levels and expected criteria.
    """
    def __init__(self, data, rules):
        if not isinstance(data, dict):
            raise ValueError("data must be a dictionary.")
        self.data = data
        self.rules = rules

    def validate(self):
        """
        Validates <formula> elements according to specified rules.

        Yields:
            dict: Validation results for specific <formula> attributes.
        """
        yield self._validate_id()

    def _validate_id(self):
        """
        Validates the presence of the '@id' attribute in a <formula> element.

        Returns:
            dict: Validation result indicating whether the '@id' attribute is present.
        """
        if not self.data.get("formula_id"):
            return format_response(
                title="@id",
                parent=self.data.get("parent"),
                parent_id=self.data.get("parent_id"),
                parent_article_type=self.data.get("parent_article_type"),
                parent_lang=self.data.get("parent_lang"),
                item="@id",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="@id",
                obtained=None,
                advice="Identify the @id",
                data=self.data,
                error_level=self.rules["id_error_level"],
            )
