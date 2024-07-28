from ..models.formula import ArticleFormulas
from ..validation.utils import format_response


class FormulaValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.formulas_by_language = ArticleFormulas(xmltree).items_by_lang

    def validate_formula_existence(self, error_level="WARNING"):
        if self.formulas_by_language:
            for lang, formula_data in self.formulas_by_language.items():
                yield format_response(
                    title="validation of <formula> elements",
                    parent=formula_data.get("parent"),
                    parent_id=formula_data.get("parent_id"),
                    parent_article_type=formula_data.get("parent_article_type"),
                    parent_lang=formula_data.get("parent_lang"),
                    item=formula_data.get("alternative_parent"),
                    sub_item=None,
                    validation_type="exist",
                    is_valid=True,
                    expected=formula_data.get("formula_id"),
                    obtained=formula_data.get("formula_id"),
                    advice=None,
                    data=formula_data,
                    error_level="OK",
                )
        else:
            yield format_response(
                title="validation of <formula> elements",
                parent="article",
                parent_id=None,
                parent_article_type=self.xmltree.get("article-type"),
                parent_lang=self.xmltree.get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                item="formula",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="<formula> element",
                obtained=None,
                advice="Include <formula> elements to properly represent mathematical expressions in the content.",
                data=None,
                error_level=error_level,
            )
