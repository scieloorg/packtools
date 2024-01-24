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
                            <date date-type="corrected">
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
                'expected_value': ['received', 'rev-request', 'rev-recd', 'accepted', 'corrected'],
                'got_value': ['received', 'rev-request', 'rev-recd', 'accepted', 'corrected'],
                'message': "Got [('received', '1998-01-05'), ('rev-request', '1998-03-14'), ('rev-recd', "
                           "'1998-05-24'), ('accepted', '1998-06-06'), ('corrected', '2012-06-01')]",
                'advice': None
            }
        ]
        obtained = dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "corrected"], ["received", "corrected"]
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_history_dates_fail_one_valid_date_not_required(self):
        self.maxDiff = None
        xml_history_date = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <history>
                            <date date-type="rev-request">
                                <day>14</day>
                                <month>03</month>
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
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': ['received', 'rev-request', 'corrected'],
                'got_value': ['rev-request'],
                'message': "Got [('rev-request', '1998-03-14')]",
                'advice': "Provide valid date for: ['received', 'corrected']"
            }
        ]
        obtained = dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "corrected"], ["received", "corrected"]
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_history_dates_success_required_date_only(self):
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
                            <date date-type="corrected">
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
                'expected_value': ['received', 'corrected'],
                'got_value': ['received', 'corrected'],
                'message': "Got [('received', '1998-01-05'), ('corrected', '2012-06-01')]",
                'advice': None
            }
        ]
        obtained = dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "corrected"], ["received", "corrected"]
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
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': ['received', 'rev-request', 'rev-recd', 'accepted', 'corrected'],
                'got_value': ['received', 'rev-request', 'rev-recd', 'accepted'],
                'message': "Got [('received', '1998-01-05'), ('rev-request', '1998-03-14'), ('rev-recd', "
                           "'1998-05-24'), ('accepted', '1998-06-06')]",
                'advice': "Provide valid date for: ['corrected']",
            }
        ]
        obtained = dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "corrected"], ["received", "corrected"]
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
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': ['received', 'rev-request', 'rev-recd', 'accepted', 'corrected'],
                'got_value': ['received', 'rev-request', 'rev-recd', 'accepted', 'unknown'],
                'message': "Got [('received', '1998-01-05'), ('rev-request', '1998-03-14'), ('rev-recd', '1998-05-24'),"
                           " ('accepted', '1998-06-06'), ('unknown', '2012-06-01')]",
                'advice': "Provide ordering of events valid date for: ['corrected'] removal of events: ['unknown']",
            }
        ]
        obtained = dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "corrected"], ["received", "corrected"]
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_history_dates_fail_one_date_element_is_missing(self):
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
                                <date date-type="corrected">
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
                'response': 'ERROR',
                'expected_value': ['received', 'accepted', 'corrected'],
                'got_value': ['accepted', 'corrected'],
                'message': "Got [('accepted', '1998-06-06'), ('corrected', '2012-06-01')]",
                'advice': "Provide valid date for: ['received']",
            },
        ]
        obtained = dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "corrected"], ["received", "corrected"]
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_history_dates_fail_one_date_element_is_invalid(self):
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
                                <date date-type="corrected">
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
                'expected_value': ['received', 'accepted', 'corrected'],
                'got_value': ['received', 'accepted', 'corrected'],
                'message': "Got [('received', '1998-01-05'), ('accepted', '1998-06-06'), ('corrected', '2012-06-01')]",
                'advice': None
            },
        ]
        obtained = dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "corrected"], ["received", "corrected"]
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
                                <date date-type="corrected">
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
                'expected_value': ['received', 'rev-request', 'rev-recd', 'accepted', 'corrected'],
                'got_value': ['rev-request', 'received', 'rev-recd', 'accepted', 'corrected'],
                'message': "Got [('rev-request', '1998-01-04'), ('received', '1998-01-05'), ('rev-recd', '1998-05-24'),"
                           " ('accepted', '1998-06-06'), ('corrected', '2012-06-01')]",
                'advice': 'Provide ordering of events',
            }
        ]
        obtained = dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "corrected"], ["received", "corrected"]
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
                                <date date-type="corrected">
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
                'expected_value': ['received', 'rev-request', 'rev-recd', 'accepted', 'corrected'],
                'got_value': ['received', 'rev-request', 'rev-recd', 'corrected'],
                'message': "Got [('received', '1998-01-05'), ('rev-request', '1998-03-14'), ('rev-recd', '1998-05-24'),"
                           " ('corrected', '2012-06-01')]",
                'advice': "Provide valid date for: ['accepted']",
            }
        ]
        obtained = dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "corrected"], ["accepted", "corrected"]
        )
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_date_is_complete_a_date_with_missing_year(self):
        _date = dict(month='02', day='05')
        expected = (False, 'a valid date for pub-date', '-02-05', 'pub-date must be complete', "Provide 'year' of the date")
        obtained = dates._date_is_complete(_date, 'pub-date')

        self.assertEqual(expected, obtained)

    def test_date_is_complete_a_date_with_missing_month(self):
        _date = dict(year='2023', day='5')
        expected = (False, 'a valid date for pub-date', '2023--5', 'pub-date must be complete', "Provide 'month' of the date")
        obtained = dates._date_is_complete(_date, 'pub-date')

        self.assertEqual(expected, obtained)

    def test_date_is_complete_a_date_with_missing_day(self):
        _date = dict(year='2023', month='2')
        expected = (False, 'a valid date for pub-date', '2023-2-', 'pub-date must be complete', "Provide 'day' of the date")
        obtained = dates._date_is_complete(_date, 'pub-date')
        self.assertEqual(expected, obtained)

    def test_date_is_complete_a_date_with_invalid_year(self):
        _date = dict(year='', month='2', day='5')
        expected = (False, 'a valid date for pub-date', '-2-5',
                    'pub-date must contain valid values, invalid literal for int() with base 10: \'\',',
                    'Provide valid values for day, month and year')
        obtained = dates._date_is_complete(_date, 'pub-date')
        self.assertEqual(expected, obtained)

    def test_date_is_complete_a_date_with_invalid_month(self):
        _date = dict(year='2023', month='o3', day='5')
        expected = (False, 'a valid date for pub-date', '2023-o3-5',
                    'pub-date must contain valid values, invalid literal for int() with base 10: \'o3\',',
                    'Provide valid values for day, month and year')
        obtained = dates._date_is_complete(_date, 'pub-date')
        self.assertEqual(expected, obtained)

    def test_date_is_complete_a_date_with_invalid_day(self):
        _date = dict(year='2023', month='3', day='1o')
        expected = (False, 'a valid date for pub-date', '2023-3-1o',
                    'pub-date must contain valid values, invalid literal for int() with base 10: \'1o\',',
                    'Provide valid values for day, month and year')
        obtained = dates._date_is_complete(_date, 'pub-date')
        self.assertEqual(expected, obtained)

    def test_date_is_complete_a_date_with_invalid_day_number(self):
        _date = dict(year='2023', month='3', day='45')
        expected = (False, 'a valid date for pub-date', '2023-3-45',
                    'pub-date must contain valid values',
                    'Provide valid values for day, month and year')
        obtained = dates._date_is_complete(_date, 'pub-date')
        self.assertEqual(expected, obtained)

    def test_date_is_complete_a_date_with_invalid_month_number(self):
        _date = dict(year='2023', month='13', day='15')
        expected = (False, 'a valid date for pub-date', '2023-13-15',
                    'pub-date must contain valid values',
                    'Provide valid values for day, month and year')
        obtained = dates._date_is_complete(_date, 'pub-date')
        self.assertEqual(expected, obtained)

    def test_date_is_complete_a_date_with_invalid_year_number(self):
        _date = dict(year='-10', month='10', day='15')
        expected = (False, 'a valid date for pub-date', '-10-10-15',
                    'pub-date must contain valid values',
                    'Provide valid values for day, month and year')
        obtained = dates._date_is_complete(_date, 'pub-date')
        self.assertEqual(expected, obtained)

    def test_date_is_complete_a_correct_date(self):
        _date = dict(year='2023', month='10', day='15')
        expected = (True, '2023-10-15', '2023-10-15', None, None)
        obtained = dates._date_is_complete(_date, 'pub-date')
        self.assertEqual(expected, obtained)

    def test_check_order(self):
        expected = [True, True, True, False, False]
        obtained = []

        order = ["received", "rev-request", "rev-recd", "accepted", "corrected"]
        for seq in [
            ["received", "corrected"],
            ["received", "rev-recd", "accepted"],
            ["rev-request", "rev-recd", "corrected"],
            ["rev-request", "rev-recd", "received", "accepted", "corrected"],
            ["accepted", "received"]
        ]:
            obtained.append(dates.is_subsequence_in_order(seq, order))

        self.assertEqual(expected, obtained)


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
