import unittest
from unittest.mock import MagicMock
from packtools.sps.validation.visual_resource_base import VisualResourceBaseValidation


class TestVisualResourceBaseValidation(unittest.TestCase):
    def setUp(self):
        self.params = {
            "media_attributes_error_level": "CRITICAL",
            "xlink_href_error_level": "WARNING",
            "valid_extension": ["jpg", "mp4", "png"]
        }

    def test_validate_id_missing_on_non_inline(self):
        data = {"tag": "media", "xml": "<media></media>", "id": None}
        validator = VisualResourceBaseValidation(data, self.params)
        result = validator.validate_id()
        self.assertEqual(result["response"], self.params["media_attributes_error_level"])
        self.assertIsNone(result["got_value"])
        self.assertEqual(result["advice"], 'Add id="" to <media></media>')

    def test_validate_id_present_on_non_inline(self):
        data = {"tag": "media", "xml": "<media></media>", "id": "media1"}
        validator = VisualResourceBaseValidation(data, self.params)
        result = validator.validate_id()
        self.assertEqual(result["response"], "OK")

    def test_validate_id_ignored_on_inline(self):
        data = {"tag": "inline-media", "xml": "<inline-media></inline-media>", "id": None}
        validator = VisualResourceBaseValidation(data, self.params)
        result = validator.validate_id()
        self.assertTrue(result["response"])
        self.assertIsNone(result["expected_value"])
        self.assertIsNone(result["advice"])

    def test_validate_xlink_href_valid_extension(self):
        data = {"tag": "media", "xlink_href": "video.mp4", "xml": "<media></media>", "id": "m1"}
        validator = VisualResourceBaseValidation(data, self.params)
        result = validator.validate_xlink_href()
        self.assertEqual(result["response"], "OK")
        self.assertEqual(result["got_value"], "video.mp4")

    def test_validate_xlink_href_invalid_extension(self):
        data = {"tag": "media", "xlink_href": "video.txt", "xml": "<media></media>", "id": "m1"}
        validator = VisualResourceBaseValidation(data, self.params)
        result = validator.validate_xlink_href()
        self.assertEqual(result["response"], "WARNING")
        self.assertEqual(result["expected_value"], "File name with extension")

    def test_validate_integration_with_mocked_accessibility(self):
        data = {
            "tag": "media",
            "xml": "<media></media>",
            "id": "m1",
            "xlink_href": "video.mp4"
        }

        # Monkey patch AccessibilityDataValidation
        from packtools.sps.validation import visual_resource_base
        visual_resource_base.AccessibilityDataValidation = lambda data, params: MagicMock(validate=lambda: iter([{"mocked": True}]))

        validator = VisualResourceBaseValidation(data, self.params)
        results = list(validator.validate())

        self.assertEqual(len(results), 3)
        self.assertTrue(any(r.get("mocked") for r in results))


if __name__ == "__main__":
    unittest.main()
