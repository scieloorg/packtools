from unittest import TestCase
from lxml import etree

from packtools.sps.validation.article_xref import ArticleXrefValidation


class ArticleXrefValidationTest(TestCase):
    def setUp(self):
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

    def test_validate_citing_elements_matches(self):
        expected = dict(
            expected_value={'aff1', 'fig1', 'table1'},
            obteined_value={'aff1', 'fig1', 'table1'},
            match=True
        )
        obtained = self.article_xref.validate_citing_elements({'aff1', 'fig1', 'table1'})
        self.assertDictEqual(expected, obtained)

    def test_validate_citing_elements_no_matches(self):
        expected = dict(
            expected_value={'aff1', 'fig1'},
            obteined_value={'aff1', 'fig1', 'table1'},
            match=False
        )
        obtained = self.article_xref.validate_citing_elements({'aff1', 'fig1'})
        self.assertDictEqual(expected, obtained)

    def test_validate_cited_elements_matches(self):
        expected = dict(
            expected_value={'aff1', 'fig1', 'table1'},
            obteined_value={'aff1', 'fig1', 'table1'},
            match=True
        )
        obtained = self.article_xref.validate_cited_elements({'aff1', 'fig1', 'table1'})
        self.assertDictEqual(expected, obtained)

    def test_validate_cited_elements_no_matches(self):
        expected = dict(
            expected_value={'aff1', 'fig1'},
            obteined_value={'aff1', 'fig1', 'table1'},
            match=False
        )
        obtained = self.article_xref.validate_cited_elements({'aff1', 'fig1'})
        self.assertDictEqual(expected, obtained)

    def test_validate_parity_between_citing_and_cited_elements(self):
        expected = dict(
            expected_value=set(),
            obteined_value=set(),
            match=True
        )
        obtained = self.article_xref.validate_parity_between_citing_and_cited_elements(set())
        self.assertDictEqual(expected, obtained)
