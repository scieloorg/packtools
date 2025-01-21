import unittest
from io import BytesIO

from lxml import etree
from packtools.sps.models.related_articles import RelatedItems


def create_xml_tree(xml_content):
    return etree.parse(BytesIO(xml_content.encode("utf-8")))


class TestArticleRelatedItems(unittest.TestCase):
    def setUp(self):
        xml = (
            '<?xml version="1.0" encoding="utf-8"?>'
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
        print(item)
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


class TestSubArticleRelatedItems(unittest.TestCase):
    def setUp(self):
        xml = (
            '<?xml version="1.0" encoding="utf-8"?>'
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


class TestMultipleRelatedItems(unittest.TestCase):
    def setUp(self):
        xml = (
            '<?xml version="1.0" encoding="utf-8"?>'
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


class TestNoRelatedItems(unittest.TestCase):
    def setUp(self):
        xml = (
            '<?xml version="1.0" encoding="utf-8"?>'
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


if __name__ == "__main__":
    unittest.main()
