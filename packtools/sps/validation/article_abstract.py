from packtools.sps.models.article_abstract import ArticleVisualAbstracts, ArticleHighlights, ArticleAbstract
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

    def tag_list_in_abstract_validation(self, error_level="ERROR"):
        for highlight in self.highlights:
            if highlight.get("list"):
                yield format_response(
                    title="tag <list> in abstract",
                    parent=highlight.get("parent"),
                    parent_id=highlight.get("parent_id"),
                    parent_article_type=highlight.get("parent_article_type"),
                    parent_lang=highlight.get("parent_lang"),
                    item="abstract",
                    sub_item='@abstract-type="key-points"',
                    validation_type="exist",
                    is_valid=False,
                    expected=f"<title><p>{highlight.get('list')[0]}</p></title> for each item",
                    obtained=f"<list><item>{highlight.get('list')[0]}</item></list> in each item",
                    advice="Replace <list> + <item> for <title> + <p>",
                    data=highlight,
                    error_level=error_level
                )

    def tag_p_in_abstract_validation(self, error_level="ERROR"):
        for highlight in self.highlights:
            if not highlight.get("title") or len(highlight.get("highlights")) <= 1:
                yield format_response(
                    title="tag <p> in abstract",
                    parent=highlight.get("parent"),
                    parent_id=highlight.get("parent_id"),
                    parent_article_type=highlight.get("parent_article_type"),
                    parent_lang=highlight.get("parent_lang"),
                    item="abstract",
                    sub_item='@abstract-type="key-points"',
                    validation_type="exist",
                    is_valid=False,
                    expected="more than one <title><p>item</p></title>",
                    obtained=" ".join([f"<title><p>{item}</p></title>" for item in highlight.get('highlights')]),
                    advice="Provide more than one item like <title><p>item</p></title>",
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


class ArticleAbstractValidation:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.abstracts = ArticleAbstract(xml_tree, selection="all")

    def abstract_type_validation(self, error_level="ERROR"):
        for item in self.abstracts.get_abstracts():
            if item.get("abstract_type") not in ["key-points", "graphical"]:
                yield format_response(
                    title="abstract-type attribute",
                    parent=item.get("parent"),
                    parent_id=item.get("parent_id"),
                    parent_article_type=item.get("parent_article_type"),
                    parent_lang=item.get("parent_lang"),
                    item="abstract",
                    sub_item='@abstract-type',
                    validation_type="value in list",
                    is_valid=False,
                    expected='<abstract abstract-type="key-points"> or <abstract abstract-type="graphical">',
                    obtained=f'<abstract abstract-type="{item.get("abstract_type")}">',
                    advice='Provide <abstract abstract-type="key-points"> or <abstract abstract-type="graphical">',
                    data=item,
                    error_level=error_level
                )
