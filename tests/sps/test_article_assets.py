from unittest import TestCase

from packtools.sps.utils import xml_utils

from packtools.sps.models.article_assets import (
    ArticleAssets,
    SupplementaryMaterials,
)


def generate_xmltree(snippet):
    xml = """
    <article xmlns:xlink="http://www.w3.org/1999/xlink">
      <body>
        <sec>
          <p>The Eh measurements... <xref ref-type="fig" rid="f01">Figura 1</xref>:</p>
          <p>
            {0}
          </p>
          <p>
          <fig id="f02">
              <label>Figura 2</label>
              <caption>
                  <title>Caption Figura 2</title>
              </caption>
              <graphic xlink:href="figura2.jpg"/>
              <attrib>Fonte: Dados originais da pesquisa</attrib>
          </fig>
          </p>
        </sec>
      </body>
    </article>
    """
    return xml_utils.get_xml_tree(xml.format(snippet))


def obtain_asset_dict(article_assets, package_name=None):
  assets_dict = {}

  for asset in article_assets:
    asset_metadata = {'name': asset.name, 'type': asset.type}
    if package_name:
      asset_metadata['name_canonical'] = asset.name_canonical(package_name)

    a_id = asset.id
    if a_id not in assets_dict:
      assets_dict[a_id] = []

    assets_dict[a_id].append(asset_metadata)

  return assets_dict


class ArticleAssetsTest(TestCase):
    def test_article_assets_with_one_figure(self):
      data = open('tests/sps/fixtures/document3.xml').read()
      xmltree = xml_utils.get_xml_tree(data)

      expected = {'': [{'name': 'document3-xdadaf.jpg', 'type': 'original'}]}
      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets)

      self.assertDictEqual(expected, obtained)


    def test_article_assets_with_one_figure_multiple_formats(self):
      data = """
      <article xmlns:xlink="http://www.w3.org/1999/xlink">
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
      </article>
      """
      xmltree = xml_utils.get_xml_tree(data)

      expected = {'f01': [{'name': 'original.tif', 'type': 'original'}, {'name': 'ampliada.png', 'type': 'optimised'}, {'name': 'miniatura.jpg', 'type': 'thumbnail'}]}
      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets)

      self.assertDictEqual(expected, obtained)


    def test_article_assets_with_multiple_figures(self):
      data = open('tests/sps/fixtures/document2.xml').read()
      xmltree = xml_utils.get_xml_tree(data)

      expected = {
        'f01': [
          {'name': 'https://minio.scielo.br/documentstore/1414-431X/ywDM7t6mxHzCRWp7kGF9rXQ/fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg', 'type': 'original'},
          {'name': 'https://minio.scielo.br/documentstore/1414-431X/ywDM7t6mxHzCRWp7kGF9rXQ/0c10c88b56f3f9b4f4eccfe9ddbca3fd581aac1b.jpg', 'type': 'thumbnail'}
        ],
        'f02': [
          {'name': 'https://minio.scielo.br/documentstore/1414-431X/ywDM7t6mxHzCRWp7kGF9rXQ/afd520e3ff23a23f2c973bbbaa26094e9e50f487.jpg', 'type': 'original'},
          {'name': 'https://minio.scielo.br/documentstore/1414-431X/ywDM7t6mxHzCRWp7kGF9rXQ/c2e5f2b77881866ef9820b03e99b3fedbb14cb69.jpg', 'type': 'thumbnail'}
        ]
      }
      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets)

      self.assertDictEqual(expected, obtained)


    def test_article_assets_images_outside_figure_and_name_canonical(self):
      # O XML é composto por:
      #  um artigo principal em Inglês composto por 3 figuras (cada uma com original, otimizado e miniatura)
      #  um subartigo em Espanhol com 3 figuras (cada uma com original, otimizado e miniatura)
      #  um subartigo em Português com 3 figuras (cada uma com original, otimizado e miniatura)
      # Há 27 assets sem ID
      data = open('tests/fixtures/htmlgenerator/alternatives/imagens_fora_de_fig.xml').read()
      xmltree = xml_utils.get_xml_tree(data)

      expected = {

        '': [
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/8d6031a105ac49f92d2bac1dab55785ec62ed139.tif', 'name_canonical': 'NOME-DO-PACOTE-g-n00.tif', 'type': 'original'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/d9b80494cba33a6e60786bdfc56a0c9c048125af.png', 'name_canonical': 'NOME-DO-PACOTE-g-n01.png', 'type': 'optimised'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/352c2528e5e3489f3d2c9d4a958bccd776b2667d.jpg', 'name_canonical': 'NOME-DO-PACOTE-g-n02-scielo-267x140.jpg', 'type': 'thumbnail'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/6c7e45494816692122f9467ee9b5ee7a88f86e01.tif', 'name_canonical': 'NOME-DO-PACOTE-g-n03.tif', 'type': 'original'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/c225686bbd2607bacabd946fcb55b30a10b9e5d2.png', 'name_canonical': 'NOME-DO-PACOTE-g-n04.png', 'type': 'optimised'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/d414c6174f0a5069a63c1f4450df8011666a1e35.jpg', 'name_canonical': 'NOME-DO-PACOTE-g-n05-scielo-267x140.jpg', 'type': 'thumbnail'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/7172c66d1c5fa56dc230efa7123dea014f21e62f.tif', 'name_canonical': 'NOME-DO-PACOTE-g-n06.tif', 'type': 'original'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/0d201e31cd5186c2a53f178bfd0509401f2d1ca6.png', 'name_canonical': 'NOME-DO-PACOTE-g-n07.png', 'type': 'optimised'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/0be8783d8e1eb3e4b98cf803ff71ce829a652a1b.jpg', 'name_canonical': 'NOME-DO-PACOTE-g-n08-scielo-267x140.jpg', 'type': 'thumbnail'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/9a4a202884a687ad4858fc95fbf3be801e63215b.tif', 'name_canonical': 'NOME-DO-PACOTE-g-n09-es.tif', 'type': 'original'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/d9b80494cba33a6e60786bdfc56a0c9c048125af.png', 'name_canonical': 'NOME-DO-PACOTE-g-n10-es.png', 'type': 'optimised'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/352c2528e5e3489f3d2c9d4a958bccd776b2667d.jpg', 'name_canonical': 'NOME-DO-PACOTE-g-n11-scielo-267x140-es.jpg', 'type': 'thumbnail'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/1fdbee345fae2065d9bd0fd0b4b09a4f77e99e90.tif', 'name_canonical': 'NOME-DO-PACOTE-g-n12-es.tif', 'type': 'original'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/c225686bbd2607bacabd946fcb55b30a10b9e5d2.png', 'name_canonical': 'NOME-DO-PACOTE-g-n13-es.png', 'type': 'optimised'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/d414c6174f0a5069a63c1f4450df8011666a1e35.jpg', 'name_canonical': 'NOME-DO-PACOTE-g-n14-scielo-267x140-es.jpg', 'type': 'thumbnail'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/aa495447d05a9156d0d15f5f95f8890ee1d55743.tif', 'name_canonical': 'NOME-DO-PACOTE-g-n15-es.tif', 'type': 'original'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/0d201e31cd5186c2a53f178bfd0509401f2d1ca6.png', 'name_canonical': 'NOME-DO-PACOTE-g-n16-es.png', 'type': 'optimised'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/0be8783d8e1eb3e4b98cf803ff71ce829a652a1b.jpg', 'name_canonical': 'NOME-DO-PACOTE-g-n17-scielo-267x140-es.jpg', 'type': 'thumbnail'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/e971ae023bce641ced89dfbdc40d62be94c4c738.tif', 'name_canonical': 'NOME-DO-PACOTE-g-n18-pt.tif', 'type': 'original'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/d9b80494cba33a6e60786bdfc56a0c9c048125af.png', 'name_canonical': 'NOME-DO-PACOTE-g-n19-pt.png', 'type': 'optimised'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/352c2528e5e3489f3d2c9d4a958bccd776b2667d.jpg', 'name_canonical': 'NOME-DO-PACOTE-g-n20-scielo-267x140-pt.jpg', 'type': 'thumbnail'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/30d718ea67b77dd98bcda9d3acba9cb296fcba9e.tif', 'name_canonical': 'NOME-DO-PACOTE-g-n21-pt.tif', 'type': 'original'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/c225686bbd2607bacabd946fcb55b30a10b9e5d2.png', 'name_canonical': 'NOME-DO-PACOTE-g-n22-pt.png', 'type': 'optimised'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/d414c6174f0a5069a63c1f4450df8011666a1e35.jpg', 'name_canonical': 'NOME-DO-PACOTE-g-n23-scielo-267x140-pt.jpg', 'type': 'thumbnail'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/b824ebf96bd03d51ee26edc6c3807c3092bf1901.tif', 'name_canonical': 'NOME-DO-PACOTE-g-n24-pt.tif', 'type': 'original'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/0d201e31cd5186c2a53f178bfd0509401f2d1ca6.png', 'name_canonical': 'NOME-DO-PACOTE-g-n25-pt.png', 'type': 'optimised'},
          {'name': 'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/0be8783d8e1eb3e4b98cf803ff71ce829a652a1b.jpg', 'name_canonical': 'NOME-DO-PACOTE-g-n26-scielo-267x140-pt.jpg', 'type': 'thumbnail'},
        ]
      }
      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets, package_name='NOME-DO-PACOTE')

      self.assertDictEqual(expected, obtained)


    def test_article_assets_with_media(self):
      data = """
      <article xmlns:xlink="http://www.w3.org/1999/xlink">
        <body>
          <p><media mimetype="video" mime-subtype="mp4" xlink:href="1234-5678-rctb-45-05-0110-m01.mp4"/></p>
        </body>
      </article>
      """
      xmltree = xml_utils.get_xml_tree(data)

      expected = {None: [{'name': '1234-5678-rctb-45-05-0110-m01.mp4', 'type': 'original'}],}
      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets)

      self.assertDictEqual(expected, obtained)
  

    def test_article_assets_with_media_and_graphic(self):
      data = """
      <article xmlns:xlink="http://www.w3.org/1999/xlink">
        <body>
          <p><media mimetype="video" mime-subtype="mp4" xlink:href="1234-5678-rctb-45-05-0110-m01.mp4"/></p>
          <div>
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
          </div>
        </body>
      </article>
      """
      xmltree = xml_utils.get_xml_tree(data)

      expected = {
        '': [
          {'name': '1234-5678-rctb-45-05-0110-m01.mp4', 'type': 'original'},
        ],
        'f01': [
          {'name': 'original.tif', 'type': 'original'},
          {'name': 'ampliada.png', 'type': 'optimised'},
          {'name': 'miniatura.jpg', 'type': 'thumbnail'},
        ]
      }
      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets)

      self.assertDictEqual(expected, obtained)


    def test_article_assets_with_inline_graphic(self):
      data = """
      <article xmlns:xlink="http://www.w3.org/1999/xlink">
        <front>
          <article-meta>
          </article-meta>
        </front>
        <body>
          <sec>
            <p>The Eh measurements... <xref ref-type="disp-formula" rid="e01">equation 1</xref>(in mV):</p>
            <disp-formula id="e01">
              {}
            </disp-formula>
            <p>We also used an... {}.</p>
          </sec>
          <p>We also used an ... based on the equation:<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e04.tif"/>.</p>
        </body>
      </article>
      """
      xmltree = xml_utils.get_xml_tree(data)

      expected = {
        '': [
          {'name': '1234-5678-rctb-45-05-0110-e04.tif', 'type': 'original'},
        ]
      }
      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets)

      self.assertDictEqual(expected, obtained)


    def test_article_assets_with_inline_graphic_and_others(self):
      data = """
      <article xmlns:xlink="http://www.w3.org/1999/xlink">
        <front>
          <article-meta>
          </article-meta>
        </front>
        <body>
          <sec>
            <p>The Eh measurements... <xref ref-type="disp-formula" rid="e01">equation 1</xref>(in mV):</p>
            <disp-formula id="e01">
              {}
            </disp-formula>
            <p>We also used an... {}.</p>
          </sec>
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
        </body>
      </article>
      """
      xmltree = xml_utils.get_xml_tree(data)

      expected = {
        'f01': [
          {'name': 'original.tif', 'type': 'original'},
          {'name': 'ampliada.png', 'type': 'optimised'},
          {'name': 'miniatura.jpg', 'type': 'thumbnail'},
        ],
        'f03': [
          {'name': '1234-5678-rctb-45-05-0110-gf03.tiff', 'type': 'original'},
          {'name': '1234-5678-rctb-45-05-0110-gf03.png', 'type': 'optimised'},
          {'name': '1234-5678-rctb-45-05-0110-gf03.thumbnail.jpg', 'type': 'thumbnail'},
        ],
        '': [
          {'name': '1234-5678-rctb-45-05-0110-e04.tif', 'type': 'original'},
          {'name': '1234-5678-rctb-45-05-0110-m01.mp4', 'type': 'original'},
        ]
      }

      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets)

      self.assertDictEqual(expected, obtained)


    def test_article_assets_with_supplementary_material(self):
      data = """
      <article xmlns:xlink="http://www.w3.org/1999/xlink">
        <body>
          <supplementary-material id="S1"
                                  xlink:title="local_file"
                                  xlink:href="1471-2105-1-1-s1.pdf"
                                  mimetype="application"
                                  mime-subtype="pdf">
            <label>Additional material</label>
            <caption>
              <p>Supplementary PDF file supplied by authors.</p>
            </caption>
          </supplementary-material>
        </body>
      </article>
      """

      xmltree = xml_utils.get_xml_tree(data)

      expected = {
        'S1': [
        {'name': '1471-2105-1-1-s1.pdf', 'type': 'original'},
        ]
      }
      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets)

      self.assertDictEqual(expected, obtained)


    def test_article_assets_with_supplementary_material_and_media_and_graphic(self):
      data = """
      <article xmlns:xlink="http://www.w3.org/1999/xlink">
        <body>
          <supplementary-material id="S1"
                                  xlink:title="local_file"
                                  xlink:href="1471-2105-1-1-s1.pdf"
                                  mimetype="application"
                                  mime-subtype="pdf">
            <label>Additional material</label>
            <caption>
              <p>Supplementary PDF file supplied by authors.</p>
            </caption>
          </supplementary-material>
          <p><media mimetype="video" mime-subtype="mp4" xlink:href="1234-5678-rctb-45-05-0110-m01.mp4"/></p>
          <div>
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
          </div>
        </body>
      </article>
      """

      xmltree = xml_utils.get_xml_tree(data)

      expected = {
        'S1': [
          {'name': '1471-2105-1-1-s1.pdf', 'type': 'original'},
        ],
        '': [
          {'name': '1234-5678-rctb-45-05-0110-m01.mp4', 'type': 'original'},
        ],
        'f01': [
          {'name': 'original.tif', 'type': 'original'},
          {'name': 'ampliada.png', 'type': 'optimised'},
          {'name': 'miniatura.jpg', 'type': 'thumbnail'},
        ]
      }

      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets)

      self.assertDictEqual(expected, obtained)


    def test_article_assets_with_multiple_supplementary_material(self):
      data = open('tests/sps/fixtures/document-with-supplementary-material.xml').read()
      xmltree = xml_utils.get_xml_tree(data)

      expected = {
        'f1': [
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/256bcf2e607f18b0bb3842a31332f6b48620cb09.tif', 'type': 'original'},
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/c00655410885461df4a98dd77860b81b2e5baa2c.png', 'type': 'optimised'},
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/ebd30641f55d890debe55743b8e2946135c74140.jpg', 'type': 'thumbnail'},
        ],
        'f2': [
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/b784533145d2f1557a7df00e05e5c6207fc57e2a.tif', 'type': 'original'},
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/b298055fb49aba04fa94a1287ed4c38c0680ccf7.png', 'type': 'optimised'},
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/c0a10dd209a9da0ef40f92f070ee6c77b0ca220b.jpg', 'type': 'thumbnail'},
        ],
        'f3': [
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/14717caba8b886eddbbc9e1e4a8c579631730187.tif', 'type': 'original'},
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/b0b01286ff114d6eda85f9a5afb1217d164e32b5.png', 'type': 'optimised'},
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/b03ad3e4bced80bf0a81dfe12fbe6e567982414b.jpg', 'type': 'thumbnail'},
        ],
        'f4': [
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/407a7771f32d6364ee6536278a011a2c05da3339.tif', 'type': 'original'},
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/c1ba665e5e0731d623095779a2d4099c808e776b.png', 'type': 'optimised'},
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/f1da586984d4176883f92f2fb28e9abea946b8d2.jpg', 'type': 'thumbnail'},
        ],
        'suppl01': [
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/e738857c8fb8bc085b766a812bbe73277c67d346.pdf', 'type': 'original'},
        ],
        'suppl02': [
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/b72942b47698183bf992f1ad8cebdf61d346e0cf.xls', 'type': 'original'},
        ],
        'suppl03': [
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/ffc50de0245a936540df9f98b7de123c8c597cbf.pdf', 'type': 'original'},
        ]
      }
      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets)

      self.assertDictEqual(expected, obtained)


    def test_article_assets_with_fig_group_graphic(self):
      snippet = """
      <fig-group id="f01">
        <fig xml:lang="pt">
          <label>Figura 1</label>
          <caption>
            <title>Caption Figura PT</title>
          </caption>
          <attrib>
            <p>Nota da tabela em pt</p>
          </attrib>
        </fig>
        <fig xml:lang="en">
          <label>Figure 1</label>
          <caption>
            <title>Caption Figura EN</title>
          </caption>
          <attrib>
            <p><xref ref-type="fig" rid="f01">Figure 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
          </attrib>
        </fig>
        <graphic xlink:href="original"/>
      </fig-group>
      """
      xmltree = generate_xmltree(snippet)

      expected = {
        'f01': [
          {'name': 'original', 'type': 'original'}
        ],
        'f02': [
          {'name': 'figura2.jpg', 'type': 'original'}
        ]
      }
      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets)

      self.assertDictEqual(expected, obtained)


    def test_article_assets_with_fig_group_graphic_alternatives(self):
      snippet = """
      <fig-group id="f01">
        <fig xml:lang="pt">
          <label>Figura 1</label>
          <caption>
            <title>Caption Figura PT</title>
          </caption>
          <attrib>
            <p>Nota da tabela em pt</p>
          </attrib>
        </fig>
        <fig xml:lang="en">
          <label>Figure 1</label>
          <caption>
            <title>Caption Figura EN</title>
          </caption>
          <attrib>
            <p><xref ref-type="fig" rid="f01">Figure 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
          </attrib>
        </fig>
        <alternatives>
          <graphic xlink:href="original.tif" />
          <graphic xlink:href="ampliada.png" specific-use="scielo-web" />
          <graphic xlink:href="miniatura.jpg" specific-use="scielo-web" content-type="scielo-20x20" />
        </alternatives>
      </fig-group>
      """
      xmltree = generate_xmltree(snippet)

      expected = {
        'f01': [
          {'name': 'original.tif', 'type': 'original'},
          {'name': 'ampliada.png', 'type': 'optimised'},
          {'name': 'miniatura.jpg', 'type': 'thumbnail'},
        ],
        'f02': [
          {'name': 'figura2.jpg', 'type': 'original'},
        ]
      }
      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets)

      self.assertDictEqual(expected, obtained)


    def test_article_assets_with_fig_group_graphic_before_attrib(self):
      snippet = """
      <fig-group id="f01">
        <fig xml:lang="pt">
          <label>Figura 1</label>
          <caption>
            <title>Caption Figura PT</title>
          </caption>
          <attrib>
            <p>Nota da tabela em pt</p>
          </attrib>
        </fig>
        <fig xml:lang="en">
          <label>Figure 1</label>
          <caption>
            <title>Caption Figura EN</title>
          </caption>
          <graphic xlink:href="original"/>
          <attrib>
            <p><xref ref-type="fig" rid="f01">Figure 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
          </attrib>
        </fig>
      </fig-group>
      """
      xmltree = generate_xmltree(snippet)

      expected = {
        'f01': [
          {'name': 'original', 'type': 'original'},
        ],
        'f02': [
          {'name': 'figura2.jpg', 'type': 'original'},
        ]
      }
      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets)

      self.assertDictEqual(expected, obtained)


    def test_article_assets_with_fig_group_graphic_alternatives_before_attrib(self):
      snippet = """
      <fig-group id="f01">
        <fig xml:lang="pt">
          <label>Figura 1</label>
          <caption>
            <title>Caption Figura PT</title>
          </caption>
          <attrib>
            <p>Nota da tabela em pt</p>
          </attrib>
        </fig>
        <fig xml:lang="en">
          <label>Figure 1</label>
          <caption>
            <title>Caption Figura EN</title>
          </caption>
          <alternatives>
            <graphic xlink:href="original.tif" />
            <graphic xlink:href="ampliada.png" specific-use="scielo-web" />
            <graphic xlink:href="miniatura.jpg" specific-use="scielo-web" content-type="scielo-20x20" />
          </alternatives>
          <attrib>
            <p><xref ref-type="fig" rid="f01">Figure 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
          </attrib>
        </fig>
      </fig-group>
      """
      xmltree = generate_xmltree(snippet)

      expected = {
        'f01': [
          {'name': 'original.tif', 'type': 'original'},
          {'name': 'ampliada.png', 'type': 'optimised'},
          {'name': 'miniatura.jpg', 'type': 'thumbnail'},
        ],
        'f02': [
          {'name': 'figura2.jpg', 'type': 'original'},
        ]
      }
      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets)

      self.assertDictEqual(expected, obtained)


    def test_article_assets_optimised_default(self):
      data = open('tests/sps/fixtures/2318-0889-tinf-33-e200068.xml').read()
      xmltree = xml_utils.get_xml_tree(data)

      expected = {
        'f01': [
          {'name': '2318-0889-tinf-33-e200068-gf01.tif', 'type': 'original'},
          {'name': '2318-0889-tinf-33-e200068-gf01.png', 'type': 'optimised'},
          {'name': '2318-0889-tinf-33-e200068-gf01.thumbnail.jpg', 'type': 'thumbnail'}],
        'f02': [
          {'name': '2318-0889-tinf-33-e200068-gf02.tif', 'type': 'original'},
          {'name': '2318-0889-tinf-33-e200068-gf02.png', 'type': 'optimised'},
          {'name': '2318-0889-tinf-33-e200068-gf02.thumbnail.jpg', 'type': 'thumbnail'}
        ]
      }
      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets)

      self.assertDictEqual(expected, obtained)


    def test_article_assets_optimised_png_as_original(self):
      snippet = """
      <fig-group id="f01">
        <fig xml:lang="pt">
          <label>Figura 1</label>
          <caption>
            <title>Caption Figura PT</title>
          </caption>
          <attrib>
            <p>Nota da tabela em pt</p>
          </attrib>
        </fig>
        <fig xml:lang="en">
          <label>Figure 1</label>
          <caption>
            <title>Caption Figura EN</title>
          </caption>
          <alternatives>
            <graphic xlink:href="original.png" />
            <graphic xlink:href="miniatura.jpg" specific-use="scielo-web" content-type="scielo-20x20" />
          </alternatives>
          <attrib>
            <p><xref ref-type="fig" rid="f01">Figure 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
          </attrib>
        </fig>
      </fig-group>
      """
      xmltree = generate_xmltree(snippet)

      expected = {
        'f01': [
          {'name': 'original.png', 'type': 'original'},
          {'name': 'miniatura.jpg', 'type': 'thumbnail'}],
        'f02': [
          {'name': 'figura2.jpg', 'type': 'original'},
        ]
      }
      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets)

      self.assertDictEqual(expected, obtained)

    def test_replace_names_not_found(self):
        snippet = """
        <fig-group id="f01">
            <fig xml:lang="pt">
                <label>Figura 1</label>
                <caption>
                    <title>Caption Figura PT</title>
                </caption>
                <attrib>
                    <p>Nota da tabela em pt</p>
                </attrib>
            </fig>
            <fig xml:lang="en">
                <label>Figure 1</label>
                <caption>
                    <title>Caption Figura EN</title>
                </caption>
                <alternatives>
                    <graphic xlink:href="original.png" />
                    <graphic xlink:href="miniatura.jpg" specific-use="scielo-web" content-type="scielo-20x20" />
                </alternatives>
                <attrib>
                    <p><xref ref-type="fig" rid="f01">Figure 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
                </attrib>
            </fig>
        </fig-group>
        """
        xmltree = generate_xmltree(snippet)

        from_to = {
            "original.png": "novo_original.png",
            "miniatura.jpg": "novo_miniatura.jpg",
            "figura2.jpg": "novo_figura2.jpg",
        }
        article_assets = ArticleAssets(xmltree)
        not_found = article_assets.replace_names(from_to)
        self.assertEqual(not_found, [])

        updated = article_assets.article_assets
        self.assertEqual(updated[0].name, 'novo_original.png')
        self.assertEqual(updated[1].name, 'novo_miniatura.jpg')
        self.assertEqual(updated[2].name, 'novo_figura2.jpg')

    def test_replace_names(self):
        snippet = """
        <fig-group id="f01">
            <fig xml:lang="pt">
                <label>Figura 1</label>
                <caption>
                    <title>Caption Figura PT</title>
                </caption>
                <attrib>
                    <p>Nota da tabela em pt</p>
                </attrib>
            </fig>
            <fig xml:lang="en">
                <label>Figure 1</label>
                <caption>
                    <title>Caption Figura EN</title>
                </caption>
                <alternatives>
                    <graphic xlink:href="original.png" />
                    <graphic xlink:href="miniatura.jpg" specific-use="scielo-web" content-type="scielo-20x20" />
                </alternatives>
                <attrib>
                    <p><xref ref-type="fig" rid="f01">Figure 1</xref> Identification of <italic>Senna Senna</italic> Mill. (Fabaceae) species collected in different locations in northwestern Ceará State. <sup>*</sup> Exotic, <sup>**</sup> Endemic to Brazil. Source: Herbário Francisco José de Abreu Matos (HUVA).</p>
                </attrib>
            </fig>
        </fig-group>
        """
        xmltree = generate_xmltree(snippet)

        from_to = {
            "original.png": "novo_original.png",
            "miniatura.jpg": "novo_miniatura.jpg",
            "figura02.jpg": "novo_figura2.jpg",
        }

        article_assets = ArticleAssets(xmltree)
        not_found = article_assets.replace_names(from_to)

        updated = article_assets.article_assets
        self.assertEqual(updated[0].name, 'novo_original.png')
        self.assertEqual(updated[1].name, 'novo_miniatura.jpg')
        self.assertEqual(not_found, ["figura2.jpg"])


    def test_assets_canonical_name_without_subarticles(self):
      data = open('tests/sps/fixtures/document-with-supplementary-material.xml').read()
      xmltree = xml_utils.get_xml_tree(data)

      expected = {
        'f1': [
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/256bcf2e607f18b0bb3842a31332f6b48620cb09.tif', 'name_canonical': '1676-0611-bn-2021-1306-g01.tif', 'type': 'original'},
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/c00655410885461df4a98dd77860b81b2e5baa2c.png', 'name_canonical': '1676-0611-bn-2021-1306-g01.png', 'type': 'optimised'},
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/ebd30641f55d890debe55743b8e2946135c74140.jpg', 'name_canonical': '1676-0611-bn-2021-1306-g01-scielo-267x140.jpg', 'type': 'thumbnail'},
        ],
        'f2': [
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/b784533145d2f1557a7df00e05e5c6207fc57e2a.tif', 'name_canonical': '1676-0611-bn-2021-1306-g02.tif', 'type': 'original'},
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/b298055fb49aba04fa94a1287ed4c38c0680ccf7.png', 'name_canonical': '1676-0611-bn-2021-1306-g02.png', 'type': 'optimised'},
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/c0a10dd209a9da0ef40f92f070ee6c77b0ca220b.jpg', 'name_canonical': '1676-0611-bn-2021-1306-g02-scielo-267x140.jpg', 'type': 'thumbnail'},
        ],
        'f3': [
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/14717caba8b886eddbbc9e1e4a8c579631730187.tif', 'name_canonical': '1676-0611-bn-2021-1306-g03.tif', 'type': 'original'},
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/b0b01286ff114d6eda85f9a5afb1217d164e32b5.png', 'name_canonical': '1676-0611-bn-2021-1306-g03.png', 'type': 'optimised'},
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/b03ad3e4bced80bf0a81dfe12fbe6e567982414b.jpg', 'name_canonical': '1676-0611-bn-2021-1306-g03-scielo-267x140.jpg', 'type': 'thumbnail'},
        ],
        'f4': [
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/407a7771f32d6364ee6536278a011a2c05da3339.tif', 'name_canonical': '1676-0611-bn-2021-1306-g04.tif', 'type': 'original'},
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/c1ba665e5e0731d623095779a2d4099c808e776b.png', 'name_canonical': '1676-0611-bn-2021-1306-g04.png', 'type': 'optimised'},
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/f1da586984d4176883f92f2fb28e9abea946b8d2.jpg', 'name_canonical': '1676-0611-bn-2021-1306-g04-scielo-267x140.jpg', 'type': 'thumbnail'},
        ],
        'suppl01': [
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/e738857c8fb8bc085b766a812bbe73277c67d346.pdf', 'name_canonical': '1676-0611-bn-2021-1306-s01.pdf', 'type': 'original'},
        ],
        'suppl02': [
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/b72942b47698183bf992f1ad8cebdf61d346e0cf.xls', 'name_canonical': '1676-0611-bn-2021-1306-s02.xls', 'type': 'original'},
        ],
        'suppl03': [
          {'name': 'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/ffc50de0245a936540df9f98b7de123c8c597cbf.pdf', 'name_canonical': '1676-0611-bn-2021-1306-s03.pdf', 'type': 'original'},
        ]
      }
      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets, package_name='1676-0611-bn-2021-1306')

      self.assertDictEqual(expected, obtained)


    def test_assets_canonical_name_with_subarticles_and_without_id(self):
      data = open('tests/samples/0034-8910-rsp-48-2-0232.xml').read()
      xmltree = xml_utils.get_xml_tree(data)

      expected = {
        # <graphic> sem id associado
        None: [{'name': '0034-8910-rsp-48-2-0232-ee01', 'name_canonical': '0034-8910-rsp-48-2-0232-g', 'type': 'original'}],
        # <graphic> sem id associado (o id do sub-article mais próximo é obtido)
        'TRen': [{'name': '0034-8910-rsp-48-2-0232-ee01-en', 'name_canonical': '0034-8910-rsp-48-2-0232-g00-en', 'type': 'original'}],
        'app01': [{'name': '0034-8910-rsp-48-2-0232-app01', 'name_canonical': '0034-8910-rsp-48-2-0232-g01-en', 'type': 'original'}],
        # <graphic> cujo id é f01
        'f01': [{'name': '0034-8910-rsp-48-2-0232-gf01', 'name_canonical': '0034-8910-rsp-48-2-0232-g01', 'type': 'original'}],
        # <graphic> cujo id é f01_en
        'f01_en': [{'name': '0034-8910-rsp-48-2-0232-gf01-en', 'name_canonical': '0034-8910-rsp-48-2-0232-g01-en', 'type': 'original'}],
      }
      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets, package_name='0034-8910-rsp-48-2-0232')

      self.assertDictEqual(expected, obtained)


    def test_assets_canonical_name_with_subarticles_and_ids_with_lang(self):
      data = open('tests/samples/0034-8910-rsp-48-2-0240.xml').read()
      xmltree = xml_utils.get_xml_tree(data)

      expected = {
        'f01': [{'name': '0034-8910-rsp-48-2-0240-gf01', 'name_canonical': '0034-8910-rsp-48-2-0240-g01', 'type': 'original'}],
        'f02': [{'name': '0034-8910-rsp-48-2-0240-gf02', 'name_canonical': '0034-8910-rsp-48-2-0240-g02', 'type': 'original'}],
        'f03': [{'name': '0034-8910-rsp-48-2-0240-gf03', 'name_canonical': '0034-8910-rsp-48-2-0240-g03', 'type': 'original'}],
        'f04': [{'name': '0034-8910-rsp-48-2-0240-gf04', 'name_canonical': '0034-8910-rsp-48-2-0240-g04', 'type': 'original'}],
        'f01_en': [{'name': '0034-8910-rsp-48-2-0240-gf01-en', 'name_canonical': '0034-8910-rsp-48-2-0240-g01-en', 'type': 'original'}],
        'f02_en': [{'name': '0034-8910-rsp-48-2-0240-gf02-en', 'name_canonical': '0034-8910-rsp-48-2-0240-g02-en', 'type': 'original'}],
        'f03_en': [{'name': '0034-8910-rsp-48-2-0240-gf03-en', 'name_canonical': '0034-8910-rsp-48-2-0240-g03-en', 'type': 'original'}],
        'f04_en': [{'name': '0034-8910-rsp-48-2-0240-gf04-en', 'name_canonical': '0034-8910-rsp-48-2-0240-g04-en', 'type': 'original'}],
      }
      obtained = obtain_asset_dict(ArticleAssets(xmltree).article_assets, package_name='0034-8910-rsp-48-2-0240')

      self.assertDictEqual(expected, obtained)


class SupplementaryMaterialsTest(TestCase):
    def _get_xmltree(self, xml):
        return xml_utils.get_xml_tree(xml)

    def test_inline_supplementary_material(self):
        
        data = (
        """<article xmlns:xlink="http://www.w3.org/1999/xlink" >
<back>
    <fn-group>
      <fn fn-type="supplementary-material">
        <p>
          <bold>Supplementary Information</bold>
        </p>
        <p>Supplementary information (chromatograms from chiral GC analysis) is available free of charge at <ext-link ext-link-type="uri" xlink:href="http://jbcs.sbq.org.br">http://jbcs.sbq.org.br</ext-link> as <inline-supplementary-material xlink:href="https://minio.scielo.br/documentstore/1678-4790/LgRcS7ZYYQ5wSDKw8wKytSp/818bf2b94169513756c9f4734c24d9bc774a3795.pdf" mimetype="application" mime-subtype="pdf">PDF</inline-supplementary-material> file.</p>
      </fn>
    </fn-group></back></article>

        """
        )
        xmltree = xml_utils.get_xml_tree(data)

        expected = [
            (None, 'https://minio.scielo.br/documentstore/1678-4790/LgRcS7ZYYQ5wSDKw8wKytSp/818bf2b94169513756c9f4734c24d9bc774a3795.pdf'),
        ]

        for i, item in enumerate(SupplementaryMaterials(xmltree).items):
            with self.subTest(i):
                self.assertEqual(item.id, expected[i][0])
                self.assertEqual(item.name, expected[i][1])

    def test_supplementary_material(self):
        
        data = (
        """<article xmlns:xlink="http://www.w3.org/1999/xlink" >
<back>
<app-group>
<app id="app01">
<title>Material suplementar</title>
<p>O seguinte material suplementar está disponível online:</p>
<p>
<supplementary-material id="suppl01" mime-subtype="pdf" mimetype="application" xlink:href="c834.pdf">
<label>Apêndice A –</label>
<caption>
<title>
A relação entre energia e frequência de um
<italic>quantum</italic>
obtida por Einstein em 1905
</title>
</caption>
</supplementary-material>
</p>
</app>
<app id="app02">
<p>
<supplementary-material id="suppl02" mime-subtype="pdf" mimetype="application" xlink:href="0b97.pdf">
<label>Apêndice B –</label>
<caption>
<title>Equivalência entre o Princípio de Maupertuis (mecânica do ponto material) e de Fermat (Ótica) no contexto não-relativístico.</title>
</caption>
</supplementary-material>
</p>
</app>
</app-group></back></article>

        """
        )
        xmltree = xml_utils.get_xml_tree(data)

        expected = [
            ('suppl01', 'c834.pdf'),
            ('suppl02', '0b97.pdf'),
        ]

        for i, item in enumerate(SupplementaryMaterials(xmltree).items):
            with self.subTest(i):
                self.assertEqual(item.id, expected[i][0])
                self.assertEqual(item.name, expected[i][1])

