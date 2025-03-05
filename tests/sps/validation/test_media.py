import unittest
from lxml import etree
from packtools.sps.validation.media import MediaValidation

class MediaValidationTest(unittest.TestCase):
    def setUp(self):
        self.params = {
            "media_attributes_error_level": "CRITICAL",
            "mime_type_error_level": "CRITICAL",
            "mime_subtype_error_level": "CRITICAL",
            "xlink_href_error_level": "CRITICAL",
            "accessibility_error_level": "CRITICAL",
            "alt_text_error_level": "CRITICAL",
            "long_desc_error_level": "CRITICAL",
            "transcript_error_level": "CRITICAL",
            "content_type_error_level": "CRITICAL",
            "speaker_speech_error_level": "CRITICAL",
            "media_structure_error_level": "CRITICAL",
            "cross_references_error_level": "CRITICAL"
        }

    def test_validate_id_failure(self):
        """Fails when @id attribute is missing."""
        media_data = {"mimetype": "video", "mime_subtype": "mp4", "xlink_href": "video.mp4"}
        validator = MediaValidation(media_data, None, self.params)
        results = validator.validate_id()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "Ensure @id is included.")

    def test_validate_mime_type_failure(self):
        """Fails when @mime-type is invalid."""
        media_data = {"id": "m1", "mimetype": "invalid", "mime_subtype": "mp4", "xlink_href": "video.mp4"}
        validator = MediaValidation(media_data, None, self.params)
        results = validator.validate_mime_type()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "Use a valid @mime-type (application, video, audio).")

    def test_validate_mime_subtype_failure(self):
        """Fails when @mime-subtype does not match the expected format."""
        media_data = {"id": "m1", "mimetype": "video", "mime_subtype": "avi", "xlink_href": "video.avi"}
        validator = MediaValidation(media_data, None, self.params)
        results = validator.validate_mime_subtype()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "For video, use mp4 as @mime-subtype.")

    def test_validate_xlink_href_failure(self):
        """Fails when @xlink:href is not in a valid format."""
        media_data = {"id": "m1", "mimetype": "video", "mime_subtype": "mp4", "xlink_href": "invalid_file"}
        validator = MediaValidation(media_data, None, self.params)
        results = validator.validate_xlink_href()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "Provide a valid file name with its extension in @xlink:href.")

    def test_validate_accessibility_failure(self):
        """Fails when no accessibility elements are provided."""
        media_data = {"id": "m1", "mimetype": "video", "mime_subtype": "mp4", "xlink_href": "video.mp4", "alt_text": None, "long_desc": None, "transcript": None}
        validator = MediaValidation(media_data, None, self.params)
        results = list(validator.validate())
        self.assertEqual(len(results), 11)

if __name__ == "__main__":
    unittest.main()
