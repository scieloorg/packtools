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
        if not value or valid is False:
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
        advice = (
            None
            if is_valid
            else f"Identify the reference year, previous or equal to {end_year}"
        )
        expected = (
            year if is_valid else f"reference year, previous or equal to {end_year}"
        )
        if not is_valid:
            yield from self._validate_item(
                "year",
                valid=is_valid,
                advice=advice,
                expected=expected,
                error_level=self.params["year_error_level"],
            )

    def validate_source(self):
        yield from self._validate_item("source", error_level=self.params["source_error_level"])

    def validate_article_title(self):
        publication_type = self.reference_data.get("publication_type")
        article_title = self.reference_data.get("article_title")
        if publication_type == "journal" and not article_title:
            yield from self._validate_item(
                "article_title", "article-title", error_level=self.params["article_title_error_level"])

    def validate_authors(self):
        number_authors = (
            len(self.reference_data.get("all_authors"))
            if self.reference_data.get("all_authors")
            else 0
        )
        if not number_authors:
            advice = "Identify the reference authors"
            yield from self._validate_item(
                "all_authors",
                element_name="person-group//name or person-group//collab",
                valid=number_authors,
                advice=advice,
                error_level=self.params["authors_error_level"],
            )

    def validate_publication_type(self):
        publication_type_list = self.params["publication_type_list"]
        error_level = self.params["publication_type_error_level"]
        if publication_type_list is None:
            raise ValidationReferencesException(
                "Function requires list of publications type"
            )
        publication_type = self.reference_data.get("publication_type")
        if publication_type not in publication_type_list:
            advice = (
                f"Provide a value for @publication-type, one of {publication_type_list}"
            )
            yield from self._validate_item(
                "publication_type", element_name="@publication-type", advice=advice,
                error_level=error_level, expected=publication_type_list, validation_type="value in list"
            )

    def validate_comment_is_required_or_not(self):
        comment = self.reference_data.get("comment_text", {})
        text_before_extlink = self.reference_data.get("text_before_extlink")

        ext_link_text = comment.get("ext_link_text")
        full_comment = comment.get("full_comment")
        text_between = comment.get("text_between")
        has_comment = comment.get("has_comment")

        scenarios = [
            {
                "condition": has_comment and not full_comment and text_before_extlink,
                "expected": f"<comment>{text_before_extlink}<ext-link>{ext_link_text}</ext-link></comment>",
                "obtained": f"<comment></comment>{text_before_extlink}<ext-link>{ext_link_text}</ext-link>",
                "advice": "Wrap the <ext-link> tag and its content within the <comment> tag",
            },
            {
                "condition": has_comment
                and not full_comment
                and not text_before_extlink,
                "expected": f"<ext-link>{ext_link_text}</ext-link>",
                "obtained": f"<comment></comment><ext-link>{ext_link_text}</ext-link>",
                "advice": "Remove the <comment> tag that has no content",
            },
            {
                "condition": not has_comment and text_before_extlink,
                "expected": f"<comment>{text_before_extlink}<ext-link>{ext_link_text}</ext-link></comment>",
                "obtained": f"{text_before_extlink}<ext-link>{ext_link_text}</ext-link>",
                "advice": "Wrap the <ext-link> tag and its content within the <comment> tag",
            },
            {
                "condition": full_comment and not text_between,
                "expected": f"<ext-link>{ext_link_text}</ext-link>",
                "obtained": f"<comment><ext-link>{ext_link_text}</ext-link></comment>",
                "advice": "Remove the <comment> tag that has no content",
            },
        ]

        for scenario in scenarios:
            if scenario["condition"]:
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

    def validate_mixed_citation_sub_tags(self):
        allowed_tags = self.params["allowed_tags"]
        if found_sub_tags := self.reference_data.get("mixed_citation_sub_tags"):
            remaining_tags = list(set(found_sub_tags) - set(allowed_tags))
            if remaining_tags:
                yield build_response(
                    title="mixed-citation sub elements",
                    parent=self.reference_data,
                    item="mixed-citation",
                    sub_item=None,
                    is_valid=False,
                    validation_type="exist",
                    expected=allowed_tags,
                    obtained=self.reference_data.get("mixed_citation_sub_tags"),
                    advice=f"remove {remaining_tags} from mixed-citation",
                    data=self.reference_data,
                    error_level=self.params["mixed_citation_sub_tags_error_level"],
                )

    def validate_mixed_citation(self):
        if not self.reference_data.get("mixed_citation"):
            yield build_response(
                title="mixed-citation",
                parent=self.reference_data,
                item="mixed-citation",
                sub_item=None,
                is_valid=False,
                validation_type="exist",
                expected="mixed-citation",
                obtained=None,
                advice=f"Add mixed-citation",
                data=self.reference_data,
                error_level=self.params["mixed_citation_error_level"],
            )

    def validate(self):
        yield from self.validate_year()
        yield from self.validate_source()
        yield from self.validate_publication_type()
        yield from self.validate_article_title()
        yield from self.validate_authors()
        yield from self.validate_comment_is_required_or_not()
        yield from self.validate_mixed_citation_sub_tags()


class ReferencesValidation:
    def __init__(self, xml_tree, params):
        self.xml_tree = xml_tree
        self.end_year = xml_tree
        self.params = params
        self.params["end_year"] = self.end_year

    @property
    def end_year(self):
        return self._end_year

    @end_year.setter
    def end_year(self, value):
        article_dates = ArticleDates(value)
        try:
            self._end_year = (
                int(
                    (article_dates.collection_date or article_dates.article_date)[
                        "year"
                    ]
                )
                + 1
            )
        except (ValueError, TypeError, AttributeError, KeyError):
            self._end_year = None

    def validate(self):
        xml_article_references = ArticleReferences(self.xml_tree)

        for reference_data in xml_article_references.article_references:
            validator = ReferenceValidation(reference_data, self.params)
            yield from validator.validate()

        for reference_data in xml_article_references.sub_article_references:
            validator = ReferenceValidation(reference_data, self.params)
            yield from validator.validate()