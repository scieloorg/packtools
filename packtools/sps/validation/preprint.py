from packtools.sps.models.related_articles import RelatedItems
from packtools.sps.models.dates import ArticleDates


class PreprintValidation:
    def __init__(self, xmltree):
        self.related_articles = RelatedItems(xmltree).related_articles
        self.article_dates = ArticleDates(xmltree).history_dates_dict

    def _extract_preprint_status(self):
        return [item.get('preprint') for item in self.related_articles]

    def _extract_preprint_date(self):
        preprint_date = self.article_dates.get('preprint')
        return '-'.join([preprint_date[key] for key in ['year', 'month', 'day']]) if preprint_date else None

    def preprint_validation(self):
        """
        Checks whether an article that has a preprint has the corresponding date in the history.

        XML input
        ---------
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
            <front>
                <article-meta>
                    <history>
                        <date date-type="preprint">
                            <day>18</day>
                            <month>10</month>
                            <year>2002</year>
                        </date>
                    </history>
                </article-meta>
            </front>
            <related-article id="pp1" related-article-type="preprint" ext-link-type="doi" xlink:href="10.1590/SciELOPreprints.1174"/>
        </article>

        Returns
        -------
        dict, such as:
            {
                'title': 'Preprint validation',
                'xpath': './/related-article[@related-article-type="preprint"] .//history//date[@date-type="preprint"]',
                'validation_type': 'exist, match',
                'response': 'OK',
                'expected_value': '2002-10-18',
                'got_value': '2002-10-18',
                'message': 'Got 2002-10-18 expected 2002-10-18',
                'advice': None
            }
        """
        is_preprint = self._extract_preprint_status()
        has_preprint_date = self._extract_preprint_date()

        if not (is_preprint or has_preprint_date):
            return

        response, expected_value, got_value, advice = 'OK', has_preprint_date, has_preprint_date, None

        if is_preprint and not has_preprint_date:
            response, expected_value, got_value, advice = \
                'ERROR', 'The preprint publication date', None, 'Provide the publication date of the preprint'
        elif not is_preprint and has_preprint_date:
            response, expected_value, got_value, advice = \
                'ERROR', None, has_preprint_date, 'The article does not have a preprint remove the publication date from the preprint'

        return {
                'title': 'Preprint validation',
                'xpath': './/related-article[@related-article-type="preprint"] .//history//date[@date-type="preprint"]',
                'validation_type': 'exist, match',
                'response': response,
                'expected_value': expected_value,
                'got_value': got_value,
                'message': f'Got {got_value} expected {expected_value}',
                'advice': advice
            }
