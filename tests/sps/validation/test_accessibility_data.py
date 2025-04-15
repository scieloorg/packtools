import unittest
from lxml import etree
from packtools.sps.validation.accessibility_data import XMLAccessibilityDataValidation


class TestAccessibilityDataValidation(unittest.TestCase):

    def setUp(self):
        self.params = {
            "alt_text_exist_error_level": "WARNING",
            "alt_text_content_error_level": "CRITICAL",
            "long_desc_exist_error_level": "WARNING",
            "long_desc_content_error_level": "CRITICAL",
            "transcript_error_level": "WARNING",
            "content_type_error_level": "CRITICAL",
            "speaker_speech_error_level": "WARNING",
            "structure_error_level": "CRITICAL",
            "content_types": ["machine-generated"],
        }

    def test_validate_alt_text_failure(self):
        """Fails when <alt-text> exceeds 120 characters."""
        xml_content = """
        <body>
            <media>
                <alt-text>This is an alternative text that is intentionally made longer than one hundred and twenty characters to ensure that the validation fails as expected.</alt-text>
            </media>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        response = results[0]
        self.assertEqual(response["response"], "CRITICAL")
        expected_advice = f"alt-text has {len(response['got_value'])} characters in <alt-text>This is an alternative text that is intentionally made longer than one hundred and twenty characters to ensure that the validation fails as expected.</alt-text>. Provide text with up to 120 characters."
        self.assertEqual(response["advice"], expected_advice)

    def test_validate_long_desc_failure(self):
        """Fails when <long-desc> is shorter than 120 characters."""
        xml_content = """
        <body>
            <media>
                <long-desc>Short description.</long-desc>
            </media>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())
        response = results[1]
        self.assertEqual(response["response"], "CRITICAL")
        expected_advice = f"long-desc has {len(response['got_value'])} characters in <long-desc>Short description.</long-desc>. Provide text with more than to 120 characters."
        self.assertEqual(response["advice"], expected_advice)

    def test_validate_transcript_failure(self):
        """Fails when a transcript is missing."""
        xml_content = """
        <body>
            <media>
                <alt-text>Valid alternative text.</alt-text>
                <long-desc>{}</long-desc>
            </media>
        </body>
        """.format("x" * 130)
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())
        response = results[4]

        self.assertEqual(response["response"], "WARNING")
        expected_advice = (
            "The transcript is missing in the media element. Add a <sec sec-type='transcript'> section to provide accessible text alternatives. "
            "Refer to SPS 1.10 docs for details."
        )
        self.assertEqual(response["advice"], expected_advice)

    def test_validate_content_type_failure(self):
        """Fails when @content-type is not an allowed value."""
        xml_content = """
        <body>
            <media>
                <alt-text content-type="manual">Valid alternative text.</alt-text>
            </media>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        response = results[1]
        self.assertEqual(response["response"], "CRITICAL")
        expected_advice = ('The value \'manual\' is invalid in <alt-text content-type="manual">Valid alternative text.</alt-text>. '
                           'Replace it with one of the accepted values: [\'machine-generated\'].')
        self.assertEqual(response["advice"], expected_advice)

    def test_validate_speaker_and_speech_failure(self):
        """Fails when no <speaker> and <speech> elements are present."""
        xml_content = """
        <body>
            <media>
                <sec sec-type="transcript">
                    <!-- Speaker and Speech missing -->
                </sec>
            </media>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        response = results[3]
        self.assertEqual(response["response"], "WARNING")
        expected_advice = (
            "Dialog elements are missing in the <sec sec-type='transcript'> section. Use <speaker> and <speech> to represent the dialogue. "
            "Refer to SPS 1.10 docs for details."
        )
        self.assertEqual(response["advice"], expected_advice)

    def test_validate_structure_failure(self):
        """Fails when accessibility data is in an invalid tag."""
        xml_content = """
        <body>
            <invalid>
                <alt-text>Valid alt text</alt-text>
                <long-desc>""" + "d" * 130 + """</long-desc>
            </invalid>
        </body>
        """
        xml_node = etree.fromstring(xml_content)
        validator = XMLAccessibilityDataValidation(xml_node, self.params)
        results = list(validator.validate())

        structure_res = [res for res in results if res["title"] == "structure"]
        self.assertEqual(len(structure_res), 1)
        self.assertEqual(structure_res[0]["response"], "CRITICAL")
        self.assertEqual(
            structure_res[0]["advice"],
            "Accessibility data is located in an invalid element: <invalid>. "
            "Use one of the valid elements: ('graphic', 'inline-graphic', 'media', 'inline-media'). "
            "Refer to SPS 1.10 docs for details.")


if __name__ == "__main__":
    unittest.main()
