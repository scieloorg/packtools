import unittest
from lxml import etree

from packtools.sps.validation.article_data_availability import (
    DataAvailabilityValidation,
)


class DataAvailabilityValidationTest(unittest.TestCase):
    def _assert_validation_keys(self, obtained, expected):
        """Helper method to check specific keys in the validation result"""
        keys_to_check = ["got_value", "expected_value", "advice", "response"]

        for k in keys_to_check:
            with self.subTest(k):
                self.assertEqual(expected[k], obtained[k])

    def test_validate_data_availability_fn_ok(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
                dtd-version="1.0" article-type="research-article" xml:lang="pt">
                    <back>
                        <fn-group>
                            <fn fn-type="data-availability" specific-use="data-available" id="fn1">
                                <label>Data Availability Statement</label>
                                <p>The data and code used to generate plots and perform statistical analyses have been
                                uploaded to the Open Science Framework archive: <ext-link ext-link-type="uri"
                                xlink:href="https://osf.io/jw6vg/?view_only=0335a15b6db3477f93d0ae636cdf3b4e">https://osf.io/j
                                w6vg/?view_only=0335a15b6db3477f93d0ae636cdf3b4e</ext-link>.</p>
                            </fn>
                        </fn-group>
                    </back>
                </article>
            """
        xmltree = etree.fromstring(xml)
        params = {
            "specific_use_list": [
                "data-available",
                "data-available-upon-request",
            ],
            "error_level": "ERROR",
        }

        validation = DataAvailabilityValidation(xmltree, params)
        validations = list(validation.validate_data_availability())

        # Check validation count - one exist validation + one mode validation
        self.assertEqual(2, len(validations))

        # Check the mode validation (should be the second one)
        mode_validation = validations[1]
        self.assertEqual("data availability mode", mode_validation["title"])
        self.assertEqual("OK", mode_validation["response"])
        self.assertEqual("data-available", mode_validation["got_value"])
        self.assertEqual(
            ["data-available", "data-available-upon-request"],
            mode_validation["expected_value"],
        )
        self.assertIsNone(mode_validation["advice"])

    def test_validate_data_availability_sec_ok(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
                dtd-version="1.0" article-type="research-article" xml:lang="pt">
                    <back>
                        <sec sec-type="data-availability" specific-use="data-available-upon-request">
                            <label>Data availability statement</label>
                            <p>Data will be available upon request.</p>
                        </sec>
                    </back>
                </article>
            """
        xmltree = etree.fromstring(xml)
        params = {
            "specific_use_list": [
                "data-available",
                "data-available-upon-request",
            ],
            "error_level": "ERROR",
        }

        validation = DataAvailabilityValidation(xmltree, params)
        validations = list(validation.validate_data_availability())

        # Check validation count - one exist validation + one mode validation
        self.assertEqual(2, len(validations))

        # Check the mode validation (should be the second one)
        mode_validation = validations[1]
        self.assertEqual("data availability mode", mode_validation["title"])
        self.assertEqual("OK", mode_validation["response"])
        self.assertEqual("data-available-upon-request", mode_validation["got_value"])
        self.assertEqual(
            ["data-available", "data-available-upon-request"],
            mode_validation["expected_value"],
        )
        self.assertIsNone(mode_validation["advice"])

    def test_validate_data_availability_both_sec_and_fn_ok(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
                dtd-version="1.0" article-type="research-article" xml:lang="pt">
                    <back>
                        <sec sec-type="data-availability" specific-use="data-available-upon-request">
                            <label>Data availability statement</label>
                            <p>Data will be available upon request.</p>
                        </sec>
                        <fn-group>
                            <fn fn-type="data-availability" specific-use="data-available" id="fn1">
                                <label>Data Availability Statement</label>
                                <p>The data and code used to generate plots and perform statistical analyses have been
                                uploaded to the Open Science Framework archive.</p>
                            </fn>
                        </fn-group>
                    </back>
                </article>
            """
        xmltree = etree.fromstring(xml)
        params = {
            "specific_use_list": [
                "data-available",
                "data-available-upon-request",
            ],
            "error_level": "ERROR",
        }

        validation = DataAvailabilityValidation(xmltree, params)
        validations = list(validation.validate_data_availability())

        # Check validation count - one exist validation + two mode validations (one for each item)
        self.assertEqual(3, len(validations))

        # Check the first mode validation (should be for one of the items)
        first_mode_validation = validations[1]
        self.assertEqual("data availability mode", first_mode_validation["title"])
        self.assertEqual("OK", first_mode_validation["response"])

        # Check the second mode validation (should be for the other item)
        second_mode_validation = validations[2]
        self.assertEqual("data availability mode", second_mode_validation["title"])
        self.assertEqual("OK", second_mode_validation["response"])

        # Verify we have one validation for each type
        specific_uses = [validations[1]["got_value"], validations[2]["got_value"]]
        self.assertIn("data-available", specific_uses)
        self.assertIn("data-available-upon-request", specific_uses)

    def test_validate_data_availability_fn_not_ok(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
                dtd-version="1.0" article-type="research-article" xml:lang="pt">
                    <back>
                        <fn-group>
                            <fn fn-type="data-availability" specific-use="data-available" id="fn1">
                                <label>Data Availability Statement</label>
                                <p>The data and code used to generate plots and perform statistical analyses have been
                                uploaded to the Open Science Framework archive.</p>
                            </fn>
                        </fn-group>
                    </back>
                </article>
            """
        xmltree = etree.fromstring(xml)
        params = {
            "specific_use_list": ["data-not-available", "uninformed"],
            "error_level": "ERROR",
        }

        validation = DataAvailabilityValidation(xmltree, params)
        validations = list(validation.validate_data_availability())

        # Check validation count - one exist validation + one mode validation
        self.assertEqual(2, len(validations))

        # Check the mode validation (should be the second one)
        mode_validation = validations[1]
        self.assertEqual("data availability mode", mode_validation["title"])
        self.assertEqual("ERROR", mode_validation["response"])
        self.assertEqual("data-available", mode_validation["got_value"])
        self.assertEqual(
            ["data-not-available", "uninformed"], mode_validation["expected_value"]
        )
        self.assertIn("Complete  specific-use=", mode_validation["advice"])

    def test_validate_data_availability_without_data_availability(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
                dtd-version="1.0" article-type="research-article" xml:lang="pt">
                    <back>
                    </back>
                </article>
            """
        xmltree = etree.fromstring(xml)
        params = {
            "specific_use_list": [
                "data-available",
                "data-available-upon-request",
            ],
            "error_level": "ERROR",
        }

        validation = DataAvailabilityValidation(xmltree, params)
        validations = list(validation.validate_data_availability())

        # Check validation count - should be one exist validation (no mode validation since no items exist)
        self.assertEqual(1, len(validations))

        # Check the existence validation
        exist_validation = validations[0]
        self.assertEqual("data availability statement", exist_validation["title"])
        self.assertEqual("ERROR", exist_validation["response"])
        self.assertIsNone(exist_validation["got_value"].get("tag"))
        self.assertIn("Mark in <article>", exist_validation["advice"])

    def test_validate_data_availability_article_type_optional(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
                dtd-version="1.0" article-type="case-report" xml:lang="pt">
                    <back>
                    </back>
                </article>
            """
        xmltree = etree.fromstring(xml)
        params = {
            "specific_use_list": [
                "data-available",
                "data-available-upon-request",
            ],
            "error_level": "ERROR",
        }

        validation = DataAvailabilityValidation(xmltree, params)
        validations = list(validation.validate_data_availability())

        # Check validation count - should be one exist validation (which should pass because it's optional)
        self.assertEqual(1, len(validations))

        # Check the existence validation
        exist_validation = validations[0]
        self.assertEqual("data availability statement", exist_validation["title"])
        self.assertEqual("OK", exist_validation["response"])
        self.assertIsNone(exist_validation["advice"])

    def test_validate_data_availability_article_type_unexpected_with_statement(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
                dtd-version="1.0" article-type="editorial" xml:lang="pt">
                    <back>
                        <sec sec-type="data-availability" specific-use="data-available-upon-request">
                            <label>Data availability statement</label>
                            <p>Data will be available upon request.</p>
                        </sec>
                    </back>
                </article>
            """
        xmltree = etree.fromstring(xml)
        params = {
            "specific_use_list": [
                "data-available",
                "data-available-upon-request",
            ],
            "error_level": "ERROR",
        }

        validation = DataAvailabilityValidation(xmltree, params)
        validations = list(validation.validate_data_availability())

        # Should have one existence validation (which should fail because it's unexpected)
        # and one mode validation (which should pass because the format is correct)
        self.assertEqual(2, len(validations))

        # Check the existence validation
        exist_validation = validations[0]
        self.assertEqual("data availability statement", exist_validation["title"])
        self.assertEqual("ERROR", exist_validation["response"])
        self.assertIn("Remove from <article>", exist_validation["advice"])

        # Check the mode validation
        mode_validation = validations[1]
        self.assertEqual("data availability mode", mode_validation["title"])
        self.assertEqual("OK", mode_validation["response"])

    def test_validate_data_availability_subarticle(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="pt">
                    <back>
                        <sec sec-type="data-availability" specific-use="data-available-upon-request">
                            <label>Data availability statement</label>
                            <p>Data will be available upon request.</p>
                        </sec>
                    </back>
                    <sub-article article-type="translation" id="TRen" xml:lang="en">
                        <back>
                            <fn-group>
                                <fn fn-type="data-availability" specific-use="data-available" id="fn1">
                                    <label>Data Availability Statement</label>
                                    <p>The data and code used to generate plots.</p>
                                </fn>
                            </fn-group>
                        </back>
                    </sub-article>
                </article>
            """
        xmltree = etree.fromstring(xml)
        params = {
            "specific_use_list": [
                "data-available",
                "data-available-upon-request",
            ],
            "error_level": "ERROR",
        }

        validation = DataAvailabilityValidation(xmltree, params)
        validations = list(validation.validate_data_availability())

        # Should have two existence validations (one for main article, one for sub-article)
        # and two mode validations (one for each item)
        self.assertEqual(4, len(validations))

        # Check that we have validations for both languages
        existence_validations = [
            v for v in validations if v["title"] == "data availability statement"
        ]
        languages = set()
        for v in existence_validations:
            data = v.get("data", {})
            if "parent_lang" in data:
                languages.add(data["parent_lang"])

        self.assertEqual({"pt", "en"}, languages)

    def test_validate_data_availability_body_section(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
                dtd-version="1.0" article-type="research-article" xml:lang="pt">
                    <body>
                        <sec sec-type="data-availability" specific-use="data-available-upon-request">
                            <label>Data availability statement</label>
                            <p>Data will be available upon request.</p>
                        </sec>
                    </body>
                </article>
            """
        xmltree = etree.fromstring(xml)
        params = {
            "specific_use_list": [
                "data-available",
                "data-available-upon-request",
            ],
            "error_level": "ERROR",
        }

        validation = DataAvailabilityValidation(xmltree, params)
        validations = list(validation.validate_data_availability())

        # Check validation count - one exist validation + one mode validation
        self.assertEqual(2, len(validations))

        # Check the mode validation (should be the second one)
        mode_validation = validations[1]
        self.assertEqual("data availability mode", mode_validation["title"])
        self.assertEqual("OK", mode_validation["response"])
        self.assertEqual("data-available-upon-request", mode_validation["got_value"])


if __name__ == "__main__":
    unittest.main()
