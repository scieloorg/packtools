from unittest import TestCase
from lxml import etree

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation import dates


class HistoryDatesValidationTest(TestCase):
    def test_validate_history_dates_success(self):
        self.maxDiff = None
        xml_history_date = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <history>
                            <date date-type="received">
                                <day>05</day>
                                <month>01</month>
                                <year>1998</year>
                            </date>
                            <date date-type="rev-request">
                                <day>14</day>
                                <month>03</month>
                                <year>1998</year>
                            </date>
                            <date date-type="rev-recd">
                                <day>24</day>
                                <month>05</month>
                                <year>1998</year>
                            </date>
                            <date date-type="accepted">
                                <day>06</day>
                                <month>06</month>
                                <year>1998</year>
                            </date>
                            <date date-type="approved">
                                <day>01</day>
                                <month>06</month>
                                <year>2012</year>
                            </date>
                        </history>
                    </article-meta>
                </front>
            </article>
            """
        )
        expected = [
            {
                'title': 'History date validation',
                'xpath': './/front//history//date',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': ['received', 'rev-request', 'rev-recd', 'accepted', 'approved'],
                'got_value': ['received', 'rev-request', 'rev-recd', 'accepted', 'approved'],
                'message': "Got [('received', '1998-01-05'), ('rev-request', '1998-03-14'), ('rev-recd', "
                           "'1998-05-24'), ('accepted', '1998-06-06'), ('approved', '2012-06-01')] expected ["
                           "'received', 'rev-request', 'rev-recd', 'accepted', 'approved']",
                'advice': None
            }
        ]
        obtained = dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "approved"], ["received", "approved"]
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_history_dates_success_required_data_only(self):
        self.maxDiff = None
        xml_history_date = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <history>
                            <date date-type="received">
                                <day>05</day>
                                <month>01</month>
                                <year>1998</year>
                            </date>
                            <date date-type="approved">
                                <day>01</day>
                                <month>06</month>
                                <year>2012</year>
                            </date>
                        </history>
                    </article-meta>
                </front>
            </article>
            """
        )
        expected = [
            {
                'title': 'History date validation',
                'xpath': './/front//history//date',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': ['received', 'approved'],
                'got_value': ['received', 'approved'],
                'message': "Got [('received', '1998-01-05'), ('approved', '2012-06-01')] "
                           "expected ['received', 'approved']",
                'advice': None
            }
        ]
        obtained = dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "approved"], ["received", "approved"]
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_history_dates_fail_required_date_missing(self):
        self.maxDiff = None
        xml_history_date = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <history>
                            <date date-type="received">
                                <day>05</day>
                                <month>01</month>
                                <year>1998</year>
                            </date>
                            <date date-type="rev-request">
                                <day>14</day>
                                <month>03</month>
                                <year>1998</year>
                            </date>
                            <date date-type="rev-recd">
                                <day>24</day>
                                <month>05</month>
                                <year>1998</year>
                            </date>
                            <date date-type="accepted">
                                <day>06</day>
                                <month>06</month>
                                <year>1998</year>
                            </date>
                        </history>
                    </article-meta>
                </front>
            </article>
            """
        )
        expected = [
            {
                'title': 'History date validation',
                'xpath': './/front//history//date',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'a date for approved',
                'got_value': None,
                'message': 'the event approved is required',
                'advice': 'Provide a valid date for approved',
            },
            {
                'title': 'History date validation',
                'xpath': './/front//history//date',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': ['received', 'rev-request', 'rev-recd', 'accepted'],
                'got_value': ['received', 'rev-request', 'rev-recd', 'accepted'],
                'message': "Got [('received', '1998-01-05'), ('rev-request', '1998-03-14'), ('rev-recd', "
                           "'1998-05-24'), ('accepted', '1998-06-06')] expected ['received', 'rev-request', "
                           "'rev-recd', 'accepted']",
                'advice': None
            }
        ]
        obtained = dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "approved"], ["received", "approved"]
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_history_dates_fail_unknown_event(self):
        self.maxDiff = None
        xml_history_date = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <history>
                            <date date-type="received">
                                <day>05</day>
                                <month>01</month>
                                <year>1998</year>
                            </date>
                            <date date-type="rev-request">
                                <day>14</day>
                                <month>03</month>
                                <year>1998</year>
                            </date>
                            <date date-type="rev-recd">
                                <day>24</day>
                                <month>05</month>
                                <year>1998</year>
                            </date>
                            <date date-type="accepted">
                                <day>06</day>
                                <month>06</month>
                                <year>1998</year>
                            </date>
                            <date date-type="unknown">
                                <day>01</day>
                                <month>06</month>
                                <year>2012</year>
                            </date>
                        </history>
                    </article-meta>
                </front>
            </article>
            """
        )
        expected = [
            {
                'title': 'History date validation',
                'xpath': './/front//history//date',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'a date for approved',
                'got_value': None,
                'message': 'the event approved is required',
                'advice': 'Provide a valid date for approved',
            },
            {
                'title': 'History date validation',
                'xpath': './/front//history//date',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': ['received', 'rev-request', 'rev-recd', 'accepted'],
                'got_value': ['received', 'rev-request', 'rev-recd', 'accepted'],
                'message': "Got [('received', '1998-01-05'), ('rev-request', '1998-03-14'), ('rev-recd', "
                           "'1998-05-24'), ('accepted', '1998-06-06')] expected ['received', 'rev-request', "
                           "'rev-recd', 'accepted']",
                'advice': None,
            }
        ]
        obtained = dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "approved"], ["received", "approved"]
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_history_dates_fail_one_element_of_date_is_missing(self):
        self.maxDiff = None
        xml_history_date = etree.fromstring(
            """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                    <front>
                        <article-meta>
                            <history>
                                <date date-type="received">
                                    <month>01</month>
                                    <year>1998</year>
                                </date>
                                <date date-type="rev-request">
                                    <day>14</day>
                                    <year>1998</year>
                                </date>
                                <date date-type="rev-recd">
                                    <day>24</day>
                                    <month>05</month>
                                </date>
                                <date date-type="accepted">
                                    <day>06</day>
                                    <month>06</month>
                                    <year>1998</year>
                                </date>
                                <date date-type="approved">
                                    <day>01</day>
                                    <month>06</month>
                                    <year>2012</year>
                                </date>
                            </history>
                        </article-meta>
                    </front>
                </article>
                """
        )
        expected = [
            {
                'title': 'History date validation',
                'xpath': './/front//history//date',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a valid date for received',
                'got_value': '1998-01-',
                'message': 'received must be complete',
                'advice': 'Provide \'day\' of the date',
            },
            {
                'title': 'History date validation',
                'xpath': './/front//history//date',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a valid date for rev-request',
                'got_value': '1998--14',
                'message': 'rev-request must be complete',
                'advice': 'Provide \'month\' of the date',
            },
            {
                'title': 'History date validation',
                'xpath': './/front//history//date',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a valid date for rev-recd',
                'got_value': '-05-24',
                'message': 'rev-recd must be complete',
                'advice': 'Provide \'year\' of the date',
            },
            {
                'title': 'History date validation',
                'xpath': './/front//history//date',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': ['accepted', 'approved'],
                'got_value': ['accepted', 'approved'],
                'message': "Got [('accepted', '1998-06-06'), ('approved', '2012-06-01')] expected ['accepted', "
                           "'approved']",
                'advice': None
            },
        ]
        obtained = dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "approved"], ["received", "approved"]
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_history_dates_fail_one_element_of_date_is_invalid(self):
        self.maxDiff = None
        xml_history_date = etree.fromstring(
            """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                    <front>
                        <article-meta>
                            <history>
                                <date date-type="received">
                                    <day>05</day>
                                    <month>01</month>
                                    <year>1998</year>
                                </date>
                                <date date-type="rev-request">
                                    <day>40</day>
                                    <month>03</month>
                                    <year>1998</year>
                                </date>
                                <date date-type="rev-recd">
                                    <day>24</day>
                                    <month>13</month>
                                    <year>1998</year>
                                </date>
                                <date date-type="accepted">
                                    <day>06</day>
                                    <month>06</month>
                                    <year>1998</year>
                                </date>
                                <date date-type="approved">
                                    <day>01</day>
                                    <month>06</month>
                                    <year>2012</year>
                                </date>
                            </history>
                        </article-meta>
                    </front>
                </article>
                """
        )
        expected = [
            {
                'title': 'History date validation',
                'xpath': './/front//history//date',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a valid date for rev-request',
                'got_value': '1998-03-40',
                'message': 'rev-request must contain valid values',
                'advice': 'Provide valid values for day, month and year',
            },
            {
                'title': 'History date validation',
                'xpath': './/front//history//date',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a valid date for rev-recd',
                'got_value': '1998-13-24',
                'message': 'rev-recd must contain valid values',
                'advice': 'Provide valid values for day, month and year',
            },
            {
                'title': 'History date validation',
                'xpath': './/front//history//date',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': ['received', 'accepted', 'approved'],
                'got_value': ['received', 'accepted', 'approved'],
                'message': "Got [('received', '1998-01-05'), ('accepted', '1998-06-06'), ('approved', '2012-06-01')] "
                           "expected ['received', 'accepted', 'approved']",
                'advice': None
            },
        ]
        obtained = dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "approved"], ["received", "approved"]
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_history_dates_fail_order_is_invalid(self):
        self.maxDiff = None
        xml_history_date = etree.fromstring(
            """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                    <front>
                        <article-meta>
                            <history>
                                <date date-type="received">
                                    <day>05</day>
                                    <month>01</month>
                                    <year>1998</year>
                                </date>
                                <date date-type="rev-request">
                                    <day>04</day>
                                    <month>01</month>
                                    <year>1998</year>
                                </date>
                                <date date-type="rev-recd">
                                    <day>24</day>
                                    <month>05</month>
                                    <year>1998</year>
                                </date>
                                <date date-type="accepted">
                                    <day>06</day>
                                    <month>06</month>
                                    <year>1998</year>
                                </date>
                                <date date-type="approved">
                                    <day>01</day>
                                    <month>06</month>
                                    <year>2012</year>
                                </date>
                            </history>
                        </article-meta>
                    </front>
                </article>
                """
        )
        expected = [
            {
                'title': 'History date validation',
                'xpath': './/front//history//date',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': ['received', 'rev-request', 'rev-recd', 'accepted', 'approved'],
                'got_value': ['rev-request', 'received', 'rev-recd', 'accepted', 'approved'],
                'message': "Got [('received', '1998-01-05'), ('rev-request', '1998-01-04'), ('rev-recd', "
                           "'1998-05-24'), ('accepted', '1998-06-06'), ('approved', '2012-06-01')] expected ["
                           "'received', 'rev-request', 'rev-recd', 'accepted', 'approved']",
                'advice': "Provide a valid sequence of events: ['received', 'rev-request', 'rev-recd', 'accepted', "
                          "'approved']",
            }
        ]
        obtained = dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "approved"], ["received", "approved"]
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_history_dates_fail_event_required_is_missing(self):
        self.maxDiff = None
        xml_history_date = etree.fromstring(
            """
                <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                    <front>
                        <article-meta>
                            <history>
                                <date date-type="received">
                                    <day>05</day>
                                    <month>01</month>
                                    <year>1998</year>
                                </date>
                                <date date-type="rev-request">
                                    <day>14</day>
                                    <month>03</month>
                                    <year>1998</year>
                                </date>
                                <date date-type="rev-recd">
                                    <day>24</day>
                                    <month>05</month>
                                    <year>1998</year>
                                </date>
                                <date date-type="approved">
                                    <day>01</day>
                                    <month>06</month>
                                    <year>2012</year>
                                </date>
                            </history>
                        </article-meta>
                    </front>
                </article>
                """
        )
        expected = [
            {
                'title': 'History date validation',
                'xpath': './/front//history//date',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'a date for accepted',
                'got_value': None,
                'message': 'the event accepted is required',
                'advice': 'Provide a valid date for accepted'
            },
            {
                'title': 'History date validation',
                'xpath': './/front//history//date',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': ['received', 'rev-request', 'rev-recd', 'approved'],
                'got_value': ['received', 'rev-request', 'rev-recd', 'approved'],
                'message': "Got [('received', '1998-01-05'), ('rev-request', '1998-03-14'), ('rev-recd', "
                           "'1998-05-24'), ('approved', '2012-06-01')] expected ['received', 'rev-request', "
                           "'rev-recd', 'approved']",
                'advice': None
            }
        ]
        obtained = dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "approved"], ["accepted", "approved"]
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)


class ArticleDatesValidationTest(TestCase):
    def test_validate_number_of_digits_in_article_date_is_ok(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
                    <article-id pub-id-type="other">00303</article-id>
                    <pub-date date-type="pub" publication-format="electronic">
                        <day>03</day>
                        <month>02</month>
                        <year>2024</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = get_xml_tree(xml_str)
        obtained = dates.ArticleDatesValidation(xml_tree).validate_number_of_digits_in_article_date()
        expected = [
            {
                'title': 'Article pub-date day validation',
                'xpath': './/front//pub-date[@date-type="pub"]/day',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '03',
                'got_value': '03',
                'message': 'Got 03 expected 03',
                'advice': None
            },
            {
                'title': 'Article pub-date month validation',
                'xpath': './/front//pub-date[@date-type="pub"]/month',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '02',
                'got_value': '02',
                'message': 'Got 02 expected 02',
                'advice': None
            },
            {
                'title': 'Article pub-date year validation',
                'xpath': './/front//pub-date[@date-type="pub"]/year',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '2024',
                'got_value': '2024',
                'message': 'Got 2024 expected 2024',
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_number_of_digits_in_article_date_year_is_not_ok(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
                    <article-id pub-id-type="other">00303</article-id>
                    <pub-date date-type="pub" publication-format="electronic">
                        <day>03</day>
                        <month>02</month>
                        <year>202</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = get_xml_tree(xml_str)
        obtained = dates.ArticleDatesValidation(xml_tree).validate_number_of_digits_in_article_date()
        expected = [
            {
                'title': 'Article pub-date day validation',
                'xpath': './/front//pub-date[@date-type="pub"]/day',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '03',
                'got_value': '03',
                'message': 'Got 03 expected 03',
                'advice': None
            },
            {
                'title': 'Article pub-date month validation',
                'xpath': './/front//pub-date[@date-type="pub"]/month',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '02',
                'got_value': '02',
                'message': 'Got 02 expected 02',
                'advice': None
            },
            {
                'title': 'Article pub-date year validation',
                'xpath': './/front//pub-date[@date-type="pub"]/year',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': '0202',
                'got_value': '202',
                'message': 'Got 202 expected 0202',
                'advice': 'Provide a 4-digit numeric value for year'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_number_of_digits_in_article_date_month_is_not_ok(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
                    <article-id pub-id-type="other">00303</article-id>
                    <pub-date date-type="pub" publication-format="electronic">
                        <day>03</day>
                        <month>2</month>
                        <year>2024</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = get_xml_tree(xml_str)
        obtained = dates.ArticleDatesValidation(xml_tree).validate_number_of_digits_in_article_date()
        expected = [
            {
                'title': 'Article pub-date day validation',
                'xpath': './/front//pub-date[@date-type="pub"]/day',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '03',
                'got_value': '03',
                'message': 'Got 03 expected 03',
                'advice': None
            },
            {
                'title': 'Article pub-date month validation',
                'xpath': './/front//pub-date[@date-type="pub"]/month',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': '02',
                'got_value': '2',
                'message': 'Got 2 expected 02',
                'advice': 'Provide a 2-digit numeric value for month'
            },
            {
                'title': 'Article pub-date year validation',
                'xpath': './/front//pub-date[@date-type="pub"]/year',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '2024',
                'got_value': '2024',
                'message': 'Got 2024 expected 2024',
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_number_of_digits_in_article_date_day_is_not_ok(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
                    <article-id pub-id-type="other">00303</article-id>
                    <pub-date date-type="pub" publication-format="electronic">
                        <day>3</day>
                        <month>02</month>
                        <year>2024</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = get_xml_tree(xml_str)
        obtained = dates.ArticleDatesValidation(xml_tree).validate_number_of_digits_in_article_date()
        expected = [
            {
                'title': 'Article pub-date day validation',
                'xpath': './/front//pub-date[@date-type="pub"]/day',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': '03',
                'got_value': '3',
                'message': 'Got 3 expected 03',
                'advice': 'Provide a 2-digit numeric value for day'
            },
            {
                'title': 'Article pub-date month validation',
                'xpath': './/front//pub-date[@date-type="pub"]/month',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '02',
                'got_value': '02',
                'message': 'Got 02 expected 02',
                'advice': None
            },
            {
                'title': 'Article pub-date year validation',
                'xpath': './/front//pub-date[@date-type="pub"]/year',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '2024',
                'got_value': '2024',
                'message': 'Got 2024 expected 2024',
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_number_of_digits_in_article_non_numeric_digits(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
                    <article-id pub-id-type="other">00303</article-id>
                    <pub-date date-type="pub" publication-format="electronic">
                        <day>dd</day>
                        <month>mm</month>
                        <year>yyyy</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = get_xml_tree(xml_str)
        obtained = dates.ArticleDatesValidation(xml_tree).validate_number_of_digits_in_article_date()
        expected = [
            {
                'title': 'Article pub-date day validation',
                'xpath': './/front//pub-date[@date-type="pub"]/day',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'A numeric digit for day represented with 2 digits',
                'got_value': 'dd',
                'message': 'Got a non-numeric value for day',
                'advice': 'Provide a 2-digit numeric value for day'
            },
            {
                'title': 'Article pub-date month validation',
                'xpath': './/front//pub-date[@date-type="pub"]/month',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'A numeric digit for month represented with 2 digits',
                'got_value': 'mm',
                'message': 'Got a non-numeric value for month',
                'advice': 'Provide a 2-digit numeric value for month'
            },
            {
                'title': 'Article pub-date year validation',
                'xpath': './/front//pub-date[@date-type="pub"]/year',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'A numeric digit for year represented with 4 digits',
                'got_value': 'yyyy',
                'message': 'Got a non-numeric value for year',
                'advice': 'Provide a 4-digit numeric value for year'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_date_is_ok(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
                    <article-id pub-id-type="other">00303</article-id>
                    <pub-date date-type="pub" publication-format="electronic">
                        <day>01</day>
                        <month>01</month>
                        <year>2023</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = get_xml_tree(xml_str)
        obtained = dates.ArticleDatesValidation(xml_tree).validate_article_date('2023-12-12')
        expected = {
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type="pub"]',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': 'A date in the format: YYYY-MM-DD before or equal to 2023-12-12',
                'got_value': '2023-01-01',
                'message': '2023-01-01 is an valid date',
                'advice': None
            }
        self.assertDictEqual(expected, obtained)

    def test_validate_article_date_year_is_not_ok(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
                    <article-id pub-id-type="other">00303</article-id>
                    <pub-date date-type="pub" publication-format="electronic">
                        <day>01</day>
                        <month>01</month>
                        <year>0</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = get_xml_tree(xml_str)
        obtained = dates.ArticleDatesValidation(xml_tree).validate_article_date('2023-12-12')
        expected = {
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type="pub"]',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': 'A date in the format: YYYY-MM-DD before or equal to 2023-12-12',
                'got_value': '0-01-01',
                'message': '0-01-01 is an invalid date',
                'advice': 'Provide a date in the format: YYYY-MM-DD before or equal to 2023-12-12'
            }
        self.assertDictEqual(expected, obtained)

    def test_validate_article_date_month_is_not_ok(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
                    <article-id pub-id-type="other">00303</article-id>
                    <pub-date date-type="pub" publication-format="electronic">
                        <day>01</day>
                        <month>13</month>
                        <year>2023</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = get_xml_tree(xml_str)
        obtained = dates.ArticleDatesValidation(xml_tree).validate_article_date('2023-12-12')
        expected = {
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type="pub"]',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': 'A date in the format: YYYY-MM-DD before or equal to 2023-12-12',
                'got_value': '2023-13-01',
                'message': '2023-13-01 is an invalid date',
                'advice': 'Provide a date in the format: YYYY-MM-DD before or equal to 2023-12-12'
            }
        self.assertDictEqual(expected, obtained)

    def test_validate_article_date_day_is_not_ok(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
                    <article-id pub-id-type="other">00303</article-id>
                    <pub-date date-type="pub" publication-format="electronic">
                        <day>32</day>
                        <month>01</month>
                        <year>2023</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = get_xml_tree(xml_str)
        obtained = dates.ArticleDatesValidation(xml_tree).validate_article_date('2023-12-12')
        expected = {
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type="pub"]',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': 'A date in the format: YYYY-MM-DD before or equal to 2023-12-12',
                'got_value': '2023-01-32',
                'message': '2023-01-32 is an invalid date',
                'advice': 'Provide a date in the format: YYYY-MM-DD before or equal to 2023-12-12'
            }
        self.assertDictEqual(expected, obtained)

    def test_validate_article_date_is_a_future_date(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
                    <article-id pub-id-type="other">00303</article-id>
                    <pub-date date-type="pub" publication-format="electronic">
                        <day>01</day>
                        <month>01</month>
                        <year>2023</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = get_xml_tree(xml_str)
        obtained = dates.ArticleDatesValidation(xml_tree).validate_article_date('2020-12-12')
        expected = {
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type="pub"]',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': 'A date in the format: YYYY-MM-DD before or equal to 2020-12-12',
                'got_value': '2023-01-01',
                'message': '2023-01-01 is an invalid date',
                'advice': 'Provide a date in the format: YYYY-MM-DD before or equal to 2020-12-12'
            }
        self.assertDictEqual(expected, obtained)

    def test_validate_collection_date_success(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
                    <article-id pub-id-type="other">00303</article-id>
                    <pub-date date-type="pub" publication-format="electronic">
                        <day>01</day>
                        <month>01</month>
                        <year>2023</year>
                    </pub-date>
                    <pub-date date-type="collection" publication-format="electronic">
                        <year>2023</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = get_xml_tree(xml_str)
        obtained = dates.ArticleDatesValidation(xml_tree).validate_collection_date('2023')
        expected = [
            {
                'title': 'Collection pub-date validation',
                'xpath': './/front//pub-date[@date-type="collection"]',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '2023',
                'got_value': '2023',
                'message': 'Got 2023 expected 2023',
                'advice': None
            }
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_collection_date_fail_type_digit(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
                    <article-id pub-id-type="other">00303</article-id>
                    <pub-date date-type="pub" publication-format="electronic">
                        <day>01</day>
                        <month>01</month>
                        <year>2023</year>
                    </pub-date>
                    <pub-date date-type="collection" publication-format="electronic">
                        <year>202a</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = get_xml_tree(xml_str)
        obtained = dates.ArticleDatesValidation(xml_tree).validate_collection_date('2023')
        expected = [
            {
                'title': 'Collection pub-date validation',
                'xpath': './/front//pub-date[@date-type="collection"]',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'the publication date of the collection',
                'got_value': '202a',
                'message': 'Got 202a expected the publication date of the collection',
                'advice': 'Provide only numeric values for the collection year',
            }
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_collection_date_fail_number_of_digit(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
                    <article-id pub-id-type="other">00303</article-id>
                    <pub-date date-type="pub" publication-format="electronic">
                        <day>01</day>
                        <month>01</month>
                        <year>2023</year>
                    </pub-date>
                    <pub-date date-type="collection" publication-format="electronic">
                        <year>23</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = get_xml_tree(xml_str)
        obtained = dates.ArticleDatesValidation(xml_tree).validate_collection_date('2023')
        expected = [
            {
                'title': 'Collection pub-date validation',
                'xpath': './/front//pub-date[@date-type="collection"]',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'the publication date of the collection',
                'got_value': '23',
                'message': 'Got 23 expected the publication date of the collection',
                'advice': 'Provide a four-digit numeric value for the year of collection',
            }
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_collection_date_fail_out_of_range(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
                    <article-id pub-id-type="other">00303</article-id>
                    <pub-date date-type="pub" publication-format="electronic">
                        <day>01</day>
                        <month>01</month>
                        <year>2023</year>
                    </pub-date>
                    <pub-date date-type="collection" publication-format="electronic">
                        <year>2024</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = get_xml_tree(xml_str)
        obtained = dates.ArticleDatesValidation(xml_tree).validate_collection_date('2023')
        expected = [
            {
                'title': 'Collection pub-date validation',
                'xpath': './/front//pub-date[@date-type="collection"]',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'the publication date of the collection',
                'got_value': '2024',
                'message': 'Got 2024 expected the publication date of the collection',
                'advice': 'Provide a numeric value less than or equal to 2023',
            }
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_collection_date_fail_without_date(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
        article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
                    <article-id pub-id-type="other">00303</article-id>
                    <pub-date date-type="pub" publication-format="electronic">
                        <day>01</day>
                        <month>01</month>
                        <year>2023</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>
        """

        xml_tree = get_xml_tree(xml_str)
        obtained = dates.ArticleDatesValidation(xml_tree).validate_collection_date('2023')
        expected = [
            {
                'title': 'Collection pub-date validation',
                'xpath': './/front//pub-date[@date-type="collection"]',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'the publication date of the collection',
                'got_value': None,
                'message': 'Got None expected the publication date of the collection',
                'advice': 'Provide the publication date of the collection',
            }
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)
