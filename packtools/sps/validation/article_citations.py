from packtools.sps.models.article_citations import ArticleCitations
from packtools.sps.models.dates import ArticleDates
from packtools.sps.validation.exceptions import ValidationArticleCitationsException


class ArticleCitationValidation:
    def __init__(self, xmltree, citation, publication_type_list=None):
        self.xmltree = xmltree
        self.citation = citation
        self.publication_type_list = publication_type_list

    def validate_article_citation_year(self, start_year=None, end_year=None):
        """
        Checks whether the year in an article citation exists and is valid.

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'element citation validation',
                    'item': 'element-citation',
                    'sub-item': 'year',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': '2015',
                    'got_value': '2015',
                    'message': f'Got 2015 expected 2015',
                    'advice': None
                },...
            ]
        """
        if start_year is None:
            start_year = 0
        if end_year is None:
            try:
                end_year = int(ArticleDates(self.xmltree).collection_date['year'])
            except TypeError:
                raise ValidationArticleCitationsException('Article publication date not found and is required')
        year = self.citation.get('year')
        try:
            is_valid = start_year < int(year) <= end_year
        except (TypeError, ValueError):
            is_valid = False
        yield {
            'title': 'element citation validation',
            'item': 'element-citation',
            'sub-item': 'year',
            'validation_type': 'exist',
            'response': 'OK' if is_valid else 'ERROR',
            'expected_value': f'a value for year between {start_year} and {end_year}',
            'got_value': year,
            'message': f'Got {year} expected a value for year between {start_year} and {end_year}',
            'advice': None if is_valid else f"The year in reference (ref-id: {self.citation.get('ref_id')}) is missing "
                                            f"or is invalid, provide a valid value for year"
        }

    def validate_article_citation_source(self):
        """
        Checks whether the source in an article citation exists.

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'element citation validation',
                    'item': 'element-citation',
                    'sub-item': 'source',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'Drug Alcohol Depend.',
                    'got_value': 'Drug Alcohol Depend.',
                    'message': 'Got Drug Alcohol Depend. expected Drug Alcohol Depend.',
                    'advice': None
                },...
            ]
        """
        source = self.citation.get('source')
        is_valid = source is not None
        yield {
            'title': 'element citation validation',
            'item': 'element-citation',
            'sub-item': 'source',
            'validation_type': 'exist',
            'response': 'OK' if is_valid else 'ERROR',
            'expected_value': source if is_valid else 'a valid value to source',
            'got_value': source,
            'message': f'Got {source} expected {source if is_valid else "a valid value to source"}',
            'advice': None if is_valid else f"The source in reference (ref-id: {self.citation.get('ref_id')}) is missing "
                                            f"provide a valid value to source"
        }

    def validate_article_citation_article_title(self):
        """
        Checks whether the article title in an article citation exists.

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'element citation validation',
                    'item': 'element-citation',
                    'sub-item': 'article-title',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'Smoking and potentially preventable hospitalisation: the benefit of smoking '
                                      'cessation in older ages',
                    'got_value': 'Smoking and potentially preventable hospitalisation: the benefit of smoking cessation '
                                 'in older ages',
                    'message': 'Got Smoking and potentially preventable hospitalisation: the benefit of smoking cessation '
                               'in older ages expected Smoking and potentially preventable hospitalisation: the benefit '
                               'of smoking cessation in older ages',
                    'advice': None
                },...
            ]
        """
        publication_type = self.citation.get('publication_type')
        if publication_type == 'journal':
            article_title = self.citation.get('article_title')
            is_valid = article_title is not None
            yield {
                'title': 'element citation validation',
                'item': 'element-citation',
                'sub-item': 'article-title',
                'validation_type': 'exist',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': article_title if is_valid else 'a valid value for article-title',
                'got_value': article_title,
                'message': f'Got {article_title} expected {article_title if is_valid else "a valid value for article-title"}',
                'advice': None if is_valid else f"The article-title in reference (ref-id: {self.citation.get('ref_id')}) is missing "
                                                f"provide a valid value for article-title"
            }

    def validate_article_citation_authors(self):
        """
        Checks if there are authors for the article citation.

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'element citation validation',
                    'item': 'element-citation',
                    'sub-item': 'person-group//name or person-group//colab',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'at least 1 author in each element-citation',
                    'got_value': '5 authors',
                    'message': f'Got 5 authors expected at least 1 author in each element-citation',
                    'advice': None
                },...
            ]
        """
        number_authors = len(self.citation.get('all_authors')) if self.citation.get('all_authors') else 0
        is_valid = number_authors > 0
        yield {
            'title': 'element citation validation',
            'item': 'element-citation',
            'sub-item': 'person-group//name or person-group//colab',
            'validation_type': 'exist',
            'response': 'OK' if is_valid else 'ERROR',
            'expected_value': 'at least 1 author in each element-citation',
            'got_value': f'{number_authors} authors',
            'message': f'Got {number_authors} authors expected at least 1 author in each element-citation',
            'advice': None if is_valid else f"There are no authors for the reference (ref-id: {self.citation.get('ref_id')}) "
                                            f"provide at least 1 author"
        }

    def validate_article_citation_publication_type(self, publication_type_list=None):
        """
        Checks if the publication type is present in the list of default values.

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'element citation validation',
                    'item': 'element-citation',
                    'sub-item': 'publication-type',
                    'validation_type': 'value in list',
                    'response': 'OK',
                    'expected_value': ['journal', 'book'],
                    'got_value': 'journal',
                    'message': 'Got journal expected one item of this list: journal | book',
                    'advice': None
                },...
            ]
        """
        publication_type_list = publication_type_list or self.publication_type_list
        if publication_type_list is None:
            raise ValidationArticleCitationsException('Function requires list of publications type')
        publication_type = self.citation.get('publication_type')
        is_valid = publication_type in publication_type_list
        yield {
            'title': 'element citation validation',
            'item': 'element-citation',
            'sub-item': 'publication-type',
            'validation_type': 'value in list',
            'response': 'OK' if is_valid else 'ERROR',
            'expected_value': publication_type_list,
            'got_value': publication_type,
            'message': f'Got {publication_type} expected one item of this list: {" | ".join(publication_type_list)}',
            'advice': None if is_valid else f"publication-type for the reference (ref-id: {self.citation.get('ref_id')}) "
                                            f"is missing or is invalid, provide one value from the list: {' | '.join(publication_type_list)}"
        }


class ArticleCitationsValidation:
    def __init__(self, xmltree, publication_type_list=None):
        self._xmltree = xmltree
        self.article_citations = ArticleCitations(self._xmltree).article_citations
        self.publication_type_list = publication_type_list

    def validate_article_citations(self, xmltree, publication_type_list=None, start_year=None, end_year=None):
        for article_citation in self.article_citations:
            citation = ArticleCitationValidation(xmltree, article_citation, publication_type_list)
            yield from citation.validate_article_citation_year(start_year=start_year, end_year=end_year)
            yield from citation.validate_article_citation_source()
            yield from citation.validate_article_citation_article_title()
            yield from citation.validate_article_citation_authors()
            yield from citation.validate_article_citation_publication_type(publication_type_list)




