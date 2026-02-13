"""
Tests for history element validations according to SPS 1.10.

This module tests the validation rules for the <history> element,
ensuring compliance with the SPS 1.10 specification.
"""

from unittest import TestCase
from lxml import etree

from packtools.sps.validation.history import (
    HistoryValidation,
    ALLOWED_DATE_TYPES,
    COMPLETE_DATE_REQUIRED_TYPES,
    EXEMPT_ARTICLE_TYPES,
)


class TestHistoryUniqueness(TestCase):
    """Tests for Rule 1: History element uniqueness."""
    
    def test_single_history_in_article_meta(self):
        """Test that a single <history> in article-meta is valid."""
        xml = """
        <article>
            <front>
                <article-meta>
                    <history>
                        <date date-type="received">
                            <day>15</day>
                            <month>03</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_history_uniqueness())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
        self.assertEqual(results[0]["title"], "history uniqueness")
    
    def test_single_history_in_front_stub(self):
        """Test that a single <history> in front-stub is valid."""
        xml = """
        <article>
            <sub-article article-type="reviewer-report">
                <front-stub>
                    <history>
                        <date date-type="received">
                            <day>15</day>
                            <month>03</month>
                            <year>2024</year>
                        </date>
                    </history>
                </front-stub>
            </sub-article>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_history_uniqueness())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
        self.assertEqual(results[0]["response"], "OK")
    
    def test_multiple_history_elements(self):
        """Test that multiple <history> elements are invalid."""
        xml = """
        <article>
            <front>
                <article-meta>
                    <history>
                        <date date-type="received">
                            <day>15</day>
                            <month>03</month>
                            <year>2024</year>
                        </date>
                    </history>
                    <history>
                        <date date-type="accepted">
                            <day>20</day>
                            <month>04</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_history_uniqueness())
        
        self.assertEqual(len(results), 1)
        self.assertNotEqual(results[0]["response"], "OK")
        self.assertEqual(results[0]["response"], "ERROR")
        self.assertIn("duplicate", results[0]["advice"].lower())
        self.assertIn("2", results[0]["got_value"])
    
    def test_no_history_element(self):
        """Test that no <history> element is valid."""
        xml = """
        <article>
            <front>
                <article-meta>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_history_uniqueness())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
        self.assertEqual(results[0]["response"], "OK")


class TestDateTypePresence(TestCase):
    """Tests for Rule 2: @date-type attribute presence."""
    
    def test_date_with_date_type(self):
        """Test that <date> with @date-type is valid."""
        xml = """
        <article>
            <front>
                <article-meta>
                    <history>
                        <date date-type="received">
                            <day>15</day>
                            <month>03</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_date_type_presence())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
        self.assertEqual(results[0]["response"], "OK")
        self.assertEqual(results[0]["got_value"], "received")
    
    def test_date_without_date_type(self):
        """Test that <date> without @date-type is invalid."""
        xml = """
        <article>
            <front>
                <article-meta>
                    <history>
                        <date>
                            <day>15</day>
                            <month>03</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_date_type_presence())
        
        self.assertEqual(len(results), 1)
        self.assertNotEqual(results[0]["response"], "OK")
        self.assertEqual(results[0]["response"], "CRITICAL")
        self.assertEqual(results[0]["got_value"], "missing")
        self.assertIn("Add @date-type", results[0]["advice"])
    
    def test_date_with_empty_date_type(self):
        """Test that <date> with empty @date-type is invalid."""
        xml = """
        <article>
            <front>
                <article-meta>
                    <history>
                        <date date-type="">
                            <day>15</day>
                            <month>03</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_date_type_presence())
        
        self.assertEqual(len(results), 1)
        self.assertNotEqual(results[0]["response"], "OK")
        self.assertEqual(results[0]["response"], "CRITICAL")
    
    def test_multiple_dates_mixed_presence(self):
        """Test validation of multiple dates with mixed @date-type presence."""
        xml = """
        <article>
            <front>
                <article-meta>
                    <history>
                        <date date-type="received">
                            <day>15</day>
                            <month>03</month>
                            <year>2024</year>
                        </date>
                        <date>
                            <day>20</day>
                            <month>04</month>
                            <year>2024</year>
                        </date>
                        <date date-type="accepted">
                            <day>25</day>
                            <month>05</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_date_type_presence())
        
        self.assertEqual(len(results), 3)
        # First and third should be valid
        self.assertEqual(results[0]["response"], "OK")
        self.assertNotEqual(results[1]["response"], "OK")
        self.assertEqual(results[2]["response"], "OK")


class TestDateTypeValues(TestCase):
    """Tests for Rule 3: Allowed @date-type values."""
    
    def test_valid_date_types(self):
        """Test that all allowed date types are valid."""
        for date_type in ALLOWED_DATE_TYPES:
            xml = f"""
            <article>
                <front>
                    <article-meta>
                        <history>
                            <date date-type="{date_type}">
                                <year>2024</year>
                            </date>
                        </history>
                    </article-meta>
                </front>
            </article>
            """
            tree = etree.fromstring(xml)
            validator = HistoryValidation(tree)
            results = list(validator.validate_date_type_values())
            
            self.assertEqual(len(results), 1, f"Failed for date-type={date_type}")
            self.assertEqual(results[0]["response"], "OK", f"Failed for date-type={date_type}")
            self.assertEqual(results[0]["got_value"], date_type)
    
    def test_invalid_date_type(self):
        """Test that invalid date types are rejected."""
        xml = """
        <article>
            <front>
                <article-meta>
                    <history>
                        <date date-type="invalid-type">
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_date_type_values())
        
        self.assertEqual(len(results), 1)
        self.assertNotEqual(results[0]["response"], "OK")
        self.assertEqual(results[0]["response"], "ERROR")
        self.assertEqual(results[0]["got_value"], "invalid-type")
        self.assertIn("allowed values", results[0]["advice"])
    
    def test_multiple_dates_mixed_validity(self):
        """Test validation with both valid and invalid date types."""
        xml = """
        <article>
            <front>
                <article-meta>
                    <history>
                        <date date-type="received">
                            <year>2024</year>
                        </date>
                        <date date-type="bad-type">
                            <year>2024</year>
                        </date>
                        <date date-type="accepted">
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_date_type_values())
        
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]["response"], "OK")  # received
        self.assertNotEqual(results[1]["response"], "OK")  # bad-type
        self.assertEqual(results[2]["response"], "OK")  # accepted


class TestRequiredDates(TestCase):
    """Tests for Rules 4 & 5: Required dates (received, accepted)."""
    
    def test_regular_article_with_required_dates(self):
        """Test that regular articles require received and accepted dates."""
        xml = """
        <article article-type="research-article">
            <front>
                <article-meta>
                    <history>
                        <date date-type="received">
                            <day>15</day>
                            <month>03</month>
                            <year>2024</year>
                        </date>
                        <date date-type="accepted">
                            <day>20</day>
                            <month>05</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_required_dates())
        
        # Should have 2 results: one for received, one for accepted
        self.assertEqual(len(results), 2)
        # Both should be valid
        self.assertTrue(all(r["response"] == "OK" for r in results))
        self.assertTrue(all(r["response"] == "OK" for r in results))
    
    def test_regular_article_missing_received(self):
        """Test that regular articles without received date are invalid."""
        xml = """
        <article article-type="research-article">
            <front>
                <article-meta>
                    <history>
                        <date date-type="accepted">
                            <day>20</day>
                            <month>05</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_required_dates())
        
        self.assertEqual(len(results), 2)
        # received should be invalid
        received_result = next(r for r in results if "received" in r["title"])
        self.assertNotEqual(received_result["response"], "OK")
        self.assertEqual(received_result["response"], "CRITICAL")
        self.assertIn("Add <date date-type=\"received\">", received_result["advice"])
        # accepted should be valid
        accepted_result = next(r for r in results if "accepted" in r["title"])
        self.assertEqual(accepted_result["response"], "OK")
    
    def test_regular_article_missing_accepted(self):
        """Test that regular articles without accepted date are invalid."""
        xml = """
        <article article-type="research-article">
            <front>
                <article-meta>
                    <history>
                        <date date-type="received">
                            <day>15</day>
                            <month>03</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_required_dates())
        
        self.assertEqual(len(results), 2)
        # received should be valid
        received_result = next(r for r in results if "received" in r["title"])
        self.assertEqual(received_result["response"], "OK")
        # accepted should be invalid
        accepted_result = next(r for r in results if "accepted" in r["title"])
        self.assertNotEqual(accepted_result["response"], "OK")
        self.assertEqual(accepted_result["response"], "CRITICAL")
    
    def test_exempt_article_types(self):
        """Test that exempt article types don't require received/accepted."""
        for article_type in EXEMPT_ARTICLE_TYPES:
            xml = f"""
            <article article-type="{article_type}">
                <front>
                    <article-meta>
                        <history>
                            <date date-type="corrected">
                                <day>15</day>
                                <month>03</month>
                                <year>2024</year>
                            </date>
                        </history>
                    </article-meta>
                </front>
            </article>
            """
            tree = etree.fromstring(xml)
            validator = HistoryValidation(tree)
            results = list(validator.validate_required_dates())
            
            # Should have 2 results but both should be valid (not required)
            self.assertEqual(len(results), 2, f"Failed for article-type={article_type}")
            self.assertTrue(all(r["response"] == "OK" for r in results), f"Failed for article-type={article_type}")
    
    def test_retraction_without_required_dates(self):
        """Test specific case: retraction article type."""
        xml = """
        <article article-type="retraction">
            <front>
                <article-meta>
                    <history>
                        <date date-type="retracted">
                            <day>20</day>
                            <month>06</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_required_dates())
        
        self.assertEqual(len(results), 2)
        # Both should be valid since retraction is exempt
        self.assertTrue(all(r["response"] == "OK" for r in results))


class TestCompleteDateForCriticalTypes(TestCase):
    """Tests for Rule 6: Complete date requirements for critical types."""
    
    def test_received_with_complete_date(self):
        """Test that received date with complete date is valid."""
        xml = """
        <article>
            <front>
                <article-meta>
                    <history>
                        <date date-type="received">
                            <day>15</day>
                            <month>03</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_complete_date_for_critical_types())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
        self.assertEqual(results[0]["response"], "OK")
    
    def test_received_missing_day(self):
        """Test that received date without day is invalid."""
        xml = """
        <article>
            <front>
                <article-meta>
                    <history>
                        <date date-type="received">
                            <month>03</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_complete_date_for_critical_types())
        
        self.assertEqual(len(results), 1)
        self.assertNotEqual(results[0]["response"], "OK")
        self.assertEqual(results[0]["response"], "CRITICAL")
        self.assertIn("day", results[0]["advice"])
    
    def test_accepted_missing_month(self):
        """Test that accepted date without month is invalid."""
        xml = """
        <article>
            <front>
                <article-meta>
                    <history>
                        <date date-type="accepted">
                            <day>15</day>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_complete_date_for_critical_types())
        
        self.assertEqual(len(results), 1)
        self.assertNotEqual(results[0]["response"], "OK")
        self.assertEqual(results[0]["response"], "CRITICAL")
        self.assertIn("month", results[0]["advice"])
    
    def test_corrected_missing_year(self):
        """Test that corrected date without year is invalid."""
        xml = """
        <article>
            <front>
                <article-meta>
                    <history>
                        <date date-type="corrected">
                            <day>15</day>
                            <month>03</month>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_complete_date_for_critical_types())
        
        self.assertEqual(len(results), 1)
        self.assertNotEqual(results[0]["response"], "OK")
        self.assertEqual(results[0]["response"], "CRITICAL")
        self.assertIn("year", results[0]["advice"])
    
    def test_all_critical_types(self):
        """Test that all critical types are validated for completeness."""
        for date_type in COMPLETE_DATE_REQUIRED_TYPES:
            xml = f"""
            <article>
                <front>
                    <article-meta>
                        <history>
                            <date date-type="{date_type}">
                                <day>15</day>
                                <month>03</month>
                                <year>2024</year>
                            </date>
                        </history>
                    </article-meta>
                </front>
            </article>
            """
            tree = etree.fromstring(xml)
            validator = HistoryValidation(tree)
            results = list(validator.validate_complete_date_for_critical_types())
            
            self.assertEqual(len(results), 1, f"Failed for date-type={date_type}")
            self.assertEqual(results[0]["response"], "OK", f"Failed for date-type={date_type}")
    
    def test_non_critical_type_not_validated(self):
        """Test that non-critical types are not validated by this rule."""
        xml = """
        <article>
            <front>
                <article-meta>
                    <history>
                        <date date-type="preprint">
                            <year>2023</year>
                        </date>
                        <date date-type="pub">
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_complete_date_for_critical_types())
        
        # Should not return any results for non-critical types
        self.assertEqual(len(results), 0)
    
    def test_multiple_critical_dates_mixed(self):
        """Test validation of multiple critical dates with mixed completeness."""
        xml = """
        <article>
            <front>
                <article-meta>
                    <history>
                        <date date-type="received">
                            <day>15</day>
                            <month>03</month>
                            <year>2024</year>
                        </date>
                        <date date-type="accepted">
                            <month>05</month>
                            <year>2024</year>
                        </date>
                        <date date-type="corrected">
                            <day>10</day>
                            <month>07</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_complete_date_for_critical_types())
        
        self.assertEqual(len(results), 3)
        # received should be valid
        self.assertEqual(results[0]["response"], "OK")
        # accepted should be invalid (missing day)
        self.assertNotEqual(results[1]["response"], "OK")
        # corrected should be valid
        self.assertEqual(results[2]["response"], "OK")


class TestYearPresence(TestCase):
    """Tests for Rule 7: Year presence for all dates."""
    
    def test_date_with_year(self):
        """Test that date with year is valid."""
        xml = """
        <article>
            <front>
                <article-meta>
                    <history>
                        <date date-type="preprint">
                            <year>2023</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_year_presence())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
        self.assertEqual(results[0]["response"], "OK")
        self.assertEqual(results[0]["got_value"], "2023")
    
    def test_date_without_year(self):
        """Test that date without year is invalid."""
        xml = """
        <article>
            <front>
                <article-meta>
                    <history>
                        <date date-type="preprint">
                            <month>09</month>
                            <day>21</day>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_year_presence())
        
        self.assertEqual(len(results), 1)
        self.assertNotEqual(results[0]["response"], "OK")
        self.assertEqual(results[0]["response"], "CRITICAL")
        self.assertEqual(results[0]["got_value"], "missing")
        self.assertIn("Add <year>", results[0]["advice"])
    
    def test_date_with_empty_year(self):
        """Test that date with empty year is invalid."""
        xml = """
        <article>
            <front>
                <article-meta>
                    <history>
                        <date date-type="pub">
                            <year></year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_year_presence())
        
        self.assertEqual(len(results), 1)
        self.assertNotEqual(results[0]["response"], "OK")
        self.assertEqual(results[0]["response"], "CRITICAL")
    
    def test_multiple_dates_mixed_year_presence(self):
        """Test validation of multiple dates with mixed year presence."""
        xml = """
        <article>
            <front>
                <article-meta>
                    <history>
                        <date date-type="received">
                            <day>15</day>
                            <month>03</month>
                            <year>2024</year>
                        </date>
                        <date date-type="accepted">
                            <day>20</day>
                            <month>05</month>
                        </date>
                        <date date-type="pub">
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate_year_presence())
        
        self.assertEqual(len(results), 3)
        # received should be valid
        self.assertEqual(results[0]["response"], "OK")
        # accepted should be invalid (missing year)
        self.assertNotEqual(results[1]["response"], "OK")
        # pub should be valid
        self.assertEqual(results[2]["response"], "OK")


class TestFullValidation(TestCase):
    """Tests for complete validation workflow."""
    
    def test_valid_complete_example(self):
        """Test validation of a completely valid history."""
        xml = """
        <article article-type="research-article">
            <front>
                <article-meta>
                    <history>
                        <date date-type="received">
                            <day>15</day>
                            <month>03</month>
                            <year>2024</year>
                        </date>
                        <date date-type="accepted">
                            <day>12</day>
                            <month>05</month>
                            <year>2024</year>
                        </date>
                        <date date-type="preprint">
                            <day>21</day>
                            <month>09</month>
                            <year>2023</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate())
        
        # All results should be valid
        errors = [r for r in results if r["response"] != "OK"]
        self.assertEqual(len(errors), 0, f"Found errors: {errors}")
    
    def test_invalid_multiple_issues(self):
        """Test validation with multiple issues."""
        xml = """
        <article article-type="research-article">
            <front>
                <article-meta>
                    <history>
                        <date>
                            <day>15</day>
                            <month>03</month>
                            <year>2024</year>
                        </date>
                        <date date-type="invalid-type">
                            <month>05</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate())
        
        # Should have multiple errors
        errors = [r for r in results if r["response"] != "OK"]
        self.assertGreater(len(errors), 0)
        
        # Check for specific error types
        error_titles = [e["title"] for e in errors]
        self.assertIn("date-type presence", error_titles)
        self.assertIn("date-type value", error_titles)
        self.assertIn("required date: received", error_titles)
        self.assertIn("required date: accepted", error_titles)
    
    def test_retraction_article_valid(self):
        """Test validation of retraction article (exempt from received/accepted)."""
        xml = """
        <article article-type="retraction">
            <front>
                <article-meta>
                    <history>
                        <date date-type="retracted">
                            <day>20</day>
                            <month>06</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = HistoryValidation(tree)
        results = list(validator.validate())
        
        # All results should be valid (retraction is exempt)
        errors = [r for r in results if r["response"] != "OK"]
        self.assertEqual(len(errors), 0, f"Found errors: {errors}")
