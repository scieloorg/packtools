from unittest import TestCase

from lxml import etree

from packtools.sps.models.article_xref import ArticleXref


class ArticleXrefTest(TestCase):
    def test_all_references_have_origin_and_destiny(self):
        self.xmltree = etree.fromstring(

            """
                <article>
                    <article-meta>
                        <p>citing element<xref ref-type="aff" rid="aff1">1</xref></p>     
                        <aff id="aff1">
                            <p>cited affiliation</p>
                        </aff>

                        <p>citing element<xref ref-type="fig" rid="fig1">1</xref></p>     
                        <fig id="fig1">
                            <p>cited figure</p>
                        </fig>

                        <p>citing element<xref ref-type="table" rid="table1">1</xref></p>     
                        <table id="table1">
                            <p>cited tablet</p>
                        </table>
                    </article-meta>
                </article>
            """
        )
        self.article_xref = ArticleXref(self.xmltree)
        self.assertEqual(set(), self.article_xref.reference_without_origin)

    def test_some_references_have_no_origin(self):
        self.xmltree = etree.fromstring(

            """
                <article>
                    <article-meta>   
                        <aff id="aff1">
                            <p>cited affiliation</p>
                        </aff>

                        <p>citing element<xref ref-type="fig" rid="fig1">1</xref></p>     
                        <fig id="fig1">
                            <p>cited figure</p>
                        </fig>

                        <p>citing element<xref ref-type="table" rid="table1">1</xref></p>     
                        <table id="table1">
                            <p>cited tablet</p>
                        </table>
                    </article-meta>
                </article>
            """
        )
        self.article_xref = ArticleXref(self.xmltree)
        self.assertEqual({'aff1'}, self.article_xref.reference_without_origin)

    def test_some_references_have_no_destiny(self):
        self.xmltree = etree.fromstring(

            """
                <article>
                    <article-meta>
                        <p>citing element<xref ref-type="aff" rid="aff1">1</xref></p>     
                        <aff id="aff1">
                            <p>cited affiliation</p>
                        </aff>

                        <p>citing element<xref ref-type="fig" rid="fig1">1</xref></p>     
                        
                        <p>citing element<xref ref-type="table" rid="table1">1</xref></p>     
                        <table id="table1">
                            <p>cited tablet</p>
                        </table>
                    </article-meta>
                </article>
            """
        )
        self.article_xref = ArticleXref(self.xmltree)
        self.assertEqual({'fig1'}, self.article_xref.reference_without_destiny)
