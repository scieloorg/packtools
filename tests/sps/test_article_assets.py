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
