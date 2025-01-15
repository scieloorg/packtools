from packtools.sps.models.author_notes import ArticleAuthorNotes
from packtools.sps.validation.utils import build_response
from packtools.sps.validation.exceptions import ValidationFnTypeException
from packtools.sps.validation.basefn import BaseFnValidation


class AuthorNotesFnValidation(BaseFnValidation):

    def validate_current_affiliation_attrib_type_deprecation(self):
        if "current-aff" == self.fn_data.get("fn_type"):
            return build_response(
                title="unexpected current-aff",
                parent=self.fn_data,
                item="fn",
                sub_item="@fn-type",
                validation_type="unexpected",
                is_valid=False,
                expected=expected,
                obtained=self.fn_data.get("fn_type"),
                advice=f"Use '<bio>' instead of @fn-type='current-aff'",
                data=self.fn_data,
                error_level=self.rules["current-aff_error_level"],
            )

    def validate_contribution_attrib_type_deprecation(self):
        if "con" == self.fn_data.get("fn_type"):
            return build_response(
                title="unexpected con",
                parent=self.fn_data,
                item="fn",
                sub_item="@fn-type",
                validation_type="unexpected",
                is_valid=False,
                expected=expected,
                obtained=self.fn_data.get("fn_type"),
                advice=f"Use '<role>' instead of @fn-type='con'",
                data=self.fn_data,
                error_level=self.rules["con_error_level"],
            )

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
            self.validate_current_affiliation_attrib_type_deprecation,
            self.validate_contribution_attrib_type_deprecation,
        ]
        return [response for validate in validations if (response := validate())]


class ArticleAuthorNotesValidation:
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

        xml_article = ArticleAuthorNotes(xml_tree)
        self.article_author_notes = xml_article.article_author_notes()
        self.sub_article_author_notes = xml_article.sub_article_author_notes()

    def validate(self):
        """
        Validate all footnote groups in the XML document.

        Yields:
            dict: Validation results for each footnote.
        """
        for fn_group in self.article_author_notes:
            if corresp_data := fn_group.get("corresp_data"):
                corresp_validator = CorrespValidation(corresp_data, self.rules)
                yield corresp_validator.validate_title()
                yield corresp_validator.validate_bold()
                yield corresp_validator.validate_label()

            for fn in fn_group.get("fns"):
                yield from self.validate_fn(fn)

        for fn_group in self.sub_article_author_notes:
            if corresp_data := fn_group.get("corresp_data"):
                corresp_validator = CorrespValidation(corresp_data, self.rules)
                yield corresp_validator.validate_title()
                yield corresp_validator.validate_bold()
                yield corresp_validator.validate_label()

            for fn in fn_group.get("fns"):
                yield from self.validate_fn(fn)

    def validate_fn(self, fn):
        """
        Validate an individual footnote and update the response with context.

        Args:
            fn (dict): The footnote to validate.
            context (dict): Context metadata for the footnote.

        Yields:
            dict: Validation results for the footnote.
        """
        validator = AuthorNotesFnValidation(fn_data=fn, rules=self.rules)
        yield from validator.validate()


class CorrespValidation:

    def __init__(self, corresp_data, rules):
        """
        Initialize the CorrespValidation object.

        Args:
            corresp_data (dict): Data related to the corresp.
            rules (dict): Rules defining validation constraints and error levels.
        """
        self.corresp_data = corresp_data
        self.rules = rules

    def validate_label(self):
        """
        Validate the presence of the 'label' in the corresp.
        """
        if not self.corresp_data.get("corresp_label"):
            return build_response(
                title="label",
                parent=self.corresp_data,
                item="corresp",
                sub_item="label",
                validation_type="exist",
                is_valid=False,
                expected="corresp/label",
                obtained=None,
                advice=f"Check if corresp label is present and identify it with label element",
                data=self.corresp_data,
                error_level=self.rules["corresp_label_error_level"],
            )

    def validate_title(self):
        """
        Validate the presence of 'title' when 'label' is expected.
        """
        if self.corresp_data.get("corresp_title"):
            return build_response(
                title="unexpected title element",
                parent=self.corresp_data,
                item="corresp",
                sub_item="unexpected title",
                validation_type="unexpected",
                is_valid=False,
                expected="corresp/label",
                obtained="corresp/title",
                advice=f"Replace corresp/title by corresp/label",
                data=self.corresp_data,
                error_level=self.rules["corresp_title_error_level"],
            )

    def validate_bold(self):
        """
        Validate the presence of 'bold' when 'label' is expected.
        """
        if self.corresp_data.get("corresp_bold"):
            return build_response(
                title="unexpected bold element",
                parent=self.corresp_data,
                item="corresp",
                sub_item="unexpected bold",
                validation_type="unexpected",
                is_valid=False,
                expected="corresp/label",
                obtained="corresp/bold",
                advice=f"Replace corresp/bold by corresp/label",
                data=self.corresp_data,
                error_level=self.rules["corresp_bold_error_level"],
            )
