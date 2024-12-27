from packtools.sps.models.v2.notes import ArticleNotes
from packtools.sps.validation.utils import format_response
from packtools.sps.validation.exceptions import ValidationFootnotes


class FnValidation:
    """
    Validates individual footnotes based on provided rules and DTD version.

    Attributes:
        fn_data (dict): The data of the footnote to be validated.
        rules (dict): Validation rules with error levels.
        dtd_version (float): The DTD version for specific validations.
    """

    def __init__(self, fn_data, rules, dtd_version):
        """
        Initialize the FnValidation object.

        Args:
            fn_data (dict): Data related to the footnote.
            rules (dict): Rules defining validation constraints and error levels.
            dtd_version (float): The version of the DTD schema.
        """
        self.fn_data = fn_data
        self.rules = rules
        self.dtd_version = dtd_version

    def _generate_response(self, name, expected=None, obtained=None, advice=None):
        """
        Generate a standardized validation response.

        Args:
            name (str): The name of the validation.
            expected (str, optional): The expected value for the validation. Defaults to None.
            obtained (str, optional): The obtained value for the validation. Defaults to None.
            advice (str, optional): Suggestion to fix the issue. Defaults to None.

        Returns:
            dict: A formatted response detailing the validation result.
        """
        key_error_level = f"fn_{name}_error_level"
        return format_response(
            title=name,
            parent=None,
            parent_id=None,
            parent_article_type=None,
            parent_lang=None,
            item=name,
            sub_item=None,
            validation_type="exist",
            is_valid=False,
            expected=expected or name,
            obtained=obtained,
            advice=advice or f"Identify the {name}",
            data=self.fn_data,
            error_level=self.rules[key_error_level],
        )

    def _validate(self, condition, name, expected=None, obtained=None, advice=None):
        """
        Perform a validation and generate a response if the condition fails.

        Args:
            condition (bool): Condition to validate. If False, it generates a response.
            name (str): The name of the validation.
            expected (str, optional): The expected value. Defaults to None.
            obtained (str, optional): The obtained value. Defaults to None.
            advice (str, optional): Suggestion to fix the issue. Defaults to None.

        Returns:
            dict or None: A validation response if the condition fails, otherwise None.
        """
        if condition:
            return self._generate_response(name, expected, obtained, advice)
        return None

    def validate(self):
        """
        Execute all registered validations for the footnote.

        Returns:
            list[dict]: A list of validation responses (excluding None responses).
        """
        validations = [
            self.validate_label,
            self.validate_title,
            self.validate_bold,
            self.validate_type,
            self.validate_dtd_version,
        ]
        return [response for validate in validations if (response := validate())]

    # Individual validation methods
    def validate_label(self):
        """
        Validate the presence of the 'label' in the footnote.
        """
        return self._validate(not self.fn_data.get("fn_label"), name="label")

    def validate_title(self):
        """
        Validate the presence of 'title' when 'label' is expected.
        """
        return self._validate(
            self.fn_data.get("fn_title"),
            name="title",
            expected="label",
            obtained="title",
            advice="Replace title by label",
        )

    def validate_bold(self):
        """
        Validate the presence of 'bold' when 'label' is expected.
        """
        return self._validate(
            self.fn_data.get("fn_bold"),
            name="bold",
            expected="label",
            obtained="bold",
            advice="Replace bold by label",
        )

    def validate_type(self):
        """
        Validate the presence of 'type' in the footnote.
        """
        return self._validate(not self.fn_data.get("fn_type"), name="type")

    def validate_dtd_version(self):
        """
        Validate the 'dtd_version' of the footnote for compatibility with its type.
        """
        fn_type = self.fn_data.get("fn_type")
        if self.dtd_version:
            if self.dtd_version >= 1.3 and fn_type == "conflict":
                return self._validate(
                    True,
                    name="dtd_version",
                    expected='<fn fn-type="coi-statement">',
                    obtained='<fn fn-type="conflict">',
                    advice="Replace conflict with coi-statement",
                )
            elif self.dtd_version < 1.3 and fn_type == "coi-statement":
                return self._validate(
                    True,
                    name="dtd_version",
                    expected='<fn fn-type="conflict">',
                    obtained='<fn fn-type="coi-statement">',
                    advice="Replace coi-statement with conflict",
                )


class FnGroupValidation:
    """
    Validates groups of footnotes in an XML document.

    Attributes:
        xml_tree (ElementTree): The XML tree representing the document.
        rules (dict): Validation rules.
    """

    def __init__(self, xml_tree, rules):
        """
        Initialize the FnGroupValidation object.

        Args:
            xml_tree (ElementTree): The XML tree to validate.
            rules (dict): Validation rules.
        """
        self.xml_tree = xml_tree
        self.rules = rules
        self.article_fn_groups = list(ArticleNotes(xml_tree).article_fn_groups_notes())
        self.sub_article_fn_groups = list(ArticleNotes(xml_tree).sub_article_fn_groups_notes())

    @property
    def _dtd_version(self):
        """
        Retrieve the DTD version from the XML document.

        Returns:
            float: The DTD version.

        Raises:
            ValidationFootnotes: If the DTD version is not valid.
        """
        try:
            dtd = float(self.xml_tree.find(".").get("dtd-version"))
        except (TypeError, ValueError) as e:
            raise ValidationFootnotes(f"dtd-version is not valid: {str(e)}")

        return dtd

    def validate(self):
        """
        Validate all footnote groups in the XML document.

        Yields:
            dict: Validation results for each footnote.
        """
        for fn_group in [*self.article_fn_groups, *self.sub_article_fn_groups]:
            context = self._build_context(fn_group)
            for fn in fn_group.get("fns", []):
                yield from self.validate_fn(fn, context)

    def _build_context(self, fn_group):
        """
        Build the context for a specific footnote group.

        Args:
            fn_group (dict): A group of footnotes.

        Returns:
            dict: Context containing metadata about the parent element.
        """
        return {
            "parent": fn_group.get("parent"),
            "parent_id": fn_group.get("parent_id"),
            "parent_article_type": fn_group.get("parent_article_type"),
            "parent_lang": fn_group.get("parent_lang"),
        }


    def validate_fn(self, fn, context):
        """
        Validate an individual footnote and update the response with context.

        Args:
            fn (dict): The footnote to validate.
            context (dict): Context metadata for the footnote.

        Yields:
            dict: Validation results for the footnote.
        """
        validator = FnValidation(
            fn_data=fn, rules=self.rules, dtd_version=self._dtd_version
        )
        for response in validator.validate():
            response.update(context)
            yield response
