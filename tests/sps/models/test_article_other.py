import unittest
from lxml import etree
from packtools.sps.models.article_other import OtherWithLang


class TestOtherWithLang(unittest.TestCase):
    def setUp(self):
        self.sample_xml = """
        <article article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="doi">10.1590/example-doi</article-id>
                    <article-id pub-id-type="other">00123</article-id>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="tr1" xml:lang="pt">
                <front-stub>
                    <article-id pub-id-type="doi">10.1590/example-doi-pt</article-id>
                    <article-id pub-id-type="other">00124</article-id>
                </front-stub>
            </sub-article>
            <sub-article article-type="reviewer-report" id="rr1" xml:lang="en">
                <front-stub>
                    <article-id pub-id-type="doi">10.1590/example-doi-rr</article-id>
                    <article-id pub-id-type="other">00125</article-id>
                </front-stub>
            </sub-article>
        </article>
        """
        self.xmltree = etree.fromstring(self.sample_xml.encode("utf-8"))
        self.other_with_lang = OtherWithLang(self.xmltree)

    def test_main_other(self):
        """Test if main_other property returns the correct value"""
        self.assertEqual(self.other_with_lang.main_other, "00123")

    def test_main_lang(self):
        """Test if main_lang property returns the correct language"""
        self.assertEqual(self.other_with_lang.main_lang, "en")

    def test_get_node(self):
        """Test if _get_node method returns the correct node"""
        node = self.other_with_lang._get_node('.//article-id[@pub-id-type="other"]')
        self.assertIsNotNone(node)
        self.assertEqual(node.text, "00123")

    def test_get_node_nonexistent(self):
        """Test if _get_node method returns None for nonexistent node"""
        node = self.other_with_lang._get_node(".//nonexistent")
        self.assertIsNone(node)

    def test_get_node_text(self):
        """Test if _get_node_text method returns the correct text"""
        text = self.other_with_lang._get_node_text('.//article-id[@pub-id-type="other"]')
        self.assertEqual(text, "00123")

    def test_get_node_text_nonexistent(self):
        """Test if _get_node_text method returns None for nonexistent node"""
        text = self.other_with_lang._get_node_text(".//nonexistent")
        self.assertIsNone(text)

    def test_data_main_article(self):
        """Test if data property returns correct information for main article"""
        data = self.other_with_lang.data

        self.assertEqual(len(data), 3)  # Main article + 2 sub-articles
        main_article = data[0]
        self.assertEqual(main_article["lang"], "en")
        self.assertEqual(main_article["value"], "00123")
        self.assertEqual(main_article["parent"], "article")
        self.assertEqual(main_article["parent_article_type"], "research-article")

    def test_data_translation(self):
        """Test if data property returns correct information for translation"""
        data = self.other_with_lang.data

        translation = data[1]
        self.assertEqual(translation["lang"], "pt")
        self.assertEqual(translation["value"], "00124")
        self.assertEqual(translation["parent"], "sub-article")
        self.assertEqual(translation["parent_article_type"], "translation")
        self.assertEqual(translation["parent_id"], "tr1")

    def test_data_reviewer_report(self):
        """Test if data property returns correct information for reviewer-report"""
        data = self.other_with_lang.data

        reviewer_report = data[2]
        self.assertEqual(reviewer_report["lang"], "en")
        self.assertEqual(reviewer_report["value"], "00125")
        self.assertEqual(reviewer_report["parent"], "sub-article")
        self.assertEqual(reviewer_report["parent_article_type"], "reviewer-report")
        self.assertEqual(reviewer_report["parent_id"], "rr1")

    def test_data_missing_other(self):
        """Test handling of missing other element"""
        xml_without_other = """
        <article article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="doi">10.1590/example-doi</article-id>
                </article-meta>
            </front>
        </article>
        """
        xmltree = etree.fromstring(xml_without_other.encode("utf-8"))
        other_with_lang = OtherWithLang(xmltree)
        
        self.assertIsNone(other_with_lang.main_other)
        data = other_with_lang.data
        self.assertEqual(len(data), 1)
        self.assertIsNone(data[0]["value"])


if __name__ == "__main__":
    unittest.main()
