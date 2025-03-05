import unittest
from lxml import etree
from packtools.sps.validation.accessibility_data import AccessibilityDataValidation

class TestAccessibilityDataValidation(unittest.TestCase):
    def setUp(self):
        self.params = {
            "alt_text_error_level": "CRITICAL",
            "long_desc_error_level": "CRITICAL",
            "transcript_error_level": "CRITICAL",
            "content_type_error_level": "CRITICAL",
            "speaker_speech_error_level": "CRITICAL",
            "media_structure_error_level": "CRITICAL",
            "cross_references_error_level": "CRITICAL"
        }

    def test_validate_alt_text_failure(self):
        """Fails when <alt-text> exceeds 120 characters."""
        accessibility_data = {"alt_text": "This is an alternative text that is intentionally made longer than one hundred and twenty characters to ensure that the validation fails as expected."}
        validator = AccessibilityDataValidation(accessibility_data, None, self.params)
        results = validator.validate_alt_text()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "Provide an alternative text with a maximum of 120 characters.")

    def test_validate_long_desc_failure(self):
        """Fails when <long-desc> is shorter than 120 characters."""
        accessibility_data = {"long_desc": "Short description."}
        validator = AccessibilityDataValidation(accessibility_data, None, self.params)
        results = validator.validate_long_desc()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "Provide a long description with more than 120 characters.")

    def test_validate_transcript_failure(self):
        """Fails when a transcript is missing."""
        accessibility_data = {"transcript": None}
        validator = AccessibilityDataValidation(accessibility_data, None, self.params)
        results = validator.validate_transcript()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "Provide a transcript for videos and audio files.")

    def test_validate_content_type_failure(self):
        """Fails when @content-type is not 'machine-generated'."""
        accessibility_data = {"content_type": "human-generated"}
        validator = AccessibilityDataValidation(accessibility_data, None, self.params)
        results = validator.validate_content_type()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "If applicable, use 'machine-generated' as the content-type.")

    def test_validate_speaker_and_speech_failure(self):
        """Fails when no <speaker> and <speech> elements are present."""
        accessibility_data = {"speakers": []}
        validator = AccessibilityDataValidation(accessibility_data, None, self.params)
        results = validator.validate_speaker_and_speech()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "Ensure proper markup for dialogues.")

    def test_validate_media_structure_failure(self):
        """Fails when accessibility elements are placed outside valid media tags."""
        accessibility_data = {"media_type": "invalid-tag"}
        validator = AccessibilityDataValidation(accessibility_data, None, self.params)
        results = validator.validate_media_structure()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "Ensure that accessibility elements are placed within appropriate media types.")

    def test_validate_cross_references_failure(self):
        """Fails when media does not reference a transcript."""
        accessibility_data = {"xref_refs": []}
        validator = AccessibilityDataValidation(accessibility_data, None, self.params)
        results = validator.validate_cross_references()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "Ensure that media references a transcript.")

if __name__ == "__main__":
    unittest.main()
