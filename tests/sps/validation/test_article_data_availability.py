import unittest
from lxml import etree

from packtools.sps.validation.article_data_availability import (
    DataAvailabilityValidation,
)


class DataAvailabilityTest(unittest.TestCase):

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
            "data_availability_specific_use": [
                "data-available",
                "data-available-upon-request",
            ],
            "data_availability_error_level": "ERROR",
        }
        expected = {
            "got_value": "data-available",
            "expected_value": ["data-available", "data-available-upon-request"],
            "advice": None,
            "response": "OK",
        }
        obtained = list(
            DataAvailabilityValidation(xmltree, params).validate_data_availability()
        )
        self.assertEqual(2, len(obtained))
        self._assert_validation_keys(obtained[1], expected)

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
            "data_availability_specific_use": [
                "data-available",
                "data-available-upon-request",
            ],
            "data_availability_error_level": "ERROR",
        }
        expected = {
            "got_value": "data-available-upon-request",
            "expected_value": ["data-available", "data-available-upon-request"],
            "advice": None,
            "response": "OK",
        }
        obtained = list(
            DataAvailabilityValidation(xmltree, params).validate_data_availability()
        )
        self.assertEqual(2, len(obtained))
        self._assert_validation_keys(obtained[1], expected)

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
            "data_availability_specific_use": ["data-not-available", "uninformed"],
            "data_availability_error_level": "ERROR",
        }
        expected = {
            "got_value": "data-available",
            "expected_value": 'one of ["data-not-available", "uninformed"]',
            "advice": 'Complete  specific-use="" in <fn fn-type="data-availability" specific-use=""> with valid value: ["data-not-available", "uninformed"]',
            "response": "ERROR",
        }
        obtained = list(
            DataAvailabilityValidation(xmltree, params).validate_data_availability()
        )
        self.assertEqual(2, len(obtained))
        self._assert_validation_keys(obtained[1], expected)

    def test_validate_data_availability_sec_not_ok(self):
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
            "data_availability_specific_use": ["data-not-available", "uninformed"],
            "data_availability_error_level": "ERROR",
        }
        expected = {
            "got_value": "data-available-upon-request",
            "expected_value": 'one of ["data-not-available", "uninformed"]',
            "advice": 'Complete  specific-use="" in <sec sec-type="data-availability" specific-use=""> with valid value: ["data-not-available", "uninformed"]',
            "response": "ERROR",
        }
        obtained = list(
            DataAvailabilityValidation(xmltree, params).validate_data_availability()
        )
        self.assertEqual(2, len(obtained))
        self._assert_validation_keys(obtained[1], expected)

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
            "data_availability_specific_use": [
                "data-available",
                "data-available-upon-request",
            ],
            "data_availability_error_level": "ERROR",
        }
        expected = {
            "got_value": None,
            "expected_value": {'parent': 'article', 'parent_id': None, 'parent_lang': 'pt', 'parent_article_type': 'research-article', 'original_article_type': 'research-article'},
            "advice": '''Mark in <article> the data availability statement in footnote with <fn fn-type="data-availability" specific-use=""> or in text with <sec sec-type="data_availability" specific-use="">. And complete specific-use="" with valid value: ["data-available", "data-available-upon-request"]''',
            "response": "ERROR",
        }
        obtained = list(
            DataAvailabilityValidation(xmltree, params).validate_data_availability()
        )
        self._assert_validation_keys(obtained[0], expected)

    def test_validate_data_availability_subarticle_fn_ok(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
                    <sub-article article-type="translation" id="TRen" xml:lang="en">
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
                    </sub-article>
                </article>
            """
        xmltree = etree.fromstring(xml)
        params = {
            "data_availability_specific_use": [
                "data-available",
                "data-available-upon-request",
            ],
            "data_availability_error_level": "ERROR",
        }
        expected = {
            "got_value": "data-available",
            "expected_value": ["data-available", "data-available-upon-request"],
            "advice": None,
            "response": "OK",
        }
        obtained = list(
            DataAvailabilityValidation(xmltree, params).validate_data_availability()
        )
        self.assertEqual(3, len(obtained))
        self._assert_validation_keys(obtained[-1], expected)

    def test_validate_data_availability_subarticle_missing_data_availability_statement(self):
        self.maxDiff = None
        xml = """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article"><back>
                <fn-group>
                            <fn fn-type="data-availability" specific-use="data-available" id="fn1">
                                <label>Data Availability Statement</label>
                                <p>The data and code used to generate plots and perform statistical analyses have been
                                uploaded to the Open Science Framework archive: <ext-link ext-link-type="uri"
                                xlink:href="https://osf.io/jw6vg/?view_only=0335a15b6db3477f93d0ae636cdf3b4e">https://osf.io/j
                                w6vg/?view_only=0335a15b6db3477f93d0ae636cdf3b4e</ext-link>.</p>
                            </fn>
                        </fn-group></back>
                    <sub-article article-type="translation" id="TRen" xml:lang="en">
                    </sub-article>
                </article>
            """
        xmltree = etree.fromstring(xml)
        params = {
            "data_availability_specific_use": [
                "data-available",
                "data-available-upon-request",
            ],
            "data_availability_error_level": "ERROR",
        }
        expected = {
            "got_value": "data-available",
            "expected_value": ["data-available", "data-available-upon-request"],
            "advice": None,
            "response": "OK",
        }
        obtained = list(
            DataAvailabilityValidation(xmltree, params).validate_data_availability_exist()
        )
        self.assertEqual(2, len(obtained))


if __name__ == "__main__":
    unittest.main()
