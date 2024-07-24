import unittest
from lxml import etree

from packtools.sps.models.fig import Fig, ArticleFigs


class FigTest(unittest.TestCase):
    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            '<body>'
            '<p>'
            '<fig fig-type="map" id="f02">'
            '<label>FIGURE 2</label>'
            '<caption>'
            '<title>Título da figura</title>'
            '</caption>'
            '<graphic xlink:href="1234-5678-zwy-12-04-0123-gf02.tif"/>'
            '<attrib>Fonte: IBGE (2018)</attrib>'
            '<alternatives>'
            '<graphic xlink:href="1234-5678-zwy-12-04-0123-gf02-lowres.tif" mime-subtype="low-resolution"/>'
            '<graphic xlink:href="1234-5678-zwy-12-04-0123-gf02-highres.tif" mime-subtype="high-resolution"/>'
            '<textual-alternative>'
            '<p>Texto alternativo que descreve a figura em detalhes para acessibilidade.</p>'
            '</textual-alternative>'
            '<media xlink:href="1234-5678-zwy-12-04-0123-gf02.mp4" mime-subtype="video"/>'
            '</alternatives>'
            '</fig>'
            '</p>'
            '</body>'
            '</article>'
        )
        self.xmltree = etree.fromstring(xml)
        self.fig_element = self.xmltree.xpath("//fig")[0]
        self.fig_obj = Fig(self.fig_element)

    def test_fig_id(self):
        self.assertEqual(self.fig_obj.fig_id, "f02")

    def test_fig_type(self):
        self.assertEqual(self.fig_obj.fig_type, "map")

    def test_label(self):
        self.assertEqual(self.fig_obj.label, "FIGURE 2")

    def test_graphic_href(self):
        self.assertEqual(self.fig_obj.graphic_href, "1234-5678-zwy-12-04-0123-gf02.tif")

    def test_caption_text(self):
        self.assertEqual(self.fig_obj.caption_text, "Título da figura")

    def test_source_attrib(self):
        self.assertEqual(self.fig_obj.source_attrib, "Fonte: IBGE (2018)")

    def test_alternative_elements(self):
        self.assertListEqual(self.fig_obj.alternative_elements, ['graphic', 'graphic', 'textual-alternative', 'media'])

    def test_data(self):
        expected_data = {
            "alternative_parent": "fig",
            "fig_id": "f02",
            "fig_type": "map",
            "label": "FIGURE 2",
            "graphic_href": "1234-5678-zwy-12-04-0123-gf02.tif",
            "caption_text": "Título da figura",
            "source_attrib": "Fonte: IBGE (2018)",
            "alternative_elements": ['graphic', 'graphic', 'textual-alternative', 'media']
        }
        self.assertDictEqual(self.fig_obj.data, expected_data)


class ArticleFigsTest(unittest.TestCase):
    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            '<body>'
            '<p>'
            '<fig fig-type="map" id="f02">'
            '<label>FIGURE 2</label>'
            '<caption>'
            '<title>Título da figura</title>'
            '</caption>'
            '<graphic xlink:href="1234-5678-zwy-12-04-0123-gf02.tif"/>'
            '<attrib>Fonte: IBGE (2018)</attrib>'
            '<alternatives>'
            '<graphic xlink:href="1234-5678-zwy-12-04-0123-gf02-lowres.tif" mime-subtype="low-resolution"/>'
            '<graphic xlink:href="1234-5678-zwy-12-04-0123-gf02-highres.tif" mime-subtype="high-resolution"/>'
            '<textual-alternative>'
            '<p>Texto alternativo que descreve a figura em detalhes para acessibilidade.</p>'
            '</textual-alternative>'
            '<media xlink:href="1234-5678-zwy-12-04-0123-gf02.mp4" mime-subtype="video"/>'
            '</alternatives>'
            '</fig>'
            '</p>'
            '</body>'
            '<sub-article article-type="translation" id="TRen" xml:lang="en">'
		    '<body>'
            '<fig fig-type="map" id="f01">'
            '<label>Map 1</label>'
            '<caption>'
            '<title>Título do Mapa</title>'
            '</caption>'
            '<graphic xlink:href="1234-5678-zwy-12-04-0123-gf01.tif"/>'
            '</fig>'
            '</body>'
            '</sub-article>'
            '</article>'
        )
        self.xmltree = etree.fromstring(xml)

    def test_items_by_lang(self):
        self.maxDiff = None
        obtained = ArticleFigs(self.xmltree).items_by_lang

        expected = {
            "pt": {
                "alternative_parent": "fig",
                "fig_id": "f02",
                "fig_type": "map",
                "label": "FIGURE 2",
                "graphic_href": "1234-5678-zwy-12-04-0123-gf02.tif",
                "caption_text": "Título da figura",
                "source_attrib": "Fonte: IBGE (2018)",
                "alternative_elements": ['graphic', 'graphic', 'textual-alternative', 'media'],
                "parent": "article",
                "parent_id": None,
                "parent_lang": "pt",
                "parent_article_type": "research-article",
            },
            "en": {
                "alternative_parent": "fig",
                "fig_id": "f01",
                "fig_type": "map",
                "label": "Map 1",
                "graphic_href": "1234-5678-zwy-12-04-0123-gf01.tif",
                "caption_text": "Título do Mapa",
                "source_attrib": None,
                "alternative_elements": [],
                "parent": "sub-article",
                "parent_id": "TRen",
                "parent_lang": "en",
                "parent_article_type": "translation",
            },
        }

        for lang, item in expected.items():
            with self.subTest(lang):
                self.assertDictEqual(item, obtained[lang])


if __name__ == '__main__':
    unittest.main()
