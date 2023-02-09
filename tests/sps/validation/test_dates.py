from unittest import TestCase
from datetime import date
from lxml import etree

from packtools.sps.validation import dates
from packtools.sps.utils.xml_utils import get_xml_tree


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
                'events_date': [
                    {'received': date(1998, 1, 5)},
                    {'rev-request': date(1998, 3, 14)},
                    {'rev-recd': date(1998, 5, 24)},
                    {'accepted': date(1998, 6, 6)},
                    {'approved': date(2012, 6, 1)}
                ]
            },
            'message': [],
            'result': 'ok',
            'expected_order': [date(1998, 1, 5), date(1998, 3, 14), date(1998, 5, 24), date(1998, 6, 6), date(2012, 6, 1)],
            'found_order': [date(1998, 1, 5), date(1998, 3, 14), date(1998, 5, 24), date(1998, 6, 6), date(2012, 6, 1)]
        }
        obtained = dates.ArticleDatesValidator(xml_history_date).history_dates_are_sorted(
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
                'events_date': [
                    {'received': date(1999, 1, 5)},
                    {'rev-request': date(1998, 3, 14)},
                    {'rev-recd': date(1998, 5, 24)},
                    {'accepted': date(1998, 6, 6)},
                    {'approved': date(2012, 6, 1)}
                ]
            },
            'message': [],
            'result': 'error',
            'expected_order': [date(1998, 3, 14), date(1998, 5, 24), date(1998, 6, 6), date(1999, 1, 5), date(2012, 6, 1)],
            'found_order': [date(1999, 1, 5), date(1998, 3, 14), date(1998, 5, 24), date(1998, 6, 6), date(2012, 6, 1)]
        }
        obtained = dates.ArticleDatesValidator(xml_history_date).history_dates_are_sorted(
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
                'events_date': [
                    {'rev-request': date(1998, 3, 14)},
                    {'rev-recd': date(1998, 5, 24)},
                    {'accepted': date(1998, 6, 6)},
                    {'approved': date(2012, 6, 1)}
                ]
            },
            'message': ['the event received is required'],
            'result': 'error',
            'expected_order': [date(1998, 3, 14), date(1998, 5, 24), date(1998, 6, 6), date(2012, 6, 1)],
            'found_order': [date(1998, 3, 14), date(1998, 5, 24), date(1998, 6, 6), date(2012, 6, 1)]
        }
        obtained = dates.ArticleDatesValidator(xml_history_date).history_dates_are_sorted(
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
        obtained = dates.ArticleDatesValidator(xml_history_date).history_dates_are_complete()
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
        obtained = dates.ArticleDatesValidator(xml_history_date).history_dates_are_complete()
        self.assertEqual(expected, obtained)
