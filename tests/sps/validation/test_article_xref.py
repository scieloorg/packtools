from unittest import TestCase
from lxml import etree

from packtools.sps.validation.article_xref import ArticleXrefValidation


class ArticleXrefValidationTest(TestCase):

    def test_validate_rids_matches(self):
        self.xmltree = etree.fromstring(
            """
            <article>
                <article-meta>
                    <p><xref ref-type="aff" rid="aff1">1</xref></p>     
                    <aff id="aff1">
                        <p>affiliation</p>
                    </aff>

                    <p><xref ref-type="fig" rid="fig1">1</xref></p>     
                    <fig id="fig1">
                        <p>figure</p>
                    </fig>

                    <p><xref ref-type="table" rid="table1">1</xref></p>     
                    <table id="table1">
                        <p>table</p>
                    </table>
                </article-meta>
            </article>
            """
        )
        self.article_xref = ArticleXrefValidation(self.xmltree)
        expected = dict(
            expected_value=['aff1', 'fig1', 'table1'],
            obtained_value=['aff1', 'fig1', 'table1'],
            result=[],
            message="OK: all rids have the respective ids"
        )
        obtained = self.article_xref.validate_rid()
        self.assertDictEqual(expected, obtained)

    def test_validate_rids_no_matches(self):
        self.xmltree = etree.fromstring(
            """
            <article>
                <article-meta>
                    <p><xref ref-type="aff" rid="aff1">1</xref></p>     
                    <aff id="aff1">
                        <p>affiliation</p>
                    </aff>

                    <p><xref ref-type="fig" rid="fig1">1</xref></p>     
                    <fig id="fig1">
                        <p>figure</p>
                    </fig>

                    <p><xref ref-type="table" rid="table1">1</xref></p>     
                </article-meta>
            </article>
            """
        )
        self.article_xref = ArticleXrefValidation(self.xmltree)
        expected = dict(
            expected_value=['aff1', 'fig1', 'table1'],
            obtained_value=['aff1', 'fig1'],
            result=['table1'],
            message="ERROR: rids were found with the values "
                f"{self.article_xref.validate_rid()['expected_value']} but there were "
                "no ids with the corresponding values"
        )
        obtained = self.article_xref.validate_rid()
        self.assertDictEqual(expected, obtained)

    def test_validate_ids_matches(self):
        self.xmltree = etree.fromstring(
            """
            <article>
                <article-meta>
                    <p><xref ref-type="aff" rid="aff1">1</xref></p>     
                    <aff id="aff1">
                        <p>affiliation</p>
                    </aff>

                    <p><xref ref-type="fig" rid="fig1">1</xref></p>     
                    <fig id="fig1">
                        <p>figure</p>
                    </fig>

                    <p><xref ref-type="table" rid="table1">1</xref></p>     
                    <table id="table1">
                        <p>table</p>
                    </table>
                </article-meta>
            </article>
            """
        )
        self.article_xref = ArticleXrefValidation(self.xmltree)
        expected = dict(
            obtained_value=['aff1', 'fig1', 'table1'],
            expected_value=['aff1', 'fig1', 'table1'],
            result=[],
            message="OK: all ids have the respective rids"
        )
        obtained = self.article_xref.validate_id()
        self.assertDictEqual(expected, obtained)

    def test_validate_ids_no_matches(self):
        self.xmltree = etree.fromstring(
            """
            <article>
                <article-meta>
                    <p><xref ref-type="aff" rid="aff1">1</xref></p>     
                    <aff id="aff1">
                        <p>affiliation</p>
                    </aff>

                    <p><xref ref-type="fig" rid="fig1">1</xref></p>     
                    <fig id="fig1">
                        <p>figure</p>
                    </fig>
    
                    <table id="table1">
                        <p>table</p>
                    </table>
                </article-meta>
            </article>
            """
        )
        self.article_xref = ArticleXrefValidation(self.xmltree)
        expected = dict(
            obtained_value=['aff1', 'fig1'],
            expected_value=['aff1', 'fig1', 'table1'],
            result=['table1'],
            message="ERROR: ids were found with the values "
                f"{self.article_xref.validate_id()['expected_value']} but there were "
                "no rids with the corresponding values"
        )
        obtained = self.article_xref.validate_id()
        self.assertDictEqual(expected, obtained)
