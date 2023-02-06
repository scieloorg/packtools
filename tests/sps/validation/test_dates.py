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

