from packtools.sps.models.tablewrap import ArticleTableWrappers
from packtools.sps.validation.utils import format_response


class ArticleTableWrapValidation:
    """
    Validates the <table-wrap> elements in an XML article.

    Args:
        xml_tree: XML object representing the article.
        rules: Dictionary containing validation rules.
    """

    def __init__(self, xml_tree, rules):
        if not hasattr(xml_tree, "get"):
            raise ValueError("xml_tree must be a valid XML object.")
        if not isinstance(rules, dict):
            raise ValueError("rules must be a dictionary containing error levels.")
        try:
            self.elements = list(ArticleTableWrappers(xml_tree).get_all_table_wrappers)
        except Exception as e:
            raise RuntimeError(f"Error processing table-wraps: {e}")
        self.xml_tree = xml_tree
        self.rules = rules

    def validate(self):
        """
        Performs validations on the article.
        Returns a generator with validation results.
        """
        if not self.elements:
            yield format_response(
                title="table-wrap presence",
                parent="article",
                parent_id=None,
                parent_article_type=self.xml_tree.get("article-type"),
                parent_lang=self.xml_tree.get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                item="table-wrap",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="<table-wrap> element",
                obtained=None,
                advice="Add <table-wrap> element to properly illustrate the content.",
                data=None,
                error_level=self.rules["absent_error_level"],
            )
        else:
            for element in self.elements:
                yield from TableWrapValidation(element, self.rules).validate()


class TableWrapValidation:
    """
    Validates the attributes of a <table-wrap> element.

    Args:
        data: Dictionary containing the element's data.
        rules: Dictionary containing validation rules.
    """

    def __init__(self, data, rules):
        if not isinstance(data, dict):
            raise ValueError("data must be a dictionary.")
        self.data = data
        self.rules = rules

    def validate(self):
        """
        Validates the attributes of the <table-wrap>.
        Returns a generator with validation results.
        """
        validations = [
            self.validate_id,
            self.validate_label,
            self.validate_caption,
            self.validate_table,
            self.validate_alternatives,
        ]
        return [response for validate in validations if (response := validate())]

    def validate_id(self):
        """
        Validates the presence of ID in the <table-wrap>.

        Returns:
            The validation result in the expected format.
        """
        if not self.data.get("table_wrap_id"):
            return format_response(
                title="id",
                parent=self.data.get("parent"),
                parent_id=self.data.get("parent_id"),
                parent_article_type=self.data.get("parent_article_type"),
                parent_lang=self.data.get("parent_lang"),
                item="table-wrap",
                sub_item="id",
                validation_type="exist",
                is_valid=False,
                expected="id",
                obtained=None,
                advice="Identify the id",
                data=self.data,
                error_level=self.rules["id_error_level"],
            )

    def validate_label(self):
        """
        Validates the presence of label in the <table-wrap>.

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
                item="table-wrap",
                sub_item="label",
                validation_type="exist",
                is_valid=False,
                expected="label",
                obtained=None,
                advice="Identify the label",
                data=self.data,
                error_level=self.rules["label_error_level"],
            )

    def validate_caption(self):
        """
        Validates the presence of caption in the <table-wrap>.

        Returns:
            The validation result in the expected format.
        """
        if not self.data.get("caption"):
            return format_response(
                title="caption",
                parent=self.data.get("parent"),
                parent_id=self.data.get("parent_id"),
                parent_article_type=self.data.get("parent_article_type"),
                parent_lang=self.data.get("parent_lang"),
                item="table-wrap",
                sub_item="caption",
                validation_type="exist",
                is_valid=False,
                expected="caption",
                obtained=None,
                advice="Identify the caption",
                data=self.data,
                error_level=self.rules["caption_error_level"],
            )

    def validate_table(self):
        """
        Validates the presence of table in the <table-wrap>.

        Returns:
            The validation result in the expected format.
        """
        if not self.data.get("table"):
            return format_response(
                title="table",
                parent=self.data.get("parent"),
                parent_id=self.data.get("parent_id"),
                parent_article_type=self.data.get("parent_article_type"),
                parent_lang=self.data.get("parent_lang"),
                item="table-wrap",
                sub_item="table",
                validation_type="exist",
                is_valid=False,
                expected="table",
                obtained=None,
                advice="Identify the table",
                data=self.data,
                error_level=self.rules["table_error_level"],
            )

    def validate_alternatives(self):
        """
        Validates the presence of alternatives in the <table-wrap>.

        Returns:
            The validation result in the expected format.
        """
        graphic = 1 if self.data.get("graphic") else 0
        table = 1 if self.data.get("table") else 0
        alternatives = len(self.data.get("alternative_elements"))

        # Define validation scenarios
        validation_cases = [
            {
                "condition": graphic + table == 2 and alternatives == 0,
                "expected": "alternatives",
                "obtained": None,
                "advice": "Identify the alternatives",
            },
            {
                "condition": graphic + table == 1 and alternatives > 0,
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
                    item="table-wrap",
                    sub_item="alternatives",
                    validation_type="exist",
                    is_valid=False,
                    expected=case["expected"],
                    obtained=case["obtained"],
                    advice=case["advice"],
                    data=self.data,
                    error_level=self.rules["alternatives_error_level"],
                )
