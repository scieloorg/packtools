from unittest import TestCase

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation.erratum import has_compatible_errata_and_document


class ErratumTest(TestCase):
    def test_erratum_has_compatible_errata_and_document(self):
        xml_errata = get_xml_tree("""
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="correction" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">Z6mnK3PjKhDZtHJQJYPzxpw</article-id>
                    <article-id pub-id-type="doi">10.21577/0103-5053.20170069</article-id>
                    <related-article ext-link-type="doi" id="ra4" related-article-type="corrected-article" xlink:href="10.5935/0103-5053.20140192"/>
                </article-meta>
                <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" xlink:href="10.1590/S0103-50532006000200015"/>
                <related-article ext-link-type="doi" id="ra2" related-article-type="corrected-article" xlink:href="10.1590/S0103-50532008000700007"/>
                <related-article ext-link-type="doi" id="ra3" related-article-type="corrected-article" xlink:href="10.1590/S0103-50532009000800009"/>
                <related-article ext-link-type="doi" id="ra4" related-article-type="corrected-article" xlink:href="10.5935/0103-5053.20140192"/>
            </front>
            <body>
                <sec>
                <title>New Isopropylmaltol - Ti Synthesis and its Use as a Catalyst for Olefin Polymerization</title>
                <p>
                    <italic>
                    <bold>Grasiela Gheno,<sup>a</sup> Nara R. S. Basso,<sup>b</sup> Marco A. Ceschi,<sup>a</sup> Jessé S. Costa,<sup>a</sup> Paolo R. Livotto<sup>a</sup> and Griselda B. Galland*<sup>,a</sup></bold>
                    </italic>
                </p>
                <p>
                    <italic><sup>a</sup>Instituto de Química, Universidade Federal do Rio Grande do Sul, Avenida Bento Gonçalves No. 9500, 91501-970 Porto Alegre-RS, Brazil</italic>
                </p>
                <p>
                    <italic><sup>b</sup>Faculdade de Química, Pontifícia Universidade Católica do Rio Grande do Sul, Avenida Ipiranga No. 6681, 90619-900 Porto Alegre-RS, Brazil</italic>
                </p>
                <p>
                    <italic>Vol. 25, No. 12, 2258-2265, 2014.</italic>
                </p>
                <p>
                    <ext-link ext-link-type="uri" xlink:href="http://dx.doi.org/10.5935/0103-5053.20140192">
                    <italic>http://dx.doi.org/10.5935/0103-5053.20140192</italic>
                    </ext-link>
                </p>
                <p>Page 2258</p>
                <p>The co-author's name "Jessé S. Costa" will change to "Jessie S. Costa"</p>
                </sec>
            </body>
        </article>
        """)

        xml_article = get_xml_tree("""
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">zTn4sYXBrfSTMNVPF5Dm7jr</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0103-50532014001202258</article-id>
                    <article-id pub-id-type="doi">10.5935/0103-5053.20140192</article-id>
                </article-meta>
            </front>
            <back>
                <fn-group>
                    <fn fn-type="other">
                        <label>Additions and Corrections</label>
                        <p>On page 2258, where it was read:</p>
                        <p>“Jessé S. Costa”</p>
                        <p>Now reads:</p>
                        <p>“Jessie S. Costa”</p>
                    </fn>
                </fn-group>
            </back>
        </article>
        """)

        self.assertTrue(has_compatible_errata_and_document(xml_errata, xml_article))
