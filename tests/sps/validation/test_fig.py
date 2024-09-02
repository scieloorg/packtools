import unittest
from lxml import etree

from packtools.sps.validation.fig import FigValidation
from packtools.sps.utils import xml_utils


class FigValidationTest(unittest.TestCase):
    def test_fig_validation_no_fig_elements(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<p>Some text content without figures.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(FigValidation(xml_tree).validate_fig_existence())

        expected = [
            {
                "title": "fig presence",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "fig",
                "sub_item": None,
                "validation_type": "exist",
                "response": "WARNING",
                "expected_value": "<fig> element",
                'got_value': None,
                'message': 'Got None, expected <fig> element',
                "advice": "Add <fig> element to illustrate the content.",
                "data": None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_fig_validation_with_fig_elements(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
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
        obtained = list(FigValidation(xml_tree).validate_fig_existence())

        expected = [
            {
                "title": "fig presence",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "fig",
                "sub_item": None,
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "<fig> element",
                'got_value': '<fig fig-type="None" id="f01">',
                'message': 'Got <fig fig-type="None" id="f01">, expected <fig> element',
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

    def test_fig_validation_with_fig_elements_fix_bug(self):
        self.maxDiff = None
        xml_tree = xml_utils.get_xml_tree(
            "tests/fixtures/htmlgenerator/table_wrap_group_and_fig_group/2236-8906"
            "-hoehnea-49-e1082020/2236-8906-hoehnea-49-e1082020.xml"
        )
        obtained = list(FigValidation(xml_tree).validate_fig_existence())

        expected = [
            {
                "title": "fig presence",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "item": "fig",
                "sub_item": None,
                "validation_type": "exist",
                "expected_value": "<fig> element",
                'got_value': '<fig fig-type="None" id="None">',
                "response": "OK",
                'message': 'Got <fig fig-type="None" id="None">, expected <fig> element',
                "advice": None,
                "data": {
                    "alternative_elements": [],
                    "alternative_parent": "fig",
                    "caption_text": "Mapa com a localização das três áreas de estudo, Parque Estadual da Cantareira, "
                    "São Paulo, SP, Brasil. Elaborado por Marina Kanashiro, 2019.",
                    "fig_id": None,
                    "fig_type": None,
                    "graphic_href": None,
                    "label": "Figura 1",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "source_attrib": None,
                },
            },
            {
                'title': 'fig presence',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt',
                'item': 'fig',
                'sub_item': None,
                'validation_type': 'exist',
                'expected_value': '<fig> element',
                'got_value': '<fig fig-type="None" id="None">',
                'response': 'OK',
                'message': 'Got <fig fig-type="None" id="None">, expected <fig> element',
                'advice': None,
                'data': {
                    'alternative_elements': [],
                    'alternative_parent': 'fig',
                    'caption_text': 'Axes 1 and 3 of the ordering analyses by the CA method of the three study areas, '
                                    'Parque Estadual da Cantareira, São Paulo, São Paulo State, Brasil.',
                    'fig_id': None,
                    'fig_type': None,
                    'graphic_href': '2236-8906-hoehnea-49-e1082020-gf14.tif',
                    'label': 'Figure 14',
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'pt',
                    'source_attrib': None
                }
            }
        ]

        self.assertEqual(len(obtained), 28)
        # showing only the first and last record for the figure
        self.assertDictEqual(expected[0], obtained[0])
        self.assertDictEqual(expected[1], obtained[27])


if __name__ == "__main__":
    unittest.main()
