from ..models.footnotes import ArticleFootnotes
from ..models.article_and_subarticles import ArticleAndSubArticles
from ..validation.utils import format_response
from ..validation.exceptions import ValidationFootnotes


class FootnoteValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree

    @property
    def dtd_version(self):
        article = ArticleAndSubArticles(self.xmltree)
        return article.main_dtd_version

    def fn_validation(self):
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

        fns = ArticleFootnotes(self.xmltree)
        for fn in fns.article_footnotes:
            fn_type = fn.get("fn_type")
            parent = fn.get("parent")
            parent_id = fn.get("parent_id")
            parent_article_type = fn.get("parent_article_type")
            parent_lang = fn.get("parent_lang")
            fn_parent = fn.get("fn_parent")

            if dtd >= 1.3 and fn_type == "conflict":
                yield self._generate_response(fn, parent, parent_id, parent_article_type, parent_lang, fn_parent, "coi-statement", "conflict")
            elif dtd < 1.3 and fn_type == "coi-statement":
                yield self._generate_response(fn, parent, parent_id, parent_article_type, parent_lang, fn_parent, "conflict", "coi-statement")
