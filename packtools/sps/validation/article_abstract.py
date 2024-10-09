from packtools.sps.models.article_abstract import ArticleVisualAbstracts, ArticleHighlights, ArticleAbstract
from packtools.sps.validation.utils import format_response


class AbstractValidationBase:
    """
    Base class for validating article abstracts.

    Args:
        abstract (dict): A dictionary containing the abstract information to be validated.
    """

    def __init__(self, abstract):
        # this is a dictionary with abstract data
        self.abstract = abstract

    def validate_unexpected_kwd(self, error_level="ERROR"):
        """
        Validates if unexpected keywords (kwd) are present in the abstract.

        Args:
            error_level (str): Error level to be reported. Default is "ERROR".

        Returns:
            dict: Formatted validation response if unexpected keywords are found.
        """
        if self.abstract.get("kwds"):
            return self._format_response(
                title="unexpected kwd",
                sub_item="kwd",
                is_valid=False,
                validation_type="exist",
                obtained=self.abstract.get("kwds"),
                advice=f"Remove keywords (<kwd>) from <abstract abstract-type='{self.abstract.get('abstract_type')}'>",
                error_level=error_level
            )

    def validate_tag_title_in_abstract(self, error_level="ERROR"):
        """
        Validates if the abstract contains a title.

        Args:
            error_level (str): Error level to be reported. Default is "ERROR".

        Returns:
            dict: Formatted validation response if the title is missing.
        """
        if not self.abstract.get("title"):
            return self._format_response(
                title="title",
                sub_item="title",
                validation_type="exist",
                is_valid=False,
                expected="title",
                advice="Provide title",
                error_level=error_level
            )

    def _format_response(self, title, sub_item, is_valid, validation_type, expected=None, obtained=None, advice=None,
                         error_level='WARNING'):
        """
        Formats the validation response.

        Args:
            title (str): The title of the validation issue.
            sub_item (str): The sub-item being validated.
            is_valid (bool): Whether the validation passed or failed.
            validation_type (str): The type of validation.
            expected (str, optional): The expected value.
            obtained (str, optional): The obtained value.
            advice (str, optional): Advice on how to resolve the issue. Default is None.
            error_level (str): The error level. Default is 'WARNING'.

        Returns:
            dict: A formatted validation response.
        """
        return format_response(
            title=title,
            parent=self.abstract.get("parent"),
            parent_id=self.abstract.get("parent_id"),
            parent_article_type=self.abstract.get("parent_article_type"),
            parent_lang=self.abstract.get("parent_lang"),
            item=f'abstract ({self.abstract.get("abstract_type")})',
            sub_item=sub_item,
            validation_type=validation_type,
            is_valid=is_valid,
            expected=expected,
            obtained=obtained,
            advice=advice,
            data=self.abstract,
            error_level=error_level
        )


class AbstractsValidationBase:
    """
    Base class for validating multiple article abstracts.

    Args:
        xml_tree (lxml.etree._Element): XML tree of the article.
        abstracts (list): List of abstracts to be validated.
    """

    def __init__(self, xml_tree, abstracts):
        self.xml_tree = xml_tree
        # this is a list of dictionaries with abstract data
        self.abstracts = abstracts

    def validate_exists(self, error_level="WARNING"):
        """
        Validates if the article contains any abstracts.

        Args:
            error_level (str): Error level to be reported. Default is "WARNING".

        Returns:
            dict: Formatted validation response if no abstracts are found.
        """
        if not self.abstracts:
            return format_response(
                title="Article abstracts",
                parent="article",
                parent_id=None,
                parent_article_type=self.xml_tree.get("id"),
                parent_lang=self.xml_tree.get("{http://www.w3.org/XML/1998/namespace}lang"),
                item="abstract",
                sub_item=None,
                validation_type="exist",
                is_valid=False,
                expected="abstracts",
                obtained=self.abstracts,
                advice="article has no abstract",
                data=None,
                error_level=error_level
            )


class HighlightValidation(AbstractValidationBase):
    """
    Validation class for article highlights, inheriting from AbstractValidationBase.
    """

    def validate_tag_list_in_abstract(self, error_level="ERROR"):
        """
        Validates if <list> tag is present in the abstract and suggests replacing it with <p>.

        Args:
            error_level (str): Error level to be reported. Default is "ERROR".

        Returns:
            dict: Formatted validation response if <list> tag is found.
        """
        if self.abstract.get("list"):
            return self._format_response(
                title="list",
                sub_item="list",
                validation_type="exist",
                is_valid=False,
                obtained=self.abstract.get('list'),
                advice="Remove <list> and add <p>",
                error_level=error_level
            )

    def validate_tag_p_in_abstract(self, error_level="ERROR"):
        """
        Validates if the abstract contains more than one <p> tag.

        Args:
            error_level (str): Error level to be reported. Default is "ERROR".

        Returns:
            dict: Formatted validation response if less than two <p> tags are found.
        """
        if len(self.abstract.get("highlights")) <= 1:
            return self._format_response(
                title="p",
                sub_item="p",
                validation_type="exist",
                is_valid=False,
                expected="p",
                obtained=self.abstract.get("highlights"),
                advice="Provide more than one p",
                error_level=error_level
            )


class HighlightsValidation(AbstractsValidationBase):
    """
    Validation class for highlights section of articles, inheriting from AbstractsValidationBase.
    """

    def __init__(self, xml_tree):
        # this is a list of dictionaries with highlight abstract data
        self.abstracts = list(ArticleHighlights(xml_tree).article_abstracts())
        super().__init__(xml_tree, self.abstracts)

    def validate(self, kwd_error_level="ERROR", title_error_level="ERROR", p_error_level="ERROR",
                 list_error_level="ERROR"):
        """
        Runs the validation checks for keywords, title, paragraph, and list tags in highlights.

        Args:
            kwd_error_level (str): Error level for keyword validation. Default is "ERROR".
            title_error_level (str): Error level for title validation. Default is "ERROR".
            p_error_level (str): Error level for paragraph validation. Default is "ERROR".
            list_error_level (str): Error level for list validation. Default is "ERROR".

        Yields:
            dict: Formatted validation responses for each issue found.
        """
        for abstract in self.abstracts:
            validations = HighlightValidation(abstract)
            yield validations.validate_unexpected_kwd(kwd_error_level)
            yield validations.validate_tag_title_in_abstract(title_error_level)
            yield validations.validate_tag_p_in_abstract(p_error_level)
            yield validations.validate_tag_list_in_abstract(list_error_level)


class VisualAbstractValidation(AbstractValidationBase):
    """
    Validation class for visual abstracts, inheriting from AbstractValidationBase.
    """

    def validate_tag_graphic_in_abstract(self, error_level="ERROR"):
        """
        Validates if the abstract contains a <graphic> tag.

        Args:
            error_level (str): Error level to be reported. Default is "ERROR".

        Returns:
            dict: Formatted validation response if the <graphic> tag is missing.
        """
        if not self.abstract.get("graphic"):
            return self._format_response(
                title="graphic",
                sub_item="graphic",
                validation_type="exist",
                is_valid=False,
                expected="graphic",
                advice="Provide graphic",
                error_level=error_level
            )


class VisualAbstractsValidation(AbstractsValidationBase):
    """
    Validation class for visual abstracts, inheriting from AbstractsValidationBase.
    """

    def __init__(self, xml_tree):
        # this is a list of dictionaries with visual abstract data
        self.abstracts = list(ArticleVisualAbstracts(xml_tree).article_abstracts())
        super().__init__(xml_tree, self.abstracts)

    def validate(self, kwd_error_level="ERROR", title_error_level="ERROR", graphic_error_level="ERROR"):
        """
        Runs the validation checks for keywords, title, and graphic tags in visual abstracts.

        Args:
            kwd_error_level (str): Error level for keyword validation. Default is "ERROR".
            title_error_level (str): Error level for title validation. Default is "ERROR".
            graphic_error_level (str): Error level for graphic validation. Default is "ERROR".

        Yields:
            dict: Formatted validation responses for each issue found.
        """
        for abstract in self.abstracts:
            validations = VisualAbstractValidation(abstract)
            yield validations.validate_unexpected_kwd(kwd_error_level)
            yield validations.validate_tag_title_in_abstract(title_error_level)
            yield validations.validate_tag_graphic_in_abstract(graphic_error_level)


class ArticleAbstractsValidation:
    """
    Class to validate various types of abstracts in an article.

    Args:
        xml_tree (lxml.etree._Element): XML tree of the article.
    """

    def __init__(self, xml_tree):
        # this is a list of dictionaries with abstract data
        self.abstracts = list(ArticleAbstract(xml_tree, selection="all").get_abstracts())

    def validate_abstracts_type(self, error_level="ERROR", expected_abstract_type_list=None):
        """
        Validates if the abstract types are within an expected list of types.

        Args:
            error_level (str): Error level to be reported. Default is "ERROR".
            expected_abstract_type_list (list, optional): List of expected abstract types.

        Yields:
            dict: Formatted validation responses for each abstract with unexpected type.
        """
        for abstract in self.abstracts:
            if abstract.get("abstract_type") not in (expected_abstract_type_list or []):
                yield format_response(
                    title="abstract-type attribute",
                    parent=abstract.get("parent"),
                    parent_id=abstract.get("parent_id"),
                    parent_article_type=abstract.get("parent_article_type"),
                    parent_lang=abstract.get("parent_lang"),
                    item="abstract",
                    sub_item='@abstract-type',
                    validation_type="value in list",
                    is_valid=False,
                    expected='<abstract abstract-type="key-points"> or <abstract abstract-type="graphical">',
                    obtained=f'<abstract abstract-type="{abstract.get("abstract_type")}">',
                    advice='Provide <abstract abstract-type="key-points"> or <abstract abstract-type="graphical">',
                    data=abstract,
                    error_level=error_level
                )
