from unittest import TestCase

from lxml import etree

from packtools.sps.models.article_uri import ArticleUri


class ArticleUriTest(TestCase):
    def setUp(self):
        xml = ("""
                <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
                xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
                <front>
                <article-meta>
                <article-id>S0718-71812021000100011</article-id>
                <article-id pub-id-type="doi">10.7764/69.1</article-id>
                <self-uri xlink:href="http://www.scielo.cl/scielo.php?script=sci_arttext&amp;pid=S0718-71812021000100011&amp;lng=en&amp;nrm=iso"/>
                <self-uri xlink:href="http://www.scielo.cl/scielo.php?script=sci_abstract&amp;pid=S0718-71812021000100011&amp;lng=en&amp;nrm=iso"/>
                <self-uri xlink:href="http://www.scielo.cl/scielo.php?script=sci_pdf&amp;pid=S0718-71812021000100011&amp;lng=en&amp;nrm=iso"/>
                </article-meta>
                </front>
                </article>
                """)

        xmltree = etree.fromstring(xml)
        self.article_uri = ArticleUri(xmltree)

    def test_get_article_uri(self):
        expected = {
            "sci_arttext": "http://www.scielo.cl/scielo.php?script=sci_arttext&pid=S0718-71812021000100011&lng=en&nrm=iso",
            "sci_abstract": "http://www.scielo.cl/scielo.php?script=sci_abstract&pid=S0718-71812021000100011&lng=en&nrm=iso",
            "sci_pdf": "http://www.scielo.cl/scielo.php?script=sci_pdf&pid=S0718-71812021000100011&lng=en&nrm=iso"
        }

        self.assertDictEqual(expected, self.article_uri.all_uris)
