from unittest import TestCase
from io import BytesIO

from lxml import etree
from packtools.sps.models.related_articles import RelatedItems, FulltextRelatedArticles


def create_xml_tree(xml_content):
    return etree.parse(BytesIO(xml_content.encode("utf-8")))


class TestArticleRelatedItems(TestCase):
    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">'
            "<front>"
            "<article-meta>"
            '<related-article ext-link-type="doi" id="A01" related-article-type="commentary-article" xlink:href="10.1590/0101-3173.2022.v45n1.p139">Referência do artigo comentado: FREITAS, J. H. de. <italic>Some italic text</italic> Sample text <bold>Journal Name</bold>: additional details</related-article>'
            "</article-meta>"
            "</front>"
            "</article>"
        )
        self.xml_tree = create_xml_tree(xml)
        self.related_items = RelatedItems(self.xml_tree)

    def test_article_related_articles(self):
        items = list(self.related_items.related_articles)
        xml = '<related-article ext-link-type="doi" id="A01" related-article-type="commentary-article" xlink:href="10.1590/0101-3173.2022.v45n1.p139">Referência do artigo comentado: FREITAS, J. H. de. <italic>Some italic text</italic> Sample text <bold>Journal Name</bold>: additional details</related-article>'
        self.assertEqual(len(items), 1)
        item = items[0]
        self.assertEqual(item["id"], "A01")
        self.assertEqual(item["ext-link-type"], "doi")
        self.assertEqual(item["related-article-type"], "commentary-article")
        self.assertEqual(item["href"], "10.1590/0101-3173.2022.v45n1.p139")
        self.assertEqual(
            "Referência do artigo comentado: FREITAS, J. H. de. Some italic text Sample text Journal Name: additional details",
            item["text"],
        )
        self.assertEqual(xml, item["xml"])
        self.assertEqual(item.get("parent_lang"), "en")
        self.assertEqual(item.get("parent_article_type"), "research-article")


class TestSubArticleRelatedItems(TestCase):
    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">'
            '<sub-article article-type="translation" xml:lang="es" id="tr1">'
            "<front-stub>"
            '<related-article ext-link-type="doi" id="B01" related-article-type="translated-article" xlink:href="10.1590/0101-3173.2022.v45n2.p160">Traducción del artículo: <italic>El texto original</italic> Texto de muestra <bold>Nombre de la Revista</bold>: detalles adicionales</related-article>'
            "</front-stub>"
            "</sub-article>"
            "</article>"
        )
        self.xml_tree = create_xml_tree(xml)
        self.related_items = RelatedItems(self.xml_tree)

    def test_sub_article_related_articles(self):
        items = list(self.related_items.related_articles)
        xml = '<related-article ext-link-type="doi" id="B01" related-article-type="translated-article" xlink:href="10.1590/0101-3173.2022.v45n2.p160">Traducción del artículo: <italic>El texto original</italic> Texto de muestra <bold>Nombre de la Revista</bold>: detalles adicionales</related-article>'
        self.assertEqual(len(items), 1)
        item = items[0]
        self.assertEqual(item["id"], "B01")
        self.assertEqual(item["ext-link-type"], "doi")
        self.assertEqual(item["related-article-type"], "translated-article")
        self.assertEqual(item["href"], "10.1590/0101-3173.2022.v45n2.p160")
        self.assertIn("Nombre de la Revista", item["text"])
        self.assertNotIn("bold", item["text"])
        self.assertEqual(xml, item["xml"])
        self.assertEqual(item.get("parent_lang"), "es")
        self.assertEqual(item.get("parent_article_type"), "translation")


class TestMultipleRelatedItems(TestCase):
    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">'
            "<front>"
            "<article-meta>"
            '<related-article ext-link-type="doi" id="A01" related-article-type="commentary-article" xlink:href="10.1590/example1">First reference</related-article>'
            '<related-article ext-link-type="doi" id="A02" related-article-type="corrected-article" xlink:href="10.1590/example2">Second reference</related-article>'
            "</article-meta>"
            "</front>"
            '<sub-article article-type="translation" xml:lang="pt" id="tr2">'
            "<front-stub>"
            '<related-article ext-link-type="doi" id="B01" related-article-type="translated-article" xlink:href="10.1590/example3">Third reference</related-article>'
            "</front-stub>"
            "</sub-article>"
            "</article>"
        )
        self.xml_tree = create_xml_tree(xml)
        self.related_items = RelatedItems(self.xml_tree)

    def test_multiple_related_articles(self):
        items = list(self.related_items.related_articles)

        self.assertEqual(len(items), 3)

        # Check first article
        self.assertEqual(items[0]["id"], "A01")
        self.assertEqual(items[0]["href"], "10.1590/example1")
        self.assertEqual(items[0].get("parent_lang"), "en")
        self.assertEqual(items[0].get("parent_article_type"), "research-article")

        # Check second article
        self.assertEqual(items[1]["id"], "A02")
        self.assertEqual(items[1]["href"], "10.1590/example2")
        self.assertEqual(items[1].get("parent_lang"), "en")
        self.assertEqual(items[1].get("parent_article_type"), "research-article")

        # Check sub-article
        self.assertEqual(items[2]["id"], "B01")
        self.assertEqual(items[2]["href"], "10.1590/example3")
        self.assertEqual(items[2].get("parent_lang"), "pt")
        self.assertEqual(items[2].get("parent_article_type"), "translation")


class TestNoRelatedItems(TestCase):
    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">'
            "<front>"
            "<article-meta>"
            "</article-meta>"
            "</front>"
            "</article>"
        )
        self.xml_tree = create_xml_tree(xml)
        self.related_items = RelatedItems(self.xml_tree)

    def test_no_related_articles(self):
        items = list(self.related_items.related_articles)
        self.assertEqual(len(items), 0)


class TestFulltextRelatedArticlesMainArticle(TestCase):
    """Tests for basic article with related-articles and sub-articles"""

    def setUp(self):
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en" id="a1">
            <front>
                <article-meta>
                    <related-article related-article-type="correction-forward" 
                                   ext-link-type="doi" 
                                   xlink:href="10.1590/123456789" 
                                   id="ra1">Some text</related-article>
                </article-meta>
            </front>
            <sub-article article-type="translation" xml:lang="pt" id="s1">
                <front-stub>
                    <related-article related-article-type="correction-forward"
                                   ext-link-type="doi"
                                   id="ra2">Translation related</related-article>
                </front-stub>
            </sub-article>
            <sub-article article-type="reviewer-report" xml:lang="es" id="s2">
                <front-stub>
                    <related-article related-article-type="reviewer-report-of"
                                   ext-link-type="doi"
                                   id="ra3">Text related</related-article>
                </front-stub>
            </sub-article>
        </article>"""
        self.fulltext = FulltextRelatedArticles(etree.fromstring(xml).find("."))

    def test_parent_data(self):
        expected = {
            "parent": "article",
            "parent_id": "a1",
            "parent_article_type": "research-article",
            "parent_lang": "en",
            "original_article_type": "research-article",
        }
        self.assertEqual(self.fulltext.parent_data, expected)

    def test_related_articles(self):
        related = list(self.fulltext.related_articles)
        self.assertEqual(len(related), 1)

        article = related[0]
        self.assertEqual(article["related-article-type"], "correction-forward")
        self.assertEqual(article["ext-link-type"], "doi")
        self.assertEqual(article["href"], "10.1590/123456789")
        self.assertEqual(article["id"], "ra1")
        self.assertEqual(article["text"], "Some text")
        self.assertIn("xml", article)
        self.assertEqual(article["original_article_type"], "research-article")

    def test_fulltexts(self):
        sub_articles = list(self.fulltext.fulltexts)
        self.assertEqual(len(sub_articles), 2)

        # Test translation sub-article
        translation = sub_articles[0]
        self.assertEqual(translation.parent_data["parent_article_type"], "translation")
        self.assertEqual(translation.parent_data["parent_lang"], "pt")
        self.assertEqual(
            translation.parent_data["original_article_type"], "research-article"
        )

        # Test reviewer-report sub-article
        reviewer_report = sub_articles[1]
        self.assertEqual(
            reviewer_report.parent_data["parent_article_type"], "reviewer-report"
        )
        self.assertEqual(reviewer_report.parent_data["parent_lang"], "es")
        self.assertEqual(
            reviewer_report.parent_data["original_article_type"], "reviewer-report"
        )


class TestFulltextRelatedArticlesTranslation(TestCase):
    """Tests for translation sub-article with original_article_type parameter"""

    def setUp(self):
        xml = """
        <sub-article article-type="translation" xml:lang="es" id="s1">
            <front-stub>
                <related-article related-article-type="translation-of" 
                               ext-link-type="doi" 
                               id="ra1">Translation note</related-article>
            </front-stub>
            <body>
                <related-article related-article-type="corrected-article"
                               ext-link-type="doi"
                               id="ra2">Body related</related-article>
            </body>
        </sub-article>"""
        self.fulltext = FulltextRelatedArticles(
            etree.fromstring(xml), original_article_type="research-article"
        )

    def test_parent_data_with_translation(self):
        expected = {
            "parent": "sub-article",
            "parent_id": "s1",
            "parent_article_type": "translation",
            "parent_lang": "es",
            "original_article_type": "research-article",
        }
        self.assertEqual(self.fulltext.parent_data, expected)

    def test_related_articles_in_translation(self):
        related = list(self.fulltext.related_articles)
        self.assertEqual(len(related), 2)

        # Map related articles by id
        articles = {r["id"]: r for r in related}

        # Check front-stub related article
        front = articles["ra1"]
        self.assertEqual(front["related-article-type"], "translation-of")
        self.assertEqual(front["text"], "Translation note")
        self.assertEqual(front["original_article_type"], "research-article")

        # Check body related article
        body = articles["ra2"]
        self.assertEqual(body["related-article-type"], "corrected-article")
        self.assertEqual(body["text"], "Body related")
        self.assertEqual(body["original_article_type"], "research-article")


class TestFulltextRelatedArticlesNestedStructure(TestCase):
    """Tests for complex nested structure with multiple sub-articles"""

    def setUp(self):
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en" id="main">
            <front>
                <related-article id="ra1">Main article</related-article>
            </front>
            <sub-article article-type="translation" xml:lang="pt" id="trans1">
                <front-stub>
                    <related-article id="ra2">Translation 1</related-article>
                </front-stub>
                <sub-article article-type="reviewer-report" id="abs1">
                    <front-stub>
                        <related-article id="ra3">Nested reviewer-report</related-article>
                    </front-stub>
                </sub-article>
            </sub-article>
        </article>"""
        self.fulltext = FulltextRelatedArticles(etree.fromstring(xml))

    def test_nested_structure(self):
        # Test main article
        main_related = list(self.fulltext.related_articles)
        self.assertEqual(len(main_related), 1)
        self.assertEqual(main_related[0]["text"], "Main article")

        # Test first level sub-articles
        level1_articles = list(self.fulltext.fulltexts)
        self.assertEqual(len(level1_articles), 1)

        translation = level1_articles[0]
        self.assertEqual(translation.parent_data["parent_article_type"], "translation")
        self.assertEqual(
            translation.parent_data["original_article_type"], "research-article"
        )

        # Test translation related articles
        trans_related = list(translation.related_articles)
        self.assertEqual(len(trans_related), 1)
        self.assertEqual(trans_related[0]["text"], "Translation 1")

        # Test nested reviewer-report
        nested_articles = list(translation.fulltexts)
        self.assertEqual(len(nested_articles), 1)

        reviewer_report = nested_articles[0]
        self.assertEqual(
            reviewer_report.parent_data["parent_article_type"], "reviewer-report"
        )
        self.assertEqual(
            reviewer_report.parent_data["original_article_type"], "reviewer-report"
        )

        # Test reviewer-report related articles
        abs_related = list(reviewer_report.related_articles)
        self.assertEqual(len(abs_related), 1)
        self.assertEqual(abs_related[0]["text"], "Nested reviewer-report")
