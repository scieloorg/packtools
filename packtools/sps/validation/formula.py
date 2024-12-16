from packtools.sps.models.formula import ArticleFormulas
from packtools.sps.validation.utils import format_response


class ArticleDispFormulaValidation:
    """
    Validates the presence and attributes of <disp-formula> elements in an XML tree.

    Attributes:
        xml_tree (ElementTree): The XML tree representing the article.
        elements (list): A list of <disp-formula> elements and their associated data.
        rules (dict): Validation rules specifying error levels and expected criteria.
    """
    def __init__(self, xml_tree, rules):
        if not hasattr(xml_tree, "get"):
            raise ValueError("xml_tree must be a valid XML object.")
        if not isinstance(rules, dict):
            raise ValueError("rules must be a dictionary containing error levels.")
        try:
            self.elements = list(ArticleFormulas(xml_tree).disp_formula_items)
        except Exception as e:
            raise RuntimeError(f"Error processing formula: {e}")
        self.xml_tree = xml_tree
        self.rules = rules

    def validate(self):
        """
        Performs validation for <disp-formula> elements in the article.

        Yields:
            dict: A dictionary containing the validation results for each <disp-formula> element.
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
                yield from DispFormulaValidation(data, self.rules).validate()


class DispFormulaValidation:
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
        Validates <disp-formula> elements according to specified rules.

        Returns:
            list: A list of validation results for specific <disp-formula> attributes.
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
        Validates the presence of the '@id' attribute in a <disp-formula> element.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
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
        Validates the presence of the 'label' attribute in a <disp-formula> element.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
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
        Validates the presence of the 'codification' attribute in a <disp-formula> element.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
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
        Validates the presence of the 'alternatives' attribute in a <disp-formula> element.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
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


class ArticleInlineFormulaValidation:
    """
    Validates the presence and attributes of <inline-formula> elements in an XML tree.

    Attributes:
        xml_tree (ElementTree): The XML tree representing the article.
        rules (dict): Validation rules specifying error levels and expected criteria.
        elements (list): A list of dictionaries containing data of <inline-formula> elements.
    """

    def __init__(self, xml_tree, rules):
        if not hasattr(xml_tree, "get"):
            raise ValueError("xml_tree must be a valid XML object.")
        if not isinstance(rules, dict):
            raise ValueError("rules must be a dictionary containing error levels.")
        try:
            self.elements = list(ArticleFormulas(xml_tree).inline_formula_items)
        except Exception as e:
            raise RuntimeError(f"Error processing formula: {e}")
        self.xml_tree = xml_tree
        self.rules = rules

    def validate(self):
        """
        Performs validation for <inline-formula> elements in the article.

        Yields:
            dict: A dictionary containing the validation results for each <inline-formula> element.
        """

        if not self.elements:
            yield format_response(
                title="inline-formula",
                parent="article",
                parent_id=None,
                parent_article_type=self.xml_tree.get("article-type"),
                parent_lang=self.xml_tree.get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                item="inline-formula",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="inline-formula",
                obtained=None,
                advice="Add <inline-formula> elements to properly represent mathematical expressions in the content.",
                data=None,
                error_level=self.rules["absent_error_level"],
            )
        else:
            for data in self.elements:
                yield from InlineFormulaValidation(data, self.rules).validate()


class InlineFormulaValidation:
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
        Validates <inline-formula> elements according to specified rules.

        Returns:
            list: A list of validation results for specific <inline-formula> attributes.
        """

        validations = [
            self.validate_codification,
            self.validate_alternatives
        ]
        return [response for validate in validations if (response := validate())]

    def validate_codification(self):
        """
        Validates the presence of codification (mml:math or tex-math) in a <inline-formula> element.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
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
        Validates the presence of alternatives in a <inline-formula> element.

        Returns:
            dict or None: A validation result dictionary if the validation fails; otherwise, None.
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
