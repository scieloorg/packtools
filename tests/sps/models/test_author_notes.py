from unittest import TestCase
from lxml import etree
from packtools.sps.models.author_notes import ArticleAuthorNotes


class AuthorNotesTest(TestCase):
    XML = (
        '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
        'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
        '<front>'
        '<author-notes>'
        '<corresp id="cor1">'
        '<label>*</label>'
        '<title>Corresponding Author</title>'
        '<bold>John Doe</bold>'
        '</corresp>'
        '<fn id="fn1">'
        '<label>1</label>'
        '<p>This author contributed equally to the work.</p>'
        '</fn>'
        '<fn id="fn3">'
        '<label>3</label>'
        '<p>This author received funding for the project.</p>'
        '</fn>'
        '</author-notes>'
        '</front>'
        '<sub-article article-type="translation" xml:lang="en">'
        '<front-stub>'
        '<author-notes>'
        '<corresp id="cor2">'
        '<label>*</label>'
        '<title>Corresponding Author</title>'
        '<bold>Jane Doe</bold>'
        '</corresp>'
        '<fn id="fn2">'
        '<label>2</label>'
        '<p>This author is the principal investigator.</p>'
        '</fn>'
        '<fn id="fn4">'
        '<label>4</label>'
        '<p>This author provided critical revisions to the manuscript.</p>'
        '</fn>'
        '</author-notes>'
        '</front-stub>'
        '</sub-article>'
        '</article>'
    )

    def setUp(self):
        self.xml_tree = etree.fromstring(self.XML)
        self.author_notes = ArticleAuthorNotes(self.xml_tree)

    def test_article_author_notes(self):
        # Verifica estrutura básica do retorno
        data = self.author_notes.article_author_notes()

        self.assertIn("corresp_data", data)
        self.assertIn("fns", data)

        # Verifica conteúdo de corresp_data
        corresp_data = list(data["corresp_data"])
        self.assertEqual(len(corresp_data), 1)

        corresp = corresp_data[0]
        self.assertIn("corresp", corresp)
        self.assertIn("corresp_label", corresp)
        self.assertIn("corresp_title", corresp)
        self.assertIn("corresp_bold", corresp)

        self.assertEqual(corresp["corresp"], "*Corresponding AuthorJohn Doe")
        self.assertEqual(corresp["corresp_label"], "*")
        self.assertEqual(corresp["corresp_title"], "Corresponding Author")
        self.assertEqual(corresp["corresp_bold"], "John Doe")

        # Verifica conteúdo de fns
        fns = list(data["fns"])
        self.assertEqual(len(fns), 2)

        # Verifica primeiro fn
        fn1 = fns[0]
        self.assertIn("fn_id", fn1)
        self.assertIn("fn_label", fn1)
        self.assertIn("fn_text", fn1)

        self.assertEqual(fn1["fn_id"], "fn1")
        self.assertEqual(fn1["fn_label"], "1")
        self.assertEqual(fn1["fn_text"], "1This author contributed equally to the work.")

        # Verifica segundo fn
        fn2 = fns[1]
        self.assertIn("fn_id", fn2)
        self.assertIn("fn_label", fn2)
        self.assertIn("fn_text", fn2)

        self.assertEqual(fn2["fn_id"], "fn3")
        self.assertEqual(fn2["fn_label"], "3")
        self.assertEqual(fn2["fn_text"], "3This author received funding for the project.")

    def test_sub_article_author_notes(self):
        # Verifica estrutura básica do retorno
        sub_articles = list(self.author_notes.sub_article_author_notes())
        self.assertEqual(len(sub_articles), 1)

        sub_article = sub_articles[0]
        self.assertIn("corresp_data", sub_article)
        self.assertIn("fns", sub_article)

        # Verifica conteúdo de corresp_data no sub-artigo
        corresp_data = list(sub_article["corresp_data"])
        self.assertEqual(len(corresp_data), 1)

        corresp = corresp_data[0]
        self.assertIn("corresp", corresp)
        self.assertIn("corresp_label", corresp)
        self.assertIn("corresp_title", corresp)
        self.assertIn("corresp_bold", corresp)

        self.assertEqual(corresp["corresp"], "*Corresponding AuthorJane Doe")
        self.assertEqual(corresp["corresp_label"], "*")
        self.assertEqual(corresp["corresp_title"], "Corresponding Author")
        self.assertEqual(corresp["corresp_bold"], "Jane Doe")

        # Verifica conteúdo de fns no sub-artigo
        fns = list(sub_article["fns"])
        self.assertEqual(len(fns), 2)

        # Verifica primeiro fn
        fn1 = fns[0]
        self.assertIn("fn_id", fn1)
        self.assertIn("fn_label", fn1)
        self.assertIn("fn_text", fn1)

        self.assertEqual(fn1["fn_id"], "fn2")
        self.assertEqual(fn1["fn_label"], "2")
        self.assertEqual(fn1["fn_text"], "2This author is the principal investigator.")

        # Verifica segundo fn
        fn2 = fns[1]
        self.assertIn("fn_id", fn2)
        self.assertIn("fn_label", fn2)
        self.assertIn("fn_text", fn2)

        self.assertEqual(fn2["fn_id"], "fn4")
        self.assertEqual(fn2["fn_label"], "4")
        self.assertEqual(fn2["fn_text"], "4This author provided critical revisions to the manuscript.")
