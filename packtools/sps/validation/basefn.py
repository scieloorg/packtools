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
        fn_label = self.fn_data.get("fn_label")
        is_valid = bool(fn_label)
        return build_response(
            title="label",
            parent=self.fn_data,
            item="fn",
            sub_item="label",
            validation_type="exist",
            is_valid=is_valid,
            expected="fn/label",
            obtained="fn/label" if is_valid else None,
            advice=f"Mark footnote label with <fn><label>",
            data=self.fn_data,
            error_level=self.rules["fn_label_error_level"],
        )

    def validate_title(self):
        """
        Validate the presence of 'title' when 'label' is expected.
        """
        fn_title = self.fn_data.get("fn_title")
        is_valid = not bool(fn_title)
        return build_response(
            title="unexpected title element",
            parent=self.fn_data,
            item="fn",
            sub_item="unexpected title",
            validation_type="unexpected",
            is_valid=is_valid,
            expected="fn/label" if not is_valid else None,
            obtained="fn/title" if not is_valid else None,
            advice=f"Replace <fn><title> with <fn><label>",
            data=self.fn_data,
            error_level=self.rules["fn_title_error_level"],
        )

    def validate_bold(self):
        """
        Validate the presence of 'bold' when 'label' is expected.
        """
        fn_bold = self.fn_data.get("fn_bold")
        is_valid = not bool(fn_bold)
        return build_response(
            title="unexpected bold element",
            parent=self.fn_data,
            item="fn",
            sub_item="unexpected bold",
            validation_type="unexpected",
            is_valid=is_valid,
            expected="fn/label" if not is_valid else None,
            obtained="fn/bold" if not is_valid else None,
            advice=f"Replace <fn><bold> with <fn><label>",
            data=self.fn_data,
            error_level=self.rules["fn_bold_error_level"],
        )

    def validate_type(self):
        """
        Validate the presence of 'type' in the footnote.
        """
        expected = self.rules["fn_type_expected_values"]
        fn_type = self.fn_data.get("fn_type")
        is_valid = fn_type in expected
        return build_response(
            title="fn-type value",
            parent=self.fn_data,
            item="fn",
            sub_item="@fn-type",
            validation_type="value in list",
            is_valid=is_valid,
            expected=expected,
            obtained=fn_type,
            advice=f'Complete fn-type="" in <fn fn-type=""> with a valid values: {expected}',
            data=self.fn_data,
            error_level=self.rules["fn_type_error_level"],
        )

    def validate_conflict(self):
        """
        Validate the 'conflict of interest' according to DTD version.
        """
        obtained_fn_type = self.fn_data.get("fn_type")

        if obtained_fn_type not in ("conflict", "coi-statement"):
            return

        if self.dtd_version:
            expected_fn_type = "conflict" if self.dtd_version < 1.3 else "coi-statement"
            is_valid = obtained_fn_type == expected_fn_type
            return build_response(
                title="conflict of interest declaration",
                parent=self.fn_data,
                item="fn",
                sub_item="@fn-type",
                validation_type="value",
                is_valid=is_valid,
                expected=expected_fn_type,
                obtained=obtained_fn_type,
                advice='Use <fn fn-type="conflict"> for JATS < 1.3 and <fn fn-type="coi-statement"> for JATS ≥ 1.3.',
                data=self.fn_data,
                error_level=self.rules["conflict_error_level"],
            )
