from unittest import TestCase
from lxml import etree

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation import dates


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
            ["received", "rev-request", "rev-recd", "accepted", "approved"], ["received", "approved"]
        )

            },
            ["received", "rev-request", "rev-recd", "accepted", "approved"], ["received", "approved"]
        )

            },
            ["received", "rev-request", "rev-recd", "accepted", "approved"], ["received", "approved"]
        )

        expected = [
        ]

        expected = [
        ]


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
