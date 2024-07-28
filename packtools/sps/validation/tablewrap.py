from ..models.tablewrap import ArticleTableWraps
from ..validation.utils import format_response


class TableWrapValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.table_wraps_by_language = ArticleTableWraps(xmltree).items_by_lang

    def validate_tablewrap_existence(self, error_level="WARNING"):
        if self.table_wraps_by_language:
            for lang, table_wrap_data in self.table_wraps_by_language.items():
                yield format_response(
                    title="validation of <table-wrap> elements",
                    parent=table_wrap_data.get("parent"),
                    parent_id=table_wrap_data.get("parent_id"),
                    parent_article_type=table_wrap_data.get("parent_article_type"),
                    parent_lang=table_wrap_data.get("parent_lang"),
                    item="table-wrap",
                    sub_item=None,
                    validation_type="exist",
                    is_valid=True,
                    expected=table_wrap_data.get("table_wrap_id"),
                    obtained=table_wrap_data.get("table_wrap_id"),
                    advice=None,
                    data=table_wrap_data,
                    error_level="OK",
                )
        else:
            yield format_response(
                title="validation of <table-wrap> elements",
                parent="article",
                parent_id=None,
                parent_article_type=self.xmltree.get("article-type"),
                parent_lang=self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang"),
                item="table-wrap",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="<table-wrap> element",
                obtained=None,
                advice="Add <table-wrap> element to properly illustrate the content.",
                data=None,
                error_level=error_level,
            )
