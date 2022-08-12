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
