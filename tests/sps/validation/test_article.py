from unittest import TestCase

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation.article import are_similar_articles

xml_a1_str = """
<article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
    <front>
        <article-meta>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v3">zTn4sYXBrfSTMNVPF5Dm7jr</article-id>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0103-50532014001202258</article-id>
            <article-id pub-id-type="doi">10.5935/0103-5053.20140192</article-id>
        </article-meta>
    </front>
</article>
"""


class ArticleTest(TestCase):
    def setUp(self) -> None:
        self.xml_a1 = get_xml_tree(xml_a1_str)
        
    def test_article_are_similar_articles_results_false(self):
        xml_a2 = get_xml_tree("""
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">zTn4sYXBrfSTMNVPF5Dm7js</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0103-50532014001202259</article-id>
                    <article-id pub-id-type="doi">10.5935/0103-5053.20140193</article-id>
                </article-meta>
            </front>
        </article>
        """)
        self.assertFalse(are_similar_articles(self.xml_a1, xml_a2))

