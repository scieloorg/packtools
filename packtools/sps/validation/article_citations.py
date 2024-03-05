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

