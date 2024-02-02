import unittest

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation.funding_group import FundingGroupValidation


def callable_validation_success(award_id):
    return True


def callable_validation_fail(award_id):
    return False


class FundingGroupValidationTest(unittest.TestCase):
    def test_funding_sources_validation_success_1_funding_1_award(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>Natural Science Foundation of Hunan Province</funding-source>
                                <award-id>2019JJ40269</award-id>
                            </award-group>
                            <award-group>
                                <funding-source>Hubei Provincial Natural Science Foundation of China</funding-source>
                                <award-id>2020CFB547</award-id>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).funding_sources_exist_validation()
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': './/funding-group/award-group/funding-source',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'at leats 1 value to <funding-source> and at least 1 value to <award-id>',
                'got_value': '1 values to <funding-source> and 1 values to <award-id>',
                'message': "Got ['Natural Science Foundation of Hunan Province'] as <funding-source> "
                           "['2019JJ40269'] as <award-id>",
                'advice': None
            },
            {
                'title': 'Funding source element validation',
                'xpath': './/funding-group/award-group/funding-source',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'at leats 1 value to <funding-source> and at least 1 value to <award-id>',
                'got_value': '1 values to <funding-source> and 1 values to <award-id>',
                'message': "Got ['Hubei Provincial Natural Science Foundation of China'] as <funding-source> ['2020CFB547'] as <award-id>",
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_success_2_funding_1_award(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>Natural Science Foundation of Hunan Province</funding-source>
                                <funding-source>Hubei Provincial Natural Science Foundation of China</funding-source>
                                <award-id>2019JJ40269</award-id>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).funding_sources_exist_validation()
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': './/funding-group/award-group/funding-source',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'at leats 1 value to <funding-source> and at least 1 value to <award-id>',
                'got_value': '2 values to <funding-source> and 1 values to <award-id>',
                'message': "Got ['Natural Science Foundation of Hunan Province', "
                           "'Hubei Provincial Natural Science Foundation of China'] "
                           "as <funding-source> ['2019JJ40269'] as <award-id>",
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_success_1_funding_2_award(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>Natural Science Foundation of Hunan Province</funding-source>
                                <award-id>2019JJ40269</award-id>
                                <award-id>2020CFB547</award-id>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).funding_sources_exist_validation()
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': './/funding-group/award-group/funding-source',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'at leats 1 value to <funding-source> and at least 1 value to <award-id>',
                'got_value': '1 values to <funding-source> and 2 values to <award-id>',
                'message': "Got ['Natural Science Foundation of Hunan Province'] as <funding-source> "
                           "['2019JJ40269', '2020CFB547'] as <award-id>",
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_fail_0_funding_0_award(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <front>
                    <article-meta>

                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).funding_sources_exist_validation()
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': './/funding-group/award-group/funding-source',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'at leats 1 value to <funding-source> and at least 1 value to <award-id>',
                'got_value': '0 values to <funding-source> and 0 values to <award-id>',
                'message': 'Got [] as <funding-source> [] as <award-id>',
                'advice': 'Provide values to <funding-source> and <award-id>',
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_fail_1_funding_0_award(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>Natural Science Foundation of Hunan Province</funding-source>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).funding_sources_exist_validation()
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': './/funding-group/award-group/funding-source',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'at leats 1 value to <funding-source> and at least 1 value to <award-id>',
                'got_value': '1 values to <funding-source> and 0 values to <award-id>',
                'message': "Got ['Natural Science Foundation of Hunan Province'] as <funding-source> [] as <award-id>",
                'advice': 'Provide values to <award-id>',
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_fail_0_funding_1_award(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <award-id>2019JJ40269</award-id>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).funding_sources_exist_validation()
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': './/funding-group/award-group/funding-source',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'at leats 1 value to <funding-source> and at least 1 value to <award-id>',
                'got_value': '0 values to <funding-source> and 1 values to <award-id>',
                'message': "Got [] as <funding-source> ['2019JJ40269'] as <award-id>",
                'advice': 'Provide values to <funding-source>',
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_principal_award_recipient_validation_success(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>Natural Science Foundation of Hunan Province</funding-source>
                                <award-id>2019JJ40269</award-id>
                                <principal-award-recipient>Stanford</principal-award-recipient>
                            </award-group>
                            <award-group>
                                <funding-source>Hubei Provincial Natural Science Foundation of China</funding-source>
                                <award-id>2020CFB547</award-id>
                                <principal-award-recipient>Berkeley</principal-award-recipient>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).principal_award_recipient_exist_validation()
        expected = [
            {
                'title': 'Principal award recipient element validation',
                'xpath': './/funding-group/award-group/principal-award-recipient',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'Stanford',
                'got_value': 'Stanford',
                'message': 'Got Stanford expected Stanford',
                'advice': None
            },
            {
                'title': 'Principal award recipient element validation',
                'xpath': './/funding-group/award-group/principal-award-recipient',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'Berkeley',
                'got_value': 'Berkeley',
                'message': 'Got Berkeley expected Berkeley',
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_principal_award_recipient_validation_fail(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>Natural Science Foundation of Hunan Province</funding-source>
                                <award-id>2019JJ40269</award-id>
                            </award-group>
                            <award-group>
                                <funding-source>Hubei Provincial Natural Science Foundation of China</funding-source>
                                <award-id>2020CFB547</award-id>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).principal_award_recipient_exist_validation()
        expected = [
            {
                'title': 'Principal award recipient element validation',
                'xpath': './/funding-group/award-group/principal-award-recipient',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'value to <principal-award-recipient>',
                'got_value': None,
                'message': 'Got None expected value to <principal-award-recipient>',
                'advice': 'Provide value to <principal-award-recipient>',
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_principal_investigator_validation_success(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>Natural Science Foundation of Hunan Province</funding-source>
                                <award-id>2019JJ40269</award-id>
                                <principal-award-recipient>Stanford</principal-award-recipient>
                                <principal-investigator>
                                    <string-name>
                                        <given-names>Sharon R.</given-names>
                                        <surname>Kaufman</surname>
                                    </string-name>
                                </principal-investigator>
                            </award-group>
                            <award-group>
                                <funding-source>Hubei Provincial Natural Science Foundation of China</funding-source>
                                <award-id>2020CFB547</award-id>
                                <principal-award-recipient>Berkeley</principal-award-recipient>
                                <principal-investigator>
                                    <string-name>
                                        <given-names>João</given-names>
                                        <surname>Silva</surname>
                                    </string-name>
                                </principal-investigator>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).principal_investigator_exist_validation()
        expected = [
            {
                'title': 'Principal investigator element validation',
                'xpath': './/funding-group/award-group/principal-investigator/string-name',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': {
                    "given-names": 'Sharon R.',
                    "surname": 'Kaufman'
                },
                'got_value': {
                    "given-names": 'Sharon R.',
                    "surname": 'Kaufman'
                },
                'message': "Got {'given-names': 'Sharon R.', 'surname': 'Kaufman'} expected {'given-names': 'Sharon R.', 'surname': 'Kaufman'}",
                'advice': None
            },
            {
                'title': 'Principal investigator element validation',
                'xpath': './/funding-group/award-group/principal-investigator/string-name',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': {
                    "given-names": 'João',
                    "surname": 'Silva'
                },
                'got_value': {
                    "given-names": 'João',
                    "surname": 'Silva'
                },
                'message': "Got {'given-names': 'João', 'surname': 'Silva'} expected {'given-names': 'João', 'surname': 'Silva'}",
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_principal_investigator_validation_fail(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>Natural Science Foundation of Hunan Province</funding-source>
                                <award-id>2019JJ40269</award-id>
                                <principal-award-recipient>Stanford</principal-award-recipient>
                            </award-group>
                            <award-group>
                                <funding-source>Hubei Provincial Natural Science Foundation of China</funding-source>
                                <award-id>2020CFB547</award-id>
                                <principal-award-recipient>Berkeley</principal-award-recipient>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).principal_investigator_exist_validation()
        expected = [
            {
                'title': 'Principal investigator element validation',
                'xpath': './/funding-group/award-group/principal-investigator/string-name',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'value to <principal-investigator>',
                'got_value': None,
                'message': 'Got None expected value to <principal-investigator>',
                'advice': 'Provide value to <principal-investigator>',
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_award_id_format_validation_success(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>Natural Science Foundation of Hunan Province</funding-source>
                                <award-id>2019JJ40269</award-id>
                            </award-group>
                            <award-group>
                                <funding-source>Hubei Provincial Natural Science Foundation of China</funding-source>
                                <award-id>2020CFB547</award-id>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).award_id_format_validation(callable_validation_success)
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': './/funding-group/award-group/award-id',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '2019JJ40269',
                'got_value': '2019JJ40269',
                'message': 'Got 2019JJ40269 expected 2019JJ40269',
                'advice': None
            },
            {
                'title': 'Funding source element validation',
                'xpath': './/funding-group/award-group/award-id',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '2020CFB547',
                'got_value': '2020CFB547',
                'message': 'Got 2020CFB547 expected 2020CFB547',
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_award_id_format_validation_fail(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>Natural Science Foundation of Hunan Province</funding-source>
                                <award-id>2019JJ40269</award-id>
                            </award-group>
                            <award-group>
                                <funding-source>Hubei Provincial Natural Science Foundation of China</funding-source>
                                <award-id>2020CFB547</award-id>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).award_id_format_validation(callable_validation_fail)
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': './/funding-group/award-group/award-id',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a valid value for <award-id>',
                'got_value': '2019JJ40269',
                'message': 'Got 2019JJ40269 expected a valid value for <award-id>',
                'advice': 'Provide a valid value for <award-id>'
            },
            {
                'title': 'Funding source element validation',
                'xpath': './/funding-group/award-group/award-id',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a valid value for <award-id>',
                'got_value': '2020CFB547',
                'message': 'Got 2020CFB547 expected a valid value for <award-id>',
                'advice': 'Provide a valid value for <award-id>'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_ack_exist_validation_success_article_ack(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <back>
                    <ack>
                        <title>Acknowledgments</title>
                        <p>Paragraph 1.</p>
                        <p>Paragraph 2.</p>
                        <p>Paragraph 3.</p>
                    </ack>
                </back>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).ack_exist_validation()
        expected = [
            {
                'title': 'Acknowledgment element validation',
                'xpath': './/back//ack',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': {
                    "title": 'Acknowledgments',
                    "text": 'Paragraph 1. Paragraph 2. Paragraph 3.'
                },
                'got_value': {
                    "title": 'Acknowledgments',
                    "text": 'Paragraph 1. Paragraph 2. Paragraph 3.'
                },
                'message': "Got {'title': 'Acknowledgments', 'text': 'Paragraph 1. Paragraph 2. Paragraph 3.'} "
                           "expected {'title': 'Acknowledgments', 'text': 'Paragraph 1. Paragraph 2. Paragraph 3.'}",
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_ack_exist_validation_success_sub_article_ack(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <sub-article>
                    <back>
                        <ack>
                            <title>Acknowledgments</title>
                            <p>Paragraph 1.</p>
                            <p>Paragraph 2.</p>
                            <p>Paragraph 3.</p>
                        </ack>
                    </back>
                </sub-article>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).ack_exist_validation()
        expected = [
            {
                'title': 'Acknowledgment element validation',
                'xpath': './/back//ack',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': {
                    "title": 'Acknowledgments',
                    "text": 'Paragraph 1. Paragraph 2. Paragraph 3.'
                },
                'got_value': {
                    "title": 'Acknowledgments',
                    "text": 'Paragraph 1. Paragraph 2. Paragraph 3.'
                },
                'message': "Got {'title': 'Acknowledgments', 'text': 'Paragraph 1. Paragraph 2. Paragraph 3.'} "
                           "expected {'title': 'Acknowledgments', 'text': 'Paragraph 1. Paragraph 2. Paragraph 3.'}",
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_ack_exist_validation_fail_article_ack(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <back>
                    
                </back>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).ack_exist_validation()
        expected = [
            {
                'title': 'Acknowledgment element validation',
                'xpath': './/back//ack',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'value to <ack>',
                'got_value': None,
                'message': 'Got None expected value to <ack>',
                'advice': 'Provide value to <ack>'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_statement_exist_validation_success(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>Natural Science Foundation of Hunan Province</funding-source>
                                <award-id>2019JJ40269</award-id>
                            </award-group>
                            <funding-statement>declaração de financiamento</funding-statement>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).funding_statement_exist_validation()
        expected = [
            {
                'title': 'Funding statement element validation',
                'xpath': './/funding-group/funding-statement',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'declaração de financiamento',
                'got_value': 'declaração de financiamento',
                'message': 'Got declaração de financiamento expected declaração de financiamento',
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_statement_exist_validation_fail(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>Natural Science Foundation of Hunan Province</funding-source>
                                <award-id>2019JJ40269</award-id>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).funding_statement_exist_validation()
        expected = [
            {
                'title': 'Funding statement element validation',
                'xpath': './/funding-group/funding-statement',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'value to <funding-statement>',
                'got_value': None,
                'message': 'Got None expected value to <funding-statement>',
                'advice': 'Provide value to <funding-statement>',
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)


if __name__ == '__main__':
    unittest.main()
