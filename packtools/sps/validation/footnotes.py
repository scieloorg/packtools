from packtools.sps.models.v2.notes import ArticleNotes
from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles
from packtools.sps.validation.utils import format_response
from packtools.sps.validation.exceptions import ValidationFootnotes


class AuthorNoteValidation:
    def __init__(self, fn_dict):
        self.fn_dict = fn_dict

    def missing_corresp_label_validation(self, error_level="WARNING"):
        if bool(self.fn_dict.get("corresp")) and not bool(self.fn_dict.get("corresp_label")):
            return format_response(
                title="Missing corresp label validation",
                parent=self.fn_dict.get("parent"),
                parent_id=self.fn_dict.get("parent_id"),
                parent_article_type=self.fn_dict.get("parent_article_type"),
                parent_lang=self.fn_dict.get("parent_lang"),
                item="corresp",
                sub_item="label",
                validation_type="exist",
                is_valid=False,
                expected="<label> in <corresp>",
                obtained=self.fn_dict.get("corresp_label"),
                advice="Provide <label> in <corresp>",
                data=self.fn_dict,
                error_level=error_level
            )

    def title_presence_in_corresp_validation(self, error_level="ERROR"):
        if bool(self.fn_dict.get("corresp")) and bool(self.fn_dict.get("corresp_title")):
            return format_response(
                title="Title presence in corresp validation",
                parent=self.fn_dict.get("parent"),
                parent_id=self.fn_dict.get("parent_id"),
                parent_article_type=self.fn_dict.get("parent_article_type"),
                parent_lang=self.fn_dict.get("parent_lang"),
                item="corresp",
                sub_item="title",
                validation_type="exist",
                is_valid=False,
                expected="<label> in <corresp>",
                obtained=f'<title>{self.fn_dict.get("corresp_title")}</title>',
                advice="Replace <title> by <label>",
                data=self.fn_dict,
                error_level=error_level
            )

    def bold_presence_in_corresp_validation(self, error_level="ERROR"):
        if bool(self.fn_dict.get("corresp")) and (bool(self.fn_dict.get("corresp_bold")) or self.fn_dict.get("corresp_bold") == ""):
            return format_response(
                title="Bold presence in corresp validation",
                parent=self.fn_dict.get("parent"),
                parent_id=self.fn_dict.get("parent_id"),
                parent_article_type=self.fn_dict.get("parent_article_type"),
                parent_lang=self.fn_dict.get("parent_lang"),
                item="corresp",
                sub_item="bold",
                validation_type="exist",
                is_valid=False,
                expected="<label> in <corresp>",
                obtained=f"<bold>{self.fn_dict.get('corresp_bold')}</bold>",
                advice="Replace <bold> by <label>",
                data=self.fn_dict,
                error_level=error_level
            )


class FootnoteValidation:
    def __init__(self, dtd_version, fn):
        self.dtd_version = dtd_version
        self.fn = fn

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

    def missing_fn_label_validation(self, error_level="WARNING"):
        if not bool(self.fn.get("fn_label")):
            return format_response(
                title="Missing fn label validation",
                parent=None,
                parent_id=None,
                parent_article_type=None,
                parent_lang=None,
                item="fn",
                sub_item="label",
                validation_type="exist",
                is_valid=False,
                expected="<label> in <fn>",
                obtained=self.fn.get("fn_label"),
                advice="Provide <label> in <fn>",
                data=self.fn,
                error_level=error_level
            )

    def title_presence_in_fn_validation(self, error_level="ERROR"):
        if bool(self.fn.get("fn_title")):
            return format_response(
                title="Title presence in fn validation",
                parent=None,
                parent_id=None,
                parent_article_type=None,
                parent_lang=None,
                item="fn",
                sub_item="title",
                validation_type="exist",
                is_valid=False,
                expected="<label> in <fn>",
                obtained=f'<title>{self.fn.get("fn_title")}</title>',
                advice="Replace <title> by <label>",
                data=self.fn,
                error_level=error_level
            )

    def bold_presence_in_fn_validation(self, error_level="ERROR"):
        if bool(self.fn.get("fn_bold")) or self.fn.get("fn_bold") == "":
            return format_response(
                title="Bold presence in fn validation",
                parent=None,
                parent_id=None,
                parent_article_type=None,
                parent_lang=None,
                item="fn",
                sub_item="bold",
                validation_type="exist",
                is_valid=False,
                expected="<label> in <fn>",
                obtained=f"<bold>{self.fn.get('fn_bold')}</bold>",
                advice="Replace <bold> by <label>",
                data=self.fn,
                error_level=error_level
            )


class ArticleNotesValidation:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.fns_dict = ArticleNotes(self.xml_tree).all_notes()
        self.dtd_version = xml_tree.find(".").get("dtd-version")

    def article_notes_validation(self):
        for fn_dict in self.fns_dict:
            context = {
                "parent": fn_dict.get("parent"),
                "parent_article_type": fn_dict.get("parent_article_type"),
                "parent_id": fn_dict.get("parent_id"),
                "parent_lang": fn_dict.get("parent_lang"),
            }
            for item in self.author_validation(fn_dict):
                if item:
                    item.update(context)
                    yield item
            for fn in fn_dict.get("fns"):
                for item in self.footnote_validation(fn):
                    if item:
                        item.update(context)
                        yield item

    def author_validation(self, fn_dict):
        author_validation = AuthorNoteValidation(fn_dict)
        yield author_validation.missing_corresp_label_validation()
        yield author_validation.title_presence_in_corresp_validation()
        yield author_validation.bold_presence_in_corresp_validation()

    def footnote_validation(self, fn):
        fn_validation = FootnoteValidation(self.dtd_version, fn)
        yield fn_validation.coi_statement_vs_conflict_by_dtd_validation()
        yield fn_validation.missing_fn_label_validation()
        yield fn_validation.title_presence_in_fn_validation()
        yield fn_validation.bold_presence_in_fn_validation()
