from unittest import TestCase
from lxml import etree
from packtools.sps.models.fn import ArticleFns


class FnGroupsTest(TestCase):
    XML = (
        '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
        'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
        '<front>'
        '<article-meta>'
        '<fn-group>'
        '<fn fn-type="financial-disclosure" id="fn01">'
        '<label>1</label>'
        '<p>Declaração de financiamento: sim</p>'
        '</fn>'
        '<fn fn-type="presented-at" id="fn02">'
        '<label>**</label>'
        '<p>Artigo foi apresentado na XVIII Conferência Internacional de Biblioteconomia 2014</p>'
        '</fn>'
        '</fn-group>'
        '</article-meta>'
        '</front>'
        '<sub-article article-type="translation" xml:lang="en">'
        '<front-stub>'
        '<fn-group>'
        '<fn fn-type="financial-disclosure" id="fn03">'
        '<label>1</label>'
        '<p>Funding statement: yes</p>'
        '</fn>'
        '<fn fn-type="presented-at" id="fn04">'
        '<label>**</label>'
        '<p>The article was presented at the XVIII International Conference on Library Science 2014</p>'
        '</fn>'
        '</fn-group>'
        '</front-stub>'
        '</sub-article>'
        '</article>'
    )

    def setUp(self):
        self.xml_tree = etree.fromstring(self.XML)
        self.fns = ArticleFns(self.xml_tree)

    def test_article_fn_groups_notes(self):
        obtained = list(self.fns.article_fn_groups_notes())

        # Verifica estrutura básica
        for fn_data in obtained:
            with self.subTest(fn_id=fn_data.get("fn_id")):
                self.assertIn("fn_bold", fn_data)
                self.assertIn("fn_id", fn_data)
                self.assertIn("fn_label", fn_data)
                self.assertIn("fn_parent", fn_data)
                self.assertIn("fn_text", fn_data)
                self.assertIn("fn_title", fn_data)
                self.assertIn("fn_type", fn_data)
                self.assertIn("parent", fn_data)
                self.assertIn("parent_article_type", fn_data)
                self.assertIn("parent_id", fn_data)
                self.assertIn("parent_lang", fn_data)

        # Verifica quantidade de itens
        self.assertEqual(len(obtained), 2)

        # Verifica conteúdo específico
        self.assertEqual(obtained[0]["fn_id"], "fn01")
        self.assertEqual(obtained[0]["fn_type"], "financial-disclosure")
        self.assertEqual(obtained[0]["parent_article_type"], "research-article")
        self.assertEqual(obtained[1]["fn_id"], "fn02")
        self.assertEqual(obtained[1]["fn_type"], "presented-at")
        self.assertEqual(obtained[1]["fn_text"], "**Artigo foi apresentado na XVIII Conferência Internacional de Biblioteconomia 2014")

    def test_sub_article_fn_groups_notes(self):
        obtained = list(self.fns.sub_article_fn_groups_notes())

        # Verifica estrutura básica
        for fn_data in obtained:
            with self.subTest(fn_id=fn_data.get("fn_id")):
                self.assertIn("fn_bold", fn_data)
                self.assertIn("fn_id", fn_data)
                self.assertIn("fn_label", fn_data)
                self.assertIn("fn_parent", fn_data)
                self.assertIn("fn_text", fn_data)
                self.assertIn("fn_title", fn_data)
                self.assertIn("fn_type", fn_data)
                self.assertIn("parent", fn_data)
                self.assertIn("parent_article_type", fn_data)
                self.assertIn("parent_id", fn_data)
                self.assertIn("parent_lang", fn_data)

        # Verifica quantidade de itens
        self.assertEqual(len(obtained), 2)

        # Verifica conteúdo específico
        self.assertEqual(obtained[0]["fn_id"], "fn03")
        self.assertEqual(obtained[0]["fn_type"], "financial-disclosure")
        self.assertEqual(obtained[0]["parent_lang"], "en")
        self.assertEqual(obtained[1]["fn_id"], "fn04")
        self.assertEqual(obtained[1]["fn_type"], "presented-at")
        self.assertEqual(obtained[1]["fn_text"], "**The article was presented at the XVIII International Conference on Library Science 2014")
