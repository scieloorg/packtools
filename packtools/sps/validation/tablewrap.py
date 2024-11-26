from packtools.sps.models.tablewrap import ArticleTableWrappers
from packtools.sps.validation.utils import format_response


class ArticleTableWrapValidation:
    """
    Validates the <table-wrap> elements in an XML article.

    Args:
        xml_tree: XML object representing the article.
        rules: Dictionary containing validation rules.
    """

    def __init__(self, xml_tree, rules):
        if not hasattr(xml_tree, "get"):
            raise ValueError("xml_tree must be a valid XML object.")
        if not isinstance(rules, dict):
            raise ValueError("rules must be a dictionary containing error levels.")
        try:
            self.elements = list(ArticleTableWrappers(xml_tree).get_all_table_wrappers)
        except Exception as e:
            raise RuntimeError(f"Error processing table-wraps: {e}")
        self.xml_tree = xml_tree
        self.rules = rules

    def validate(self):
        """
        Performs validations on the article.
        Returns a generator with validation results.
        """
        if not self.elements:
            yield format_response(
                title="table-wrap presence",
                parent="article",
                parent_id=None,
                parent_article_type=self.xml_tree.get("article-type"),
                parent_lang=self.xml_tree.get(
                    "{http://www.w3.org/XML/1998/namespace}lang"
                ),
                item="table-wrap",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="<table-wrap> element",
                obtained=None,
                advice="Add <table-wrap> element to properly illustrate the content.",
                data=None,
                error_level=self.rules["absent_error_level"],
            )

    def validate_tablewrap_elements(self, error_level="ERROR"):
        if self.table_wrappers:
            for table_wrap_data in self.table_wrappers:
                elements_found = []
                for element in ["table_wrap_id", "label", "caption"]:
                    value = table_wrap_data.get(element)
                    if value:
                        elements_found.append(value)
                if not bool(elements_found):
                    yield format_response(
                        title="table-wrap elements",
                        parent=table_wrap_data.get("parent"),
                        parent_id=table_wrap_data.get("parent_id"),
                        parent_article_type=table_wrap_data.get("parent_article_type"),
                        parent_lang=table_wrap_data.get("parent_lang"),
                        item="table-wrap",
                        sub_item="table-wrap/@id or label or caption",
                        validation_type="exist",
                        is_valid=False,
                        expected="table-wrap/@id or label or caption elements",
                        obtained=elements_found,
                        advice="provide table-wrap/@id or label or caption for table-wrap",
                        data=table_wrap_data,
                        error_level=error_level,
                    )
