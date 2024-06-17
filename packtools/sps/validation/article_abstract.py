from packtools.sps.models.article_abstract import ArticleVisualAbstracts, ArticleHighlights
from packtools.sps.validation.utils import format_response


class HighlightsValidation:
    def __init__(self, xmltree):
        self.highlights = list(ArticleHighlights(xmltree).article_highlights())

    def highlight_validation(self, error_level=None):
        error_level = error_level or 'WARNING'
        if not self.highlights:
            yield format_response(
                title="Article highlights validation",
                parent=None,
                parent_id=None,
                parent_article_type=None,
                parent_lang=None,
                item="abstract",
                sub_item='@abstract-type="key-points"',
                validation_type="exist",
                is_valid=False,
                expected="article highlights",
                obtained=None,
                advice=None,
                data=None,
                error_level=error_level
            )
        else:
            for highlight in self.highlights:
                yield format_response(
                    title="Article highlights validation",
                    parent=highlight.get("parent"),
                    parent_id=highlight.get("parent_id"),
                    parent_article_type=highlight.get("parent_article_type"),
                    parent_lang=highlight.get("parent_lang"),
                    item="abstract",
                    sub_item='@abstract-type="key-points"',
                    validation_type="exist",
                    is_valid=True,
                    expected=highlight.get("highlights"),
                    obtained=highlight.get("highlights"),
                    advice=None,
                    data=highlight,
                    error_level=error_level
                )


class VisualAbstractsValidation:
    def __init__(self, xmltree):
        self.visual_abstracts = list(ArticleVisualAbstracts(xmltree).article_visual_abstracts())

    def visual_abstracts_validation(self, error_level=None):
        error_level = error_level or 'WARNING'
        if not self.visual_abstracts:
            yield format_response(
                title="Article visual abstracts validation",
                parent=None,
                parent_id=None,
                parent_article_type=None,
                parent_lang=None,
                item="abstract",
                sub_item='@abstract-type="graphical"',
                validation_type="exist",
                is_valid=False,
                expected="article visual abstracts",
                obtained=None,
                advice=None,
                data=None,
                error_level=error_level
            )
        else:
            for visual_abstract in self.visual_abstracts:
                yield format_response(
                    title="Article visual abstracts validation",
                    parent=visual_abstract.get("parent"),
                    parent_id=visual_abstract.get("parent_id"),
                    parent_article_type=visual_abstract.get("parent_article_type"),
                    parent_lang=visual_abstract.get("parent_lang"),
                    item="abstract",
                    sub_item='@abstract-type="graphical"',
                    validation_type="exist",
                    is_valid=True,
                    expected=visual_abstract.get("graphic"),
                    obtained=visual_abstract.get("graphic"),
                    advice=None,
                    data=visual_abstract,
                    error_level=error_level
                )
