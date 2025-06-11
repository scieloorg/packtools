from unittest import TestCase
from lxml import etree

from packtools.sps.utils import xml_utils
from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles, Fulltext


class ArticleAndSubarticlesTest(TestCase):
    def test_main_lang(self):
        data = """<article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en"></article>"""
        xmltree = xml_utils.get_xml_tree(data)

        expected = "en"
        obtained = ArticleAndSubArticles(xmltree).main_lang

        self.assertEqual(expected, obtained)

    def test_all_lang(self):
        with open(
            "tests/samples/article-abstract-en-sub-articles-pt-es.xml", "r"
        ) as data:
            xmltree = xml_utils.get_xml_tree(data.read())

        expected = ["en", "pt", "es"]
        obtained = [d["lang"] for d in ArticleAndSubArticles(xmltree).data]

        self.assertListEqual(expected, obtained)

    def test_main_article_type(self):
        data = """<article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en"></article>"""
        xmltree = xml_utils.get_xml_tree(data)

        expected = "research-article"
        obtained = ArticleAndSubArticles(xmltree).main_article_type

        self.assertEqual(expected, obtained)

    def test_all_article_type(self):
        with open(
            "tests/samples/article-abstract-en-sub-articles-pt-es.xml", "r"
        ) as data:
            xmltree = xml_utils.get_xml_tree(data.read())

        expected = ["research-article", "translation", "translation"]
        obtained = [d["article_type"] for d in ArticleAndSubArticles(xmltree).data]

        self.assertListEqual(expected, obtained)

    def test_elements_order(self):
        self.maxDiff = None
        with open(
            "tests/samples/artigo-com-traducao-e-pareceres-traduzidos.xml", "r"
        ) as data:
            xmltree = xml_utils.get_xml_tree(data.read())

        expected = [
            {
                "article_id": None,
                "article_type": "research-article",
                "lang": "pt",
                "line_number": 2,
                "subject": "ARTIGOS",
                "parent_name": "article",
                "doi": "10.1590/2176-4573p59270",
            },
            {
                "article_id": "s2",
                "article_type": "reviewer-report",
                "lang": "pt",
                "line_number": 93,
                "subject": "Pareceres",
                "parent_name": "sub-article",
                "doi": None,
            },
            {
                "article_id": "s3",
                "article_type": "reviewer-report",
                "lang": "pt",
                "line_number": 141,
                "subject": "Pareceres",
                "parent_name": "sub-article",
                "doi": None,
            },
            {
                "article_id": "s1",
                "article_type": "translation",
                "lang": "en",
                "line_number": 189,
                "subject": "ARTICLES",
                "parent_name": "sub-article",
                "doi": "10.1590/2176-4573e59270",
            },
            {
                "article_id": "s5",
                "article_type": "reviewer-report",
                "lang": "en",
                "line_number": 233,
                "subject": "Reviews",
                "parent_name": "sub-article",
                "doi": None,
            },
            {
                "article_id": "s6",
                "article_type": "reviewer-report",
                "lang": "en",
                "line_number": 271,
                "subject": "Reviews",
                "parent_name": "sub-article",
                "doi": None,
            },
        ]
        obtained = [d for d in ArticleAndSubArticles(xmltree).data]

        self.assertListEqual(expected, obtained)

    def test_main_specific_use(self):
        data = """<article xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" 
        dtd-version="1.1" specific-use="sps-1.9" xml:lang="en"></article>"""
        xmltree = xml_utils.get_xml_tree(data)

        expected = 'sps-1.9'
        obtained = ArticleAndSubArticles(xmltree).specific_use

        self.assertEqual(expected, obtained)

    def test_main_dtd_version(self):
        data = """<article xmlns:mml="http://www.w3.org/1998/Math/MathML" 
        xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" 
        dtd-version="1.1" specific-use="sps-1.9" xml:lang="en"></article>"""
        xmltree = xml_utils.get_xml_tree(data)

        expected = '1.1'
        obtained = ArticleAndSubArticles(xmltree).dtd_version

        self.assertEqual(expected, obtained)

    def test_main_article_subject(self):
        with open(
            "tests/samples/article-abstract-en-sub-articles-pt-es.xml", "r"
        ) as data:
            xmltree = xml_utils.get_xml_tree(data.read())

        expected = "Original Article"
        obtained = ArticleAndSubArticles(xmltree).main_subject

        self.assertEqual(expected, obtained)

    def test_all_article_subject(self):
        self.maxDiff = None
        with open(
            "tests/samples/article-abstract-en-sub-articles-pt-es.xml", "r"
        ) as data:
            xmltree = xml_utils.get_xml_tree(data.read())

        expected = ["Original Article", "Artigo Original", "Artículo Original"]
        obtained = [d["subject"] for d in ArticleAndSubArticles(xmltree).data]

        self.assertListEqual(expected, obtained)


class TestFulltext(TestCase):
    def setUp(self):
        """
        Configura o XML básico para os testes
        """
        self.xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink"
                xmlns:xml="http://www.w3.org/XML/1998/namespace"
                article-type="research-article"
                xml:lang="en"
                id="123">
            <front>
                <article-meta/>
            </front>
            <body>
                <sec/>
            </body>
            <back>
                <ref-list/>
            </back>
        </article>"""
        self.node = etree.fromstring(self.xml)
        self.fulltext = Fulltext(self.node)

    def test_init(self):
        """Testa inicialização básica"""
        self.assertEqual(self.fulltext.tag, "article")
        self.assertEqual(self.fulltext.article_type, "research-article")
        self.assertEqual(self.fulltext.lang, "en")
        self.assertEqual(self.fulltext.id, "123")

    def test_front_article(self):
        """Testa propriedade front para article"""
        self.assertIsNotNone(self.fulltext.front)
        self.assertEqual(self.fulltext.front.tag, "front")

    def test_front_sub_article(self):
        """Testa propriedade front para sub-article"""
        xml_sub = """
        <sub-article article-type="translation" xml:lang="pt" id="s1">
            <front-stub>
                <article-meta/>
            </front-stub>
        </sub-article>"""
        node_sub = etree.fromstring(xml_sub)
        fulltext_sub = Fulltext(node_sub)

        self.assertIsNotNone(fulltext_sub.front)
        self.assertEqual(fulltext_sub.front.tag, "front-stub")

    def test_body(self):
        """Testa propriedade body"""
        self.assertIsNotNone(self.fulltext.body)
        self.assertEqual(self.fulltext.body.tag, "body")

    def test_back(self):
        """Testa propriedade back"""
        self.assertIsNotNone(self.fulltext.back)
        self.assertEqual(self.fulltext.back.tag, "back")

    def test_sub_articles(self):
        """Testa propriedade sub_articles"""
        xml = """
        <article>
            <front/>
            <sub-article article-type="translation" xml:lang="es" id="s1">
                <front-stub/>
            </sub-article>
            <sub-article article-type="other" xml:lang="fr" id="s2">
                <front-stub/>
            </sub-article>
        </article>"""
        node = etree.fromstring(xml)
        fulltext = Fulltext(node)

        self.assertEqual(len(fulltext.sub_articles), 2)
        self.assertEqual(fulltext.sub_articles[0].tag, "sub-article")
        self.assertEqual(fulltext.sub_articles[1].tag, "sub-article")

    def test_translations(self):
        """Testa propriedade translations"""
        xml = """
        <article>
            <front/>
            <sub-article article-type="translation" xml:lang="es" id="s1">
                <front-stub/>
            </sub-article>
            <sub-article article-type="other" xml:lang="fr" id="s2">
                <front-stub/>
            </sub-article>
        </article>"""
        node = etree.fromstring(xml)
        fulltext = Fulltext(node)

        self.assertEqual(len(fulltext.translations), 1)
        self.assertEqual(fulltext.translations[0].get("article-type"), "translation")
        self.assertEqual(
            fulltext.translations[0].get("{http://www.w3.org/XML/1998/namespace}lang"),
            "es",
        )

    def test_not_translations(self):
        """Testa propriedade not_translations"""
        xml = """
        <article>
            <front/>
            <sub-article article-type="translation" xml:lang="es" id="s1">
                <front-stub/>
            </sub-article>
            <sub-article article-type="other" xml:lang="fr" id="s2">
                <front-stub/>
            </sub-article>
        </article>"""
        node = etree.fromstring(xml)
        fulltext = Fulltext(node)

        self.assertEqual(len(fulltext.not_translations), 1)
        self.assertEqual(fulltext.not_translations[0].get("article-type"), "other")
        self.assertEqual(
            fulltext.not_translations[0].get(
                "{http://www.w3.org/XML/1998/namespace}lang"
            ),
            "fr",
        )

    def test_attribs(self):
        """Testa propriedade attribs"""
        expected = {
            "tag": "article",
            "id": "123",
            "lang": "en",
            "article_type": "research-article",
        }
        self.assertEqual(self.fulltext.attribs, expected)

    def test_attribs_parent_prefixed(self):
        """Testa propriedade attribs_parent_prefixed"""
        expected = {
            "parent": "article",
            "parent_id": "123",
            "parent_lang": "en",
            "parent_article_type": "research-article",
            "original_article_type": "research-article",
        }
        self.assertEqual(self.fulltext.attribs_parent_prefixed, expected)

    def test_fulltexts(self):
        """Testa propriedade fulltexts"""
        xml = """
        <article article-type="research-article" xml:lang="en" id="123">
            <front/>
            <sub-article article-type="translation" xml:lang="es" id="s1">
                <front-stub/>
            </sub-article>
            <sub-article article-type="other" xml:lang="fr" id="s2">
                <front-stub/>
            </sub-article>
        </article>"""
        node = etree.fromstring(xml)
        fulltext = Fulltext(node)
        data = fulltext.fulltexts

        # Verifica estrutura básica
        self.assertIn("attribs", data)
        self.assertIn("attribs_parent_prefixed", data)
        self.assertIn("translations", data)
        self.assertIn("not_translations", data)
        self.assertIn("sub_articles", data)

        # Verifica conteúdo
        self.assertEqual(len(data["translations"]), 1)
        self.assertEqual(len(data["not_translations"]), 1)
        self.assertEqual(len(data["sub_articles"]), 2)

        # Verifica se as traduções são instâncias de Fulltext
        self.assertIsInstance(data["translations"][0], Fulltext)
        self.assertIsInstance(data["not_translations"][0], Fulltext)
        self.assertIsInstance(data["sub_articles"][0], Fulltext)

    def test_missing_optional_attributes(self):
        """Testa inicialização com atributos opcionais ausentes"""
        xml = """
        <article>
            <front/>
        </article>"""
        node = etree.fromstring(xml)
        fulltext = Fulltext(node)

        self.assertIsNone(fulltext.lang)
        self.assertIsNone(fulltext.article_type)
        self.assertIsNone(fulltext.id)

    def test_empty_sections(self):
        """Testa artigo sem seções body e back"""
        xml = """
        <article>
            <front/>
        </article>"""
        node = etree.fromstring(xml)
        fulltext = Fulltext(node)

        self.assertIsNotNone(fulltext.front)
        self.assertIsNone(fulltext.body)
        self.assertIsNone(fulltext.back)
