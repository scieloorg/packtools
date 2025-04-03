from packtools.sps.models.fn import XMLFns
from packtools.sps.validation.basefn import BaseFnValidation
from packtools.sps.validation.utils import build_response


class FnValidation(BaseFnValidation):

    def validate(self):
        """
        Execute all registered validations for the footnote.

        Returns:
            list[dict]: A list of validation responses (excluding None responses).
        """
        validations = [
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
        fn_types = []
        for fn_group in self.article_fn_groups:
            fn_types.append(fn_group["fn_type"])
            yield from self.validate_fn(fn_group)

        for fn_group in self.sub_article_fn_groups:
            fn_types.append(fn_group["fn_type"])
            yield from self.validate_fn(fn_group)

        yield from self.validate_edited_by()

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
