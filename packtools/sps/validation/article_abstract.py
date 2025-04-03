from packtools.sps.models.v2.abstract import XMLAbstracts
from packtools.sps.validation.utils import format_response, build_response


class AbstractValidation:
    """
    Base class for validating article abstracts.

    Args:
        abstract (dict): A dictionary containing the abstract information to be validated.
    """

    def __init__(self, abstract, params=None):
        # this is a dictionary with abstract data
        self.abstract = abstract
        self.params = self.get_default_params()
        self.params.update(params or {})

    def get_default_params(self):
        return {
            "default_error_level": "ERROR",
            "kwd_error_level": "ERROR",
            "title_error_level": "ERROR",
            "abstract_type_error_level": "CRITICAL",
            "abstract_presence_error_level": "WARNING",
            "article_type_requires_abstract_error_level": "CRITICAL",
            "article_type_unexpects_abstract_error_level": "CRITICAL",
            "abstract_type_list": [
                "key-points",
                "graphical",
                "summary",
                None
            ],
            "article_type_requires": [
                "case-report",
                "research-article",
                "review-article"
            ],
            "article_type_unexpects": [
                "addendum",
                "article-commentary",
                "book-review",
                "brief-report",
                "correction",
                "discussion",
                "editorial",
                "letter",
                "obituary",
                "partial-retraction",
                "rapid-communication",
                "reply",
                "retraction",
                "other"            
            ],
            "article_type_neutral": [
                "clinical-instruction",
                "data-article",
                "oration",
                "product-review",
                "reviewer-report"
            ]
        }

    def _format_response(
        self,
        title,
        sub_item,
        is_valid,
        validation_type,
        expected=None,
        obtained=None,
        advice=None,
        error_level="WARNING",
    ):
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
        return build_response(
            title=title,
            parent=self.abstract,
            item='abstract',
            sub_item=self.abstract.get("abstract_type"),
            validation_type=validation_type,
            is_valid=is_valid,
            expected=expected,
            obtained=obtained,
            advice=advice,
            data=self.abstract,
            error_level=error_level,
        )

    def validate(self):
        yield self.validate_abstract_type()
        yield self.validate_title()

        abstract_type = self.abstract.get("abstract_type")
        if abstract_type is None:
            yield self.validate_kwd()
        elif abstract_type == "key-points":
            yield self.validate_p()
            yield self.validate_list()
        elif abstract_type == "summary":
            yield self.validate_p()
        elif abstract_type == "graphical":
            yield self.validate_graphic()

    def validate_abstract_type(self):
        expected_abstract_type_list = self.params["abstract_type_list"]
        abstract_type = self.abstract.get("abstract_type")
        xml = self.abstract.get("xml")
        if abstract_type:
            advice = f'Replace {abstract_type} in {xml} by a valid value: {expected_abstract_type_list}'
        else:
            advice = f'Add abstract type in {xml}. Valid values: {expected_abstract_type_list}'
        is_valid = abstract_type in (expected_abstract_type_list or [])
        return build_response(
            title="@abstract-type",
            parent=self.abstract,
            item="abstract",
            sub_item="@abstract-type",
            validation_type="value in list",
            is_valid=is_valid,
            expected=expected_abstract_type_list,
            obtained=abstract_type,
            advice=advice,
            data=self.abstract,
            error_level=self.params["abstract_type_error_level"],
        )

    def validate_graphic(self):
        """
        Validates if the abstract contains a <graphic> tag.

        Returns:
            dict: Formatted validation response if the <graphic> tag is missing.
        """
        error_level = self.params.get("graphic_error_level", self.params["default_error_level"])
        graphic = self.abstract.get("graphic")
        return self._format_response(
            title="graphic",
            sub_item="graphic",
            validation_type="exist",
            is_valid=bool(graphic),
            expected="graphic",
            advice='Mark graphic in <abstract abstract-type="graphical">',
            error_level=error_level,
        )

    def validate_kwd(self):
        error_level = self.params.get("kwd_error_level", self.params["default_error_level"])
        if not self.abstract.get("abstract_type"):
            is_valid = bool(self.abstract.get("kwds"))
            lang = self.abstract.get("lang")
            return self._format_response(
                title="kwd",
                sub_item="kwd",
                is_valid=is_valid,
                validation_type="exist",
                obtained=self.abstract.get("kwds"),
                advice=f"Add keywords ({lang})",
                error_level=self.params["kwd_error_level"],
            )

    def validate_title(self):
        """
        Validates if the abstract contains a title.

        Returns:
            dict: Formatted validation response if the title is missing.
        """
        error_level = self.params.get("title_error_level", self.params["default_error_level"])
        title = self.abstract.get("title")
        return self._format_response(
            title="title",
            sub_item="title",
            validation_type="exist",
            is_valid=bool(title),
            expected="title",
            advice="Mark abstract title with <title> in <abstract>",
            error_level=self.params["title_error_level"],
        )

    def validate_list(self):
        """
        Validates if <list> tag is present in the abstract and suggests replacing it with <p>.

        Returns:
            dict: Formatted validation response if <list> tag is found.
        """
        error_level = self.params.get("list_error_level", self.params["default_error_level"])
        is_valid = not self.abstract.get("list")
        return self._format_response(
            title="list",
            sub_item="list",
            validation_type="exist",
            is_valid=is_valid,
            obtained=self.abstract.get("list"),
            advice='Replace <list> inside <abstract abstract-type="key-points"> by <p>',
            error_level=error_level,
        )

    def validate_p(self):
        """
        Validates if the abstract contains more than one <p> tag.

        Returns:
            dict: Formatted validation response if less than two <p> tags are found.
        """
        error_level = self.params.get("p_error_level", self.params["default_error_level"])
        is_valid = len(self.abstract.get("p") or []) <= 1
        return self._format_response(
            title="p",
            sub_item="p",
            validation_type="exist",
            is_valid=is_valid,
            expected="p",
            obtained=self.abstract.get("highlights"),
            advice='Mark each key-point with <p> in <abstract abstract-type="key-points">',
            error_level=error_level,
        )


class AbstractsValidationBase:
    def __init__(self, xml_tree, abstracts, params=None):
        self.xml_tree = xml_tree
        self.article_type = xml_tree.find(".").get("article-type")
        self.lang = xml_tree.get("{http://www.w3.org/XML/1998/namespace}lang")
        self.params = self.get_default_params()
        self.params.update(params or {})
        self.abstracts = list(abstracts or [])

    def get_default_params(self):
        return {
            "default_error_level": "ERROR",
            "kwd_error_level": "ERROR",
            "title_error_level": "ERROR",
            "abstract_type_error_level": "CRITICAL",
            "abstract_presence_error_level": "WARNING",
            "article_type_requires_abstract_error_level": "CRITICAL",
            "article_type_unexpects_abstract_error_level": "CRITICAL",
            "abstract_type_list": [
                "key-points",
                "graphical",
                "summary",
                None
            ],
            "article_type_requires": [
                "case-report",
                "research-article",
                "review-article"
            ],
            "article_type_unexpects": [
                "addendum",
                "article-commentary",
                "book-review",
                "brief-report",
                "correction",
                "discussion",
                "editorial",
                "letter",
                "obituary",
                "partial-retraction",
                "rapid-communication",
                "reply",
                "retraction",
                "other"            
            ],
            "article_type_neutral": [
                "clinical-instruction",
                "data-article",
                "oration",
                "product-review",
                "reviewer-report"
            ]
        }

    def validate(self):
        for item in self.abstracts:
            validator = AbstractValidation(item)
            yield from validator.validate()
        

class StandardAbstractsValidation(AbstractsValidationBase):

    def validate_exists(self):
        data = self.abstracts
        error_level = self.params["default_error_level"]
        is_valid = True
        advice = None

        if self.article_type in self.params["article_type_requires"]:
            expected = f"Abstract is required"
            is_valid = bool(data)
            error_level = self.params["article_type_requires_abstract_error_level"]
            advice = f"Mark abstract which is required for {self.article_type}"
        elif self.article_type in self.params["article_type_unexpects"]:
            expected = f"Abstract is unexpected"
            is_valid = not bool(data)
            error_level = self.params["article_type_unexpects_abstract_error_level"]
            advice = f"Abstract is not expected for {self.article_type}"
        elif self.article_type in self.params["article_type_neutral"]:
            is_valid = True
            expected = f"Abstract is optional"
            advice = None
        else:
            raise ValueError(
                f"Unable to identify if abstract is required or unexpected or neutral or acceptable"
            )
        return format_response(
            title="abstract",
            parent="article",
            parent_id=None,
            parent_article_type=self.article_type,
            parent_lang=self.lang,
            item="abstract",
            sub_item=None,
            validation_type="exist",
            is_valid=is_valid,
            expected=expected,
            obtained=data,
            advice=advice,
            data=data,
            error_level=error_level,
        )

    def validate(self):
        yield from super().validate()
        yield self.validate_exists()


class XMLAbstractsValidation:
    def __init__(self, xmltree, params=None):
        self.xmltree = xmltree
        self.article_type = xmltree.find(".").get("article-type")
        self.lang = xmltree.get("{http://www.w3.org/XML/1998/namespace}lang")
        self.params = self.get_default_params()
        self.params.update(params or {})
        self.xml_abstracts = XMLAbstracts(xmltree)

    def get_default_params(self):
        return {
            "default_error_level": "ERROR",
            "kwd_error_level": "ERROR",
            "title_error_level": "ERROR",
            "abstract_type_error_level": "CRITICAL",
            "abstract_presence_error_level": "WARNING",
            "article_type_requires_abstract_error_level": "CRITICAL",
            "article_type_unexpects_abstract_error_level": "CRITICAL",
            "abstract_type_list": [
                "key-points",
                "graphical",
                "summary",
                None
            ],
            "article_type_requires": [
                "case-report",
                "research-article",
                "review-article"
            ],
            "article_type_unexpects": [
                "addendum",
                "article-commentary",
                "book-review",
                "brief-report",
                "correction",
                "discussion",
                "editorial",
                "letter",
                "obituary",
                "partial-retraction",
                "rapid-communication",
                "reply",
                "retraction",
                "other"            
            ],
            "article_type_neutral": [
                "clinical-instruction",
                "data-article",
                "oration",
                "product-review",
                "reviewer-report"
            ]
        }

    def validate(self):
        validator = StandardAbstractsValidation(
            self.xmltree, self.xml_abstracts.standard_abstracts, self.params["abstract_rules"]
        )
        yield from validator.validate()

        validator = AbstractsValidationBase(
            self.xmltree, self.xml_abstracts.key_points_abstracts, self.params["highlight_rules"]
        )
        yield from validator.validate()
        
        validator = AbstractsValidationBase(
            self.xmltree, self.xml_abstracts.visual_abstracts, self.params["graphical_abstract_rules"]
        )
        yield from validator.validate()
        
        validator = AbstractsValidationBase(
            self.xmltree, self.xml_abstracts.summary_abstracts, self.params["abstract_rules"]
        )
        yield from validator.validate()
