from datetime import date
from unittest import TestCase
from unittest.mock import Mock, patch

from lxml import etree
from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation import dates
from packtools.sps.validation.dates import DateValidation, FulltextDatesValidation


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
        self.assertIsInstance(result[0], dict)  # Should return a single response dict
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
        """Set up test fixtures before each test method."""
        self.mock_fulltext_dates = Mock()
        self.mock_fulltext_dates.fulltext = Mock()
        self.mock_fulltext_dates.fulltext.article_type = "research-article"
        self.mock_fulltext_dates.translations = {}
        self.mock_fulltext_dates.not_translations = {}

        self.base_params = {
            "parent": {
                "parent": "test_parent",
                "parent_id": "123",
                "parent_article_type": "research-article",
                "parent_lang": "en",
            },
            "required_events": ["received", "accepted"],
            "pre_pub_ordered_events": ["received", "revised", "accepted"],
            "pos_pub_ordered_events": ["pub", "corrected", "retracted"],
            "unexpected_events_error_level": "ERROR",
            "missing_events_error_level": "ERROR",
            "history_order_error_level": "ERROR",
        }

    def test_validate_history_events_with_unexpected_events(self):
        """Test validation when there are unexpected events in history."""
        self.mock_fulltext_dates.date_types_ordered_by_date = [
            "received",
            "unknown_event",
            "accepted",
        ]
        self.mock_fulltext_dates.history_dates = {
            "received": "2023-01-01",
            "unknown_event": "2023-02-01",
            "accepted": "2023-03-01",
        }

        validator = FulltextDatesValidation(self.mock_fulltext_dates, self.base_params)
        results = list(validator.validate_history_events())

        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result["title"], "unexpected events")
        self.assertEqual(result["got_value"], ["received", "unknown_event", "accepted"])
        self.assertEqual(
            result["expected_value"],
            ["received", "revised", "accepted", "pub", "corrected", "retracted"],
        )
        self.assertIn("Fix date-type or exclude unexpected dates", result["advice"])
        self.assertEqual(result["response"], "ERROR")

    def test_validate_history_events_with_missing_events(self):
        """Test validation when required events are missing."""
        self.mock_fulltext_dates.date_types_ordered_by_date = ["received"]
        self.mock_fulltext_dates.history_dates = {"received": "2023-01-01"}

        validator = FulltextDatesValidation(self.mock_fulltext_dates, self.base_params)
        results = list(validator.validate_history_events())

        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result["title"], "missing events")
        self.assertEqual(result["got_value"], ["received"])
        self.assertEqual(
            result["expected_value"],
            ["received", "revised", "accepted", "pub", "corrected", "retracted"],
        )
        self.assertIn("Fix date-type or including missing dates", result["advice"])
        self.assertEqual(result["response"], "ERROR")

    def test_validate_history_order_with_incorrect_order(self):
        """Test validation when history events are in incorrect order."""
        self.mock_fulltext_dates.date_types_ordered_by_date = ["accepted", "received"]
        self.mock_fulltext_dates.history_dates = {
            "accepted": "2023-01-01",
            "received": "2023-02-01",
        }

        validator = FulltextDatesValidation(self.mock_fulltext_dates, self.base_params)
        results = list(validator.validate_history_order())

        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result["title"], "ordered events")
        self.assertEqual(result["got_value"], ["accepted", "received"])
        self.assertEqual(
            result["expected_value"],
            ["received", "revised", "accepted", "pub", "corrected", "retracted"],
        )
        self.assertIn("Check and fix date and date-type", result["advice"])
        self.assertEqual(result["response"], "ERROR")

    @patch("packtools.sps.validation.dates.date", return_value=date(2024, 1, 1))
    def test_validate_article_date(self, mock_date):
        """Test validation of article date."""
        self.mock_fulltext_dates.article_date = {
            "is_complete": False,
            "year": None,
            "month": None,
            "day": None,
            "type": "pub",
        }

        with patch(
            "packtools.sps.validation.dates.DateValidation"
        ) as MockDateValidation:

            mock_date_validation = MockDateValidation()
            validator = FulltextDatesValidation(
                self.mock_fulltext_dates, self.base_params
            )
            list(validator.validate_article_date())  # Consume the generator
            # Verify that DateValidation was called with correct parameters
        self.assertEqual(mock_date_validation.validate_date.call_count, 1)
        self.assertEqual(mock_date_validation.validate_complete_date.call_count, 1)

    def test_validate_collection_date(self):
        """Test validation of collection date."""
        self.mock_fulltext_dates.collection_date = {
            "is_complete": False,
            "year": None,
            "month": None,
            "day": None,
            "type": "collection",
        }

        with patch(
            "packtools.sps.validation.dates.DateValidation"
        ) as MockDateValidation:
            mock_date_validation = MockDateValidation()
            validator = FulltextDatesValidation(
                self.mock_fulltext_dates, self.base_params
            )
            list(validator.validate_collection_date())  # Consume the generator

        # Verify that only basic validation was called, not completeness
        self.assertEqual(mock_date_validation.validate_date.call_count, 1)
        self.assertEqual(mock_date_validation.validate_complete_date.call_count, 0)


class TestArticleTypeParamsOverride(TestCase):
    def setUp(self):
        """Set up test fixtures."""
        self.mock_fulltext = Mock()
        self.mock_fulltext_dates = Mock()
        self.mock_fulltext_dates.fulltext = self.mock_fulltext
        self.mock_fulltext_dates.translations = {}
        self.mock_fulltext_dates.not_translations = {}
        self.mock_fulltext_dates.date_types_ordered_by_date = []
        self.mock_fulltext_dates.related_articles = []

    def test_article_type_params_override_defaults(self):
        """Test that article-type specific parameters override default values."""
        # Arrange
        self.mock_fulltext.article_type = "research-article"

        params = {
            # Default values
            "day_format_error_level": "CRITICAL",
            "month_format_error_level": "CRITICAL",
            "required_events": ["received"],
            # Article type specific params
            "research-article": {
                "day_format_error_level": "WARNING",
                "required_events": ["received", "accepted", "published"],
                "history_order_error_level": "ERROR",
            },
        }

        # Act
        validator = FulltextDatesValidation(self.mock_fulltext_dates, params)

        # Assert
        self.assertEqual(validator.params["day_format_error_level"], "WARNING")
        self.assertEqual(validator.params["month_format_error_level"], "CRITICAL")
        self.assertEqual(
            validator.params["required_events"], ["received", "accepted", "published"]
        )
        self.assertEqual(validator.params["history_order_error_level"], "ERROR")

    def test_multiple_article_types_params(self):
        """Test that correct article type parameters are used for different article types."""
        # Arrange
        params = {
            # Default values
            "day_format_error_level": "CRITICAL",
            "required_events": ["received"],
            # Article type specific params
            "research-article": {
                "day_format_error_level": "WARNING",
                "required_events": ["received", "accepted", "published"],
            },
            "review-article": {
                "day_format_error_level": "ERROR",
                "required_events": ["received", "reviewed"],
            },
        }

        # Test research-article
        self.mock_fulltext.article_type = "research-article"
        validator_research = FulltextDatesValidation(self.mock_fulltext_dates, params)

        self.assertEqual(validator_research.params["day_format_error_level"], "WARNING")
        self.assertEqual(
            validator_research.params["required_events"],
            ["received", "accepted", "published"],
        )

        # Test review-article
        self.mock_fulltext.article_type = "review-article"
        validator_review = FulltextDatesValidation(self.mock_fulltext_dates, params)

        self.assertEqual(validator_review.params["day_format_error_level"], "ERROR")
        self.assertEqual(
            validator_review.params["required_events"], ["received", "reviewed"]
        )

    def test_undefined_article_type_uses_defaults(self):
        """Test that undefined article type falls back to default values."""
        # Arrange
        self.mock_fulltext.article_type = "undefined-type"

        params = {
            # Default values
            "day_format_error_level": "CRITICAL",
            "required_events": ["received"],
            "research-article": {
                "day_format_error_level": "WARNING",
                "required_events": ["received", "accepted"],
            },
        }

        # Act
        validator = FulltextDatesValidation(self.mock_fulltext_dates, params)

        # Assert
        self.assertEqual(validator.params["day_format_error_level"], "CRITICAL")
        self.assertEqual(validator.params["required_events"], ["received"])

    def test_partial_article_type_params_override(self):
        """Test that partial article-type params only override specified values."""
        # Arrange
        self.mock_fulltext.article_type = "research-article"

        params = {
            # Default values
            "day_format_error_level": "CRITICAL",
            "month_format_error_level": "CRITICAL",
            "required_events": ["received"],
            "pre_pub_ordered_events": ["received", "revised", "accepted"],
            # Partial override for research-article
            "research-article": {
                "day_format_error_level": "WARNING",
                "required_events": ["received", "accepted"],
            },
        }

        # Act
        validator = FulltextDatesValidation(self.mock_fulltext_dates, params)

        # Assert
        # These should be overridden
        self.assertEqual(validator.params["day_format_error_level"], "WARNING")
        self.assertEqual(validator.params["required_events"], ["received", "accepted"])

        # These should maintain default values
        self.assertEqual(validator.params["month_format_error_level"], "CRITICAL")
        self.assertEqual(
            validator.params["pre_pub_ordered_events"],
            ["received", "revised", "accepted"],
        )

    def test_validate_with_article_type_params(self):
        """Test that validation uses article-type specific parameters."""
        # Arrange
        self.mock_fulltext.article_type = "research-article"
        self.mock_fulltext_dates.date_types_ordered_by_date = ["received"]
        self.mock_fulltext_dates.history_dates = {"received": "2023-01-01"}

        params = {
            "required_events": ["received"],
            "research-article": {
                "required_events": ["received", "accepted"],
                "missing_events_error_level": "ERROR",
            },
        }

        # Act
        validator = FulltextDatesValidation(self.mock_fulltext_dates, params)
        results = list(validator.validate_history_events())

        # Assert
        missing_event_result = next(
            r for r in results if r["title"] == "missing events"
        )
        self.assertEqual(missing_event_result["response"], "ERROR")
        self.assertIn("accepted", missing_event_result["advice"])


class TestFulltextDatesValidation(TestCase):
    def create_mock_fulltext_dates(self, related_articles=None):
        """Helper method to create a mock FulltextDates object"""
        mock_fulltext = Mock()
        mock_fulltext_dates = Mock()
        mock_fulltext_dates.fulltext = mock_fulltext
        mock_fulltext_dates.related_articles = related_articles or []
        mock_fulltext_dates.date_types_ordered_by_date = []
        return mock_fulltext_dates

    def test_init_with_no_related_articles(self):
        """Test initialization without any related articles"""
        params = {
            "required_events": ["received", "accepted"],
            "pre_pub_ordered_events": ["received", "revised", "accepted"],
            "pos_pub_ordered_events": ["pub", "corrected", "retracted"],
            "related-article-type": {
                "addendum": "addended",
                "correction": "corrected",
                "retraction": "retracted",
            },
        }

        mock_fulltext_dates = self.create_mock_fulltext_dates()
        validator = FulltextDatesValidation(mock_fulltext_dates, params)

        self.assertEqual(validator.params["required_events"], ["received", "accepted"])

    def test_init_with_single_related_article(self):
        """Test initialization with a single related article that should add an event"""
        params = {
            "required_events": ["received", "accepted"],
            "pre_pub_ordered_events": ["received", "revised", "accepted"],
            "pos_pub_ordered_events": ["pub", "corrected", "retracted"],
            "related-article-type": {
                "addendum": "addended",
                "correction": "corrected",
                "retraction": "retracted",
            },
        }

        related_articles = [{"related-article-type": "correction"}]
        mock_fulltext_dates = self.create_mock_fulltext_dates(related_articles)

        validator = FulltextDatesValidation(mock_fulltext_dates, params)

        self.assertIn("corrected", validator.params["required_events"])
        self.assertEqual(
            set(validator.params["required_events"]),
            {"received", "accepted", "corrected"},
        )

    def test_init_with_multiple_related_articles(self):
        """Test initialization with multiple related articles"""
        params = {
            "required_events": ["received", "accepted"],
            "pre_pub_ordered_events": ["received", "revised", "accepted"],
            "pos_pub_ordered_events": ["pub", "corrected", "retracted"],
            "related-article-type": {
                "addendum": "addended",
                "correction": "corrected",
                "retraction": "retracted",
            },
        }

        related_articles = [
            {"related-article-type": "correction"},
            {"related-article-type": "retraction"},
            {"related-article-type": "addendum"},
        ]
        mock_fulltext_dates = self.create_mock_fulltext_dates(related_articles)

        validator = FulltextDatesValidation(mock_fulltext_dates, params)

        expected_events = {"received", "accepted", "corrected", "retracted", "addended"}
        self.assertEqual(set(validator.params["required_events"]), expected_events)

    def test_init_with_null_related_article_type(self):
        """Test initialization with related article types that map to None"""
        params = {
            "required_events": ["received", "accepted"],
            "pre_pub_ordered_events": ["received", "revised", "accepted"],
            "pos_pub_ordered_events": ["pub", "corrected", "retracted"],
            "related-article-type": {
                "letter": None,
                "response": None,
                "correction": "corrected",
            },
        }

        related_articles = [
            {"related-article-type": "letter"},
            {"related-article-type": "response"},
            {"related-article-type": "correction"},
        ]
        mock_fulltext_dates = self.create_mock_fulltext_dates(related_articles)

        validator = FulltextDatesValidation(mock_fulltext_dates, params)

        self.assertEqual(
            set(validator.params["required_events"]),
            {"received", "accepted", "corrected"},
        )

    def test_init_with_unknown_related_article_type(self):
        """Test initialization with unknown related article type"""
        params = {
            "required_events": ["received", "accepted"],
            "pre_pub_ordered_events": ["received", "revised", "accepted"],
            "pos_pub_ordered_events": ["pub", "corrected", "retracted"],
            "related-article-type": {"correction": "corrected"},
        }

        related_articles = [
            {"related-article-type": "unknown_type"},
            {"related-article-type": "correction"},
        ]
        mock_fulltext_dates = self.create_mock_fulltext_dates(related_articles)

        validator = FulltextDatesValidation(mock_fulltext_dates, params)

        self.assertEqual(
            set(validator.params["required_events"]),
            {"received", "accepted", "corrected"},
        )

    def test_init_with_duplicate_related_articles(self):
        """Test initialization with duplicate related article types"""
        params = {
            "required_events": ["received", "accepted"],
            "pre_pub_ordered_events": ["received", "revised", "accepted"],
            "pos_pub_ordered_events": ["pub", "corrected", "retracted"],
            "related-article-type": {"correction": "corrected"},
        }

        related_articles = [
            {"related-article-type": "correction"},
            {"related-article-type": "correction"},
        ]
        mock_fulltext_dates = self.create_mock_fulltext_dates(related_articles)

        validator = FulltextDatesValidation(mock_fulltext_dates, params)

        # Should only add "corrected" once
        self.assertEqual(validator.params["required_events"].count("corrected"), 2)
        self.assertEqual(
            set(validator.params["required_events"]),
            {"received", "accepted", "corrected"},
        )

    def test_init_preserves_original_required_events(self):
        """Test that original required events are preserved when adding related article events"""
        params = {
            "required_events": ["received", "accepted"],
            "pre_pub_ordered_events": ["received", "revised", "accepted"],
            "pos_pub_ordered_events": ["pub", "corrected", "retracted"],
            "related-article-type": {"correction": "corrected"},
        }

        related_articles = [{"related-article-type": "correction"}]
        mock_fulltext_dates = self.create_mock_fulltext_dates(related_articles)

        validator = FulltextDatesValidation(mock_fulltext_dates, params)

        for event in ["received", "accepted"]:
            self.assertIn(event, validator.params["required_events"])
