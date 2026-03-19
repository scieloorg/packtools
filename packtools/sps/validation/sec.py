from packtools.sps.models.sec import ArticleSecs
from packtools.sps.validation.utils import build_response


class SecValidation:
    """Validates a single <sec> element."""

    def __init__(self, data, params):
        self.data = data
        self.params = params

    def validate(self):
        yield self.validate_title()
        result = self.validate_sec_type_value()
        if result:
            yield result
        result = self.validate_transcript_id()
        if result:
            yield result
        result = self.validate_combined_format()
        if result:
            yield result
        result = self.validate_non_combinable()
        if result:
            yield result
        yield self.validate_content()

    def validate_title(self):
        """Rule 1: <title> is mandatory in <sec> for accessibility."""
        has_title = self.data.get("has_title")
        return build_response(
            title="sec title",
            parent=self.data,
            item="sec",
            sub_item="title",
            validation_type="exist",
            is_valid=has_title,
            expected="<title> element in <sec>",
            obtained=self.data.get("title"),
            advice="Add <title> element to <sec> for accessibility",
            data=self.data,
            error_level=self.params.get("title_error_level", "CRITICAL"),
        )

    def validate_sec_type_value(self):
        """Rule 2: When present, @sec-type must have a valid value."""
        sec_type = self.data.get("sec_type")
        if not sec_type:
            return None

        valid_sec_types = self.params.get("valid_sec_types", [])
        # Handle combined types (e.g. "materials|methods")
        parts = sec_type.split("|")
        is_valid = all(part in valid_sec_types for part in parts)

        return build_response(
            title="sec type value",
            parent=self.data,
            item="sec",
            sub_item="@sec-type",
            validation_type="value in list",
            is_valid=is_valid,
            expected=str(valid_sec_types),
            obtained=sec_type,
            advice=f'Replace @sec-type="{sec_type}" with a valid value: {valid_sec_types}',
            data=self.data,
            error_level=self.params.get("sec_type_value_error_level", "ERROR"),
        )

    def validate_transcript_id(self):
        """Rule 3: <sec sec-type="transcript"> must have @id."""
        sec_type = self.data.get("sec_type")
        if sec_type != "transcript":
            return None

        sec_id = self.data.get("sec_id")
        is_valid = bool(sec_id)

        return build_response(
            title="transcript id",
            parent=self.data,
            item="sec",
            sub_item="@id",
            validation_type="exist",
            is_valid=is_valid,
            expected='@id attribute in <sec sec-type="transcript">',
            obtained=sec_id,
            advice='Add @id attribute to <sec sec-type="transcript">',
            data=self.data,
            error_level=self.params.get("transcript_id_error_level", "ERROR"),
        )

    def validate_combined_format(self):
        """Rule 5: Combined sec-types must use pipe separator."""
        sec_type = self.data.get("sec_type")
        if not sec_type:
            return None

        # Only check if it looks like a combined type (contains separator chars)
        # If it contains spaces or commas but not pipes, it's incorrectly formatted
        has_space_separator = " " in sec_type and "|" not in sec_type
        has_comma_separator = "," in sec_type and "|" not in sec_type

        if not has_space_separator and not has_comma_separator:
            return None

        return build_response(
            title="sec type combined format",
            parent=self.data,
            item="sec",
            sub_item="@sec-type",
            validation_type="format",
            is_valid=False,
            expected='Combined sec-types separated by pipe "|" (e.g., "materials|methods")',
            obtained=sec_type,
            advice=f'Use pipe "|" as separator in @sec-type="{sec_type}" (e.g., "materials|methods")',
            data=self.data,
            error_level=self.params.get("combined_format_error_level", "WARNING"),
        )

    def validate_non_combinable(self):
        """Rule 6: transcript, supplementary-material, and data-availability cannot be combined."""
        sec_type = self.data.get("sec_type")
        if not sec_type or "|" not in sec_type:
            return None

        non_combinable = self.params.get(
            "non_combinable_sec_types",
            ["data-availability", "supplementary-material", "transcript"],
        )
        parts = sec_type.split("|")

        found_non_combinable = [p for p in parts if p in non_combinable]
        if not found_non_combinable:
            return None

        return build_response(
            title="sec type non-combinable",
            parent=self.data,
            item="sec",
            sub_item="@sec-type",
            validation_type="format",
            is_valid=False,
            expected=f"Types {non_combinable} must not be combined with other types",
            obtained=sec_type,
            advice=f'Do not combine "{found_non_combinable[0]}" with other types in @sec-type="{sec_type}"',
            data=self.data,
            error_level=self.params.get("non_combinable_error_level", "WARNING"),
        )

    def validate_content(self):
        """Rule 7: <sec> should contain at least one <p> after <title>."""
        paragraph_count = self.data.get("paragraph_count", 0)
        is_valid = paragraph_count > 0

        return build_response(
            title="sec content",
            parent=self.data,
            item="sec",
            sub_item="p",
            validation_type="exist",
            is_valid=is_valid,
            expected="At least one <p> element in <sec>",
            obtained=f"{paragraph_count} paragraphs",
            advice="Add at least one <p> element to <sec>",
            data=self.data,
            error_level=self.params.get("content_error_level", "WARNING"),
        )


class XMLSecValidation:
    """Validates all <sec> elements in the XML document."""

    def __init__(self, xmltree, params):
        self.xmltree = xmltree
        self.params = params
        self.article_secs = ArticleSecs(xmltree)

    def validate(self):
        yield from self.validate_secs()
        yield from self.validate_data_availability_presence()

    def validate_secs(self):
        """Validate each <sec> element individually."""
        for sec_data in self.article_secs.all_secs:
            validator = SecValidation(sec_data, self.params)
            yield from validator.validate()

    def validate_data_availability_presence(self):
        """Rule 4: Certain article types require a data-availability section."""
        required_types = self.params.get(
            "data_availability_required_article_types",
            [
                "data-article",
                "brief-report",
                "case-report",
                "rapid-communication",
                "research-article",
                "review-article",
            ],
        )

        article_type = self.article_secs.main_article_type
        if not article_type or article_type not in required_types:
            return

        body_sec_types = self.article_secs.body_sec_types
        has_data_availability = "data-availability" in body_sec_types

        parent = {
            "parent": "article",
            "parent_id": None,
            "parent_article_type": article_type,
            "parent_lang": self.xmltree.find(".").get(
                "{http://www.w3.org/XML/1998/namespace}lang"
            ),
        }

        yield build_response(
            title="data availability section",
            parent=parent,
            item="sec",
            sub_item='@sec-type="data-availability"',
            validation_type="exist",
            is_valid=has_data_availability,
            expected='<sec sec-type="data-availability"> in <body>',
            obtained=(
                '<sec sec-type="data-availability">'
                if has_data_availability
                else "missing"
            ),
            advice=(
                f'Add <sec sec-type="data-availability" specific-use="..."> to <body> '
                f'(required for article-type="{article_type}")'
            ),
            data=parent,
            error_level=self.params.get("data_availability_error_level", "ERROR"),
        )
