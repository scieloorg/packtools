from packtools.sps.models.article_abstract import ArticleVisualAbstracts, ArticleHighlights, ArticleAbstract
from packtools.sps.validation.utils import format_response


class AbstractValidationBase:
    def __init__(self, xmltree, expected, item_type, sub_item_type, extractor_class):
        self.items = list(extractor_class(xmltree).article_abstracts())
        self.item_type = item_type
        self.sub_item_type = sub_item_type
        self.expected = expected

    def validate_existence(self, error_level='WARNING'):
        if not self.items:
            yield self._format_response(
                title=f"Article {self.item_type}",
                is_valid=False,
                expected=self.item_type,
                obtained=None,
                error_level=error_level
            )
        else:
            for item in self.items:
                yield self._format_response(
                    title=f"Article {self.item_type}",
                    is_valid=True,
                    expected=item.get(self.expected),
                    obtained=item.get(self.expected),
                    data=item,
                    error_level=error_level
                )

    def kwd_in_abstract_validation(self, error_level="ERROR"):
        for item in self.items:
            if item.get("kwds"):
                yield self._format_response(
                    title="kwd in abstract",
                    is_valid=False,
                    expected=f"keywords (<kwd>) not in <abstract abstract-type='{self.sub_item_type}'>",
                    obtained=item.get("kwds"),
                    advice=f"Remove keywords (<kwd>) from <abstract abstract-type='{self.sub_item_type}'>",
                    data=item,
                    error_level=error_level
                )

    def _format_response(self, title, is_valid, expected, obtained, advice=None, data=None, error_level='WARNING'):
        return format_response(
            title=title,
            parent=data.get("parent") if data else None,
            parent_id=data.get("parent_id") if data else None,
            parent_article_type=data.get("parent_article_type") if data else None,
            parent_lang=data.get("parent_lang") if data else None,
            item="abstract",
            sub_item=f'@abstract-type="{self.sub_item_type}"',
            validation_type="exist",
            is_valid=is_valid,
            expected=expected,
            obtained=obtained,
            advice=advice,
            data=data,
            error_level=error_level
        )


class HighlightsValidation(AbstractValidationBase):
    def __init__(self, xmltree):
        super().__init__(xmltree, "highlights", "highlights", "key-points", ArticleHighlights)

    def tag_list_in_abstract_validation(self, error_level="ERROR"):
        for highlight in self.items:
            if highlight.get("list"):
                yield self._format_response(
                    title="tag <list> in abstract",
                    is_valid=False,
                    expected=f"<title><p>{highlight.get('list')[0]}</p></title> for each item",
                    obtained=f"<list><item>{highlight.get('list')[0]}</item></list> in each item",
                    advice="Replace <list> + <item> for <title> + <p>",
                    data=highlight,
                    error_level=error_level
                )

    def tag_p_in_abstract_validation(self, error_level="ERROR"):
        for highlight in self.items:
            if not highlight.get("title") or len(highlight.get("highlights")) <= 1:
                obtained = f"<title>{highlight.get('title')}</title>" + "".join([f"<p>{item}</p>" for item in highlight.get('highlights', [])])
                yield self._format_response(
                    title="tag <p> in abstract",
                    is_valid=False,
                    expected="<title>TITLE</title> and more than one <p>ITEM</p>",
                    obtained=obtained,
                    advice="Provide like <title>TITLE</title> and more than one <p>ITEM</p>",
                    data=highlight,
                    error_level=error_level
                )


class VisualAbstractsValidation(AbstractValidationBase):
    def __init__(self, xmltree):
        super().__init__(xmltree, "graphic", "visual abstracts", "graphical", ArticleVisualAbstracts)


class ArticleAbstractValidation:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.abstracts = ArticleAbstract(xml_tree, selection="all")

    def abstract_type_validation(self, error_level="ERROR", expected_abstract_type_validate=None):
        for item in self.abstracts.get_abstracts():
            if item.get("abstract_type") not in expected_abstract_type_validate:
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
