import unittest
from lxml import etree

from packtools.sps.validation.fig import FigValidation


class FigValidationTest(unittest.TestCase):
    def test_fig_validation_no_fig_elements(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<p>Some text content without figures.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(FigValidation(xmltree).validate_fig_existence())

        expected = [
            {
                "title": "validation of <fig> elements",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "fig",
                "sub_item": None,
                "validation_type": "exist",
                "response": "WARNING",
                "expected_value": "<fig> element",
                "got_value": None,
                "message": "Got None, expected <fig> element",
                "advice": "Add <fig> element to illustrate the content.",
                "data": None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_fig_validation_with_fig_elements(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<fig id="f01">'
            "<label>Figure 1</label>"
            '<graphic xlink:href="image1.png"/>'
            "<alternatives>"
            '<graphic xlink:href="image1-lowres.png" mime-subtype="low-resolution"/>'
            '<graphic xlink:href="image1-highres.png" mime-subtype="high-resolution"/>'
            "</alternatives>"
            "</fig>"
            "</body>"
            "</article>"
        )
        obtained = list(FigValidation(xmltree).validate_fig_existence())

        expected = [
            {
                "title": "validation of <fig> elements",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "fig",
                "sub_item": None,
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "f01",
                "got_value": "f01",
                "message": "Got f01, expected f01",
                "advice": None,
                "data": {
                    "alternative_parent": "fig",
                    "fig_id": "f01",
                    "fig_type": None,
                    "label": "Figure 1",
                    "graphic_href": "image1.png",
                    "caption_text": "",
                    "source_attrib": None,
                    "alternative_elements": ["graphic", "graphic"],
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


if __name__ == "__main__":
    unittest.main()
