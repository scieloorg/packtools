from packtools.sps.models.front_articlemeta_issue import ArticleMetaIssue
from packtools.sps.validation.exceptions import MissingJournalDataException
from packtools.sps.validation.utils import build_response


def is_valid_value(value, zero_is_allowed):
    """
    Validates if a given value is a valid alphanumeric or numeric value.

    Args:
        value (str): The value to be validated
        zero_is_allowed (bool): Whether zero is considered a valid value

    Returns:
        dict: Contains validation results including:
            - got: The input value
            - expected: What was expected
            - is_valid: Boolean indicating if the value is valid
    """
    if value.isdigit():
        expected = str(int(value))
        if not zero_is_allowed and expected == "0":
            return {
                "got": value,
                "expected": "alphanumeric value, except 0",
                "is_valid": False,
            }
        return {"got": value, "expected": expected, "is_valid": expected == value}
    elif value.isalnum():
        return {"got": value, "expected": value, "is_valid": True}
    return {"got": value, "expected": "alphanumeric value", "is_valid": False}


class IssueValidation:
    """
    Class responsible for validating journal issue metadata in XML format.
    Performs various checks on volume, number, and supplement information.
    """

    def __init__(self, xml_tree, params):
        """
        Initialize with XML tree and validation parameters.

        Args:
            xml_tree: XML tree containing issue metadata
            params: Dictionary of validation parameters
        """
        self.xml_tree = xml_tree
        self.article_issue = ArticleMetaIssue(xml_tree)
        self.params = params

    def validate_volume_format(self, error_level):
        """
        Validates the format of the volume number.
        Checks if the volume number is a valid non-zero alphanumeric value.

        Args:
            error_level: Severity level for validation errors

        Returns:
            dict: Validation response with results
        """
        if self.article_issue.volume:
            result = is_valid_value(self.article_issue.volume, zero_is_allowed=False)
            return build_response(
                title="volume",
                parent={"parent": "article"},
                item="volume",
                sub_item=None,
                validation_type="format",
                is_valid=result["is_valid"],
                expected=result["expected"],
                obtained=result["got"],
                advice="Consulte SPS documentation to complete volume element",
                data=self.article_issue.data,
                error_level=error_level,
            )

    def validate_number_format(self, error_level):
        """
        Validates the format of the issue number.
        Checks if the issue number is a valid non-zero alphanumeric value.

        Args:
            error_level: Severity level for validation errors

        Returns:
            dict: Validation response with results
        """
        if self.article_issue.number:
            result = is_valid_value(self.article_issue.number, zero_is_allowed=False)
            return build_response(
                title="number",
                parent={"parent": "article"},
                item="number",
                sub_item=None,
                validation_type="format",
                is_valid=result["is_valid"],
                expected=result["expected"],
                obtained=result["got"],
                advice="Consulte SPS documentation to complete issue element",
                data=self.article_issue.data,
                error_level=error_level,
            )

    def validate_supplement_format(self, error_level):
        """
        Validates the format of the supplement number.
        Unlike volume and issue, supplement can be zero.

        Args:
            error_level: Severity level for validation errors

        Returns:
            dict: Validation response with results
        """
        if self.article_issue.suppl:
            result = is_valid_value(self.article_issue.suppl, zero_is_allowed=True)
            return build_response(
                title="supplement",
                parent={"parent": "article"},
                item="supplement",
                sub_item=None,
                validation_type="format",
                is_valid=result["is_valid"],
                expected=result["expected"],
                obtained=result["got"],
                advice="Consulte SPS documentation to complete issue or supplement elements",
                data=self.article_issue.data,
                error_level=error_level,
            )

    def validate_issue_format(self, error_level):
        """
        Validates special issue or supplement format.
        Handles different formats like 'spe' (special) and 'sup' (supplement).

        Args:
            error_level: Severity level for validation errors

        Returns:
            dict: Validation response with results if format is invalid
        """
        parsed_issue = self.article_issue.parsed_issue

        got_number = parsed_issue.get("number")
        got_type_value = parsed_issue.get("type_value")
        got_type = parsed_issue.get("type")
        got_valid_format = parsed_issue.get("type_valid_format")

        if got_type:
            # Build expected format based on issue type (special or supplement)
            if "spe" in self.article_issue.issue.lower():
                if got_number:
                    expected = [f"{got_number} spe {got_type_value}"]
                else:
                    expected = [f"spe {got_type_value}"]
            elif "sup" in self.article_issue.issue.lower():
                if got_number:
                    expected = [f"{got_number} suppl {got_type_value}"]
                else:
                    expected = [f"suppl {got_type_value}"]
            else:
                if got_number:
                    expected = [
                        f"{got_number} suppl {got_type_value}",
                        f"{got_number} spe {got_type_value}",
                    ]
                else:
                    expected = [f"suppl {got_type_value}", f"spe {got_type_value}"]

            return build_response(
                title="special or supplement",
                parent={"parent": "article"},
                item="issue",
                sub_item="special or supplement",
                validation_type="format",
                is_valid=got_valid_format,
                expected=expected,
                obtained=parsed_issue,
                advice=(
                    "Consulte SPS documentation to complete issue element"
                    if not got_valid_format
                    else None
                ),
                data={"issue": self.article_issue.issue},
                error_level=error_level,
            )

    def validate_expected_issues(self, expected_issues, error_level):
        """
        Validates if the issue exists in the list of expected issues.

        Args:
            expected_issues: List of valid issues
            error_level: Severity level for validation errors

        Returns:
            dict: Validation response with results
        """
        issue = {
            "volume": self.article_issue.volume,
            "number": self.article_issue.number,
            "supplement": self.article_issue.suppl,
        }
        if not expected_issues:
            return build_response(
                title="registered issue",
                parent={"parent": "article"},
                item="volume, number, supplement",
                sub_item=None,
                validation_type="value in list",
                is_valid=False,
                expected="Journal issue list",
                obtained=issue,
                advice="Provide registered issues to check issue data in XML file",
                data={"issue": issue},
                error_level=error_level,
            )

        return build_response(
            title="registered issue",
            parent={"parent": "article"},
            item="volume, number, supplement",
            sub_item=None,
            validation_type="value in list",
            is_valid=issue in expected_issues,
            expected=expected_issues,
            obtained=issue,
            advice="Consulte SPS documentation to complete volume, issue and supplement elements",
            data={"issue": issue},
            error_level=error_level,
        )

    def validate(self):
        """
        Performs all validation checks for the issue.
        Yields validation results for volume, number, supplement formats
        and checks against expected issues.

        Raises:
            MissingJournalDataException: If journal_data is missing from params
        """
        yield self.validate_volume_format(self.params["volume_format_error_level"])
        yield self.validate_number_format(self.params["number_format_error_level"])
        yield self.validate_supplement_format(
            self.params["supplement_format_error_level"]
        )
        yield self.validate_issue_format(self.params["issue_format_error_level"])

        try:
            journal_data = self.params["journal_data"]
        except KeyError:
            raise MissingJournalDataException(
                "IssueValidation.validate requires journal_data['issues']"
            )
        else:
            expected_issues = journal_data.get("issues")
            yield self.validate_expected_issues(
                expected_issues,
                self.params["expected_issues_error_level"],
            )


class PaginationValidation:
    """
    Class responsible for validating article pagination information.
    Checks for proper page numbering or electronic location ID.
    """

    def __init__(self, xml_tree):
        """
        Initialize with XML tree containing pagination data.

        Args:
            xml_tree: XML tree with article metadata
        """
        self.xml_tree = xml_tree
        self.issue = ArticleMetaIssue(xml_tree)

    def validate(self, error_level):
        """
        Validates pagination format according to SPS rules.
        Article must have either:
        - Electronic location ID (e_location), or
        - Both first page (fpage) and last page (lpage), or
        - Neither if it's an ahead-of-print article

        Args:
            error_level: Severity level for validation errors

        Returns:
            dict: Validation response if validation fails
        """
        e_location = bool(self.issue.elocation_id)
        fpage = bool(self.issue.fpage)
        lpage = bool(self.issue.lpage)
        volume = bool(self.issue.volume)
        number = bool(self.issue.number)

        is_valid = False
        if e_location or (fpage and lpage):
            is_valid = True
        elif not e_location and not fpage and not lpage:
            if volume or number:
                is_valid = False
            else:
                # ahead of print article - no pagination needed
                is_valid = True

        if not is_valid:
            return build_response(
                title="Pagination",
                parent={"parent": "article"},
                item="elocation-id | fpage / lpage",
                sub_item="elocation-id | fpage / lpage",
                validation_type="match",
                is_valid=is_valid,
                expected="elocation-id or fpage + lpage",
                obtained=f"elocation-id: {self.issue.elocation_id}, fpage: {self.issue.fpage}, lpage: {self.issue.lpage}",
                advice="Provide elocation-id or fpage + lpage",
                data=self.issue.data,
                error_level=error_level,
            )
