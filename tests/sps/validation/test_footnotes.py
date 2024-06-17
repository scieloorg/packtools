import unittest
from lxml import etree

from packtools.sps.validation.footnotes import FootnoteValidation


class MyTestCase(unittest.TestCase):
    def test_fn_validation_coi_statement_expected(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.3" article-type="research-article" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<author-notes>'
            '<corresp>'
            '<label>Correspondência</label>:  Roseana Mara Aredes Priuli  Av. Juscelino Kubistcheck de Oliveira, 1220, '
            'Jardim Panorama, Condomínio Recanto Real Rua 4, 440  15021-450 São José do Rio Preto, SP, Brasil  E-mail: '
            '<email>roseanap@gmail.com</email>'
            '</corresp>'
            '<fn id="fn_01" fn-type="conflict">'
            '<p>Os autores declaram não haver conflito de interesses.</p>'
            '</fn>'
            '</author-notes>'
            '</article-meta>'
            '</front>'
            '<sub-article article-type="translation" id="TRen" xml:lang="en">'
            '<front-stub>'
            '<author-notes>'
            '<fn fn-type="conflict">'
            '<p>The authors declare there is no conflict of interest.</p>'
            '</fn>'
            '</author-notes>'
            '</front-stub>'
            '</sub-article>'
            '</article>'
        )
        obtained = list(FootnoteValidation(xmltree).fn_validation())

        expected = [
            {
                'title': 'Footnotes validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'author-notes',
                'sub_item': 'fn',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': '<fn fn-type="coi-statement">',
                'got_value': '<fn fn-type="conflict">',
                'message': 'Got <fn fn-type="conflict">, expected <fn fn-type="coi-statement">',
                'advice': 'replace conflict with coi-statement',
                'data': {
                    'fn_id': 'fn_01',
                    'fn_parent': 'author-notes',
                    'fn_type': 'conflict',
                    'parent': 'article',
                    'parent_id': None,
                    'parent_article_type': 'research-article',
                    'parent_lang': 'pt'
                },
            },
            {
                'title': 'Footnotes validation',
                'parent': 'sub-article',
                'parent_id': 'TRen',
                'parent_article_type': 'translation',
                'parent_lang': 'en',
                'item': 'author-notes',
                'sub_item': 'fn',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': '<fn fn-type="coi-statement">',
                'got_value': '<fn fn-type="conflict">',
                'message': 'Got <fn fn-type="conflict">, expected <fn fn-type="coi-statement">',
                'advice': 'replace conflict with coi-statement',
                'data': {
                    'fn_id': None,
                    'fn_parent': 'author-notes',
                    'fn_type': 'conflict',
                    'parent': 'sub-article',
                    'parent_id': 'TRen',
                    'parent_article_type': 'translation',
                    'parent_lang': 'en'
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_fn_validation_conflit_expected(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.2" article-type="research-article" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<author-notes>'
            '<corresp>'
            '<label>Correspondência</label>:  Roseana Mara Aredes Priuli  Av. Juscelino Kubistcheck de Oliveira, 1220, '
            'Jardim Panorama, Condomínio Recanto Real Rua 4, 440  15021-450 São José do Rio Preto, SP, Brasil  E-mail: '
            '<email>roseanap@gmail.com</email>'
            '</corresp>'
            '<fn id="fn_01" fn-type="coi-statement">'
            '<p>Os autores declaram não haver conflito de interesses.</p>'
            '</fn>'
            '</author-notes>'
            '</article-meta>'
            '</front>'
            '<sub-article article-type="translation" id="TRen" xml:lang="en">'
            '<front-stub>'
            '<author-notes>'
            '<fn fn-type="coi-statement">'
            '<p>The authors declare there is no conflict of interest.</p>'
            '</fn>'
            '</author-notes>'
            '</front-stub>'
            '</sub-article>'
            '</article>'
        )
        obtained = list(FootnoteValidation(xmltree).fn_validation())

        expected = [
            {
                'title': 'Footnotes validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'author-notes',
                'sub_item': 'fn',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': '<fn fn-type="conflict">',
                'got_value': '<fn fn-type="coi-statement">',
                'message': 'Got <fn fn-type="coi-statement">, expected <fn fn-type="conflict">',
                'advice': 'replace coi-statement with conflict',
                'data': {
                    'fn_id': 'fn_01',
                    'fn_parent': 'author-notes',
                    'fn_type': 'coi-statement',
                    'parent': 'article',
                    'parent_id': None,
                    'parent_article_type': 'research-article',
                    'parent_lang': 'pt'
                },
            },
            {
                'title': 'Footnotes validation',
                'parent': 'sub-article',
                'parent_id': 'TRen',
                'parent_article_type': 'translation',
                'parent_lang': 'en',
                'item': 'author-notes',
                'sub_item': 'fn',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': '<fn fn-type="conflict">',
                'got_value': '<fn fn-type="coi-statement">',
                'message': 'Got <fn fn-type="coi-statement">, expected <fn fn-type="conflict">',
                'advice': 'replace coi-statement with conflict',
                'data': {
                    'fn_id': None,
                    'fn_parent': 'author-notes',
                    'fn_type': 'coi-statement',
                    'parent': 'sub-article',
                    'parent_id': 'TRen',
                    'parent_article_type': 'translation',
                    'parent_lang': 'en'
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


if __name__ == '__main__':
    unittest.main()
