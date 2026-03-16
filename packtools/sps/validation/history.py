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

XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"


class HistoryValidation:
    """
    Validates the <history> element according to SPS 1.10 rules.

    Each validation method iterates independently over every relevant container
    (<article-meta> for the main article and each <front-stub> for sub-articles),
    so that exemption logic, uniqueness checks, and required-date checks are all
    evaluated in the correct per-document scope.

    Validation rules:
    - Uniqueness of <history> element (per container)
    - Presence of @date-type attribute
    - Allowed values for @date-type
    - Required dates (driven by ``date_list`` in the rules JSON) with exceptions
      per container article-type
    - Complete date requirements for critical date types
    - Minimum year requirement for all dates
    """

    def __init__(self, xmltree, params=None):
        """
        Initialize HistoryValidation.

        Args:
            xmltree: XML tree containing the article
            params: Optional dictionary of validation parameters.

                    When provided by the orchestrator via ``xml_validations.py``,
                    this dict is the content of the ``history_dates_rules`` key
                    from the pipeline configuration JSON, which has the shape::

                        {
                            "error_level": "CRITICAL",
                            "date_list": [
                                {"type": "received",  "required": true},
                                {"type": "accepted",  "required": true},
                                ...
                            ]
                        }

                    ``error_level`` is used as the default severity for every
                    validation rule.  ``date_list`` drives which date types are
                    considered required (replaces the formerly hardcoded pair
                    received/accepted).

                    Individual rule levels can still be overridden with the
                    explicit keys below (all optional):
                    - history_uniqueness_error_level
                    - date_type_presence_error_level
                    - date_type_value_error_level
                    - required_date_error_level
                    - complete_date_error_level
                    - year_presence_error_level
        """
        self.xmltree = xmltree
        self.params = params or {}

        # Use the JSON's single error_level as the default for every rule;
        # fall back to hard-coded sensible defaults when the key is absent.
        default_error_level = self.params.get("error_level", "CRITICAL")
        default_uniqueness_level = self.params.get("error_level", "ERROR")

        self.params.setdefault("history_uniqueness_error_level", default_uniqueness_level)
        self.params.setdefault("date_type_presence_error_level", default_error_level)
        self.params.setdefault("date_type_value_error_level", default_error_level)
        self.params.setdefault("required_date_error_level", default_error_level)
        self.params.setdefault("complete_date_error_level", default_error_level)
        self.params.setdefault("year_presence_error_level", default_error_level)

        # Build the set of required date types from date_list.
        # Falls back to {"received", "accepted"} when no date_list is provided.
        date_list = self.params.get("date_list", [])
        if date_list:
            self.required_date_types = [
                d["type"] for d in date_list if d.get("required", False)
            ]
        else:
            self.required_date_types = ["received", "accepted"]

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _get_contexts(self):
        """
        Yield one context dict per validatable container in the document.

        Each context represents either:
        - the main article's <front/article-meta>, or
        - a <sub-article>'s <front-stub>.

        Yields:
            dict with keys:
                container     - the article-meta or front-stub Element
                article_type  - @article-type of the owning article/sub-article
                lang          - @xml:lang of the owning article/sub-article
                parent        - "article" or "sub-article"
                parent_id     - value of @id on <sub-article>, or None
        """
        root = self.xmltree.find(".")
        if root is not None:
            article_meta = root.find("front/article-meta")
            if article_meta is not None:
                yield {
                    "container": article_meta,
                    "article_type": root.get("article-type"),
                    "lang": root.get(XML_LANG),
                    "parent": "article",
                    "parent_id": None,
                }

        for sub_article in self.xmltree.xpath(".//sub-article"):
            front_stub = sub_article.find("front-stub")
            if front_stub is not None:
                yield {
                    "container": front_stub,
                    "article_type": sub_article.get("article-type"),
                    "lang": sub_article.get(XML_LANG),
                    "parent": "sub-article",
                    "parent_id": sub_article.get("id"),
                }

    def _build_parent_info(self, ctx):
        """
        Build a parent information dict compatible with build_response()
        from a context yielded by _get_contexts().

        The ``parent`` field identifies the container document ("article" or
        "sub-article"), matching the convention used by other validators such
        as ArticleDoiValidation and XMLPeerReviewValidation.
        """
        return {
            "parent": ctx["parent"],
            "parent_id": ctx["parent_id"],
            "parent_article_type": ctx["article_type"],
            "parent_lang": ctx["lang"],
        }

    # ------------------------------------------------------------------
    # Validation rules
    # ------------------------------------------------------------------

    def validate_history_uniqueness(self):
        """
        Rule 1: Validate that <history> appears at most once per container.

        The <history> element must appear at most once inside <article-meta>
        and at most once inside each <front-stub>.  A valid document may have
        one <history> in <article-meta> **and** one in each sub-article's
        <front-stub> without triggering this rule.

        Yields:
            dict: Validation result (one per container)
        """
        for ctx in self._get_contexts():
            container = ctx["container"]
            parent = self._build_parent_info(ctx)

            history_count = len(container.findall("history"))
            is_valid = history_count <= 1

            advice = None
            if not is_valid:
                advice = (
                    f"Remove duplicate <history> elements. "
                    f"Found {history_count} occurrences, expected at most 1."
                )

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

        The @date-type attribute is required for all <date> elements within
        <history>.  Validation is scoped per container.

        Yields:
            dict: Validation result for each <date> element
        """
        for ctx in self._get_contexts():
            container = ctx["container"]
            parent = self._build_parent_info(ctx)

            for date_elem in container.findall("history/date"):
                date_type = date_elem.get("date-type")
                has_date_type = date_type is not None and date_type.strip() != ""

                day = date_elem.findtext("day")
                month = date_elem.findtext("month")
                year = date_elem.findtext("year")
                date_parts = {"day": day, "month": month, "year": year}

                advice = None
                if not has_date_type:
                    advice = (
                        f"Add @date-type attribute to <date> element. "
                        f"Date parts: {date_parts}"
                    )

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

        The @date-type attribute must have one of the allowed values according
        to SPS 1.10.  Dates without @date-type are skipped here (covered by
        Rule 2).  Validation is scoped per container.

        Yields:
            dict: Validation result for each <date> element
        """
        for ctx in self._get_contexts():
            container = ctx["container"]
            parent = self._build_parent_info(ctx)

            for date_elem in container.findall("history/date"):
                date_type = date_elem.get("date-type")

                if date_type is None or date_type.strip() == "":
                    continue

                is_valid = date_type in ALLOWED_DATE_TYPES

                day = date_elem.findtext("day")
                month = date_elem.findtext("month")
                year = date_elem.findtext("year")
                date_parts = {
                    "day": day,
                    "month": month,
                    "year": year,
                    "date-type": date_type,
                }

                advice = None
                if not is_valid:
                    advice = (
                        f"Change @date-type='{date_type}' to one of the "
                        f"allowed values: {', '.join(ALLOWED_DATE_TYPES)}"
                    )

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
        Validate presence of required dates.

        Which date types are required is driven by ``date_list`` in the
        ``history_dates_rules`` JSON configuration (entries with
        ``"required": true``).  When no configuration is provided the
        validator falls back to requiring ``received`` and ``accepted``.

        Exempt article types (EXEMPT_ARTICLE_TYPES) are never required to
        carry any of these dates.  Each container is evaluated independently
        using *its own* @article-type, so a ``reviewer-report`` sub-article
        is correctly exempt even when the parent article is a
        ``research-article``.

        Yields:
            dict: One validation result per (container, required_date_type)
        """
        for ctx in self._get_contexts():
            container = ctx["container"]
            article_type = ctx["article_type"]
            parent = self._build_parent_info(ctx)

            is_exempt = article_type in EXEMPT_ARTICLE_TYPES

            found_date_types = [
                d.get("date-type")
                for d in container.findall("history/date")
                if d.get("date-type")
            ]

            for required_type in self.required_date_types:
                has_date = required_type in found_date_types
                date_required = not is_exempt
                is_valid = has_date or not date_required

                advice = None
                if not is_valid:
                    advice = (
                        f'Add <date date-type="{required_type}"> '
                        "to <history>"
                    )

                yield build_response(
                    title=f"required date: {required_type}",
                    parent=parent,
                    item="history",
                    sub_item=f"date[@date-type='{required_type}']",
                    validation_type="exist",
                    is_valid=is_valid,
                    expected=(
                        f'<date date-type="{required_type}"> present'
                        if date_required
                        else "not required (exempt article type)"
                    ),
                    obtained="present" if has_date else "missing",
                    advice=advice,
                    data={
                        "article_type": article_type,
                        "is_exempt": is_exempt,
                        "found_date_types": found_date_types,
                    },
                    error_level=(
                        self.params["required_date_error_level"]
                        if date_required
                        else "OK"
                    ),
                )

    def validate_complete_date_for_critical_types(self):
        """
        Rule 6: Validate complete dates for critical date types.

        For received, accepted, corrected, retracted, expression-of-concern:
        <day>, <month>, and <year> are required.  Validation is scoped per
        container.

        Yields:
            dict: Validation result for each critical date
        """
        for ctx in self._get_contexts():
            container = ctx["container"]
            parent = self._build_parent_info(ctx)

            for date_elem in container.findall("history/date"):
                date_type = date_elem.get("date-type")

                if date_type not in COMPLETE_DATE_REQUIRED_TYPES:
                    continue

                day = date_elem.findtext("day")
                month = date_elem.findtext("month")
                year = date_elem.findtext("year")

                has_day = day is not None and day.strip() != ""
                has_month = month is not None and month.strip() != ""
                has_year = year is not None and year.strip() != ""

                is_complete = has_day and has_month and has_year

                date_parts = {
                    "day": day,
                    "month": month,
                    "year": year,
                    "date-type": date_type,
                }

                missing_parts = []
                if not has_day:
                    missing_parts.append("day")
                if not has_month:
                    missing_parts.append("month")
                if not has_year:
                    missing_parts.append("year")

                advice = None
                if not is_complete:
                    advice = (
                        f'Add missing elements to <date date-type="{date_type}">: '
                        f"{', '.join(missing_parts)}"
                    )

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

        For all date types, at least <year> must be present.  Validation is
        scoped per container.

        Yields:
            dict: Validation result for each date
        """
        for ctx in self._get_contexts():
            container = ctx["container"]
            parent = self._build_parent_info(ctx)

            for date_elem in container.findall("history/date"):
                date_type = date_elem.get("date-type")
                year = date_elem.findtext("year")

                has_year = year is not None and year.strip() != ""

                day = date_elem.findtext("day")
                month = date_elem.findtext("month")
                date_parts = {
                    "day": day,
                    "month": month,
                    "year": year,
                    "date-type": date_type,
                }

                advice = None
                if not has_year:
                    advice = (
                        f'Add <year> element to <date date-type="{date_type}">'
                    )

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
