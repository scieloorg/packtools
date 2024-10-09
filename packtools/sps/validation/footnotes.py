from packtools.sps.models.v2.notes import ArticleNotes
from packtools.sps.validation.utils import format_response
from packtools.sps.validation.exceptions import ValidationFootnotes


class BaseNoteValidation:
    def __init__(self, note_dict, element_tag):
        self.note_dict = note_dict
        self.element_tag = element_tag
        self.check_element_existence = bool(self.note_dict.get("corresp")) if self.element_tag == "corresp" else True

    def missing_element_label_validation(self, error_level="WARNING"):
        if self.check_element_existence and not bool(self.note_dict.get(f"{self.element_tag}_label")):
            return format_response(
                title=f"Missing {self.element_tag} label validation",
                parent=self.note_dict.get("parent"),
                parent_id=self.note_dict.get("parent_id"),
                parent_article_type=self.note_dict.get("parent_article_type"),
                parent_lang=self.note_dict.get("parent_lang"),
                item=self.element_tag,
                sub_item="label",
                validation_type="exist",
                is_valid=False,
                expected=f"<label> in <{self.element_tag}>",
                obtained=self.note_dict.get(f"{self.element_tag}_label"),
                advice=f"Provide <label> in <{self.element_tag}>",
                data=self.note_dict,
                error_level=error_level
            )

    def title_presence_in_element_validation(self, error_level="ERROR"):
        if self.check_element_existence and bool(self.note_dict.get(f"{self.element_tag}_title")):
            return format_response(
                title=f"Title presence in {self.element_tag} validation",
                parent=self.note_dict.get("parent"),
                parent_id=self.note_dict.get("parent_id"),
                parent_article_type=self.note_dict.get("parent_article_type"),
                parent_lang=self.note_dict.get("parent_lang"),
                item=self.element_tag,
                sub_item="title",
                validation_type="exist",
                is_valid=False,
                expected=f"<label> in <{self.element_tag}>",
                obtained=f'<title>{self.note_dict.get(f"{self.element_tag}_title")}</title>',
                advice="Replace <title> by <label>",
                data=self.note_dict,
                error_level=error_level
            )

    def bold_presence_in_element_validation(self, error_level="ERROR"):
        if self.check_element_existence and (bool(self.note_dict.get(f"{self.element_tag}_bold")) or self.note_dict.get(f"{self.element_tag}_bold") == ""):
            return format_response(
                title=f"Bold presence in {self.element_tag} validation",
                parent=self.note_dict.get("parent"),
                parent_id=self.note_dict.get("parent_id"),
                parent_article_type=self.note_dict.get("parent_article_type"),
                parent_lang=self.note_dict.get("parent_lang"),
                item=self.element_tag,
                sub_item="bold",
                validation_type="exist",
                is_valid=False,
                expected=f"<label> in <{self.element_tag}>",
                obtained=f"<bold>{self.note_dict.get(f'{self.element_tag}_bold')}</bold>",
                advice="Replace <bold> by <label>",
                data=self.note_dict,
                error_level=error_level
            )


class AuthorNoteValidation(BaseNoteValidation):
    def __init__(self, fn_dict):
        super().__init__(note_dict=fn_dict, element_tag='corresp')


class FootnoteValidation(BaseNoteValidation):
    def __init__(self, dtd_version, fn):
        self.dtd_version = dtd_version
        self.fn = fn
        super().__init__(note_dict=fn, element_tag='fn')

    def coi_statement_vs_conflict_by_dtd_validation(self, error_level="ERROR"):
        """
        Checks if fn-type is coi-statement for dtd-version >= 1.3

        XML input
        ---------
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        dtd-version="1.3" article-type="research-article" xml:lang="pt">
           <front>
              <article-meta>
                 <author-notes>
                    <fn id="fn_01" fn-type="conflict">
                       <p>Os autores declaram não haver conflito de interesses.</p>
                    </fn>
                 </author-notes>
              </article-meta>
           </front>
           <sub-article article-type="translation" id="TRen" xml:lang="en">
              <front-stub>
                 <author-notes>
                    <fn fn-type="conflict">
                       <p>The authors declare there is no conflict of interest.</p>
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
                    },...
                ]
        """
        try:
            dtd = float(self.dtd_version)
        except (TypeError, ValueError) as e:
            raise ValidationFootnotes(f"dtd-version is not valid: {str(e)}")

        if not dtd:
            return

        fn_type = self.fn.get("fn_type")
        if dtd >= 1.3 and fn_type == "conflict":
            return format_response(
                title="coi statement vs conflict by dtd",
                parent=None,
                parent_id=None,
                parent_article_type=None,
                parent_lang=None,
                item=self.fn.get("fn_parent"),
                sub_item="fn",
                validation_type="match",
                is_valid=False,
                expected='<fn fn-type="coi-statement">',
                obtained='<fn fn-type="conflict">',
                advice="replace conflict with coi-statement",
                data=self.fn,
                error_level=error_level
            )
        elif dtd < 1.3 and fn_type == "coi-statement":
            return format_response(
                title="coi statement vs conflict by dtd",
                parent=None,
                parent_id=None,
                parent_article_type=None,
                parent_lang=None,
                item=self.fn.get("fn_parent"),
                sub_item="fn",
                validation_type="match",
                is_valid=False,
                expected='<fn fn-type="conflict">',
                obtained='<fn fn-type="coi-statement">',
                advice="replace coi-statement with conflict",
                data=self.fn,
                error_level=error_level
            )


class ArticleNotesValidation:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.fns_dict = list(ArticleNotes(self.xml_tree).all_notes())
        self.dtd_version = xml_tree.find(".").get("dtd-version")

    def generate_context(self, fn_dict):
        """
        Gera o contexto comum para todas as validações.
        """
        return {
            "parent": fn_dict.get("parent"),
            "parent_article_type": fn_dict.get("parent_article_type"),
            "parent_id": fn_dict.get("parent_id"),
            "parent_lang": fn_dict.get("parent_lang"),
        }

    def article_author_notes_validation(self):
        """
        Valida as notas de autor (author notes) do artigo.
        """
        for fn_dict in self.fns_dict:
            context = self.generate_context(fn_dict)
            for item in self.author_validation(fn_dict):
                if item:
                    item.update(context)
                    yield item

    def article_footnotes_validation(self):
        """
        Valida as notas de rodapé (footnotes) do artigo.
        """
        for fn_dict in self.fns_dict:
            context = self.generate_context(fn_dict)
            for fn in fn_dict.get("fns"):
                for item in self.footnote_validation(fn):
                    if item:
                        item.update(context)
                        yield item

    def article_notes_validation(self):
        """
        Executa as validações para todas as notas do artigo (autor e rodapé).
        """
        yield from self.article_author_notes_validation()
        yield from self.article_footnotes_validation()

    def author_validation(self, fn_dict):
        """
        Aplica as validações de notas de autor.
        """
        author_validation = AuthorNoteValidation(fn_dict)
        yield author_validation.missing_element_label_validation()
        yield author_validation.title_presence_in_element_validation()
        yield author_validation.bold_presence_in_element_validation()

    def footnote_validation(self, fn):
        """
        Aplica as validações de notas de rodapé.
        """
        fn_validation = FootnoteValidation(self.dtd_version, fn)
        yield fn_validation.coi_statement_vs_conflict_by_dtd_validation()
        yield fn_validation.missing_element_label_validation()
        yield fn_validation.title_presence_in_element_validation()
        yield fn_validation.bold_presence_in_element_validation()
