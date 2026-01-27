from packtools.sps.models.v2.abstract import XMLAbstracts
from packtools.sps.validation.utils import format_response, build_response
import gettext

# Configuração de internacionalização
_ = gettext.gettext


class AbstractValidation:
    """
    Validates article abstracts according to SPS 1.10 rules.

    SPS 1.10 Rules:
    - Simple/structured abstracts (no @abstract-type): REQUIRE <kwd-group> sibling
    - graphical, key-points, summary: PROHIBIT <kwd-group> sibling
    - key-points: REQUIRE multiple <p> tags
    - key-points: PROHIBIT <list> tags
    - graphical: REQUIRE <graphic> element
    - All types: REQUIRE <title>

    Args:
        abstract (dict): A dictionary containing the abstract information to be validated.
        params (dict, optional): Validation parameters. Defaults to None.
    """

    def __init__(self, abstract, params=None):
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
        advice_text=None,
        advice_params=None,
    ):
        """
        Formats the validation response with i18n support.

        Args:
            title (str): The title of the validation issue.
            sub_item (str): The sub-item being validated.
            is_valid (bool): Whether the validation passed or failed.
            validation_type (str): The type of validation.
            expected (str, optional): The expected value.
            obtained (str, optional): The obtained value.
            advice (str, optional): Advice on how to resolve the issue.
            error_level (str): The error level. Default is 'WARNING'.
            advice_text (str, optional): i18n template for advice.
            advice_params (dict, optional): Parameters for i18n template.

        Returns:
            dict: A formatted validation response.
        """
        return build_response(
            title=title,
            parent=self.abstract,
            item='abstract',
            sub_item=sub_item,
            validation_type=validation_type,
            is_valid=is_valid,
            expected=expected,
            obtained=obtained,
            advice=advice,
            data=self.abstract,
            error_level=error_level,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate(self):
        """
        Main validation method that orchestrates all validations.

        Yields validation responses for:
        - Abstract type validity
        - Title presence
        - Keywords presence/absence (depending on type)
        - Type-specific validations (p, list, graphic)
        """
        result = self.validate_abstract_type()
        if result:
            yield result

        result = self.validate_title()
        if result:
            yield result

        abstract_type = self.abstract.get("abstract_type")

        if abstract_type is None:
            # Simple or structured abstract - keywords are REQUIRED
            result = self.validate_kwd_required()
            if result:
                yield result
        else:
            # Special types - keywords are PROHIBITED
            result = self.validate_kwd_not_allowed()
            if result:
                yield result

            if abstract_type == "key-points":
                result = self.validate_p_multiple()
                if result:
                    yield result
                result = self.validate_list()
                if result:
                    yield result
            elif abstract_type == "graphical":
                result = self.validate_graphic()
                if result:
                    yield result
            # summary doesn't need additional validations

    def validate_abstract_type(self):
        """
        Validates that @abstract-type has a valid value.

        Valid values: 'key-points', 'graphical', 'summary', or None (for simple/structured)

        Returns:
            dict: Validation response
        """
        expected_abstract_type_list = self.params["abstract_type_list"]
        abstract_type = self.abstract.get("abstract_type")
        xml = self.abstract.get("xml")

        if abstract_type:
            advice = f'Replace {abstract_type} in {xml} by a valid value: {expected_abstract_type_list}'
            advice_text = _('Replace {value} in {element} by a valid value: {valid_values}')
            advice_params = {
                "value": abstract_type,
                "element": xml,
                "valid_values": str(expected_abstract_type_list)
            }
        else:
            advice = f'Add abstract type in {xml}. Valid values: {expected_abstract_type_list}'
            advice_text = _('Add abstract type in {element}. Valid values: {valid_values}')
            advice_params = {
                "element": xml,
                "valid_values": str(expected_abstract_type_list)
            }

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
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_graphic(self):
        """
        Validates that graphical abstract contains a <graphic> tag.

        SPS 1.10: Visual Abstract must have an image representation.

        Returns:
            dict: Validation response
        """
        error_level = self.params.get("graphic_error_level", self.params["default_error_level"])
        graphic = self.abstract.get("graphic_href")

        if isinstance(graphic, str):
            has_graphic = bool(graphic.strip())
        else:
            has_graphic = bool(graphic)

        return self._format_response(
            title="graphic",
            sub_item="graphic",
            validation_type="exist",
            is_valid=has_graphic,
            expected="graphic",
            obtained=graphic,
            advice='Mark graphic in <abstract abstract-type="graphical">',
            advice_text=_('Mark {element} in {container}'),
            advice_params={
                "element": "graphic",
                "container": '<abstract abstract-type="graphical">'
            },
            error_level=error_level,
        )

    def validate_kwd_required(self):
        """
        Validates that simple/structured abstracts HAVE keywords.

        SPS 1.10: "Resumos <abstract> e <trans-abstract>, simples e estruturado,
        exigem palavras-chave <kwd-group>"

        Keywords must be siblings of <abstract> with matching @xml:lang.

        Returns:
            dict: Validation response
        """
        error_level = self.params.get("kwd_error_level", self.params["default_error_level"])
        kwds = self.abstract.get("kwds")
        is_valid = bool(kwds)
        lang = self.abstract.get("lang")
        xml = self.abstract.get("xml")

        return self._format_response(
            title="kwd",
            sub_item="kwd",
            is_valid=is_valid,
            validation_type="exist",
            expected=f"<kwd-group xml:lang='{lang}'>",
            obtained=kwds,
            advice=f'Add <kwd-group xml:lang="{lang}"> as sibling of {xml}',
            advice_text=_('Add {element} as sibling of {container}'),
            advice_params={
                "element": f'<kwd-group xml:lang="{lang}">',
                "container": xml
            },
            error_level=error_level,
        )

    def validate_kwd_not_allowed(self):
        """
        Validates that special abstract types DO NOT have keywords.

        SPS 1.10: "Resumos <abstract> graphical, key-points e summary,
        não permitem palavras-chave <kwd-group>."

        Even though keywords are siblings, they shouldn't be associated
        (matching xml:lang) with these special types.

        Returns:
            dict: Validation response
        """
        abstract_type = self.abstract.get("abstract_type")

        if abstract_type in ["graphical", "key-points", "summary"]:
            error_level = self.params.get("kwd_error_level", self.params["default_error_level"])
            kwds = self.abstract.get("kwds")
            has_kwds = bool(kwds)
            lang = self.abstract.get("lang")
            xml = self.abstract.get("xml")

            return self._format_response(
                title="unexpected kwd",
                sub_item="kwd",
                is_valid=not has_kwds,
                validation_type="exist",
                expected=None,
                obtained=kwds,
                advice=f'Remove <kwd-group xml:lang="{lang}"> which is associated with {xml} by language',
                advice_text=_('Remove {element} which is associated with {container} by language'),
                advice_params={
                    "element": f'<kwd-group xml:lang="{lang}">',
                    "container": xml
                },
                error_level=error_level,
            )

    def validate_title(self):
        """
        Validates that abstract contains a title.

        SPS 1.10: All abstract types require a <title>.

        Returns:
            dict: Validation response
        """
        error_level = self.params.get("title_error_level", self.params["default_error_level"])
        title = self.abstract.get("title")

        # Title comes as dict with 'plain_text' and 'html_text' from model
        # Check if title exists and has content
        has_title = False
        if title:
            if isinstance(title, dict):
                plain_text = title.get("plain_text", "").strip()
                has_title = bool(plain_text)
            elif isinstance(title, str):
                has_title = bool(title.strip())
            else:
                has_title = bool(title)

        return self._format_response(
            title="title",
            sub_item="title",
            validation_type="exist",
            is_valid=has_title,
            expected="title",
            obtained=title,
            advice="Mark abstract title with <title> in <abstract>",
            advice_text=_("Mark abstract title with {element} in {container}"),
            advice_params={
                "element": "<title>",
                "container": "<abstract>"
            },
            error_level=error_level,
        )

    def validate_list(self):
        """
        Validates that <list> tag is NOT present in key-points abstract.

        SPS 1.10: "Não usar <list> + <list-item> para o tipo <abstract abstract-type="key-points">"
        Use <p> tags instead.

        Returns:
            dict: Validation response
        """
        error_level = self.params.get("list_error_level", self.params["default_error_level"])
        list_items = self.abstract.get("list_items")
        is_valid = not bool(list_items)

        return self._format_response(
            title="list",
            sub_item="list",
            validation_type="exist",
            is_valid=is_valid,
            expected=None,
            obtained=list_items,
            advice='Replace <list> inside <abstract abstract-type="key-points"> by <p>',
            advice_text=_('Replace {wrong_element} inside {container} by {correct_element}'),
            advice_params={
                "wrong_element": "<list>",
                "container": '<abstract abstract-type="key-points">',
                "correct_element": "<p>"
            },
            error_level=error_level,
        )

    def validate_p_multiple(self):
        """
        Validates that key-points abstract contains more than one <p> tag.

        SPS 1.10: "key-points: Destaques do Documento (Highlights) -
        Palavras que transmitem os resultados principais do documento."

        Each highlight should be in a separate <p> tag.

        Returns:
            dict: Validation response
        """
        error_level = self.params.get("p_error_level", self.params["default_error_level"])
        p_list = self.abstract.get("p") or []
        # FIXED: Was <= 1, should be > 1 for multiple paragraphs
        is_valid = len(p_list) > 1

        return self._format_response(
            title="p",
            sub_item="p",
            validation_type="exist",
            is_valid=is_valid,
            expected="more than one p",
            obtained=p_list,
            advice='Provide more than one <p> in <abstract abstract-type="key-points">',
            advice_text=_('Provide more than one {element} in {container}'),
            advice_params={
                "element": "<p>",
                "container": '<abstract abstract-type="key-points">'
            },
            error_level=error_level,
        )


class AbstractsValidationBase:
    """
    Base class for validating multiple abstracts.

    Args:
        xml_tree: The XML tree containing abstracts
        abstracts: Iterator of abstract data dictionaries
        params: Validation parameters
    """

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
        """
        Validates all abstracts in the collection.

        Yields:
            dict: Validation responses for each abstract
        """
        for item in self.abstracts:
            validator = AbstractValidation(item, self.params)
            yield from validator.validate()


class StandardAbstractsValidation(AbstractsValidationBase):
    """
    Validates standard (simple/structured) abstracts with existence rules.
    """

    def validate_exists(self):
        """
        Validates whether standard abstracts should exist based on article type.

        SPS 1.10 rules:
        - Required for: case-report, research-article, review-article
        - Unexpected for: addendum, article-commentary, book-review, etc.
        - Optional for: clinical-instruction, data-article, etc.

        Returns:
            dict: Validation response
        """
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
                f"Unable to identify if abstract is required or unexpected or neutral for article-type '{self.article_type}'"
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
        """
        Validates standard abstracts including existence check.

        Yields:
            dict: Validation responses
        """
        yield from super().validate()
        yield self.validate_exists()


class XMLAbstractsValidation:
    """
    Main validation class that orchestrates validation of all abstract types.

    Args:
        xmltree: The XML tree to validate
        params: Validation parameters (optional)
    """

    def __init__(self, xmltree, params=None):
        self.xmltree = xmltree
        self.article_type = xmltree.find(".").get("article-type")
        self.lang = xmltree.get("{http://www.w3.org/XML/1998/namespace}lang")
        self.params = self.get_default_params()
        self.params.update(params or {})
        self.xml_abstracts = XMLAbstracts(xmltree)

    def get_default_params(self):
        return {
            "abstract_rules": {
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
            },
            "highlight_rules": {
                "default_error_level": "ERROR",
                "p_error_level": "ERROR",
                "list_error_level": "ERROR",
                "kwd_error_level": "ERROR",
            },
            "graphical_abstract_rules": {
                "default_error_level": "ERROR",
                "graphic_error_level": "ERROR",
                "kwd_error_level": "ERROR",
            },
            "summary_rules": {
                "default_error_level": "ERROR",
                "kwd_error_level": "ERROR",
            }
        }

    def validate(self):
        """
        Main validation method that validates all abstract types.

        Validates:
        - Standard abstracts (simple/structured)
        - Highlights (key-points)
        - Visual abstracts (graphical)
        - In Brief (summary)

        Yields:
            dict: Validation responses for all abstracts
        """
        # Validate standard abstracts
        validator = StandardAbstractsValidation(
            self.xmltree,
            self.xml_abstracts.standard_abstracts,
            self.params.get("abstract_rules", {})
        )
        yield from validator.validate()

        # Validate highlights
        validator = AbstractsValidationBase(
            self.xmltree,
            self.xml_abstracts.key_points_abstracts,
            self.params.get("highlight_rules", {})
        )
        yield from validator.validate()
        
        # Validate visual abstracts
        validator = AbstractsValidationBase(
            self.xmltree,
            self.xml_abstracts.visual_abstracts,
            self.params.get("graphical_abstract_rules", {})
        )
        yield from validator.validate()
        
        # Validate summary abstracts
        validator = AbstractsValidationBase(
            self.xmltree,
            self.xml_abstracts.summary_abstracts,
            self.params.get("summary_rules", {})
        )
        yield from validator.validate()
