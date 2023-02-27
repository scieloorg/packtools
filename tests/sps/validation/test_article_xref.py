from unittest import TestCase
from lxml import etree

from packtools.sps.validation.article_xref import ArticleXrefValidation


class ArticleXrefValidationTest(TestCase):

    def test_validate_rid_elements_matches(self):
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
        self.article_xref = ArticleXrefValidation(self.xmltree)
        expected = dict(
            rid_elements={'aff1', 'fig1', 'table1'},
            id_elements={'aff1', 'fig1', 'table1'},
            diff=set(),
            msg="OK: all rid elements have the respective id elements"
        )
        obtained = self.article_xref.validate_rid_elements()
        self.assertDictEqual(expected, obtained)

    def test_validate_rid_elements_no_matches(self):
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
                </article-meta>
            </article>
            """
        )
        self.article_xref = ArticleXrefValidation(self.xmltree)
        expected = dict(
            rid_elements={'aff1', 'fig1', 'table1'},
            id_elements={'aff1', 'fig1'},
            diff={'table1'},
            msg="ERROR: the rid elements {'table1'} do not have the respective id elements"
        )
        obtained = self.article_xref.validate_rid_elements()
        self.assertDictEqual(expected, obtained)

    def test_validate_id_elements_matches(self):
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
        self.article_xref = ArticleXrefValidation(self.xmltree)
        expected = dict(
            rid_elements={'aff1', 'fig1', 'table1'},
            id_elements={'aff1', 'fig1', 'table1'},
            diff=set(),
            msg="OK: all id elements have the respective rid elements"
        )
        obtained = self.article_xref.validate_id_elements()
        self.assertDictEqual(expected, obtained)

    def test_validate_id_elements_no_matches(self):
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
    
                    <table id="table1">
                        <p>cited tablet</p>
                    </table>
                </article-meta>
            </article>
            """
        )
        self.article_xref = ArticleXrefValidation(self.xmltree)
        expected = dict(
            rid_elements={'aff1', 'fig1'},
            id_elements={'aff1', 'fig1', 'table1'},
            diff={'table1'},
            msg="ERROR: the id elements {'table1'} do not have the respective rid elements"
        )
        obtained = self.article_xref.validate_id_elements()
        self.assertDictEqual(expected, obtained)
