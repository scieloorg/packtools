import re

from packtools.sps.models.front_articlemeta_issue import ArticleMetaIssue
from packtools.sps.validation.utils import build_response
from packtools.sps import i18n


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


SUPPLEMENT_TERMS = ("suppl", "supl", "supp", "sup", "supplement", "s")
SPECIAL_TERMS = ("spe", "esp", "nesp", "nspe", "especial", "noesp")


def parse_issue_value(issue):
    """
    Parses the content of <issue> tolerating case, punctuation, leading
    zeros, missing spaces and variant terms for supplement and special
    issue.

    Returns:
        dict with "number", "kind" ("suppl", "spe" or None) and "value",
        or None when the content is not recognized
    """
    text = re.sub(r"[^0-9a-z]+", " ", (issue or "").lower())
    text = re.sub(r"(?<=[0-9])(?=[a-z])|(?<=[a-z])(?=[0-9])", " ", text)
    tokens = []
    for token in text.split():
        if token in SUPPLEMENT_TERMS:
            tokens.append("suppl")
        elif token in SPECIAL_TERMS:
            tokens.append("spe")
        elif token.isdigit():
            tokens.append(str(int(token)))
        else:
            return None

    shape = tuple("N" if t.isdigit() else t for t in tokens)
    numbers = [t for t in tokens if t.isdigit()]
    shapes = {
        ("N",): (0, None, None),
        ("N", "suppl", "N"): (0, "suppl", 1),
        ("suppl", "N"): (None, "suppl", 0),
        ("N", "suppl"): (0, "suppl", None),
        ("suppl",): (None, "suppl", None),
        ("spe", "N"): (None, "spe", 0),
        ("N", "spe", "N"): (None, "spe", 1),
        ("N", "spe"): (None, "spe", None),
        ("spe",): (None, "spe", None),
    }
    if shape not in shapes:
        return None
    number_index, kind, value_index = shapes[shape]
    return {
        "number": numbers[number_index] if number_index is not None else None,
        "kind": kind,
        "value": numbers[value_index] if value_index is not None else None,
    }


def format_issue_value(parsed):
    """
    Returns the <issue> content in the SPS 1.10 format
    ("4", "4 suppl 1", "suppl 1" or "spe1"), or None when the supplement or
    special issue number is missing.
    """
    number, kind, value = parsed["number"], parsed["kind"], parsed["value"]
    if kind and not value:
        return None
    if kind == "spe":
        return f"spe{value}"
    if kind == "suppl":
        return f"{number} suppl {value}" if number else f"suppl {value}"
    return number


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

    def validate_volume_format(self):
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
                title="issue volume format",
                parent={"parent": "article"},
                item="volume",
                sub_item=None,
                validation_type="format",
                is_valid=result["is_valid"],
                expected=result["expected"],
                obtained=result["got"],
                advice=f'Replace {result["got"]} in <article-meta><volume> with {result["expected"]}',
                advice_text=i18n._("Replace {obtained} in <article-meta><volume> with {expected}"),
                advice_params={
                    "obtained": result["got"],
                    "expected": result["expected"],
                },
                data=self.article_issue.data,
                error_level=self.params["volume_format_error_level"],
                element_name="article-meta",
                sub_element_name="volume"
            )

    def validate_number_format(self):
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
                title="issue number format",
                parent={"parent": "article"},
                item="number",
                sub_item=None,
                validation_type="format",
                is_valid=result["is_valid"],
                expected=result["expected"],
                obtained=result["got"],
                advice=f'Replace {result["got"]} in <article-meta><issue> with {result["expected"]}',
                advice_text=i18n._("Replace {obtained} in <article-meta><issue> with {expected}"),
                advice_params={
                    "obtained": result["got"],
                    "expected": result["expected"],
                },
                data=self.article_issue.data,
                error_level=self.params["number_format_error_level"],
                element_name="article-meta",
                sub_element_name="issue"
            )

    def validate_supplement_format(self):
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
                title="supplement format",
                parent={"parent": "article"},
                item="supplement",
                sub_item=None,
                validation_type="format",
                is_valid=result["is_valid"],
                expected=result["expected"],
                obtained=result["got"],
                advice=f'Replace {result["got"]} in <article-meta><supplement> with {result["expected"]}',
                advice_text=i18n._("Replace {obtained} in <article-meta><supplement> with {expected}"),
                advice_params={
                    "obtained": result["got"],
                    "expected": result["expected"],
                },
                data=self.article_issue.data,
                error_level=self.params["supplement_format_error_level"],
                element_name="article-meta",
                sub_element_name="supplement"
            )

    def validate_issue_format(self):
        """
        Validates special issue or supplement format.

        SPS 1.10 accepts "4 suppl 1", "suppl 1" and "spe1" for supplement and
        special issue, always with the supplement or special issue number.

        Returns:
            dict: Validation response, or None when <issue> has only the
            issue number (validated by validate_number_format)
        """
        issue = self.article_issue.issue
        if not issue:
            return None

        parsed_issue = self.article_issue.parsed_issue
        got_number = parsed_issue.get("number")
        got_type_value = parsed_issue.get("type_value")
        if not (got_type_value or "").isdigit():
            got_type_value = "N"

        parsed = parse_issue_value(issue)
        if parsed and not parsed["kind"]:
            return None
        if not parsed and not parsed_issue.get("type"):
            return None

        formatted = parsed and format_issue_value(parsed)
        missing_number = bool(parsed) and not formatted
        if formatted:
            expected = [formatted]
        elif missing_number:
            if parsed["kind"] == "spe":
                expected = ["speN"]
            elif parsed["number"]:
                expected = [f'{parsed["number"]} suppl N']
            else:
                expected = ["suppl N"]
        elif "spe" in issue.lower():
            expected = [f"spe{got_type_value}"]
        elif "sup" in issue.lower():
            if got_number:
                expected = [f"{got_number} suppl {got_type_value}"]
            else:
                expected = [f"suppl {got_type_value}"]
        else:
            if got_number:
                expected = [
                    f"{got_number} suppl {got_type_value}",
                    f"spe{got_type_value}",
                ]
            else:
                expected = [f"suppl {got_type_value}", f"spe{got_type_value}"]

        is_valid = bool(formatted) and issue.strip() == formatted

        if is_valid:
            advice = None
            advice_text = None
            advice_params = None
        elif missing_number:
            advice = (
                f"Add the supplement or special issue number to "
                f"<article-meta><issue>{issue}</issue>. Expected format: {expected}"
            )
            advice_text = i18n._(
                "Add the supplement or special issue number to "
                "<article-meta><issue>{issue}</issue>. Expected format: {expected}"
            )
            advice_params = {"issue": issue, "expected": expected}
        else:
            advice = f"Replace {issue} in <article-meta><issue> with one of {expected}"
            advice_text = i18n._("Replace {issue} in <article-meta><issue> with one of {expected}")
            advice_params = {"issue": issue, "expected": expected}

        return build_response(
            title="special or supplement",
            parent={"parent": "article"},
            item="issue",
            sub_item="special or supplement",
            validation_type="format",
            is_valid=is_valid,
            expected=expected,
            obtained=parsed_issue,
            advice=advice,
            advice_text=advice_text,
            advice_params=advice_params,
            data={"issue": issue},
            error_level=self.params["issue_format_error_level"],
        )

    def validate_expected_issues(self):
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
        try:
            expected_issues = self.params["journal_data"]["issues"]
        except (KeyError, TypeError) as e:
            expected_issues = None 

        if not expected_issues:
            return build_response(
                title="registered issue",
                parent={"parent": "article"},
                item="volume, number, supplement",
                sub_item=None,
                validation_type="value in list",
                is_valid=False,
                expected="Journal issue registered in title manager or scielo manager or core",
                obtained=issue,
                advice="Unable to check if issue is registered",
                message_text=i18n._(
                    "Got {issue}, but the registered journal issue could not "
                    "be checked"
                ),
                message_params={"issue": issue},
                advice_text=i18n._("Unable to check if issue is registered"),
                advice_params={},
                data=issue,
                error_level="WARNING",
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
            advice=f'Replace {issue} in <article-meta> with one of {expected_issues}',
            advice_text=i18n._("Replace {issue} in <article-meta> with one of {expected_issues}"),
            advice_params={
                "issue": issue,
                "expected_issues": expected_issues,
            },
            data=issue,
            error_level=self.params["expected_issues_error_level"],
        )

    def validate_issue_element_uniqueness(self):
        """
        Validates that <issue> element appears at most once in <article-meta>.
        According to SPS 1.10, only one <issue> element is allowed.

        Returns:
            dict: Validation response with results
        """
        issue_elements = self.xml_tree.findall(".//front/article-meta/issue")
        count = len(issue_elements)
        is_valid = count <= 1
        
        return build_response(
            title="issue element uniqueness",
            parent={"parent": "article"},
            item="issue",
            sub_item=None,
            validation_type="unique",
            is_valid=is_valid,
            expected="at most one <issue> element in <article-meta>",
            obtained=f"{count} <issue> element(s) found",
            advice=f"Remove duplicate <issue> elements from <article-meta>. Found {count} elements, expected at most 1.",
            advice_text=i18n._("Remove duplicate <issue> elements from <article-meta>. Found {count} elements, expected at most 1."),
            advice_params={"count": count},
            data={"issue_count": count, "issue_values": [elem.text for elem in issue_elements]},
            error_level=self.params.get("issue_element_uniqueness_error_level", "ERROR"),
        )

    def validate_issue_no_punctuation(self):
        """
        Validates that <issue> value does not contain punctuation marks.
        According to SPS 1.10, punctuation like . , - / : ; are not allowed.

        Returns:
            dict: Validation response with results
        """
        if not self.article_issue.issue:
            return None
            
        issue_value = self.article_issue.issue
        # Check for common punctuation marks
        punctuation_marks = ['.', ',', '-', '/', ':', ';', '!', '?', '(', ')', '[', ']', '{', '}', '"', "'"]
        found_punctuation = [p for p in punctuation_marks if p in issue_value]
        is_valid = len(found_punctuation) == 0
        
        return build_response(
            title="issue value without punctuation",
            parent={"parent": "article"},
            item="issue",
            sub_item=None,
            validation_type="format",
            is_valid=is_valid,
            expected="issue value without punctuation marks",
            obtained=issue_value,
            advice=f"Remove punctuation marks {found_punctuation} from <issue> value '{issue_value}'",
            advice_text=i18n._("Remove punctuation marks {found_punctuation} from <issue> value '{issue_value}'"),
            advice_params={
                "found_punctuation": found_punctuation,
                "issue_value": issue_value,
            },
            data={"issue": issue_value, "punctuation_found": found_punctuation},
            error_level=self.params.get("issue_no_punctuation_error_level", "ERROR"),
        )

    def validate_issue_no_uppercase(self):
        """
        Validates that <issue> value does not contain uppercase letters.
        According to SPS 1.10, all letters must be lowercase.

        Returns:
            dict: Validation response with results
        """
        if not self.article_issue.issue:
            return None
            
        issue_value = self.article_issue.issue
        has_uppercase = any(c.isupper() for c in issue_value)
        is_valid = not has_uppercase
        
        return build_response(
            title="issue value without uppercase",
            parent={"parent": "article"},
            item="issue",
            sub_item=None,
            validation_type="format",
            is_valid=is_valid,
            expected="issue value in lowercase only",
            obtained=issue_value,
            advice=f"Convert uppercase letters to lowercase in <issue> value '{issue_value}'. Expected: '{issue_value.lower()}'",
            advice_text=i18n._("Convert uppercase letters to lowercase in <issue> value '{issue_value}'. Expected: '{expected}'"),
            advice_params={
                "issue_value": issue_value,
                "expected": issue_value.lower(),
            },
            data={"issue": issue_value, "expected": issue_value.lower()},
            error_level=self.params.get("issue_no_uppercase_error_level", "ERROR"),
        )

    def validate_issue_supplement_nomenclature(self):
        """
        Validates that supplement uses correct nomenclature 'suppl'.
        According to SPS 1.10, must use 'suppl' not 'supl', 'supplement', 'sup'.

        Returns:
            dict: Validation response with results
        """
        if not self.article_issue.issue:
            return None
            
        issue_value = self.article_issue.issue
        issue_lower = issue_value.lower()
        
        # Check if issue contains supplement-related terms
        if "sup" not in issue_lower:
            return None
            
        # Check for invalid supplement nomenclatures using regex
        invalid_patterns = []
        
        # Check for specific invalid patterns
        if re.search(r'\bsupl\b', issue_lower):
            invalid_patterns.append('supl')
        if re.search(r'\bsupplement\b', issue_lower):
            invalid_patterns.append('supplement')
        if re.search(r'\bsup\b', issue_lower):
            invalid_patterns.append('sup')
            
        is_valid = len(invalid_patterns) == 0
        
        return build_response(
            title="issue supplement nomenclature",
            parent={"parent": "article"},
            item="issue",
            sub_item="supplement nomenclature",
            validation_type="format",
            is_valid=is_valid,
            expected="supplement nomenclature as 'suppl'",
            obtained=issue_value,
            advice=f"Use 'suppl' for supplement nomenclature in <issue> value '{issue_value}'. Invalid terms found: {invalid_patterns}",
            advice_text=i18n._("Use 'suppl' for supplement nomenclature in <issue> value '{issue_value}'. Invalid terms found: {invalid_patterns}"),
            advice_params={
                "issue_value": issue_value,
                "invalid_patterns": invalid_patterns,
            },
            data={"issue": issue_value, "invalid_terms": invalid_patterns},
            error_level=self.params.get("issue_supplement_nomenclature_error_level", "ERROR"),
        )

    def validate_issue_special_nomenclature(self):
        """
        Validates that special issues use correct nomenclature 'spe'.
        According to SPS 1.10, must use 'spe' not 'esp', 'nesp', 'nspe', 'especial', 'noesp'.

        Returns:
            dict: Validation response with results
        """
        if not self.article_issue.issue:
            return None
            
        issue_value = self.article_issue.issue
        issue_lower = issue_value.lower()
        
        tokens = issue_lower.split()

        # Match invalid indicators anchored at the start of each whitespace-separated
        # token (longest alternative first) to avoid two problems with plain substring
        # matching: (1) double-matches where a longer indicator also contains a shorter
        # one (e.g. 'nspe1' should report only 'nspe', not also 'esp'); (2) false
        # positives where an unrelated token happens to contain the indicator as an
        # internal substring (e.g. 'resp1' must not match 'esp').
        indicator_pattern = re.compile(
            r'^(especial|noesp|nspe|nesp|esp)([0-9a-z]*)?$'
        )

        found_invalid = []
        for token in tokens:
            match = indicator_pattern.match(token)
            if match:
                found_invalid.append(match.group(1))

        # If no invalid indicators found and 'spe' is not present, not a special issue
        if not found_invalid and 'spe' not in issue_lower:
            return None
            
        is_valid = len(found_invalid) == 0
        
        return build_response(
            title="issue special nomenclature",
            parent={"parent": "article"},
            item="issue",
            sub_item="special issue nomenclature",
            validation_type="format",
            is_valid=is_valid,
            expected="special issue nomenclature as 'spe'",
            obtained=issue_value,
            advice=f"Use 'spe' for special issue nomenclature in <issue> value '{issue_value}'. Invalid terms found: {found_invalid}",
            advice_text=i18n._("Use 'spe' for special issue nomenclature in <issue> value '{issue_value}'. Invalid terms found: {found_invalid}"),
            advice_params={
                "issue_value": issue_value,
                "found_invalid": found_invalid,
            },
            data={"issue": issue_value, "invalid_terms": found_invalid},
            error_level=self.params.get("issue_special_nomenclature_error_level", "ERROR"),
        )

    def validate_no_supplement_element(self):
        """
        Validates that <supplement> element does not exist in <article-meta>.
        According to SPS 1.10, <supplement> is not allowed in <article-meta>.
        Supplements should be identified in <issue> element instead.

        Returns:
            dict: Validation response with results
        """
        supplement_elements = self.xml_tree.findall(".//front/article-meta/supplement")
        count = len(supplement_elements)
        is_valid = count == 0
        
        return build_response(
            title="supplement element not allowed",
            parent={"parent": "article"},
            item="supplement",
            sub_item=None,
            validation_type="unexpected",
            is_valid=is_valid,
            expected="no <supplement> element in <article-meta>",
            obtained=f"{count} <supplement> element(s) found",
            advice="Remove <supplement> element(s) from <article-meta>. Use <issue> element to indicate supplements (e.g., '4 suppl 1').",
            advice_text=i18n._("Remove <supplement> element(s) from <article-meta>. Use <issue> element to indicate supplements (e.g., '4 suppl 1')."),
            advice_params={},
            data={"supplement_count": count, "supplement_values": [elem.text for elem in supplement_elements]},
            error_level=self.params.get("no_supplement_element_error_level", "CRITICAL"),
        )

    def validate_issue_no_leading_zeros(self):
        """
        Validates that numeric parts of <issue> do not have leading zeros.
        According to SPS 1.10, should use '4' not '04'.

        Returns:
            dict: Validation response with results
        """
        if not self.article_issue.issue:
            return None
            
        issue_value = self.article_issue.issue
        parts = issue_value.split()

        # Detect leading zeros in purely numeric tokens ('04') AND in numeric runs
        # embedded inside alphanumeric tokens ('spe01', 'suppl01').
        # Pattern: a digit run starting with 0 preceded by a non-digit or start of string.
        _leading_zero_re = re.compile(r'(?:(?<=\D)|^)(0\d+)')

        issues_found = []
        for part in parts:
            if part.isdigit():
                # Purely numeric token: flag if it has a leading zero and is not '0'
                if len(part) > 1 and part[0] == '0':
                    issues_found.append(part)
            else:
                # Alphanumeric token: flag if it contains an embedded run with leading zero
                if _leading_zero_re.search(part):
                    issues_found.append(part)

        def _normalize(p):
            """Remove leading zeros: '04' -> '4', 'spe01' -> 'spe1', '0' -> '0'."""
            if p.isdigit():
                return str(int(p))
            return _leading_zero_re.sub(lambda m: str(int(m.group(1))), p)

        is_valid = len(issues_found) == 0
        expected_value = ' '.join(_normalize(p) for p in parts)
        
        return build_response(
            title="issue value without leading zeros",
            parent={"parent": "article"},
            item="issue",
            sub_item=None,
            validation_type="format",
            is_valid=is_valid,
            expected="numeric values without leading zeros",
            obtained=issue_value,
            advice=f"Remove leading zeros from numeric parts in <issue> value '{issue_value}'. Expected: '{expected_value}'",
            advice_text=i18n._("Remove leading zeros from numeric parts in <issue> value '{issue_value}'. Expected: '{expected_value}'"),
            advice_params={
                "issue_value": issue_value,
                "expected_value": expected_value,
            },
            data={"issue": issue_value, "parts_with_leading_zeros": issues_found, "expected": expected_value},
            error_level=self.params.get("issue_no_leading_zeros_error_level", "WARNING"),
        )

    def validate(self):
        """
        Performs all validation checks for the issue.
        Yields validation results for volume, number, supplement formats
        and checks against expected issues.

        Raises:
            MissingJournalDataException: If journal_data is missing from params
        """
        yield self.validate_volume_format()
        yield self.validate_number_format()
        yield self.validate_supplement_format()
        yield self.validate_issue_format()
        yield self.validate_expected_issues()
        # New SPS 1.10 validations for <issue> element
        yield self.validate_issue_element_uniqueness()
        yield self.validate_issue_no_punctuation()
        yield self.validate_issue_no_uppercase()
        yield self.validate_issue_supplement_nomenclature()
        yield self.validate_issue_special_nomenclature()
        yield self.validate_no_supplement_element()
        yield self.validate_issue_no_leading_zeros()


class PaginationValidation:
    """
    Class responsible for validating article pagination information.
    Checks for proper page numbering or electronic location ID.
    """

    def __init__(self, xml_tree, params):
        """
        Initialize with XML tree containing pagination data.

        Args:
            xml_tree: XML tree with article metadata
        """
        self.xml_tree = xml_tree
        self.issue = ArticleMetaIssue(xml_tree)
        self.params = params

    def validate(self):
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

        return build_response(
            title="Pagination",
            parent={"parent": "article"},
            item="elocation-id | fpage / lpage",
            sub_item="elocation-id | fpage / lpage",
            validation_type="match",
            is_valid=is_valid,
            expected="elocation id or first and last pages",
            obtained=f"elocation-id: {self.issue.elocation_id}, fpage: {self.issue.fpage}, lpage: {self.issue.lpage}",
            advice="Mark elocation id with <elocation-id> or first page with <fpage> and last page with <lpage>",
            advice_text=i18n._("Mark elocation id with <elocation-id> or first page with <fpage> and last page with <lpage>"),
            advice_params={},
            data=self.issue.data,
            error_level=self.params["pagination_error_level"],
        )
