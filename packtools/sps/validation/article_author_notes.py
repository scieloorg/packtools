from packtools.sps.models.article_author_notes import ArticleAuthorNotes
from packtools.sps.validation.utils import format_response
from packtools.sps.validation.exceptions import ValidationFnTypeException


class AuthorNotesValidation:
    def __init__(self, xmltree, fn_type_list=None):
        self.xmltree = xmltree
        self.author_notes = ArticleAuthorNotes(self.xmltree).author_notes
        self.fn_type_list = fn_type_list

    def validate_corresp_tag_presence(self, author_note, error_level="ERROR"):
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
        corresp = author_note.get("corresp")
        is_valid = bool(corresp)
        yield format_response(
            title="Author notes validation",
            parent=author_note.get("parent"),
            parent_id=author_note.get("parent_id"),
            parent_article_type=author_note.get("parent_article_type"),
            parent_lang=author_note.get("parent_lang"),
            item="author-notes",
            sub_item="corresp",
            validation_type="exist",
            is_valid=is_valid,
            expected=corresp if is_valid else "corresponding author identification",
            obtained=corresp,
            advice="provide identification data of the corresponding author",
            error_level=error_level,
            data=author_note
        )

    def validate_fn_type_attribute_presence(self, author_note, error_level="ERROR"):
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
        fn_types = author_note.get("fn_types")
        fn_count = author_note.get("fn_count")
        is_valid = len(fn_types) == fn_count
        yield format_response(
            title="Author notes validation",
            parent=author_note.get("parent"),
            parent_id=author_note.get("parent_id"),
            parent_article_type=author_note.get("parent_article_type"),
            parent_lang=author_note.get("parent_lang"),
            item="fn",
            sub_item="@fn-type",
            validation_type="exist",
            is_valid=is_valid,
            expected=f"{fn_count} fn-types",
            obtained=f"{len(fn_types)} fn-types",
            advice="provide one @fn-type for each <fn> tag",
            error_level=error_level,
            data=author_note
        )

    def validate_fn_type_attribute_value(self, author_note, fn_type_list=None, error_level="ERROR"):
        """
            Checks whether the value of the fn-type tag complies with the list of expected values.

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
                    },...
                ]
            """
        fn_type_list = fn_type_list or self.fn_type_list
        if not fn_type_list:
            raise ValidationFnTypeException("Function requires list of fn-types")
        for fn_type in author_note.get("fn_types") or []:
            yield format_response(
                title="Author notes validation",
                parent=author_note.get("parent"),
                parent_id=author_note.get("parent_id"),
                parent_article_type=author_note.get("parent_article_type"),
                parent_lang=author_note.get("parent_lang"),
                item="fn",
                sub_item="@fn-type",
                validation_type="value in list",
                is_valid=fn_type in fn_type_list,
                expected=fn_type_list,
                obtained=fn_type,
                advice=f"provide a value for @fn-type according according to the list: {fn_type_list}",
                error_level=error_level,
                data=author_note
            )

    def validate_author_note(self, fn_type_list=None):
        for author_note in self.author_notes:
            yield from self.validate_corresp_tag_presence(author_note)
            yield from self.validate_fn_type_attribute_presence(author_note)
            yield from self.validate_fn_type_attribute_value(author_note, fn_type_list)
