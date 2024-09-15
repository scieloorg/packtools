from packtools.sps.models.v2.notes import ArticleNotes
from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles
from packtools.sps.validation.utils import format_response
from packtools.sps.validation.exceptions import ValidationFootnotes


class FootnoteValidation:
    def __init__(self, xml_tree, fns_dict):
        self.xml_tree = xml_tree
        self.fns_dict = fns_dict

    @property
    def dtd_version(self):
        article = ArticleAndSubArticles(self.xml_tree)
        return article.main_dtd_version

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

        for fn in self.fns_dict.get("fns"):
            fn_type = fn.get("fn_type")
            if dtd >= 1.3 and fn_type == "conflict":
                yield format_response(
                    title="Footnotes validation",
                    parent=self.fns_dict.get("parent"),
                    parent_id=self.fns_dict.get("parent_id"),
                    parent_article_type=self.fns_dict.get("parent_article_type"),
                    parent_lang=self.fns_dict.get("parent_lang"),
                    item=fn.get("fn_parent"),
                    sub_item="fn",
                    validation_type="match",
                    is_valid=False,
                    expected='<fn fn-type="coi-statement">',
                    obtained='<fn fn-type="conflict">',
                    advice="replace conflict with coi-statement",
                    data=self.fns_dict,
                    error_level=error_level
                )
            elif dtd < 1.3 and fn_type == "coi-statement":
                yield format_response(
                    title="Footnotes validation",
                    parent=self.fns_dict.get("parent"),
                    parent_id=self.fns_dict.get("parent_id"),
                    parent_article_type=self.fns_dict.get("parent_article_type"),
                    parent_lang=self.fns_dict.get("parent_lang"),
                    item=fn.get("fn_parent"),
                    sub_item="fn",
                    validation_type="match",
                    is_valid=False,
                    expected='<fn fn-type="conflict">',
                    obtained='<fn fn-type="coi-statement">',
                    advice="replace coi-statement with conflict",
                    data=self.fns_dict,
                    error_level=error_level
                )

    def missing_corresp_label_validation(self, error_level="WARNING"):
        if bool(self.fns_dict.get("corresp")) and not bool(self.fns_dict.get("corresp_label")):
            yield format_response(
                title="Missing corresp label validation",
                parent=self.fns_dict.get("parent"),
                parent_id=self.fns_dict.get("parent_id"),
                parent_article_type=self.fns_dict.get("parent_article_type"),
                parent_lang=self.fns_dict.get("parent_lang"),
                item="corresp",
                sub_item="label",
                validation_type="exist",
                is_valid=False,
                expected="<label> in <corresp>",
                obtained=self.fns_dict.get("corresp_label"),
                advice="Provide <label> in <corresp>",
                data=self.fns_dict,
                error_level=error_level
            )

    def missing_fn_label_validation(self, error_level="WARNING"):
        for fn in self.fns_dict.get("fns"):
            if not bool(fn.get("fn_label")):
                yield format_response(
                    title="Missing fn label validation",
                    parent=self.fns_dict.get("parent"),
                    parent_id=self.fns_dict.get("parent_id"),
                    parent_article_type=self.fns_dict.get("parent_article_type"),
                    parent_lang=self.fns_dict.get("parent_lang"),
                    item="fn",
                    sub_item="label",
                    validation_type="exist",
                    is_valid=False,
                    expected="<label> in <fn>",
                    obtained=fn.get("fn_label"),
                    advice="Provide <label> in <fn>",
                    data=self.fns_dict,
                    error_level=error_level
                )

    def title_presence_in_corresp_validation(self, error_level="ERROR"):
        if bool(self.fns_dict.get("corresp")) and bool(self.fns_dict.get("corresp_title")):
            yield format_response(
                title="Title presence in corresp validation",
                parent=self.fns_dict.get("parent"),
                parent_id=self.fns_dict.get("parent_id"),
                parent_article_type=self.fns_dict.get("parent_article_type"),
                parent_lang=self.fns_dict.get("parent_lang"),
                item="corresp",
                sub_item="title",
                validation_type="exist",
                is_valid=False,
                expected="<title> not in <corresp>",
                obtained=f'<title>{self.fns_dict.get("corresp_title")}</title>',
                advice="Remove <title> from <corresp>",
                data=self.fns_dict,
                error_level=error_level
            )

    def title_presence_in_fn_validation(self, error_level="ERROR"):
        for fn in self.fns_dict.get("fns"):
            if bool(fn.get("fn_title")):
                yield format_response(
                    title="Title presence in fn validation",
                    parent=self.fns_dict.get("parent"),
                    parent_id=self.fns_dict.get("parent_id"),
                    parent_article_type=self.fns_dict.get("parent_article_type"),
                    parent_lang=self.fns_dict.get("parent_lang"),
                    item="fn",
                    sub_item="title",
                    validation_type="exist",
                    is_valid=False,
                    expected="<title> not in <fn>",
                    obtained=f'<title>{fn.get("fn_title")}</title>',
                    advice="Remove <title> from <fn>",
                    data=self.fns_dict,
                    error_level=error_level
                )

    def bold_presence_in_corresp_validation(self, error_level="ERROR"):
        if bool(self.fns_dict.get("corresp")) and (bool(self.fns_dict.get("corresp_bold")) or self.fns_dict.get("corresp_bold") == ""):
            yield format_response(
                title="Bold presence in corresp validation",
                parent=self.fns_dict.get("parent"),
                parent_id=self.fns_dict.get("parent_id"),
                parent_article_type=self.fns_dict.get("parent_article_type"),
                parent_lang=self.fns_dict.get("parent_lang"),
                item="corresp",
                sub_item="bold",
                validation_type="exist",
                is_valid=False,
                expected="<bold> not in <corresp>",
                obtained=f"<bold>{self.fns_dict.get('corresp_bold')}</bold>",
                advice="Remove <bold> from <corresp>",
                data=self.fns_dict,
                error_level=error_level
            )

    def bold_presence_in_fn_validation(self, error_level="ERROR"):
        for fn in self.fns_dict.get("fns"):
            if bool(fn.get("fn_bold")) or fn.get("fn_bold") == "":
                yield format_response(
                    title="Bold presence in fn validation",
                    parent=self.fns_dict.get("parent"),
                    parent_id=self.fns_dict.get("parent_id"),
                    parent_article_type=self.fns_dict.get("parent_article_type"),
                    parent_lang=self.fns_dict.get("parent_lang"),
                    item="fn",
                    sub_item="bold",
                    validation_type="exist",
                    is_valid=False,
                    expected="<bold> not in <fn>",
                    obtained=f"<bold>{fn.get('fn_bold')}</bold>",
                    advice="Remove <bold> from <fn>",
                    data=self.fns_dict,
                    error_level=error_level
                )


class FootnotesValidation:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree

    def article_notes_validation(self):
        for fns_dict in ArticleNotes(self.xml_tree).all_notes():
            validation = FootnoteValidation(self.xml_tree, fns_dict)
            yield from validation.coi_statement_vs_conflict_by_dtd_validation()
            yield from validation.missing_corresp_label_validation()
            yield from validation.title_presence_in_corresp_validation()
            yield from validation.title_presence_in_fn_validation()
            yield from validation.bold_presence_in_corresp_validation()
            yield from validation.bold_presence_in_fn_validation()
