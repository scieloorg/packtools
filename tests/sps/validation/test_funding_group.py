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
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = list(FundingGroupValidation(xml_tree, special_chars_funding=['.', ','],
                                               special_chars_award_id=['/', '.',
                                                                       '-']).funding_sources_exist_validation())

        self.assertListEqual([], obtained)

    def test_funding_sources_validation_success_2_funding_1_award_in_funding_group(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        obtained = list(FundingGroupValidation(
            xml_tree,
            special_chars_funding=['.', ','],
            special_chars_award_id=['/', '.', '-']
        ).funding_sources_exist_validation())
        expected = [
            {
                'title': 'Funding source element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'award-group',
                'sub_item': 'funding-source',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'at least 1 value for funding source and at least 1 value for award id',
                'got_value': '2 values for funding source and 1 values for award id',
                'message': 'Got 2 values for funding source and 1 values for award id, expected at least 1 value for '
                           'funding source and at least 1 value for award id',
                'advice': None,
                'data': {
                    'ack': [],
                    'article_lang': "pt",
                    'article_type': "research-article",
                    'award_groups': [
                        {
                            'award-id': ['2019JJ40269'],
                            'funding-source': [
                                'Natural Science Foundation of Hunan Province',
                                'Hubei Provincial Natural Science Foundation of China'
                            ]
                        }
                    ],
                    'fn_financial_information': [],
                    'funding_sources': [
                        'Natural Science Foundation of Hunan Province',
                        'Hubei Provincial Natural Science Foundation of China'
                    ],
                    'funding_statement': None,
                    'principal_award_recipients': []
                },
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_funding_sources_validation_success_2_funding_1_award_in_fn_group_financial_disclosure(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        obtained = list(FundingGroupValidation(
            xml_tree,
            special_chars_funding=['.', ','],
            special_chars_award_id=['/', '.', '-']
        ).funding_sources_exist_validation())
        expected = [
            {
                'title': 'Funding source element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'fn',
                'sub_item': "@fn-type='financial-disclosure'",
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'at least 1 value for funding source and at least 1 value for award id',
                'got_value': '2 values that look like funding source and 2 values that look like award id',
                'message': 'Got 2 values that look like funding source and 2 values that look like award id, '
                           'expected at least 1 value for funding source and at least 1 value for award id',
                'advice': None,
                'data': {
                    'ack': [],
                    'article_lang': "pt",
                    'article_type': "research-article",
                    'award_groups': [],
                    'fn_financial_information': [
                        {
                            'fn-type': 'financial-disclosure',
                            'look-like-award-id': [
                                '303625/2019-8',
                                '2016/17640-0'
                            ],
                            'look-like-funding-source': [
                                'Conselho Nacional de Desenvolvimento Científico e Tecnológico',
                                'Fundação de Amparo à Pesquisa do Estado de São Paulo'
                            ]
                        }
                    ],
                    'funding_sources': [],
                    'funding_statement': None,
                    'principal_award_recipients': []
                },
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_funding_sources_validation_success_2_funding_1_award_in_fn_group_supported_by(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        obtained = list(FundingGroupValidation(
            xml_tree,
            special_chars_funding=['.', ','],
            special_chars_award_id=['/', '.', '-']
        ).funding_sources_exist_validation())
        expected = [
            {
                'title': 'Funding source element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'fn',
                'sub_item': "@fn-type='supported-by'",
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'at least 1 value for funding source',
                'got_value': '2 values that look like funding source and 2 values that look like award id',
                'message': 'Got 2 values that look like funding source and 2 values that look like award id, '
                           'expected at least 1 value for funding source',
                'advice': None,
                'data': {
                    'ack': [],
                    'article_lang': "pt",
                    'article_type': "research-article",
                    'award_groups': [],
                    'fn_financial_information': [
                        {
                            'fn-type': 'supported-by',
                            'look-like-award-id': [
                                '303625/2019-8',
                                '2016/17640-0'
                            ],
                            'look-like-funding-source': [
                                'Conselho Nacional de Desenvolvimento Científico e Tecnológico',
                                'Fundação de Amparo à Pesquisa do Estado de São Paulo'
                            ]
                        }
                    ],
                    'funding_sources': [],
                    'funding_statement': None,
                    'principal_award_recipients': []
                },
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_funding_sources_validation_success_1_funding_2_award_in_funding_group(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        obtained = list(FundingGroupValidation(
            xml_tree,
            special_chars_funding=['.', ','],
            special_chars_award_id=['/', '.', '-']
        ).funding_sources_exist_validation())
        expected = [
            {
                'title': 'Funding source element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'award-group',
                'sub_item': 'funding-source',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'at least 1 value for funding source and at least 1 value for award id',
                'got_value': '1 values for funding source and 2 values for award id',
                'message': 'Got 1 values for funding source and 2 values for award id, expected at least 1 value for '
                           'funding source and at least 1 value for award id',
                'advice': None,
                'data': {
                    'ack': [],
                    'article_lang': "pt",
                    'article_type': "research-article",
                    'award_groups': [
                        {
                            'award-id': ['2019JJ40269', '2020CFB547'],
                            'funding-source': ['Natural Science Foundation of Hunan Province']
                        }
                    ],
                    'fn_financial_information': [],
                    'funding_sources': ['Natural Science Foundation of Hunan Province'],
                    'funding_statement': None,
                    'principal_award_recipients': []
                },
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_funding_sources_validation_success_1_funding_2_award_in_fn_group_financial_disclosure(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        obtained = list(FundingGroupValidation(
            xml_tree,
            special_chars_funding=['.', ','],
            special_chars_award_id=['/', '.', '-']
        ).funding_sources_exist_validation())
        expected = [
            {
                'title': 'Funding source element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'fn',
                'sub_item': "@fn-type='financial-disclosure'",
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'at least 1 value for funding source and at least 1 value for award id',
                'got_value': '1 values that look like funding source and 2 values that look like award id',
                'message': 'Got 1 values that look like funding source and 2 values that look like award id, '
                           'expected at least 1 value for funding source and at least 1 value for award id',
                'advice': None,
                'data': {
                    'ack': [],
                    'article_lang': "pt",
                    'article_type': "research-article",
                    'award_groups': [],
                    'fn_financial_information': [
                        {
                            'fn-type': 'financial-disclosure',
                            'look-like-award-id': ['303625/2019-8', '2016/17640-0'],
                            'look-like-funding-source': ['Conselho Nacional de Desenvolvimento Científico e Tecnológico']
                        }
                    ],
                    'funding_sources': [],
                    'funding_statement': None,
                    'principal_award_recipients': []},
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_funding_sources_validation_success_1_funding_2_award_in_fn_group_supported_by(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        obtained = list(FundingGroupValidation(
            xml_tree,
            special_chars_funding=['.', ','],
            special_chars_award_id=['/', '.', '-']
        ).funding_sources_exist_validation())
        expected = [
            {
                'title': 'Funding source element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'fn',
                'sub_item': "@fn-type='supported-by'",
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'at least 1 value for funding source',
                'got_value': '1 values that look like funding source and 2 values that look like award id',
                'message': 'Got 1 values that look like funding source and 2 values that look like award id, '
                           'expected at least 1 value for funding source',
                'advice': None,
                'data': {
                    'ack': [],
                    'article_lang': "pt",
                    'article_type': "research-article",
                    'award_groups': [],
                    'fn_financial_information': [
                        {
                            'fn-type': 'supported-by',
                            'look-like-award-id': ['303625/2019-8', '2016/17640-0'],
                            'look-like-funding-source': [
                                'Conselho Nacional de Desenvolvimento Científico e Tecnológico'
                            ]
                        }
                    ],
                    'funding_sources': [],
                    'funding_statement': None,
                    'principal_award_recipients': []
                },
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_funding_sources_validation_fail_0_funding_0_award_in_funding_group(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        obtained = list(FundingGroupValidation(
            xml_tree,
            special_chars_funding=['.', ','],
            special_chars_award_id=['/', '.', '-']
        ).funding_sources_exist_validation())
        expected = [
            {
                'title': 'Funding source element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'award-group',
                'sub_item': 'funding-source',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'at least 1 value for funding source and at least 1 value for award id',
                'got_value': '0 values for funding source and 0 values for award id',
                'message': 'Got 0 values for funding source and 0 values for award id, expected at least 1 value for '
                           'funding source and at least 1 value for award id',
                'advice': 'Provide values for award id and funding source',
                'data': {
                    'ack': [],
                    'article_lang': "pt",
                    'article_type': "research-article",
                    'award_groups': [
                        {
                            'award-id': [],
                            'funding-source': []
                        }
                    ],
                    'fn_financial_information': [],
                    'funding_sources': [],
                    'funding_statement': None,
                    'principal_award_recipients': []},
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_funding_sources_validation_fail_0_funding_0_award_in_fn_group_financial_disclosure(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
                <back>
                    <fn-group>
                        <fn fn-type="financial-disclosure">

                        </fn>
                    </fn-group>
                </back>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = list(FundingGroupValidation(
            xml_tree,
            special_chars_funding=['.', ','],
            special_chars_award_id=['/', '.', '-']
        ).funding_sources_exist_validation())
        expected = [
            {
                'title': 'Funding source element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'fn',
                'sub_item': "@fn-type='financial-disclosure'",
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'at least 1 value for funding source and at least 1 value for award id',
                'got_value': '0 values that look like funding source and 0 values that look like award id',
                'message': 'Got 0 values that look like funding source and 0 values that look like award id, '
                           'expected at least 1 value for funding source and at least 1 value for award id',
                'advice': 'Provide values for award id and funding source',
                'data': {
                    'ack': [],
                    'article_lang': "pt",
                    'article_type': "research-article",
                    'award_groups': [],
                    'fn_financial_information': [
                        {
                            'fn-type': 'financial-disclosure',
                            'look-like-award-id': [],
                            'look-like-funding-source': []
                        }
                    ],
                    'funding_sources': [],
                    'funding_statement': None,
                    'principal_award_recipients': []
                },
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_funding_sources_validation_fail_0_funding_0_award_in_fn_group_supported_by(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
                <back>
                    <fn-group>
                        <fn fn-type="supported-by">

                        </fn>
                    </fn-group>
                </back>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = list(FundingGroupValidation(
            xml_tree,
            special_chars_funding=['.', ','],
            special_chars_award_id=['/', '.', '-']
        ).funding_sources_exist_validation())
        expected = [
            {
                'title': 'Funding source element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'fn',
                'sub_item': "@fn-type='supported-by'",
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'at least 1 value for funding source',
                'got_value': '0 values that look like funding source and 0 values that look like award id',
                'message': 'Got 0 values that look like funding source and 0 values that look like award id, '
                           'expected at least 1 value for funding source',
                'advice': 'Provide value for funding source',
                'data': {
                    'ack': [],
                    'article_lang': "pt",
                    'article_type': "research-article",
                    'award_groups': [],
                    'fn_financial_information': [
                        {
                            'fn-type': 'supported-by',
                            'look-like-award-id': [],
                            'look-like-funding-source': []
                        }
                    ],
                    'funding_sources': [],
                    'funding_statement': None,
                    'principal_award_recipients': []
                },
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_funding_sources_validation_fail_1_funding_0_award_in_funding_group(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        obtained = list(FundingGroupValidation(
            xml_tree,
            special_chars_funding=['.', ','],
            special_chars_award_id=['/', '.', '-']
        ).funding_sources_exist_validation())
        expected = [
            {
                'title': 'Funding source element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'award-group',
                'sub_item': 'funding-source',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'at least 1 value for funding source and at least 1 value for award id',
                'got_value': '1 values for funding source and 0 values for award id',
                'message': 'Got 1 values for funding source and 0 values for award id, expected at least 1 value for '
                           'funding source and at least 1 value for award id',
                'advice': 'Provide value for award id or move funding source to <fn fn-type="supported-by">',
                'data': {
                    'ack': [],
                    'article_lang': "pt",
                    'article_type': "research-article",
                    'award_groups': [
                        {
                            'award-id': [],
                            'funding-source': ['Natural Science Foundation of Hunan Province']
                        }
                    ],
                    'fn_financial_information': [],
                    'funding_sources': ['Natural Science Foundation of Hunan Province'],
                    'funding_statement': None,
                    'principal_award_recipients': []
                },
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_funding_sources_validation_fail_1_funding_0_award_in_fn_group_financial_disclosure(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        obtained = list(FundingGroupValidation(
            xml_tree,
            special_chars_funding=['.', ','],
            special_chars_award_id=['/', '.', '-']
        ).funding_sources_exist_validation())
        expected = [
            {
                'title': 'Funding source element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'fn',
                'sub_item': "@fn-type='financial-disclosure'",
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'at least 1 value for funding source and at least 1 value for award id',
                'got_value': '1 values that look like funding source and 0 values that look like award id',
                'message': 'Got 1 values that look like funding source and 0 values that look like award id, '
                           'expected at least 1 value for funding source and at least 1 value for award id',
                'advice': 'Provide value for award id or move funding source to <fn fn-type="supported-by">',
                'data': {
                    'ack': [],
                    'article_lang': "pt",
                    'article_type': "research-article",
                    'award_groups': [],
                    'fn_financial_information': [
                        {
                            'fn-type': 'financial-disclosure',
                            'look-like-award-id': [],
                            'look-like-funding-source': ['Conselho Nacional de Desenvolvimento Científico e Tecnológico']
                        }
                    ],
                    'funding_sources': [],
                    'funding_statement': None,
                    'principal_award_recipients': []
                },
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_funding_sources_validation_fail_1_funding_0_award_in_fn_group_supported_by(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        obtained = list(FundingGroupValidation(
            xml_tree,
            special_chars_funding=['.', ','],
            special_chars_award_id=['/', '.', '-']
        ).funding_sources_exist_validation())
        expected = [
            {
                'title': 'Funding source element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'fn',
                'sub_item': "@fn-type='supported-by'",
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'at least 1 value for funding source',
                'got_value': '1 values that look like funding source and 0 values that look like award id',
                'message': 'Got 1 values that look like funding source and 0 values that look like award id, '
                           'expected at least 1 value for funding source',
                'advice': None,
                'data': {
                    'ack': [],
                    'article_lang': "pt",
                    'article_type': "research-article",
                    'award_groups': [],
                    'fn_financial_information': [
                        {
                            'fn-type': 'supported-by',
                            'look-like-award-id': [],
                            'look-like-funding-source': ['Conselho Nacional de Desenvolvimento Científico e Tecnológico']
                        }
                    ],
                    'funding_sources': [],
                    'funding_statement': None,
                    'principal_award_recipients': []
                },
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_funding_sources_validation_fail_0_funding_1_award_in_funding_group(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        obtained = list(FundingGroupValidation(
            xml_tree,
            special_chars_funding=['.', ','],
            special_chars_award_id=['/', '.', '-']
        ).funding_sources_exist_validation())
        expected = [
            {
                'title': 'Funding source element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'award-group',
                'sub_item': 'funding-source',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'at least 1 value for funding source and at least 1 value for award id',
                'got_value': '0 values for funding source and 1 values for award id',
                'message': 'Got 0 values for funding source and 1 values for award id, expected at least 1 value for '
                           'funding source and at least 1 value for award id',
                'advice': 'Provide value for funding source',
                'data': {
                    'ack': [],
                    'article_lang': "pt",
                    'article_type': "research-article",
                    'award_groups': [
                        {
                            'award-id': ['2019JJ40269'],
                            'funding-source': []
                        }
                    ],
                    'fn_financial_information': [],
                    'funding_sources': [],
                    'funding_statement': None,
                    'principal_award_recipients': []},
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_funding_sources_validation_fail_0_funding_1_award_in_fn_group_financial_disclosure(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        obtained = list(FundingGroupValidation(
            xml_tree,
            special_chars_funding=['.', ','],
            special_chars_award_id=['/', '.', '-']
        ).funding_sources_exist_validation())
        expected = [
            {
                'title': 'Funding source element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'fn',
                'sub_item': "@fn-type='financial-disclosure'",
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'at least 1 value for funding source and at least 1 value for award id',
                'got_value': '0 values that look like funding source and 1 values that look like award id',
                'message': 'Got 0 values that look like funding source and 1 values that look like award id, '
                           'expected at least 1 value for funding source and at least 1 value for award id',
                'advice': 'Provide value for funding source',
                'data': {
                    'ack': [],
                    'article_lang': "pt",
                    'article_type': "research-article",
                    'award_groups': [],
                    'fn_financial_information': [
                        {
                            'fn-type': 'financial-disclosure',
                            'look-like-award-id': ['2016/17640-0'],
                            'look-like-funding-source': []
                        }
                    ],
                    'funding_sources': [],
                    'funding_statement': None,
                    'principal_award_recipients': []},
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_funding_sources_validation_fail_0_funding_1_award_in_fn_group_supported_by(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        obtained = list(FundingGroupValidation(
            xml_tree,
            special_chars_funding=['.', ','],
            special_chars_award_id=['/', '.', '-']
        ).funding_sources_exist_validation())
        expected = [
            {
                'title': 'Funding source element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'fn',
                'sub_item': "@fn-type='supported-by'",
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'at least 1 value for funding source',
                'got_value': '0 values that look like funding source and 1 values that look like award id',
                'message': 'Got 0 values that look like funding source and 1 values that look like award id, '
                           'expected at least 1 value for funding source',
                'advice': 'Provide value for funding source',
                'data': {
                    'ack': [],
                    'article_lang': "pt",
                    'article_type': "research-article",
                    'award_groups': [],
                    'fn_financial_information': [
                        {
                            'fn-type': 'supported-by',
                            'look-like-award-id': ['2016/17640-0'],
                            'look-like-funding-source': []
                        }
                    ],
                    'funding_sources': [],
                    'funding_statement': None,
                    'principal_award_recipients': []},
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_award_id_format_validation_success(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        obtained = list(FundingGroupValidation(xml_tree).award_id_format_validation(callable_validation_success))
        expected = [
            {
                'title': 'Funding source element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'award-group',
                'sub_item': 'award-id',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '2019JJ40269',
                'got_value': '2019JJ40269',
                'message': 'Got 2019JJ40269, expected 2019JJ40269',
                'advice': None,
                'data': {
                    'ack': [],
                    'article_lang': "pt",
                    'article_type': "research-article",
                    'award_groups': [
                        {
                            'award-id': ['2019JJ40269'],
                            'funding-source': ['Natural Science Foundation of Hunan Province']
                        },
                        {
                            'award-id': ['2020CFB547'],
                            'funding-source': ['Hubei Provincial Natural Science Foundation of China']
                        }
                    ],
                    'fn_financial_information': [],
                    'funding_sources': [
                        'Natural Science Foundation of Hunan Province',
                        'Hubei Provincial Natural Science Foundation of China'
                    ],
                    'funding_statement': None,
                    'principal_award_recipients': []
                },
            },
            {
                'title': 'Funding source element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'award-group',
                'sub_item': 'award-id',
                'validation_type': 'format',
                'response': 'OK',
                'expected_value': '2020CFB547',
                'got_value': '2020CFB547',
                'message': 'Got 2020CFB547, expected 2020CFB547',
                'advice': None,
                'data': {
                    'ack': [],
                    'article_lang': "pt",
                    'article_type': "research-article",
                    'award_groups': [
                        {
                            'award-id': ['2019JJ40269'],
                            'funding-source': ['Natural Science Foundation of Hunan Province']
                        },
                        {
                            'award-id': ['2020CFB547'],
                            'funding-source': ['Hubei Provincial Natural Science Foundation of China']
                        }
                    ],
                    'fn_financial_information': [],
                    'funding_sources': [
                        'Natural Science Foundation of Hunan Province',
                        'Hubei Provincial Natural Science Foundation of China'
                    ],
                    'funding_statement': None,
                    'principal_award_recipients': []
                },
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_award_id_format_validation_fail(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        obtained = list(FundingGroupValidation(xml_tree).award_id_format_validation(callable_validation_fail))
        expected = [
            {
                'title': 'Funding source element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'award-group',
                'sub_item': 'award-id',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a valid value for award id',
                'got_value': '2019JJ40269',
                'message': 'Got 2019JJ40269, expected a valid value for award id',
                'advice': 'Provide a valid value for award id',
                'data': {
                    'ack': [],
                    'article_lang': "pt",
                    'article_type': "research-article",
                    'award_groups': [
                        {
                            'award-id': ['2019JJ40269'],
                            'funding-source': ['Natural Science Foundation of Hunan Province']
                        },
                        {
                            'award-id': ['2020CFB547'],
                            'funding-source': ['Hubei Provincial Natural Science Foundation of China']
                        }
                    ],
                    'fn_financial_information': [],
                    'funding_sources': [
                        'Natural Science Foundation of Hunan Province',
                        'Hubei Provincial Natural Science Foundation of China'
                    ],
                    'funding_statement': None,
                    'principal_award_recipients': []
                },
            },
            {
                'title': 'Funding source element validation',
                'parent': 'article',
                'parent_article_type': "research-article",
                'parent_id': None,
                'parent_lang': "pt",
                'item': 'award-group',
                'sub_item': 'award-id',
                'validation_type': 'format',
                'response': 'ERROR',
                'expected_value': 'a valid value for award id',
                'got_value': '2020CFB547',
                'message': 'Got 2020CFB547, expected a valid value for award id',
                'advice': 'Provide a valid value for award id',
                'data': {
                    'ack': [],
                    'article_lang': "pt",
                    'article_type': "research-article",
                    'award_groups': [
                        {
                            'award-id': ['2019JJ40269'],
                            'funding-source': ['Natural Science Foundation of Hunan Province']
                        },
                        {
                            'award-id': ['2020CFB547'],
                            'funding-source': ['Hubei Provincial Natural Science Foundation of China']
                        }
                    ],
                    'fn_financial_information': [],
                    'funding_sources': [
                        'Natural Science Foundation of Hunan Province',
                        'Hubei Provincial Natural Science Foundation of China'
                    ],
                    'funding_statement': None,
                    'principal_award_recipients': []
                },
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_award_id_format_validation_fail_without_funding_group(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>

                    </article-meta>
                </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = list(FundingGroupValidation(xml_tree).award_id_format_validation(callable_validation_fail))
        self.assertEqual([], obtained)

    def test_award_id_format_validation_fail_without_award_id(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
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
        obtained = list(FundingGroupValidation(xml_tree).award_id_format_validation(callable_validation_fail))
        self.assertEqual([], obtained)


if __name__ == '__main__':
    unittest.main()
