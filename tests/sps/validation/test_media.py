import unittest
from lxml import etree

from packtools.sps.validation.media import MediaValidation


class MediaValidationTest(unittest.TestCase):
    def test_media_validation_no_elements(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<p>Some text content without media.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(MediaValidation(xmltree).validate_media_existence())

        expected = [
            {
                "title": "validation of <media> elements",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "media",
                "sub_item": None,
                "validation_type": "exist",
                "response": "WARNING",
                "expected_value": "<media> element",
                "got_value": None,
                "message": "Got None, expected <media> element",
                "advice": "Consider adding a <media> element to include multimedia content related to the article.",
                "data": None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_media_validation_with_elements(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<media mimetype="video" mime-subtype="mp4" xlink:href="media1.mp4">'
            "<label>Media 1</label>"
            "</media>"
            "</body>"
            '<sub-article article-type="translation" xml:lang="en">'
            "<body>"
            '<media mimetype="audio" mime-subtype="mp3" xlink:href="media2.mp3">'
            "<label>Media 2</label>"
            "</media>"
            "</body>"
            "</sub-article>"
            "</article>"
        )
        obtained = list(MediaValidation(xmltree).validate_media_existence())

        expected = [
            {
                "title": "validation of <media> elements",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "media",
                "sub_item": None,
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "media element",
                "got_value": "media element",
                "message": "Got media element, expected media element",
                "advice": None,
                "data": {
                    "mimetype": "video",
                    "mime_subtype": "mp4",
                    "xlink_href": "media1.mp4",
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            },
            {
                "title": "validation of <media> elements",
                "parent": "sub-article",
                "parent_id": None,
                "parent_article_type": "translation",
                "parent_lang": "en",
                "item": "media",
                "sub_item": None,
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "media element",
                "got_value": "media element",
                "message": "Got media element, expected media element",
                "advice": None,
                "data": {
                    "mimetype": "audio",
                    "mime_subtype": "mp3",
                    "xlink_href": "media2.mp3",
                    "parent": "sub-article",
                    "parent_id": None,
                    "parent_article_type": "translation",
                    "parent_lang": "en",
                },
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


if __name__ == "__main__":
    unittest.main()
