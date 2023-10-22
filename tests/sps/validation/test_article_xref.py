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
                        'expected_value': True,
                        'got_value': True,
                        'message': 'Got True, expected True',
                        'advice': 'For each xref[@rid="aff1"] must have one corresponding element which @id="aff1"'
                    },
                    {
                        'title': 'xref element rid attribute validation',
                        'xpath': './/xref[@rid]',
                        'validation_type': 'match',
                        'response': 'OK',
                        'expected_value': True,
                        'got_value': True,
                        'message': 'Got True, expected True',
                        'advice': 'For each xref[@rid="fig1"] must have one corresponding element which @id="fig1"'
                    },
                    {
                        'title': 'xref element rid attribute validation',
                        'xpath': './/xref[@rid]',
                        'validation_type': 'match',
                        'response': 'OK',
                        'expected_value': True,
                        'got_value': True,
                        'message': 'Got True, expected True',
                        'advice': 'For each xref[@rid="table1"] must have one corresponding element which @id="table1"'
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
                        'expected_value': True,
                        'got_value': True,
                        'message': 'Got True, expected True',
                        'advice': 'For each xref[@rid="aff1"] must have one corresponding element which @id="aff1"'
                    },
                    {
                        'title': 'xref element rid attribute validation',
                        'xpath': './/xref[@rid]',
                        'validation_type': 'match',
                        'response': 'OK',
                        'expected_value': True,
                        'got_value': True,
                        'message': 'Got True, expected True',
                        'advice': 'For each xref[@rid="fig1"] must have one corresponding element which @id="fig1"'
                    },
                    {
                        'title': 'xref element rid attribute validation',
                        'xpath': './/xref[@rid]',
                        'validation_type': 'match',
                        'response': 'ERROR',
                        'expected_value': True,
                        'got_value': False,
                        'message': 'Got False, expected True',
                        'advice': 'For each xref[@rid="table1"] must have one corresponding element which @id="table1"'
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
                        'expected_value': True,
                        'got_value': True,
                        'message': 'Got True, expected True',
                        'advice': 'For each @id="aff1" must have one corresponding element which xref[@rid="aff1"]'
                    },
                    {
                        'title': 'xref element id attribute validation',
                        'xpath': './/*[@id]',
                        'validation_type': 'match',
                        'response': 'OK',
                        'expected_value': True,
                        'got_value': True,
                        'message': 'Got True, expected True',
                        'advice': 'For each @id="fig1" must have one corresponding element which xref[@rid="fig1"]'
                    },
                    {
                        'title': 'xref element id attribute validation',
                        'xpath': './/*[@id]',
                        'validation_type': 'match',
                        'response': 'OK',
                        'expected_value': True,
                        'got_value': True,
                        'message': 'Got True, expected True',
                        'advice': 'For each @id="table1" must have one corresponding element which xref[@rid="table1"]'
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
                        'expected_value': True,
                        'got_value': True,
                        'message': 'Got True, expected True',
                        'advice': 'For each @id="aff1" must have one corresponding element which xref[@rid="aff1"]'
                    },
                    {
                        'title': 'xref element id attribute validation',
                        'xpath': './/*[@id]',
                        'validation_type': 'match',
                        'response': 'OK',
                        'expected_value': True,
                        'got_value': True,
                        'message': 'Got True, expected True',
                        'advice': 'For each @id="fig1" must have one corresponding element which xref[@rid="fig1"]'
                    },
                    {
                        'title': 'xref element id attribute validation',
                        'xpath': './/*[@id]',
                        'validation_type': 'match',
                        'response': 'ERROR',
                        'expected_value': True,
                        'got_value': False,
                        'message': 'Got False, expected True',
                        'advice': 'For each @id="table1" must have one corresponding element which xref[@rid="table1"]'
                    }
                ]
        }
        obtained = self.article_xref.validate_id()
        self.assertDictEqual(expected, obtained)
