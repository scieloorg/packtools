from unittest import TestCase

from packtools.sps.utils import xml_utils

from packtools.sps.models.article_renditions import ArticleRenditions


def generate_xmltree(extralang1, extralang2=None, extralang3=None):
    xml = """
    <article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="pt">
        <front>
            <article-meta>
                {0}
            </article-meta>
        </front>
        {1}
        {2}
        <body>
            <sec><p>The Eh measurements... <xref ref-type="fig" rid="f01">Figura 1</xref>:</p></sec>
        </body>
    </article>
    """
    return xml_utils.get_xml_tree(xml.format(extralang1, extralang2, extralang3))


class ArticleRenditionsTest(TestCase):
    def test_article_assets_with_one_language(self):
      data = """<article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang='es'></article>"""
      xmltree = xml_utils.get_xml_tree(data)

      expected = ['es']
      obtained = [r.language for r in ArticleRenditions(xmltree).article_renditions]

      self.assertListEqual(expected, obtained)


    def test_article_assets_with_two_languages(self):
      snippet = """<sub-article xml:lang='es' article-type='translation'><front-stub></front-stub></sub-article>"""
      xmltree = generate_xmltree(snippet)

      expected = ['pt', 'es']
      obtained = [r.language for r in ArticleRenditions(xmltree).article_renditions]

      self.assertListEqual(expected, obtained)
