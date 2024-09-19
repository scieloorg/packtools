from packtools.sps.models.article_citations import ArticleCitations
from packtools.sps.models.dates import ArticleDates
from packtools.sps.validation.exceptions import ValidationArticleCitationsException
from packtools.sps.validation.utils import format_response


class ArticleCitationValidation:
    def __init__(self, xmltree, citation, publication_type_list=None):
        self.xmltree = xmltree
        self.citation = citation
        self.publication_type_list = publication_type_list

    def validate_article_citation_year(
        self, start_year=None, end_year=None, error_level="ERROR"
    ):
        """
        Checks whether the year in an article citation exists and is valid.

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'element citation validation',
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
        if start_year is None:
            start_year = 0
        if end_year is None:
            try:
                end_year = int(ArticleDates(self.xmltree).collection_date["year"])
            except (KeyError, TypeError, ValueError):
                end_year = int(ArticleDates(self.xmltree).article_date["year"])
        year = self.citation.get("year")
        try:
            is_valid = start_year < int(year) <= end_year
        except (TypeError, ValueError):
            is_valid = False
        yield format_response(
            title="element citation validation",
            parent=self.citation.get("parent"),
            parent_id=self.citation.get("parent_id"),
            parent_article_type=self.citation.get("parent_article_type"),
            parent_lang=self.citation.get("parent_lang"),
            item="element-citation",
            sub_item="year",
            is_valid=is_valid,
            validation_type="exist",
            expected=f"a value for year between {start_year} and {end_year}",
            obtained=year,
            advice=f"The year in reference (ref-id: {self.citation.get('ref_id')}) is missing or is invalid, "
            f"provide a valid value for year",
            data=self.citation,
            error_level=error_level,
        )

    def validate_article_citation_source(self, error_level="ERROR"):
        """
        Checks whether the source in an article citation exists.

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'element citation validation',
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
        source = self.citation.get("source")
        is_valid = source is not None
        yield format_response(
            title="element citation validation",
            parent=self.citation.get("parent"),
            parent_id=self.citation.get("parent_id"),
            parent_article_type=self.citation.get("parent_article_type"),
            parent_lang=self.citation.get("parent_lang"),
            item="element-citation",
            sub_item="source",
            is_valid=is_valid,
            validation_type="exist",
            expected=source if is_valid else "a valid value to source",
            obtained=source,
            advice=f"The source in reference (ref-id: {self.citation.get('ref_id')}) is missing "
            f"provide a valid value to source",
            data=self.citation,
            error_level=error_level,
        )

    def validate_article_citation_article_title(self, error_level="ERROR"):
        """
        Checks whether the article title in an article citation exists.

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'element citation validation',
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
        if publication_type == "journal":
            article_title = self.citation.get("article_title")
            is_valid = article_title is not None
            yield format_response(
                title="element citation validation",
                parent=self.citation.get("parent"),
                parent_id=self.citation.get("parent_id"),
                parent_article_type=self.citation.get("parent_article_type"),
                parent_lang=self.citation.get("parent_lang"),
                item="element-citation",
                sub_item="article-title",
                is_valid=is_valid,
                validation_type="exist",
                expected=(
                    article_title if is_valid else "a valid value for article-title"
                ),
                obtained=article_title,
                advice=f"The article-title in reference (ref-id: {self.citation.get('ref_id')}) is missing "
                f"provide a valid value for article-title",
                data=self.citation,
                error_level=error_level,
            )

    def validate_article_citation_authors(self, error_level="ERROR"):
        """
        Checks if there are authors for the article citation.

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'element citation validation',
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
        is_valid = number_authors > 0
        yield format_response(
            title="element citation validation",
            parent=self.citation.get("parent"),
            parent_id=self.citation.get("parent_id"),
            parent_article_type=self.citation.get("parent_article_type"),
            parent_lang=self.citation.get("parent_lang"),
            item="element-citation",
            sub_item="person-group//name or person-group//collab",
            is_valid=is_valid,
            validation_type="exist",
            expected="at least 1 author in each element-citation",
            obtained=f"{number_authors} authors",
            advice=f"There are no authors for the reference (ref-id: {self.citation.get('ref_id')}) "
            f"provide at least 1 author",
            data=self.citation,
            error_level=error_level,
        )

    def validate_article_citation_publication_type(
        self, publication_type_list=None, error_level="ERROR"
    ):
        """
        Checks if the publication type is present in the list of default values.

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'element citation validation',
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
        publication_type_list = publication_type_list or self.publication_type_list
        if publication_type_list is None:
            raise ValidationArticleCitationsException(
                "Function requires list of publications type"
            )
        publication_type = self.citation.get("publication_type")
        is_valid = publication_type in publication_type_list
        yield format_response(
            title="element citation validation",
            parent=self.citation.get("parent"),
            parent_id=self.citation.get("parent_id"),
            parent_article_type=self.citation.get("parent_article_type"),
            parent_lang=self.citation.get("parent_lang"),
            item="element-citation",
            sub_item="publication-type",
            is_valid=is_valid,
            validation_type="value in list",
            expected=publication_type_list,
            obtained=publication_type,
            advice=f"publication-type for the reference (ref-id: {self.citation.get('ref_id')}) is missing or is "
            f"invalid, provide one value from the list: {' | '.join(publication_type_list)}",
            data=self.citation,
            error_level=error_level,
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
                "advice": "Wrap the <ext-link> tag and its content within the <comment> tag"
            },
            {
                "condition": has_comment and not full_comment and not text_before_extlink,
                "expected": f"<ext-link>{ext_link_text}</ext-link>",
                "obtained": f"<comment></comment><ext-link>{ext_link_text}</ext-link>",
                "advice": "Remove the <comment> tag that has no content"
            },
            {
                "condition": not has_comment and text_before_extlink,
                "expected": f"<comment>{text_before_extlink}<ext-link>{ext_link_text}</ext-link></comment>",
                "obtained": f"{text_before_extlink}<ext-link>{ext_link_text}</ext-link>",
                "advice": "Wrap the <ext-link> tag and its content within the <comment> tag"
            },
            {
                "condition": full_comment and not text_between,
                "expected": f"<ext-link>{ext_link_text}</ext-link>",
                "obtained": f"<comment><ext-link>{ext_link_text}</ext-link></comment>",
                "advice": "Remove the <comment> tag that has no content"
            }
        ]

        for scenario in scenarios:
            if scenario["condition"]:
                yield format_response(
                    title="validate comment is required or not",
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


class ArticleCitationsValidation:
    def __init__(self, xmltree, publication_type_list=None):
        self._xmltree = xmltree
        self.article_citations = ArticleCitations(self._xmltree).article_citations
        self.publication_type_list = publication_type_list

    def validate_article_citations(
        self, xmltree, publication_type_list=None, start_year=None, end_year=None
    ):
        for article_citation in self.article_citations:
            citation = ArticleCitationValidation(
                xmltree, article_citation, publication_type_list
            )
            yield from citation.validate_article_citation_year(
                start_year=start_year, end_year=end_year
            )
            yield from citation.validate_article_citation_source()
            yield from citation.validate_article_citation_article_title()
            yield from citation.validate_article_citation_authors()
            yield from citation.validate_article_citation_publication_type(
                publication_type_list
            )
            yield from citation.validate_comment_is_required_or_not()
