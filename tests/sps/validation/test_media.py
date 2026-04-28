import unittest
from unittest.mock import MagicMock

from packtools.sps.validation.media import MediaValidation


class MediaValidationTest(unittest.TestCase):

    def setUp(self):
        self.params = {
            "media_attributes_error_level": "CRITICAL",
            "xlink_href_error_level": "CRITICAL",
            "valid_extension": ["mp3", "mp4", "zip", "pdf", "xlsx", "docx", "pptx"],
            "mime_types_and_subtypes": [
                {"mimetype": "video", "mime-subtype": "mp4"},
                {"mimetype": "audio", "mime-subtype": "mp3"},
                {"mimetype": "application", "mime-subtype": "zip"},
                {"mimetype": "application", "mime-subtype": "pdf"},
                {"mimetype": "application", "mime-subtype": "xlsx"},
                {"mimetype": "application", "mime-subtype": "docx"},
                {"mimetype": "application", "mime-subtype": "pptx"},
            ],
            "mime_type_error_level": "CRITICAL",
        }

    def test_validate_id_failure(self):
        """Fails when @id attribute is missing."""
        data = {
            "tag": "media",
            "xml": "<media></media>",
            "id": None,
            "xlink_href": "video.mp4",
            "mimetype": "video",
            "mime_subtype": "mp4",
        }
        validator = MediaValidation(data, self.params)
        result = validator.validate_id()
        self.assertEqual(result["response"], "CRITICAL")
        self.assertIsNone(result["got_value"])

    def test_validate_id_success(self):
        """Passes when @id attribute is present."""
        data = {
            "tag": "media",
            "xml": "<media></media>",
            "id": "m1",
            "xlink_href": "video.mp4",
            "mimetype": "video",
            "mime_subtype": "mp4",
        }
        validator = MediaValidation(data, self.params)
        result = validator.validate_id()
        self.assertEqual(result["response"], "OK")

    def test_validate_mime_type_and_subtype_failure(self):
        """Fails when mime-type/mime-subtype combination is invalid."""
        data = {
            "tag": "media",
            "xml": "<media></media>",
            "id": "m1",
            "xlink_href": "video.mp4",
            "mimetype": "invalid",
            "mime_subtype": "mp4",
        }
        validator = MediaValidation(data, self.params)
        result = validator.validate_mime_type_and_subtype()
        self.assertEqual(result["response"], "CRITICAL")
        self.assertIsNotNone(result["advice"])

    def test_validate_mime_type_and_subtype_success(self):
        """Passes when mime-type/mime-subtype combination is valid."""
        data = {
            "tag": "media",
            "xml": "<media></media>",
            "id": "m1",
            "xlink_href": "video.mp4",
            "mimetype": "video",
            "mime_subtype": "mp4",
        }
        validator = MediaValidation(data, self.params)
        result = validator.validate_mime_type_and_subtype()
        self.assertEqual(result["response"], "OK")

    def test_validate_mime_type_and_subtype_audio_failure(self):
        """Fails when audio has wrong mime-subtype."""
        data = {
            "tag": "media",
            "xml": "<media></media>",
            "id": "m1",
            "xlink_href": "audio.wav",
            "mimetype": "audio",
            "mime_subtype": "wav",
        }
        validator = MediaValidation(data, self.params)
        result = validator.validate_mime_type_and_subtype()
        self.assertEqual(result["response"], "CRITICAL")

    def test_validate_xlink_href_failure(self):
        """Fails when @xlink:href has invalid extension."""
        data = {
            "tag": "media",
            "xml": "<media></media>",
            "id": "m1",
            "xlink_href": "invalid_file",
            "mimetype": "video",
            "mime_subtype": "mp4",
        }
        validator = MediaValidation(data, self.params)
        result = validator.validate_xlink_href()
        self.assertEqual(result["response"], "CRITICAL")
        self.assertIsNotNone(result["advice"])

    def test_validate_xlink_href_success(self):
        """Passes when @xlink:href has valid extension."""
        data = {
            "tag": "media",
            "xml": "<media></media>",
            "id": "m1",
            "xlink_href": "video.mp4",
            "mimetype": "video",
            "mime_subtype": "mp4",
        }
        validator = MediaValidation(data, self.params)
        result = validator.validate_xlink_href()
        self.assertEqual(result["response"], "OK")

    def test_validate_integration_with_mocked_accessibility(self):
        """Tests full validate() flow ensures accessibility is NOT duplicated.

        Accessibility validation is performed separately by the orchestrator
        through ``XMLAccessibilityDataValidation``, so ``MediaValidation``
        must not yield accessibility entries to avoid duplicated rows in the
        validation report.
        """
        data = {
            "tag": "media",
            "xml": "<media></media>",
            "id": "m1",
            "xlink_href": "video.mp4",
            "mimetype": "video",
            "mime_subtype": "mp4",
        }

        from packtools.sps.validation import visual_resource_base
        original = visual_resource_base.AccessibilityDataValidation
        visual_resource_base.AccessibilityDataValidation = lambda data, params: MagicMock(
            validate=lambda: iter([{"mocked": True}])
        )

        try:
            validator = MediaValidation(data, self.params)
            results = list(validator.validate())
            # 1 (mime_type_and_subtype) + 1 (id) + 1 (xlink_href);
            # accessibility entries must NOT be present here.
            self.assertEqual(len(results), 3)
            self.assertFalse(any(r.get("mocked") for r in results))
        finally:
            visual_resource_base.AccessibilityDataValidation = original

    def test_validate_xlink_href_missing_attribute(self):
        """Missing @xlink:href must produce an error entry, not be swallowed.

        Regression test: previously ``os.path.splitext(None)`` raised a
        ``TypeError`` inside the generator, which silently halted the
        validation flow and produced no entry for the missing attribute.
        """
        data = {
            "tag": "media",
            "xml": '<media id="m01" mimetype="video" mime-subtype="mp4"/>',
            "id": "m01",
            "xlink_href": None,
            "mimetype": "video",
            "mime_subtype": "mp4",
        }
        validator = MediaValidation(data, self.params)
        result = validator.validate_xlink_href()
        self.assertEqual(result["response"], self.params["xlink_href_error_level"])
        self.assertIsNone(result["got_value"])

    def test_validate_inline_media_id_not_required(self):
        """For inline-media, @id is not required."""
        data = {
            "tag": "inline-media",
            "xml": "<inline-media></inline-media>",
            "id": None,
            "xlink_href": "document.pdf",
            "mimetype": "application",
            "mime_subtype": "pdf",
        }
        validator = MediaValidation(data, self.params)
        result = validator.validate_id()
        self.assertEqual(result["response"], "OK")


if __name__ == "__main__":
    unittest.main()
