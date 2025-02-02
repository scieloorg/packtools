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
        self.assertEqual(result, [])

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
        self.assertEqual(result, [])

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
        self.assertEqual(result, [])

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
        self.assertEqual(len(results), 0)  # No validation errors

    def test_invalid_date_components(self):
        # Test invalid month
        invalid_date = self.base_date_data.copy()
        invalid_date["month"] = "13"
        validator = DateValidation(invalid_date, self.base_params)
        results = list(validator.validate_date())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")

        # Test invalid year
        invalid_date["year"] = "abc"
        validator = DateValidation(invalid_date, self.base_params)
        results = list(validator.validate_date())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")


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
        self.assertEqual(len(results), 0)  # No validation errors

    def test_incomplete_date(self):
        """Test date marked as incomplete."""
        incomplete_date = self.base_date_data.copy()
        incomplete_date["is_complete"] = False
        validator = DateValidation(incomplete_date, self.base_params)
        result = list(validator.validate_complete_date())
        self.assertIsInstance(
            result[0], dict
        )  # Should return a single response dict
        self.assertEqual(result[0]["response"], "ERROR")
        self.assertEqual(result[0]["validation_type"], "format")
        self.assertEqual(result[0]["expected_value"], "complete date")


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
        self.assertEqual(len(results), 0)

    def test_future_pre_pub_date(self):
        """Test pre-publication date after limit."""
        future_date = self.base_date_data.copy()
        future_date["display"] = "2025-01-01"
        validator = DateValidation(future_date, self.base_params)
        results = list(validator.validate_complete_date())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")
        self.assertIn("<=", results[0]["advice"])


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

        # Check that validation was performed
        self.assertGreater(len(validation_results), 0)

        # Verify article date validation
        article_date_results = [
            r for r in validation_results if r.get("sub_item") == "pub"
        ]
        # Se não houver resposta com "CRITICAL", significa que a validação passou
        self.assertFalse(
            any(r.get("response") == "CRITICAL" for r in article_date_results)
        )

    def test_validate_date_formats(self):
        """Test validation of date formats"""
        # Create XML with invalid date formats
        invalid_xml = """
            <article>
                <front>
                    <article-meta>
                        <pub-date date-type="pub">
                            <year>24</year>
                            <month>1</month>
                            <day>5</day>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        invalid_tree = etree.fromstring(invalid_xml)

        validator = FulltextDatesValidation(invalid_tree, self.default_params)
        validation_results = list(validator.validate())

        expected = [
            "Provide 4-digits year",
            "Provide 2-digits month",
            "Provide 2-digits day",
            "Provide date (pub: 24-1-5) < 2025-01-29",
            "Fix date-type or include missing dates: ['received', 'accepted']",
        ]

        # Deve haver resposta com "CRITICAL" devido aos formatos inválidos
        self.assertEqual(5, len(validation_results))

    def test_validate_future_dates(self):
        """Test validation of future dates"""
        # Create XML with future dates
        future_xml = f"""
            <article>
                <front>
                    <article-meta>
                        <pub-date date-type="pub">
                            <year>2025</year>
                            <month>01</month>
                            <day>01</day>
                        </pub-date>
                    </article-meta>
                </front>
            </article>
        """
        future_tree = etree.fromstring(future_xml)

        validator = FulltextDatesValidation(future_tree, self.default_params)
        validation_results = list(validator.validate())

        # Check future date validation
        value_results = [
            r for r in validation_results if r.get("validation_type") == "value"
        ]
        # Deve haver resposta com "CRITICAL" devido à data futura
        self.assertTrue(
            any(r.get("response") == "CRITICAL" for r in value_results)
        )

    def test_validate_translation_subarticle(self):
        """Test validation of translation sub-article"""
        translation_xml = """
        <article article-type="research-article" xml:lang="pt">
            <sub-article article-type="translation" id="en" xml:lang="en">
                <front-stub>
                    <pub-date date-type="pub">
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

        # Verify pub date validation
        pub_date_results = [
            r for r in validation_results if r.get("sub_item") == "pub"
        ]
        self.assertFalse(
            any(r.get("response") == "CRITICAL" for r in pub_date_results)
        )

    def test_validate_reviewer_report_subarticle_complete(self):
        """Test validation of reviewer report sub-article with complete history"""
        reviewer_report_xml = """
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

        # Check history dates validation
        history_results = [
            r for r in validation_results if r.get("item") == "history"
        ]
        self.assertFalse(
            any(r.get("response") == "CRITICAL" for r in history_results)
        )

    def test_validate_reviewer_report_subarticle_missing_events(self):
        """Test validation of reviewer report sub-article with missing required events"""
        reviewer_report_xml = """
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

        # Check for missing events validation
        missing_events_results = [
            r for r in validation_results if r.get("title") == "missing events"
        ]
        self.assertTrue(
            any(r.get("response") == "CRITICAL" for r in missing_events_results)
        )

    def test_validate_subarticle_invalid_dates(self):
        """Test validation of sub-article with invalid date formats"""
        invalid_subarticle_xml = """
            <sub-article article-type="letter" id="en" xml:lang="en">
                <front-stub>
                    <pub-date date-type="pub">
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

        # Check format validation results
        format_results = [
            r
            for r in validation_results
            if r.get("validation_type") == "format"
        ]
        self.assertTrue(
            any(r.get("response") == "CRITICAL" for r in format_results)
        )
