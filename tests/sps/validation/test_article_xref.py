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
                        'title': 'xref element rid attribute validation',
                        'xpath': './/xref[@rid]',
                        'validation_type': 'match',
                        'response': 'OK',
                        'expected_value': 'aff1',
                        'got_value': 'aff1',
                        'message': 'rid have the respective id',
                        'advice': None
                    },
                    {
                        'title': 'xref element rid attribute validation',
                        'xpath': './/xref[@rid]',
                        'validation_type': 'match',
                        'response': 'OK',
                        'expected_value': 'fig1',
                        'got_value': 'fig1',
                        'message': 'rid have the respective id',
                        'advice': None
                    },
                    {
                        'title': 'xref element rid attribute validation',
                        'xpath': './/xref[@rid]',
                        'validation_type': 'match',
                        'response': 'OK',
                        'expected_value': 'table1',
                        'got_value': 'table1',
                        'message': 'rid have the respective id',
                        'advice': None
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
                        'title': 'xref element rid attribute validation',
                        'xpath': './/xref[@rid]',
                        'validation_type': 'match',
                        'response': 'OK',
                        'expected_value': 'aff1',
                        'got_value': 'aff1',
                        'message': 'rid have the respective id',
                        'advice': None
                    },
                    {
                        'title': 'xref element rid attribute validation',
                        'xpath': './/xref[@rid]',
                        'validation_type': 'match',
                        'response': 'OK',
                        'expected_value': 'fig1',
                        'got_value': 'fig1',
                        'message': 'rid have the respective id',
                        'advice': None
                    },
                    {
                        'title': 'xref element rid attribute validation',
                        'xpath': './/xref[@rid]',
                        'validation_type': 'match',
                        'response': 'ERROR',
                        'expected_value': 'table1',
                        'got_value': None,
                        'message': 'rid does not have the respective id',
                        'advice': 'add attribute id = table1 to the corresponding rid = table1'
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
                        'title': 'xref element id attribute validation',
                        'xpath': './/*[@id]',
                        'validation_type': 'match',
                        'response': 'OK',
                        'expected_value': 'aff1',
                        'got_value': 'aff1',
                        'message': 'id have the respective rid',
                        'advice': None
                    },
                    {
                        'title': 'xref element id attribute validation',
                        'xpath': './/*[@id]',
                        'validation_type': 'match',
                        'response': 'OK',
                        'expected_value': 'fig1',
                        'got_value': 'fig1',
                        'message': 'id have the respective rid',
                        'advice': None
                    },
                    {
                        'title': 'xref element id attribute validation',
                        'xpath': './/*[@id]',
                        'validation_type': 'match',
                        'response': 'OK',
                        'expected_value': 'table1',
                        'got_value': 'table1',
                        'message': 'id have the respective rid',
                        'advice': None
                    }
                ]
        }
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

        expected = {
            'validation':
                [
                    {
                        'title': 'xref element id attribute validation',
                        'xpath': './/*[@id]',
                        'validation_type': 'match',
                        'response': 'OK',
                        'expected_value': 'aff1',
                        'got_value': 'aff1',
                        'message': 'id have the respective rid',
                        'advice': None
                    },
                    {
                        'title': 'xref element id attribute validation',
                        'xpath': './/*[@id]',
                        'validation_type': 'match',
                        'response': 'OK',
                        'expected_value': 'fig1',
                        'got_value': 'fig1',
                        'message': 'id have the respective rid',
                        'advice': None
                    },
                    {
                        'title': 'xref element id attribute validation',
                        'xpath': './/*[@id]',
                        'validation_type': 'match',
                        'response': 'ERROR',
                        'expected_value': 'table1',
                        'got_value': None,
                        'message': 'id does not have the respective rid',
                        'advice': 'add attribute rid = table1 to the corresponding id = table1'
                    }
                ]
        }
        obtained = self.article_xref.validate_id()
        self.assertDictEqual(expected, obtained)
