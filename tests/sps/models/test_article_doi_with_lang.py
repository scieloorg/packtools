import unittest
from unittest.mock import Mock, patch
from lxml import etree
from packtools.sps.models.article_doi_with_lang import DoiWithLang


class TestDoiWithLang(unittest.TestCase):
    def setUp(self):
        self.sample_xml = """
        <article article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="doi">10.1590/example-doi</article-id>
                    <title-group>
                        <article-title>Sample Article Title</article-title>
                    </title-group>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Smith</surname>
                                <given-names>John</given-names>
                            </name>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="tr1" xml:lang="pt">
                <front-stub>
                    <article-id pub-id-type="doi">10.1590/example-doi-pt</article-id>
                    <title-group>
                        <article-title>Título do Artigo em Português</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
        </article>
        """
        self.xmltree = etree.fromstring(self.sample_xml.encode("utf-8"))
        self.doi_with_lang = DoiWithLang(self.xmltree)

    def test_main_doi(self):
        """Test if main_doi property returns the correct DOI"""
        self.assertEqual(self.doi_with_lang.main_doi, "10.1590/example-doi")

    def test_main_lang(self):
        """Test if main_lang property returns the correct language"""
        self.assertEqual(self.doi_with_lang.main_lang, "en")

    def test_get_node(self):
        """Test if _get_node method returns the correct node"""
        node = self.doi_with_lang._get_node('.//article-id[@pub-id-type="doi"]')
        self.assertIsNotNone(node)
        self.assertEqual(node.text, "10.1590/example-doi")

    def test_get_node_nonexistent(self):
        """Test if _get_node method returns None for nonexistent node"""
        node = self.doi_with_lang._get_node(".//nonexistent")
        self.assertIsNone(node)

    def test_get_node_text(self):
        """Test if _get_node_text method returns the correct text"""
        text = self.doi_with_lang._get_node_text('.//article-id[@pub-id-type="doi"]')
        self.assertEqual(text, "10.1590/example-doi")

    def test_get_node_text_nonexistent(self):
        """Test if _get_node_text method returns None for nonexistent node"""
        text = self.doi_with_lang._get_node_text(".//nonexistent")
        self.assertIsNone(text)

    @patch("packtools.sps.models.article_titles.ArticleTitles")
    @patch("packtools.sps.models.article_contribs.XMLContribs")
    def test_data_main_article(self, mock_contribs, mock_titles):
        """Test if data property returns correct information for main article"""
        # Mock the ArticleTitles and XMLContribs
        mock_titles.return_value.article_title_dict = {
            "en": {"plain_text": "Sample Article Title"}
        }
        mock_contribs.return_value.contribs = [
            {"contrib_name": {"surname": "Smith", "given-names": "John"}}
        ]

        doi_with_lang = DoiWithLang(self.xmltree)
        data = doi_with_lang.data

        self.assertEqual(len(data), 2)  # Main article + translation
        main_article = data[0]
        self.assertEqual(main_article["lang"], "en")
        self.assertEqual(main_article["value"], "10.1590/example-doi")
        self.assertEqual(main_article["parent"], "article")
        self.assertEqual(main_article["parent_article_type"], "research-article")
        self.assertEqual(main_article["article_title"], "Sample Article Title")
        self.assertEqual(main_article["authors"], ["Smith, John"])

    @patch("packtools.sps.models.article_titles.ArticleTitles")
    @patch("packtools.sps.models.article_contribs.XMLContribs")
    def test_data_translation(self, mock_contribs, mock_titles):
        """Test if data property returns correct information for translation"""
        # Mock the ArticleTitles and XMLContribs
        mock_titles.return_value.article_title_dict = {
            "pt": {"plain_text": "Título do Artigo em Português"}
        }
        mock_contribs.return_value.contribs = [
            {"contrib_name": {"surname": "Smith", "given-names": "John"}}
        ]

        doi_with_lang = DoiWithLang(self.xmltree)
        data = doi_with_lang.data

        translation = data[1]
        self.assertEqual(translation["lang"], "pt")
        self.assertEqual(translation["value"], "10.1590/example-doi-pt")
        self.assertEqual(translation["parent"], "sub-article")
        self.assertEqual(translation["parent_article_type"], "translation")
        self.assertEqual(translation["parent_id"], "tr1")
        self.assertEqual(translation["article_title"], "Título do Artigo em Português")
        self.assertEqual(translation["authors"], ["Smith, John"])

    def test_data_missing_author_info(self):
        """Test handling of missing author information"""
        with patch(
            "packtools.sps.models.article_doi_with_lang.XMLContribs"
        ) as mock_contribs:
            mock_contribs.return_value.contribs = [
                {"contrib_name": {}}
            ]  # Missing required fields
            doi_with_lang = DoiWithLang(self.xmltree)
            data = doi_with_lang.data
            self.assertEqual(
                data[0]["authors"], []
            )  # Should handle missing author info gracefully


if __name__ == "__main__":
    unittest.main()
