import unittest

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation.funding_group import FundingGroupValidation


class FundingGroupValidationTest(unittest.TestCase):
    def test_funding_sources_validation_success(self):
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
        obtained = FundingGroupValidation(xml_tree).funding_sources_validation()
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': './/funding-group/award-group/funding-source',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'Natural Science Foundation of Hunan Province (2019JJ40269)',
                'got_value': 'Natural Science Foundation of Hunan Province (2019JJ40269)',
                'message': 'Got Natural Science Foundation of Hunan Province (2019JJ40269) '
                           'expected Natural Science Foundation of Hunan Province (2019JJ40269)',
                'advice': None
            },
            {
                'title': 'Funding source element validation',
                'xpath': './/funding-group/award-group/funding-source',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'Hubei Provincial Natural Science Foundation of China (2020CFB547)',
                'got_value': 'Hubei Provincial Natural Science Foundation of China (2020CFB547)',
                'message': 'Got Hubei Provincial Natural Science Foundation of China (2020CFB547) '
                           'expected Hubei Provincial Natural Science Foundation of China (2020CFB547)',
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_fail(self):
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
        obtained = FundingGroupValidation(xml_tree).funding_sources_validation()
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': './/funding-group/award-group/funding-source',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'values to <funding-source> and <award-id>',
                'got_value': None,
                'message': 'Got None expected values to <funding-source> and <award-id>',
                'advice': 'Provide values to <funding-source> and <award-id>',
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_fail_without_award_id(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                <funding-source>Natural Science Foundation of Hunan Province</funding-source>
                            </award-group>
                            <award-group>
                                <funding-source>Hubei Provincial Natural Science Foundation of China</funding-source>
                            </award-group>
                        </funding-group>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).funding_sources_validation()
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': './/funding-group/award-group/funding-source',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'values to <funding-source> and <award-id>',
                'got_value': 'Natural Science Foundation of Hunan Province (None)',
                'message': 'Got Natural Science Foundation of Hunan Province (None) '
                           'expected values to <funding-source> and <award-id>',
                'advice': 'Provide values to <funding-source> and <award-id>',
            },
            {
                'title': 'Funding source element validation',
                'xpath': './/funding-group/award-group/funding-source',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'values to <funding-source> and <award-id>',
                'got_value': 'Hubei Provincial Natural Science Foundation of China (None)',
                'message': 'Got Hubei Provincial Natural Science Foundation of China (None) '
                           'expected values to <funding-source> and <award-id>',
                'advice': 'Provide values to <funding-source> and <award-id>',
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
        obtained = FundingGroupValidation(xml_tree).principal_award_recipient_validation()
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
        obtained = FundingGroupValidation(xml_tree).principal_award_recipient_validation()
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
        obtained = FundingGroupValidation(xml_tree).principal_investigator_validation()
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
        obtained = FundingGroupValidation(xml_tree).principal_investigator_validation()
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


if __name__ == '__main__':
    unittest.main()
