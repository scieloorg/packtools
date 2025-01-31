from packtools.sps.validation.utils import build_response


class BaseFnValidation:
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

    def validate_label(self):
        """
        Validate the presence of the 'label' in the footnote.
        """
        if not self.fn_data.get("fn_label"):
            return build_response(
                title="label",
                parent=self.fn_data,
                item="fn",
                sub_item="label",
                validation_type="exist",
                is_valid=False,
                expected="fn/label",
                obtained=None,
                advice=f"Check if footnote label is present and identify it with label element",
                data=self.fn_data,
                error_level=self.rules["fn_label_error_level"],
            )

    def validate_title(self):
        """
        Validate the presence of 'title' when 'label' is expected.
        """
        if self.fn_data.get("fn_title"):
            return build_response(
                title="unexpected title element",
                parent=self.fn_data,
                item="fn",
                sub_item="unexpected title",
                validation_type="unexpected",
                is_valid=False,
                expected="fn/label",
                obtained="fn/title",
                advice=f"Replace fn/title by fn/label",
                data=self.fn_data,
                error_level=self.rules["fn_title_error_level"],
            )

    def validate_bold(self):
        """
        Validate the presence of 'bold' when 'label' is expected.
        """
        if self.fn_data.get("fn_bold"):
            return build_response(
                title="unexpected bold element",
                parent=self.fn_data,
                item="fn",
                sub_item="unexpected bold",
                validation_type="unexpected",
                is_valid=False,
                expected="fn/label",
                obtained="fn/bold",
                advice=f"Replace fn/bold by fn/label",
                data=self.fn_data,
                error_level=self.rules["fn_bold_error_level"],
            )

    def validate_type(self):
        """
        Validate the presence of 'type' in the footnote.
        """
        expected = self.rules["fn_type_expected_values"]
        if self.fn_data.get("fn_type") not in expected:
            return build_response(
                title="fn-type value",
                parent=self.fn_data,
                item="fn",
                sub_item="@fn-type",
                validation_type="value in list",
                is_valid=False,
                expected=expected,
                obtained=self.fn_data.get("fn_type"),
                advice=f"Select one of {expected}",
                data=self.fn_data,
                error_level=self.rules["fn_type_error_level"],
            )

    def validate_conflict(self):
        """
        Validate the 'conflict of interest' according to DTD version.
        """
        fn_type = self.fn_data.get("fn_type")

        if fn_type not in ("conflict", "coi-statement"):
            return

        if self.dtd_version:
            if self.dtd_version < 1.3:
                expected_fn_type = "conflict"
            elif self.dtd_version >= 1.3:
                expected_fn_type = "coi-statement"

            if fn_type != expected_fn_type:
                return build_response(
                    title="conflict of interest declaration",
                    parent=self.fn_data,
                    item="fn",
                    sub_item="@fn-type",
                    validation_type="value",
                    is_valid=False,
                    expected=expected_fn_type,
                    obtained=fn_type,
                    advice="For JATS < 1.3, use fn/@fn-type='conflict'. For JATS >= 1.3, use fn/@fn-type='coi-statement'",
                    data=self.fn_data,
                    error_level=self.rules["conflict_error_level"],
                )
