from packtools.sps.models.fn import XMLFns
from packtools.sps.validation.basefn import BaseFnValidation
from packtools.sps.validation.utils import build_response


class FnValidation(BaseFnValidation):

    def validate_fn_type_presence_in_fn_group(self):
        """
        Validate that @fn-type attribute is mandatory for <fn> in <fn-group>.
        
        SPS 1.10 Rule 3: @fn-type is required for all <fn> elements in <fn-group>.
        """
        # Check if this fn is in fn-group context
        fn_parent = self.fn_data.get("fn_parent")
        if fn_parent != "fn-group":
            return None
            
        fn_type = self.fn_data.get("fn_type")
        is_valid = fn_type is not None
        
        if not is_valid:
            advice = 'Add mandatory @fn-type attribute to <fn> in <fn-group>'
            advice_text = 'Add mandatory @fn-type attribute to <fn> in <fn-group>'
            advice_params = {}
            
            return build_response(
                title="@fn-type attribute presence in fn-group",
                parent=self.fn_data,
                item="fn",
                sub_item="@fn-type",
                validation_type="exist",
                is_valid=False,
                expected="@fn-type attribute",
                obtained=None,
                advice=advice,
                data=self.fn_data,
                error_level="CRITICAL",
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate(self):
        """
        Execute all registered validations for the footnote.

        Returns:
            list[dict]: A list of validation responses (excluding None responses).
        """
        validations = [
            self.validate_fn_type_presence_in_fn_group,
            self.validate_label,
            self.validate_title,
            self.validate_bold,
            self.validate_type,
            self.validate_conflict,
        ]
        return [response for validate in validations if (response := validate())]


class XMLFnGroupValidation:
    """
    Validates groups of footnotes in an XML document.

    Attributes:
        xml_tree (ElementTree): The XML tree representing the document.
        rules (dict): Validation rules.
    """

    def __init__(self, xml_tree, rules):
        """
        Initialize the FnGroupValidation object.

        Args:
            xml_tree (ElementTree): The XML tree to validate.
            rules (dict): Validation rules.
        """
        self.xml_tree = xml_tree
        self.rules = rules
        self.dtd_version = xml_tree

        self.xml_article = XMLFns(xml_tree)

        self.article_fn_groups = list(self.xml_article.article_fn_groups_notes())
        self.sub_article_fn_groups = list(self.xml_article.sub_article_fn_groups_notes())

    @property
    def dtd_version(self):
        return self._dtd_version

    @dtd_version.setter
    def dtd_version(self, xml_tree):
        """
        Retrieve the DTD version from the XML document.

        Returns:
            float: The DTD version.

        Raises:
            ValidationFootnotes: If the DTD version is not valid.
        """
        try:
            self._dtd_version = float(xml_tree.find(".").get("dtd-version"))
        except (TypeError, ValueError) as e:
            self._dtd_version = None

    def validate(self):
        """
        Validate all footnote groups in the XML document.

        Yields:
            dict: Validation results for each footnote.
        """
        # Validate uniqueness of <fn-group> elements
        yield from self.validate_fn_group_uniqueness()
        
        fn_types = []
        for fn_group in self.article_fn_groups:
            fn_types.append(fn_group["fn_type"])
            yield from self.validate_fn(fn_group)

        for fn_group in self.sub_article_fn_groups:
            fn_types.append(fn_group["fn_type"])
            yield from self.validate_fn(fn_group)

        yield from self.validate_edited_by()

    def validate_fn_group_uniqueness(self):
        """
        Validate that <fn-group> appears at most once in the document.
        
        SPS 1.10 Rule 6: <fn-group> should appear at most once per article/sub-article.
        """
        # Check article level - xml_tree root is already the article element
        article_fn_group_count = len(self.xml_tree.xpath("./front//fn-group | ./body//fn-group | ./back//fn-group"))
        
        if article_fn_group_count > 1:
            advice = f'<fn-group> element should appear at most once in the article. Found {article_fn_group_count} occurrences.'
            advice_text = '<fn-group> element should appear at most once in the article. Found {count} occurrences.'
            advice_params = {"count": str(article_fn_group_count)}
            
            yield build_response(
                title="fn-group uniqueness",
                parent={},
                item="fn-group",
                sub_item=None,
                validation_type="uniqueness",
                is_valid=False,
                expected="at most 1 <fn-group>",
                obtained=f"{article_fn_group_count} <fn-group> elements",
                advice=advice,
                data={"count": article_fn_group_count},
                error_level="ERROR",
                advice_text=advice_text,
                advice_params=advice_params,
            )
        
        # Check sub-article level
        for sub_article in self.xml_tree.xpath(".//sub-article"):
            sub_article_id = sub_article.get("id", "unknown")
            sub_fn_group_count = len(sub_article.xpath(".//fn-group"))
            
            if sub_fn_group_count > 1:
                advice = f'<fn-group> element should appear at most once in sub-article (id={sub_article_id}). Found {sub_fn_group_count} occurrences.'
                advice_text = '<fn-group> element should appear at most once in sub-article (id={id}). Found {count} occurrences.'
                advice_params = {
                    "id": sub_article_id,
                    "count": str(sub_fn_group_count)
                }
                
                yield build_response(
                    title="fn-group uniqueness in sub-article",
                    parent={"parent_id": sub_article_id},
                    item="fn-group",
                    sub_item=None,
                    validation_type="uniqueness",
                    is_valid=False,
                    expected="at most 1 <fn-group>",
                    obtained=f"{sub_fn_group_count} <fn-group> elements",
                    advice=advice,
                    data={"count": sub_fn_group_count, "sub_article_id": sub_article_id},
                    error_level="ERROR",
                    advice_text=advice_text,
                    advice_params=advice_params,
                )

    def validate_fn(self, fn):
        """
        Validate an individual footnote and update the response with context.

        Args:
            fn (dict): The footnote to validate.
            context (dict): Context metadata for the footnote.

        Yields:
            dict: Validation results for the footnote.
        """
        validator = FnValidation(
            fn_data=fn, rules=self.rules, dtd_version=self.dtd_version
        )
        yield from validator.validate()

    def validate_edited_by(self):
        is_valid = bool(self.xml_article.fn_edited_by)
        yield build_response(
            title="edited-by",
            parent={},
            item="fn",
            sub_item="@fn-type",
            validation_type="value",
            is_valid=is_valid,
            expected='<fn fn-type="edited-by">',
            obtained='<fn fn-type="edited-by">' if is_valid else None,
            advice='Make the responsible editor with <fn fn-type="edited-by">',
            data=list(self.xml_article.fn_edited_by),
            error_level=self.rules["fn_type_error_level"]
        )
