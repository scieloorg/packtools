from unittest import TestCase

from lxml import etree

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation.article_and_subarticles import (
    ArticleLangValidation,
    ArticleAttribsValidation,
    ArticleTypeValidation,
    ArticleIdValidation, JATSAndDTDVersionValidation,
)



class ArticleAndSubarticlesTest(TestCase):

    def setUp(self):
        self.params = {
            "language_codes_list": ["pt", "en", "es"],
            "language_error_level": "CRITICAL",
            "specific_use_list": {
                "sps-1.1": ["1.0"],
                "sps-1.2": ["1.0"],
                "sps-1.3": ["1.0"],
                "sps-1.4": ["1.0"],
                "sps-1.5": ["1.0"],
                "sps-1.6": ["1.0"],
                "sps-1.7": ["1.0", "1.1"],
                "sps-1.8": ["1.0", "1.1"],
                "sps-1.9": ["1.1"],
                "sps-1.10": ["1.1", "1.2", "1.3"]
            },
            "specific_use_error_level": "CRITICAL",
            "dtd_version_list": ["1.1", "1.2", "1.3"],
            "dtd_version_error_level": "CRITICAL",
            "article_type_list": ["research-article"],
            "article_type_list_error_level": "CRITICAL",
            "subjects_list": [
                {"subject": "Original Article", "lang": "en"},
                {"subject": "Artigo Original", "lang": "pt"},
                {"subject": "Artículo Original", "lang": "es"},
            ],
            "target_article_types": ["research-article"],
            "expected_similarity": 0.7,
            "expected_similarity_error_level": "CRITICAL",
            "id_other_error_level": "CRITICAL",
            "jats_and_dtd_version_error_level": "CRITICAL"
        }

    def test_article_has_no_language_attribute(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">zTn4sYXBrfSTMNVPF5Dm7jr</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0103-50532014001202258</article-id>
                    <article-id pub-id-type="doi">10.5935/0103-5053.20140192</article-id>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = ArticleLangValidation(xml_tree, self.params).validate_language()

        expected = [
            {
                "title": "text language",
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': None,
                'item': 'article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "CRITICAL",
                "expected_value": "one of ['pt', 'en', 'es']",
                "got_value": None,
                'message': "Got None, expected one of ['pt', 'en', 'es']",
                "advice": "Provide for article/@xml:lang one of ['pt', 'en', 'es']",
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'parent_name': 'article',
                    'lang': None,
                    'line_number': 2,
                    'subject': None
                }
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_article_has_valid_language(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">zTn4sYXBrfSTMNVPF5Dm7jr</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0103-50532014001202258</article-id>
                    <article-id pub-id-type="doi">10.5935/0103-5053.20140192</article-id>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = ArticleLangValidation(xml_tree, self.params).validate_language()

        expected = [
            {
                "title": "text language",
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'en',
                'item': 'article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": "en",
                "got_value": "en",
                "message": "Got en, expected one of ['pt', 'en', 'es']",
                "advice": None,
                "data": {
                    "parent_name": "article",
                    "article_id": None,
                    'article_type': 'research-article',
                    'lang': 'en',
                    'line_number': 2,
                    'subject': None
                }
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_article_has_invalid_language(self):
        self.maxDiff = None
        xml_str = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="e">
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v3">zTn4sYXBrfSTMNVPF5Dm7jr</article-id>
                    <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0103-50532014001202258</article-id>
                    <article-id pub-id-type="doi">10.5935/0103-5053.20140192</article-id>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = ArticleLangValidation(xml_tree, self.params).validate_language()

        expected = [
            {
                "title": "text language",
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'e',
                'item': 'article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "CRITICAL",
                "expected_value": "one of ['pt', 'en', 'es']",
                "got_value": "e",
                'message': "Got e, expected one of ['pt', 'en', 'es']",
                "advice": "Provide for article/@xml:lang one of ['pt', 'en', 'es']",
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'parent_name': 'article',
                    'lang': 'e',
                    'line_number': 2,
                    'subject': None
                }
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_article_and_subarticles_have_valid_languages(self):
        self.maxDiff = None
        with open("tests/samples/article-abstract-en-sub-articles-pt-es.xml") as data:
            xml_tree = get_xml_tree(data.read())

        obtained = ArticleLangValidation(xml_tree, self.params).validate_language()

        expected = [
            {
                "title": 'text language',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'en',
                'item': 'article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": 'en',
                "got_value": "en",
                'message': "Got en, expected one of ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'parent_name': 'article',
                    'lang': 'en',
                    'line_number': 2,
                    'subject': 'Original Article'
                },
            },
            {
                "title": 'text language',
                'parent': 'sub-article',
                'parent_id': 's1',
                'parent_article_type': 'translation',
                'parent_lang': 'pt',
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": 'pt',
                "got_value": "pt",
                'message': "Got pt, expected one of ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': 's1',
                    'article_type': 'translation',
                    'parent_name': 'sub-article',
                    'lang': 'pt',
                    'line_number': 1307,
                    'subject': 'Artigo Original'
                },
            },
            {
                "title": 'text language',
                'parent': 'sub-article',
                'parent_id': 's2',
                'parent_article_type': 'translation',
                'parent_lang': 'es',
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": 'es',
                "got_value": "es",
                'message': "Got es, expected one of ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': 's2',
                    'article_type': 'translation',
                    'parent_name': 'sub-article',
                    'lang': 'es',
                    'line_number': 1527,
                    'subject': 'Artículo Original'
                },

            },
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_article_and_subarticles_with_three_valid_languages(self):
        self.maxDiff = None
        xml_str = """
        <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink">
            <sub-article article-type="translation" id="s1" xml:lang="pt">
            </sub-article>
            <sub-article article-type="translation" id="s2" xml:lang="es">
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleLangValidation(xml_tree, self.params).validate_language()

        expected = [
            {
                "title": 'text language',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'en',
                'item': 'article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": "en",
                "got_value": "en",
                'message': "Got en, expected one of ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'parent_name': 'article',
                    'lang': 'en',
                    'line_number': 2,
                    'subject': None
                },
            },
            {
                "title": 'text language',
                'parent': 'sub-article',
                'parent_id': 's1',
                'parent_article_type': 'translation',
                'parent_lang': 'pt',
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": "pt",
                "got_value": "pt",
                'message': "Got pt, expected one of ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': 's1',
                    'article_type': 'translation',
                    'parent_name': 'sub-article',
                    'lang': 'pt',
                    'line_number': 3,
                    'subject': None
                },
            },
            {
                "title": 'text language',
                'parent': 'sub-article',
                'parent_id': 's2',
                'parent_article_type': 'translation',
                'parent_lang': 'es',
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": "es",
                "got_value": "es",
                'message': "Got es, expected one of ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': 's2',
                    'article_type': 'translation',
                    'parent_name': 'sub-article',
                    'lang': 'es',
                    'line_number': 5,
                    'subject': None
                },
            },
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_article_and_subarticles_with_two_valid_languages_and_one_invalid(self):
        self.maxDiff = None
        xml_str = """
        <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink">
            <sub-article article-type="translation" id="s1" xml:lang="pt">
            </sub-article>
            <sub-article article-type="translation" id="s2" xml:lang="">
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleLangValidation(xml_tree, self.params).validate_language()

        expected = [
            {
                "title": 'text language',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'en',
                'item': 'article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": 'en',
                "got_value": "en",
                'message': "Got en, expected one of ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'parent_name': 'article',
                    'lang': 'en',
                    'line_number': 2,
                    'subject': None
                },
            },
            {
                "title": 'text language',
                'parent': 'sub-article',
                'parent_id': 's1',
                'parent_article_type': 'translation',
                'parent_lang': 'pt',
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": "pt",
                "got_value": "pt",
                'message': "Got pt, expected one of ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': 's1',
                    'article_type': 'translation',
                    'parent_name': 'sub-article',
                    'lang': 'pt',
                    'line_number': 3,
                    'subject': None
                },
            },
            {
                "title": 'text language',
                'parent': 'sub-article',
                'parent_id': 's2',
                'parent_article_type': 'translation',
                'parent_lang': '',
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "CRITICAL",
                "expected_value": "one of ['pt', 'en', 'es']",
                "got_value": "",
                'message': "Got , expected one of ['pt', 'en', 'es']",
                "advice": 'Provide for sub-article[@id="s2"]/@xml:lang one of [\'pt\', \'en\', \'es\']',
                'data': {
                    'article_id': 's2',
                    'article_type': 'translation',
                    'parent_name': 'sub-article',
                    'lang': '',
                    'line_number': 5,
                    'subject': None
                }
            },
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_article_and_subarticles_with_one_valid_language_one_empty_and_one_invalid(self):
        self.maxDiff = None
        xml_str = """
        <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink">
            <sub-article article-type="translation" id="s1">
            </sub-article>
            <sub-article article-type="translation" id="s2" xml:lang="">
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleLangValidation(xml_tree, self.params).validate_language()

        expected = [
            {
                "title": 'text language',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'en',
                'item': 'article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": 'en',
                "got_value": "en",
                'message': "Got en, expected one of ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'parent_name': 'article',
                    'lang': 'en',
                    'line_number': 2,
                    'subject': None
                },
            },
            {
                "title": 'text language',
                'parent': 'sub-article',
                'parent_id': 's1',
                'parent_article_type': 'translation',
                'parent_lang': None,
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "CRITICAL",
                "expected_value": "one of ['pt', 'en', 'es']",
                "got_value": None,
                'message': "Got None, expected one of ['pt', 'en', 'es']",
                "advice": 'Provide for sub-article[@id="s1"]/@xml:lang one of [\'pt\', \'en\', \'es\']',
                'data': {
                    'article_id': 's1',
                    'article_type': 'translation',
                    'parent_name': 'sub-article',
                    'lang': None,
                    'line_number': 3,
                    'subject': None
                },
            },
            {
                "title": 'text language',
                'parent': 'sub-article',
                'parent_id': 's2',
                'parent_article_type': 'translation',
                'parent_lang': '',
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "CRITICAL",
                "expected_value": "one of ['pt', 'en', 'es']",
                "got_value": "",
                'message': "Got , expected one of ['pt', 'en', 'es']",
                "advice": 'Provide for sub-article[@id="s2"]/@xml:lang one of [\'pt\', \'en\', \'es\']',
                'data': {
                    'article_id': 's2',
                    'article_type': 'translation',
                    'parent_name': 'sub-article',
                    'lang': '',
                    'line_number': 5,
                    'subject': None
                },
            },
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_article_and_subarticles_with_two_invalid_languages(self):
        self.maxDiff = None
        xml_str = """
        <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="portugol" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink">
            <sub-article article-type="translation" id="s1" xml:lang="en">
            </sub-article>
            <sub-article article-type="translation" id="s2" xml:lang="thisisaninvalidlanguagecode">
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = ArticleLangValidation(xml_tree, self.params).validate_language()

        expected = [
            {
                "title": 'text language',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'portugol',
                'item': 'article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "CRITICAL",
                "expected_value": "one of ['pt', 'en', 'es']",
                "got_value": "portugol",
                'message': "Got portugol, expected one of ['pt', 'en', 'es']",
                "advice": "Provide for article/@xml:lang one of ['pt', 'en', 'es']",
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'parent_name': 'article',
                    'lang': 'portugol',
                    'line_number': 2,
                    'subject': None
                },
            },
            {
                "title": 'text language',
                'parent': 'sub-article',
                'parent_id': 's1',
                'parent_article_type': 'translation',
                'parent_lang': 'en',
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": "en",
                "got_value": "en",
                'message': "Got en, expected one of ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': 's1',
                    'article_type': 'translation',
                    'parent_name': 'sub-article',
                    'lang': 'en',
                    'line_number': 3,
                    'subject': None
                },
            },
            {
                "title": 'text language',
                'parent': 'sub-article',
                'parent_id': 's2',
                'parent_article_type': 'translation',
                'parent_lang': 'thisisaninvalidlanguagecode',
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "CRITICAL",
                "expected_value": "one of ['pt', 'en', 'es']",
                "got_value": "thisisaninvalidlanguagecode",
                'message': "Got thisisaninvalidlanguagecode, expected one of ['pt', 'en', 'es']",
                "advice": 'Provide for sub-article[@id="s2"]/@xml:lang one of [\'pt\', \'en\', \'es\']',
                'data': {
                    'article_id': 's2',
                    'article_type': 'translation',
                    'parent_name': 'sub-article',
                    'lang': 'thisisaninvalidlanguagecode',
                    'line_number': 5,
                    'subject': None
                }
            },
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_article_and_subarticles_specific_use(self):
        self.maxDiff = None
        xml_str = """
        <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="portugol" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink">
            <sub-article article-type="translation" id="s1" xml:lang="en">
            </sub-article>
            <sub-article article-type="translation" id="s2" xml:lang="thisisaninvalidlanguagecode">
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = list(
            ArticleAttribsValidation(xml_tree, self.params).validate_specific_use()
        )

        expected = [
            {
                "title": 'article/@specific-use',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'portugol',
                'item': 'article',
                'sub_item': '@specific-use',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": 'sps-1.9',
                "got_value": "sps-1.9",
                'message': "Got sps-1.9, expected one of ['sps-1.1', 'sps-1.2', 'sps-1.3', 'sps-1.4', 'sps-1.5', 'sps-1.6', 'sps-1.7', 'sps-1.8', 'sps-1.9', 'sps-1.10']",
                "advice": None,
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'parent_name': 'article',
                    'dtd_version': '1.1',
                    'lang': 'portugol',
                    'line_number': 2,
                    'specific_use': 'sps-1.9',
                    'subject': None
                },
            }
        ]

        self.assertEqual(obtained, expected)

    def test_article_and_subarticles_without_specific_use(self):
        self.maxDiff = None
        xml_str = """
        <article article-type="research-article" dtd-version="1.1" xml:lang="portugol" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink">
            <sub-article article-type="translation" id="s1" xml:lang="en">
            </sub-article>
            <sub-article article-type="translation" id="s2" xml:lang="thisisaninvalidlanguagecode">
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = list(
            ArticleAttribsValidation(xml_tree, self.params).validate_specific_use()
        )

        expected = [
            {
                "title": "article/@specific-use",
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'portugol',
                'item': 'article',
                'sub_item': '@specific-use',
                "validation_type": "value in list",
                "response": "CRITICAL",
                "expected_value": "one of ['sps-1.1', 'sps-1.2', 'sps-1.3', 'sps-1.4', 'sps-1.5', 'sps-1.6', 'sps-1.7', 'sps-1.8', 'sps-1.9', 'sps-1.10']",
                "got_value": None,
                'message': "Got None, expected one of ['sps-1.1', 'sps-1.2', 'sps-1.3', 'sps-1.4', 'sps-1.5', 'sps-1.6', 'sps-1.7', 'sps-1.8', 'sps-1.9', 'sps-1.10']",
                "advice": "Provide for article/@specific-use one of ['sps-1.1', 'sps-1.2', 'sps-1.3', 'sps-1.4', 'sps-1.5', 'sps-1.6', 'sps-1.7', 'sps-1.8', 'sps-1.9', 'sps-1.10']",
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'parent_name': 'article',
                    'dtd_version': '1.1',
                    'lang': 'portugol',
                    'line_number': 2,
                    'specific_use': None,
                    'subject': None
                },
            }
        ]

        self.assertEqual(obtained, expected)

    def test_article_and_subarticles_dtd_version(self):
        self.maxDiff = None
        xml_str = """
        <article article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="portugol" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink">
            <sub-article article-type="translation" id="s1" xml:lang="en">
            </sub-article>
            <sub-article article-type="translation" id="s2" xml:lang="thisisaninvalidlanguagecode">
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = list(
            ArticleAttribsValidation(xml_tree, self.params).validate_dtd_version()
        )

        expected = [
            {
                "title": 'article/@dtd-version',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'portugol',
                'item': 'article',
                'sub_item': '@dtd-version',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": '1.1',
                "got_value": "1.1",
                'message': "Got 1.1, expected one of ['1.1', '1.2', '1.3']",
                "advice": None,
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'parent_name': 'article',
                    'dtd_version': '1.1',
                    'lang': 'portugol',
                    'line_number': 2,
                    'specific_use': 'sps-1.9',
                    'subject': None
                },
            }
        ]

        self.assertEqual(obtained, expected)

    def test_article_and_subarticles_article_type_is_valid(self):
        self.maxDiff = None
        xml_str = """
        <article article-type="research-article" specific-use="sps-1.9" xml:lang="portugol" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink">
            <sub-article article-type="translation" id="s1" xml:lang="en">
            </sub-article>
            <sub-article article-type="translation" id="s2" xml:lang="thisisaninvalidlanguagecode">
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = list(
            ArticleTypeValidation(xml_tree, self.params).validate_article_type()
        )

        expected = [
            {
                "title": 'article/@article-type',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'portugol',
                'item': 'article',
                'sub_item': '@article-type',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": "research-article",
                "got_value": "research-article",
                'message': "Got research-article, expected one of ['research-article']",
                "advice": None,
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'parent_name': 'article',
                    'dtd_version': None,
                    'lang': 'portugol',
                    'line_number': 2,
                    'specific_use': 'sps-1.9',
                    'subject': None
                }
            }
        ]

        self.assertEqual(obtained, expected)

    def test_article_and_subarticles_article_type_is_not_valid(self):
        self.maxDiff = None
        xml_str = """
        <article article-type="main" specific-use="sps-1.9" xml:lang="portugol" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink">
            <sub-article article-type="translation" id="s1" xml:lang="en">
            </sub-article>
            <sub-article article-type="translation" id="s2" xml:lang="thisisaninvalidlanguagecode">
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = list(
            ArticleTypeValidation(xml_tree, self.params).validate_article_type()
        )

        expected = [
            {
                "title": 'article/@article-type',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'main',
                'parent_lang': 'portugol',
                'item': 'article',
                'sub_item': '@article-type',
                "validation_type": "value in list",
                "response": "CRITICAL",
                "expected_value": "one of ['research-article']",
                "got_value": "main",
                'message': "Got main, expected one of ['research-article']",
                "advice": "Provide for article/@article-type one of ['research-article']",
                'data': {
                    'article_id': None,
                    'article_type': 'main',
                    'parent_name': 'article',
                    'dtd_version': None,
                    'lang': 'portugol',
                    'line_number': 2,
                    'specific_use': 'sps-1.9',
                    'subject': None
                },
            }
        ]

        self.assertEqual(obtained, expected)

    def test_article_and_subarticles_article_type_vs_subject_similarity(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
                <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
                <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                        <subject>Scientific Article</subject>
                        </subj-group>
                    </article-categories>
                <sub-article article-type="translation" id="s1" xml:lang="pt">
                    <article-categories>
                        <subj-group subj-group-type="heading">
                        <subject>Artigo Científico</subject>
                        </subj-group>
                    </article-categories>
                </sub-article>
                <sub-article article-type="translation" id="s2" xml:lang="es">
                    <article-categories>
                        <subj-group subj-group-type="heading">
                        <subject>Artículo Científico</subject>
                        </subj-group>
                    </article-categories>
                </sub-article>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = ArticleTypeValidation(xml_tree, self.params).validate_article_type_vs_subject_similarity()

        expected = [
            {
                "title": "Article type vs subjects validation",
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'en',
                'item': 'article',
                'sub_item': '@article-type',
                "validation_type": "similarity",
                "response": "CRITICAL",
                "expected_value": 0.7,
                "got_value": 0.6818181818181818,
                'message': 'Got 0.6818181818181818, expected 0.7',
                "advice": "The subject Scientific Article (en) does not match the items provided in the list: "
                "Original Article (en) | Artigo Original (pt) | Artículo Original (es)",
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'parent_name': 'article',
                    'dtd_version': '1.1',
                    'lang': 'en',
                    'line_number': 3,
                    'specific_use': 'sps-1.9',
                    'subject': 'Scientific Article'
                },
            },
            {
                "title": "Article type vs subjects validation",
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'en',
                'item': 'article',
                'sub_item': '@article-type',
                "validation_type": "similarity",
                "response": "ERROR",
                "expected_value": 0.7,
                "got_value": 0.6190476190476191,
                'message': 'Got 0.6190476190476191, expected 0.7',
                "advice": "The subject Artigo Científico (pt) does not match the items provided in the list: "
                "Original Article (en) | Artigo Original (pt) | Artículo Original (es)",
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'parent_name': 'article',
                    'dtd_version': '1.1',
                    'lang': 'en',
                    'line_number': 3,
                    'specific_use': 'sps-1.9',
                    'subject': 'Scientific Article'
                },
            },
            {
                "title": "Article type vs subjects validation",
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'en',
                'item': 'article',
                'sub_item': '@article-type',
                "validation_type": "similarity",
                "response": "ERROR",
                "expected_value": 0.7,
                "got_value": 0.6521739130434783,
                'message': 'Got 0.6521739130434783, expected 0.7',
                "advice": "The subject Artículo Científico (es) does not match the items provided in the list: "
                "Original Article (en) | Artigo Original (pt) | Artículo Original (es)",
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'parent_name': 'article',
                    'dtd_version': '1.1',
                    'lang': 'en',
                    'line_number': 3,
                    'specific_use': 'sps-1.9',
                    'subject': 'Scientific Article'
                },
            },
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_article_and_subarticles_validate_article_id_other_is_ok(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
            <article-id pub-id-type="other">123</article-id>
            </article-meta>
            </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = list(ArticleIdValidation(xml_tree, self.params).validate_article_id_other())

        expected = [
            {
                "title": 'article-id (@pub-id-type="other")',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'en',
                'item': 'article-id',
                'sub_item': '@pub-id-type="other"',
                "validation_type": "format",
                "response": "OK",
                "expected_value": "123",
                "got_value": "123",
                'message': 'Got 123, expected numerical value from 1 to 99999',
                "advice": None,
                'data': {
                    'other': '123',
                    'v2': 'S0104-11692020000100303',
                    'v3': 'TPg77CCrGj4wcbLCh9vG8bS'
                },
            }
        ]
        self.assertEqual(expected, obtained)

    def test_article_and_subarticles_validate_article_id_other_non_numeric_digit(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
            <article-id pub-id-type="other">x23</article-id>
            </article-meta>
            </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = list(ArticleIdValidation(xml_tree, self.params).validate_article_id_other())

        expected = [
            {
                "title": 'article-id (@pub-id-type="other")',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'en',
                'item': 'article-id',
                'sub_item': '@pub-id-type="other"',
                "validation_type": "format",
                "response": "CRITICAL",
                'expected_value': 'numerical value from 1 to 99999',
                "got_value": "x23",
                'message': 'Got x23, expected numerical value from 1 to 99999',
                "advice": 'Provide for <article-id pub-id-type="other"> numerical value from 1 to 99999',
                'data': {
                    'other': 'x23',
                    'v2': 'S0104-11692020000100303',
                    'v3': 'TPg77CCrGj4wcbLCh9vG8bS'
                },
            }
        ]
        self.assertEqual(expected, obtained)

    def test_article_and_subarticles_validate_article_id_other_with_more_than_five_digits(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
            <article-id pub-id-type="other">123456</article-id>
            </article-meta>
            </front>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = list(ArticleIdValidation(xml_tree, self.params).validate_article_id_other())

        expected = [
            {
                "title": 'article-id (@pub-id-type="other")',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'en',
                'item': 'article-id',
                'sub_item': '@pub-id-type="other"',
                "validation_type": "format",
                "response": "CRITICAL",
                "expected_value": 'numerical value from 1 to 99999',
                "got_value": "123456",
                'message': 'Got 123456, expected numerical value from 1 to 99999',
                "advice": 'Provide for <article-id pub-id-type="other"> numerical value from 1 to 99999',
                'data': {
                    'other': '123456',
                    'v2': 'S0104-11692020000100303',
                    'v3': 'TPg77CCrGj4wcbLCh9vG8bS'
                },
            }
        ]
        self.assertEqual(expected, obtained)

    def test_article_and_subarticles_without_dtd_version(self):
        self.maxDiff = None
        xml_str = """
        <article article-type="research-article" specific-use="sps-1.9" xml:lang="portugol" xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink">
            <sub-article article-type="translation" id="s1" xml:lang="en">
            </sub-article>
            <sub-article article-type="translation" id="s2" xml:lang="thisisaninvalidlanguagecode">
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = list(
            ArticleAttribsValidation(xml_tree, self.params).validate_dtd_version()
        )

        expected = [
            {
                "title": "article/@dtd-version",
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article',
                'parent_lang': 'portugol',
                'item': 'article',
                'sub_item': '@dtd-version',
                "validation_type": "value in list",
                "response": "CRITICAL",
                "expected_value": "one of ['1.1', '1.2', '1.3']",
                "got_value": None,
                'message': "Got None, expected one of ['1.1', '1.2', '1.3']",
                'advice': "Provide for article/@dtd-version one of ['1.1', '1.2', '1.3']",
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'parent_name': 'article',
                    'dtd_version': None,
                    'lang': 'portugol',
                    'line_number': 2,
                    'specific_use': 'sps-1.9',
                    'subject': None
                },
            }
        ]

        self.assertEqual(obtained, expected)

    def test_validate_jats_and_dtd_version(self):
        xml_str = """
        <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.3 20210610//EN" "JATS-journalpublishing1-3.dtd">
        <article article-type="research-article" dtd-version="1.1" xml:lang="en" specific-use="sps-1.9"
                 xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink">
        </article>
        """

        xml_tree = etree.fromstring(xml_str)

        # Instancia a classe de validação
        validator = JATSAndDTDVersionValidation(xml_tree, self.params)

        # Executa a validação
        obtained = list(validator.validate())

        # Resultado esperado
        expected = []

        # Verifica se a validação foi bem-sucedida
        self.assertEqual(obtained, expected)

    def test_validate_jats_and_dtd_version_incompatible(self):
        self.maxDiff = None
        xml_str = """
        <!DOCTYPE article PUBLIC "-//NLM//DTD JATS (Z39.96) Journal Publishing DTD v1.1 20210610//EN" "JATS-journalpublishing1-1.dtd">
        <article article-type="research-article" dtd-version="1.0" xml:lang="en" specific-use="sps-1.9"
                 xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink">
        </article>
        """

        xml_tree = etree.fromstring(xml_str)

        # Instancia a classe de validação
        validator = JATSAndDTDVersionValidation(xml_tree, self.params)

        # Executa a validação
        obtained = list(validator.validate())

        # Resultado esperado
        expected = [
            {
                "title": 'article-id (@pub-id-type="other")',
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "research-article",
                "parent_lang": "en",
                "item": "dtd-version",
                "sub_item": None,
                "validation_type": "match",
                'message': "Got 1.0, expected ['1.1']",
                "advice": "Incompatibility: SPS sps-1.9 is not compatible with JATS 1.0.",
                "response": "CRITICAL",
                'data': [
                    {
                        'article_id': None,
                        'article_type': 'research-article',
                        'lang': 'en',
                        'line_number': 4,
                        'parent_name': 'article',
                        'subject': None
                    }
                ],
               'expected_value': ['1.1'],
               'got_value': '1.0',
            }
        ]

        # Verifica se o resultado obtido é igual ao esperado
        self.assertEqual(obtained, expected)
