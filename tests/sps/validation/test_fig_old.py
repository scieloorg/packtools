import unittest
from lxml import etree

from packtools.sps.validation.fig import ArticleFigValidation
from packtools.sps.utils import xml_utils


class FigValidationTest(unittest.TestCase):
    def test_fig_validation_no_fig(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<p>Some text content without figures.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(
            xml_tree,
            {
                "error_level": "WARNING",
                "required_error_level": "CRITICAL",
                "absent_error_level": "WARNING",
                "id_error_level": "CRITICAL",
                "label_error_level": "CRITICAL",
                "caption_error_level": "CRITICAL",
                "content_error_level": "CRITICAL",
                "article_types_requires": ["research-article"]
            }
        ).validate())

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
                "response": 'CRITICAL',
                "expected_value": "<fig/>",
                'got_value': None,
                'message': 'Got None, expected <fig/>',
                "advice": 'article-type=research-article requires <fig/>. Found 0. Identify the fig or check if article-type is correct',
                "data": None,
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_fig_validation_fig_without_id(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<fig>'
            "<label>Figure 1</label>"
            "<caption>"
            "<title>título da imagem</title>"
            "</caption>"
            "<alternatives>"
            '<graphic xlink:href="image1-lowres.png" mime-subtype="low-resolution"/>'
            '<graphic xlink:href="image1-highres.png" mime-subtype="high-resolution"/>'
            "</alternatives>"
            "</fig>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(
            xml_tree,
            {
                "error_level": "WARNING",
                "required_error_level": "CRITICAL",
                "absent_error_level": "WARNING",
                "id_error_level": "CRITICAL",
                "label_error_level": "CRITICAL",
                "caption_error_level": "CRITICAL",
                "content_error_level": "CRITICAL",
                "article_types_requires": ["research-article"],
                "file_extension_error_level": "CRITICAL",
                "allowed file extensions": ["tif", "jpg", "png", "svg"]
            }
        ).validate())

        expected = [
            {
                "title": 'id',
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "fig",
                "sub_item": 'id',
                "validation_type": "exist",
                "response": 'CRITICAL',
                "expected_value": 'id',
                'got_value': None,
                'message': 'Got None, expected id',
                "advice": 'Identify the id',
                "data": {
                    "alternative_parent": "fig",
                    "id": None,
                    "type": None,
                    "label": "Figure 1",
                    "graphic": 'image1-lowres.png',
                    "caption": 'título da imagem',
                    "source_attrib": None,
                    "alternatives": ["graphic", "graphic"],
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    'file_extension': 'png',
                },
            }
        ]

        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_fig_validation_fig_without_label(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<fig id="f01">'
            "<caption>"
            "<title>título da imagem</title>"
            "</caption>"
            "<alternatives>"
            '<graphic xlink:href="image1-lowres.png" mime-subtype="low-resolution"/>'
            '<graphic xlink:href="image1-highres.png" mime-subtype="high-resolution"/>'
            "</alternatives>"
            "</fig>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(
            xml_tree,
            {
                "error_level": "WARNING",
                "required_error_level": "CRITICAL",
                "absent_error_level": "WARNING",
                "id_error_level": "CRITICAL",
                "label_error_level": "CRITICAL",
                "caption_error_level": "CRITICAL",
                "content_error_level": "CRITICAL",
                "article_types_requires": ["research-article"],
                "file_extension_error_level": "CRITICAL",
                "allowed file extensions": ["tif", "jpg", "png", "svg"]
            }
        ).validate())

        expected = [
            {
                "title": 'label',
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "fig",
                "sub_item": 'label',
                "validation_type": "exist",
                "response": 'CRITICAL',
                "expected_value": 'label',
                'got_value': None,
                'message': 'Got None, expected label',
                "advice": 'Identify the label',
                "data": {
                    "alternative_parent": "fig",
                    'id': 'f01',
                    "type": None,
                    "label": None,
                    "graphic": 'image1-lowres.png',
                    "caption": 'título da imagem',
                    "source_attrib": None,
                    "alternatives": ["graphic", "graphic"],
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    'file_extension': 'png',
                },
            }
        ]

        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_fig_validation_fig_without_caption(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<fig id="f01">'
            "<label>Figure 1</label>"
            "<alternatives>"
            '<graphic xlink:href="image1-lowres.png" mime-subtype="low-resolution"/>'
            '<graphic xlink:href="image1-highres.png" mime-subtype="high-resolution"/>'
            "</alternatives>"
            "</fig>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(
            xml_tree,
            {
                "error_level": "WARNING",
                "required_error_level": "CRITICAL",
                "absent_error_level": "WARNING",
                "id_error_level": "CRITICAL",
                "label_error_level": "CRITICAL",
                "caption_error_level": "CRITICAL",
                "content_error_level": "CRITICAL",
                "article_types_requires": ["research-article"],
                "file_extension_error_level": "CRITICAL",
                "allowed file extensions": ["tif", "jpg", "png", "svg"]
            }
        ).validate())

        expected = [
            {
                "title": 'caption',
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "fig",
                "sub_item": 'caption',
                "validation_type": "exist",
                "response": 'CRITICAL',
                "expected_value": 'caption',
                'got_value': None,
                'message': 'Got None, expected caption',
                "advice": 'Identify the caption',
                "data": {
                    "alternative_parent": "fig",
                    'id': 'f01',
                    "type": None,
                    "label": 'Figure 1',
                    "graphic": 'image1-lowres.png',
                    "caption": '',
                    "source_attrib": None,
                    "alternatives": ["graphic", "graphic"],
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    'file_extension': 'png',
                },
            }
        ]

        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_fig_validation_fig_without_graphic_and_alternatives(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<fig id="f01">'
            "<label>Figure 1</label>"
            "<caption>"
            "<title>título da imagem</title>"
            "</caption>"
            "</fig>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(
            xml_tree,
            {
                "error_level": "WARNING",
                "required_error_level": "CRITICAL",
                "absent_error_level": "WARNING",
                "id_error_level": "CRITICAL",
                "label_error_level": "CRITICAL",
                "caption_error_level": "CRITICAL",
                "content_error_level": "CRITICAL",
                "article_types_requires": ["research-article"],
                "file_extension_error_level": "CRITICAL",
                "allowed file extensions": ["tif", "jpg", "png", "svg"]
            }
        ).validate())

        expected = [
            {
                "title": 'graphic or alternatives',
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "fig",
                "sub_item": 'graphic or alternatives',
                "validation_type": "exist",
                "response": 'CRITICAL',
                "expected_value": 'graphic or alternatives',
                'got_value': None,
                'message': 'Got None, expected graphic or alternatives',
                "advice": 'Identify the graphic or alternatives',
                "data": {
                    "alternative_parent": "fig",
                    'id': 'f01',
                    "type": None,
                    "label": 'Figure 1',
                    "graphic": None,
                    "caption": 'título da imagem',
                    "source_attrib": None,
                    "alternatives": [],
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    'file_extension': None,
                },
            },
            {
                "title": "file extension",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "fig",
                "sub_item": "file extension",
                "validation_type": "value in list",
                "response": "CRITICAL",
                "expected_value": "one of ['tif', 'jpg', 'png', 'svg']",
                "got_value": None,
                "message": "Got None, expected one of ['tif', 'jpg', 'png', 'svg']",
                "advice": "provide a file with one of the following extensions ['tif', 'jpg', 'png', 'svg']",
                "data": {
                    "alternative_parent": "fig",
                    "id": "f01",
                    "type": None,
                    "label": "Figure 1",
                    "graphic": None,
                    "caption": "título da imagem",
                    "source_attrib": None,
                    "alternatives": [],
                    "parent": "article",
                    "parent_id": None,
                    "parent_article_type": "research-article",
                    "parent_lang": "pt",
                    "file_extension": None
                }
            }
        ]

        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_fig_validation_file_extension(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
                     dtd-version="1.0" article-type="research-article" xml:lang="pt">
                <body>
                    <p>
                        <fig fig-type="map" id="f02">
                            <label>FIGURE 2</label>
                            <caption>
                                <title>Título da figura 1 em Português</title>
                            </caption>
                            <graphic xlink:href="1234-5678-zwy-12-04-0123-gf02.bmp"/>
                            <attrib>Fonte: IBGE (2018)</attrib>
                        </fig>
                    </p>
                </body>
            </article>
            """
        )
        obtained = list(ArticleFigValidation(
            xml_tree,
            {
                "error_level": "WARNING",
                "required_error_level": "CRITICAL",
                "absent_error_level": "WARNING",
                "id_error_level": "CRITICAL",
                "label_error_level": "CRITICAL",
                "caption_error_level": "CRITICAL",
                "content_error_level": "CRITICAL",
                "article_types_requires": ["research-article"],
                "file_extension_error_level": "CRITICAL",
                "allowed file extensions": ["tif", "jpg", "png", "svg"]
            }
        ).validate())

        expected = [
            {
                "title": "file extension",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "pt",
                "item": "fig",
                "sub_item": "file extension",
                "validation_type": "value in list",
                "response": 'CRITICAL',
                "expected_value": "one of ['tif', 'jpg', 'png', 'svg']",
                'got_value': "bmp",
                'message': "Got bmp, expected one of ['tif', 'jpg', 'png', 'svg']",
                "advice": "provide a file with one of the following extensions ['tif', 'jpg', 'png', 'svg']",
                "data": {
                    'alternative_parent': 'fig',
                    'alternatives': [],
                    'caption': 'Título da figura 1 em Português',
                    'file_extension': 'bmp',
                    'graphic': '1234-5678-zwy-12-04-0123-gf02.bmp',
                    'id': 'f02',
                    'label': 'FIGURE 2',
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'pt',
                    'source_attrib': 'Fonte: IBGE (2018)',
                    'type': 'map'
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])



if __name__ == "__main__":
    unittest.main()
