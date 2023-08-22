from unittest import TestCase

from packtools.sps.models.v2.article_assets import ArticleAssets
from packtools.sps.utils import xml_utils


def get_xmltree(xml_assets, sub_xml_assets=None):

    return xml_utils.get_xml_tree(
        f"""<article  xmlns:xlink="http://www.w3.org/1999/xlink" >
        <front>
        </front>
        <body>
        {xml_assets or ''}
        </body>
        <back>
        </back>
        <sub-article xml:lang="en" id="sa01">
            <body>
            {sub_xml_assets or ''}
            </body>
        </sub-article>
        </article>"""
    )


class ArticleAssetsFiggroupTest(TestCase):

    def setUp(self):
        xmltree = get_xmltree(
            """<fig-group id="f1">
            <fig xml:lang="pt">
              <label>Figura 1</label>
              <caption>
                <title>Localização do Parque Estadual de Itapeva, Torres, Estado do Rio Grande do Sul, Brasil e áreas de coleta.</title>
              </caption>
            </fig>
            <fig xml:lang="en">
              <label>Figure 1</label>
              <caption>
                <title>Location of Parque Estadual de Itapeva, Torres, Rio Grande do Sul State, Brazil and collection areas.</title>
              </caption>
              <alternatives>
                <graphic xlink:href="original.tif"/>
                <graphic xlink:href="otimizado.png" specific-use="scielo-web"/>
                <graphic xlink:href="mini.jpg" specific-use="scielo-web" content-type="scielo-267x140"/>
              </alternatives>
            </fig>
          </fig-group>"""
        )
        self.article_assets = ArticleAssets(xmltree)

    def test_article_assets_items(self):
        expected_items = [
            {
                'id': 'f1',
                'is_supplementary_material': False,
                'number': None,
                'tag': 'fig-group',
                'type': 'original',
                'xlink_href': 'original.tif'
            },
            {
                'id': 'f1',
                'is_supplementary_material': False,
                'number': None,
                'tag': 'fig-group',
                'type': 'optimised',
                'xlink_href': 'otimizado.png'
            },
            {
                'id': 'f1',
                'is_supplementary_material': False,
                'number': None,
                'tag': 'fig-group',
                'type': 'thumbnail',
                'xlink_href': 'mini.jpg'
            },
        ]
        items = list(self.article_assets.items)
        for i, expected in enumerate(expected_items):
            with self.subTest(i):
                self.assertEqual(expected, items[i].data)

    def test_article_assets_grouped_by_id(self):
        expected_items = {
            "f1": [
                {
                    'id': 'f1',
                    'is_supplementary_material': False,
                    'number': None,
                    'tag': 'fig-group',
                    'type': 'original',
                        'xlink_href': 'original.tif'
                },
                {
                    'id': 'f1',
                    'is_supplementary_material': False,
                    'number': None,
                    'tag': 'fig-group',
                    'type': 'optimised',
                    'xlink_href': 'otimizado.png'
                },
                {
                    'id': 'f1',
                    'is_supplementary_material': False,
                    'number': None,
                    'tag': 'fig-group',
                    'type': 'thumbnail',
                    'xlink_href': 'mini.jpg'
                },
            ]
        }
        self.assertEqual(expected_items, self.article_assets.grouped_by_id)


class ArticleAssetsTest(TestCase):

    def setUp(self):
        xmltree = get_xmltree("""
            <fig id="f01">
            <label>Figura 1</label>
            <caption>
                <title>Caption Figura 1</title>
            </caption>
            <disp-formula>
              <alternatives>
                  <graphic xlink:href="original.tif" />
                  <graphic xlink:href="ampliada.png" specific-use="scielo-web" />
                  <graphic xlink:href="miniatura.jpg" specific-use="scielo-web" content-type="scielo-20x20" />
              </alternatives>
            </disp-formula>
            <attrib>Fonte: Dados originais da pesquisa</attrib>
            </fig>
            <fig id="f03">
            <label>Fig. 3</label>
            <caption>
                <title>titulo da imagem</title>
            </caption>
            <alternatives>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-gf03.tiff"/>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-gf03.png" specific-use="scielo-web"/>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-gf03.thumbnail.jpg" specific-use="scielo-web" content-type="scielo-267x140"/>
            </alternatives>
            </fig>
            <p>We also used an ... based on the equation:<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e04.tif"/>.</p>
            <p><media mimetype="video" mime-subtype="mp4" xlink:href="1234-5678-rctb-45-05-0110-m01.mp4"/></p>
        """)
        self.article_assets = ArticleAssets(xmltree)

    def test_sps_pkg_name(self):
        expected_items = [
            {
                "xlink_href": "original.tif",
                "canonical_name": "NOME-DO-PACOTE-gf01.tif",
            },
            {
                "xlink_href": "ampliada.png",
                "canonical_name": "NOME-DO-PACOTE-gf01.png",
            },
            {
                "xlink_href": "miniatura.jpg",
                "canonical_name": "NOME-DO-PACOTE-gf01-scielo-20x20.jpg",
            },
            {
                "xlink_href": "1234-5678-rctb-45-05-0110-gf03.tiff",
                "canonical_name": "NOME-DO-PACOTE-gf03.tiff",
            },
            {
                "xlink_href": "1234-5678-rctb-45-05-0110-gf03.png",
                "canonical_name": "NOME-DO-PACOTE-gf03.png",
            },
            {
                "xlink_href": "1234-5678-rctb-45-05-0110-gf03.thumbnail.jpg",
                "canonical_name": "NOME-DO-PACOTE-gf03-scielo-267x140.jpg",
            },
            {
                "xlink_href": "1234-5678-rctb-45-05-0110-e04.tif",
                "canonical_name": "NOME-DO-PACOTE-g1.tif",
            },
            {
                "xlink_href": "1234-5678-rctb-45-05-0110-m01.mp4",
                "canonical_name": "NOME-DO-PACOTE-g2.mp4",
            },
        ]
        items = list(self.article_assets.items)
        for i, expected in enumerate(expected_items):
            new_name = items[i].name_canonical("NOME-DO-PACOTE")
            with self.subTest(i):
                self.assertEqual(expected["xlink_href"], items[i].xlink_href)
                self.assertEqual(expected["canonical_name"], new_name)
