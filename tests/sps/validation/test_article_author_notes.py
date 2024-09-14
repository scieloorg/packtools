import unittest
from lxml import etree

from packtools.sps.validation.article_author_notes import AuthorNotesValidation
from packtools.sps.models.article_author_notes import ArticleAuthorNotes


class ArticleAuthorNotesValidationTest(unittest.TestCase):
    def test_validate_corresp_tag_presence_success(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            '''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="pt">
            <front>
            <article-meta>
            <author-notes>
            <corresp>
            <label>Correspondência</label>:  Karine de Lima Sírio Boclin  Sousa Lima, 257 apto. 902 Copacabana  22081-010 Rio de Janeiro, RJ, Brasil  E-mail: <email>karine.boclin@gmail.com</email>
            </corresp>
            <fn fn-type="conflict">
            <p>Os autores declaram não haver conflito de interesses.</p>
            </fn>
            </author-notes>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
            <front-stub>
            <author-notes>
            <corresp>
            <label>Correspondence</label>:  Karine de Lima Sírio Boclin  Sousa Lima, 257 apto. 902 Copacabana  22081-010 Rio de Janeiro, RJ, Brasil  E-mail: <email>karine.boclin@gmail.com</email>
            </corresp>
            <fn fn-type="conflict">
            <p>The authors declare that there is no conflict of interest.</p>
            </fn>
            </author-notes>
            </front-stub>
            </sub-article>
            </article>
            '''
        )
        author_note = list(ArticleAuthorNotes(self.xmltree).author_notes)[0]
        obtained = list(AuthorNotesValidation(self.xmltree).validate_corresp_tag_presence(author_note))
        expected = [
            {
                'title': 'Author notes validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'author-notes',
                'sub_item': 'corresp',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': ['Correspondência: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana '
                                   '22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                'got_value': ['Correspondência: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana '
                              '22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                'message': "Got ['Correspondência: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana "
                           "22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'], expected "
                           "['Correspondência: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana "
                           "22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com']",
                'advice': None,
                'data': {
                    'corresp': ['Correspondência: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana'
                                     ' 22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                    'fn_count': 1,
                    'fn_types': ['conflict'],
                    'parent': 'article',
                    'parent_id': None,
                    'parent_article_type': 'research-article',
                    'parent_lang': 'pt'
                }
            }]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_corresp_tag_presence_fail(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            '''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="pt">
            <front>
            <article-meta>
            <author-notes>
            
            <fn fn-type="conflict">
            <p>Os autores declaram não haver conflito de interesses.</p>
            </fn>
            </author-notes>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
            <front-stub>
            <author-notes>
            
            <fn fn-type="conflict">
            <p>The authors declare that there is no conflict of interest.</p>
            </fn>
            </author-notes>
            </front-stub>
            </sub-article>
            </article>
            '''
        )
        author_note = list(ArticleAuthorNotes(self.xmltree).author_notes)[0]
        obtained = list(AuthorNotesValidation(self.xmltree).validate_corresp_tag_presence(author_note))
        expected = [
            {
                'title': 'Author notes validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'author-notes',
                'sub_item': 'corresp',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'corresponding author identification',
                'got_value': [],
                'message': "Got [], expected corresponding author identification",
                'advice': 'provide identification data of the corresponding author',
                'data': {
                    'corresp': [],
                    'fn_count': 1,
                    'fn_types': ['conflict'],
                    'parent': 'article',
                    'parent_id': None,
                    'parent_article_type': 'research-article',
                    'parent_lang': 'pt'
                }
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_fn_type_attribute_presence_success(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            '''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="pt">
            <front>
            <article-meta>
            <author-notes>
            <corresp>
            <label>Correspondência</label>:  Karine de Lima Sírio Boclin  Sousa Lima, 257 apto. 902 Copacabana  22081-010 Rio de Janeiro, RJ, Brasil  E-mail: <email>karine.boclin@gmail.com</email>
            </corresp>
            <fn fn-type="conflict">
            <p>Os autores declaram não haver conflito de interesses.</p>
            </fn>
            </author-notes>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
            <front-stub>
            <author-notes>
            <corresp>
            <label>Correspondence</label>:  Karine de Lima Sírio Boclin  Sousa Lima, 257 apto. 902 Copacabana  22081-010 Rio de Janeiro, RJ, Brasil  E-mail: <email>karine.boclin@gmail.com</email>
            </corresp>
            <fn fn-type="conflict">
            <p>The authors declare that there is no conflict of interest.</p>
            </fn>
            </author-notes>
            </front-stub>
            </sub-article>
            </article>
            '''
        )

        author_note = list(ArticleAuthorNotes(self.xmltree).author_notes)[0]
        obtained = list(AuthorNotesValidation(self.xmltree).validate_fn_type_attribute_presence(author_note))
        expected = [
            {
                'title': 'Author notes validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'fn',
                'sub_item': '@fn-type',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '1 fn-types',
                'got_value': '1 fn-types',
                'message': "Got 1 fn-types, expected 1 fn-types",
                'advice': None,
                'data': {
                    'corresp': ['Correspondência: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana'
                                     ' 22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                    'fn_count': 1,
                    'fn_types': ['conflict'],
                    'parent': 'article',
                    'parent_id': None,
                    'parent_article_type': 'research-article',
                    'parent_lang': 'pt'
                }
            }
            ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_fn_type_attribute_presence_fail(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            '''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="pt">
            <front>
            <article-meta>
            <author-notes>
            <corresp>
            <label>Correspondência</label>:  Karine de Lima Sírio Boclin  Sousa Lima, 257 apto. 902 Copacabana  22081-010 Rio de Janeiro, RJ, Brasil  E-mail: <email>karine.boclin@gmail.com</email>
            </corresp>
            <fn>
            <p>Os autores declaram não haver conflito de interesses.</p>
            </fn>
            </author-notes>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
            <front-stub>
            <author-notes>
            <corresp>
            <label>Correspondence</label>:  Karine de Lima Sírio Boclin  Sousa Lima, 257 apto. 902 Copacabana  22081-010 Rio de Janeiro, RJ, Brasil  E-mail: <email>karine.boclin@gmail.com</email>
            </corresp>
            <fn>
            <p>The authors declare that there is no conflict of interest.</p>
            </fn>
            </author-notes>
            </front-stub>
            </sub-article>
            </article>
            '''
        )

        author_note = list(ArticleAuthorNotes(self.xmltree).author_notes)[0]
        obtained = list(AuthorNotesValidation(self.xmltree).validate_fn_type_attribute_presence(author_note))
        expected = [
            {
                'title': 'Author notes validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'fn',
                'sub_item': '@fn-type',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': '1 fn-types',
                'got_value': '0 fn-types',
                'message': "Got 0 fn-types, expected 1 fn-types",
                'advice': 'provide one @fn-type for each <fn> tag',
                'data': {
                    'corresp': ['Correspondência: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana'
                                     ' 22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                    'fn_count': 1,
                    'fn_types': [],
                    'parent': 'article',
                    'parent_id': None,
                    'parent_article_type': 'research-article',
                    'parent_lang': 'pt'
                }
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_fn_type_attribute_value_success(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            '''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="pt">
            <front>
            <article-meta>
            <author-notes>
            <corresp>
            <label>Correspondência</label>:  Karine de Lima Sírio Boclin  Sousa Lima, 257 apto. 902 Copacabana  22081-010 Rio de Janeiro, RJ, Brasil  E-mail: <email>karine.boclin@gmail.com</email>
            </corresp>
            <fn fn-type="conflict">
            <p>Os autores declaram não haver conflito de interesses.</p>
            </fn>
            </author-notes>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
            <front-stub>
            <author-notes>
            <corresp>
            <label>Correspondence</label>:  Karine de Lima Sírio Boclin  Sousa Lima, 257 apto. 902 Copacabana  22081-010 Rio de Janeiro, RJ, Brasil  E-mail: <email>karine.boclin@gmail.com</email>
            </corresp>
            <fn fn-type="conflict">
            <p>The authors declare that there is no conflict of interest.</p>
            </fn>
            </author-notes>
            </front-stub>
            </sub-article>
            </article>
            '''
        )

        author_note = list(ArticleAuthorNotes(self.xmltree).author_notes)[0]
        obtained = list(AuthorNotesValidation(self.xmltree).validate_fn_type_attribute_value(author_note, ['conflict']))
        expected = [
            {
                'title': 'Author notes validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'fn',
                'sub_item': '@fn-type',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['conflict'],
                'got_value': 'conflict',
                'message': "Got conflict, expected ['conflict']",
                'advice': None,
                'data': {
                    'corresp': ['Correspondência: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana'
                                     ' 22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                    'fn_count': 1,
                    'fn_types': ['conflict'],
                    'parent': 'article',
                    'parent_id': None,
                    'parent_article_type': 'research-article',
                    'parent_lang': 'pt'
                }
            }
            ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_fn_type_attribute_value_fail(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            '''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="pt">
            <front>
            <article-meta>
            <author-notes>
            <corresp>
            <label>Correspondência</label>:  Karine de Lima Sírio Boclin  Sousa Lima, 257 apto. 902 Copacabana  22081-010 Rio de Janeiro, RJ, Brasil  E-mail: <email>karine.boclin@gmail.com</email>
            </corresp>
            <fn fn-type="conflict">
            <p>Os autores declaram não haver conflito de interesses.</p>
            </fn>
            </author-notes>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
            <front-stub>
            <author-notes>
            <corresp>
            <label>Correspondence</label>:  Karine de Lima Sírio Boclin  Sousa Lima, 257 apto. 902 Copacabana  22081-010 Rio de Janeiro, RJ, Brasil  E-mail: <email>karine.boclin@gmail.com</email>
            </corresp>
            <fn fn-type="conflict">
            <p>The authors declare that there is no conflict of interest.</p>
            </fn>
            </author-notes>
            </front-stub>
            </sub-article>
            </article>
            '''
        )

        author_note = list(ArticleAuthorNotes(self.xmltree).author_notes)[0]
        obtained = list(AuthorNotesValidation(self.xmltree).validate_fn_type_attribute_value(author_note, ['coi-statement']))
        expected = [
            {
                'title': 'Author notes validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'fn',
                'sub_item': '@fn-type',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': ['coi-statement'],
                'got_value': 'conflict',
                'message': "Got conflict, expected ['coi-statement']",
                'advice': "provide a value for @fn-type according according to the list: ['coi-statement']",
                'data': {
                    'corresp': ['Correspondência: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana'
                                     ' 22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                    'fn_count': 1,
                    'fn_types': ['conflict'],
                    'parent': 'article',
                    'parent_id': None,
                    'parent_article_type': 'research-article',
                    'parent_lang': 'pt'
                }
            }
            ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_author_note(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            '''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="pt">
            <front>
            <article-meta>
            <author-notes>
            <corresp>
            <label>Correspondência</label>:  Karine de Lima Sírio Boclin  Sousa Lima, 257 apto. 902 Copacabana  22081-010 Rio de Janeiro, RJ, Brasil  E-mail: <email>karine.boclin@gmail.com</email>
            </corresp>
            <fn fn-type="conflict">
            <p>Os autores declaram não haver conflito de interesses.</p>
            </fn>
            </author-notes>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
            <front-stub>
            <author-notes>
            <corresp>
            <label>Correspondence</label>:  Karine de Lima Sírio Boclin  Sousa Lima, 257 apto. 902 Copacabana  22081-010 Rio de Janeiro, RJ, Brasil  E-mail: <email>karine.boclin@gmail.com</email>
            </corresp>
            <fn fn-type="conflict">
            <p>The authors declare that there is no conflict of interest.</p>
            </fn>
            </author-notes>
            </front-stub>
            </sub-article>
            </article>
            '''
        )

        obtained = list(AuthorNotesValidation(self.xmltree).validate_author_note(['conflict']))
        expected = [
            {
                'title': 'Author notes validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'author-notes',
                'sub_item': 'corresp',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': ['Correspondência: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana '
                                   '22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                'got_value': ['Correspondência: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana '
                              '22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                'message': "Got ['Correspondência: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana "
                           "22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'], expected ["
                           "'Correspondência: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana "
                           "22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com']",
                'advice': None,
                'data': {
                    'corresp': ['Correspondência: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana'
                                     ' 22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                    'fn_count': 1,
                    'fn_types': ['conflict'],
                    'parent': 'article',
                    'parent_id': None,
                    'parent_article_type': 'research-article',
                    'parent_lang': 'pt'
                }
            },
            {
                'title': 'Author notes validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'fn',
                'sub_item': '@fn-type',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '1 fn-types',
                'got_value': '1 fn-types',
                'message': 'Got 1 fn-types, expected 1 fn-types',
                'advice': None,
                'data': {
                    'corresp': ['Correspondência: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana'
                                ' 22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                    'fn_count': 1,
                    'fn_types': ['conflict'],
                    'parent': 'article',
                    'parent_id': None,
                    'parent_article_type': 'research-article',
                    'parent_lang': 'pt'
                }
            },
            {
                'title': 'Author notes validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'fn',
                'sub_item': '@fn-type',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['conflict'],
                'got_value': 'conflict',
                'message': "Got conflict, expected ['conflict']",
                'advice': None,
                'data': {
                    'corresp': ['Correspondência: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana'
                                ' 22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                    'fn_count': 1,
                    'fn_types': ['conflict'],
                    'parent': 'article',
                    'parent_id': None,
                    'parent_article_type': 'research-article',
                    'parent_lang': 'pt'
                }
            },
            {
                'title': 'Author notes validation',
                'parent': 'sub-article',
                'parent_id': 'TRen',
                'parent_article_type': 'translation',
                'parent_lang': 'en',
                'item': 'author-notes',
                'sub_item': 'corresp',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': ['Correspondence: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana '
                                   '22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                'got_value': ['Correspondence: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana '
                              '22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                'message': "Got ['Correspondence: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana "
                           "22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'], expected ["
                           "'Correspondence: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana "
                           "22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com']",
                'advice': None,
                'data': {
                    'corresp': ['Correspondence: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana'
                                ' 22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                    'fn_count': 1,
                    'fn_types': ['conflict'],
                    'parent': 'sub-article',
                    'parent_id': 'TRen',
                    'parent_article_type': 'translation',
                    'parent_lang': 'en'
                }
            },
            {
                'title': 'Author notes validation',
                'parent': 'sub-article',
                'parent_id': 'TRen',
                'parent_article_type': 'translation',
                'parent_lang': 'en',
                'item': 'fn',
                'sub_item': '@fn-type',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '1 fn-types',
                'got_value': '1 fn-types',
                'message': 'Got 1 fn-types, expected 1 fn-types',
                'advice': None,
                'data': {
                    'corresp': ['Correspondence: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana'
                                ' 22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                    'fn_count': 1,
                    'fn_types': ['conflict'],
                    'parent': 'sub-article',
                    'parent_id': 'TRen',
                    'parent_article_type': 'translation',
                    'parent_lang': 'en'
                }
            },
            {
                'title': 'Author notes validation',
                'parent': 'sub-article',
                'parent_id': 'TRen',
                'parent_article_type': 'translation',
                'parent_lang': 'en',
                'item': 'fn',
                'sub_item': '@fn-type',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['conflict'],
                'got_value': 'conflict',
                'message': "Got conflict, expected ['conflict']",
                'advice': None,
                'data': {
                    'corresp': ['Correspondence: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana'
                                ' 22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                    'fn_count': 1,
                    'fn_types': ['conflict'],
                    'parent': 'sub-article',
                    'parent_id': 'TRen',
                    'parent_article_type': 'translation',
                    'parent_lang': 'en'
                }
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_current_affiliation_attrib_type_deprecation(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            '''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="pt">
            <front>
            <article-meta>
            <author-notes>
            <fn fn-type="current-aff">
            <institution>Universidade de São Paulo</institution>
            <addr-line>Departamento de Biologia</addr-line>
            <city>São Paulo</city>
            <country>Brasil</country>
            </fn>
            </author-notes>
            </article-meta>
            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
            <front-stub>
            <author-notes>
            <fn fn-type="current-aff">
            <institution>University of São Paulo</institution>
            <addr-line>Department of Biology</addr-line>
            <city>São Paulo</city>
            <country>Brazil</country>
            </fn>
            </author-notes>
            </front-stub>
            </sub-article>
            </article>
            '''
        )

        author_note = list(ArticleAuthorNotes(self.xmltree).author_notes)[0]
        obtained = list(AuthorNotesValidation(self.xmltree).validate_current_affiliation_attrib_type_deprecation(author_note))
        expected = [
            {
                'title': 'Author notes current aff deprecated validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'fn',
                'sub_item': '@fn-type',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': None,
                'got_value': 'current-aff',
                'message': 'Got current-aff, expected None',
                'advice': "Author's mini CV/biography data use <bio>",
                'data': {
                    'corresp': [],
                    'fn_count': 1,
                    'fn_types': ['current-aff'],
                    'parent': 'article',
                    'parent_id': None,
                    'parent_article_type': 'research-article',
                    'parent_lang': 'pt'
                }
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_contribution_attrib_type_deprecation(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            '''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" dtd-version="1.0" article-type="research-article" xml:lang="pt">
            <front>
            <article-meta>
            <contrib-group>
            <contrib contrib-type="author">
            <name>
            <surname>Silva</surname>
            <given-names>João</given-names>
            </name>
            <role>Lead Author</role>
            </contrib>
            </contrib-group>
            <author-notes>
            <fn fn-type="con">Lead Author</fn>
            </author-notes>
            </article-meta>
            </front>
            </article>
            '''
        )

        author_note = list(ArticleAuthorNotes(self.xmltree).author_notes)[0]
        obtained = list(AuthorNotesValidation(self.xmltree).validate_contribution_attrib_type_deprecation(author_note))
        expected = [
            {
                'title': 'Author notes contribution deprecated validation',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'pt',
                'item': 'fn',
                'sub_item': '@fn-type',
                'validation_type': 'exist',
                'response': 'WARNING',
                'expected_value': None,
                'got_value': 'con',
                'message': 'Got con, expected None',
                'advice': "Using @fn-type='con' for authorship contributions is discouraged; use <role> instead.",
                'data': {
                    'corresp': [],
                    'fn_count': 1,
                    'fn_types': ['con'],
                    'parent': 'article',
                    'parent_id': None,
                    'parent_article_type': 'research-article',
                    'parent_lang': 'pt'
                }
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)


if __name__ == '__main__':
    unittest.main()
