from unittest import TestCase

from packtools.sps.utils import xml_utils

from packtools.sps.models.article_assets import ArticleAssets


class ArticleAssetsTest(TestCase):
    def test_article_assets_with_one_figure(self):
      data = open('tests/sps/fixtures/document3.xml').read()
      xmltree = xml_utils.get_xml_tree(data)

      expected = {None: ['document3-xdadaf.jpg']}
      obtained = {}

      for asset in ArticleAssets(xmltree).article_assets:
        a_id = asset.id
        a_name = asset.name

        if a_id not in obtained:
          obtained[a_id] = []

        obtained[a_id].append(a_name)

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

      expected = {'f01': ['original.tif', 'ampliada.png', 'miniatura.jpg']}
      obtained = {}

      for asset in ArticleAssets(xmltree).article_assets:
        a_id = asset.id
        a_name = asset.name

        if a_id not in obtained:
          obtained[a_id] = []

        obtained[a_id].append(a_name)

      self.assertDictEqual(expected, obtained)


    def test_article_assets_with_multiple_figures(self):
      data = open('tests/sps/fixtures/document2.xml').read()
      xmltree = xml_utils.get_xml_tree(data)

      expected = {
        'f01': [
          'https://minio.scielo.br/documentstore/1414-431X/ywDM7t6mxHzCRWp7kGF9rXQ/fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg',
          'https://minio.scielo.br/documentstore/1414-431X/ywDM7t6mxHzCRWp7kGF9rXQ/0c10c88b56f3f9b4f4eccfe9ddbca3fd581aac1b.jpg'
        ],
        'f02': [
          'https://minio.scielo.br/documentstore/1414-431X/ywDM7t6mxHzCRWp7kGF9rXQ/afd520e3ff23a23f2c973bbbaa26094e9e50f487.jpg',
          'https://minio.scielo.br/documentstore/1414-431X/ywDM7t6mxHzCRWp7kGF9rXQ/c2e5f2b77881866ef9820b03e99b3fedbb14cb69.jpg'
        ]
      }
      obtained = {}

      for asset in ArticleAssets(xmltree).article_assets:
        a_id = asset.id
        a_name = asset.name

        if a_id not in obtained:
          obtained[a_id] = []

        obtained[a_id].append(a_name)

      self.assertDictEqual(expected, obtained)


    def test_article_assets_images_outside_figure(self):
      data = open('tests/fixtures/htmlgenerator/alternatives/imagens_fora_de_fig.xml').read()
      xmltree = xml_utils.get_xml_tree(data)

      expected = {
        None: [
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/8d6031a105ac49f92d2bac1dab55785ec62ed139.tif',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/d9b80494cba33a6e60786bdfc56a0c9c048125af.png',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/352c2528e5e3489f3d2c9d4a958bccd776b2667d.jpg',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/6c7e45494816692122f9467ee9b5ee7a88f86e01.tif',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/c225686bbd2607bacabd946fcb55b30a10b9e5d2.png',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/d414c6174f0a5069a63c1f4450df8011666a1e35.jpg',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/7172c66d1c5fa56dc230efa7123dea014f21e62f.tif',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/0d201e31cd5186c2a53f178bfd0509401f2d1ca6.png',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/0be8783d8e1eb3e4b98cf803ff71ce829a652a1b.jpg',
        ],
        # figures that belong to subarticle s1
        's1': [
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/9a4a202884a687ad4858fc95fbf3be801e63215b.tif',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/d9b80494cba33a6e60786bdfc56a0c9c048125af.png',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/352c2528e5e3489f3d2c9d4a958bccd776b2667d.jpg',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/1fdbee345fae2065d9bd0fd0b4b09a4f77e99e90.tif',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/c225686bbd2607bacabd946fcb55b30a10b9e5d2.png',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/d414c6174f0a5069a63c1f4450df8011666a1e35.jpg',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/aa495447d05a9156d0d15f5f95f8890ee1d55743.tif',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/0d201e31cd5186c2a53f178bfd0509401f2d1ca6.png',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/0be8783d8e1eb3e4b98cf803ff71ce829a652a1b.jpg',
        ],
        # figures that belong to subarticle s2
        's2': [
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/e971ae023bce641ced89dfbdc40d62be94c4c738.tif',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/d9b80494cba33a6e60786bdfc56a0c9c048125af.png',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/352c2528e5e3489f3d2c9d4a958bccd776b2667d.jpg',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/30d718ea67b77dd98bcda9d3acba9cb296fcba9e.tif',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/c225686bbd2607bacabd946fcb55b30a10b9e5d2.png',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/d414c6174f0a5069a63c1f4450df8011666a1e35.jpg',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/b824ebf96bd03d51ee26edc6c3807c3092bf1901.tif',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/0d201e31cd5186c2a53f178bfd0509401f2d1ca6.png',
          'https://minio.scielo.br/documentstore/1518-8345/L34w8qg8ccfQxW79FZH3Bnh/0be8783d8e1eb3e4b98cf803ff71ce829a652a1b.jpg',
        ]
      }
      obtained = {}

      for asset in ArticleAssets(xmltree).article_assets:
        a_id = asset.id
        a_name = asset.name

        if a_id not in obtained:
          obtained[a_id] = []

        obtained[a_id].append(a_name)

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

      expected = {None: ['1234-5678-rctb-45-05-0110-m01.mp4'],}
      obtained = {}

      for asset in ArticleAssets(xmltree).article_assets:
        a_id = asset.id
        a_name = asset.name

        if a_id not in obtained:
          obtained[a_id] = []

        obtained[a_id].append(a_name)

      self.assertDictEqual(expected, obtained)
  

