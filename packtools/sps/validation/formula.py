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
            self.elements = list(ArticleFormulas(xml_tree).items)
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
        if not self.elements:
            yield format_response(
                title="disp-formula",
                parent="article",
                parent_id=None,
                parent_article_type=self.xml_tree.get("article-type"),
                parent_lang=self.xml_tree.get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                item="disp-formula",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="disp-formula",
                obtained=None,
                advice="Add <disp-formula> elements to properly represent mathematical expressions in the content.",
                data=None,
                error_level=self.rules["absent_error_level"],
            )
        else:
            for data in self.elements:
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
        validations = [
            self.validate_id,
            self.validate_label,
            self.validate_codification,
            self.validate_alternatives
        ]
        return [response for validate in validations if (response := validate())]

    def validate_id(self):
        """
        Validates the presence of the '@id' attribute in a <formula> element.

        Returns:
            dict: Validation result indicating whether the '@id' attribute is present.
        """
        if not self.data.get("id"):
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

    def validate_label(self):
        """
        Validates the presence of label in the <disp-formula>.

        Returns:
            The validation result in the expected format.
        """
        if not self.data.get("label"):
            return format_response(
                title="label",
                parent=self.data.get("parent"),
                parent_id=self.data.get("parent_id"),
                parent_article_type=self.data.get("parent_article_type"),
                parent_lang=self.data.get("parent_lang"),
                item="label",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="label",
                obtained=None,
                advice="Identify the label",
                data=self.data,
                error_level=self.rules["label_error_level"],
            )

    def validate_codification(self):
        """
        Validates the presence of codification (mml:math or tex-math) in the <disp-formula>.

        Returns:
            The validation result in the expected format.
        """
        mml = self.data.get("mml_math") or []
        tex = self.data.get("tex_math") or []
        if len(mml) + len(tex) == 0:
            return format_response(
                title="mml:math or tex-math",
                parent=self.data.get("parent"),
                parent_id=self.data.get("parent_id"),
                parent_article_type=self.data.get("parent_article_type"),
                parent_lang=self.data.get("parent_lang"),
                item="mml:math or tex-math",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="mml:math or tex-math",
                obtained=None,
                advice="Identify the mml:math or tex-math",
                data=self.data,
                error_level=self.rules["codification_error_level"],
            )

    def validate_alternatives(self):
        """
        Validates the presence of alternatives in the <disp-formula>.

        Returns:
            The validation result in the expected format.
        """

        graphic = self.data.get("graphic")
        alternatives = self.data.get("alternative_elements")

        # Define validation scenarios
        validation_cases = [
            {
                "condition": graphic != [] and alternatives == [],
                "expected": "alternatives",
                "obtained": None,
                "advice": "Identify the alternatives",
            },
            {
                "condition": graphic == [] and alternatives != [],
                "expected": None,
                "obtained": "alternatives",
                "advice": "Remove the alternatives",
            },
        ]

        # Evaluate conditions and return formatted response if any validation fails
        for case in validation_cases:
            if case["condition"]:
                return format_response(
                    title="alternatives",
                    parent=self.data.get("parent"),
                    parent_id=self.data.get("parent_id"),
                    parent_article_type=self.data.get("parent_article_type"),
                    parent_lang=self.data.get("parent_lang"),
                    item="alternatives",
                    sub_item=None,
                    validation_type="exist",
                    is_valid=False,
                    expected=case["expected"],
                    obtained=case["obtained"],
                    advice=case["advice"],
                    data=self.data,
                    error_level=self.rules["alternatives_error_level"],
                )