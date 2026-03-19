from datetime import date
from unittest import TestCase
from unittest.mock import Mock, patch

from lxml import etree

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation import dates
from packtools.sps.validation.dates import (
    DateValidation,
    FulltextDatesValidation,
)

PARAMS = {
    "day_format_error_level": "CRITICAL",
    "month_format_error_level": "CRITICAL",
    "year_format_error_level": "CRITICAL",
    "year_value_error_level": "CRITICAL",
    "format_error_level": "CRITICAL",
    "value_error_level": "CRITICAL",
    "limit_error_level": "CRITICAL",
    "unexpected_events_error_level": "CRITICAL",
    "missing_events_error_level": "CRITICAL",
    "history_order_error_level": "CRITICAL",
    "required_events": ["received", "accepted"],
    "pre_pub_ordered_events": ["preprint", "received", "revised", "accepted"],
    "pos_pub_ordered_events": ["pub", "corrected", "retracted"],
    "parent": {"parent": None},
    "required_history_events_for_related_article_type": {
        "correction-forward": "corrected",
        "addendum": "corrected",
        "commentary-article": "commented",
        "correction": "corrected",
        "letter": None,
        "partial-retraction": "retracted",
        "retraction": "retracted",
        "response": None,
        "peer-reviewed-article": None,
        "preprint": "preprint",
        "updated-article": "updated",
        "companion": None,
        "republished-article": "republished",
        "corrected-article": "corrected",
        "expression-of-concern": None,
    },
    "required_history_events_for_article_type": {
        "reviewer-report": "reviewer-report-received",
    },
    "limit_date": None,
}


class TestDateFormatValidation(TestCase):
    """Test cases for date format validation."""

    def setUp(self):
        self.base_params = {
            "parent": {"parent": "article", "parent_id": "1234"},
            "year_format_error_level": "ERROR",
            "month_format_error_level": "ERROR",
            "day_format_error_level": "ERROR",
        }

        self.base_date_data = {
            "type": "pub",
            "year": "2024",
            "month": "01",
            "day": "15",
        }

    def test_year_format_validation(self):
        # Test valid year format
        validator = DateValidation(self.base_date_data, self.base_params)
        result = list(validator.validate_year_format())
        self.assertEqual(result[0]["response"], "OK")
        self.assertEqual(result[0]["got_value"], "2024")
        self.assertEqual(result[0]["expected_value"], "4-digits year")
        self.assertEqual(result[0]["title"], "year format")
        self.assertEqual(result[0]["validation_type"], "format")
        self.assertIsNone(result[0]["advice"])

        # Test invalid year format
        invalid_year = self.base_date_data.copy()
        invalid_year["year"] = "24"
        validator = DateValidation(invalid_year, self.base_params)
        result = list(validator.validate_year_format())
        self.assertEqual(result[0]["response"], "ERROR")
        self.assertEqual(result[0]["got_value"], "24")
        self.assertEqual(result[0]["expected_value"], "4-digits year")

    def test_month_format_validation(self):
        # Test valid month format
        validator = DateValidation(self.base_date_data, self.base_params)
        result = list(validator.validate_month_format())
        self.assertEqual(result[0]["response"], "OK")
        self.assertEqual(result[0]["got_value"], "01")
        self.assertEqual(result[0]["expected_value"], "2-digits month")
        self.assertEqual(result[0]["title"], "month format")
        self.assertEqual(result[0]["validation_type"], "format")
        self.assertIsNone(result[0]["advice"])

        # Test invalid month format
        invalid_month = self.base_date_data.copy()
        invalid_month["month"] = "1"
        validator = DateValidation(invalid_month, self.base_params)
        result = list(validator.validate_month_format())
        self.assertEqual(result[0]["response"], "ERROR")
        self.assertEqual(result[0]["got_value"], "1")
        self.assertEqual(result[0]["expected_value"], "2-digits month")

    def test_day_format_validation(self):
        # Test valid day format
        validator = DateValidation(self.base_date_data, self.base_params)
        result = list(validator.validate_day_format())
        self.assertEqual(result[0]["response"], "OK")
        self.assertEqual(result[0]["got_value"], "15")
        self.assertEqual(result[0]["expected_value"], "2-digits day")
        self.assertEqual(result[0]["title"], "day format")
        self.assertEqual(result[0]["validation_type"], "format")
        self.assertIsNone(result[0]["advice"])

        # Test invalid day format
        invalid_day = self.base_date_data.copy()
        invalid_day["day"] = "5"
        validator = DateValidation(invalid_day, self.base_params)
        result = list(validator.validate_day_format())
        self.assertEqual(result[0]["response"], "ERROR")
        self.assertEqual(result[0]["got_value"], "5")
        self.assertEqual(result[0]["expected_value"], "2-digits day")


class TestDateValidation(TestCase):
    """Test cases for general date validation."""

    def setUp(self):
        self.base_params = {
            "parent": {"parent": "article", "parent_id": "1234"},
            "value_error_level": "ERROR",
            "year_format_error_level": "ERROR",
            "month_format_error_level": "ERROR",
        }

        self.base_date_data = {
            "type": "pub",
            "year": "2024",
            "month": "01",
        }

    def test_valid_date(self):
        validator = DateValidation(self.base_date_data, self.base_params)
        results = list(validator.validate_date())
        responses = [item["response"] for item in results]
        advices = [item["advice"] for item in results]
        self.assertEqual(["OK", "OK", "OK"], responses)
        self.assertEqual([None, None, None], advices)
        self.assertEqual(len(results), 3)  # No validation errors

    def test_invalid_date_components(self):
        # Test invalid month
        invalid_date = self.base_date_data.copy()
        invalid_date["month"] = "13"
        validator = DateValidation(invalid_date, self.base_params)
        results = list(validator.validate_date())
        responses = [item["response"] for item in results]
        advices = [item["advice"] for item in results]
        self.assertEqual(["ERROR"], responses)
        self.assertEqual(
            ['<date date-type="pub"> (None) is invalid: month must be in 1..12'],
            advices,
        )
        self.assertEqual(len(results), 1)

        # Test invalid year
        invalid_date["year"] = "abc"
        validator = DateValidation(invalid_date, self.base_params)
        results = list(validator.validate_date())
        responses = [item["response"] for item in results]
        advices = [item["advice"] for item in results]
        self.assertEqual(["ERROR"], responses)
        self.assertEqual(
            [
                "<date date-type=\"pub\"> (None) is invalid: invalid literal for int() with base 10: 'abc'"
            ],
            advices,
        )
        self.assertEqual(len(results), 1)


class TestCompleteDateValidation(TestCase):
    """Test cases for complete date validation."""

    def setUp(self):
        self.base_params = {
            "parent": {"parent": "article", "parent_id": "1234"},
            "format_error_level": "ERROR",
            "limit_error_level": "ERROR",
            "limit_date": "2024-12-31",
            "pre_pub_ordered_events": ["received", "accepted"],
            "pos_pub_ordered_events": ["published", "corrected"],
        }

        self.base_date_data = {
            "type": "received",
            "year": "2024",
            "month": "01",
            "day": "15",
            "display": "2024-01-15",
            "is_complete": True,
        }

    def test_valid_complete_date(self):
        """Test valid complete date within limit."""
        validator = DateValidation(self.base_date_data, self.base_params)
        results = list(validator.validate_complete_date())
        responses = [item["response"] for item in results]
        advices = [item["advice"] for item in results]
        self.assertEqual(["OK"], responses)
        self.assertEqual([None], advices)
        self.assertEqual(len(results), 1)  # No validation errors

    def test_incomplete_date(self):
        """Test date marked as incomplete."""
        incomplete_date = self.base_date_data.copy()
        incomplete_date["is_complete"] = False
        validator = DateValidation(incomplete_date, self.base_params)
        result = list(validator.validate_complete_date())
        self.assertIsInstance(result[0], dict)  # Should return a single response dict
        self.assertEqual(result[0]["response"], "ERROR")
        self.assertEqual(result[0]["validation_type"], "format")
        self.assertEqual(
            result[0]["expected_value"],
            "a date with year, month (2-digits) and day (2-digits)",
        )


class TestPrePubDateValidation(TestCase):
    """Test cases for pre-publication date validation."""

    def setUp(self):
        self.base_params = {
            "parent": {"parent": "article", "parent_id": "1234"},
            "limit_error_level": "ERROR",
            "limit_date": "2024-12-31",
            "pre_pub_ordered_events": ["received", "accepted"],
            "pos_pub_ordered_events": ["published", "corrected"],
        }

        self.base_date_data = {
            "type": "received",
            "year": "2024",
            "month": "01",
            "day": "15",
            "display": "2024-01-15",
            "is_complete": True,
        }

    def test_valid_pre_pub_date(self):
        """Test valid pre-publication date."""
        validator = DateValidation(self.base_date_data, self.base_params)
        results = list(validator.validate_complete_date())
        responses = [item["response"] for item in results]
        advices = [item["advice"] for item in results]
        self.assertEqual(["OK"], responses)
        self.assertEqual([None], advices)
        self.assertEqual(len(results), 1)

    def test_future_pre_pub_date(self):
        """Test pre-publication date after limit."""
        future_date = self.base_date_data.copy()
        future_date["display"] = "2025-01-01"
        validator = DateValidation(future_date, self.base_params)
        results = list(validator.validate_complete_date())
        responses = [item["response"] for item in results]
        advices = [item["advice"] for item in results]
        self.assertEqual(["ERROR"], responses)
        self.assertEqual(
            [
                '<date date-type="received"> (2025-01-01) must be previous to limit date (2024-12-31)'
            ],
            advices,
        )
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")


class TestFulltextDatesValidation(TestCase):
    def setUp(self):
        # XML sample that will be used across tests
        self.xml_str = """
            <article article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <pub-date date-type="pub">
                            <year>2024</year>
                            <month>01</month>
                            <day>15</day>
                        </pub-date>
                        <pub-date date-type="collection">
                            <year>2024</year>
                            <month>03</month>
                        </pub-date>
                        <history>
                            <date date-type="received">
                                <year>2023</year>
                                <month>12</month>
                                <day>01</day>
                            </date>
                        </history>
                    </article-meta>
                </front>
                <sub-article article-type="translation" id="en" xml:lang="en">
                    <front-stub>
                        <pub-date date-type="pub">
                            <year>2024</year>
                            <month>02</month>
                            <day>01</day>
                        </pub-date>
                    </front-stub>
                </sub-article>
                <sub-article article-type="reviewer-report" id="suppl1" xml:lang="en">
                    <front-stub>
                        <pub-date date-type="pub">
                            <year>2024</year>
                            <month>03</month>
                            <day>01</day>
                        </pub-date>
                        <history>
                            <date date-type="received">
                                <year>2024</year>
                                <month>01</month>
                                <day>20</day>
                            </date>
                            <date date-type="rev-recd">
                                <year>2024</year>
                                <month>02</month>
                                <day>15</day>
                            </date>
                            <date date-type="rev-request">
                                <year>2024</year>
                                <month>01</month>
                                <day>25</day>
                            </date>
                            <date date-type="accepted">
                                <year>2024</year>
                                <month>02</month>
                                <day>20</day>
                            </date>
                        </history>
                    </front-stub>
                </sub-article>
            </article>
        """
        self.tree = etree.fromstring(self.xml_str)

        # Default validation parameters
        self.default_params = {
            "day_format_error_level": "CRITICAL",
            "month_format_error_level": "CRITICAL",
            "year_format_error_level": "CRITICAL",
            "format_error_level": "CRITICAL",
            "value_error_level": "CRITICAL",
            "limit_error_level": "CRITICAL",
            "history_order_error_level": "CRITICAL",
            "missing_events_error_level": "CRITICAL",
            "unexpected_events_error_level": "CRITICAL",
            "required_events": ["received", "accepted"],
            "pre_pub_ordered_events": ["received", "revised", "accepted"],
            "pos_pub_ordered_events": ["pub", "corrected", "retracted"],
            "required_history_events_for_article_type": {},
            "required_history_events_for_related_article_type": {},
            "parent": {"parent": "article"},
            "limit": "2029-01-01",
        }

    def test_validate_main_article(self):
        """Test validation of the main article dates"""
        validator = FulltextDatesValidation(self.tree, self.default_params)
        validation_results = list(validator.validate())

        # Check pub-date presence validations pass for main article
        presence_results = [r for r in validation_results if "presence" in r["title"]]
        pub_presence = [r for r in presence_results if r["sub_item"] == "pub"]
        collection_presence = [r for r in presence_results if r["sub_item"] == "collection"]
        self.assertTrue(any(r["response"] == "OK" for r in pub_presence))
        self.assertTrue(any(r["response"] == "OK" for r in collection_presence))

        # Check publication-format validation (no pub-dates have it in test XML)
        pub_format_results = [r for r in validation_results if r["title"] == "pub-date publication-format"]
        self.assertTrue(len(pub_format_results) > 0)

        # Check missing events CRITICAL is present
        missing_events_results = [r for r in validation_results if r["title"] == "missing events"]
        self.assertTrue(any(r["response"] == "CRITICAL" for r in missing_events_results))

    def test_validate_date_formats(self):
        """Test validation of date formats"""
        # Create XML with invalid date formats
        invalid_xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <year>24</year>
                            <month>1</month>
                            <day>5</day>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2024</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        invalid_tree = etree.fromstring(invalid_xml)

        validator = FulltextDatesValidation(invalid_tree, self.default_params)
        validation_results = list(validator.validate())

        # Check format validation errors
        format_results = [r for r in validation_results if "format" in r["title"] and r["response"] != "OK"]
        format_advices = [r["advice"] for r in format_results]
        self.assertIn('Complete <pub-date date-type="pub"><year> with 4-digits', format_advices)
        self.assertIn('Complete <pub-date date-type="pub"><month> with 2-digits', format_advices)
        self.assertIn('Complete <pub-date date-type="pub"><day> with 2-digits', format_advices)

        # Check missing events
        missing_results = [r for r in validation_results if r["title"] == "missing events"]
        self.assertTrue(any(r["response"] == "CRITICAL" for r in missing_results))

    def test_validate_future_dates(self):
        """Test validation of future dates"""
        # Create XML with future dates
        future_xml = f"""
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <year>2025</year>
                            <month>01</month>
                            <day>01</day>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        future_tree = etree.fromstring(future_xml)

        validator = FulltextDatesValidation(future_tree, self.default_params)
        validation_results = list(validator.validate())
        non_ok_advices = [
            item["advice"] for item in validation_results if item["response"] != "OK"
        ]
        # Missing events should be the only CRITICAL
        self.assertEqual(
            ["History dates found: []. Add missing dates: ['received', 'accepted']"],
            non_ok_advices,
        )

    def test_validate_translation_subarticle(self):
        """Test validation of translation sub-article"""
        translation_xml = """
        <article article-type="research-article" xml:lang="pt">
            <sub-article article-type="translation" id="en" xml:lang="en">
                <front-stub>
                    <pub-date publication-format="electronic" date-type="pub">
                        <year>2024</year>
                        <month>02</month>
                        <day>01</day>
                    </pub-date>
                </front-stub>
            </sub-article>
        </article>
        """
        translation_node = etree.fromstring(translation_xml)

        params = self.default_params.copy()
        params["parent"] = {
            "parent": "sub-article",
            "article-type": "translation",
        }

        validator = FulltextDatesValidation(translation_node, params)
        validation_results = list(validator.validate())
        responses = [item["response"] for item in validation_results]

        # Main article (no dates) should have presence CRITICALs
        main_presence = [r for r in validation_results if "presence" in r["title"]
                         and r.get("parent") is None]

        # Sub-article pub dates should pass format validation
        pub_date_format_results = [r for r in validation_results
                                   if r.get("sub_item") == "pub"
                                   and "format" in r.get("title", "")]
        for r in pub_date_format_results:
            self.assertEqual("OK", r["response"])

    def test_validate_reviewer_report_subarticle_complete(self):
        """Test validation of reviewer report sub-article with complete history"""
        reviewer_report_xml = """
            <sub-article article-type="reviewer-report" id="suppl1" xml:lang="en">
                <front-stub>
                    <pub-date publication-format="electronic" date-type="pub">
                        <year>2024</year>
                        <month>03</month>
                        <day>01</day>
                    </pub-date>
                    <history>
                        <date date-type="received">
                            <year>2024</year>
                            <month>01</month>
                            <day>20</day>
                        </date>
                        <date date-type="accepted">
                            <year>2024</year>
                            <month>02</month>
                            <day>20</day>
                        </date>
                    </history>
                </front-stub>
            </sub-article>
        """
        reviewer_node = etree.fromstring(reviewer_report_xml)

        params = self.default_params.copy()
        params["parent"] = {
            "parent": "sub-article",
            "article-type": "reviewer-report",
        }

        validator = FulltextDatesValidation(reviewer_node, params)
        validation_results = list(validator.validate())
        responses = [item["response"] for item in validation_results]
        # No pub-date-specific CRITICALs for sub-articles
        pub_date_non_ok = [r for r in validation_results
                          if r["response"] != "OK" and r["title"].startswith("pub-date")]
        self.assertEqual(0, len(pub_date_non_ok),
                         f"Expected no pub-date errors: {[(r['title'], r['response']) for r in pub_date_non_ok]}")

    def test_validate_reviewer_report_subarticle_missing_events(self):
        """Test validation of reviewer report sub-article with missing required events"""
        reviewer_report_xml = """
            <sub-article article-type="reviewer-report" id="suppl1" xml:lang="en">
                <front-stub>
                    <pub-date publication-format="electronic" date-type="pub">
                        <year>2024</year>
                        <month>03</month>
                        <day>01</day>
                    </pub-date>
                    <history>
                        <date date-type="received">
                            <year>2024</year>
                            <month>01</month>
                            <day>20</day>
                        </date>
                    </history>
                </front-stub>
            </sub-article>
        """
        reviewer_node = etree.fromstring(reviewer_report_xml)

        params = self.default_params.copy()
        params["parent"] = {
            "parent": "sub-article",
            "article-type": "reviewer-report",
        }
        params["required_events"] = ["received", "accepted"]

        validator = FulltextDatesValidation(reviewer_node, params)
        validation_results = list(validator.validate())
        responses = [item["response"] for item in validation_results]

        # Only missing events should be CRITICAL
        critical_results = [r for r in validation_results if r["response"] == "CRITICAL"]
        self.assertEqual(1, len(critical_results))
        self.assertEqual("missing events", critical_results[0]["title"])

    def test_validate_subarticle_invalid_dates(self):
        """Test validation of sub-article with invalid date formats"""
        invalid_subarticle_xml = """
            <sub-article article-type="letter" id="en" xml:lang="en">
                <front-stub>
                    <pub-date publication-format="electronic" date-type="pub">
                        <year>24</year>
                        <month>2</month>
                        <day>1</day>
                    </pub-date>
                </front-stub>
            </sub-article>
        """
        invalid_node = etree.fromstring(invalid_subarticle_xml)

        params = self.default_params.copy()
        params["parent"] = {
            "parent": "sub-article",
            "article-type": "translation",
        }

        validator = FulltextDatesValidation(invalid_node, params)
        validation_results = list(validator.validate())
        non_ok = [r for r in validation_results if r["response"] != "OK"]
        non_ok_advices = [r["advice"] for r in non_ok]

        # Check format errors are detected
        self.assertIn('Complete <pub-date date-type="pub"><year> with 4-digits', non_ok_advices)
        self.assertIn('Complete <pub-date date-type="pub"><month> with 2-digits', non_ok_advices)
        self.assertIn('Complete <pub-date date-type="pub"><day> with 2-digits', non_ok_advices)
        # Check missing events
        self.assertIn("History dates found: []. Add missing dates: ['received', 'accepted']", non_ok_advices)


class TestPubDatePresenceValidation(TestCase):
    """Test cases for pub-date presence validation (Rules 1 & 2)."""

    def setUp(self):
        self.params = {
            "parent": {"parent": "article"},
            "required_events": [],
        }

    def test_pub_date_pub_presence_ok(self):
        """Rule 1: pub-date with date-type='pub' exists"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <year>2025</year><month>01</month><day>15</day>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_pub_date_pub_presence())
        self.assertEqual(1, len(results))
        self.assertEqual("OK", results[0]["response"])

    def test_pub_date_pub_presence_missing(self):
        """Rule 1: pub-date with date-type='pub' is missing"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_pub_date_pub_presence())
        self.assertEqual(1, len(results))
        self.assertEqual("CRITICAL", results[0]["response"])
        self.assertIn("pub", results[0]["advice"])

    def test_pub_date_collection_presence_ok(self):
        """Rule 2: pub-date with date-type='collection' exists"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <year>2025</year><month>01</month><day>15</day>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_pub_date_collection_presence())
        self.assertEqual(1, len(results))
        self.assertEqual("OK", results[0]["response"])

    def test_pub_date_collection_presence_missing(self):
        """Rule 2: pub-date with date-type='collection' is missing"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <year>2025</year><month>01</month><day>15</day>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_pub_date_collection_presence())
        self.assertEqual(1, len(results))
        self.assertEqual("CRITICAL", results[0]["response"])
        self.assertIn("collection", results[0]["advice"])

    def test_pub_date_presence_not_checked_for_sub_articles(self):
        """Rules 1 & 2: Presence is not checked for sub-articles"""
        xml = """
            <article article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <year>2024</year><month>02</month><day>01</day>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2024</year>
                        </pub-date>
                    </article-meta>
                </front>
                <sub-article article-type="translation" id="en" xml:lang="en">
                    <front-stub>
                        <pub-date publication-format="electronic" date-type="pub">
                            <year>2024</year><month>02</month><day>01</day>
                        </pub-date>
                    </front-stub>
                </sub-article>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        # Get results from the sub-article's validation (via translations)
        sub_results = list(validator.validate_translations())
        # Sub-article should NOT have presence validation results
        presence_results = [r for r in sub_results if "presence" in r["title"]]
        self.assertEqual(0, len(presence_results))


class TestPublicationFormatValidation(TestCase):
    """Test cases for publication-format validation (Rule 3)."""

    def setUp(self):
        self.params = {
            "parent": {"parent": "article"},
            "required_events": [],
        }

    def test_publication_format_electronic_ok(self):
        """Rule 3: All pub-dates have publication-format='electronic'"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <year>2025</year><month>01</month><day>15</day>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_publication_format())
        self.assertEqual(2, len(results))
        self.assertTrue(all(r["response"] == "OK" for r in results))

    def test_publication_format_missing(self):
        """Rule 3: pub-date without publication-format"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date date-type="pub">
                            <year>2025</year><month>01</month><day>15</day>
                        </pub-date>
                        <pub-date date-type="collection">
                            <year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_publication_format())
        self.assertEqual(2, len(results))
        self.assertTrue(all(r["response"] == "CRITICAL" for r in results))

    def test_publication_format_wrong_value(self):
        """Rule 3: pub-date with wrong publication-format value"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="print" date-type="pub">
                            <year>2025</year><month>01</month><day>15</day>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_publication_format())
        self.assertEqual(2, len(results))
        pub_result = [r for r in results if r["sub_item"] == "pub"][0]
        coll_result = [r for r in results if r["sub_item"] == "collection"][0]
        self.assertEqual("CRITICAL", pub_result["response"])
        self.assertEqual("print", pub_result["got_value"])
        self.assertEqual("OK", coll_result["response"])


class TestPubDateRequiredElementsValidation(TestCase):
    """Test cases for required elements validation (Rules 4, 5, 6)."""

    def setUp(self):
        self.params = {
            "parent": {"parent": "article"},
            "required_events": [],
        }

    def test_pub_date_pub_all_elements_present(self):
        """Rule 4: pub date has day, month, and year"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>15</day><month>03</month><year>2025</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_pub_date_pub_required_elements())
        self.assertEqual(3, len(results))
        self.assertTrue(all(r["response"] == "OK" for r in results))

    def test_pub_date_pub_missing_day(self):
        """Rule 4: pub date missing day"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <month>03</month><year>2025</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_pub_date_pub_required_elements())
        day_result = [r for r in results if "day" in r["title"]][0]
        self.assertEqual("CRITICAL", day_result["response"])

    def test_pub_date_pub_missing_month(self):
        """Rule 4: pub date missing month"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>15</day><year>2025</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_pub_date_pub_required_elements())
        month_result = [r for r in results if "month" in r["title"]][0]
        self.assertEqual("CRITICAL", month_result["response"])

    def test_pub_date_pub_with_placeholder_zeros(self):
        """Rule 4: pub date with 00 placeholders should still pass (elements present)"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>00</day><month>00</month><year>2025</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_pub_date_pub_required_elements())
        self.assertEqual(3, len(results))
        self.assertTrue(all(r["response"] == "OK" for r in results))

    def test_collection_date_year_present(self):
        """Rule 5: collection date has year"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>01</day><month>01</month><year>2025</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_pub_date_collection_required_year())
        self.assertEqual(1, len(results))
        self.assertEqual("OK", results[0]["response"])

    def test_collection_date_no_day(self):
        """Rule 6: collection date does not have day (valid)"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>01</day><month>01</month><year>2025</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_pub_date_collection_no_day())
        self.assertEqual(1, len(results))
        self.assertEqual("OK", results[0]["response"])

    def test_collection_date_with_day_error(self):
        """Rule 6: collection date has day (invalid)"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>01</day><month>01</month><year>2025</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <day>15</day><month>03</month><year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_pub_date_collection_no_day())
        self.assertEqual(1, len(results))
        self.assertEqual("ERROR", results[0]["response"])
        self.assertIn("Remove <day>", results[0]["advice"])

    def test_collection_date_with_month_ok(self):
        """Collection date with month is valid (monthly periodicity)"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>01</day><month>01</month><year>2025</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <month>03</month><year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_pub_date_collection_no_day())
        self.assertEqual(1, len(results))
        self.assertEqual("OK", results[0]["response"])

    def test_collection_date_with_season_ok(self):
        """Collection date with season is valid (bimonthly/quarterly)"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>01</day><month>01</month><year>2025</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <season>Jan-Feb</season><year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_pub_date_collection_no_day())
        self.assertEqual(1, len(results))
        self.assertEqual("OK", results[0]["response"])


class TestPubDateUniquenessValidation(TestCase):
    """Test cases for pub-date uniqueness validation (Rule 8)."""

    def setUp(self):
        self.params = {
            "parent": {"parent": "article"},
            "required_events": [],
        }

    def test_uniqueness_ok(self):
        """Rule 8: Exactly one pub and one collection"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>01</day><month>01</month><year>2025</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_pub_date_uniqueness())
        self.assertEqual(2, len(results))
        self.assertTrue(all(r["response"] == "OK" for r in results))

    def test_duplicate_pub_date_types(self):
        """Rule 8: Duplicate pub-date with same date-type"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>01</day><month>01</month><year>2025</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>15</day><month>03</month><year>2025</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_pub_date_uniqueness())
        pub_result = [r for r in results if r["sub_item"] == "pub"][0]
        coll_result = [r for r in results if r["sub_item"] == "collection"][0]
        self.assertEqual("ERROR", pub_result["response"])
        self.assertEqual("OK", coll_result["response"])


class TestDayMonthValuesValidation(TestCase):
    """Test cases for day/month numeric range validation (Rule 9)."""

    def setUp(self):
        self.params = {
            "parent": {"parent": "article"},
            "required_events": [],
        }

    def test_valid_day_month_values(self):
        """Rule 9: Valid day (01-31) and month (01-12)"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>15</day><month>03</month><year>2025</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <month>03</month><year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_day_month_values())
        self.assertTrue(all(r["response"] == "OK" for r in results))

    def test_invalid_day_value(self):
        """Rule 9: Day value out of range (32)"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>32</day><month>03</month><year>2025</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_day_month_values())
        day_results = [r for r in results if r["title"] == "pub-date day value"]
        self.assertTrue(any(r["response"] == "ERROR" for r in day_results))

    def test_invalid_month_value(self):
        """Rule 9: Month value out of range (13)"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>01</day><month>13</month><year>2025</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_day_month_values())
        month_results = [r for r in results if r["title"] == "pub-date month value"]
        self.assertTrue(any(r["response"] == "ERROR" for r in month_results))

    def test_zero_day_month_valid(self):
        """Rule 9: Day/month with 00 (placeholder) is valid"""
        xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>00</day><month>00</month><year>2025</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate_day_month_values())
        self.assertTrue(all(r["response"] == "OK" for r in results))


class TestFullValidXml(TestCase):
    """Integration tests with complete valid XML examples from the issue."""

    def setUp(self):
        self.params = {
            "parent": {"parent": "article"},
            "required_events": [],
        }

    def test_annual_periodicity(self):
        """Valid XML: Annual periodicity (collection with year only)"""
        xml = """
            <article article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>01</day><month>01</month><year>2025</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate())
        non_ok = [r for r in results if r["response"] != "OK"]
        self.assertEqual(0, len(non_ok), f"Expected all OK: {[(r['title'], r['response']) for r in non_ok]}")

    def test_monthly_periodicity(self):
        """Valid XML: Monthly periodicity (collection with month+year)"""
        xml = """
            <article article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>01</day><month>01</month><year>2025</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <month>01</month><year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate())
        non_ok = [r for r in results if r["response"] != "OK"]
        self.assertEqual(0, len(non_ok), f"Expected all OK: {[(r['title'], r['response']) for r in non_ok]}")

    def test_bimonthly_with_season(self):
        """Valid XML: Bimonthly with season"""
        xml = """
            <article article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>01</day><month>01</month><year>2025</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <season>Jan-Feb</season><year>2025</year>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        tree = etree.fromstring(xml)
        validator = FulltextDatesValidation(tree, self.params)
        results = list(validator.validate())
        non_ok = [r for r in results if r["response"] != "OK"]
        self.assertEqual(0, len(non_ok), f"Expected all OK: {[(r['title'], r['response']) for r in non_ok]}")
