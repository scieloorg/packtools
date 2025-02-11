from packtools.sps.models.author_notes import XMLAuthorNotes
from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles

from packtools.sps.validation.utils import build_response
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
                expected="bio",
                obtained=self.fn_data.get("fn_type"),
                advice='<fn fn-type="current-aff"> is deprecated. Use <fn fn-type="bio"> instead.',
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
                expected="role",
                obtained=self.fn_data.get("fn_type"),
                advice='<fn fn-type="con"> is deprecated. '
                       'Use <role content-type="http://credit.niso.org/contributor-roles/CONTRIBUTION/"> '
                       'inside <contrib> instead. Replace CONTRIBUTION with the author\'s contribution type.',
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


class XMLAuthorNotesValidation:
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
        self.dtd_version = ArticleAndSubArticles(xml_tree).dtd_version

        xml_article = XMLAuthorNotes(xml_tree)
        self.article_author_notes = xml_article.article_author_notes()
        self.sub_article_author_notes = xml_article.sub_article_author_notes()

    def validate(self):
        """
        Validate all footnote groups in the XML document.

        Yields:
            dict: Validation results for each footnote (excluding None).
        """
        fn_group = self.article_author_notes
        yield from self.validate_fn_group(fn_group)

        for fn_group in self.sub_article_author_notes:
            yield from self.validate_fn_group(fn_group)

    def validate_fn_group(self, fn_group):
        for corresp_data in fn_group.get("corresp_data"):
            corresp_validator = CorrespValidation(corresp_data, self.rules)
            for result in [
                corresp_validator.validate_title(),
                corresp_validator.validate_bold(),
                corresp_validator.validate_label()
            ]:
                if result is not None:
                    yield result

        for fn in fn_group.get("fns"):
            for result in self.validate_fn(fn):
                if result is not None:
                    yield result


    def validate_fn(self, fn):
        """
        Validate an individual footnote and update the response with context.

        Args:
            fn (dict): The footnote to validate.

        Yields:
            dict: Validation results for the footnote (excluding None).
        """
        validator = AuthorNotesFnValidation(fn_data=fn, rules=self.rules, dtd_version=self.dtd_version)
        for result in validator.validate():
            if result is not None:
                yield result


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
        corresp_label = self.corresp_data.get("corresp_label")
        is_valid = bool(corresp_label)
        return build_response(
            title="label",
            parent=self.corresp_data,
            item="corresp",
            sub_item="label",
            validation_type="exist",
            is_valid=is_valid,
            expected="corresp/label",
            obtained="corresp/label" if is_valid else None,
            advice=f"Mark corresp label with <corresp><label>",
            data=self.corresp_data,
            error_level=self.rules["corresp_label_error_level"],
        )

    def validate_title(self):
        """
        Validate the presence of 'title' when 'label' is expected.
        """
        corresp_title = self.corresp_data.get("corresp_title")
        is_valid = not bool(corresp_title)
        return build_response(
            title="unexpected title element",
            parent=self.corresp_data,
            item="corresp",
            sub_item="unexpected title",
            validation_type="unexpected",
            is_valid=is_valid,
            expected="corresp/label" if not is_valid else None,
            obtained="corresp/title" if not is_valid else None,
            advice=f"Replace <corresp><title> with <corresp><label>",
            data=self.corresp_data,
            error_level=self.rules["corresp_title_error_level"],
        )

    def validate_bold(self):
        """
        Validate the presence of 'bold' when 'label' is expected.
        """
        corresp_bold = self.corresp_data.get("corresp_bold")
        is_valid = not bool(corresp_bold)
        return build_response(
            title="unexpected bold element",
            parent=self.corresp_data,
            item="corresp",
            sub_item="unexpected bold",
            validation_type="unexpected",
            is_valid=is_valid,
            expected="corresp/label" if not is_valid else None,
            obtained="corresp/bold" if not is_valid else None,
            advice=f"Replace <corresp><bold> with <corresp><label>",
            data=self.corresp_data,
            error_level=self.rules["corresp_bold_error_level"],
        )
