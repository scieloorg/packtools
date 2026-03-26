"""
Validations for the <response> element according to SPS 1.10 specification.

This module implements validations for the <response> element, which identifies
a set of responses related to a letter or commentary, mandatorily published
alongside the letter/commentary.

Reference: https://docs.google.com/document/d/1GTv4Inc2LS_AXY-ToHT3HmO66UT0VAHWJNOIqzBNSgA/edit#heading=h.response
"""

from packtools.sps.validation.utils import build_response


XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"


class ResponseValidation:
    """
    Validates <response> elements according to SPS 1.10 rules.

    Validation rules:
    - Presence of @response-type attribute
    - Value of @response-type must be "reply"
    - Presence of @xml:lang attribute
    - Presence of @id attribute
    - Uniqueness of @id across all <response> elements
    - Presence of <front-stub> child element
    - Presence of <body> child element
    """

    def __init__(self, xmltree, params=None):
        self.xmltree = xmltree
        self.params = params or {}

    def _get_response_elements(self):
        """
        Yield context dicts for each <response> element found in the document.

        Searches for <response> elements as children of <article> and
        <sub-article>.
        """
        root = self.xmltree.find(".")
        if root is None:
            return

        for response_node in root.xpath(".//response"):
            parent_node = response_node.getparent()
            if parent_node is not None:
                parent_tag = parent_node.tag
                if parent_tag == "article":
                    parent_id = None
                    parent_article_type = parent_node.get("article-type")
                    parent_lang = parent_node.get(XML_LANG)
                elif parent_tag == "sub-article":
                    parent_id = parent_node.get("id")
                    parent_article_type = parent_node.get("article-type")
                    parent_lang = parent_node.get(XML_LANG)
                else:
                    parent_id = None
                    parent_article_type = None
                    parent_lang = None
            else:
                parent_tag = None
                parent_id = None
                parent_article_type = None
                parent_lang = None

            yield {
                "node": response_node,
                "parent": parent_tag,
                "parent_id": parent_id,
                "parent_article_type": parent_article_type,
                "parent_lang": parent_lang,
                "response_type": (response_node.get("response-type") or "").strip() or None,
                "xml_lang": (response_node.get(XML_LANG) or "").strip() or None,
                "id": (response_node.get("id") or "").strip() or None,
                "has_front_stub": response_node.find("front-stub") is not None,
                "has_body": response_node.find("body") is not None,
            }

    def _build_parent_info(self, ctx):
        return {
            "parent": ctx["parent"],
            "parent_id": ctx["parent_id"],
            "parent_article_type": ctx["parent_article_type"],
            "parent_lang": ctx["parent_lang"],
        }

    def validate(self):
        yield from self.validate_response_type_presence()
        yield from self.validate_response_type_value()
        yield from self.validate_xml_lang_presence()
        yield from self.validate_id_presence()
        yield from self.validate_id_uniqueness()
        yield from self.validate_front_stub_presence()
        yield from self.validate_body_presence()

    def validate_response_type_presence(self):
        """
        Rule 1: Validate that @response-type attribute is present in <response>.
        """
        error_level = self.params.get(
            "response_type_presence_error_level", "CRITICAL"
        )
        for ctx in self._get_response_elements():
            response_type = ctx["response_type"]
            is_valid = bool(response_type)
            yield build_response(
                title="response @response-type presence",
                parent=self._build_parent_info(ctx),
                item="response",
                sub_item="@response-type",
                validation_type="exist",
                is_valid=is_valid,
                expected="reply",
                obtained=response_type,
                advice='Add @response-type="reply" to <response>.',
                data=ctx.get("id"),
                error_level=error_level,
                element_name="response",
                attribute_name="response-type",
            )

    def validate_response_type_value(self):
        """
        Rule 2: Validate that @response-type value is "reply".
        """
        error_level = self.params.get(
            "response_type_value_error_level", "ERROR"
        )
        for ctx in self._get_response_elements():
            response_type = ctx["response_type"]
            if not response_type:
                continue
            is_valid = response_type == "reply"
            yield build_response(
                title="response @response-type value",
                parent=self._build_parent_info(ctx),
                item="response",
                sub_item="@response-type",
                validation_type="value",
                is_valid=is_valid,
                expected="reply",
                obtained=response_type,
                advice='Replace @response-type with "reply" in <response>.',
                data=ctx.get("id"),
                error_level=error_level,
                element_name="response",
                attribute_name="response-type",
            )

    def validate_xml_lang_presence(self):
        """
        Rule 3: Validate that @xml:lang attribute is present in <response>.
        """
        error_level = self.params.get(
            "xml_lang_presence_error_level", "CRITICAL"
        )
        for ctx in self._get_response_elements():
            xml_lang = ctx["xml_lang"]
            is_valid = bool(xml_lang)
            yield build_response(
                title="response @xml:lang presence",
                parent=self._build_parent_info(ctx),
                item="response",
                sub_item="@xml:lang",
                validation_type="exist",
                is_valid=is_valid,
                expected="a valid xml:lang value",
                obtained=xml_lang,
                advice="Add @xml:lang to <response>.",
                data=ctx.get("id"),
                error_level=error_level,
                element_name="response",
                attribute_name="xml:lang",
            )

    def validate_id_presence(self):
        """
        Rule 4: Validate that @id attribute is present in <response>.
        """
        error_level = self.params.get(
            "id_presence_error_level", "CRITICAL"
        )
        for ctx in self._get_response_elements():
            response_id = ctx["id"]
            is_valid = bool(response_id)
            yield build_response(
                title="response @id presence",
                parent=self._build_parent_info(ctx),
                item="response",
                sub_item="@id",
                validation_type="exist",
                is_valid=is_valid,
                expected="a unique id value",
                obtained=response_id,
                advice="Add @id to <response>.",
                data=ctx.get("id"),
                error_level=error_level,
                element_name="response",
                attribute_name="id",
            )

    def validate_id_uniqueness(self):
        """
        Rule 5: Validate that each <response> has a unique @id value.
        """
        error_level = self.params.get(
            "id_uniqueness_error_level", "ERROR"
        )
        seen_ids = {}
        contexts = list(self._get_response_elements())
        for ctx in contexts:
            response_id = ctx["id"]
            if not response_id:
                continue
            if response_id in seen_ids:
                seen_ids[response_id] += 1
            else:
                seen_ids[response_id] = 1

        duplicates = {k for k, v in seen_ids.items() if v > 1}
        if not duplicates:
            return

        for ctx in contexts:
            response_id = ctx["id"]
            if response_id not in duplicates:
                continue
            yield build_response(
                title="response @id uniqueness",
                parent=self._build_parent_info(ctx),
                item="response",
                sub_item="@id",
                validation_type="unique",
                is_valid=False,
                expected="a unique @id for each <response>",
                obtained=response_id,
                advice=f'Replace duplicate @id="{response_id}" with a unique value in <response>.',
                data=response_id,
                error_level=error_level,
                element_name="response",
                attribute_name="id",
            )

    def validate_front_stub_presence(self):
        """
        Rule 6: Validate that <front-stub> is present in <response>.
        """
        error_level = self.params.get(
            "front_stub_presence_error_level", "WARNING"
        )
        for ctx in self._get_response_elements():
            is_valid = ctx["has_front_stub"]
            yield build_response(
                title="response front-stub presence",
                parent=self._build_parent_info(ctx),
                item="response",
                sub_item="front-stub",
                validation_type="exist",
                is_valid=is_valid,
                expected="<front-stub> element",
                obtained="front-stub" if is_valid else None,
                advice="Add <front-stub> with response metadata inside <response>.",
                data=ctx.get("id"),
                error_level=error_level,
                element_name="response",
                sub_element_name="front-stub",
            )

    def validate_body_presence(self):
        """
        Rule 7: Validate that <body> is present in <response>.
        """
        error_level = self.params.get(
            "body_presence_error_level", "WARNING"
        )
        for ctx in self._get_response_elements():
            is_valid = ctx["has_body"]
            yield build_response(
                title="response body presence",
                parent=self._build_parent_info(ctx),
                item="response",
                sub_item="body",
                validation_type="exist",
                is_valid=is_valid,
                expected="<body> element",
                obtained="body" if is_valid else None,
                advice="Add <body> with response content inside <response>.",
                data=ctx.get("id"),
                error_level=error_level,
                element_name="response",
                sub_element_name="body",
            )
