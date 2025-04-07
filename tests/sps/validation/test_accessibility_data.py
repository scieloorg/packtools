import unittest
from lxml import etree
from packtools.sps.validation.accessibility_data import AccessibilityDataValidation


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
            "media_structure_error_level": "CRITICAL",
            "content_types": ["machine-generated"],
        }

    def test_validate_alt_text_failure(self):
        """Fails when <alt-text> exceeds 120 characters."""
        xml_content = """
        <media xmlns:xlink="http://www.w3.org/1999/xlink" 
               mimetype="video" mime-subtype="mp4" xlink:href="1234-5678.mp4" content-type="machine-generated">
            <alt-text>This is an alternative text that is intentionally made longer than one hundred and twenty characters to ensure that the validation fails as expected.</alt-text>
        </media>
        """
        xml_node = etree.fromstring(xml_content)
        validator = AccessibilityDataValidation(xml_node, self.params)
        result = validator.validate_alt_text()
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["error_level"], "CRITICAL")
        self.assertIn("does not exceed 120 characters", result["advice"])

    def test_validate_long_desc_failure(self):
        """Fails when <long-desc> is shorter than 120 characters."""
        xml_content = """
        <media>
            <long-desc>Short description.</long-desc>
        </media>
        """
        xml_node = etree.fromstring(xml_content)
        validator = AccessibilityDataValidation(xml_node, self.params)
        result = validator.validate_long_desc()
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["error_level"], "CRITICAL")
        self.assertIn("more than 120 characters", result["advice"])

    def test_validate_transcript_failure(self):
        """Fails when a transcript is missing."""
        xml_content = """
        <media>
            <alt-text>Valid alternative text.</alt-text>
            <long-desc>{}</long-desc>
        </media>
        """.format("x" * 130)
        xml_node = etree.fromstring(xml_content)
        validator = AccessibilityDataValidation(xml_node, self.params)
        result = validator.validate_transcript()
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["error_level"], "WARNING")
        self.assertIn("transcript for videos", result["advice"])

    def test_validate_content_type_failure(self):
        """Fails when @content-type is not an allowed value."""
        xml_content = """
        <media content-type="manual">
            <alt-text>Valid alternative text.</alt-text>
        </media>
        """
        xml_node = etree.fromstring(xml_content)
        validator = AccessibilityDataValidation(xml_node, self.params)
        result = validator.validate_content_type()
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["error_level"], "CRITICAL")
        self.assertIn("replace @content-type", result["advice"])

    def test_validate_speaker_and_speech_failure(self):
        """Fails when no <speaker> and <speech> elements are present."""
        xml_content = """
        <media>
            <sec sec-type="transcript">
                <!-- Speaker and Speech missing -->
            </sec>
        </media>
        """
        xml_node = etree.fromstring(xml_content)
        validator = AccessibilityDataValidation(xml_node, self.params)
        result = validator.validate_speaker_and_speech()
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["error_level"], "WARNING")
        self.assertIn("Use <speaker> and <speech>", result["advice"])

    def test_validate_media_structure_failure(self):
        """Fails when accessibility elements are placed outside valid media tags."""
        xml_content = """
        <article>
            <alt-text>Incorrect placement.</alt-text>
        </article>
        """
        xml_node = etree.fromstring(xml_content)
        validator = AccessibilityDataValidation(xml_node, self.params)
        result = validator.validate_media_structure()
        self.assertFalse(result["is_valid"])
        self.assertEqual(result["error_level"], "CRITICAL")
        self.assertIn("accessibility elements are placed", result["advice"])


if __name__ == "__main__":
    unittest.main()
