from packtools.sps.models.article_citations import ArticleCitations
from packtools.sps.models.dates import ArticleDates
from packtools.sps.validation.exceptions import ValidationArticleCitationsException
from packtools.sps.validation.utils import format_response


class ArticleCitationValidation:
    def __init__(self, citation):
        self.citation = citation

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
        value = self.citation.get(item_name)
        element_name = element_name or item_name
        advice = advice or f"Identify the reference {element_name}"
        expected = expected or f"reference {element_name}"
        if not value or valid is False:
            yield format_response(
                title=f"reference {element_name}",
                parent=self.citation.get("parent"),
                parent_id=self.citation.get("parent_id"),
                parent_article_type=self.citation.get("parent_article_type"),
                parent_lang=self.citation.get("parent_lang"),
                item="element-citation",
                sub_item=element_name,
                is_valid=valid,
                validation_type=validation_type or "exist",
                expected=expected,
                obtained=value,
                advice=advice,
                data=self.citation,
                error_level=error_level,
            )

    def validate_year(self, end_year, error_level="ERROR"):
        """
        Checks whether the year in an article citation exists and is valid.

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'reference xxxx',
                    'parent': None,
                    'parent_id': None,
                    'item': 'element-citation',
                    'sub-item': 'year',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'a value for year between 2000 and 2020',
                    'got_value': '2015',
                    'message': 'Got 2015, expected a value for year between 2000 and 2020',
                    'advice': None,
                    'data': {
                        'all_authors': [
                            {'given-names': 'B', 'prefix': 'The Honorable', 'suffix': 'III', 'surname': 'Tran'},
                            {'given-names': 'MO', 'surname': 'Falster'},
                            {'given-names': 'K', 'surname': 'Douglas'},
                            {'given-names': 'F', 'surname': 'Blyth'},
                            {'given-names': 'LR', 'surname': 'Jorm'}
                        ],
                        'article_title': 'Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages',
                        'author_type': 'person',
                        'citation_ids': {
                            'doi': '10.1016/B1',
                            'pmcid': '11111111',
                            'pmid': '00000000'
                        },
                        'elocation_id': 'elocation_B1',
                        'fpage': '85',
                        'label': '1',
                        'lpage': '91',
                        'main_author': {'given-names': 'B', 'prefix': 'The Honorable', 'suffix': 'III', 'surname': 'Tran'},
                        'mixed_citation': '1. Tran B, Falster MO, Douglas K, Blyth F, Jorm '
                                          'LR. Smoking and potentially preventable '
                                          'hospitalisation: the benefit of smoking cessation '
                                          'in older ages. Drug Alcohol Depend. '
                                          '2015;150:85-91. DOI: '
                                          'https://doi.org/10.1016/j.drugalcdep.2015.02.028',
                        'publication_type': 'journal',
                        'ref_id': 'B1',
                        'source': 'Drug Alcohol Depend.',
                        'volume': '150',
                        'year': '2015'
                    }
                },...
            ]
        """
        if not end_year:
            raise ValueError("ArticleCitationValidation.validate_year requires valid value for end_year")
        year = self.citation.get("year")
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
                error_level=error_level,
            )

    def validate_source(self, error_level="ERROR"):
        """
        Checks whether the source in an article citation exists.

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'reference xxxx',
                    'parent': None,
                    'parent_id': None,
                    'item': 'element-citation',
                    'sub_item': 'source',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'Drug Alcohol Depend.',
                    'got_value': 'Drug Alcohol Depend.',
                    'message': 'Got Drug Alcohol Depend., expected Drug Alcohol Depend.',
                    'advice': None,
                    'data': {
                        'all_authors': [
                            {'given-names': 'B', 'prefix': 'The Honorable', 'suffix': 'III', 'surname': 'Tran'},
                            {'given-names': 'MO', 'surname': 'Falster'},
                            {'given-names': 'K', 'surname': 'Douglas'},
                            {'given-names': 'F', 'surname': 'Blyth'},
                            {'given-names': 'LR', 'surname': 'Jorm'}
                        ],
                        'article_title': 'Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages',
                        'author_type': 'person',
                        'citation_ids': {
                            'doi': '10.1016/B1',
                            'pmcid': '11111111',
                            'pmid': '00000000'
                        },
                        'elocation_id': 'elocation_B1',
                        'fpage': '85',
                        'label': '1',
                        'lpage': '91',
                        'main_author': {'given-names': 'B', 'prefix': 'The Honorable', 'suffix': 'III', 'surname': 'Tran'},
                        'mixed_citation': '1. Tran B, Falster MO, Douglas K, Blyth F, Jorm '
                                          'LR. Smoking and potentially preventable '
                                          'hospitalisation: the benefit of smoking cessation '
                                          'in older ages. Drug Alcohol Depend. '
                                          '2015;150:85-91. DOI: '
                                          'https://doi.org/10.1016/j.drugalcdep.2015.02.028',
                        'publication_type': 'journal',
                        'ref_id': 'B1',
                        'source': 'Drug Alcohol Depend.',
                        'volume': '150',
                        'year': '2015'
                    }
                },...
            ]
        """
        yield from self._validate_item("source", error_level=error_level)

    def validate_article_title(self, error_level="ERROR"):
        """
        Checks whether the article title in an article citation exists.

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'reference xxxx',
                    'parent': None,
                    'parent_id': None,
                    'item': 'element-citation',
                    'sub-item': 'article-title',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'Smoking and potentially preventable hospitalisation: the benefit of smoking '
                                      'cessation in older ages',
                    'got_value': 'Smoking and potentially preventable hospitalisation: the benefit of smoking cessation '
                                 'in older ages',
                    'message': 'Got Smoking and potentially preventable hospitalisation: the benefit of smoking cessation '
                               'in older ages, expected Smoking and potentially preventable hospitalisation: the benefit '
                               'of smoking cessation in older ages',
                    'advice': None,
                    'data': {
                        'all_authors': [
                            {'given-names': 'B', 'prefix': 'The Honorable', 'suffix': 'III', 'surname': 'Tran'},
                            {'given-names': 'MO', 'surname': 'Falster'},
                            {'given-names': 'K', 'surname': 'Douglas'},
                            {'given-names': 'F', 'surname': 'Blyth'},
                            {'given-names': 'LR', 'surname': 'Jorm'}
                        ],
                        'article_title': 'Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages',
                        'author_type': 'person',
                        'citation_ids': {
                            'doi': '10.1016/B1',
                            'pmcid': '11111111',
                            'pmid': '00000000'
                        },
                        'elocation_id': 'elocation_B1',
                        'fpage': '85',
                        'label': '1',
                        'lpage': '91',
                        'main_author': {'given-names': 'B', 'prefix': 'The Honorable', 'suffix': 'III', 'surname': 'Tran'},
                        'mixed_citation': '1. Tran B, Falster MO, Douglas K, Blyth F, Jorm '
                                          'LR. Smoking and potentially preventable '
                                          'hospitalisation: the benefit of smoking cessation '
                                          'in older ages. Drug Alcohol Depend. '
                                          '2015;150:85-91. DOI: '
                                          'https://doi.org/10.1016/j.drugalcdep.2015.02.028',
                        'publication_type': 'journal',
                        'ref_id': 'B1',
                        'source': 'Drug Alcohol Depend.',
                        'volume': '150',
                        'year': '2015'
                    }
                },...
            ]
        """
        publication_type = self.citation.get("publication_type")
        article_title = self.citation.get("article_title")
        if publication_type == "journal" and not article_title:
            yield from self._validate_item("article_title", "article-title", error_level=error_level)

    def validate_authors(self, error_level="ERROR"):
        """
        Checks if there are authors for the article citation.

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'reference xxxx',
                    'parent': None,
                    'parent_id': None,
                    'item': 'element-citation',
                    'sub-item': 'person-group//name or person-group//collab',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'at least 1 author in each element-citation',
                    'got_value': '5 authors',
                    'message': f'Got 5 authors, expected at least 1 author in each element-citation',
                    'advice': None,
                    'data': {
                        'all_authors': [
                            {'given-names': 'B', 'prefix': 'The Honorable', 'suffix': 'III', 'surname': 'Tran'},
                            {'given-names': 'MO', 'surname': 'Falster'},
                            {'given-names': 'K', 'surname': 'Douglas'},
                            {'given-names': 'F', 'surname': 'Blyth'},
                            {'given-names': 'LR', 'surname': 'Jorm'}
                        ],
                        'article_title': 'Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages',
                        'author_type': 'person',
                        'citation_ids': {
                            'doi': '10.1016/B1',
                            'pmcid': '11111111',
                            'pmid': '00000000'
                        },
                        'elocation_id': 'elocation_B1',
                        'fpage': '85',
                        'label': '1',
                        'lpage': '91',
                        'main_author': {'given-names': 'B', 'prefix': 'The Honorable', 'suffix': 'III', 'surname': 'Tran'},
                        'mixed_citation': '1. Tran B, Falster MO, Douglas K, Blyth F, Jorm '
                                          'LR. Smoking and potentially preventable '
                                          'hospitalisation: the benefit of smoking cessation '
                                          'in older ages. Drug Alcohol Depend. '
                                          '2015;150:85-91. DOI: '
                                          'https://doi.org/10.1016/j.drugalcdep.2015.02.028',
                        'publication_type': 'journal',
                        'ref_id': 'B1',
                        'source': 'Drug Alcohol Depend.',
                        'volume': '150',
                        'year': '2015'
                    }
                },...
            ]
        """
        number_authors = (
            len(self.citation.get("all_authors"))
            if self.citation.get("all_authors")
            else 0
        )
        if not number_authors:
            advice = "Identify the reference authors"
            yield from self._validate_item(
                "all_authors",
                element_name="person-group//name or person-group//collab",
                valid=number_authors,
                advice=advice,
                error_level=error_level,
            )

    def validate_publication_type(self, publication_type_list, error_level="ERROR"):
        """
        Checks if the publication type is present in the list of default values.

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'reference xxxx',
                    'parent': None,
                    'parent_id': None,
                    'item': 'element-citation',
                    'sub_item': 'publication-type',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': ['journal', 'book'],
                    'got_value': 'journal',
                    'message': "Got journal, expected ['journal', 'book']",
                    'advice': None,
                    'data': {
                        'all_authors': [
                            {'given-names': 'B', 'prefix': 'The Honorable', 'suffix': 'III', 'surname': 'Tran'},
                            {'given-names': 'MO', 'surname': 'Falster'},
                            {'given-names': 'K', 'surname': 'Douglas'},
                            {'given-names': 'F', 'surname': 'Blyth'},
                            {'given-names': 'LR', 'surname': 'Jorm'}
                        ],
                        'article_title': 'Smoking and potentially preventable hospitalisation: the benefit of smoking cessation in older ages',
                        'author_type': 'person',
                        'citation_ids': {
                            'doi': '10.1016/B1',
                            'pmcid': '11111111',
                            'pmid': '00000000'
                        },
                        'elocation_id': 'elocation_B1',
                        'fpage': '85',
                        'label': '1',
                        'lpage': '91',
                        'main_author': {'given-names': 'B', 'prefix': 'The Honorable', 'suffix': 'III', 'surname': 'Tran'},
                        'mixed_citation': '1. Tran B, Falster MO, Douglas K, Blyth F, Jorm '
                                          'LR. Smoking and potentially preventable '
                                          'hospitalisation: the benefit of smoking cessation '
                                          'in older ages. Drug Alcohol Depend. '
                                          '2015;150:85-91. DOI: '
                                          'https://doi.org/10.1016/j.drugalcdep.2015.02.028',
                        'publication_type': 'journal',
                        'ref_id': 'B1',
                        'source': 'Drug Alcohol Depend.',
                        'volume': '150',
                        'year': '2015'
                    }
                },...
            ]
        """
        if publication_type_list is None:
            raise ValidationArticleCitationsException(
                "Function requires list of publications type"
            )
        publication_type = self.citation.get("publication_type")
        if publication_type not in publication_type_list:
            advice = (
                f"Provide a value for @publication-type, one of {publication_type_list}"
            )
            yield from self._validate_item(
                "publication_type", element_name="@publication-type", advice=advice, error_level=error_level, expected=publication_type_list, validation_type="value in list"
            )

    def validate_comment_is_required_or_not(self, error_level="ERROR"):
        comment = self.citation.get("comment_text", {})
        text_before_extlink = self.citation.get("text_before_extlink")

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
                yield format_response(
                    title="comment is required or not",
                    parent=self.citation.get("parent"),
                    parent_id=self.citation.get("parent_id"),
                    parent_article_type=self.citation.get("parent_article_type"),
                    parent_lang=self.citation.get("parent_lang"),
                    item="element-citation",
                    sub_item="comment",
                    is_valid=False,
                    validation_type="exist",
                    expected=scenario["expected"],
                    obtained=scenario["obtained"],
                    advice=scenario["advice"],
                    data=self.citation,
                    error_level=error_level,
                )

    def validate_mixed_citation_tags(self, error_level="ERROR", allowed_tags=None):
        if allowed_tags is None:
            raise ValidationArticleCitationsException(
                "Function requires list of allowed tags"
            )
        remaining_tags = list(
            set(self.citation.get("mixed_citation_sub_tags")) - set(allowed_tags)
        )
        if remaining_tags:
            yield format_response(
                title="mixed citation sub-tags",
                parent=self.citation.get("parent"),
                parent_id=self.citation.get("parent_id"),
                parent_article_type=self.citation.get("parent_article_type"),
                parent_lang=self.citation.get("parent_lang"),
                item="element-citation",
                sub_item="mixed-citation",
                is_valid=False,
                validation_type="exist",
                expected=allowed_tags,
                obtained=self.citation.get("mixed_citation_sub_tags"),
                advice=f"remove {remaining_tags} from mixed-citation",
                data=self.citation,
                error_level=error_level,
            )


class ArticleCitationsValidation:
    def __init__(self, xml_tree, publication_type_list, allowed_tags=None):
        self.xml_tree = xml_tree
        self.article_citations = ArticleCitations(self.xml_tree).article_citations
        self.publication_type_list = publication_type_list
        self.allowed_tags = allowed_tags
        article_dates = ArticleDates(xml_tree)
        try:
            self.end_year = (
                int(
                    (article_dates.collection_date or article_dates.article_date)[
                        "year"
                    ]
                )
                + 1
            )
        except (ValueError, TypeError, AttributeError, KeyError):
            self.end_year = None

    def validate(
        self,
        year_error_level=None,
        source_error_level=None,
        article_title_error_level=None,
        authors_error_level=None,
        publication_type_error_level=None,
        comment_error_level=None,
        mixed_citation_error_level=None,
    ):
        for article_citation in self.article_citations:
            citation = ArticleCitationValidation(article_citation)
            yield from citation.validate_year(
                end_year=self.end_year,
                error_level=year_error_level,
            )
            yield from citation.validate_source(source_error_level)
            yield from citation.validate_publication_type(
                self.publication_type_list, publication_type_error_level
            )
            yield from citation.validate_article_title(article_title_error_level)
            yield from citation.validate_authors(authors_error_level)
            yield from citation.validate_comment_is_required_or_not(comment_error_level)

            if self.allowed_tags:
                yield from citation.validate_mixed_citation_tags(
                    allowed_tags=self.allowed_tags
                )
