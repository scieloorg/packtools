"""
Tests for <response> element validations according to SPS 1.10.

This module tests the validation rules for the <response> element,
ensuring compliance with the SPS 1.10 specification.
"""

from unittest import TestCase
from lxml import etree

from packtools.sps.validation.response import ResponseValidation


class TestResponseTypePresence(TestCase):
    """Tests for Rule 1: @response-type presence."""

    def test_response_type_present(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="reply" xml:lang="en" id="S1">
                <front-stub/>
                <body><p>Response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_response_type_presence())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_response_type_missing(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response xml:lang="en" id="S1">
                <front-stub/>
                <body><p>Response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_response_type_presence())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")

    def test_response_type_empty(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="" xml:lang="en" id="S1">
                <front-stub/>
                <body><p>Response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_response_type_presence())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")

    def test_response_type_whitespace_only(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="   " xml:lang="en" id="S1">
                <front-stub/>
                <body><p>Response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_response_type_presence())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")


class TestResponseTypeValue(TestCase):
    """Tests for Rule 2: @response-type value must be 'reply'."""

    def test_response_type_reply(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="reply" xml:lang="en" id="S1">
                <front-stub/>
                <body><p>Response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_response_type_value())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_response_type_wrong_value(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="answer" xml:lang="en" id="S1">
                <front-stub/>
                <body><p>Response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_response_type_value())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")
        self.assertEqual(results[0]["got_value"], "answer")

    def test_response_type_uppercase(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="Reply" xml:lang="en" id="S1">
                <front-stub/>
                <body><p>Response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_response_type_value())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")
        self.assertEqual(results[0]["got_value"], "Reply")

    def test_response_type_missing_skips_value_check(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response xml:lang="en" id="S1">
                <front-stub/>
                <body><p>Response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_response_type_value())

        self.assertEqual(len(results), 0)


class TestXmlLangPresence(TestCase):
    """Tests for Rule 3: @xml:lang presence."""

    def test_xml_lang_present(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="reply" xml:lang="en" id="S1">
                <front-stub/>
                <body><p>Response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_xml_lang_presence())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_xml_lang_missing(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="reply" id="S1">
                <front-stub/>
                <body><p>Response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_xml_lang_presence())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")

    def test_xml_lang_empty(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="reply" xml:lang="" id="S1">
                <front-stub/>
                <body><p>Response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_xml_lang_presence())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")


class TestIdPresence(TestCase):
    """Tests for Rule 4: @id presence."""

    def test_id_present(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="reply" xml:lang="en" id="S1">
                <front-stub/>
                <body><p>Response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_id_presence())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_id_missing(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="reply" xml:lang="en">
                <front-stub/>
                <body><p>Response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_id_presence())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")

    def test_id_empty(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="reply" xml:lang="en" id="">
                <front-stub/>
                <body><p>Response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_id_presence())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")


class TestIdUniqueness(TestCase):
    """Tests for Rule 5: @id uniqueness."""

    def test_unique_ids(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="reply" xml:lang="en" id="S1">
                <front-stub/>
                <body><p>First response</p></body>
            </response>
            <response response-type="reply" xml:lang="en" id="S2">
                <front-stub/>
                <body><p>Second response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_id_uniqueness())

        self.assertEqual(len(results), 0)

    def test_duplicate_ids(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="reply" xml:lang="en" id="S1">
                <front-stub/>
                <body><p>First response</p></body>
            </response>
            <response response-type="reply" xml:lang="en" id="S1">
                <front-stub/>
                <body><p>Second response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_id_uniqueness())

        self.assertEqual(len(results), 2)
        for r in results:
            self.assertEqual(r["response"], "ERROR")
            self.assertEqual(r["got_value"], "S1")

    def test_three_duplicate_ids(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="reply" xml:lang="en" id="S1">
                <front-stub/>
                <body><p>First</p></body>
            </response>
            <response response-type="reply" xml:lang="en" id="S1">
                <front-stub/>
                <body><p>Second</p></body>
            </response>
            <response response-type="reply" xml:lang="en" id="S1">
                <front-stub/>
                <body><p>Third</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_id_uniqueness())

        self.assertEqual(len(results), 3)

    def test_no_responses_no_errors(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_id_uniqueness())

        self.assertEqual(len(results), 0)

    def test_missing_ids_not_counted_as_duplicates(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="reply" xml:lang="en">
                <front-stub/>
                <body><p>First</p></body>
            </response>
            <response response-type="reply" xml:lang="en">
                <front-stub/>
                <body><p>Second</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_id_uniqueness())

        self.assertEqual(len(results), 0)


class TestFrontStubPresence(TestCase):
    """Tests for Rule 6: <front-stub> presence."""

    def test_front_stub_present(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="reply" xml:lang="en" id="S1">
                <front-stub/>
                <body><p>Response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_front_stub_presence())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_front_stub_missing(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="reply" xml:lang="en" id="S1">
                <body><p>Response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_front_stub_presence())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "WARNING")


class TestBodyPresence(TestCase):
    """Tests for Rule 7: <body> presence."""

    def test_body_present(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="reply" xml:lang="en" id="S1">
                <front-stub/>
                <body><p>Response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_body_presence())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_body_missing(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="reply" xml:lang="en" id="S1">
                <front-stub/>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate_body_presence())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "WARNING")


class TestMultipleResponses(TestCase):
    """Tests with multiple response elements."""

    def test_multiple_valid_responses(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="reply" xml:lang="en" id="S1">
                <front-stub/>
                <body><p>First response</p></body>
            </response>
            <response response-type="reply" xml:lang="en" id="S2">
                <front-stub/>
                <body><p>Second response</p></body>
            </response>
            <response response-type="reply" xml:lang="en" id="S3">
                <front-stub/>
                <body><p>Third response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate())

        ok_results = [r for r in results if r["response"] == "OK"]
        error_results = [r for r in results if r["response"] != "OK"]
        self.assertEqual(len(error_results), 0)
        # 7 rules × 3 responses = 21, minus uniqueness (0 issues) = at least 18
        self.assertGreater(len(ok_results), 0)

    def test_no_response_elements_yields_nothing(self):
        xml = """
        <article article-type="research-article" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate())

        self.assertEqual(len(results), 0)


class TestResponseInSubArticle(TestCase):
    """Tests for response elements within sub-article."""

    def test_response_in_sub_article(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <sub-article article-type="translation" xml:lang="pt" id="sub1">
                <front-stub/>
                <body><p>Translated content</p></body>
                <response response-type="reply" xml:lang="pt" id="S1-pt">
                    <front-stub/>
                    <body><p>Resposta em português.</p></body>
                </response>
            </sub-article>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate())

        error_results = [r for r in results if r["response"] != "OK"]
        self.assertEqual(len(error_results), 0)

        # Verify parent info points to sub-article
        for r in results:
            if r["response"] == "OK":
                self.assertEqual(r["parent"], "sub-article")
                self.assertEqual(r["parent_id"], "sub1")


class TestValidateAll(TestCase):
    """Tests for the validate() method that runs all validations."""

    def test_valid_response(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="reply" xml:lang="en" id="S1">
                <front-stub>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Smith</surname>
                                <given-names>John</given-names>
                            </name>
                        </contrib>
                    </contrib-group>
                </front-stub>
                <body><p>Response content.</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate())

        error_results = [r for r in results if r["response"] != "OK"]
        self.assertEqual(len(error_results), 0)

    def test_response_all_attributes_missing(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response>
                <front-stub/>
                <body><p>Response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate())

        critical_results = [r for r in results if r["response"] == "CRITICAL"]
        # Missing: @response-type, @xml:lang, @id = 3 CRITICAL
        self.assertEqual(len(critical_results), 3)

    def test_response_with_all_errors(self):
        """Response with wrong type, missing lang, missing id, no front-stub, no body."""
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="answer">
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        validator = ResponseValidation(tree)
        results = list(validator.validate())

        # @response-type value error (ERROR), @xml:lang missing (CRITICAL),
        # @id missing (CRITICAL), no front-stub (WARNING), no body (WARNING)
        error_results = [r for r in results if r["response"] != "OK"]
        self.assertGreaterEqual(len(error_results), 4)


class TestCustomErrorLevels(TestCase):
    """Tests for custom error levels via params."""

    def test_custom_error_level_for_response_type(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response xml:lang="en" id="S1">
                <front-stub/>
                <body><p>Response</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        params = {"response_type_presence_error_level": "WARNING"}
        validator = ResponseValidation(tree, params)
        results = list(validator.validate_response_type_presence())

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "WARNING")

    def test_custom_error_level_for_id_uniqueness(self):
        xml = """
        <article article-type="letter" xml:lang="en">
            <front><article-meta/></front>
            <body><p>Content</p></body>
            <response response-type="reply" xml:lang="en" id="S1">
                <front-stub/>
                <body><p>First</p></body>
            </response>
            <response response-type="reply" xml:lang="en" id="S1">
                <front-stub/>
                <body><p>Second</p></body>
            </response>
        </article>
        """
        tree = etree.fromstring(xml)
        params = {"id_uniqueness_error_level": "CRITICAL"}
        validator = ResponseValidation(tree, params)
        results = list(validator.validate_id_uniqueness())

        for r in results:
            self.assertEqual(r["response"], "CRITICAL")
