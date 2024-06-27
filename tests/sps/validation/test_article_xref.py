from unittest import TestCase

from lxml import etree

from packtools.sps.validation.article_xref import ArticleXrefValidation


class ArticleXrefValidationTest(TestCase):

    def test_validate_rids_matches(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article>
                <front>
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
                </front>
            </article>
            """
        )
        obtained = list(ArticleXrefValidation(self.xmltree).validate_rid())

        expected = [
            {
                'title': 'xref element rid attribute validation',
                'parent': 'article',
                'parent_article_type': None,
                'parent_id': None,
                'parent_lang': None,
                'item': 'xref',
                'sub_item': '@rid',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'aff1',
                'got_value': 'aff1',
                'message': 'Got aff1, expected aff1',
                'advice': None,
                'data': {
                    'ids': [('aff', 'aff1'), ('fig', 'fig1'), ('table', 'table1')],
                    'parent': 'article',
                    'parent_article_type': None,
                    'parent_id': None,
                    'parent_lang': None,
                    'rids': ['aff1', 'fig1', 'table1']},
            },
            {
                'title': 'xref element rid attribute validation',
                'parent': 'article',
                'parent_article_type': None,
                'parent_id': None,
                'parent_lang': None,
                'item': 'xref',
                'sub_item': '@rid',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'fig1',
                'got_value': 'fig1',
                'message': 'Got fig1, expected fig1',
                'advice': None,
                'data': {
                    'ids': [('aff', 'aff1'), ('fig', 'fig1'), ('table', 'table1')],
                    'parent': 'article',
                    'parent_article_type': None,
                    'parent_id': None,
                    'parent_lang': None,
                    'rids': ['aff1', 'fig1', 'table1']},
            },
            {
                'title': 'xref element rid attribute validation',
                'parent': 'article',
                'parent_article_type': None,
                'parent_id': None,
                'parent_lang': None,
                'item': 'xref',
                'sub_item': '@rid',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'table1',
                'got_value': 'table1',
                'message': 'Got table1, expected table1',
                'advice': None,
                'data': {
                    'ids': [('aff', 'aff1'), ('fig', 'fig1'), ('table', 'table1')],
                    'parent': 'article',
                    'parent_article_type': None,
                    'parent_id': None,
                    'parent_lang': None,
                    'rids': ['aff1', 'fig1', 'table1']},
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_rids_no_matches(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article>
                <front>
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
                </front>
            </article>
            """
        )
        self.article_xref = ArticleXrefValidation(self.xmltree)

        expected = [
            {
                'title': 'xref element rid attribute validation',
                'parent': 'article',
                'parent_article_type': None,
                'parent_id': None,
                'parent_lang': None,
                'item': 'xref',
                'sub_item': '@rid',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'aff1',
                'got_value': 'aff1',
                'message': 'Got aff1, expected aff1',
                'advice': None,
                'data': {
                    'ids': [('aff', 'aff1'), ('fig', 'fig1')],
                    'parent': 'article',
                    'parent_article_type': None,
                    'parent_id': None,
                    'parent_lang': None,
                    'rids': ['aff1', 'fig1', 'table1']},
            },
            {
                'title': 'xref element rid attribute validation',
                'parent': 'article',
                'parent_article_type': None,
                'parent_id': None,
                'parent_lang': None,
                'item': 'xref',
                'sub_item': '@rid',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'fig1',
                'got_value': 'fig1',
                'message': 'Got fig1, expected fig1',
                'advice': None,
                'data': {
                    'ids': [('aff', 'aff1'), ('fig', 'fig1')],
                    'parent': 'article',
                    'parent_article_type': None,
                    'parent_id': None,
                    'parent_lang': None,
                    'rids': ['aff1', 'fig1', 'table1']},
            },
            {
                'title': 'xref element rid attribute validation',
                'parent': 'article',
                'parent_article_type': None,
                'parent_id': None,
                'parent_lang': None,
                'item': 'xref',
                'sub_item': '@rid',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': 'table1',
                'got_value': None,
                'message': 'Got None, expected table1',
                'advice': 'For each xref[@rid="table1"] must have at least one corresponding element which @id="table1"',
                'data': {
                    'ids': [('aff', 'aff1'), ('fig', 'fig1')],
                    'parent': 'article',
                    'parent_article_type': None,
                    'parent_id': None,
                    'parent_lang': None,
                    'rids': ['aff1', 'fig1', 'table1']},
            }
        ]
        obtained = list(self.article_xref.validate_rid())
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_ids_matches(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article>
                <front>
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
                </front>
            </article>
            """
        )
        self.article_xref = ArticleXrefValidation(self.xmltree)

        expected = [
            {
                'title': 'element id attribute validation',
                'parent': 'article',
                'parent_article_type': None,
                'parent_id': None,
                'parent_lang': None,
                'item': 'aff',
                'sub_item': '@id',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'aff1',
                'got_value': 'aff1',
                'message': 'Got aff1, expected aff1',
                'advice': None,
                'data': {
                    'ids': [('aff', 'aff1'), ('fig', 'fig1'), ('table', 'table1')],
                    'parent': 'article',
                    'parent_article_type': None,
                    'parent_id': None,
                    'parent_lang': None,
                    'rids': ['aff1', 'fig1', 'table1']
                }
            },
            {
                'title': 'element id attribute validation',
                'parent': 'article',
                'parent_article_type': None,
                'parent_id': None,
                'parent_lang': None,
                'item': 'fig',
                'sub_item': '@id',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'fig1',
                'got_value': 'fig1',
                'message': 'Got fig1, expected fig1',
                'advice': None,
                'data': {
                    'ids': [('aff', 'aff1'), ('fig', 'fig1'), ('table', 'table1')],
                    'parent': 'article',
                    'parent_article_type': None,
                    'parent_id': None,
                    'parent_lang': None,
                    'rids': ['aff1', 'fig1', 'table1']
                }
            },
            {
                'title': 'element id attribute validation',
                'parent': 'article',
                'parent_article_type': None,
                'parent_id': None,
                'parent_lang': None,
                'item': 'table',
                'sub_item': '@id',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'table1',
                'got_value': 'table1',
                'message': 'Got table1, expected table1',
                'advice': None,
                'data': {
                    'ids': [('aff', 'aff1'), ('fig', 'fig1'), ('table', 'table1')],
                    'parent': 'article',
                    'parent_article_type': None,
                    'parent_id': None,
                    'parent_lang': None,
                    'rids': ['aff1', 'fig1', 'table1']
                }
            }
        ]

        obtained = list(self.article_xref.validate_id())

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_ids_no_matches(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article>
                <front>
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
                </front>
            </article>
            """
        )
        self.article_xref = ArticleXrefValidation(self.xmltree)

        expected = [
            {
                'title': 'element id attribute validation',
                'parent': 'article',
                'parent_article_type': None,
                'parent_id': None,
                'parent_lang': None,
                'item': 'aff',
                'sub_item': '@id',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'aff1',
                'got_value': 'aff1',
                'message': 'Got aff1, expected aff1',
                'advice': None,
                'data': {
                    'ids': [('aff', 'aff1'), ('fig', 'fig1'), ('table', 'table1')],
                    'parent': 'article',
                    'parent_article_type': None,
                    'parent_id': None,
                    'parent_lang': None,
                    'rids': ['aff1', 'fig1']
                },
            },
            {
                'title': 'element id attribute validation',
                'parent': 'article',
                'parent_article_type': None,
                'parent_id': None,
                'parent_lang': None,
                'item': 'fig',
                'sub_item': '@id',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'fig1',
                'got_value': 'fig1',
                'message': 'Got fig1, expected fig1',
                'advice': None,
                'data': {
                    'ids': [('aff', 'aff1'), ('fig', 'fig1'), ('table', 'table1')],
                    'parent': 'article',
                    'parent_article_type': None,
                    'parent_id': None,
                    'parent_lang': None,
                    'rids': ['aff1', 'fig1']
                },
            },
            {
                'title': 'element id attribute validation',
                'parent': 'article',
                'parent_article_type': None,
                'parent_id': None,
                'parent_lang': None,
                'item': 'table',
                'sub_item': '@id',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': 'table1',
                'got_value': None,
                'message': 'Got None, expected table1',
                'advice': 'For each @id="table1" must have at least one corresponding element which xref[@rid="table1"]',
                'data': {
                    'ids': [('aff', 'aff1'), ('fig', 'fig1'), ('table', 'table1')],
                    'parent': 'article',
                    'parent_article_type': None,
                    'parent_id': None,
                    'parent_lang': None,
                    'rids': ['aff1', 'fig1']
                },
            }
        ]

        obtained = list(self.article_xref.validate_id())

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)
