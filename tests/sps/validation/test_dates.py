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


