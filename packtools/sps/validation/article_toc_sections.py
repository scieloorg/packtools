from packtools.sps.models.v2.article_toc_sections import ArticleTocSections
from packtools.sps.validation.utils import format_response, build_response
from packtools.sps.validation.similarity_utils import how_similar


class XMLTocSectionsValidation:
    def __init__(self, xmltree, params=None):
        """
        Initialize the XMLTocSectionsValidation class with parameters.

        Args:
            xmltree: XML tree object
            params (dict): Dictionary containing validation parameters
                {
                    'expected_toc_sections': dict with expected TOC sections,
                    'subj_group_type_error_level': str for TOC validation error level,
                    'error_level_title': str for title validation error level,
                    'error_level_section': str for section validation error level
                }
        """
        self.params = params or {}
        self.xml_toc_sections = ArticleTocSections(xmltree)

    def validate(self):
        """
        Check whether the TOC sections match the options provided in a standard list.

        Returns
        -------
        generator of dict
            A generator that yields dictionaries with validation results.
        """
        for lang, subjects in self.xml_toc_sections.sections_by_lang.items():
            for i, subject in enumerate(subjects):

                validator = SubjectValidation(subject, self.params)
                
                if i > 0:
                    # cada idioma deve ter somente 1 subject-group (heading)
                    # mas por engano, pode haver mais, valida o excedente
                    yield validator.validate_unexpected_item()
                    continue

                yield validator.validate_subj_group_type()
                yield validator.validate_subsection()
                yield validator.validate_section()
                yield validator.validade_article_title_is_different_from_section_title()


class SubjectValidation:

    def __init__(self, data, params):
        self.data = data
        self.lang = data["parent_lang"]

        self.params = {}
        self.params.update(params)

        # Set default values from params or use class defaults
        self.expected_toc_sections = (
            self.params.get("toc_sections")
            or (self.params.get("journal_data") or {}).get("toc_sections")
            or {}
        )
        self.subj_group_type_error_level = self.params.get(
            "subj_group_type_error_level", "CRITICAL"
        )
        self.subsection_error_level = self.params.get(
            "subsection_error_level", "CRITICAL"
        )
        self.value_error_level = self.params.get("value_error_level", "CRITICAL")
        self.article_title_and_toc_section_are_similar_error_level = self.params.get(
            "article_title_and_toc_section_are_similar_error_level", "ERROR"
        )
        self.params.setdefault("article_title_and_toc_section_max_similarity", 0.7)
        self.params.setdefault("unexpected_subj_group_error_level", "CRITICAL")

    def validate_unexpected_item(self):
        subj_group_type = self.data.get("subj_group_type")
        subject = self.data.get("subject") or ""
        subsections = self.data.get("subsections")
        section_title = self.data.get("section") or ""
        article_title = self.data.get("article_title") or ""

        valid = False
        # Há seções excedentes (heading)
        if subj_group_type:
            advice = f'Remove <subject-group subj-group-type="heading"><subject>{subject}</subject></subject-group> because it is unexpected, only one subject-group is acceptable'
        else:
            advice = f'Remove <subject-group><subject>{subject}</subject></subject-group> because it is unexpected, only one subject-group is acceptable'
        return build_response(
            title="unexpected subject-group",
            parent=self.data,
            item="subj-group",
            sub_item="@subj-group-type",
            is_valid=valid,
            validation_type="match",
            expected=None,
            obtained=self.data,
            advice=advice,
            data=self.data,
            error_level=self.params["unexpected_subj_group_error_level"],
        )

    def validate_subj_group_type(self):
        subj_group_type = self.data.get("subj_group_type")
        subject = self.data.get("subject") or ""
        subsections = self.data.get("subsections")
        section_title = self.data.get("section") or ""
        article_title = self.data.get("article_title") or ""

        valid = subj_group_type == "heading"
        if subj_group_type and subject:
            advice = f'Replace <subject-group subj-group-type="{subj_group_type}"><subject>{subject}</subject></subject-group> by <subject-group subj-group-type="heading"><subject>{subject}</subject></subject-group>'
        elif subject:
            advice = f'Replace <subject-group><subject>{subject}</subject></subject-group> by <subject-group subj-group-type="heading"><subject>{subject}</subject></subject-group>'
        else:
            advice = f'Mark table of contents section with  <subject-group subj-group-type="heading"><subject>table of contents section</subject></subject-group>'
        return build_response(
            title="table of contents section",
            parent=self.data,
            item="subj-group",
            sub_item="@subj-group-type",
            is_valid=valid,
            validation_type="match",
            expected="heading",
            obtained=subj_group_type,
            advice=advice,
            data=self.data,
            error_level=self.subj_group_type_error_level,
        )

    def validate_subsection(self):
        subj_group_type = self.data.get("subj_group_type")
        subject = self.data.get("subject") or ""
        subsections = self.data.get("subsections")
        section_title = self.data.get("section") or ""
        article_title = self.data.get("article_title") or ""
        subsection_text = " ".join(subsections or "")

        # Há a recomendação de marcar a subseção junto com a seção 'seção: subseção'
        # É desincentivado a usar subject-group/subject-group
        valid = not subsections
        advice = f'Write section and subsection in one subject: <subject-group subj-group-type="heading"><subject>{subject}: {subsection_text}</subject></subject-group>. Remove <subject-group><subject>{subsection_text}</subject></subject-group>'
        return build_response(
            title="table of contents section with subsection",
            parent=self.data,
            item="subj-group",
            sub_item="@subj-group-type",
            is_valid=valid,
            validation_type="match",
            expected=[],
            obtained=subsections,
            advice=advice,
            data=self.data,
            error_level=self.subsection_error_level,
        )

    def validate_section(self):
        subj_group_type = self.data.get("subj_group_type")
        subject = self.data.get("subject") or ""
        subsections = self.data.get("subsections")
        section_title = self.data.get("section") or ""
        article_title = self.data.get("article_title") or ""
        subsection_text = " ".join(subsections or "")
        journal = self.data.get("journal") or ""

        if subsection_text:
            subject = f"{section_title}: {subsection_text}"

        valid = False
        expected = "table of contents section"
        if subject:
            validation_type = "value in list"
            expected_toc_sections = self.expected_toc_sections.get(self.lang) or []
            expected = expected_toc_sections or self.expected_toc_sections

            if self.expected_toc_sections:
                valid = (
                    expected_toc_sections and subject in expected_toc_sections
                )
                expected_items = (
                    expected_toc_sections or self.expected_toc_sections
                )
                advice = f"{subject} is not registered as a table of contents section. Valid values: {self.expected_toc_sections}"
            else:
                advice = f'Unable to check if {subject} (<subject-group subj-group-type="heading"><subject>{subject}</subject></subject-group>) is a valid table of contents section because the journal ({journal}) sections were not informed'
        else:
            validation_type = "exist"
            advice = 'Mark table of contents section with <subject-group subj-group-type="heading"><subject></subject></subject-group>'

        return build_response(
            title="table of contents section",
            parent=self.data,
            item="subj-group",
            sub_item="subject",
            is_valid=valid,
            validation_type=validation_type,
            expected=expected,
            obtained=subject,
            advice=advice,
            data=self.data,
            error_level=self.value_error_level,
        )

    def validade_article_title_is_different_from_section_title(self):
        subj_group_type = self.data.get("subj_group_type")
        subject = self.data.get("subject") or ""
        subsections = self.data.get("subsections")
        section_title = self.data.get("section") or ""
        article_title = self.data.get("article_title") or ""
        subsection_text = " ".join(subsections or "")

        score = how_similar(article_title, section_title)
        valid = (
            article_title and section_title and
            score
            < self.params["article_title_and_toc_section_max_similarity"]
        )
        data = {}
        data["lang"] = self.lang
        data["article-title"] = article_title
        data["section_title"] = section_title

        msg = f"The article title ({article_title}) must represent its contents and must be different from the section title ({section_title}) to get a better ranking in search results"
        return build_response(
            title="document title must be meaningful",
            parent=self.data,
            item="subj-group",
            sub_item="subject",
            is_valid=valid,
            validation_type="match",
            expected=msg,
            obtained=article_title,
            advice=msg,
            data=data,
            error_level=self.article_title_and_toc_section_are_similar_error_level,
        )
