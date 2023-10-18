from unittest import TestCase

import self as self
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

        expected = {
            'validation':
                [
                    {
                        'context': 'xref element rid attribute validation',
                        'result': 'OK',
                        'expected_value': 'aff1',
                        'got_value': 'aff1',
                        'error_type': None,
                        'message': 'rid have the respective id'
                    },
                    {
                        'context': 'xref element rid attribute validation',
                        'result': 'OK',
                        'expected_value': 'fig1',
                        'got_value': 'fig1',
                        'error_type': None,
                        'message': 'rid have the respective id'
                    },
                    {
                        'context': 'xref element rid attribute validation',
                        'result': 'OK',
                        'expected_value': 'table1',
                        'got_value': 'table1',
                        'error_type': None,
                        'message': 'rid have the respective id'
                    }
                ]
        }
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

        expected = {
            'validation':
                [
                    {
                        'context': 'xref element rid attribute validation',
                        'result': 'OK',
                        'expected_value': 'aff1',
                        'got_value': 'aff1',
                        'error_type': None,
                        'message': 'rid have the respective id'
                    },
                    {
                        'context': 'xref element rid attribute validation',
                        'result': 'OK',
                        'expected_value': 'fig1',
                        'got_value': 'fig1',
                        'error_type': None,
                        'message': 'rid have the respective id'
                    },
                    {
                        'context': 'xref element rid attribute validation',
                        'result': 'ERROR',
                        'expected_value': 'table1',
                        'got_value': None,
                        'error_type': 'no match',
                        'message': 'rid does not have the respective id'
                    }
                ]
        }
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

        expected = {
            'validation':
                [
                    {
                        'context': 'xref element id attribute validation',
                        'result': 'OK',
                        'expected_value': 'aff1',
                        'got_value': 'aff1',
                        'error_type': None,
                        'message': 'id have the respective rid'
                    },
                    {
                        'context': 'xref element id attribute validation',
                        'result': 'OK',
                        'expected_value': 'fig1',
                        'got_value': 'fig1',
                        'error_type': None,
                        'message': 'id have the respective rid'
                    },
                    {
                        'context': 'xref element id attribute validation',
                        'result': 'OK',
                        'expected_value': 'table1',
                        'got_value': 'table1',
                        'error_type': None,
                        'message': 'id have the respective rid'
                    }
                ]
        }
        obtained = self.article_xref.validate_id()
        self.assertDictEqual(expected, obtained)

    def test_validate_ids_no_matches(self):
        self.maxDiff = None
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

        expected = {
            'validation':
                [
                    {
                        'context': 'xref element id attribute validation',
                        'result': 'OK',
                        'expected_value': 'aff1',
                        'got_value': 'aff1',
                        'error_type': None,
                        'message': 'id have the respective rid'
                    },
                    {
                        'context': 'xref element id attribute validation',
                        'result': 'OK',
                        'expected_value': 'fig1',
                        'got_value': 'fig1',
                        'error_type': None,
                        'message': 'id have the respective rid'
                    },
                    {
                        'context': 'xref element id attribute validation',
                        'result': 'ERROR',
                        'expected_value': 'table1',
                        'got_value': None,
                        'error_type': 'no match',
                        'message': 'id does not have the respective rid'
                    }
                ]
        }
        obtained = self.article_xref.validate_id()
        self.assertDictEqual(expected, obtained)
