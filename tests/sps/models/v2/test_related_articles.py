"""
<related-article ext-link-type="doi" id="A01" related-article-type="commentary-article" xlink:href="10.1590/0101-3173.2022.v45n1.p139">
Referência do artigo comentado: FREITAS, J. H. de. Cinismo e indiferenciación: la huella de Glucksmann en
<italic>El coraje de la verdad</italic>
de Foucault.
<bold>Trans/form/ação</bold>
: revista de Filosofia da Unesp, v. 45, n. 1, p. 139-158, 2022.
</related-article>
"""

from unittest import TestCase

from packtools.sps.utils import xml_utils
from packtools.sps.models.v2.related_articles import RelatedArticle, RelatedArticlesByNode, RelatedArticles


class RelatedArticleTest(TestCase):
    def test_related_article(self):
        self.maxDiff = None
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
              <related-article ext-link-type="doi" id="A01" related-article-type="commentary-article" xlink:href="10.1590/0101-3173.2022.v45n1.p139">
                Referência do artigo comentado: FREITAS, J. H. de. Cinismo e indiferenciación: la huella de Glucksmann en
                <italic>El coraje de la verdad</italic>
                de Foucault.
                <bold>Trans/form/ação</bold>
                : revista de Filosofia da Unesp, v. 45, n. 1, p. 139-158, 2022.
                </related-article>
                </front>
            </article>
            """
        obtained = RelatedArticle(xml_utils.get_xml_tree(xml).xpath(".//related-article")[0]).data()
        expected = {
            "ext-link-type": "doi",
            "id": "A01",
            "related-article-type": "commentary-article",
            "href": "10.1590/0101-3173.2022.v45n1.p139",
            "text": "Referência do artigo comentado: FREITAS, J. H. de. Cinismo e indiferenciación: la huella de "
                    "Glucksmann en <i>El coraje de la verdad</i> de Foucault. Trans/form/ação : revista de Filosofia "
                    "da Unesp, v. 45, n. 1, p. 139-158, 2022.",
            'full_tag': '<related-article xmlns:xlink="http://www.w3.org/1999/xlink" ext-link-type="doi" id="A01" '
                        'related-article-type="commentary-article" xlink:href="10.1590/0101-3173.2022.v45n1.p139">',
        }
        self.assertDictEqual(obtained, expected)


class RelatedArticlesByNodeTest(TestCase):
    def test_related_articles(self):
        self.maxDiff = None
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="article-commentary" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">
            <front>
            <article-meta>
            <related-article ext-link-type="doi" id="A01" related-article-type="commentary-article" xlink:href="10.1590/0101-3173.2022.v45n1.p139">
            Referência do artigo comentado: FREITAS, J. H. de. Cinismo e indiferenciación: la huella de Glucksmann en
            <italic>El coraje de la verdad</italic>
            de Foucault.
            <bold>Trans/form/ação</bold>
            : revista de Filosofia da Unesp, v. 45, n. 1, p. 139-158, 2022.
            </related-article>
            </article-meta>
            </front>
            </article>
            """
        obtained = list(RelatedArticlesByNode(xml_utils.get_xml_tree(xml).find(".")).related_articles())
        expected = [
            {
                "parent": "article",
                "parent_article_type": "article-commentary",
                "parent_id": None,
                "parent_lang": "pt",
                "ext-link-type": "doi",
                "id": "A01",
                "related-article-type": "commentary-article",
                "href": "10.1590/0101-3173.2022.v45n1.p139",
                "text": "Referência do artigo comentado: FREITAS, J. H. de. Cinismo e indiferenciación: la huella de "
                        "Glucksmann en <i>El coraje de la verdad</i> de Foucault. Trans/form/ação : revista de Filosofia "
                        "da Unesp, v. 45, n. 1, p. 139-158, 2022.",
                'full_tag': '<related-article xmlns:xlink="http://www.w3.org/1999/xlink" ext-link-type="doi" id="A01" '
                            'related-article-type="commentary-article" xlink:href="10.1590/0101-3173.2022.v45n1.p139">',
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(item, expected[i])


class RelatedArticlesTest(TestCase):
    def setUp(self):
        self.xml_tree = xml_utils.get_xml_tree("tests/fixtures/htmlgenerator/related-article/varias_erratas.xml")

    def test_article(self):
        obtained = list(RelatedArticles(self.xml_tree).article())
        expected = [
            {
                'ext-link-type': 'doi',
                'href': '10.1590/s1413-65382620000100001',
                'id': 'RA1',
                'parent': 'article',
                'parent_article_type': 'correction',
                'parent_id': None,
                'parent_lang': 'pt',
                'related-article-type': 'corrected-article',
                'text': '',
                'full_tag': '<related-article xmlns:xlink="http://www.w3.org/1999/xlink" id="RA1" '
                            'related-article-type="corrected-article" ext-link-type="doi" '
                            'xlink:href="10.1590/s1413-65382620000100001" />',
            },
            {
                'ext-link-type': 'doi',
                'href': '10.1590/s1413-65382620000100009',
                'id': 'RA9',
                'parent': 'article',
                'parent_article_type': 'correction',
                'parent_id': None,
                'parent_lang': 'pt',
                'related-article-type': 'corrected-article',
                'text': '',
                'full_tag': '<related-article xmlns:xlink="http://www.w3.org/1999/xlink" id="RA9" '
                            'related-article-type="corrected-article" ext-link-type="doi" '
                            'xlink:href="10.1590/s1413-65382620000100009" />',
            },

        ]
        self.assertEqual(len(obtained), 9)
        self.assertDictEqual(obtained[0], expected[0])
        self.assertDictEqual(obtained[8], expected[1])

    def test_sub_articles(self):
        obtained = list(RelatedArticles(self.xml_tree).sub_articles())
        expected = [
            {
                'ext-link-type': 'doi',
                'href': '10.1590/s1413-65382620000100001',
                'id': 'RA10',
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': "s1",
                'parent_lang': 'en',
                'related-article-type': 'corrected-article',
                'text': '',
                'full_tag': '<related-article xmlns:xlink="http://www.w3.org/1999/xlink" id="RA10" '
                            'related-article-type="corrected-article" ext-link-type="doi" '
                            'xlink:href="10.1590/s1413-65382620000100001" />',
            },
            {
                'ext-link-type': 'doi',
                'href': '10.1590/s1413-65382620000100009',
                'id': 'RA18',
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': "s1",
                'parent_lang': 'en',
                'related-article-type': 'corrected-article',
                'text': '',
                'full_tag': '<related-article xmlns:xlink="http://www.w3.org/1999/xlink" id="RA18" '
                            'related-article-type="corrected-article" ext-link-type="doi" '
                            'xlink:href="10.1590/s1413-65382620000100009" />',
            },

        ]
        self.assertEqual(len(obtained), 9)
        self.assertDictEqual(obtained[0], expected[0])
        self.assertDictEqual(obtained[8], expected[1])

    def test_related_articles(self):
        obtained = list(RelatedArticles(self.xml_tree).related_articles())

        self.assertEqual(len(obtained), 18)
