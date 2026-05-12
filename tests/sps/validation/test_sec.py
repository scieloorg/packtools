"""
Tests for SecValidation and XMLSecValidation classes according to SPS 1.10 specification.

Tests validation of <sec> elements including:
- <title> presence (accessibility requirement)
- @sec-type valid values
- @id requirement for transcript sections
- data-availability section presence for indexable article types
- Combined sec-type format (pipe separator)
- Non-combinable sec-types
- Content presence (<p> elements)
"""

import unittest
from lxml import etree

from packtools.sps.models.sec import ArticleSecs
from packtools.sps.validation.sec import SecValidation, XMLSecValidation


class TestSecValidationTitle(unittest.TestCase):
    """Test Rule 1: <title> is mandatory in <sec>."""

    def setUp(self):
        self.params = {
            "title_error_level": "CRITICAL",
            "sec_type_value_error_level": "ERROR",
            "transcript_id_error_level": "ERROR",
            "data_availability_error_level": "ERROR",
            "combined_format_error_level": "WARNING",
            "non_combinable_error_level": "WARNING",
            "content_error_level": "WARNING",
            "valid_sec_types": [
                "cases", "conclusions", "data-availability", "discussion",
                "intro", "materials", "methods", "results", "subjects",
                "supplementary-material", "transcript",
            ],
            "non_combinable_sec_types": [
                "data-availability", "supplementary-material", "transcript",
            ],
            "data_availability_required_article_types": [
                "data-article", "brief-report", "case-report",
                "rapid-communication", "research-article", "review-article",
            ],
        }

    def test_sec_with_title_passes(self):
        xml = """
        <article>
            <body>
                <sec sec-type="methods">
                    <title>Methods</title>
                    <p>Content here.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        validator = SecValidation(secs[0], self.params)
        result = validator.validate_title()
        self.assertEqual(result["response"], "OK")

    def test_sec_without_title_fails(self):
        xml = """
        <article>
            <body>
                <sec>
                    <p>Content without title.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        validator = SecValidation(secs[0], self.params)
        result = validator.validate_title()
        self.assertEqual(result["response"], "CRITICAL")
        self.assertIn("Add <title>", result["advice"])


class TestSecValidationSecTypeValue(unittest.TestCase):
    """Test Rule 2: @sec-type must have a valid value when present."""

    def setUp(self):
        self.params = {
            "title_error_level": "CRITICAL",
            "sec_type_value_error_level": "ERROR",
            "transcript_id_error_level": "ERROR",
            "data_availability_error_level": "ERROR",
            "combined_format_error_level": "WARNING",
            "non_combinable_error_level": "WARNING",
            "content_error_level": "WARNING",
            "valid_sec_types": [
                "cases", "conclusions", "data-availability", "discussion",
                "intro", "materials", "methods", "results", "subjects",
                "supplementary-material", "transcript",
            ],
            "non_combinable_sec_types": [
                "data-availability", "supplementary-material", "transcript",
            ],
            "data_availability_required_article_types": [],
        }

    def test_valid_sec_type_passes(self):
        xml = """
        <article>
            <body>
                <sec sec-type="methods">
                    <title>Methods</title>
                    <p>Content.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        validator = SecValidation(secs[0], self.params)
        result = validator.validate_sec_type_value()
        self.assertEqual(result["response"], "OK")

    def test_invalid_sec_type_fails(self):
        xml = """
        <article>
            <body>
                <sec sec-type="invalid-type">
                    <title>Something</title>
                    <p>Content.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        validator = SecValidation(secs[0], self.params)
        result = validator.validate_sec_type_value()
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], "invalid-type")

    def test_no_sec_type_returns_none(self):
        xml = """
        <article>
            <body>
                <sec>
                    <title>Free Section</title>
                    <p>Content.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        validator = SecValidation(secs[0], self.params)
        result = validator.validate_sec_type_value()
        self.assertIsNone(result)

    def test_combined_sec_type_valid(self):
        xml = """
        <article>
            <body>
                <sec sec-type="materials|methods">
                    <title>Materials and Methods</title>
                    <p>Content.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        validator = SecValidation(secs[0], self.params)
        result = validator.validate_sec_type_value()
        self.assertEqual(result["response"], "OK")


class TestSecValidationTranscriptId(unittest.TestCase):
    """Test Rule 3: <sec sec-type="transcript"> must have @id."""

    def setUp(self):
        self.params = {
            "title_error_level": "CRITICAL",
            "sec_type_value_error_level": "ERROR",
            "transcript_id_error_level": "ERROR",
            "data_availability_error_level": "ERROR",
            "combined_format_error_level": "WARNING",
            "non_combinable_error_level": "WARNING",
            "content_error_level": "WARNING",
            "valid_sec_types": [
                "cases", "conclusions", "data-availability", "discussion",
                "intro", "materials", "methods", "results", "subjects",
                "supplementary-material", "transcript",
            ],
            "non_combinable_sec_types": [
                "data-availability", "supplementary-material", "transcript",
            ],
            "data_availability_required_article_types": [],
        }

    def test_transcript_with_id_passes(self):
        xml = """
        <article>
            <body>
                <sec sec-type="transcript" id="TR1">
                    <title>Interview Transcript</title>
                    <p>Content.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        validator = SecValidation(secs[0], self.params)
        result = validator.validate_transcript_id()
        self.assertEqual(result["response"], "OK")

    def test_transcript_without_id_fails(self):
        xml = """
        <article>
            <body>
                <sec sec-type="transcript">
                    <title>Interview Transcript</title>
                    <p>Content.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        validator = SecValidation(secs[0], self.params)
        result = validator.validate_transcript_id()
        self.assertEqual(result["response"], "ERROR")
        self.assertIn("Add @id", result["advice"])

    def test_non_transcript_returns_none(self):
        xml = """
        <article>
            <body>
                <sec sec-type="methods">
                    <title>Methods</title>
                    <p>Content.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        validator = SecValidation(secs[0], self.params)
        result = validator.validate_transcript_id()
        self.assertIsNone(result)


class TestSecValidationCombinedFormat(unittest.TestCase):
    """Test Rule 5: Combined sec-types must use pipe separator."""

    def setUp(self):
        self.params = {
            "title_error_level": "CRITICAL",
            "sec_type_value_error_level": "ERROR",
            "transcript_id_error_level": "ERROR",
            "data_availability_error_level": "ERROR",
            "combined_format_error_level": "WARNING",
            "non_combinable_error_level": "WARNING",
            "content_error_level": "WARNING",
            "valid_sec_types": [
                "cases", "conclusions", "data-availability", "discussion",
                "intro", "materials", "methods", "results", "subjects",
                "supplementary-material", "transcript",
            ],
            "non_combinable_sec_types": [
                "data-availability", "supplementary-material", "transcript",
            ],
            "data_availability_required_article_types": [],
        }

    def test_pipe_separator_returns_none(self):
        xml = """
        <article>
            <body>
                <sec sec-type="materials|methods">
                    <title>Materials and Methods</title>
                    <p>Content.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        validator = SecValidation(secs[0], self.params)
        result = validator.validate_combined_format()
        self.assertIsNone(result)

    def test_space_separator_fails(self):
        xml = """
        <article>
            <body>
                <sec sec-type="materials methods">
                    <title>Materials and Methods</title>
                    <p>Content.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        validator = SecValidation(secs[0], self.params)
        result = validator.validate_combined_format()
        self.assertEqual(result["response"], "WARNING")

    def test_comma_separator_fails(self):
        xml = """
        <article>
            <body>
                <sec sec-type="materials,methods">
                    <title>Materials and Methods</title>
                    <p>Content.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        validator = SecValidation(secs[0], self.params)
        result = validator.validate_combined_format()
        self.assertEqual(result["response"], "WARNING")

    def test_single_sec_type_returns_none(self):
        xml = """
        <article>
            <body>
                <sec sec-type="methods">
                    <title>Methods</title>
                    <p>Content.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        validator = SecValidation(secs[0], self.params)
        result = validator.validate_combined_format()
        self.assertIsNone(result)


class TestSecValidationNonCombinable(unittest.TestCase):
    """Test Rule 6: transcript, supplementary-material, data-availability cannot be combined."""

    def setUp(self):
        self.params = {
            "title_error_level": "CRITICAL",
            "sec_type_value_error_level": "ERROR",
            "transcript_id_error_level": "ERROR",
            "data_availability_error_level": "ERROR",
            "combined_format_error_level": "WARNING",
            "non_combinable_error_level": "WARNING",
            "content_error_level": "WARNING",
            "valid_sec_types": [
                "cases", "conclusions", "data-availability", "discussion",
                "intro", "materials", "methods", "results", "subjects",
                "supplementary-material", "transcript",
            ],
            "non_combinable_sec_types": [
                "data-availability", "supplementary-material", "transcript",
            ],
            "data_availability_required_article_types": [],
        }

    def test_combined_transcript_fails(self):
        xml = """
        <article>
            <body>
                <sec sec-type="transcript|methods">
                    <title>Transcript and Methods</title>
                    <p>Content.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        validator = SecValidation(secs[0], self.params)
        result = validator.validate_non_combinable()
        self.assertEqual(result["response"], "WARNING")

    def test_combined_data_availability_fails(self):
        xml = """
        <article>
            <body>
                <sec sec-type="data-availability|methods">
                    <title>Data Availability</title>
                    <p>Content.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        validator = SecValidation(secs[0], self.params)
        result = validator.validate_non_combinable()
        self.assertEqual(result["response"], "WARNING")

    def test_combined_valid_types_returns_none(self):
        xml = """
        <article>
            <body>
                <sec sec-type="materials|methods">
                    <title>Materials and Methods</title>
                    <p>Content.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        validator = SecValidation(secs[0], self.params)
        result = validator.validate_non_combinable()
        self.assertIsNone(result)

    def test_no_pipe_returns_none(self):
        xml = """
        <article>
            <body>
                <sec sec-type="transcript" id="TR1">
                    <title>Transcript</title>
                    <p>Content.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        validator = SecValidation(secs[0], self.params)
        result = validator.validate_non_combinable()
        self.assertIsNone(result)


class TestSecValidationContent(unittest.TestCase):
    """Test Rule 7: <sec> should contain at least one <p>."""

    def setUp(self):
        self.params = {
            "title_error_level": "CRITICAL",
            "sec_type_value_error_level": "ERROR",
            "transcript_id_error_level": "ERROR",
            "data_availability_error_level": "ERROR",
            "combined_format_error_level": "WARNING",
            "non_combinable_error_level": "WARNING",
            "content_error_level": "WARNING",
            "valid_sec_types": [
                "cases", "conclusions", "data-availability", "discussion",
                "intro", "materials", "methods", "results", "subjects",
                "supplementary-material", "transcript",
            ],
            "non_combinable_sec_types": [
                "data-availability", "supplementary-material", "transcript",
            ],
            "data_availability_required_article_types": [],
        }

    def test_sec_with_paragraph_passes(self):
        xml = """
        <article>
            <body>
                <sec sec-type="methods">
                    <title>Methods</title>
                    <p>Method description.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        validator = SecValidation(secs[0], self.params)
        result = validator.validate_content()
        self.assertEqual(result["response"], "OK")

    def test_sec_without_paragraph_fails(self):
        xml = """
        <article>
            <body>
                <sec sec-type="methods">
                    <title>Methods</title>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        validator = SecValidation(secs[0], self.params)
        result = validator.validate_content()
        self.assertEqual(result["response"], "WARNING")
        self.assertIn("Add at least one <p>", result["advice"])


class TestXMLSecValidationDataAvailability(unittest.TestCase):
    """Test Rule 4: data-availability section required for certain article types."""

    def setUp(self):
        self.params = {
            "title_error_level": "CRITICAL",
            "sec_type_value_error_level": "ERROR",
            "transcript_id_error_level": "ERROR",
            "data_availability_error_level": "ERROR",
            "combined_format_error_level": "WARNING",
            "non_combinable_error_level": "WARNING",
            "content_error_level": "WARNING",
            "valid_sec_types": [
                "cases", "conclusions", "data-availability", "discussion",
                "intro", "materials", "methods", "results", "subjects",
                "supplementary-material", "transcript",
            ],
            "non_combinable_sec_types": [
                "data-availability", "supplementary-material", "transcript",
            ],
            "data_availability_required_article_types": [
                "data-article", "brief-report", "case-report",
                "rapid-communication", "research-article", "review-article",
            ],
        }

    def test_research_article_with_data_availability_passes(self):
        xml = """
        <article article-type="research-article">
            <body>
                <sec sec-type="intro">
                    <title>Introduction</title>
                    <p>Intro content.</p>
                </sec>
                <sec sec-type="data-availability" specific-use="data-available-on-request">
                    <title>Data Availability</title>
                    <p>Data available on request.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        validator = XMLSecValidation(tree, self.params)
        results = [r for r in validator.validate_data_availability_presence()
                   if r is not None]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_research_article_without_data_availability_fails(self):
        xml = """
        <article article-type="research-article">
            <body>
                <sec sec-type="intro">
                    <title>Introduction</title>
                    <p>Intro content.</p>
                </sec>
                <sec sec-type="methods">
                    <title>Methods</title>
                    <p>Methods content.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        validator = XMLSecValidation(tree, self.params)
        results = [r for r in validator.validate_data_availability_presence()
                   if r is not None]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")

    def test_editorial_no_data_availability_check(self):
        xml = """
        <article article-type="editorial">
            <body>
                <sec>
                    <title>Editorial</title>
                    <p>Editorial content.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        validator = XMLSecValidation(tree, self.params)
        results = list(validator.validate_data_availability_presence())
        self.assertEqual(len(results), 0)

    def test_case_report_with_data_availability_passes(self):
        xml = """
        <article article-type="case-report">
            <body>
                <sec sec-type="cases">
                    <title>Case Study</title>
                    <p>Case content.</p>
                </sec>
                <sec sec-type="data-availability" specific-use="data-available">
                    <title>Data Availability</title>
                    <p>Data available.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        validator = XMLSecValidation(tree, self.params)
        results = [r for r in validator.validate_data_availability_presence()
                   if r is not None]
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")


class TestXMLSecValidationIntegration(unittest.TestCase):
    """Integration tests for XMLSecValidation.validate()."""

    def setUp(self):
        self.params = {
            "title_error_level": "CRITICAL",
            "sec_type_value_error_level": "ERROR",
            "transcript_id_error_level": "ERROR",
            "data_availability_error_level": "ERROR",
            "combined_format_error_level": "WARNING",
            "non_combinable_error_level": "WARNING",
            "content_error_level": "WARNING",
            "valid_sec_types": [
                "cases", "conclusions", "data-availability", "discussion",
                "intro", "materials", "methods", "results", "subjects",
                "supplementary-material", "transcript",
            ],
            "non_combinable_sec_types": [
                "data-availability", "supplementary-material", "transcript",
            ],
            "data_availability_required_article_types": [
                "data-article", "brief-report", "case-report",
                "rapid-communication", "research-article", "review-article",
            ],
        }

    def test_valid_complete_article(self):
        xml = """
        <article article-type="research-article">
            <body>
                <sec sec-type="intro">
                    <title>Introduction</title>
                    <p>Introduction content.</p>
                </sec>
                <sec sec-type="materials|methods">
                    <title>Materials and Methods</title>
                    <p>Methods content.</p>
                </sec>
                <sec sec-type="results">
                    <title>Results</title>
                    <p>Results content.</p>
                </sec>
                <sec sec-type="discussion">
                    <title>Discussion</title>
                    <p>Discussion content.</p>
                </sec>
                <sec sec-type="conclusions">
                    <title>Conclusions</title>
                    <p>Conclusions content.</p>
                </sec>
                <sec sec-type="data-availability" specific-use="data-available-on-request">
                    <title>Data Availability</title>
                    <p>Data available on request.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        validator = XMLSecValidation(tree, self.params)
        results = [r for r in validator.validate() if r is not None]

        # All results should be OK
        for result in results:
            self.assertEqual(result["response"], "OK", f"Failed: {result['title']} - {result.get('advice')}")

    def test_sec_with_subsec(self):
        xml = """
        <article article-type="editorial">
            <body>
                <sec sec-type="methods">
                    <title>Methodology</title>
                    <sec>
                        <title>Methodology in Science</title>
                        <p>Lorem ipsum dolor sit amet.</p>
                    </sec>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        validator = XMLSecValidation(tree, self.params)
        results = [r for r in validator.validate() if r is not None]

        # Parent sec has no direct <p> (only subsec), but subsec has <p>
        # Filter only "sec content" results
        content_results = [r for r in results if r["title"] == "sec content"]
        # The parent sec should have WARNING (no direct p), subsec should be OK
        parent_content = content_results[0]
        self.assertEqual(parent_content["response"], "WARNING")
        subsec_content = content_results[1]
        self.assertEqual(subsec_content["response"], "OK")

    def test_transcript_sec_without_id_fails(self):
        xml = """
        <article article-type="editorial">
            <body>
                <sec sec-type="transcript">
                    <title>Interview</title>
                    <p>Content.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        validator = XMLSecValidation(tree, self.params)
        results = [r for r in validator.validate() if r is not None]

        # Find the transcript_id result
        transcript_results = [r for r in results if r["title"] == "transcript id"]
        self.assertEqual(len(transcript_results), 1)
        self.assertEqual(transcript_results[0]["response"], "ERROR")


class TestSecModel(unittest.TestCase):
    """Test the ArticleSecs model."""

    def test_all_secs_returns_all_sections(self):
        xml = """
        <article article-type="research-article">
            <body>
                <sec sec-type="intro">
                    <title>Introduction</title>
                    <p>Content.</p>
                </sec>
                <sec sec-type="methods">
                    <title>Methods</title>
                    <p>Content.</p>
                    <sec>
                        <title>Subsection</title>
                        <p>Sub content.</p>
                    </sec>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        secs = list(ArticleSecs(tree).all_secs)
        self.assertEqual(len(secs), 3)

    def test_first_level_body_secs(self):
        xml = """
        <article article-type="research-article">
            <body>
                <sec sec-type="intro">
                    <title>Introduction</title>
                    <p>Content.</p>
                </sec>
                <sec sec-type="methods">
                    <title>Methods</title>
                    <p>Content.</p>
                    <sec>
                        <title>Subsection</title>
                        <p>Sub content.</p>
                    </sec>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        first_level = list(ArticleSecs(tree).first_level_body_secs)
        self.assertEqual(len(first_level), 2)

    def test_body_sec_types(self):
        xml = """
        <article article-type="research-article">
            <body>
                <sec sec-type="intro">
                    <title>Introduction</title>
                    <p>Content.</p>
                </sec>
                <sec sec-type="methods">
                    <title>Methods</title>
                    <p>Content.</p>
                </sec>
                <sec>
                    <title>Free Section</title>
                    <p>Content.</p>
                </sec>
            </body>
        </article>
        """
        tree = etree.fromstring(xml.encode())
        sec_types = ArticleSecs(tree).body_sec_types
        self.assertEqual(sec_types, ["intro", "methods"])


if __name__ == "__main__":
    unittest.main()
