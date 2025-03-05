from packtools.sps.models.references import XMLReferences
from packtools.sps.models.dates import ArticleDates
from packtools.sps.validation.exceptions import ValidationReferencesException
from packtools.sps.validation.utils import build_response, get_future_date


class ReferenceValidation:
    def __init__(self, reference_data, params):
        self.data = reference_data
        self.params = self.get_default_params()
        self.params.update(params or {})
        self.publication_type_list = list(self.params["publication_type_requires"].keys())
        self.requires = self.params["publication_type_requires"].get(self.publication_type) or ["source", "year"]

    @property
    def info(self):
        ref = self.data.get("ref_id") or self.data.get("mixed_citation") or self.data
        return f'{ref} ({self.publication_type})'

    @property
    def publication_type(self):
        return self.data.get("publication_type")

    def get_default_params(self):
        return {
            # Error levels for different validations
            "year_error_level": "ERROR",
            "source_error_level": "ERROR",
            "article_title_error_level": "ERROR",
            "authors_error_level": "ERROR",
            "publication_type_error_level": "ERROR",
            "comment_error_level": "ERROR",
            "mixed_citation_sub_tags_error_level": "ERROR",
            "mixed_citation_error_level": "ERROR",
            "title_tag_by_dtd_version_error_level": "ERROR",

            # Allowed tags in mixed citations
            "allowed_tags": [
                "bold",
                "italic",
                "sup",
                "sub",
                "ext-link",
                # "named-content"
            ],
            
            "dtd_version": "1.1"  # Default DTD version
        }

    def _validate_item(
        self,
        label,
        item_name,
        element_name=None,
        valid=None,
        advice=None,
        expected=None,
        error_level=None,
        validation_type=None,
    ):
        value = self.data.get(item_name)
        element_name = element_name or item_name
        advice = advice or f"Mark {label} with <{element_name}>"
        expected = expected or f"reference {element_name}"

        advice = f'{self.info} : {advice}'

        if valid is None:
            valid = bool(value)
        yield build_response(
            title=f"reference {element_name}",
            parent=self.data,
            item="element-citation",
            sub_item=element_name,
            is_valid=valid,
            validation_type=validation_type or "exist",
            expected=expected,
            obtained=value,
            advice=advice,
            data=self.data,
            error_level=error_level,
        )

    def validate_year(self):
        # data do artigo que cita a referência
        end_year = self.data["citing_pub_year"]
        if not end_year:
            raise ValueError("ReferenceValidation.validate_year requires valid value for end_year")
        year = self.data.get("year")
        try:
            is_valid = int(year) <= int(end_year)
        except (TypeError, ValueError):
            is_valid = False

        if year:
            advice = (
                f"Mark the reference year ({year}) with <year> and it must be previous or equal to {end_year}"
            )
            expected = f"reference year ({year}) previous or equal to {end_year}"
        else:
            advice = (
                f"Mark the reference year with <year> and it must be previous or equal to {end_year}"
            )
            expected = f"reference year previous or equal to {end_year}"
        yield from self._validate_item(
            "reference year",
            "year",
            valid=is_valid,
            advice=advice,
            expected=expected,
            error_level=self.params["year_error_level"],
            validation_type="format"
        )

    def validate_source(self):
        if "source" in self.requires:
            yield from self._validate_item(
                "reference source",
                "source", error_level=self.params["source_error_level"])

    def validate_article_title(self):
        if "article-title" in self.requires:
            article_title = self.data.get("article_title")
            yield from self._validate_item(
                "article title",
                "article_title", "article-title", error_level=self.params["article_title_error_level"])

    def validate_authors(self):
        if "person-group" in self.requires:
            number_authors = (
                len(self.data.get("all_authors"))
                if self.data.get("all_authors")
                else 0
            )
            valid = number_authors > 0
            yield from self._validate_item(
                "reference authors",
                "all_authors",
                element_name="person-group//name or person-group//collab",
                valid=valid,
                advice=f'Mark reference authors with <name> (person) or <collab> (institutional)',
                error_level=self.params["authors_error_level"],
            )

    def validate_publication_type(self):
        publication_type_list = self.publication_type_list
        error_level = self.params["publication_type_error_level"]
        if publication_type_list is None:
            raise ValidationReferencesException(
                "Function requires list of publications type"
            )
        publication_type = self.publication_type
        valid = publication_type in publication_type_list
        advice = (
            f'Complete publication-type="" in <element-citation publication-type=""> with valid value: {publication_type_list}'
        )
        yield from self._validate_item(
            "reference type",
            "publication_type", advice=advice,
            valid=valid,
            error_level=error_level, expected=publication_type_list, validation_type="value in list"
        )

    def validate_comment_is_required_or_not(self):
        text_before_extlink = self.data.get("text_before_extlink")

        ext_link_uri = self.data.get("ext_link_uri")
        ext_link_text = self.data.get("ext_link_text")
        full_comment = self.data.get("full_comment")
        text_between = self.data.get("text_between")
        has_comment = self.data.get("has_comment")

        ext_link_xml = f'<ext-link xlink:href="{ext_link_uri}">{ext_link_text}</ext-link>'
        ext_link_tag_with_attrib = f'<ext-link xlink:href="{ext_link_uri}">'

        scenarios = [
            {
                "condition": has_comment and not full_comment and text_before_extlink,
                "expected": f"<comment>{text_before_extlink}{ext_link_xml}</comment>",
                "obtained": f"<comment></comment>{text_before_extlink}{ext_link_xml}",
                "advice": f"Wrap {text_before_extlink}{ext_link_xml} with <comment> tag",
            },
            {
                "condition": has_comment
                and not full_comment
                and not text_before_extlink,
                "expected": ext_link_xml,
                "obtained": f"<comment></comment>{ext_link_xml}",
                "advice": f"Analyze and decide to remove <comment> or mark the text between <comment> and {ext_link_tag_with_attrib}",
            },
            {
                "condition": not has_comment and text_before_extlink,
                "expected": f"<comment>{text_before_extlink}{ext_link_xml}</comment>",
                "obtained": f"{text_before_extlink}{ext_link_xml}",
                "advice": f"Wrap the {text_before_extlink}{ext_link_xml} with <comment> tag",
            },
            {
                "condition": full_comment and not text_between,
                "expected": ext_link_xml,
                "obtained": f"<comment>{ext_link_xml}</comment>",
                "advice": f"Analyze and decide to remove <comment> or mark the text between <comment> and {ext_link_tag_with_attrib}",
            },
        ]

        for scenario in scenarios:
            advice = scenario["advice"]
            advice = f'{self.info} : {advice}'

            if scenario["condition"]:
                yield build_response(
                    title="comment is required or not",
                    parent=self.data,
                    item="element-citation",
                    sub_item="comment",
                    is_valid=False,
                    validation_type="exist",
                    expected=scenario["expected"],
                    obtained=scenario["obtained"],
                    advice=advice,
                    data=self.data,
                    error_level=self.params["comment_error_level"],
                )

    def validate_mixed_citation_sub_tags(self):
        allowed_tags = self.params["allowed_tags"]
        if found_sub_tags := self.data.get("mixed_citation_sub_tags"):
            remaining_tags = list(set(found_sub_tags) - set(allowed_tags))
            if remaining_tags:
                yield build_response(
                    title="mixed-citation sub elements",
                    parent=self.data,
                    item="mixed-citation",
                    sub_item=None,
                    is_valid=False,
                    validation_type="exist",
                    expected=allowed_tags,
                    obtained=self.data.get("mixed_citation_sub_tags"),
                    advice=f"remove {remaining_tags} from mixed-citation",
                    data=self.data,
                    error_level=self.params["mixed_citation_sub_tags_error_level"],
                )

    def validate_mixed_citation(self):
        valid = self.data.get("mixed_citation")
        advice = f"{self.info}: mark the full reference with <mixed-citation>"
        yield build_response(
            title="mixed-citation",
            parent=self.data,
            item="mixed-citation",
            sub_item=None,
            is_valid=valid,
            validation_type="exist",
            expected="mixed-citation",
            obtained=None,
            advice=advice,
            data=self.data,
            error_level=self.params["mixed_citation_error_level"],
        )

    def validate_title_tag_by_dtd_version(self):
        chapter_title = self.data.get("chapter_title")
        try:
            dtd_version = float(self.params.get("dtd_version"))
        except ValueError:
            raise ValueError("Invalid DTD version: expected a numeric value.")

        if dtd_version >= 1.3 and bool(chapter_title):
            yield build_response(
                title="part-title",
                parent=self.data,
                item="element-citation",
                sub_item="part-title",
                is_valid=False,
                validation_type="exist",
                expected="<part-title>",
                obtained="<chapter-title>",
                advice=f'{self.info} : replace <chapter-title> by <part-title>',
                data=self.data,
                error_level=self.params.get("title_tag_by_dtd_version_error_level"),
            )

    def validate_unmatched_marks(self):
        # {"not_marked": not_marked, "marked": marked, "unmatched": unmatched}
        is_valid = not self.data["unmatched"]
        for item in self.data["unmatched"]:
            yield build_response(
                title="element-citation versus mixed-citation",
                parent=self.data,
                item="element-citation",
                sub_item=None,
                is_valid=False,
                validation_type="match",
                expected=None,
                obtained=item,
                advice=f'{self.info} : {item.get("text")} ({item.get("tag")}) not found in <mixed-citation>{self.data.get("mixed_citation")}</mixed-citation>',
                data=self.data,
                error_level=self.params.get("unmatched_data_error_level"),
            )

    def validate_not_marked(self):
        # {"not_marked": not_marked, "marked": marked, "unmatched": unmatched}
        is_valid = not self.data["filtered_not_marked"]
        for item in self.data["filtered_not_marked"]:
            yield build_response(
                title="element-citation versus mixed-citation",
                parent=self.data,
                item="element-citation",
                sub_item=None,
                is_valid=False,
                validation_type="match",
                expected=None,
                obtained=item,
                advice=f'{self.info} : "{item}" was not marked, analyze it and mark it with a corresponding tag',
                data=self.data,
                error_level=self.params.get("not_marked_data_error_level"),
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
        yield from self.validate_not_marked()
        # yield from self.validate_unmatched_marks()


class ReferencesValidation:
    def __init__(self, xml_tree, params):
        self.xml_tree = xml_tree
        self.params = params

    def validate(self):
        xml_references = XMLReferences(self.xml_tree)

        for reference_data in xml_references.items:
            validator = ReferenceValidation(reference_data, self.params)
            yield from validator.validate()
