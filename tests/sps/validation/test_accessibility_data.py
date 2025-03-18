import unittest
from lxml import etree
from packtools.sps.validation.accessibility_data import AccessibilityDataValidation


class TestAccessibilityDataValidation(unittest.TestCase):

    def test_validate_alt_text_failure(self):
        """Fails when <alt-text> exceeds 120 characters."""
        xml_content = """
        <media xmlns:xlink="http://www.w3.org/1999/xlink" 
               mimetype="video" mime-subtype="mp4" xlink:href="1234-5678.mp4" content-type="machine-generated">
            <alt-text>This is an alternative text that is intentionally made longer than one hundred and twenty characters to ensure that the validation fails as expected.</alt-text>
        </media>
        """
        xml_node = etree.fromstring(xml_content)
        params = {"alt_text_error_level": "CRITICAL"}

        validator = AccessibilityDataValidation(xml_node, params)
        results = validator.validate_alt_text()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(
            results["advice"],
            "Provide an alternative text with a maximum of 120 characters.",
        )

    def test_validate_long_desc_failure(self):
        """Fails when <long-desc> is shorter than 120 characters."""
        xml_content = """
        <media>
            <long-desc>Short description.</long-desc>
        </media>
        """
        xml_node = etree.fromstring(xml_content)
        params = {"long_desc_error_level": "CRITICAL"}

        validator = AccessibilityDataValidation(xml_node, params)
        results = validator.validate_long_desc()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(
            results["advice"],
            "Provide a long description with more than 120 characters.",
        )

    def test_validate_transcript_failure(self):
        """Fails when a transcript is missing."""
        xml_content = """
        <media>
            <alt-text>Valid alternative text.</alt-text>
            <long-desc>Valid long description exceeding 120 characters...</long-desc>
        </media>
        """
        xml_node = etree.fromstring(xml_content)
        params = {"transcript_error_level": "CRITICAL"}

        validator = AccessibilityDataValidation(xml_node, params)
        results = validator.validate_transcript()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(
            results["advice"], "Provide a transcript for videos and audio files."
        )

    def test_validate_content_type_failure(self):
        """Fails when @content-type is not 'machine-generated'."""
        xml_content = """
        <media content-type="manual">
            <alt-text>Valid alternative text.</alt-text>
        </media>
        """
        xml_node = etree.fromstring(xml_content)
        params = {"content_type_error_level": "CRITICAL"}

        validator = AccessibilityDataValidation(xml_node, params)
        results = validator.validate_content_type()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(
            results["advice"],
            "If applicable, use 'machine-generated' as the content-type.",
        )

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
        params = {"speaker_speech_error_level": "CRITICAL"}

        validator = AccessibilityDataValidation(xml_node, params)
        results = validator.validate_speaker_and_speech()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "Ensure proper markup for dialogues.")

    def test_validate_media_structure_failure(self):
        """Fails when accessibility elements are placed outside valid media tags."""
        xml_content = """
        <article>
            <alt-text>Incorrect placement.</alt-text>
        </article>
        """
        xml_node = etree.fromstring(xml_content)
        params = {"media_structure_error_level": "CRITICAL"}

        validator = AccessibilityDataValidation(xml_node, params)
        results = validator.validate_media_structure()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(
            results["advice"],
            "Ensure that accessibility elements are placed within appropriate media types.",
        )


if __name__ == "__main__":
    unittest.main()
