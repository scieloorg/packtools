import unittest
from lxml import etree

from packtools.sps.validation.article_author_notes import AuthorNotesValidation


class ArticleAuthorNotesValidationTest(unittest.TestCase):
    def test_corresp_validation_success(self):
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

        obtained = list(AuthorNotesValidation(self.xmltree).corresp_validation())
        expected = [
            {
                'title': 'Author notes validation',
                'parent': 'article',
                'parent_id': None,
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
                    'parent_id': None
                }
            },
            {
                'title': 'Author notes validation',
                'parent': 'sub-article',
                'parent_id': 'TRen',
                'item': 'author-notes',
                'sub_item': 'corresp',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': ['Correspondence: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana '
                                   '22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                'got_value': ['Correspondence: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana '
                              '22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                'message': "Got ['Correspondence: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana "
                           "22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'], expected "
                           "['Correspondence: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana "
                           "22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com']",
                'advice': None,
                'data': {
                    'corresp': ['Correspondence: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana'
                                ' 22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                    'fn_count': 1,
                    'fn_types': ['conflict'],
                    'parent': 'sub-article',
                    'parent_id': 'TRen'
                }
            }]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_corresp_validation_fail(self):
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

        obtained = list(AuthorNotesValidation(self.xmltree).corresp_validation())
        expected = [
            {
                'title': 'Author notes validation',
                'parent': 'article',
                'parent_id': None,
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
                    'parent_id': None
                }
            },
            {
                'title': 'Author notes validation',
                'parent': 'sub-article',
                'parent_id': 'TRen',
                'item': 'author-notes',
                'sub_item': 'corresp',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'corresponding author identification',
                'got_value': [],
                'message': 'Got [], expected corresponding author identification',
                'advice': 'provide identification data of the corresponding author',
                'data': {
                    'corresp': [],
                    'fn_count': 1,
                    'fn_types': ['conflict'],
                    'parent': 'sub-article',
                    'parent_id': 'TRen'
                }
            }]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_fn_type_validation_success(self):
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

        obtained = list(AuthorNotesValidation(self.xmltree).fn_type_validation())
        expected = [
            {
                'title': 'Author notes validation',
                'parent': 'article',
                'parent_id': None,
                'item': 'fn',
                'sub_item': '@fn-type',
                'validation_type': 'match',
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
                    'parent_id': None
                }
            },
            {
                'title': 'Author notes validation',
                'parent': 'sub-article',
                'parent_id': 'TRen',
                'item': 'fn',
                'sub_item': '@fn-type',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': '1 fn-types',
                'got_value': '1 fn-types',
                'message': "Got 1 fn-types, expected 1 fn-types",
                'advice': None,
                'data': {
                    'corresp': ['Correspondence: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana'
                                ' 22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                    'fn_count': 1,
                    'fn_types': ['conflict'],
                    'parent': 'sub-article',
                    'parent_id': 'TRen'
                }
            }]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_fn_type_validation_fail(self):
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

        obtained = list(AuthorNotesValidation(self.xmltree).fn_type_validation())
        expected = [
            {
                'title': 'Author notes validation',
                'parent': 'article',
                'parent_id': None,
                'item': 'fn',
                'sub_item': '@fn-type',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': '1 fn-types',
                'got_value': '0 fn-types',
                'message': "Got 0 fn-types, expected 1 fn-types",
                'advice': 'provide one <@fn-type> for each <fn> tag',
                'data': {
                    'corresp': ['Correspondência: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana'
                                     ' 22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                    'fn_count': 1,
                    'fn_types': [],
                    'parent': 'article',
                    'parent_id': None
                }
            },
            {
                'title': 'Author notes validation',
                'parent': 'sub-article',
                'parent_id': 'TRen',
                'item': 'fn',
                'sub_item': '@fn-type',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': '1 fn-types',
                'got_value': '0 fn-types',
                'message': "Got 0 fn-types, expected 1 fn-types",
                'advice': 'provide one <@fn-type> for each <fn> tag',
                'data': {
                    'corresp': ['Correspondence: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana'
                                ' 22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                    'fn_count': 1,
                    'fn_types': [],
                    'parent': 'sub-article',
                    'parent_id': 'TRen'
                }
            }]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)


if __name__ == '__main__':
    unittest.main()
