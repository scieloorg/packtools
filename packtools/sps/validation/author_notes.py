from packtools.sps.models.author_notes import XMLAuthorNotes
from packtools.sps.models.article_and_subarticles import ArticleAndSubArticles

from packtools.sps.validation.utils import build_response
from packtools.sps.validation.basefn import BaseFnValidation


class AuthorNotesFnValidation(BaseFnValidation):

    def validate_fn_type_presence(self):
        """
        Validate that @fn-type attribute is mandatory for <fn> in <author-notes>.
        
        SPS 1.10 Rule 1: @fn-type is required for all <fn> elements in <author-notes>.
        """
        fn_type = self.fn_data.get("fn_type")
        is_valid = fn_type is not None
        
        if not is_valid:
            advice = 'Add mandatory @fn-type attribute to <fn> in <author-notes>. Valid values for author notes: abbr, coi-statement, corresp'
            advice_text = 'Add mandatory @fn-type attribute to <fn> in <author-notes>. Valid values for author notes: {values}'
            advice_params = {"values": "abbr, coi-statement, corresp"}
            
            return build_response(
                title="@fn-type attribute presence",
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

    def validate_fn_type_author_notes_values(self):
        """
        Validate that @fn-type has allowed values for <fn> in <author-notes>.
        
        SPS 1.10 Rule 2: For author notes, only specific values are allowed:
        abbr, coi-statement, corresp
        """
        fn_type = self.fn_data.get("fn_type")
        
        # Only validate if fn_type exists
        if fn_type is None:
            return None
            
        # SPS 1.10 allowed values for author-notes context
        allowed_values = ["abbr", "coi-statement", "corresp"]
        is_valid = fn_type in allowed_values
        
        if not is_valid:
            advice = f'@fn-type="{fn_type}" is not valid for <fn> in <author-notes>. Use one of: {", ".join(allowed_values)}'
            advice_text = '@fn-type="{fn_type}" is not valid for <fn> in <author-notes>. Use one of: {values}'
            advice_params = {
                "fn_type": fn_type,
                "values": ", ".join(allowed_values)
            }
            
            return build_response(
                title="@fn-type value in author-notes",
                parent=self.fn_data,
                item="fn",
                sub_item="@fn-type",
                validation_type="value in list",
                is_valid=False,
                expected=allowed_values,
                obtained=fn_type,
                advice=advice,
                data=self.fn_data,
                error_level="ERROR",
                advice_text=advice_text,
                advice_params=advice_params,
            )

    def validate_corresp_type_recommendation(self):
        """
        Warn when @fn-type="corresp" is used in <author-notes>.
        
        SPS 1.10 Rule 8: Recommend using <corresp> element instead of <fn fn-type="corresp">.
        """
        fn_type = self.fn_data.get("fn_type")
        
        if fn_type == "corresp":
            advice = 'For corresponding author information, use <corresp> element instead of <fn fn-type="corresp">'
            advice_text = 'For corresponding author information, use <corresp> element instead of <fn fn-type="corresp">'
            advice_params = {}
            
            return build_response(
                title="corresp element recommendation",
                parent=self.fn_data,
                item="fn",
                sub_item="@fn-type",
                validation_type="recommendation",
                is_valid=False,
                expected="<corresp> element",
                obtained='<fn fn-type="corresp">',
                advice=advice,
                data=self.fn_data,
                error_level="WARNING",
                advice_text=advice_text,
                advice_params=advice_params,
            )

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
            self.validate_fn_type_presence,
            self.validate_fn_type_author_notes_values,  # Replaces validate_type from BaseFnValidation with author-notes-specific values
            self.validate_corresp_type_recommendation,
            self.validate_label,
            self.validate_title,
            self.validate_bold,
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
        self.sub_article_author_notes = list(xml_article.sub_article_author_notes())

    def validate(self):
        """
        Validate all footnote groups in the XML document.

        Yields:
            dict: Validation results for each footnote (excluding None).
        """
        # Validate uniqueness of <author-notes> in article
        yield from self.validate_author_notes_uniqueness()
        
        fn_group = self.article_author_notes
        yield from self.validate_fn_group(fn_group)

        for fn_group in self.sub_article_author_notes:
            yield from self.validate_fn_group(fn_group)

    def validate_author_notes_uniqueness(self):
        """
        Validate that <author-notes> appears at most once in the document.
        
        SPS 1.10 Rule 4: <author-notes> should appear at most once per article/sub-article.
        """
        # Check article level - find root is already the article element
        article_author_notes_count = len(self.xml_tree.xpath("./front//author-notes"))
        
        if article_author_notes_count > 1:
            advice = f'<author-notes> element should appear at most once in the article. Found {article_author_notes_count} occurrences.'
            advice_text = '<author-notes> element should appear at most once in the article. Found {count} occurrences.'
            advice_params = {"count": str(article_author_notes_count)}
            
            yield build_response(
                title="author-notes uniqueness",
                parent={},
                item="author-notes",
                sub_item=None,
                validation_type="uniqueness",
                is_valid=False,
                expected="at most 1 <author-notes>",
                obtained=f"{article_author_notes_count} <author-notes> elements",
                advice=advice,
                data={"count": article_author_notes_count},
                error_level="ERROR",
                advice_text=advice_text,
                advice_params=advice_params,
            )
        
        # Check sub-article level
        for sub_article in self.xml_tree.xpath(".//sub-article"):
            sub_article_id = sub_article.get("id", "unknown")
            sub_author_notes_count = len(sub_article.xpath(".//author-notes"))
            
            if sub_author_notes_count > 1:
                advice = f'<author-notes> element should appear at most once in sub-article (id={sub_article_id}). Found {sub_author_notes_count} occurrences.'
                advice_text = '<author-notes> element should appear at most once in sub-article (id={id}). Found {count} occurrences.'
                advice_params = {
                    "id": sub_article_id,
                    "count": str(sub_author_notes_count)
                }
                
                yield build_response(
                    title="author-notes uniqueness in sub-article",
                    parent={"parent_id": sub_article_id},
                    item="author-notes",
                    sub_item=None,
                    validation_type="uniqueness",
                    is_valid=False,
                    expected="at most 1 <author-notes>",
                    obtained=f"{sub_author_notes_count} <author-notes> elements",
                    advice=advice,
                    data={"count": sub_author_notes_count, "sub_article_id": sub_article_id},
                    error_level="ERROR",
                    advice_text=advice_text,
                    advice_params=advice_params,
                )

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
