from unittest import TestCase

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation.article_and_subarticles import ArticleValidation


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

        obtained = ArticleValidation(xml_tree).validate_language(language_codes_list=['pt', 'en', 'es'])

        expected = [
            {
                'title': 'Article element lang attribute validation',
                'xpath': './article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': ['pt', 'en', 'es'],
                'got_value': None,
                'message': 'Got <article article-type=research-article xml:lang=None> expected one item of this list: pt | en | es',
                'advice': "<article article-type=research-article xml:lang=None> has None as language, expected one item of this list: pt | en | es"

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

        obtained = ArticleValidation(xml_tree).validate_language(language_codes_list=['pt', 'en', 'es'])

        expected = [
            {
                'title': 'Article element lang attribute validation',
                'xpath': './article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['pt', 'en', 'es'],
                'got_value': 'en',
                'message': 'Got <article article-type=research-article xml:lang=en> expected one item of this list: pt | en | es',
                'advice': None

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_article_has_invalid_language(self):
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

        obtained = ArticleValidation(xml_tree).validate_language(language_codes_list=['pt', 'en', 'es'])

        expected = [
            {
                'title': 'Article element lang attribute validation',
                'xpath': './article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': ['pt', 'en', 'es'],
                'got_value': 'e',
                'message': 'Got <article article-type=research-article xml:lang=e> expected one item of this list: pt | en | es',
                'advice': "<article article-type=research-article xml:lang=e> has e as language, expected one item of this list: pt | en | es"

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_article_and_subarticles_have_valid_languages(self):
        self.maxDiff = None
        with open('tests/samples/article-abstract-en-sub-articles-pt-es.xml') as data:
            xml_tree = get_xml_tree(data.read())

        obtained = ArticleValidation(xml_tree).validate_language(language_codes_list=['pt', 'en', 'es'])

        expected = [
            {
                'title': 'Article element lang attribute validation',
                'xpath': './article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['pt', 'en', 'es'],
                'got_value': 'en',
                'message': 'Got <article article-type=research-article xml:lang=en> expected one item of this list: pt | en | es',
                'advice': None

            },
            {
                'title': 'Article element lang attribute validation',
                'xpath': './/sub-article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['pt', 'en', 'es'],
                'got_value': 'pt',
                'message': 'Got <sub-article article-type=translation id=s1 xml:lang=pt> expected one item of this list: pt | en | es',
                'advice': None

            },
            {
                'title': 'Article element lang attribute validation',
                'xpath': './/sub-article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['pt', 'en', 'es'],
                'got_value': 'es',
                'message': 'Got <sub-article article-type=translation id=s2 xml:lang=es> expected one item of this list: pt | en | es',
                'advice': None

            }
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
        obtained = ArticleValidation(xml_tree).validate_language(language_codes_list=['pt', 'en', 'es'])

        expected = [
            {
                'title': 'Article element lang attribute validation',
                'xpath': './article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['pt', 'en', 'es'],
                'got_value': 'en',
                'message': 'Got <article article-type=research-article xml:lang=en> expected one item of this list: pt | en | es',
                'advice': None

            },
            {
                'title': 'Article element lang attribute validation',
                'xpath': './/sub-article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['pt', 'en', 'es'],
                'got_value': 'pt',
                'message': 'Got <sub-article article-type=translation id=s1 xml:lang=pt> expected one item of this list: pt | en | es',
                'advice': None

            },
            {
                'title': 'Article element lang attribute validation',
                'xpath': './/sub-article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['pt', 'en', 'es'],
                'got_value': 'es',
                'message': 'Got <sub-article article-type=translation id=s2 xml:lang=es> expected one item of this list: pt | en | es',
                'advice': None

            }
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
        obtained = ArticleValidation(xml_tree).validate_language(language_codes_list=['pt', 'en', 'es'])

        expected = [
            {
                'title': 'Article element lang attribute validation',
                'xpath': './article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['pt', 'en', 'es'],
                'got_value': 'en',
                'message': 'Got <article article-type=research-article xml:lang=en> expected one item of this list: pt | en | es',
                'advice': None

            },
            {
                'title': 'Article element lang attribute validation',
                'xpath': './/sub-article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['pt', 'en', 'es'],
                'got_value': 'pt',
                'message': 'Got <sub-article article-type=translation id=s1 xml:lang=pt> expected one item of this list: pt | en | es',
                'advice': None

            },
            {
                'title': 'Article element lang attribute validation',
                'xpath': './/sub-article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': ['pt', 'en', 'es'],
                'got_value': '',
                'message': 'Got <sub-article article-type=translation id=s2 xml:lang=> expected one item of this list: pt | en | es',
                'advice': "<sub-article article-type=translation id=s2 xml:lang=> has  as language, expected one item of this list: pt | en | es"

            }
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
        obtained = ArticleValidation(xml_tree).validate_language(language_codes_list=['pt', 'en', 'es'])

        expected = [
            {
                'title': 'Article element lang attribute validation',
                'xpath': './article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['pt', 'en', 'es'],
                'got_value': 'en',
                'message': 'Got <article article-type=research-article xml:lang=en> expected one item of this list: pt | en | es',
                'advice': None

            },
            {
                'title': 'Article element lang attribute validation',
                'xpath': './/sub-article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': ['pt', 'en', 'es'],
                'got_value': None,
                'message': 'Got <sub-article article-type=translation id=s1 xml:lang=None> expected one item of this list: pt | en | es',
                'advice': "<sub-article article-type=translation id=s1 xml:lang=None> has None as language, expected one item of this list: pt | en | es"

            },
            {
                'title': 'Article element lang attribute validation',
                'xpath': './/sub-article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': ['pt', 'en', 'es'],
                'got_value': '',
                'message': 'Got <sub-article article-type=translation id=s2 xml:lang=> expected one item of this list: pt | en | es',
                'advice': "<sub-article article-type=translation id=s2 xml:lang=> has  as language, expected one item of this list: pt | en | es"

            }
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

        obtained = ArticleValidation(xml_tree).validate_language(language_codes_list=['pt', 'en', 'es'])

        expected = [
            {
                'title': 'Article element lang attribute validation',
                'xpath': './article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': ['pt', 'en', 'es'],
                'got_value': 'portugol',
                'message': 'Got <article article-type=research-article xml:lang=portugol> expected one item of this list: pt | en | es',
                'advice': "<article article-type=research-article xml:lang=portugol> has portugol as language, expected one item of this list: pt | en | es"

            },
            {
                'title': 'Article element lang attribute validation',
                'xpath': './/sub-article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['pt', 'en', 'es'],
                'got_value': 'en',
                'message': 'Got <sub-article article-type=translation id=s1 xml:lang=en> expected one item of this list: pt | en | es',
                'advice': None

            },
            {
                'title': 'Article element lang attribute validation',
                'xpath': './/sub-article/@xml:lang',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': ['pt', 'en', 'es'],
                'got_value': 'thisisaninvalidlanguagecode',
                'message': 'Got <sub-article article-type=translation id=s2 xml:lang=thisisaninvalidlanguagecode> expected one item of this list: pt | en | es',
                'advice': "<sub-article article-type=translation id=s2 xml:lang=thisisaninvalidlanguagecode> has thisisaninvalidlanguagecode as language, expected one item of this list: pt | en | es"

            }
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

        obtained = ArticleValidation(xml_tree).validate_specific_use(specific_use_list=['sps-1.9', 'preprint', 'special-issue'])

        expected = {
            'title': 'Article element specific-use attribute validation',
            'xpath': './article/specific-use',
            'validation_type': 'value in list',
            'response': 'OK',
            'expected_value': ['sps-1.9', 'preprint', 'special-issue'],
            'got_value': 'sps-1.9',
            'message': 'Got sps-1.9 expected one item of this list: sps-1.9 | preprint | special-issue',
            'advice': None
        }

        self.assertDictEqual(obtained, expected)

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

        obtained = ArticleValidation(xml_tree).validate_specific_use(specific_use_list=['sps-1.9', 'preprint', 'special-issue'])

        expected = {
            'title': 'Article element specific-use attribute validation',
            'xpath': './article/specific-use',
            'validation_type': 'value in list',
            'response': 'ERROR',
            'expected_value': ['sps-1.9', 'preprint', 'special-issue'],
            'got_value': None,
            'message': 'Got None expected one item of this list: sps-1.9 | preprint | special-issue',
            'advice': 'XML research-article has None as specific-use, expected one item of this list: sps-1.9 | preprint | special-issue'
        }

        self.assertDictEqual(obtained, expected)

