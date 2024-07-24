from ..models.fig import ArticleFigs
from ..validation.utils import format_response


class FigValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.figures_by_language = ArticleFigs(xmltree).items_by_lang

    def validate_fig_existence(self, error_level="WARNING"):
        if self.figures_by_language:
            for lang, figure_data in self.figures_by_language.items():
                yield format_response(
                    title="validation of <fig> elements",
                    parent=figure_data.get("parent"),
                    parent_id=figure_data.get("parent_id"),
                    parent_article_type=figure_data.get("parent_article_type"),
                    parent_lang=figure_data.get("parent_lang"),
                    item="fig",
                    sub_item=None,
                    validation_type="exist",
                    is_valid=True,
                    expected=figure_data.get("fig_id"),
                    obtained=figure_data.get("fig_id"),
                    advice=None,
                    data=figure_data,
                    error_level="OK",
                )
        else:
            yield format_response(
                title="validation of <fig> elements",
                parent="article",
                parent_id=None,
                parent_article_type=self.xmltree.get("article-type"),
                parent_lang=self.xmltree.get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                item="fig",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="<fig> element",
                obtained=None,
                advice="Add <fig> element to illustrate the content.",
                data=None,
                error_level=error_level,
            )
