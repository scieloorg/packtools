from packtools.sps.models.references import ArticleReferences
from packtools.sps.models.dates import ArticleDates
from packtools.sps.validation.exceptions import ValidationReferencesException
from packtools.sps.validation.utils import build_response


class ReferenceValidation:
    def __init__(self, reference_data, params):
        self.reference_data = reference_data
        self.params = params

    def _validate_item(
        self,
        item_name,
        element_name=None,
        valid=None,
        advice=None,
        expected=None,
        error_level=None,
        validation_type=None,
    ):
        value = self.reference_data.get(item_name)
        element_name = element_name or item_name
        advice = advice or f"Identify the reference {element_name}"
        expected = expected or f"reference {element_name}"

        yield build_response(
            title=f"reference {element_name}",
            parent=self.reference_data,
            item="element-citation",
            sub_item=element_name,
            is_valid=valid,
            validation_type=validation_type or "exist",
            expected=expected,
            obtained=value,
            advice=advice,
            data=self.reference_data,
            error_level=error_level,
        )

    def validate_year(self):
        end_year = self.params.get("end_year")
        if not end_year:
            raise ValueError("ReferenceValidation.validate_year requires valid value for end_year")
        year = self.reference_data.get("year")
        try:
            is_valid = int(year) <= end_year
        except (TypeError, ValueError):
            is_valid = False
        advice = f"Mark reference publication year with <ref-list><ref><element-citation><year>, ensure that year is previous or equal to {end_year}"
        expected = (
            year if is_valid else f"reference publication year, previous or equal to {end_year}"
        )

        yield from self._validate_item(
            "year",
            valid=is_valid,
            advice=advice,
            expected=expected,
            error_level=self.params["year_error_level"],
        )

    def validate_source(self):
        source = self.reference_data.get("source")
        is_valid = bool(source)
        advice = "Mark main source title of a reference with <ref-list><ref><element-citation><source>"
        expected = source if is_valid else "Main source title of a reference"

        yield from self._validate_item(
            "source",
            valid=is_valid,
            advice=advice,
            expected=expected,
            error_level=self.params["source_error_level"]
        )

    def validate_article_title(self):
        publication_type = self.reference_data.get("publication_type")
        article_title = self.reference_data.get("article_title")
        is_valid = publication_type != "journal" or bool(article_title)
        advice = f"A title is required for '{publication_type}'. Please add one."
        expected = article_title if is_valid else "Article title"

        yield from self._validate_item(
            "article_title",
            valid=is_valid,
            advice=advice,
            expected=expected,
            error_level=self.params["article_title_error_level"]
        )

    def validate_authors(self):
        number_authors = (
            len(self.reference_data.get("all_authors"))
            if self.reference_data.get("all_authors")
            else 0
        )
        is_valid = number_authors > 0
        advice = "The reference must include at least one author or collaboration group."
        expected = "At least one author or collaboration group."
        yield from self._validate_item(
            "all_authors",
            element_name="person-group//name or person-group//collab",
            valid=is_valid,
            advice=advice,
            error_level=self.params["authors_error_level"],
            expected=expected
        )

    def validate_publication_type(self):
        publication_type_list = self.params["publication_type_list"]
        error_level = self.params["publication_type_error_level"]
        if publication_type_list is None:
            raise ValidationReferencesException(
                "Function requires list of publications type"
            )
        publication_type = self.reference_data.get("publication_type")
        is_valid = publication_type in publication_type_list
        advice = (
            f'Specify a valid publication type in <element-citation publication-type="VALUE">. '
            f'Replace VALUE with one of: {publication_type_list}'
        )
        yield from self._validate_item(
            "publication_type",
            element_name="@publication-type",
            advice=advice,
            error_level=error_level,
            expected=publication_type_list,
            validation_type="value in list",
            valid=is_valid,
        )

    def validate_comment_is_required_or_not(self):
        comment = self.reference_data.get("comment_text") or {}
        text_before_extlink = self.reference_data.get("text_before_extlink")
        ext_link_text = comment.get("ext_link_text")
        full_comment = comment.get("full_comment")
        text_between = comment.get("text_between")
        has_comment = comment.get("has_comment")

        parent_tag = "element-citation"

        scenarios = [
            {
                "condition": has_comment and not full_comment and text_before_extlink,
                "expected": f"<comment>{text_before_extlink}<ext-link>{ext_link_text}</ext-link></comment>",
                "obtained": f"<comment></comment>{text_before_extlink}<ext-link>{ext_link_text}</ext-link>",
                "advice": f"Inside <{parent_tag}>, wrap the <ext-link> tag and its content within the <comment> tag.",
            },
            {
                "condition": has_comment and not full_comment and not text_before_extlink,
                "expected": f"<ext-link>{ext_link_text}</ext-link>",
                "obtained": f"<comment></comment><ext-link>{ext_link_text}</ext-link>",
                "advice": f"Inside <{parent_tag}>, remove the empty <comment> tag to clean up the structure.",
            },
            {
                "condition": not has_comment and text_before_extlink,
                "expected": f"<comment>{text_before_extlink}<ext-link>{ext_link_text}</ext-link></comment>",
                "obtained": f"{text_before_extlink}<ext-link>{ext_link_text}</ext-link>",
                "advice": f"Inside <{parent_tag}>, wrap the <ext-link> tag and its content within the <comment> tag.",
            },
            {
                "condition": full_comment and not text_between,
                "expected": f"<ext-link>{ext_link_text}</ext-link>",
                "obtained": f"<comment><ext-link>{ext_link_text}</ext-link></comment>",
                "advice": f"Inside <{parent_tag}>, remove the <comment> tag if it has no additional content.",
            },
        ]

        found_issue = False
        for scenario in scenarios:
            if scenario["condition"]:
                found_issue = True
                yield build_response(
                    title="comment is required or not",
                    parent=self.reference_data,
                    item="element-citation",
                    sub_item="comment",
                    is_valid=False,
                    validation_type="exist",
                    expected=scenario["expected"],
                    obtained=scenario["obtained"],
                    advice=scenario["advice"],
                    data=self.reference_data,
                    error_level=self.params["comment_error_level"],
                )

        if not found_issue:
            yield build_response(
                title="comment is required or not",
                parent=self.reference_data,
                item="element-citation",
                sub_item="comment",
                is_valid=True,
                validation_type="exist",
                expected="Valid structure",
                obtained="Valid structure",
                advice=None,
                data=self.reference_data,
                error_level="INFO",
            )

    def validate_mixed_citation_sub_tags(self):
        allowed_tags = self.params["allowed_tags"]
        if found_sub_tags := self.reference_data.get("mixed_citation_sub_tags"):
            remaining_tags = list(set(found_sub_tags) - set(allowed_tags))
            is_valid = not bool(remaining_tags)
            yield build_response(
                title="mixed-citation sub elements",
                parent=self.reference_data,
                item="mixed-citation",
                sub_item=None,
                is_valid=is_valid,
                validation_type="exist",
                expected=allowed_tags,
                obtained=self.reference_data.get("mixed_citation_sub_tags"),
                advice=f"Remove the following invalid sub-tags from <mixed-citation>: {remaining_tags}.",
                data=self.reference_data,
                error_level=self.params["mixed_citation_sub_tags_error_level"],
            )

    def validate_mixed_citation(self):
        mixed_citation = self.reference_data.get("mixed_citation")
        is_valid = bool(mixed_citation)
        if not mixed_citation:
            advice = f"Add <mixed-citation> inside <element-citation>."
        elif isinstance(mixed_citation, str) and not mixed_citation.strip():
            advice = f"<mixed-citation> inside <element-citation> should not be empty."
        else:
            advice = None
        yield build_response(
            title="mixed-citation",
            parent=self.reference_data,
            item="mixed-citation",
            sub_item=None,
            is_valid=is_valid,
            validation_type="exist",
            expected="mixed-citation",
            obtained=mixed_citation,
            advice=advice,
            data=self.reference_data,
            error_level=self.params["mixed_citation_error_level"],
        )

    def validate_title_tag_by_dtd_version(self):
        chapter_title = self.reference_data.get("chapter_title")
        dtd_version = self.params.get("dtd_version")
        if dtd_version is None:
            raise ValueError("DTD version is missing.")
        try:
            dtd_version = float(dtd_version)
        except ValueError:
            raise ValueError(f"Invalid DTD version: '{dtd_version}' is not a numeric value.")

        if dtd_version >= 1.3 and bool(chapter_title):
            advice = f"Use <part-title> instead of <chapter-title> in <element-citation> for compatibility with DTD {dtd_version}."
            yield build_response(
                title="part-title",
                parent=self.reference_data,
                item="element-citation",
                sub_item="part-title",
                is_valid=False,
                validation_type="exist",
                expected="<part-title>",
                obtained="<chapter-title>",
                advice=advice,
                data=self.reference_data,
                error_level=self.params.get("title_tag_by_dtd_version_error_level"),
            )

    def validate(self):
        yield from self.validate_year()
        yield from self.validate_source()
        yield from self.validate_publication_type()
        yield from self.validate_article_title()
        yield from self.validate_authors()
        yield from self.validate_comment_is_required_or_not()
        yield from self.validate_mixed_citation_sub_tags()
        yield from self.validate_mixed_citation()
        yield from self.validate_title_tag_by_dtd_version()


class ReferencesValidation:
    def __init__(self, xml_tree, params):
        self.xml_tree = xml_tree
        self.params = params

    def validate(self):
        xml_article_references = ArticleReferences(self.xml_tree)

        for reference_data in xml_article_references.article_references:
            validator = ReferenceValidation(reference_data, self.params)
            yield from validator.validate()

        for reference_data in xml_article_references.sub_article_references:
            validator = ReferenceValidation(reference_data, self.params)
            yield from validator.validate()
