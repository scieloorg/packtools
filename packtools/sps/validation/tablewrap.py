from lxml import etree

from packtools.sps.models.tablewrap import ArticleTableWrappers
from packtools.sps.validation.utils import format_response


class TableWrapValidation:
    def __init__(self, xmltree):
        self.xmltree = xmltree
        self.table_wrappers = list(ArticleTableWrappers(xmltree).article_table_wrappers)

    def validate_tablewrap_existence(self, error_level="WARNING"):
        if self.table_wrappers:
            for table_wrap_data in self.table_wrappers:
                table_wrap_node = table_wrap_data.get("node").element
                yield format_response(
                    title="table-wrap presence",
                    parent=table_wrap_data.get("parent"),
                    parent_id=table_wrap_data.get("parent_id"),
                    parent_article_type=table_wrap_data.get("parent_article_type"),
                    parent_lang=table_wrap_data.get("parent_lang"),
                    item="table-wrap",
                    sub_item=None,
                    validation_type="exist",
                    is_valid=True,
                    expected="<table-wrap> element",
                    obtained=etree.tostring(table_wrap_node, encoding='unicode'),
                    advice=None,
                    data=table_wrap_data,
                    error_level="OK",
                )
        else:
            yield format_response(
                title="table-wrap presence",
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
