import unittest
from lxml import etree

from packtools.sps.validation.footnotes import FootnoteValidation
from packtools.sps.models.v2.notes import ArticleNotes


class MyTestCase(unittest.TestCase):
    def test_coi_statement_vs_conflict_by_dtd_validation_coi_statement_expected(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
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
        obtained = []
        for fns_dict in ArticleNotes(xml_tree).all_notes():
            obtained.extend(FootnoteValidation(xml_tree, fns_dict).coi_statement_vs_conflict_by_dtd_validation())

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
                    'corresp': 'Correspondência: Roseana Mara Aredes Priuli Av. '
                               'Juscelino Kubistcheck de Oliveira, 1220, Jardim '
                               'Panorama, Condomínio Recanto Real Rua 4, 440 15021-450 '
                               'São José do Rio Preto, SP, Brasil E-mail: '
                               'roseanap@gmail.com',
                    'corresp_label': 'Correspondência',
                    'corresp_title': None,
                    'corresp_bold': None,
                    'fns': [
                        {
                            'fn_bold': None,
                            'fn_id': 'fn_01',
                            'fn_label': None,
                            'fn_parent': 'author-notes',
                            'fn_text': 'Os autores declaram não haver conflito de interesses.',
                            'fn_type': 'conflict',
                            'fn_title': None
                        }
                    ],
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
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
                    'corresp': None,
                    'corresp_label': None,
                    'corresp_title': None,
                    'corresp_bold': None,
                    'fns': [
                        {
                            'fn_bold': None,
                            'fn_id': None,
                            'fn_label': None,
                            'fn_parent': 'author-notes',
                            'fn_text': 'The authors declare there is no conflict of interest.',
                            'fn_type': 'conflict',
                            'fn_title': None
                        }
                    ],
                    'parent': 'sub-article',
                    'parent_article_type': 'translation',
                    'parent_id': 'TRen',
                    'parent_lang': 'en'
                },
            },
        ]

        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_coi_statement_vs_conflict_by_dtd_validation_conflit_expected(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
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

        obtained = []
        for fns_dict in ArticleNotes(xml_tree).all_notes():
            obtained.extend(FootnoteValidation(xml_tree, fns_dict).coi_statement_vs_conflict_by_dtd_validation())

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
                    'corresp': 'Correspondência: Roseana Mara Aredes Priuli Av. '
                               'Juscelino Kubistcheck de Oliveira, 1220, Jardim '
                               'Panorama, Condomínio Recanto Real Rua 4, 440 15021-450 '
                               'São José do Rio Preto, SP, Brasil E-mail: '
                               'roseanap@gmail.com',
                    'corresp_label': 'Correspondência',
                    'corresp_title': None,
                    'corresp_bold': None,
                    'fns': [
                        {
                            'fn_bold': None,
                            'fn_id': 'fn_01',
                            'fn_label': None,
                            'fn_parent': 'author-notes',
                            'fn_text': 'Os autores declaram não haver conflito de interesses.',
                            'fn_type': 'coi-statement',
                            'fn_title': None
                        }
                    ],
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
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
                    'corresp': None,
                    'corresp_label': None,
                    'corresp_title': None,
                    'corresp_bold': None,
                    'fns': [
                        {
                            'fn_bold': None,
                            'fn_id': None,
                            'fn_label': None,
                            'fn_parent': 'author-notes',
                            'fn_text': 'The authors declare there is no conflict of interest.',
                            'fn_type': 'coi-statement',
                            'fn_title': None
                        }
                    ],
                    'parent': 'sub-article',
                    'parent_article_type': 'translation',
                    'parent_id': 'TRen',
                    'parent_lang': 'en'
                },
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_missing_corresp_label_validation(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.2" article-type="research-article" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<author-notes>'
            '<corresp>'
            'Roseana Mara Aredes Priuli  Av. Juscelino Kubistcheck de Oliveira, 1220, '
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

        obtained = []
        for fns_dict in ArticleNotes(xml_tree).all_notes():
            obtained.extend(FootnoteValidation(xml_tree, fns_dict).missing_corresp_label_validation())

        expected = [
            {
                'title': 'Missing corresp label validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'corresp',
                'sub_item': 'label',
                'validation_type': 'exist',
                'response': 'WARNING',
                'expected_value': '<label> in <corresp>',
                'got_value': None,
                'message': 'Got None, expected <label> in <corresp>',
                'advice': 'Provide <label> in <corresp>',
                'data': {
                    'corresp': 'Roseana Mara Aredes Priuli Av. '
                               'Juscelino Kubistcheck de Oliveira, 1220, Jardim '
                               'Panorama, Condomínio Recanto Real Rua 4, 440 15021-450 '
                               'São José do Rio Preto, SP, Brasil E-mail: '
                               'roseanap@gmail.com',
                    'corresp_label': None,
                    'corresp_title': None,
                    'corresp_bold': None,
                    'fns': [
                        {
                            'fn_bold': None,
                            'fn_id': 'fn_01',
                            'fn_label': None,
                            'fn_parent': 'author-notes',
                            'fn_text': 'Os autores declaram não haver conflito de interesses.',
                            'fn_type': 'coi-statement',
                            'fn_title': None
                        }
                    ],
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'pt'
                },
            }
        ]

        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_missing_fn_label_validation(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.2" article-type="research-article" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<author-notes>'
            '<corresp>'
            'Roseana Mara Aredes Priuli  Av. Juscelino Kubistcheck de Oliveira, 1220, '
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

        obtained = []
        for fns_dict in ArticleNotes(xml_tree).all_notes():
            obtained.extend(FootnoteValidation(xml_tree, fns_dict).missing_fn_label_validation())

        expected = [
            {
                'title': 'Missing fn label validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'fn',
                'sub_item': 'label',
                'validation_type': 'exist',
                'response': 'WARNING',
                'expected_value': '<label> in <fn>',
                'got_value': None,
                'message': 'Got None, expected <label> in <fn>',
                'advice': 'Provide <label> in <fn>',
                'data': {
                    'corresp': 'Roseana Mara Aredes Priuli Av. '
                               'Juscelino Kubistcheck de Oliveira, 1220, Jardim '
                               'Panorama, Condomínio Recanto Real Rua 4, 440 15021-450 '
                               'São José do Rio Preto, SP, Brasil E-mail: '
                               'roseanap@gmail.com',
                    'corresp_label': None,
                    'corresp_title': None,
                    'corresp_bold': None,
                    'fns': [
                        {
                            'fn_bold': None,
                            'fn_id': 'fn_01',
                            'fn_label': None,
                            'fn_parent': 'author-notes',
                            'fn_text': 'Os autores declaram não haver conflito de interesses.',
                            'fn_type': 'coi-statement',
                            'fn_title': None
                        }
                    ],
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'pt'
                },
            },
            {
                'title': 'Missing fn label validation',
                'parent': 'sub-article',
                'parent_id': 'TRen',
                'parent_article_type': 'translation',
                'parent_lang': 'en',
                'item': 'fn',
                'sub_item': 'label',
                'validation_type': 'exist',
                'response': 'WARNING',
                'expected_value': '<label> in <fn>',
                'got_value': None,
                'message': 'Got None, expected <label> in <fn>',
                'advice': 'Provide <label> in <fn>',
                'data': {
                    'corresp': None,
                    'corresp_label': None,
                    'corresp_title': None,
                    'corresp_bold': None,
                    'fns': [
                        {
                            'fn_bold': None,
                            'fn_id': None,
                            'fn_label': None,
                            'fn_parent': 'author-notes',
                            'fn_text': 'The authors declare there is no conflict of interest.',
                            'fn_type': 'coi-statement',
                            'fn_title': None
                        }
                    ],
                    'parent': 'sub-article',
                    'parent_article_type': 'translation',
                    'parent_id': 'TRen',
                    'parent_lang': 'en'
                },
            }
        ]

        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_title_presence_in_corresp_validation(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.2" article-type="research-article" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<author-notes>'
            '<corresp>'
            '<title>Correspondente</title>'
            'Roseana Mara Aredes Priuli  Av. Juscelino Kubistcheck de Oliveira, 1220, '
            'Jardim Panorama, Condomínio Recanto Real Rua 4, 440  15021-450 São José do Rio Preto, SP, Brasil  E-mail: '
            '<email>roseanap@gmail.com</email>'
            '</corresp>'
            '<fn id="fn_01" fn-type="coi-statement">'
            '<p>Os autores declaram não haver conflito de interesses.</p>'
            '</fn>'
            '</author-notes>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        obtained = []
        for fns_dict in ArticleNotes(xml_tree).all_notes():
            obtained.extend(FootnoteValidation(xml_tree, fns_dict).title_presence_in_corresp_validation())

        expected = [
            {
                'title': 'Title presence in corresp validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'corresp',
                'sub_item': 'title',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': '<title> not in <corresp>',
                'got_value': '<title>Correspondente</title>',
                'message': 'Got <title>Correspondente</title>, expected <title> not in <corresp>',
                'advice': 'Remove <title> from <corresp>',
                'data': {
                    'corresp': 'CorrespondenteRoseana Mara Aredes Priuli Av. '
                               'Juscelino Kubistcheck de Oliveira, 1220, Jardim '
                               'Panorama, Condomínio Recanto Real Rua 4, 440 15021-450 '
                               'São José do Rio Preto, SP, Brasil E-mail: '
                               'roseanap@gmail.com',
                    'corresp_label': None,
                    'corresp_title': 'Correspondente',
                    'corresp_bold': None,
                    'fns': [
                        {
                            'fn_bold': None,
                            'fn_id': 'fn_01',
                            'fn_label': None,
                            'fn_parent': 'author-notes',
                            'fn_text': 'Os autores declaram não haver conflito de interesses.',
                            'fn_type': 'coi-statement',
                            'fn_title': None
                        }
                    ],
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'pt'
                },
            }
        ]

        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_title_presence_in_fn_validation(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.2" article-type="research-article" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<author-notes>'
            '<corresp>'
            '<title>Correspondente</title>'
            'Roseana Mara Aredes Priuli  Av. Juscelino Kubistcheck de Oliveira, 1220, '
            'Jardim Panorama, Condomínio Recanto Real Rua 4, 440  15021-450 São José do Rio Preto, SP, Brasil  E-mail: '
            '<email>roseanap@gmail.com</email>'
            '</corresp>'
            '<fn id="fn_01" fn-type="coi-statement">'
            '<title>Conflito</title>'
            '<p>Os autores declaram não haver conflito de interesses.</p>'
            '</fn>'
            '</author-notes>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        obtained = []
        for fns_dict in ArticleNotes(xml_tree).all_notes():
            obtained.extend(FootnoteValidation(xml_tree, fns_dict).title_presence_in_fn_validation())

        expected = [
            {
                'title': 'Title presence in fn validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'fn',
                'sub_item': 'title',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': '<title> not in <fn>',
                'got_value': '<title>Conflito</title>',
                'message': 'Got <title>Conflito</title>, expected <title> not in <fn>',
                'advice': 'Remove <title> from <fn>',
                'data': {
                    'corresp': 'CorrespondenteRoseana Mara Aredes Priuli Av. '
                               'Juscelino Kubistcheck de Oliveira, 1220, Jardim '
                               'Panorama, Condomínio Recanto Real Rua 4, 440 15021-450 '
                               'São José do Rio Preto, SP, Brasil E-mail: '
                               'roseanap@gmail.com',
                    'corresp_label': None,
                    'corresp_title': 'Correspondente',
                    'corresp_bold': None,
                    'fns': [
                        {
                            'fn_bold': None,
                            'fn_id': 'fn_01',
                            'fn_label': None,
                            'fn_parent': 'author-notes',
                            'fn_text': 'ConflitoOs autores declaram não haver conflito de interesses.',
                            'fn_type': 'coi-statement',
                            'fn_title': 'Conflito'
                        }
                    ],
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'pt'
                },
            }
        ]

        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_bold_presence_in_corresp_validation(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.2" article-type="research-article" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<author-notes>'
            '<corresp>'
            '<bold></bold>'
            'Roseana Mara Aredes Priuli  Av. Juscelino Kubistcheck de Oliveira, 1220, '
            'Jardim Panorama, Condomínio Recanto Real Rua 4, 440  15021-450 São José do Rio Preto, SP, Brasil  E-mail: '
            '<email>roseanap@gmail.com</email>'
            '</corresp>'
            '<fn id="fn_01" fn-type="coi-statement">'
            '<p>Os autores declaram não haver conflito de interesses.</p>'
            '</fn>'
            '</author-notes>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        obtained = []
        for fns_dict in ArticleNotes(xml_tree).all_notes():
            obtained.extend(FootnoteValidation(xml_tree, fns_dict).bold_presence_in_corresp_validation())

        expected = [
            {
                'title': 'Bold presence in corresp validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'corresp',
                'sub_item': 'bold',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': '<bold> not in <corresp>',
                'got_value': '<bold></bold>',
                'message': 'Got <bold></bold>, expected <bold> not in <corresp>',
                'advice': 'Remove <bold> from <corresp>',
                'data': {
                    'corresp': 'Roseana Mara Aredes Priuli Av. '
                               'Juscelino Kubistcheck de Oliveira, 1220, Jardim '
                               'Panorama, Condomínio Recanto Real Rua 4, 440 15021-450 '
                               'São José do Rio Preto, SP, Brasil E-mail: '
                               'roseanap@gmail.com',
                    'corresp_label': None,
                    'corresp_title': None,
                    'corresp_bold': "",
                    'fns': [
                        {
                            'fn_bold': None,
                            'fn_id': 'fn_01',
                            'fn_label': None,
                            'fn_parent': 'author-notes',
                            'fn_text': 'Os autores declaram não haver conflito de interesses.',
                            'fn_type': 'coi-statement',
                            'fn_title': None
                        }
                    ],
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'pt'
                },
            }
        ]

        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_bold_presence_in_fn_validation(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.2" article-type="research-article" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<author-notes>'
            '<corresp>'
            '<title>Correspondente</title>'
            'Roseana Mara Aredes Priuli  Av. Juscelino Kubistcheck de Oliveira, 1220, '
            'Jardim Panorama, Condomínio Recanto Real Rua 4, 440  15021-450 São José do Rio Preto, SP, Brasil  E-mail: '
            '<email>roseanap@gmail.com</email>'
            '</corresp>'
            '<fn id="fn_01" fn-type="coi-statement">'
            '<bold>Conflito</bold>'
            '<p>Os autores declaram não haver conflito de interesses.</p>'
            '</fn>'
            '</author-notes>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        obtained = []
        for fns_dict in ArticleNotes(xml_tree).all_notes():
            obtained.extend(FootnoteValidation(xml_tree, fns_dict).bold_presence_in_fn_validation())

        expected = [
            {
                'title': 'Bold presence in fn validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'fn',
                'sub_item': 'bold',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': '<bold> not in <fn>',
                'got_value': '<bold>Conflito</bold>',
                'message': 'Got <bold>Conflito</bold>, expected <bold> not in <fn>',
                'advice': 'Remove <bold> from <fn>',
                'data': {
                    'corresp': 'CorrespondenteRoseana Mara Aredes Priuli Av. '
                               'Juscelino Kubistcheck de Oliveira, 1220, Jardim '
                               'Panorama, Condomínio Recanto Real Rua 4, 440 15021-450 '
                               'São José do Rio Preto, SP, Brasil E-mail: '
                               'roseanap@gmail.com',
                    'corresp_label': None,
                    'corresp_title': 'Correspondente',
                    'corresp_bold': None,
                    'fns': [
                        {
                            'fn_bold': 'Conflito',
                            'fn_id': 'fn_01',
                            'fn_label': None,
                            'fn_parent': 'author-notes',
                            'fn_text': 'ConflitoOs autores declaram não haver conflito de interesses.',
                            'fn_type': 'coi-statement',
                            'fn_title': None
                        }
                    ],
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'pt'
                },
            }
        ]

        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


if __name__ == '__main__':
    unittest.main()
