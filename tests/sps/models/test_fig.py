import unittest
from lxml import etree

from packtools.sps.models.fig import Fig, ArticleFigs


class FigTest(unittest.TestCase):
    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<p>"
            '<fig fig-type="map" id="f02">'
            "<label>FIGURE 2</label>"
            "<caption>"
            "<title>Título da figura</title>"
            "</caption>"
            '<graphic xlink:href="1234-5678-zwy-12-04-0123-gf02.tif"/>'
            "<attrib>Fonte: IBGE (2018)</attrib>"
            "<alternatives>"
            '<graphic xlink:href="1234-5678-zwy-12-04-0123-gf02-lowres.tif" mime-subtype="low-resolution"/>'
            '<graphic xlink:href="1234-5678-zwy-12-04-0123-gf02-highres.tif" mime-subtype="high-resolution"/>'
            "<textual-alternative>"
            "<p>Texto alternativo que descreve a figura em detalhes para acessibilidade.</p>"
            "</textual-alternative>"
            '<media xlink:href="1234-5678-zwy-12-04-0123-gf02.mp4" mime-subtype="video"/>'
            "</alternatives>"
            "</fig>"
            "</p>"
            "</body>"
            "</article>"
        )
        self.xml_tree = etree.fromstring(xml)
        self.fig_element = self.xml_tree.xpath("//fig")[0]
        self.fig_obj = Fig(self.fig_element)

    def test_str_main_tag(self):
        self.assertEqual(
            self.fig_obj.str_main_tag(),
            '<fig fig-type="map" id="f02">'
        )

    def test_str(self):
        self.maxDiff = None
        self.assertEqual(
            str(self.fig_obj),
            "<fig xmlns:xlink=\"http://www.w3.org/1999/xlink\" "
            "xmlns:mml=\"http://www.w3.org/1998/Math/MathML\" fig-type=\"map\" id=\"f02\"><label>FIGURE "
            "2</label><caption><title>Título da figura</title></caption><graphic "
            "xlink:href=\"1234-5678-zwy-12-04-0123-gf02.tif\"/><attrib>Fonte: IBGE ("
            "2018)</attrib><alternatives><graphic xlink:href=\"1234-5678-zwy-12-04-0123-gf02-lowres.tif\" "
            "mime-subtype=\"low-resolution\"/><graphic xlink:href=\"1234-5678-zwy-12-04-0123-gf02-highres.tif\" "
            "mime-subtype=\"high-resolution\"/><textual-alternative><p>Texto alternativo que descreve a figura em "
            "detalhes para acessibilidade.</p></textual-alternative><media "
            "xlink:href=\"1234-5678-zwy-12-04-0123-gf02.mp4\" mime-subtype=\"video\"/></alternatives></fig>"
        )

    def test_xml(self):
        self.maxDiff = None
        self.assertEqual(
            self.fig_obj.xml(),
            """<fig xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" fig-type="map" id="f02">
  <label>FIGURE 2</label>
  <caption>
    <title>Título da figura</title>
  </caption>
  <graphic xlink:href="1234-5678-zwy-12-04-0123-gf02.tif"/>
  <attrib>Fonte: IBGE (2018)</attrib>
  <alternatives>
    <graphic xlink:href="1234-5678-zwy-12-04-0123-gf02-lowres.tif" mime-subtype="low-resolution"/>
    <graphic xlink:href="1234-5678-zwy-12-04-0123-gf02-highres.tif" mime-subtype="high-resolution"/>
    <textual-alternative>
      <p>Texto alternativo que descreve a figura em detalhes para acessibilidade.</p>
    </textual-alternative>
    <media xlink:href="1234-5678-zwy-12-04-0123-gf02.mp4" mime-subtype="video"/>
  </alternatives>
</fig>
"""
        )

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
        self.assertListEqual(
            self.fig_obj.alternative_elements,
            ["graphic", "graphic", "textual-alternative", "media"],
        )

    def test_data(self):
        expected_data = {
            "alternative_parent": "fig",
            "id": "f02",
            "type": "map",
            "label": "FIGURE 2",
            "graphic": "1234-5678-zwy-12-04-0123-gf02.tif",
            "caption": "Título da figura",
            "source_attrib": "Fonte: IBGE (2018)",
            "alternatives": [
                "graphic",
                "graphic",
                "textual-alternative",
                "media",
            ],
            "file_extension": "tif",
        }
        self.assertDictEqual(self.fig_obj.data, expected_data)


class ArticleFigsTest(unittest.TestCase):
    def setUp(self):
        xml = (
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
                            <graphic xlink:href="1234-5678-zwy-12-04-0123-gf02.tif"/>
                            <attrib>Fonte: IBGE (2018)</attrib>
                            <alternatives>
                                <graphic xlink:href="1234-5678-zwy-12-04-0123-gf02-lowres.tif" mime-subtype="low-resolution"/>
                                <graphic xlink:href="1234-5678-zwy-12-04-0123-gf02-highres.tif" mime-subtype="high-resolution"/>
                                <textual-alternative>
                                    <p>Texto alternativo que descreve a figura em detalhes para acessibilidade.</p>
                                </textual-alternative>
                                <media xlink:href="1234-5678-zwy-12-04-0123-gf02.mp4" mime-subtype="video"/>
                            </alternatives>
                        </fig>
                    </p>
                    <p>
                        <fig fig-type="map" id="f03">
                            <label>FIGURE 3</label>
                            <caption>
                                <title>Título da figura 2 em Português</title>
                            </caption>
                            <graphic xlink:href="1234-5678-zwy-12-04-0123-gf03.tif"/>
                            <attrib>Fonte: IBGE (2019)</attrib>
                            <alternatives>
                                <graphic xlink:href="1234-5678-zwy-12-04-0123-gf03-lowres.tif" mime-subtype="low-resolution"/>
                                <graphic xlink:href="1234-5678-zwy-12-04-0123-gf03-highres.tif" mime-subtype="high-resolution"/>
                                <textual-alternative>
                                    <p>Texto alternativo que descreve a figura em detalhes para acessibilidade.</p>
                                </textual-alternative>
                                <media xlink:href="1234-5678-zwy-12-04-0123-gf03.mp4" mime-subtype="video"/>
                            </alternatives>
                        </fig>
                    </p>
                </body>
                <sub-article article-type="translation" id="TRen" xml:lang="en">
                    <body>
                        <p>
                            <fig fig-type="map" id="f01">
                                <label>FIGURE 1</label>
                                <caption>
                                    <title>Title of Map 1</title>
                                </caption>
                                <graphic xlink:href="1234-5678-zwy-12-04-0123-gf01.tif"/>
                            </fig>
                        </p>
                        <p>
                            <fig fig-type="map" id="f04">
                                <label>FIGURE 4</label>
                                <caption>
                                    <title>Title of Map 2</title>
                                </caption>
                                <graphic xlink:href="1234-5678-zwy-12-04-0123-gf04.tif"/>
                            </fig>
                        </p>
                    </body>
                </sub-article>
                <sub-article article-type="supplementary-material" id="SM1" xml:lang="en">
                    <front-stub>
                        <title-group>
                            <article-title>Supplementary Material: Detailed Methodology</article-title>
                        </title-group>
                    </front-stub>
                    <body>
                        <sec>
                            <title>Supplementary Figures</title>
                            <fig fig-type="chart" id="sf1">
                                <label>SUPPLEMENTARY FIGURE 1</label>
                                <caption>
                                    <title>Chart Showing Additional Data</title>
                                </caption>
                                <graphic xlink:href="1234-5678-zwy-12-04-0123-sf01.tif"/>
                                <attrib>Data Source: Experimental Data 2020</attrib>
                            </fig>
                        </sec>
                    </body>
                </sub-article>
            </article>
            """
        )
        self.xml_tree = etree.fromstring(xml)

    def test_get_all_figs(self):
        self.maxDiff = None
        obtained = list(ArticleFigs(self.xml_tree).get_all_figs)

        expected = [
            {
                "alternative_parent": "fig",
                "id": "f02",
                "type": "map",
                "label": "FIGURE 2",
                "graphic": "1234-5678-zwy-12-04-0123-gf02.tif",
                "caption": "Título da figura 1 em Português",
                "source_attrib": "Fonte: IBGE (2018)",
                "alternatives": [
                    "graphic",
                    "graphic",
                    "textual-alternative",
                    "media",
                ],
                "parent": "article",
                "parent_id": None,
                "parent_lang": "pt",
                "parent_article_type": "research-article",
                "file_extension": "tif",
            },
            {
                "alternative_parent": "fig",
                "id": "f03",
                "type": "map",
                "label": "FIGURE 3",
                "graphic": "1234-5678-zwy-12-04-0123-gf03.tif",
                "caption": "Título da figura 2 em Português",
                "source_attrib": "Fonte: IBGE (2019)",
                "alternatives": [
                    "graphic",
                    "graphic",
                    "textual-alternative",
                    "media",
                ],
                "parent": "article",
                "parent_id": None,
                "parent_lang": "pt",
                "parent_article_type": "research-article",
                "file_extension": "tif",
            },
            {
                "alternative_parent": "fig",
                "id": "f01",
                "type": "map",
                "label": "FIGURE 1",
                "graphic": "1234-5678-zwy-12-04-0123-gf01.tif",
                "caption": "Title of Map 1",
                "source_attrib": None,
                "alternatives": [],
                "parent": "sub-article",
                "parent_id": "TRen",
                "parent_lang": "en",
                "parent_article_type": "translation",
                "file_extension": "tif",
            },
            {
                "alternative_parent": "fig",
                "id": "f04",
                "type": "map",
                "label": "FIGURE 4",
                "graphic": "1234-5678-zwy-12-04-0123-gf04.tif",
                "caption": "Title of Map 2",
                "source_attrib": None,
                "alternatives": [],
                "parent": "sub-article",
                "parent_id": "TRen",
                "parent_lang": "en",
                "parent_article_type": "translation",
                "file_extension": "tif",
            },
            {
                'alternatives': [],
                'alternative_parent': 'fig',
                'caption': 'Chart Showing Additional Data',
                'id': 'sf1',
                'type': 'chart',
                'graphic': '1234-5678-zwy-12-04-0123-sf01.tif',
                'label': 'SUPPLEMENTARY FIGURE 1',
                'parent': 'sub-article',
                'parent_article_type': 'supplementary-material',
                'parent_id': 'SM1',
                'parent_lang': 'en',
                'source_attrib': 'Data Source: Experimental Data 2020',
                "file_extension": "tif",
            }

        ]

        self.assertEqual(len(obtained), 5)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_get_article_figs(self):
        self.maxDiff = None
        obtained = list(ArticleFigs(self.xml_tree).get_article_figs)

        expected = [
            {
                "alternative_parent": "fig",
                "id": "f02",
                "type": "map",
                "label": "FIGURE 2",
                "graphic": "1234-5678-zwy-12-04-0123-gf02.tif",
                "caption": "Título da figura 1 em Português",
                "source_attrib": "Fonte: IBGE (2018)",
                "alternatives": [
                    "graphic",
                    "graphic",
                    "textual-alternative",
                    "media",
                ],
                "parent": "article",
                "parent_id": None,
                "parent_lang": "pt",
                "parent_article_type": "research-article",
                "file_extension": "tif",
            },
            {
                "alternative_parent": "fig",
                "id": "f03",
                "type": "map",
                "label": "FIGURE 3",
                "graphic": "1234-5678-zwy-12-04-0123-gf03.tif",
                "caption": "Título da figura 2 em Português",
                "source_attrib": "Fonte: IBGE (2019)",
                "alternatives": [
                    "graphic",
                    "graphic",
                    "textual-alternative",
                    "media",
                ],
                "parent": "article",
                "parent_id": None,
                "parent_lang": "pt",
                "parent_article_type": "research-article",
                "file_extension": "tif",
            }
        ]

        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_get_sub_article_translation_figs(self):
        self.maxDiff = None
        obtained = list(ArticleFigs(self.xml_tree).get_sub_article_translation_figs)

        expected = [
            {
                "alternative_parent": "fig",
                "id": "f01",
                "type": "map",
                "label": "FIGURE 1",
                "graphic": "1234-5678-zwy-12-04-0123-gf01.tif",
                "caption": "Title of Map 1",
                "source_attrib": None,
                "alternatives": [],
                "parent": "sub-article",
                "parent_id": "TRen",
                "parent_lang": "en",
                "parent_article_type": "translation",
                "file_extension": "tif",
            },
            {
                "alternative_parent": "fig",
                "id": "f04",
                "type": "map",
                "label": "FIGURE 4",
                "graphic": "1234-5678-zwy-12-04-0123-gf04.tif",
                "caption": "Title of Map 2",
                "source_attrib": None,
                "alternatives": [],
                "parent": "sub-article",
                "parent_id": "TRen",
                "parent_lang": "en",
                "parent_article_type": "translation",
                "file_extension": "tif",
            }
        ]

        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(item, expected[i])

    def test_get_sub_article_non_translation_figs(self):
        self.maxDiff = None
        obtained = list(ArticleFigs(self.xml_tree).get_sub_article_non_translation_figs)

        expected = [
            {
                'alternatives': [],
                'alternative_parent': 'fig',
                'caption': 'Chart Showing Additional Data',
                'id': 'sf1',
                'type': 'chart',
                'graphic': '1234-5678-zwy-12-04-0123-sf01.tif',
                'label': 'SUPPLEMENTARY FIGURE 1',
                'parent': 'sub-article',
                'parent_article_type': 'supplementary-material',
                'parent_id': 'SM1',
                'parent_lang': 'en',
                'source_attrib': 'Data Source: Experimental Data 2020',
                "file_extension": "tif",
            }
        ]

        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


if __name__ == "__main__":
    unittest.main()
