"""
Unit tests for ext-link model data extraction.

Tests the ExtLink and ArticleExtLinks classes to ensure proper extraction
of ext-link elements from XML documents, including attributes and parent context.
"""
from unittest import TestCase
from io import BytesIO

from lxml import etree
from packtools.sps.models.ext_link import ExtLink, ArticleExtLinks


def create_xml_tree(xml_content):
    """Helper function to create XML tree from string content."""
    return etree.parse(BytesIO(xml_content.encode("utf-8")))


class TestExtLinkBasic(TestCase):
    """Tests for basic ext-link extraction."""

    def setUp(self):
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">'
            '<body>'
            '<p>'
            '<ext-link ext-link-type="uri" xlink:href="https://www.scielo.br/" xlink:title="SciELO Platform">'
            'SciELO Brasil'
            '</ext-link>'
            '</p>'
            '</body>'
            '</article>'
        )
        self.xml_tree = create_xml_tree(xml)

    def test_ext_link_extraction(self):
        """Test extraction of basic ext-link with all attributes."""
        ext_link_model = ExtLink(self.xml_tree.getroot())
        items = list(ext_link_model.ext_links)

        self.assertEqual(len(items), 1)
        item = items[0]

        self.assertEqual(item["ext_link_type"], "uri")
        self.assertEqual(item["xlink_href"], "https://www.scielo.br/")
        self.assertEqual(item["xlink_title"], "SciELO Platform")
        self.assertEqual(item["text"], "SciELO Brasil")
        self.assertEqual(item["parent"], "article")
        self.assertIsNone(item["parent_id"])
        self.assertEqual(item["parent_lang"], "en")
        self.assertEqual(item["parent_article_type"], "research-article")

    def test_ext_link_without_title(self):
        """Test ext-link without xlink:title attribute."""
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<body>'
            '<ext-link ext-link-type="doi" xlink:href="https://doi.org/10.1590/example">'
            'DOI Link'
            '</ext-link>'
            '</body>'
            '</article>'
        )
        xml_tree = create_xml_tree(xml)
        ext_link_model = ExtLink(xml_tree.getroot())
        items = list(ext_link_model.ext_links)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["ext_link_type"], "doi")
        self.assertEqual(items[0]["xlink_href"], "https://doi.org/10.1590/example")
        self.assertIsNone(items[0]["xlink_title"])
        self.assertEqual(items[0]["text"], "DOI Link")


class TestExtLinkMissingAttributes(TestCase):
    """Tests for ext-link with missing attributes."""

    def test_ext_link_missing_type(self):
        """Test ext-link without ext-link-type attribute."""
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<body>'
            '<ext-link xlink:href="https://example.com">Example</ext-link>'
            '</body>'
            '</article>'
        )
        xml_tree = create_xml_tree(xml)
        ext_link_model = ExtLink(xml_tree.getroot())
        items = list(ext_link_model.ext_links)

        self.assertEqual(len(items), 1)
        self.assertIsNone(items[0]["ext_link_type"])
        self.assertEqual(items[0]["xlink_href"], "https://example.com")
        self.assertEqual(items[0]["text"], "Example")

    def test_ext_link_missing_href(self):
        """Test ext-link without xlink:href attribute."""
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<body>'
            '<ext-link ext-link-type="uri">Example Link</ext-link>'
            '</body>'
            '</article>'
        )
        xml_tree = create_xml_tree(xml)
        ext_link_model = ExtLink(xml_tree.getroot())
        items = list(ext_link_model.ext_links)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["ext_link_type"], "uri")
        self.assertIsNone(items[0]["xlink_href"])
        self.assertEqual(items[0]["text"], "Example Link")

    def test_ext_link_missing_all_attributes(self):
        """Test ext-link without any attributes."""
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<body>'
            '<ext-link>Plain Text Link</ext-link>'
            '</body>'
            '</article>'
        )
        xml_tree = create_xml_tree(xml)
        ext_link_model = ExtLink(xml_tree.getroot())
        items = list(ext_link_model.ext_links)

        self.assertEqual(len(items), 1)
        self.assertIsNone(items[0]["ext_link_type"])
        self.assertIsNone(items[0]["xlink_href"])
        self.assertIsNone(items[0]["xlink_title"])
        self.assertEqual(items[0]["text"], "Plain Text Link")


class TestExtLinkMultiple(TestCase):
    """Tests for multiple ext-link elements."""

    def test_multiple_ext_links(self):
        """Test extraction of multiple ext-links."""
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">'
            '<body>'
            '<p><ext-link ext-link-type="uri" xlink:href="https://site1.com">Link 1</ext-link></p>'
            '<p><ext-link ext-link-type="doi" xlink:href="https://doi.org/10.1590/test">Link 2</ext-link></p>'
            '<p><ext-link ext-link-type="pmid" xlink:href="https://pubmed.ncbi.nlm.nih.gov/12345/">Link 3</ext-link></p>'
            '</body>'
            '</article>'
        )
        xml_tree = create_xml_tree(xml)
        ext_link_model = ExtLink(xml_tree.getroot())
        items = list(ext_link_model.ext_links)

        self.assertEqual(len(items), 3)

        self.assertEqual(items[0]["ext_link_type"], "uri")
        self.assertEqual(items[0]["xlink_href"], "https://site1.com")
        self.assertEqual(items[0]["text"], "Link 1")

        self.assertEqual(items[1]["ext_link_type"], "doi")
        self.assertEqual(items[1]["xlink_href"], "https://doi.org/10.1590/test")
        self.assertEqual(items[1]["text"], "Link 2")

        self.assertEqual(items[2]["ext_link_type"], "pmid")
        self.assertEqual(items[2]["xlink_href"], "https://pubmed.ncbi.nlm.nih.gov/12345/")
        self.assertEqual(items[2]["text"], "Link 3")


class TestExtLinkInSubArticles(TestCase):
    """Tests for ext-link in sub-articles."""

    def test_ext_link_in_translation(self):
        """Test ext-link extraction from translation sub-article."""
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">'
            '<body><p>Main article content</p></body>'
            '<sub-article article-type="translation" xml:lang="pt" id="s1">'
            '<body>'
            '<p><ext-link ext-link-type="uri" xlink:href="https://exemplo.com.br">Link em português</ext-link></p>'
            '</body>'
            '</sub-article>'
            '</article>'
        )
        xml_tree = create_xml_tree(xml)
        article_ext_links = ArticleExtLinks(xml_tree.getroot())
        items = article_ext_links.ext_links

        self.assertEqual(len(items), 1)
        item = items[0]

        self.assertEqual(item["ext_link_type"], "uri")
        self.assertEqual(item["xlink_href"], "https://exemplo.com.br")
        self.assertEqual(item["text"], "Link em português")
        self.assertEqual(item["parent"], "sub-article")
        self.assertEqual(item["parent_id"], "s1")
        self.assertEqual(item["parent_lang"], "pt")
        self.assertEqual(item["parent_article_type"], "translation")

    def test_ext_links_main_and_sub_articles(self):
        """Test ext-link extraction from both main article and sub-articles."""
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">'
            '<body>'
            '<p><ext-link ext-link-type="uri" xlink:href="https://main.com">Main Link</ext-link></p>'
            '</body>'
            '<sub-article article-type="translation" xml:lang="es" id="s1">'
            '<body>'
            '<p><ext-link ext-link-type="doi" xlink:href="https://doi.org/10.1590/test">Sub Link 1</ext-link></p>'
            '</body>'
            '</sub-article>'
            '<sub-article article-type="translation" xml:lang="pt" id="s2">'
            '<body>'
            '<p><ext-link ext-link-type="pmid" xlink:href="https://pubmed.ncbi.nlm.nih.gov/123/">Sub Link 2</ext-link></p>'
            '</body>'
            '</sub-article>'
            '</article>'
        )
        xml_tree = create_xml_tree(xml)
        article_ext_links = ArticleExtLinks(xml_tree.getroot())
        items = article_ext_links.ext_links

        self.assertEqual(len(items), 3)

        self.assertEqual(items[0]["text"], "Main Link")
        self.assertEqual(items[0]["parent"], "article")
        self.assertEqual(items[0]["parent_lang"], "en")

        self.assertEqual(items[1]["text"], "Sub Link 1")
        self.assertEqual(items[1]["parent"], "sub-article")
        self.assertEqual(items[1]["parent_id"], "s1")
        self.assertEqual(items[1]["parent_lang"], "es")

        self.assertEqual(items[2]["text"], "Sub Link 2")
        self.assertEqual(items[2]["parent"], "sub-article")
        self.assertEqual(items[2]["parent_id"], "s2")
        self.assertEqual(items[2]["parent_lang"], "pt")

    def test_ext_links_deeply_nested_sub_articles(self):
        """Test ext-link extraction from sub-articles nested more than two levels deep.

        Regression test for the recursive traversal fix: the previous implementation
        used two nested for-loops, silently missing ext-links beyond the second level.
        The fix uses _collect_ext_links() which recurses through fulltexts at any depth.
        """
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">'
            '<body>'
            '<p><ext-link ext-link-type="uri" xlink:href="https://main.com">Main Link</ext-link></p>'
            '</body>'
            '<sub-article article-type="translation" xml:lang="pt" id="s1">'
            '<body>'
            '<p><ext-link ext-link-type="uri" xlink:href="https://level1.com">Level 1 Link</ext-link></p>'
            '</body>'
            '<sub-article article-type="translation" xml:lang="es" id="s2">'
            '<body>'
            '<p><ext-link ext-link-type="uri" xlink:href="https://level2.com">Level 2 Link</ext-link></p>'
            '</body>'
            '<sub-article article-type="translation" xml:lang="fr" id="s3">'
            '<body>'
            '<p><ext-link ext-link-type="uri" xlink:href="https://level3.com">Level 3 Link</ext-link></p>'
            '</body>'
            '</sub-article>'
            '</sub-article>'
            '</sub-article>'
            '</article>'
        )
        xml_tree = create_xml_tree(xml)
        article_ext_links = ArticleExtLinks(xml_tree.getroot())
        items = article_ext_links.ext_links

        self.assertEqual(len(items), 4)

        texts = [item["text"] for item in items]
        self.assertIn("Main Link", texts)
        self.assertIn("Level 1 Link", texts)
        self.assertIn("Level 2 Link", texts)
        self.assertIn("Level 3 Link", texts)

        # Verify parent context is preserved at the deepest nesting level
        level3 = next(i for i in items if i["text"] == "Level 3 Link")
        self.assertEqual(level3["parent"], "sub-article")
        self.assertEqual(level3["parent_id"], "s3")
        self.assertEqual(level3["parent_lang"], "fr")

    def test_ext_links_cached_property_returns_same_object(self):
        """Test that repeated accesses to ext_links return the identical object.

        Verifies cached_property behavior: the XML is parsed only once and
        subsequent calls return the same cached list instance.
        """
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xml:lang="en">'
            '<body>'
            '<p><ext-link ext-link-type="uri" xlink:href="https://example.com">Link</ext-link></p>'
            '</body>'
            '</article>'
        )
        xml_tree = create_xml_tree(xml)
        article_ext_links = ArticleExtLinks(xml_tree.getroot())

        first_call = article_ext_links.ext_links
        second_call = article_ext_links.ext_links

        # assertIs guarantees same object in memory, not just equal content
        self.assertIs(first_call, second_call)
        self.assertEqual(len(first_call), 1)


class TestExtLinkTextContent(TestCase):
    """Tests for ext-link text content extraction."""

    def test_ext_link_with_nested_formatting(self):
        """Test ext-link with nested formatting elements."""
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<body>'
            '<ext-link ext-link-type="uri" xlink:href="https://example.com">'
            'Text with <italic>italic</italic> and <bold>bold</bold> formatting'
            '</ext-link>'
            '</body>'
            '</article>'
        )
        xml_tree = create_xml_tree(xml)
        ext_link_model = ExtLink(xml_tree.getroot())
        items = list(ext_link_model.ext_links)

        self.assertEqual(len(items), 1)
        self.assertIn("italic", items[0]["text"])
        self.assertIn("bold", items[0]["text"])
        self.assertNotIn("<italic>", items[0]["text"])
        self.assertNotIn("<bold>", items[0]["text"])

    def test_ext_link_empty_text(self):
        """Test ext-link with empty text content."""
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<body>'
            '<ext-link ext-link-type="uri" xlink:href="https://example.com"></ext-link>'
            '</body>'
            '</article>'
        )
        xml_tree = create_xml_tree(xml)
        ext_link_model = ExtLink(xml_tree.getroot())
        items = list(ext_link_model.ext_links)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["text"], "")


class TestExtLinkNoExtLinks(TestCase):
    """Tests for documents without ext-links."""

    def test_no_ext_links(self):
        """Test document without any ext-links."""
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<body><p>Regular paragraph without links</p></body>'
            '</article>'
        )
        xml_tree = create_xml_tree(xml)
        ext_link_model = ExtLink(xml_tree.getroot())
        items = list(ext_link_model.ext_links)

        self.assertEqual(len(items), 0)

    def test_no_ext_links_with_subarticles(self):
        """Test document with sub-articles but no ext-links."""
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<body><p>Main content</p></body>'
            '<sub-article article-type="translation" id="s1">'
            '<body><p>Translated content</p></body>'
            '</sub-article>'
            '</article>'
        )
        xml_tree = create_xml_tree(xml)
        article_ext_links = ArticleExtLinks(xml_tree.getroot())
        items = article_ext_links.ext_links

        self.assertEqual(len(items), 0)


class TestExtLinkDifferentTypes(TestCase):
    """Tests for ext-link with different type values."""

    def test_all_allowed_ext_link_types(self):
        """Test all allowed ext-link-type values."""
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<body>'
            '<p><ext-link ext-link-type="uri" xlink:href="https://example.com">URI Link</ext-link></p>'
            '<p><ext-link ext-link-type="doi" xlink:href="https://doi.org/10.1590/test">DOI Link</ext-link></p>'
            '<p><ext-link ext-link-type="pmid" xlink:href="https://pubmed.ncbi.nlm.nih.gov/123/">PMID Link</ext-link></p>'
            '<p><ext-link ext-link-type="pmcid" xlink:href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC123/">PMCID Link</ext-link></p>'
            '<p><ext-link ext-link-type="clinical-trial" xlink:href="https://clinicaltrials.gov/study/NCT123">Trial Link</ext-link></p>'
            '</body>'
            '</article>'
        )
        xml_tree = create_xml_tree(xml)
        ext_link_model = ExtLink(xml_tree.getroot())
        items = list(ext_link_model.ext_links)

        self.assertEqual(len(items), 5)

        types = [item["ext_link_type"] for item in items]
        self.assertIn("uri", types)
        self.assertIn("doi", types)
        self.assertIn("pmid", types)
        self.assertIn("pmcid", types)
        self.assertIn("clinical-trial", types)


class TestExtLinkInFrontAndBack(TestCase):
    """Tests for ext-link in different document sections."""

    def test_ext_link_in_front(self):
        """Test ext-link extraction from front section."""
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<front>'
            '<article-meta>'
            '<author-notes>'
            '<fn><p><ext-link ext-link-type="uri" xlink:href="https://orcid.org/123">ORCID</ext-link></p></fn>'
            '</author-notes>'
            '</article-meta>'
            '</front>'
            '</article>'
        )
        xml_tree = create_xml_tree(xml)
        ext_link_model = ExtLink(xml_tree.getroot())
        items = list(ext_link_model.ext_links)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["ext_link_type"], "uri")
        self.assertEqual(items[0]["xlink_href"], "https://orcid.org/123")

    def test_ext_link_in_back(self):
        """Test ext-link extraction from back section."""
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<back>'
            '<fn-group>'
            '<fn><p><ext-link ext-link-type="uri" xlink:href="https://example.com/supplementary">Supplementary Data</ext-link></p></fn>'
            '</fn-group>'
            '</back>'
            '</article>'
        )
        xml_tree = create_xml_tree(xml)
        ext_link_model = ExtLink(xml_tree.getroot())
        items = list(ext_link_model.ext_links)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["text"], "Supplementary Data")

    def test_ext_link_in_all_sections(self):
        """Test ext-link extraction from front, body, and back."""
        xml = (
            '<article xmlns:xlink="http://www.w3.org/1999/xlink">'
            '<front><article-meta><author-notes><fn><p>'
            '<ext-link ext-link-type="uri" xlink:href="https://front.com">Front Link</ext-link>'
            '</p></fn></author-notes></article-meta></front>'
            '<body><p><ext-link ext-link-type="uri" xlink:href="https://body.com">Body Link</ext-link></p></body>'
            '<back><fn-group><fn><p>'
            '<ext-link ext-link-type="uri" xlink:href="https://back.com">Back Link</ext-link>'
            '</p></fn></fn-group></back>'
            '</article>'
        )
        xml_tree = create_xml_tree(xml)
        ext_link_model = ExtLink(xml_tree.getroot())
        items = list(ext_link_model.ext_links)

        self.assertEqual(len(items), 3)
        texts = [item["text"] for item in items]
        self.assertIn("Front Link", texts)
        self.assertIn("Body Link", texts)
        self.assertIn("Back Link", texts)


if __name__ == "__main__":
    import unittest
    unittest.main()
