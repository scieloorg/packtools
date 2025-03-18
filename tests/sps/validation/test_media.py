import unittest
from lxml import etree
from packtools.sps.validation.media import MediaValidation
from packtools.sps.models.media import (
    Media,
)  # Importando a classe correta para obter media_data


class MediaValidationTest(unittest.TestCase):

    def test_validate_id_failure(self):
        """Fails when @id attribute is missing."""
        xml_content = """
        <media mimetype="video" mime-subtype="mp4" xlink:href="video.mp4" 
               xmlns:xlink="http://www.w3.org/1999/xlink">
        </media>
        """
        media_node = etree.fromstring(xml_content)
        media_data = Media(media_node).data  # Criando media_data a partir de media_node
        params = {"media_attributes_error_level": "CRITICAL"}

        validator = MediaValidation(media_node, media_data, params)
        results = validator.validate_id()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "Ensure @id is included.")

    def test_validate_mime_type_failure(self):
        """Fails when @mime-type is invalid."""
        xml_content = """
        <media id="m1" mimetype="invalid" mime-subtype="mp4" xlink:href="video.mp4" 
               xmlns:xlink="http://www.w3.org/1999/xlink">
        </media>
        """
        media_node = etree.fromstring(xml_content)
        media_data = Media(media_node).data
        params = {"mime_type_error_level": "CRITICAL"}

        validator = MediaValidation(media_node, media_data, params)
        results = validator.validate_mime_type()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(
            results["advice"], "Use a valid @mime-type (application, video, audio)."
        )

    def test_validate_mime_subtype_failure(self):
        """Fails when @mime-subtype does not match the expected format."""
        xml_content = """
        <media id="m1" mimetype="video" mime-subtype="avi" xlink:href="video.avi" 
               xmlns:xlink="http://www.w3.org/1999/xlink">
        </media>
        """
        media_node = etree.fromstring(xml_content)
        media_data = Media(media_node).data
        params = {"mime_subtype_error_level": "CRITICAL"}

        validator = MediaValidation(media_node, media_data, params)
        results = validator.validate_mime_subtype()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(results["advice"], "For video, use mp4 as @mime-subtype.")

    def test_validate_xlink_href_failure(self):
        """Fails when @xlink:href is not in a valid format."""
        xml_content = """
        <media id="m1" mimetype="video" mime-subtype="mp4" xlink:href="invalid_file" 
               xmlns:xlink="http://www.w3.org/1999/xlink">
        </media>
        """
        media_node = etree.fromstring(xml_content)
        media_data = Media(media_node).data
        params = {"xlink_href_error_level": "CRITICAL"}

        validator = MediaValidation(media_node, media_data, params)
        results = validator.validate_xlink_href()
        self.assertEqual(results["response"], "CRITICAL")
        self.assertEqual(
            results["advice"],
            "Provide a valid file name with its extension in @xlink:href.",
        )

    def test_validate_accessibility_failure(self):
        """Fails when no accessibility elements are provided."""
        xml_content = """
        <media id="m1" mimetype="video" mime-subtype="mp4" xlink:href="video.mp4" 
               xmlns:xlink="http://www.w3.org/1999/xlink">
        </media>
        """
        media_node = etree.fromstring(xml_content)
        media_data = Media(media_node).data
        params = {
            "accessibility_error_level": "CRITICAL",
            "mime_type_error_level": "CRITICAL",
            "mime_subtype_error_level": "CRITICAL",
            "alt_text_error_level": "CRITICAL",
            "long_desc_error_level": "CRITICAL",
            "transcript_error_level": "CRITICAL",
            "content_type_error_level": "CRITICAL",
            "speaker_speech_error_level": "CRITICAL",
        }

        validator = MediaValidation(media_node, media_data, params)
        results = list(validator.validate())
        self.assertEqual(len(results), 9)


if __name__ == "__main__":
    unittest.main()
