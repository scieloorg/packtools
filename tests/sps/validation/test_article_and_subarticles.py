from unittest import TestCase

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation.article_and_subarticles import (
    ArticleLangValidation,
    ArticleAttribsValidation,
    ArticleTypeValidation,
    ArticleSubjectsValidation,
    ArticleIdValidation,
)


class ArticleAndSubarticlesTest(TestCase):
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

        obtained = ArticleLangValidation(xml_tree).validate_language(
            language_codes_list=["pt", "en", "es"]
        )

        expected = [
            {
                "title": "Article element lang attribute validation",
                'parent': 'article',
                'parent_id': None,
                'item': 'article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": ["pt", "en", "es"],
                "got_value": None,
                'message': "Got None, expected ['pt', 'en', 'es']",
                "advice": "<article article-type=research-article xml:lang=None> has None as language, expected one item of this list: pt | en | es",
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
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

        obtained = ArticleLangValidation(xml_tree).validate_language(
            language_codes_list=["pt", "en", "es"]
        )

        expected = [
            {
                "title": "Article element lang attribute validation",
                'parent': 'article',
                'parent_id': None,
                'item': 'article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["pt", "en", "es"],
                "got_value": "en",
                "message": "Got en, expected ['pt', 'en', 'es']",
                "advice": None,
                "data": {
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

        obtained = ArticleLangValidation(xml_tree).validate_language(
            language_codes_list=["pt", "en", "es"]
        )

        expected = [
            {
                "title": "Article element lang attribute validation",
                'parent': 'article',
                'parent_id': None,
                'item': 'article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": ["pt", "en", "es"],
                "got_value": "e",
                'message': "Got e, expected ['pt', 'en', 'es']",
                "advice": "<article article-type=research-article xml:lang=e> has e as language, expected one item of this list: pt | en | es",
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
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

        obtained = ArticleLangValidation(xml_tree).validate_language(
            language_codes_list=["pt", "en", "es"]
        )

        expected = [
            {
                "title": "Article element lang attribute validation",
                'parent': 'article',
                'parent_id': None,
                'item': 'article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["pt", "en", "es"],
                "got_value": "en",
                'message': "Got en, expected ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'lang': 'en',
                    'line_number': 2,
                    'subject': 'Original Article'
                },
            },
            {
                "title": "Article element lang attribute validation",
                'parent': 'sub-article',
                'parent_id': 's1',
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["pt", "en", "es"],
                "got_value": "pt",
                'message': "Got pt, expected ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': 's1',
                    'article_type': 'translation',
                    'lang': 'pt',
                    'line_number': 1307,
                    'subject': 'Artigo Original'
                },
            },
            {
                "title": "Article element lang attribute validation",
                'parent': 'sub-article',
                'parent_id': 's2',
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["pt", "en", "es"],
                "got_value": "es",
                'message': "Got es, expected ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': 's2',
                    'article_type': 'translation',
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
        obtained = ArticleLangValidation(xml_tree).validate_language(
            language_codes_list=["pt", "en", "es"]
        )

        expected = [
            {
                "title": "Article element lang attribute validation",
                'parent': 'article',
                'parent_id': None,
                'item': 'article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["pt", "en", "es"],
                "got_value": "en",
                'message': "Got en, expected ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'lang': 'en',
                    'line_number': 2,
                    'subject': None
                },
            },
            {
                "title": "Article element lang attribute validation",
                'parent': 'sub-article',
                'parent_id': 's1',
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["pt", "en", "es"],
                "got_value": "pt",
                'message': "Got pt, expected ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': 's1',
                    'article_type': 'translation',
                    'lang': 'pt',
                    'line_number': 3,
                    'subject': None
                },
            },
            {
                "title": "Article element lang attribute validation",
                'parent': 'sub-article',
                'parent_id': 's2',
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["pt", "en", "es"],
                "got_value": "es",
                'message': "Got es, expected ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': 's2',
                    'article_type': 'translation',
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
        obtained = ArticleLangValidation(xml_tree).validate_language(
            language_codes_list=["pt", "en", "es"]
        )

        expected = [
            {
                "title": "Article element lang attribute validation",
                'parent': 'article',
                'parent_id': None,
                'item': 'article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["pt", "en", "es"],
                "got_value": "en",
                'message': "Got en, expected ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'lang': 'en',
                    'line_number': 2,
                    'subject': None
                },
            },
            {
                "title": "Article element lang attribute validation",
                'parent': 'sub-article',
                'parent_id': 's1',
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["pt", "en", "es"],
                "got_value": "pt",
                'message': "Got pt, expected ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': 's1',
                    'article_type': 'translation',
                    'lang': 'pt',
                    'line_number': 3,
                    'subject': None
                },
            },
            {
                "title": "Article element lang attribute validation",
                'parent': 'sub-article',
                'parent_id': 's2',
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": ["pt", "en", "es"],
                "got_value": "",
                'message': "Got , expected ['pt', 'en', 'es']",
                "advice": "<sub-article article-type=translation id=s2 xml:lang=> has  as language, expected one item of this list: pt | en | es",
                'data': {
                    'article_id': 's2',
                    'article_type': 'translation',
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
        obtained = ArticleLangValidation(xml_tree).validate_language(
            language_codes_list=["pt", "en", "es"]
        )

        expected = [
            {
                "title": "Article element lang attribute validation",
                'parent': 'article',
                'parent_id': None,
                'item': 'article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["pt", "en", "es"],
                "got_value": "en",
                'message': "Got en, expected ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'lang': 'en',
                    'line_number': 2,
                    'subject': None
                },
            },
            {
                "title": "Article element lang attribute validation",
                'parent': 'sub-article',
                'parent_id': 's1',
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": ["pt", "en", "es"],
                "got_value": None,
                'message': "Got None, expected ['pt', 'en', 'es']",
                "advice": "<sub-article article-type=translation id=s1 xml:lang=None> has None as language, expected one item of this list: pt | en | es",
                'data': {
                    'article_id': 's1',
                    'article_type': 'translation',
                    'lang': None,
                    'line_number': 3,
                    'subject': None
                },
            },
            {
                "title": "Article element lang attribute validation",
                'parent': 'sub-article',
                'parent_id': 's2',
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": ["pt", "en", "es"],
                "got_value": "",
                'message': "Got , expected ['pt', 'en', 'es']",
                "advice": "<sub-article article-type=translation id=s2 xml:lang=> has  as language, expected one item of this list: pt | en | es",
                'data': {
                    'article_id': 's2',
                    'article_type': 'translation',
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

        obtained = ArticleLangValidation(xml_tree).validate_language(
            language_codes_list=["pt", "en", "es"]
        )

        expected = [
            {
                "title": "Article element lang attribute validation",
                'parent': 'article',
                'parent_id': None,
                'item': 'article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": ["pt", "en", "es"],
                "got_value": "portugol",
                'message': "Got portugol, expected ['pt', 'en', 'es']",
                "advice": "<article article-type=research-article xml:lang=portugol> has portugol as language, expected one item of this list: pt | en | es",
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'lang': 'portugol',
                    'line_number': 2,
                    'subject': None
                },
            },
            {
                "title": "Article element lang attribute validation",
                'parent': 'sub-article',
                'parent_id': 's1',
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["pt", "en", "es"],
                "got_value": "en",
                'message': "Got en, expected ['pt', 'en', 'es']",
                "advice": None,
                'data': {
                    'article_id': 's1',
                    'article_type': 'translation',
                    'lang': 'en',
                    'line_number': 3,
                    'subject': None
                },
            },
            {
                "title": "Article element lang attribute validation",
                'parent': 'sub-article',
                'parent_id': 's2',
                'item': 'sub-article',
                'sub_item': '@xml:lang',
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": ["pt", "en", "es"],
                "got_value": "thisisaninvalidlanguagecode",
                'message': "Got thisisaninvalidlanguagecode, expected ['pt', 'en', 'es']",
                "advice": "<sub-article article-type=translation id=s2 xml:lang=thisisaninvalidlanguagecode> has thisisaninvalidlanguagecode as language, expected one item of this list: pt | en | es",
                'data': {
                    'article_id': 's2',
                    'article_type': 'translation',
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
            ArticleAttribsValidation(xml_tree).validate_specific_use(
                specific_use_list=["sps-1.9", "preprint", "special-issue"]
            )
        )

        expected = [
            {
                "title": "Article element specific-use attribute validation",
                'parent': 'article',
                'parent_id': None,
                'item': 'article',
                'sub_item': '@specific-use',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["sps-1.9", "preprint", "special-issue"],
                "got_value": "sps-1.9",
                'message': "Got sps-1.9, expected ['sps-1.9', 'preprint', 'special-issue']",
                "advice": None,
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
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
            ArticleAttribsValidation(xml_tree).validate_specific_use(
                specific_use_list=["sps-1.9", "preprint", "special-issue"]
            )
        )

        expected = [
            {
                "title": "Article element specific-use attribute validation",
                'parent': 'article',
                'parent_id': None,
                'item': 'article',
                'sub_item': '@specific-use',
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": ["sps-1.9", "preprint", "special-issue"],
                "got_value": None,
                'message': "Got None, expected ['sps-1.9', 'preprint', 'special-issue']",
                "advice": "XML research-article has None as specific-use, expected one item of this list: sps-1.9 | preprint | special-issue",
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
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
            ArticleAttribsValidation(xml_tree).validate_dtd_version(
                dtd_version_list=["1.1", "1.2", "1.3"]
            )
        )

        expected = [
            {
                "title": "Article element dtd-version attribute validation",
                'parent': 'article',
                'parent_id': None,
                'item': 'article',
                'sub_item': '@dtd-version',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["1.1", "1.2", "1.3"],
                "got_value": "1.1",
                'message': "Got 1.1, expected ['1.1', '1.2', '1.3']",
                "advice": None,
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
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
            ArticleTypeValidation(xml_tree).validate_article_type(
                article_type_list=["research-article"]
            )
        )

        expected = [
            {
                "title": "Article type validation",
                'parent': 'article',
                'parent_id': None,
                'item': 'article',
                'sub_item': '@article-type',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["research-article"],
                "got_value": "research-article",
                'message': "Got research-article, expected ['research-article']",
                "advice": None,
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
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
            ArticleTypeValidation(xml_tree).validate_article_type(
                article_type_list=["research-article"]
            )
        )

        expected = [
            {
                "title": "Article type validation",
                'parent': 'article',
                'parent_id': None,
                'item': 'article',
                'sub_item': '@article-type',
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": ["research-article"],
                "got_value": "main",
                'message': "Got main, expected ['research-article']",
                "advice": "XML has main as article-type, expected one item of this list: research-article",
                'data': {
                    'article_id': None,
                    'article_type': 'main',
                    'dtd_version': None,
                    'lang': 'portugol',
                    'line_number': 2,
                    'specific_use': 'sps-1.9',
                    'subject': None
                },
            }
        ]

        self.assertEqual(obtained, expected)

    def test_article_and_subarticles_there_is_subject_there_should_be_no_subject(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
            <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
            <article-id pub-id-type="other">00303</article-id>
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
        obtained = list(ArticleSubjectsValidation(xml_tree).validate_without_subjects())

        expected = [
            {
                "title": "Article type vs subjects validation",
                'parent': 'article',
                'parent_id': None,
                'item': 'article',
                'sub_item': '@article-type',
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": None,
                "got_value": [
                    "scientific article",
                    "artigo científico",
                    "artículo científico",
                ],
                'message': "Got ['scientific article', 'artigo científico', 'artículo científico'], expected None",
                "advice": "XML has scientific article, artigo científico, artículo científico as subjects, expected "
                "no subjects",
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'dtd_version': '1.1',
                    'lang': 'en',
                    'line_number': 3,
                    'specific_use': 'sps-1.9',
                    'subject': 'Scientific Article'
                },
            }
        ]

        self.assertEqual(obtained, expected)

    def test_article_and_subarticles_there_is_no_subject_there_should_be_no_subject(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <article-id pub-id-type="publisher-id" specific-use="scielo-v3">TPg77CCrGj4wcbLCh9vG8bS</article-id>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v2">S0104-11692020000100303</article-id>
            <article-id pub-id-type="doi">10.1590/1518-8345.2927.3231</article-id>
            <article-id pub-id-type="other">00303</article-id>
            <sub-article article-type="translation" id="s1" xml:lang="pt">
            </sub-article>
            <sub-article article-type="translation" id="s2" xml:lang="es">
            </sub-article>
            </article>
            """
        xml_tree = get_xml_tree(xml_str)
        obtained = list(ArticleSubjectsValidation(xml_tree).validate_without_subjects())

        expected = [
            {
                "title": "Article type vs subjects validation",
                'parent': 'article',
                'parent_id': None,
                'item': 'article',
                'sub_item': '@article-type',
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": None,
                'got_value': [],
                'message': 'Got [], expected None',
                "advice": None,
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
                    'dtd_version': '1.1',
                    'lang': 'en',
                    'line_number': 3,
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
        obtained = ArticleSubjectsValidation(
            xml_tree
        ).validate_article_type_vs_subject_similarity(
            subjects_list=[
                {"subject": "Original Article", "lang": "en"},
                {"subject": "Artigo Original", "lang": "pt"},
                {"subject": "Artículo Original", "lang": "es"},
            ],
            expected_similarity=0.7,
        )

        expected = [
            {
                "title": "Article type vs subjects validation",
                'parent': 'article',
                'parent_id': None,
                'item': 'article',
                'sub_item': '@article-type',
                "validation_type": "similarity",
                "response": "ERROR",
                "expected_value": 0.7,
                "got_value": 0.6818181818181818,
                'message': 'Got 0.6818181818181818, expected 0.7',
                "advice": "The subject Scientific Article (en) does not match the items provided in the list: "
                "Original Article (en) | Artigo Original (pt) | Artículo Original (es)",
                'data': {
                    'article_id': None,
                    'article_type': 'research-article',
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
        obtained = list(ArticleIdValidation(xml_tree).validate_article_id_other())

        expected = [
            {
                "title": "Article id other validation",
                'parent': 'article',
                'parent_id': None,
                'item': 'article-id',
                'sub_item': '@pub-id-type="other"',
                "validation_type": "format",
                "response": "OK",
                "expected_value": "123",
                "got_value": "123",
                'message': 'Got 123, expected 123',
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
        obtained = list(ArticleIdValidation(xml_tree).validate_article_id_other())

        expected = [
            {
                "title": "Article id other validation",
                'parent': 'article',
                'parent_id': None,
                'item': 'article-id',
                'sub_item': '@pub-id-type="other"',
                "validation_type": "format",
                "response": "ERROR",
                'expected_value': 'a numeric value with up to five digits',
                "got_value": "x23",
                'message': 'Got x23, expected a numeric value with up to five digits',
                "advice": 'Provide a numeric value for <article-id pub-id-type="other"> with up to five digits',
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
        obtained = list(ArticleIdValidation(xml_tree).validate_article_id_other())

        expected = [
            {
                "title": "Article id other validation",
                'parent': 'article',
                'parent_id': None,
                'item': 'article-id',
                'sub_item': '@pub-id-type="other"',
                "validation_type": "format",
                "response": "ERROR",
                "expected_value": "a numeric value with up to five digits",
                "got_value": "123456",
                'message': 'Got 123456, expected a numeric value with up to five digits',
                "advice": 'Provide a numeric value for <article-id pub-id-type="other"> with up to five digits',
                'data': {
                    'other': '123456',
                    'v2': 'S0104-11692020000100303',
                    'v3': 'TPg77CCrGj4wcbLCh9vG8bS'
                },
            }
        ]
        self.assertEqual(expected, obtained)
