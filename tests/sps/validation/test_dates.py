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
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'history',
                'sub_item': 'date',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': ['received', 'rev-request', 'rev-recd', 'accepted', 'corrected'],
                'got_value': ['received', 'rev-request', 'rev-recd', 'accepted', 'corrected'],
                'message': "Got ['received', 'rev-request', 'rev-recd', 'accepted', 'corrected'], expected ["
                           "'received', 'rev-request', 'rev-recd', 'accepted', 'corrected']",
                'advice': None,
                'data': {
                    'article_date': None,
                    'collection_date': None,
                    'history': {
                        'received': {
                            'day': '05',
                            'month': '01',
                            'type': 'received',
                            'year': '1998'
                        },
                        'rev-request': {
                            'day': '14',
                            'month': '03',
                            'type': 'rev-request',
                            'year': '1998'
                        },
                        'rev-recd': {
                            'day': '24',
                            'month': '05',
                            'type': 'rev-recd',
                            'year': '1998'
                        },
                        'accepted': {
                            'day': '06',
                            'month': '06',
                            'type': 'accepted',
                            'year': '1998'
                        },
                        'corrected': {
                            'day': '01',
                            'month': '06',
                            'type': 'corrected',
                            'year': '2012'
                        }
                    },
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en'
                },
            }
        ]
        obtained = list(dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "corrected"], ["received", "corrected"]
        ))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

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
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'history',
                'sub_item': 'date',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': ['received', 'rev-request', 'corrected'],
                'got_value': ['rev-request'],
                'message': "Got ['rev-request'], expected ['received', 'rev-request', 'corrected']",
                'advice': "Provide: valid date for ['received', 'corrected'];",
                'data': {
                    'article_date': None,
                    'collection_date': None,
                    'history': {
                        'rev-request': {
                            'day': '14',
                            'month': '03',
                            'type': 'rev-request',
                            'year': '1998'
                        }
                    },
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en'
                },
            }
        ]
        obtained = list(dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "corrected"], ["received", "corrected"]
        ))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

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
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'history',
                'sub_item': 'date',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': ['received', 'corrected'],
                'got_value': ['received', 'corrected'],
                'message': "Got ['received', 'corrected'], expected ['received', 'corrected']",
                'advice': None,
                'data': {
                    'article_date': None,
                    'collection_date': None,
                    'history': {
                        'corrected': {
                            'day': '01',
                            'month': '06',
                            'type': 'corrected',
                            'year': '2012'
                        },
                        'received': {
                            'day': '05',
                            'month': '01',
                            'type': 'received',
                            'year': '1998'
                        }
                    },
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en'
                },
            }
        ]
        obtained = list(dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "corrected"], ["received", "corrected"]
        ))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

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
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'history',
                'sub_item': 'date',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': ["received", "rev-request", "rev-recd", "accepted", "corrected"],
                'got_value': ['received', 'rev-request', 'rev-recd', 'accepted'],
                'message': "Got ['received', 'rev-request', 'rev-recd', 'accepted'], expected ['received', "
                           "'rev-request', 'rev-recd', 'accepted', 'corrected']",
                'advice': "Provide: valid date for ['corrected'];",
                'data': {
                    'article_date': None,
                    'collection_date': None,
                    'history': {
                        'received': {
                            'day': '05',
                            'month': '01',
                            'type': 'received',
                            'year': '1998'
                        },
                        'rev-request': {
                            'day': '14',
                            'month': '03',
                            'type': 'rev-request',
                            'year': '1998'
                        },
                        'rev-recd': {
                            'day': '24',
                            'month': '05',
                            'type': 'rev-recd',
                            'year': '1998'
                        },
                        'accepted': {
                            'day': '06',
                            'month': '06',
                            'type': 'accepted',
                            'year': '1998'
                        },
                    },
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en'
                },
            }
        ]
        obtained = list(dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "corrected"], ["received", "corrected"]
        ))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

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
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'history',
                'sub_item': 'date',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': ['received', 'rev-request', 'rev-recd', 'accepted', 'corrected'],
                'got_value': ['received', 'rev-request', 'rev-recd', 'accepted', 'unknown'],
                'message': "Got ['received', 'rev-request', 'rev-recd', 'accepted', 'unknown'], expected ["
                           "'received', 'rev-request', 'rev-recd', 'accepted', 'corrected']",
                'advice': "Provide: the dates of ['received', 'rev-request', 'rev-recd', 'accepted', 'corrected'] in "
                          "chronological order; valid date for ['corrected']; removal of events ['unknown'];",
                'data': {
                    'article_date': None,
                    'collection_date': None,
                    'history': {
                        'received': {
                            'day': '05',
                            'month': '01',
                            'type': 'received',
                            'year': '1998'
                        },
                        'rev-request': {
                            'day': '14',
                            'month': '03',
                            'type': 'rev-request',
                            'year': '1998'
                        },
                        'rev-recd': {
                            'day': '24',
                            'month': '05',
                            'type': 'rev-recd',
                            'year': '1998'
                        },
                        'accepted': {
                            'day': '06',
                            'month': '06',
                            'type': 'accepted',
                            'year': '1998'
                        },
                        'unknown': {
                            'day': '01',
                            'month': '06',
                            'type': 'unknown',
                            'year': '2012'
                        }
                    },
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en'
                },
            }
        ]
        obtained = list(dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "corrected"], ["received", "corrected"]
        ))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

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
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'history',
                'sub_item': 'date',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a valid date for received',
                'got_value': '1998-01-',
                'message': 'Got 1998-01-, expected a valid date for received',
                'advice': "Provide 'day' of the date",
                'data': {
                    'article_date': None,
                    'collection_date': None,
                    'history': {
                        'received': {
                            'month': '01',
                            'type': 'received',
                            'year': '1998'
                        },
                        'rev-request': {
                            'day': '14',
                            'type': 'rev-request',
                            'year': '1998'
                        },
                        'rev-recd': {
                            'day': '24',
                            'month': '05',
                            'type': 'rev-recd'
                        },
                        'accepted': {
                            'day': '06',
                            'month': '06',
                            'type': 'accepted',
                            'year': '1998'
                        },
                        'corrected': {
                            'day': '01',
                            'month': '06',
                            'type': 'corrected',
                            'year': '2012'
                        }
                    },
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en'
                },
            },
            {
                'title': 'History date validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'history',
                'sub_item': 'date',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a valid date for rev-request',
                'got_value': '1998--14',
                'message': 'Got 1998--14, expected a valid date for rev-request',
                'advice': "Provide 'month' of the date",
                'data': {
                    'article_date': None,
                    'collection_date': None,
                    'history': {
                        'received': {
                            'month': '01',
                            'type': 'received',
                            'year': '1998'
                        },
                        'rev-request': {
                            'day': '14',
                            'type': 'rev-request',
                            'year': '1998'
                        },
                        'rev-recd': {
                            'day': '24',
                            'month': '05',
                            'type': 'rev-recd'
                        },
                        'accepted': {
                            'day': '06',
                            'month': '06',
                            'type': 'accepted',
                            'year': '1998'
                        },
                        'corrected': {
                            'day': '01',
                            'month': '06',
                            'type': 'corrected',
                            'year': '2012'
                        }
                    },
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en'
                },
            },
            {
                'title': 'History date validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'history',
                'sub_item': 'date',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a valid date for rev-recd',
                'got_value': '-05-24',
                'message': 'Got -05-24, expected a valid date for rev-recd',
                'advice': "Provide 'year' of the date",
                'data': {
                    'article_date': None,
                    'collection_date': None,
                    'history': {
                        'received': {
                            'month': '01',
                            'type': 'received',
                            'year': '1998'
                        },
                        'rev-request': {
                            'day': '14',
                            'type': 'rev-request',
                            'year': '1998'
                        },
                        'rev-recd': {
                            'day': '24',
                            'month': '05',
                            'type': 'rev-recd'
                        },
                        'accepted': {
                            'day': '06',
                            'month': '06',
                            'type': 'accepted',
                            'year': '1998'
                        },
                        'corrected': {
                            'day': '01',
                            'month': '06',
                            'type': 'corrected',
                            'year': '2012'
                        }
                    },
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en'
                },
            },
            {
                'title': 'History date validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'history',
                'sub_item': 'date',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': ['received', 'accepted', 'corrected'],
                'got_value': ['accepted', 'corrected'],
                'message': "Got ['accepted', 'corrected'], expected ['received', 'accepted', 'corrected']",
                'advice': "Provide: valid date for ['received'];",
                'data': {
                    'article_date': None,
                    'collection_date': None,
                    'history': {
                        'received': {
                            'month': '01',
                            'type': 'received',
                            'year': '1998'
                        },
                        'rev-request': {
                            'day': '14',
                            'type': 'rev-request',
                            'year': '1998'
                        },
                        'rev-recd': {
                            'day': '24',
                            'month': '05',
                            'type': 'rev-recd'
                        },
                        'accepted': {
                            'day': '06',
                            'month': '06',
                            'type': 'accepted',
                            'year': '1998'
                        },
                        'corrected': {
                            'day': '01',
                            'month': '06',
                            'type': 'corrected',
                            'year': '2012'
                        }
                    },
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en'
                },
            },
        ]
        obtained = list(dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "corrected"], ["received", "corrected"]
        ))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

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
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'history',
                'sub_item': 'date',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a valid date for rev-request',
                'got_value': '1998-03-40',
                'message': 'Got 1998-03-40, expected a valid date for rev-request',
                'advice': 'Provide valid values for day, month and year',
                'data': {
                    'article_date': None,
                    'collection_date': None,
                    'history': {
                        'received': {
                            'day': '05',
                            'month': '01',
                            'type': 'received',
                            'year': '1998'
                        },
                        'rev-request': {
                            'day': '40',
                            'month': '03',
                            'type': 'rev-request',
                            'year': '1998'
                        },
                        'rev-recd': {
                            'day': '24',
                            'month': '13',
                            'year': '1998',
                            'type': 'rev-recd'
                        },
                        'accepted': {
                            'day': '06',
                            'month': '06',
                            'type': 'accepted',
                            'year': '1998'
                        },
                        'corrected': {
                            'day': '01',
                            'month': '06',
                            'type': 'corrected',
                            'year': '2012'
                        }
                    },
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en'
                },
            },
            {
                'title': 'History date validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'history',
                'sub_item': 'date',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a valid date for rev-recd',
                'got_value': '1998-13-24',
                'message': 'Got 1998-13-24, expected a valid date for rev-recd',
                'advice': 'Provide valid values for day, month and year',
                'data': {
                    'article_date': None,
                    'collection_date': None,
                    'history': {
                        'received': {
                            'day': '05',
                            'month': '01',
                            'type': 'received',
                            'year': '1998'
                        },
                        'rev-request': {
                            'day': '40',
                            'month': '03',
                            'type': 'rev-request',
                            'year': '1998'
                        },
                        'rev-recd': {
                            'day': '24',
                            'month': '13',
                            'year': '1998',
                            'type': 'rev-recd'
                        },
                        'accepted': {
                            'day': '06',
                            'month': '06',
                            'type': 'accepted',
                            'year': '1998'
                        },
                        'corrected': {
                            'day': '01',
                            'month': '06',
                            'type': 'corrected',
                            'year': '2012'
                        }
                    },
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en'
                },
            },
            {
                'title': 'History date validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'history',
                'sub_item': 'date',
                'validation_type': 'value',
                'response': 'OK',
                'expected_value': ['received', 'accepted', 'corrected'],
                'got_value': ['received', 'accepted', 'corrected'],
                'message': "Got ['received', 'accepted', 'corrected'], expected ['received', 'accepted', 'corrected']",
                'advice': None,
                'data': {
                    'article_date': None,
                    'collection_date': None,
                    'history': {
                        'received': {
                            'day': '05',
                            'month': '01',
                            'type': 'received',
                            'year': '1998'
                        },
                        'rev-request': {
                            'day': '40',
                            'month': '03',
                            'type': 'rev-request',
                            'year': '1998'
                        },
                        'rev-recd': {
                            'day': '24',
                            'month': '13',
                            'year': '1998',
                            'type': 'rev-recd'
                        },
                        'accepted': {
                            'day': '06',
                            'month': '06',
                            'type': 'accepted',
                            'year': '1998'
                        },
                        'corrected': {
                            'day': '01',
                            'month': '06',
                            'type': 'corrected',
                            'year': '2012'
                        }
                    },
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en'
                },
            },
        ]
        obtained = list(dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "corrected"], ["received", "corrected"]
        ))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

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
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'history',
                'sub_item': 'date',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': ["received", "rev-request", "rev-recd", "accepted", "corrected"],
                'got_value': ['rev-request', 'received', 'rev-recd', 'accepted', 'corrected'],
                'message': "Got ['rev-request', 'received', 'rev-recd', 'accepted', 'corrected'], expected ["
                           "'received', 'rev-request', 'rev-recd', 'accepted', 'corrected']",
                'advice': "Provide: the dates of ['received', 'rev-request', 'rev-recd', 'accepted', 'corrected'] in "
                          "chronological order;",
                'data': {
                    'article_date': None,
                    'collection_date': None,
                    'history': {
                        'received': {
                            'day': '05',
                            'month': '01',
                            'type': 'received',
                            'year': '1998'
                        },
                        'rev-request': {
                            'day': '04',
                            'month': '01',
                            'type': 'rev-request',
                            'year': '1998'
                        },
                        'rev-recd': {
                            'day': '24',
                            'month': '05',
                            'type': 'rev-recd',
                            'year': '1998'
                        },
                        'accepted': {
                            'day': '06',
                            'month': '06',
                            'type': 'accepted',
                            'year': '1998'
                        },
                        'corrected': {
                            'day': '01',
                            'month': '06',
                            'type': 'corrected',
                            'year': '2012'
                        }
                    },
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en'
                },
            }
        ]
        obtained = list(dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "corrected"], ["received", "corrected"]
        ))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

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
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'history',
                'sub_item': 'date',
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': ['received', 'rev-request', 'rev-recd', 'accepted', 'corrected'],
                'got_value': ['received', 'rev-request', 'rev-recd', 'corrected'],
                'message': "Got ['received', 'rev-request', 'rev-recd', 'corrected'], expected ['received', "
                           "'rev-request', 'rev-recd', 'accepted', 'corrected']",

                'advice': "Provide: valid date for ['accepted'];",
                'data': {
                    'article_date': None,
                    'collection_date': None,
                    'history': {
                        'received': {
                            'day': '05',
                            'month': '01',
                            'type': 'received',
                            'year': '1998'
                        },
                        'rev-request': {
                            'day': '14',
                            'month': '03',
                            'type': 'rev-request',
                            'year': '1998'
                        },
                        'rev-recd': {
                            'day': '24',
                            'month': '05',
                            'type': 'rev-recd',
                            'year': '1998'
                        },
                        'corrected': {
                            'day': '01',
                            'month': '06',
                            'type': 'corrected',
                            'year': '2012'
                        }
                    },
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en'
                },
            }
        ]
        obtained = list(dates.ArticleDatesValidation(xml_history_date).validate_history_dates(
            ["received", "rev-request", "rev-recd", "accepted", "corrected"], ["accepted", "corrected"]
        ))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

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
        obtained = list(dates.ArticleDatesValidation(xml_tree).validate_number_of_digits_in_article_date())
        expected = [
            {
                'title': 'Article pub-date day validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'pub-date',
                'sub_item': 'day',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '03',
                'got_value': '03',
                'message': 'Got 03, expected 03',
                'advice': None,
                'data': {'day': '03', 'month': '02', 'type': 'pub', 'year': '2024'},
            },
            {
                'title': 'Article pub-date month validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'pub-date',
                'sub_item': 'month',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '02',
                'got_value': '02',
                'message': 'Got 02, expected 02',
                'advice': None,
                'data': {'day': '03', 'month': '02', 'type': 'pub', 'year': '2024'},
            },
            {
                'title': 'Article pub-date year validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'pub-date',
                'sub_item': 'year',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '2024',
                'got_value': '2024',
                'message': 'Got 2024, expected 2024',
                'advice': None,
                'data': {'day': '03', 'month': '02', 'type': 'pub', 'year': '2024'},
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

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
        obtained = list(dates.ArticleDatesValidation(xml_tree).validate_number_of_digits_in_article_date())
        expected = [
            {
                'title': 'Article pub-date day validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'pub-date',
                'sub_item': 'day',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '03',
                'got_value': '03',
                'message': 'Got 03, expected 03',
                'advice': None,
                'data': {'day': '03', 'month': '02', 'type': 'pub', 'year': '202'},
            },
            {
                'title': 'Article pub-date month validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'pub-date',
                'sub_item': 'month',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '02',
                'got_value': '02',
                'message': 'Got 02, expected 02',
                'advice': None,
                'data': {'day': '03', 'month': '02', 'type': 'pub', 'year': '202'},
            },
            {
                'title': 'Article pub-date year validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'pub-date',
                'sub_item': 'year',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': '0202',
                'got_value': '202',
                'message': 'Got 202, expected 0202',
                'advice': 'Provide a 4-digit numeric value for year',
                'data': {'day': '03', 'month': '02', 'type': 'pub', 'year': '202'},
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

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
        obtained = list(dates.ArticleDatesValidation(xml_tree).validate_number_of_digits_in_article_date())
        expected = [
            {
                'title': 'Article pub-date day validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'pub-date',
                'sub_item': 'day',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '03',
                'got_value': '03',
                'message': 'Got 03, expected 03',
                'advice': None,
                'data': {'day': '03', 'month': '2', 'type': 'pub', 'year': '2024'},
            },
            {
                'title': 'Article pub-date month validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'pub-date',
                'sub_item': 'month',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': '02',
                'got_value': '2',
                'message': 'Got 2, expected 02',
                'advice': 'Provide a 2-digit numeric value for month',
                'data': {'day': '03', 'month': '2', 'type': 'pub', 'year': '2024'},
            },
            {
                'title': 'Article pub-date year validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'pub-date',
                'sub_item': 'year',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '2024',
                'got_value': '2024',
                'message': 'Got 2024, expected 2024',
                'advice': None,
                'data': {'day': '03', 'month': '2', 'type': 'pub', 'year': '2024'},
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

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
        obtained = list(dates.ArticleDatesValidation(xml_tree).validate_number_of_digits_in_article_date())
        expected = [
            {
                'title': 'Article pub-date day validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'pub-date',
                'sub_item': 'day',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': '03',
                'got_value': '3',
                'message': 'Got 3, expected 03',
                'advice': 'Provide a 2-digit numeric value for day',
                'data': {'day': '3', 'month': '02', 'type': 'pub', 'year': '2024'},
            },
            {
                'title': 'Article pub-date month validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'pub-date',
                'sub_item': 'month',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '02',
                'got_value': '02',
                'message': 'Got 02, expected 02',
                'advice': None,
                'data': {'day': '3', 'month': '02', 'type': 'pub', 'year': '2024'},
            },
            {
                'title': 'Article pub-date year validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'pub-date',
                'sub_item': 'year',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '2024',
                'got_value': '2024',
                'message': 'Got 2024, expected 2024',
                'advice': None,
                'data': {'day': '3', 'month': '02', 'type': 'pub', 'year': '2024'},
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

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
        obtained = list(dates.ArticleDatesValidation(xml_tree).validate_number_of_digits_in_article_date())
        expected = [
            {
                'title': 'Article pub-date day validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'pub-date',
                'sub_item': 'day',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a numeric digit for day represented with 2 digits',
                'got_value': 'dd',
                'message': 'Got dd, expected a numeric digit for day represented with 2 digits',
                'advice': 'Provide a 2-digit numeric value for day',
                'data': {'day': 'dd', 'month': 'mm', 'type': 'pub', 'year': 'yyyy'},
            },
            {
                'title': 'Article pub-date month validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'pub-date',
                'sub_item': 'month',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a numeric digit for month represented with 2 digits',
                'got_value': 'mm',
                'message': 'Got mm, expected a numeric digit for month represented with 2 digits',
                'advice': 'Provide a 2-digit numeric value for month',
                'data': {'day': 'dd', 'month': 'mm', 'type': 'pub', 'year': 'yyyy'},
            },
            {
                'title': 'Article pub-date year validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'pub-date',
                'sub_item': 'year',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a numeric digit for year represented with 4 digits',
                'got_value': 'yyyy',
                'message': 'Got yyyy, expected a numeric digit for year represented with 4 digits',
                'advice': 'Provide a 4-digit numeric value for year',
                'data': {'day': 'dd', 'month': 'mm', 'type': 'pub', 'year': 'yyyy'},
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

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
            'parent': 'article',
            'parent_article_type': 'research-article',
            'parent_id': None,
            'parent_lang': 'en',
            'item': 'pub-date',
            'sub_item': "@date-type='pub'",
            'validation_type': 'value',
            'response': 'OK',
            'expected_value': 'a date in the format: YYYY-MM-DD before or equal to 2023-12-12',
            'got_value': '2023-01-01',
            'message': 'Got 2023-01-01, expected a date in the format: YYYY-MM-DD before or equal to 2023-12-12',
            'advice': None,
            'data': {'day': '01', 'month': '01', 'type': 'pub', 'year': '2023'},
        }

        self.assertDictEqual(obtained, expected)

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
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'pub-date',
                'sub_item': "@date-type='pub'",
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': 'a date in the format: YYYY-MM-DD before or equal to 2023-12-12',
                'got_value': '0-01-01',
                'message': 'Got 0-01-01, expected a date in the format: YYYY-MM-DD before or equal to 2023-12-12',
                'advice': 'Provide a date in the format: YYYY-MM-DD before or equal to 2023-12-12',
                'data': {'day': '01', 'month': '01', 'type': 'pub', 'year': '0'},
            }

        self.assertDictEqual(obtained, expected)

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
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'pub-date',
                'sub_item': "@date-type='pub'",
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': 'a date in the format: YYYY-MM-DD before or equal to 2023-12-12',
                'got_value': '2023-13-01',
                'message': 'Got 2023-13-01, expected a date in the format: YYYY-MM-DD before or equal to 2023-12-12',
                'advice': 'Provide a date in the format: YYYY-MM-DD before or equal to 2023-12-12',
                'data': {'day': '01', 'month': '13', 'type': 'pub', 'year': '2023'},
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
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'pub-date',
                'sub_item': "@date-type='pub'",
                'validation_type': 'value',
                'response': 'ERROR',
                'expected_value': 'a date in the format: YYYY-MM-DD before or equal to 2023-12-12',
                'got_value': '2023-01-32',
                'message': 'Got 2023-01-32, expected a date in the format: YYYY-MM-DD before or equal to 2023-12-12',
                'advice': 'Provide a date in the format: YYYY-MM-DD before or equal to 2023-12-12',
                'data': {'day': '32', 'month': '01', 'type': 'pub', 'year': '2023'},
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
            'parent': 'article',
            'parent_article_type': 'research-article',
            'parent_id': None,
            'parent_lang': 'en',
            'item': 'pub-date',
            'sub_item': "@date-type='pub'",
            'validation_type': 'value',
            'response': 'ERROR',
            'expected_value': 'a date in the format: YYYY-MM-DD before or equal to 2020-12-12',
            'got_value': '2023-01-01',
            'message': 'Got 2023-01-01, expected a date in the format: YYYY-MM-DD before or equal to 2020-12-12',
            'advice': 'Provide a date in the format: YYYY-MM-DD before or equal to 2020-12-12',
            'data': {'day': '01', 'month': '01', 'type': 'pub', 'year': '2023'},
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
        expected = {
            'title': 'Collection pub-date validation',
            'parent': 'article',
            'parent_article_type': 'research-article',
            'parent_id': None,
            'parent_lang': 'en',
            'item': 'pub-date',
            'sub_item': "@date-type='collection'",
            'validation_type': 'format',
            'response': 'OK',
            'expected_value': '2023',
            'got_value': '2023',
            'message': 'Got 2023, expected 2023',
            'advice': None,
            'data': {'type': 'collection', 'year': '2023'},
        }

        self.assertDictEqual(obtained, expected)

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
        expected = {
            'title': 'Collection pub-date validation',
            'parent': 'article',
            'parent_article_type': 'research-article',
            'parent_id': None,
            'parent_lang': 'en',
            'item': 'pub-date',
            'sub_item': "@date-type='collection'",
            'validation_type': 'format',
            'response': 'ERROR',
            'expected_value': 'the publication date of the collection',
            'got_value': '202a',
            'message': 'Got 202a, expected the publication date of the collection',
            'advice': 'Provide only numeric values for the collection year',
            'data': {'type': 'collection', 'year': '202a'},
        }

        self.assertDictEqual(obtained, expected)

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
        expected = {
            'title': 'Collection pub-date validation',
            'parent': 'article',
            'parent_article_type': 'research-article',
            'parent_id': None,
            'parent_lang': 'en',
            'item': 'pub-date',
            'sub_item': "@date-type='collection'",
            'validation_type': 'format',
            'response': 'ERROR',
            'expected_value': 'the publication date of the collection',
            'got_value': '23',
            'message': 'Got 23, expected the publication date of the collection',
            'advice': 'Provide a four-digit numeric value for the year of collection',
            'data': {'type': 'collection', 'year': '23'},
        }

        self.assertDictEqual(obtained, expected)

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
        expected = {
            'title': 'Collection pub-date validation',
            'parent': 'article',
            'parent_article_type': 'research-article',
            'parent_id': None,
            'parent_lang': 'en',
            'item': 'pub-date',
            'sub_item': "@date-type='collection'",
            'validation_type': 'format',
            'response': 'ERROR',
            'expected_value': 'the publication date of the collection',
            'got_value': '2024',
            'message': 'Got 2024, expected the publication date of the collection',
            'advice': 'Provide a numeric value less than or equal to 2023',
            'data': {'type': 'collection', 'year': '2024'},
        }

        self.assertDictEqual(obtained, expected)

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
        expected = {
            'title': 'Collection pub-date validation',
            'parent': 'article',
            'parent_article_type': 'research-article',
            'parent_id': None,
            'parent_lang': 'en',
            'item': 'pub-date',
            'sub_item': "@date-type='collection'",
            'validation_type': 'exist',
            'response': 'ERROR',
            'expected_value': 'the publication date of the collection',
            'got_value': None,
            'message': 'Got None, expected the publication date of the collection',
            'advice': 'Provide the publication date of the collection',
            'data': None,
        }

        self.assertDictEqual(obtained, expected)
