from unittest import TestCase

from packtools.sps.utils import xml_utils

from packtools.sps.models.article_assets import ArticleAssets


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
        None: [
          '1234-5678-rctb-45-05-0110-m01.mp4',
        ],
        'f01': [
          'original.tif',
          'ampliada.png',
          'miniatura.jpg',
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
        None: [
          '1234-5678-rctb-45-05-0110-e04.tif',
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
          'original.tif',
          'ampliada.png',
          'miniatura.jpg',
        ],
        'f03': [
          '1234-5678-rctb-45-05-0110-gf03.tiff',
          '1234-5678-rctb-45-05-0110-gf03.png',
          '1234-5678-rctb-45-05-0110-gf03.thumbnail.jpg',
        ],
        None: [
          '1234-5678-rctb-45-05-0110-e04.tif',
          '1234-5678-rctb-45-05-0110-m01.mp4',
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
        '1471-2105-1-1-s1.pdf',
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
          '1471-2105-1-1-s1.pdf',
        ],
        None: [
          '1234-5678-rctb-45-05-0110-m01.mp4',
        ],
        'f01': [
          'original.tif',
          'ampliada.png',
          'miniatura.jpg',
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


    def test_article_assets_with_multiple_supplementary_material(self):
      data = open('tests/sps/fixtures/document-with-supplementary-material.xml').read()
      xmltree = xml_utils.get_xml_tree(data)

      expected = {
        'f1': [
          'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/256bcf2e607f18b0bb3842a31332f6b48620cb09.tif',
          'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/c00655410885461df4a98dd77860b81b2e5baa2c.png',
          'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/ebd30641f55d890debe55743b8e2946135c74140.jpg',
        ],
        'f2': [
          'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/b784533145d2f1557a7df00e05e5c6207fc57e2a.tif',
          'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/b298055fb49aba04fa94a1287ed4c38c0680ccf7.png',
          'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/c0a10dd209a9da0ef40f92f070ee6c77b0ca220b.jpg',
        ],
        'f3': [
          'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/14717caba8b886eddbbc9e1e4a8c579631730187.tif',
          'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/b0b01286ff114d6eda85f9a5afb1217d164e32b5.png',
          'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/b03ad3e4bced80bf0a81dfe12fbe6e567982414b.jpg',
        ],
        'f4': [
          'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/407a7771f32d6364ee6536278a011a2c05da3339.tif',
          'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/c1ba665e5e0731d623095779a2d4099c808e776b.png',
          'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/f1da586984d4176883f92f2fb28e9abea946b8d2.jpg',
        ],
        'suppl01': [
          'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/e738857c8fb8bc085b766a812bbe73277c67d346.pdf',
        ],
        'suppl02': [
          'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/b72942b47698183bf992f1ad8cebdf61d346e0cf.xls',
        ],
        'suppl03': [
          'https://minio.scielo.br/documentstore/1676-0611/GJq3kzJLQw876pxRdSrhmQG/ffc50de0245a936540df9f98b7de123c8c597cbf.pdf',
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
