from packtools.sps.models.article_citations import ArticleCitations
from packtools.sps.validation.exceptions import ValidationArticleCitationsException


class ArticleCitationsValidation:
    def __init__(self, xmltree, publication_type_list=None):
        self._xmltree = xmltree
        self.article_citations = list(ArticleCitations(self._xmltree).article_citations)
        self.publication_type_list = publication_type_list

    def validate_article_citation_year(self):
        """
        Checks whether the year in an article citation exists and is valid.

        Returns
        -------
        list of dict
            A list of dictionaries, such as:
            [
                {
                    'title': 'element citation validation',
                    'element': 'element-citation',
                    'sub-element': 'year',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': '2015',
                    'got_value': '2015',
                    'message': f'Got 2015 expected 2015',
                    'advice': None
                },...
            ]
        """
        for citation in self.article_citations:
            if citation.get('year'):
                year = str(citation['year'])
                is_valid = year.isdigit() and len(year) == 4
            else:
                year = None
                is_valid = False
            yield {
                'title': 'element citation validation',
                'element': 'element-citation',
                'sub-element': 'year',
                'validation_type': 'exist',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': year if is_valid else 'a valid value to year',
                'got_value': year,
                'message': f'Got {year} expected {year if is_valid else "a valid value to year"}',
                'advice': None if is_valid else f"The year in reference (ref-id: {citation.get('ref_id')}) is missing "
                                                f"or is invalid, provide a valid value to year"
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
                    'element': 'element-citation',
                    'sub-element': 'source',
                    'validation_type': 'exist',
                    'response': 'OK',
                    'expected_value': 'Drug Alcohol Depend.',
                    'got_value': 'Drug Alcohol Depend.',
                    'message': 'Got Drug Alcohol Depend. expected Drug Alcohol Depend.',
                    'advice': None
                },...
            ]
        """
        for citation in self.article_citations:
            source = citation.get('source')
            is_valid = source is not None
            yield {
                'title': 'element citation validation',
                'element': 'element-citation',
                'sub-element': 'source',
                'validation_type': 'exist',
                'response': 'OK' if is_valid else 'ERROR',
                'expected_value': source if is_valid else 'a valid value to source',
                'got_value': source,
                'message': f'Got {source} expected {source if is_valid else "a valid value to source"}',
                'advice': None if is_valid else f"The source in reference (ref-id: {citation.get('ref_id')}) is missing "
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
                    'element': 'element-citation',
                    'sub-element': 'article-title',
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
        for citation in self.article_citations:
            publication_type = citation.get('publication_type')
            if publication_type == 'journal':
                article_title = citation.get('article_title')
                is_valid = article_title is not None
                yield {
                    'title': 'element citation validation',
                    'element': 'element-citation',
                    'sub-element': 'article-title',
                    'validation_type': 'exist',
                    'response': 'OK' if is_valid else 'ERROR',
                    'expected_value': article_title if is_valid else 'a valid value to article-title',
                    'got_value': article_title,
                    'message': f'Got {article_title} expected {article_title if is_valid else "a valid value to article-title"}',
                    'advice': None if is_valid else f"The article-title in reference (ref-id: {citation.get('ref_id')}) is missing "
                                                    f"provide a valid value to article-title"
                }

