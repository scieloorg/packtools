import unittest
from lxml import etree
from packtools.sps.models.article_author_notes import ArticleAuthorNotes


class AuthorNotesTest(unittest.TestCase):
    def test_author_notes(self):
        self.xml_tree = etree.fromstring(
            '''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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

        obtained = list(ArticleAuthorNotes(self.xml_tree).author_notes)
        expected = [
            {
                'corresp': ['Correspondência: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana '
                            '22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                'fn_count': 1,
                'fn_types': ['conflict'],
                'parent': 'article',
                'parent_id': None,
                'parent_lang': 'pt',
                'parent_article_type': 'research-article',
            },
            {
                'corresp': ['Correspondence: Karine de Lima Sírio Boclin Sousa Lima, 257 apto. 902 Copacabana '
                            '22081-010 Rio de Janeiro, RJ, Brasil E-mail: karine.boclin@gmail.com'],
                'fn_count': 1,
                'fn_types': ['conflict'],
                'parent': 'sub-article',
                'parent_id': 'TRen',
                'parent_lang': 'en',
                'parent_article_type': 'translation',
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)


if __name__ == '__main__':
    unittest.main()
