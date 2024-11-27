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
        else:
            for element in self.elements:
                yield from TableWrapValidation(element, self.rules).validate()


class TableWrapValidation:
    """
    Validates the attributes of a <table-wrap> element.

    Args:
        data: Dictionary containing the element's data.
        rules: Dictionary containing validation rules.
    """

    def __init__(self, data, rules):
        if not isinstance(data, dict):
            raise ValueError("data must be a dictionary.")
        self.data = data
        self.rules = rules

    def validate(self):
        """
        Validates the attributes of the <table-wrap>.
        Returns a generator with validation results.
        """
        for name, title in (("table_wrap_id", "id"), ("label", "label"), ("caption", "caption")):
            if resp := self._validate_item(name, title):
                yield resp

    def _validate_item(self, name, title):
        """
        Validates the presence of an attribute in the <table-wrap>.

        Args:
            name: Name of the attribute to validate.

        Returns:
            The validation result in the expected format.
        """
        if not self.data.get(name):
            key_error_level = f"{title}_error_level"
            return format_response(
                title=title,
                parent=self.data.get("parent"),
                parent_id=self.data.get("parent_id"),
                parent_article_type=self.data.get("parent_article_type"),
                parent_lang=self.data.get("parent_lang"),
                item="table-wrap",
                sub_item=title,
                validation_type="exist",
                is_valid=False,
                expected=title,
                obtained=None,
                advice=f"Identify the {title}",
                data=self.data,
                error_level=self.rules[key_error_level],
            )
