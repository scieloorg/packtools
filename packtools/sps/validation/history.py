"""
Validations for the <history> element according to SPS 1.10 specification.

This module implements validations for the <history> element, which groups
historical dates for documents (received, accepted, revised, preprint, corrections,
retractions, etc.).

Reference: https://docs.google.com/document/d/1GTv4Inc2LS_AXY-ToHT3HmO66UT0VAHWJNOIqzBNSgA/edit?tab=t.0#heading=h.history
"""

from packtools.sps.validation.utils import build_response


# Allowed values for @date-type according to SPS 1.10
ALLOWED_DATE_TYPES = [
    "received",  # Date manuscript was received
    "accepted",  # Date manuscript was accepted
    "corrected",  # Date of approval of Errata or Addendum
    "expression-of-concern",  # Date of approval of Expression of Concern
    "pub",  # Publication date
    "preprint",  # Date published as preprint
    "resubmitted",  # Date manuscript was resubmitted
    "retracted",  # Date of approval of retraction
    "rev-recd",  # Date revised manuscript was received
    "rev-request",  # Date revisions were requested
    "reviewer-report-received",  # Date reviewer report was received (exclusive for @article-type="reviewer-report")
]

# Date types that require complete date (day, month, year)
COMPLETE_DATE_REQUIRED_TYPES = [
    "received",
    "accepted",
    "corrected",
    "retracted",
    "expression-of-concern",
]

# Article types that are exempt from received/accepted requirements
EXEMPT_ARTICLE_TYPES = [
    "correction",  # errata
    "retraction",
    "addendum",
    "expression-of-concern",
    "reviewer-report",
]


class HistoryValidation:
    """
    Validates the <history> element according to SPS 1.10 rules.
    
    This class implements validation rules for:
    - Uniqueness of <history> element
    - Presence of @date-type attribute
    - Allowed values for @date-type
    - Required dates (received, accepted) with exceptions
    - Complete date requirements for critical date types
    - Minimum year requirement for all dates
    """
    
    def __init__(self, xmltree, params=None):
        """
        Initialize HistoryValidation.
        
        Args:
            xmltree: XML tree containing the article
            params: Optional dictionary of validation parameters
        """
        self.xmltree = xmltree
        self.params = params or {}
        self.params.setdefault("history_uniqueness_error_level", "ERROR")
        self.params.setdefault("date_type_presence_error_level", "CRITICAL")
        self.params.setdefault("date_type_value_error_level", "ERROR")
        self.params.setdefault("required_date_error_level", "CRITICAL")
        self.params.setdefault("complete_date_error_level", "CRITICAL")
        self.params.setdefault("year_presence_error_level", "CRITICAL")
        
        # Get article type to determine if exempt from required dates
        self.article_type = self._get_article_type()
        
    def _get_article_type(self):
        """Get the article type from the XML."""
        article = self.xmltree.find(".")
        if article is not None:
            return article.get("article-type")
        return None
    
    def _get_parent_info(self, node=None):
        """Build parent information for validation responses."""
        article = self.xmltree.find(".")
        return {
            "parent": "article-meta" if node is None else node.tag,
            "parent_id": None,
            "parent_article_type": self.article_type,
            "parent_lang": article.get("{http://www.w3.org/XML/1998/namespace}lang") if article is not None else None,
        }
    
    def validate_history_uniqueness(self):
        """
        Rule 1: Validate that <history> appears at most once.
        
        The <history> element must appear at most once in <article-meta> or <front-stub>.
        
        Yields:
            dict: Validation result
        """
        # Check in article-meta
        article_meta_history = self.xmltree.xpath(".//front/article-meta/history")
        
        # Check in front-stub
        front_stub_history = self.xmltree.xpath(".//front-stub/history")
        
        # Combine all history elements
        all_history = article_meta_history + front_stub_history
        history_count = len(all_history)
        
        is_valid = history_count <= 1
        
        parent = self._get_parent_info()
        
        advice = None
        if not is_valid:
            advice = f"Remove duplicate <history> elements. Found {history_count} occurrences, expected at most 1."
        
        yield build_response(
            title="history uniqueness",
            parent=parent,
            item="history",
            sub_item=None,
            validation_type="uniqueness",
            is_valid=is_valid,
            expected="at most one <history> element",
            obtained=f"{history_count} <history> element(s)",
            advice=advice,
            data={"history_count": history_count},
            error_level=self.params["history_uniqueness_error_level"],
        )
    
    def validate_date_type_presence(self):
        """
        Rule 2: Validate that all <date> elements within <history> have @date-type.
        
        The @date-type attribute is required for all <date> elements within <history>.
        
        Yields:
            dict: Validation result for each <date> element
        """
        history_dates = self.xmltree.xpath(".//history/date")
        
        for date_elem in history_dates:
            date_type = date_elem.get("date-type")
            has_date_type = date_type is not None and date_type.strip() != ""
            
            parent = self._get_parent_info(date_elem)
            
            # Get date parts for context
            day = date_elem.findtext("day")
            month = date_elem.findtext("month")
            year = date_elem.findtext("year")
            date_parts = {"day": day, "month": month, "year": year}
            
            advice = None
            if not has_date_type:
                advice = f"Add @date-type attribute to <date> element. Date parts: {date_parts}"
            
            yield build_response(
                title="date-type presence",
                parent=parent,
                item="date",
                sub_item="@date-type",
                validation_type="exist",
                is_valid=has_date_type,
                expected="@date-type attribute present",
                obtained=date_type if has_date_type else "missing",
                advice=advice,
                data=date_parts,
                error_level=self.params["date_type_presence_error_level"],
            )
    
    def validate_date_type_values(self):
        """
        Rule 3: Validate that @date-type has allowed values.
        
        The @date-type attribute must have one of the allowed values according to SPS 1.10.
        
        Yields:
            dict: Validation result for each <date> element
        """
        history_dates = self.xmltree.xpath(".//history/date")
        
        for date_elem in history_dates:
            date_type = date_elem.get("date-type")
            
            # Skip if date-type is missing (covered by validate_date_type_presence)
            if date_type is None or date_type.strip() == "":
                continue
            
            is_valid = date_type in ALLOWED_DATE_TYPES
            
            parent = self._get_parent_info(date_elem)
            
            # Get date parts for context
            day = date_elem.findtext("day")
            month = date_elem.findtext("month")
            year = date_elem.findtext("year")
            date_parts = {"day": day, "month": month, "year": year, "date-type": date_type}
            
            advice = None
            if not is_valid:
                advice = f"Change @date-type='{date_type}' to one of the allowed values: {', '.join(ALLOWED_DATE_TYPES)}"
            
            yield build_response(
                title="date-type value",
                parent=parent,
                item="date",
                sub_item="@date-type",
                validation_type="value in list",
                is_valid=is_valid,
                expected=ALLOWED_DATE_TYPES,
                obtained=date_type,
                advice=advice,
                data=date_parts,
                error_level=self.params["date_type_value_error_level"],
            )
    
    def validate_required_dates(self):
        """
        Rules 4 & 5: Validate presence of required dates (received, accepted).
        
        The dates received and accepted are required, except for:
        - correction (errata)
        - retraction
        - addendum
        - expression-of-concern
        - reviewer-report
        
        Yields:
            dict: Validation results for required dates
        """
        # Check if article type is exempt
        is_exempt = self.article_type in EXEMPT_ARTICLE_TYPES
        
        # Get all date-types from history
        history_dates = self.xmltree.xpath(".//history/date")
        found_date_types = [d.get("date-type") for d in history_dates if d.get("date-type")]
        
        parent = self._get_parent_info()
        
        # Check for "received" date
        has_received = "received" in found_date_types
        received_required = not is_exempt
        received_valid = has_received or not received_required
        
        advice_received = None
        if not received_valid:
            advice_received = "Add <date date-type=\"received\"> with complete date (day, month, year) to <history>"
        
        yield build_response(
            title="required date: received",
            parent=parent,
            item="history",
            sub_item="date[@date-type='received']",
            validation_type="exist",
            is_valid=received_valid,
            expected="<date date-type=\"received\"> present" if received_required else "not required (exempt article type)",
            obtained="present" if has_received else "missing",
            advice=advice_received,
            data={"article_type": self.article_type, "is_exempt": is_exempt, "found_date_types": found_date_types},
            error_level=self.params["required_date_error_level"] if received_required else "OK",
        )
        
        # Check for "accepted" date
        has_accepted = "accepted" in found_date_types
        accepted_required = not is_exempt
        accepted_valid = has_accepted or not accepted_required
        
        advice_accepted = None
        if not accepted_valid:
            advice_accepted = "Add <date date-type=\"accepted\"> with complete date (day, month, year) to <history>"
        
        yield build_response(
            title="required date: accepted",
            parent=parent,
            item="history",
            sub_item="date[@date-type='accepted']",
            validation_type="exist",
            is_valid=accepted_valid,
            expected="<date date-type=\"accepted\"> present" if accepted_required else "not required (exempt article type)",
            obtained="present" if has_accepted else "missing",
            advice=advice_accepted,
            data={"article_type": self.article_type, "is_exempt": is_exempt, "found_date_types": found_date_types},
            error_level=self.params["required_date_error_level"] if accepted_required else "OK",
        )
    
    def validate_complete_date_for_critical_types(self):
        """
        Rule 6: Validate complete dates for critical date types.
        
        For received, accepted, corrected, retracted, expression-of-concern:
        <day>, <month>, and <year> are required.
        
        Yields:
            dict: Validation result for each critical date
        """
        history_dates = self.xmltree.xpath(".//history/date")
        
        for date_elem in history_dates:
            date_type = date_elem.get("date-type")
            
            # Skip if not a critical type
            if date_type not in COMPLETE_DATE_REQUIRED_TYPES:
                continue
            
            # Check for day, month, year
            day = date_elem.findtext("day")
            month = date_elem.findtext("month")
            year = date_elem.findtext("year")
            
            has_day = day is not None and day.strip() != ""
            has_month = month is not None and month.strip() != ""
            has_year = year is not None and year.strip() != ""
            
            is_complete = has_day and has_month and has_year
            
            parent = self._get_parent_info(date_elem)
            
            date_parts = {"day": day, "month": month, "year": year, "date-type": date_type}
            
            missing_parts = []
            if not has_day:
                missing_parts.append("day")
            if not has_month:
                missing_parts.append("month")
            if not has_year:
                missing_parts.append("year")
            
            advice = None
            if not is_complete:
                advice = f"Add missing elements to <date date-type=\"{date_type}\">: {', '.join(missing_parts)}"
            
            yield build_response(
                title=f"complete date for {date_type}",
                parent=parent,
                item="date",
                sub_item=f"@date-type='{date_type}'",
                validation_type="format",
                is_valid=is_complete,
                expected="complete date with day, month, and year",
                obtained=f"day={day}, month={month}, year={year}",
                advice=advice,
                data=date_parts,
                error_level=self.params["complete_date_error_level"],
            )
    
    def validate_year_presence(self):
        """
        Rule 7: Validate that all dates have at least <year>.
        
        For all date types, at least <year> must be present.
        
        Yields:
            dict: Validation result for each date
        """
        history_dates = self.xmltree.xpath(".//history/date")
        
        for date_elem in history_dates:
            date_type = date_elem.get("date-type")
            year = date_elem.findtext("year")
            
            has_year = year is not None and year.strip() != ""
            
            parent = self._get_parent_info(date_elem)
            
            day = date_elem.findtext("day")
            month = date_elem.findtext("month")
            date_parts = {"day": day, "month": month, "year": year, "date-type": date_type}
            
            advice = None
            if not has_year:
                advice = f"Add <year> element to <date date-type=\"{date_type}\">"
            
            yield build_response(
                title=f"year presence for {date_type}",
                parent=parent,
                item="date",
                sub_item="year",
                validation_type="exist",
                is_valid=has_year,
                expected="<year> element present",
                obtained=year if has_year else "missing",
                advice=advice,
                data=date_parts,
                error_level=self.params["year_presence_error_level"],
            )
    
    def validate(self):
        """
        Perform all history validations.
        
        Yields:
            Generator of validation results for all checks
        """
        yield from self.validate_history_uniqueness()
        yield from self.validate_date_type_presence()
        yield from self.validate_date_type_values()
        yield from self.validate_required_dates()
        yield from self.validate_complete_date_for_critical_types()
        yield from self.validate_year_presence()
