import unittest

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation.funding_group import FundingGroupValidation


def callable_validation_success(award_id):
    return True


def callable_validation_fail(award_id):
    return False


class FundingGroupValidationTest(unittest.TestCase):
    def test_funding_sources_validation_success_without_funding_information(self):
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
        obtained = list(FundingGroupValidation(xml_tree).funding_sources_exist_validation())

        self.assertListEqual([], obtained)

    def test_funding_sources_validation_success_2_funding_1_award_in_funding_group(self):
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
                'expected_value': 'at least 1 value to funding source and at least 1 value to award id',
                'got_value': '2 values to funding source and 1 values to award id',
                'message': "Got ['Natural Science Foundation of Hunan Province', "
                           "'Hubei Provincial Natural Science Foundation of China'] "
                           "as funding source and ['2019JJ40269'] as award id",
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_success_2_funding_1_award_in_fn_group_financial_disclosure(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <back>
                    <fn-group>
                        <fn fn-type="financial-disclosure">
                            <p>Conselho Nacional de Desenvolvimento Científico e Tecnológico</p>
                            <p>Grant No: 303625/2019-8</p>
                            <p>Fundação de Amparo à Pesquisa do Estado de São Paulo</p>
                            <p>Grant No: 2016/17640-0</p>
                        </fn>
                    </fn-group>
                </back>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).funding_sources_exist_validation()
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': ".//fn-group/fn[@fn-type='financial-disclosure']//p",
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'at least 1 value to funding source and at least 1 value to award id',
                'got_value': '2 values to funding source and 2 values to award id',
                'message': "Got ['Conselho Nacional de Desenvolvimento Científico e Tecnológico', "
                           "'Fundação de Amparo à Pesquisa do Estado de São Paulo'] as funding source and "
                           "['303625/2019-8', '2016/17640-0'] as award id",
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_success_2_funding_1_award_in_fn_group_supported_by(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <back>
                    <fn-group>
                        <fn fn-type="supported-by">
                            <p>Conselho Nacional de Desenvolvimento Científico e Tecnológico</p>
                            <p>Grant No: 303625/2019-8</p>
                            <p>Fundação de Amparo à Pesquisa do Estado de São Paulo</p>
                            <p>Grant No: 2016/17640-0</p>
                        </fn>
                    </fn-group>
                </back>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).funding_sources_exist_validation()
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': ".//fn-group/fn[@fn-type='supported-by']//p",
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'at least 1 value to funding source',
                'got_value': '2 values to funding source and 2 values to award id',
                'message': "Got ['Conselho Nacional de Desenvolvimento Científico e Tecnológico', "
                           "'Fundação de Amparo à Pesquisa do Estado de São Paulo'] as funding source and "
                           "['303625/2019-8', '2016/17640-0'] as award id",
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_success_1_funding_2_award_in_funding_group(self):
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
                'expected_value': 'at least 1 value to funding source and at least 1 value to award id',
                'got_value': '1 values to funding source and 2 values to award id',
                'message': "Got ['Natural Science Foundation of Hunan Province'] as funding source and "
                           "['2019JJ40269', '2020CFB547'] as award id",
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_success_1_funding_2_award_in_fn_group_financial_disclosure(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <back>
                    <fn-group>
                        <fn fn-type="financial-disclosure">
                            <p>Conselho Nacional de Desenvolvimento Científico e Tecnológico</p>
                            <p>Grant No: 303625/2019-8</p>
                            <p>Grant No: 2016/17640-0</p>
                        </fn>
                    </fn-group>
                </back>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).funding_sources_exist_validation()
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': ".//fn-group/fn[@fn-type='financial-disclosure']//p",
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'at least 1 value to funding source and at least 1 value to award id',
                'got_value': '1 values to funding source and 2 values to award id',
                'message': "Got ['Conselho Nacional de Desenvolvimento Científico e Tecnológico'] as funding source and "
                           "['303625/2019-8', '2016/17640-0'] as award id",
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_success_1_funding_2_award_in_fn_group_supported_by(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <back>
                    <fn-group>
                        <fn fn-type="supported-by">
                            <p>Conselho Nacional de Desenvolvimento Científico e Tecnológico</p>
                            <p>Grant No: 303625/2019-8</p>
                            <p>Grant No: 2016/17640-0</p>
                        </fn>
                    </fn-group>
                </back>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).funding_sources_exist_validation()
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': ".//fn-group/fn[@fn-type='supported-by']//p",
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'at least 1 value to funding source',
                'got_value': '1 values to funding source and 2 values to award id',
                'message': "Got ['Conselho Nacional de Desenvolvimento Científico e Tecnológico'] as funding source and "
                           "['303625/2019-8', '2016/17640-0'] as award id",
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_fail_0_funding_0_award_in_funding_group(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <front>
                    <article-meta>
                        <funding-group>
                            <award-group>
                                
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
                'expected_value': 'at least 1 value to funding source and at least 1 value to award id',
                'got_value': '0 values to funding source and 0 values to award id',
                'message': 'Got [] as funding source and [] as award id',
                'advice': 'Provide values to award id and funding source'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_fail_0_funding_0_award_in_fn_group_financial_disclosure(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <back>
                    <fn-group>
                        <fn fn-type="financial-disclosure">
                            
                        </fn>
                    </fn-group>
                </back>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).funding_sources_exist_validation()
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': ".//fn-group/fn[@fn-type='financial-disclosure']//p",
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'at least 1 value to funding source and at least 1 value to award id',
                'got_value': '0 values to funding source and 0 values to award id',
                'message': 'Got [] as funding source and [] as award id',
                'advice': 'Provide values to award id and funding source'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_fail_0_funding_0_award_in_fn_group_supported_by(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <back>
                    <fn-group>
                        <fn fn-type="supported-by">

                        </fn>
                    </fn-group>
                </back>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).funding_sources_exist_validation()
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': ".//fn-group/fn[@fn-type='supported-by']//p",
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'at least 1 value to funding source',
                'got_value': '0 values to funding source and 0 values to award id',
                'message': 'Got [] as funding source and [] as award id',
                'advice': 'Provide value to funding source'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_fail_1_funding_0_award_in_funding_group(self):
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
                'expected_value': 'at least 1 value to funding source and at least 1 value to award id',
                'got_value': '1 values to funding source and 0 values to award id',
                'message': "Got ['Natural Science Foundation of Hunan Province'] as funding source and [] as award id",
                'advice': 'Provide value to award id or move funding source to <fn fn-type="supported-by">'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_fail_1_funding_0_award_in_fn_group_financial_disclosure(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <back>
                    <fn-group>
                        <fn fn-type="financial-disclosure">
                            <p>Conselho Nacional de Desenvolvimento Científico e Tecnológico</p>
                        </fn>
                    </fn-group>
                </back>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).funding_sources_exist_validation()
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': ".//fn-group/fn[@fn-type='financial-disclosure']//p",
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'at least 1 value to funding source and at least 1 value to award id',
                'got_value': '1 values to funding source and 0 values to award id',
                'message': "Got ['Conselho Nacional de Desenvolvimento Científico e Tecnológico'] as funding source "
                           "and [] as award id",
                'advice': 'Provide value to award id or move funding source to <fn fn-type="supported-by">'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_fail_1_funding_0_award_in_fn_group_supported_by(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <back>
                    <fn-group>
                        <fn fn-type="supported-by">
                            <p>Conselho Nacional de Desenvolvimento Científico e Tecnológico</p>
                        </fn>
                    </fn-group>
                </back>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).funding_sources_exist_validation()
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': ".//fn-group/fn[@fn-type='supported-by']//p",
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'at least 1 value to funding source',
                'got_value': '1 values to funding source and 0 values to award id',
                'message': "Got ['Conselho Nacional de Desenvolvimento Científico e Tecnológico'] as funding source "
                           "and [] as award id",
                'advice': None
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_fail_0_funding_1_award_in_funding_group(self):
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
                'expected_value': 'at least 1 value to funding source and at least 1 value to award id',
                'got_value': '0 values to funding source and 1 values to award id',
                'message': "Got [] as funding source and ['2019JJ40269'] as award id",
                'advice': 'Provide value to funding source',
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_fail_0_funding_1_award_in_fn_group_financial_disclosure(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <back>
                    <fn-group>
                        <fn fn-type="financial-disclosure">
                            <p>Grant No: 2016/17640-0</p>
                        </fn>
                    </fn-group>
                </back>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).funding_sources_exist_validation()
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': ".//fn-group/fn[@fn-type='financial-disclosure']//p",
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'at least 1 value to funding source and at least 1 value to award id',
                'got_value': '0 values to funding source and 1 values to award id',
                'message': "Got [] as funding source and ['2016/17640-0'] as award id",
                'advice': 'Provide value to funding source',
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_funding_sources_validation_fail_0_funding_1_award_in_fn_group_supported_by(self):
        self.maxDiff = None
        xml_str = """
            <article>
                <back>
                    <fn-group>
                        <fn fn-type="supported-by">
                            <p>Grant No: 2016/17640-0</p>
                        </fn>
                    </fn-group>
                </back>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = FundingGroupValidation(xml_tree).funding_sources_exist_validation()
        expected = [
            {
                'title': 'Funding source element validation',
                'xpath': ".//fn-group/fn[@fn-type='supported-by']//p",
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'at least 1 value to funding source',
                'got_value': '0 values to funding source and 1 values to award id',
                'message': "Got [] as funding source and ['2016/17640-0'] as award id",
                'advice': 'Provide value to funding source',
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
                'expected_value': 'a valid value for award id',
                'got_value': '2019JJ40269',
                'message': 'Got 2019JJ40269 expected a valid value for award id',
                'advice': 'Provide a valid value for award id'
            },
            {
                'title': 'Funding source element validation',
                'xpath': './/funding-group/award-group/award-id',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a valid value for award id',
                'got_value': '2020CFB547',
                'message': 'Got 2020CFB547 expected a valid value for award id',
                'advice': 'Provide a valid value for award id'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)


if __name__ == '__main__':
    unittest.main()
