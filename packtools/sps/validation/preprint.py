from packtools.sps.models.v2.related_articles import RelatedArticles
from packtools.sps.models.article_dates import HistoryDates
from packtools.sps.validation.utils import format_response


class PreprintValidation:
    def __init__(self, xml_tree):
        self.xml_tree = xml_tree
        self.related_articles = RelatedArticles(xml_tree).related_articles()
        self.article_dates = list(HistoryDates(xml_tree).history_dates())

    def _extract_preprint_status(self):
        return [item for item in self.related_articles if item.get('related-article-type') == "preprint"]

    def _extract_preprint_date(self):
        if self.article_dates:
            preprint_date = self.article_dates[0].get("history", {}).get("preprint")
            return '-'.join([preprint_date[key] for key in ['year', 'month', 'day']]) if preprint_date else None

    def preprint_validation(self, error_level="ERROR"):
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
        has_preprint = self._extract_preprint_status()
        has_preprint_date = self._extract_preprint_date()

        if not (has_preprint or has_preprint_date):
            return []

        response, expected_value, got_value, advice = True, has_preprint_date, has_preprint_date, None

        if has_preprint and not has_preprint_date:
            response, expected_value, got_value, advice = \
                False, 'The preprint publication date', None, 'Provide the publication date of the preprint'
        elif not has_preprint and has_preprint_date:
            response, expected_value, got_value, advice = \
                False, None, has_preprint_date, 'The article does not reference the preprint, ' \
                                                  'provide it as in the example: <related-article id="pp1" ' \
                                                  'related-article-type="preprint" ext-link-type="doi" ' \
                                                  'xlink:href="10.1590/SciELOPreprints.1174"/>'

        yield format_response(
            title='Preprint validation',
            parent="article",
            parent_id=None,
            parent_article_type=self.xml_tree.get("article-type"),
            parent_lang=self.xml_tree.get("{http://www.w3.org/XML/1998/namespace}lang"),
            item='related-article / date',
            sub_item='@related-article-type=preprint / @date-type=preprint',
            validation_type='exist',
            is_valid=response,
            expected=expected_value,
            obtained=got_value,
            advice=advice,
            data=has_preprint[0] if has_preprint else None,
            error_level=error_level,
        )
