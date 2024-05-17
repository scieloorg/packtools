from packtools.sps.models.article_author_notes import ArticleAuthorNotes
from packtools.sps.validation.utils import format_response


class AuthorNotesValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.author_notes = ArticleAuthorNotes(self.xmltree).author_notes

    def validate_corresp_tag_presence(self):
        """
            Checks the existence of the corresponding author identification.

            XML input
            ---------
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

            Returns
            -------
            list of dict
                A list of dictionaries, such as:
                [
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
                            'parent_id': None,
                            'parent_article_type': 'research-article',
                            'parent_lang': 'pt'
                        }
                    },,...
                ]
            """
        for author_note in self.author_notes:
            corresp = author_note.get("corresp")
            is_valid = bool(corresp)
            yield format_response(
                title="Author notes validation",
                parent=author_note.get("parent"),
                parent_id=author_note.get("parent_id"),
                item="author-notes",
                sub_item="corresp",
                validation_type="exist",
                is_valid=is_valid,
                expected=corresp if is_valid else "corresponding author identification",
                obtained=corresp,
                advice="provide identification data of the corresponding author",
                data=author_note
            )

    def validate_fn_type_attribute_presence(self):
        """
            Checks if every fn tag has the fn-type attribute.

            XML input
            ---------
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

            Returns
            -------
            list of dict
                A list of dictionaries, such as:
                [
                    {
                        'title': 'Author notes validation',
                        'parent': 'article',
                        'parent_id': None,
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
                    },...
                ]
            """
        for author_note in self.author_notes:
            fn_types = author_note.get("fn_types")
            fn_count = author_note.get("fn_count")
            is_valid = len(fn_types) == fn_count
            yield format_response(
                title="Author notes validation",
                parent=author_note.get("parent"),
                parent_id=author_note.get("parent_id"),
                item="fn",
                sub_item="@fn-type",
                validation_type="exist",
                is_valid=is_valid,
                expected=f"{fn_count} fn-types",
                obtained=f"{len(fn_types)} fn-types",
                advice="provide one @fn-type for each <fn> tag",
                data=author_note
            )


