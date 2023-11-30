from unittest import TestCase
from datetime import date
from lxml import etree

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation import dates


class IsCompleteDateTest(TestCase):
    def test_is_complete_a_date_with_missing_year(self):
        _date = dict(
            month='2',
            day='5',
        )
        expected = dict(
            input=_date,
            result='error',
            message="pub-date must be complete. Provide 'year' of the date.",
            element='year',
        )
        obtained = dates.is_complete(_date, 'pub-date')
        self.assertDictEqual(expected, obtained)

    def test_is_complete_a_date_with_missing_month(self):
        _date = dict(
            year='2023',
            day='5',
        )
        expected = dict(
            input=_date,
            result='error',
            message="pub-date must be complete. Provide 'month' of the date.",
            element='month',
        )
        obtained = dates.is_complete(_date, 'pub-date')
        self.assertDictEqual(expected, obtained)

    def test_is_complete_a_date_with_missing_day(self):
        _date = dict(
            year='2023',
            month='2',
        )
        expected = dict(
            input=_date,
            result='error',
            message="pub-date must be complete. Provide 'day' of the date.",
            element='day',
        )
        obtained = dates.is_complete(_date, 'pub-date')
        self.assertDictEqual(expected, obtained)

    def test_is_complete_a_date_with_invalid_year(self):
        _date = dict(
            year='',
            month='2',
            day='5',
        )
        expected = dict(
            input=_date,
            result='error',
            message="pub-date must contain valid values, enter valid values for day, month and year",
            element='pub-date',
        )
        obtained = dates.is_complete(_date, 'pub-date')
        self.assertDictEqual(expected, obtained)

    def test_is_complete_a_date_with_invalid_month(self):
        _date = dict(
            year='2023',
            month='o3',
            day='5',
        )
        expected = dict(
            input=_date,
            result='error',
            message="pub-date must contain valid values, enter valid values for day, month and year",
            element='pub-date',
        )
        obtained = dates.is_complete(_date, 'pub-date')
        self.assertDictEqual(expected, obtained)

    def test_is_complete_a_date_with_invalid_day(self):
        _date = dict(
            year='2023',
            month='3',
            day='1o',
        )
        expected = dict(
            input=_date,
            result='error',
            message="pub-date must contain valid values, enter valid values for day, month and year",
            element='pub-date',
        )
        obtained = dates.is_complete(_date, 'pub-date')
        self.assertDictEqual(expected, obtained)

    def test_is_complete_a_date_with_invalid_day_number(self):
        _date = dict(
            year='2023',
            month='3',
            day='45',
        )
        expected = dict(
            input=_date,
            result='error',
            message="pub-date must contain valid values, day is out of range for month, "
                    "enter valid values for day, month and year",
            element='pub-date',
        )
        obtained = dates.is_complete(_date, 'pub-date')
        self.assertDictEqual(expected, obtained)

    def test_is_complete_a_date_with_invalid_month_number(self):
        _date = dict(
            year='2023',
            month='13',
            day='15',
        )
        expected = dict(
            input=_date,
            result='error',
            message="pub-date must contain valid values, month must be in 1..12, "
                    "enter valid values for day, month and year",
            element='pub-date',
        )
        obtained = dates.is_complete(_date, 'pub-date')
        self.assertDictEqual(expected, obtained)

    def test_is_complete_a_date_with_invalid_year_number(self):
        _date = dict(
            year='-10',
            month='10',
            day='15',
        )
        expected = dict(
            input=_date,
            result='error',
            message="pub-date must contain valid values, year -10 is out of range, "
                    "enter valid values for day, month and year",
            element='pub-date',
        )
        obtained = dates.is_complete(_date, 'pub-date')
        self.assertDictEqual(expected, obtained)

    def test_is_complete_a_correct_date(self):
        _date = dict(
            year='2023',
            month='10',
            day='15',
        )
        expected = dict(
            input=_date,
            result='ok',
            element='pub-date',
            object_date=date(2023, 10, 15),
        )
        obtained = dates.is_complete(_date, 'pub-date')
        self.assertDictEqual(expected, obtained)


class IsSortedHistoryDateTest(TestCase):
    def test_is_sorted_a_sorted_date_list(self):
        xml_history_date = etree.fromstring("""
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>20</day>
                            <month>04</month>
                            <year>2022</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2003</year>
                        </pub-date>
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
            """)
        expected = {
            'input': {
                'order_of_events': ["received", "rev-request", "rev-recd", "accepted", "approved"],
                'required_events': ["received", "approved"],
                'events_date': {
                    'received': {'type': 'received', 'year': '1998', 'month': '01', 'day': '05'},
                    'rev-request': {'type': 'rev-request', 'year': '1998', 'month': '03', 'day': '14'},
                    'rev-recd': {'type': 'rev-recd', 'year': '1998', 'month': '05', 'day': '24'},
                    'accepted': {'type': 'accepted', 'year': '1998', 'month': '06', 'day': '06'},
                    'approved': {'type': 'approved', 'year': '2012', 'month': '06', 'day': '01'}
                }
            },
            'message': [],
            'result': 'ok',
            'expected_order': [date(1998, 1, 5), date(1998, 3, 14), date(1998, 5, 24), date(1998, 6, 6), date(2012, 6, 1)],
            'found_order': [date(1998, 1, 5), date(1998, 3, 14), date(1998, 5, 24), date(1998, 6, 6), date(2012, 6, 1)]
        }
        obtained = dates.ArticleDatesValidation(xml_history_date).history_dates_are_sorted(
            ["received", "rev-request", "rev-recd", "accepted", "approved"], ["received", "approved"]
        )
        self.assertDictEqual(expected, obtained)

    def test_is_sorted_a_unsorted_date_list(self):
        xml_history_date = etree.fromstring("""
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <pub-date publication-format="electronic" date-type="pub">
                        <day>20</day>
                        <month>04</month>
                        <year>2022</year>
                    </pub-date>
                    <pub-date publication-format="electronic" date-type="collection">
                        <year>2003</year>
                    </pub-date>
                    <history>
                        <date date-type="received">
                            <day>05</day>
                            <month>01</month>
                            <year>1999</year>
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
        """)
        expected = {
            'input': {
                'order_of_events': ["received", "rev-request", "rev-recd", "accepted", "approved"],
                'required_events': ["received", "approved"],
                'events_date': {
                    'received': {'type': 'received', 'year': '1999', 'month': '01', 'day': '05'},
                    'rev-request': {'type': 'rev-request', 'year': '1998', 'month': '03', 'day': '14'},
                    'rev-recd': {'type': 'rev-recd', 'year': '1998', 'month': '05', 'day': '24'},
                    'accepted': {'type': 'accepted', 'year': '1998', 'month': '06', 'day': '06'},
                    'approved': {'type': 'approved', 'year': '2012', 'month': '06', 'day': '01'}
                }
            },
            'message': [],
            'result': 'error',
            'expected_order': [date(1998, 3, 14), date(1998, 5, 24), date(1998, 6, 6), date(1999, 1, 5), date(2012, 6, 1)],
            'found_order': [date(1999, 1, 5), date(1998, 3, 14), date(1998, 5, 24), date(1998, 6, 6), date(2012, 6, 1)]
        }
        obtained = dates.ArticleDatesValidation(xml_history_date).history_dates_are_sorted(
            ["received", "rev-request", "rev-recd", "accepted", "approved"], ["received", "approved"]
        )
        self.assertDictEqual(expected, obtained)

    def test_is_sorted_a_date_list_without_one_date_required(self):
        xml_history_date = etree.fromstring("""
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <pub-date publication-format="electronic" date-type="pub">
                        <day>20</day>
                        <month>04</month>
                        <year>2022</year>
                    </pub-date>
                    <pub-date publication-format="electronic" date-type="collection">
                        <year>2003</year>
                    </pub-date>
                    <history>
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
        """)
        expected = {
            'input': {
                'order_of_events': ["received", "rev-request", "rev-recd", "accepted", "approved"],
                'required_events': ["received", "approved"],
                'events_date': {
                    'rev-request': {'type': 'rev-request', 'year': '1998', 'month': '03', 'day': '14'},
                    'rev-recd': {'type': 'rev-recd', 'year': '1998', 'month': '05', 'day': '24'},
                    'accepted': {'type': 'accepted', 'year': '1998', 'month': '06', 'day': '06'},
                    'approved': {'type': 'approved', 'year': '2012', 'month': '06', 'day': '01'}
                }
            },
            'message': ['the event received is required'],
            'result': 'error',
            'expected_order': [date(1998, 3, 14), date(1998, 5, 24), date(1998, 6, 6), date(2012, 6, 1)],
            'found_order': [date(1998, 3, 14), date(1998, 5, 24), date(1998, 6, 6), date(2012, 6, 1)]
        }
        obtained = dates.ArticleDatesValidation(xml_history_date).history_dates_are_sorted(
            ["received", "rev-request", "rev-recd", "accepted", "approved"], ["received", "approved"]
        )
        self.assertDictEqual(expected, obtained)

    def test_is_sorted_a_complete_date_list(self):
        xml_history_date = etree.fromstring("""
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>20</day>
                            <month>04</month>
                            <year>2022</year>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2003</year>
                        </pub-date>
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
            """)
        expected = [
            {'input': {'year': '1998', 'month': '01', 'day': '05', 'type': 'received'},
             'result': 'ok',
             'element': 'received',
             'object_date': date(1998, 1, 5)},
            {'input': {'year': '1998', 'month': '03', 'day': '14', 'type': 'rev-request'},
             'result': 'ok',
             'element': 'rev-request',
             'object_date': date(1998, 3, 14)},
            {'input': {'year': '1998', 'month': '05', 'day': '24', 'type': 'rev-recd'},
             'result': 'ok',
             'element': 'rev-recd',
             'object_date': date(1998, 5, 24)},
            {'input': {'year': '1998', 'month': '06', 'day': '06', 'type': 'accepted'},
             'result': 'ok',
             'element': 'accepted',
             'object_date': date(1998, 6, 6)},
            {'input': {'year': '2012', 'month': '06', 'day': '01', 'type': 'approved'},
             'result': 'ok',
             'element': 'approved',
             'object_date': date(2012, 6, 1)},
        ]
        obtained = dates.ArticleDatesValidation(xml_history_date).history_dates_are_complete()
        self.assertEqual(expected, obtained)

    def test_is_sorted_a_incomplete_date_list(self):
        xml_history_date = etree.fromstring("""
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <pub-date publication-format="electronic" date-type="pub">
                            <day>20</day>
                            <month>04</month>
                        </pub-date>
                        <pub-date publication-format="electronic" date-type="collection">
                            <year>2003</year>
                        </pub-date>
                        <history>
                            <date date-type="received">
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
            """)
        expected = [
            {'input': {'year': '1998', 'month': '01', 'type': 'received'},
             'result': 'error',
             'element': 'day',
             'message': "received must be complete. Provide 'day' of the date."},
            {'input': {'year': '1998', 'month': '03', 'day': '14', 'type': 'rev-request'},
             'result': 'ok',
             'element': 'rev-request',
             'object_date': date(1998, 3, 14)},
            {'input': {'year': '1998', 'month': '05', 'day': '24', 'type': 'rev-recd'},
             'result': 'ok',
             'element': 'rev-recd',
             'object_date': date(1998, 5, 24)},
            {'input': {'year': '1998', 'month': '06', 'day': '06', 'type': 'accepted'},
             'result': 'ok',
             'element': 'accepted',
             'object_date': date(1998, 6, 6)},
            {'input': {'year': '2012', 'month': '06', 'day': '01', 'type': 'approved'},
             'result': 'ok',
             'element': 'approved',
             'object_date': date(2012, 6, 1)}
        ]
        obtained = dates.ArticleDatesValidation(xml_history_date).history_dates_are_complete()
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
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type:pub]',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '03',
                'got_value': '03',
                'message': 'Got 2 expected 2 numeric digits',
                'advice': None
            },
            {
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type:pub]',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '02',
                'got_value': '02',
                'message': 'Got 2 expected 2 numeric digits',
                'advice': None
            },
            {
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type:pub]',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '2024',
                'got_value': '2024',
                'message': 'Got 4 expected 4 numeric digits',
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
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type:pub]',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '03',
                'got_value': '03',
                'message': 'Got 2 expected 2 numeric digits',
                'advice': None
            },
            {
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type:pub]',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '02',
                'got_value': '02',
                'message': 'Got 2 expected 2 numeric digits',
                'advice': None
            },
            {
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type:pub]',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': '0202',
                'got_value': '202',
                'message': 'Got 3 expected 4 numeric digits',
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
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type:pub]',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '03',
                'got_value': '03',
                'message': 'Got 2 expected 2 numeric digits',
                'advice': None
            },
            {
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type:pub]',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': '02',
                'got_value': '2',
                'message': 'Got 1 expected 2 numeric digits',
                'advice': 'Provide a 2-digit numeric value for month'
            },
            {
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type:pub]',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '2024',
                'got_value': '2024',
                'message': 'Got 4 expected 4 numeric digits',
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
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type:pub]',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': '03',
                'got_value': '3',
                'message': 'Got 1 expected 2 numeric digits',
                'advice': 'Provide a 2-digit numeric value for day'
            },
            {
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type:pub]',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '02',
                'got_value': '02',
                'message': 'Got 2 expected 2 numeric digits',
                'advice': None
            },
            {
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type:pub]',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '2024',
                'got_value': '2024',
                'message': 'Got 4 expected 4 numeric digits',
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
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type:pub]',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'A numeric digit for day represented with 2 digits',
                'got_value': 'dd',
                'message': 'Got a non-numeric value for day',
                'advice': 'Provide a 2-digit numeric value for day'
            },
            {
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type:pub]',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'A numeric digit for month represented with 2 digits',
                'got_value': 'mm',
                'message': 'Got a non-numeric value for month',
                'advice': 'Provide a 2-digit numeric value for month'
            },
            {
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type:pub]',
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
        obtained = dates.ArticleDatesValidation(xml_tree).validate_article_date(2023, 12, 12)
        expected = {
                'title': 'Article pub-date validation',
                'xpath': './/front//pub-date[@date-type:pub]',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': 'A date in the format: YYYY-MM-DD',
                'got_value': '2023-01-01',
                'message': '2023-01-01 is an valid date',
                'advice': None
            }
        self.assertDictEqual(expected, obtained)

                'response': 'ERROR',
                'expected_value': 'A date in the format: YYYY-MM-DD',
                'got_value': '202-0-32',
                'message': '202-0-32 is an invalid date',
                'advice': 'Fix the following issue on the given date: month must be in 1..12'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)
