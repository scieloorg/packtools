import unittest

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation.article_lang import ArticleLangValidation


class ArticleLangTest(unittest.TestCase):
    def test_validate_article_lang_success(self):
        self.maxDiff = None
        xml_str = """
        <article  xml:lang="pt">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título em português</article-title>
                        <trans-title-group xml:lang="en">
                            <trans-title>Title in english</trans-title>
                        </trans-title-group>
                    </title-group>
                    <abstract><p>Resumo em português</p></abstract>
                    <trans-abstract xml:lang="en">Abstract in english</trans-abstract>
                    <kwd-group xml:lang="pt">
                        <kwd>Palavra chave 1</kwd>
                        <kwd>Palavra chave 2</kwd>
                    </kwd-group>
                    <kwd-group xml:lang="en">
                        <kwd>Keyword 1</kwd>
                        <kwd>Keyword 2</kwd>
                    </kwd-group>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = ArticleLangValidation(xml_tree).validate_article_lang()

        expected = [
            {
                'title': 'abstract element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//abstract/@xml:lang',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'pt',
                'got_value': 'pt',
                'message': 'Got pt expected pt',
                'advice': None

            },
            {
                'title': 'abstract element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//abstract/@xml:lang',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'en',
                'got_value': 'en',
                'message': 'Got en expected en',
                'advice': None

            },
            {
                'title': 'kwd-group element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//kwd-group/@xml:lang',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'pt',
                'got_value': 'pt',
                'message': 'Got pt expected pt',
                'advice': None

            },
            {
                'title': 'kwd-group element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//kwd-group/@xml:lang',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'en',
                'got_value': 'en',
                'message': 'Got en expected en',
                'advice': None

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_lang_fail_abstract_does_not_match(self):
        self.maxDiff = None
        xml_str = """
        <article  xml:lang="pt">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título em português</article-title>
                        <trans-title-group xml:lang="en">
                            <trans-title>Title in english</trans-title>
                        </trans-title-group>
                    </title-group>
                    <abstract><p>Resumo em português</p></abstract>
                    <trans-abstract xml:lang="pt">Abstract in english</trans-abstract>
                    <kwd-group xml:lang="pt">
                        <kwd>Palavra chave 1</kwd>
                        <kwd>Palavra chave 2</kwd>
                    </kwd-group>
                    <kwd-group xml:lang="en">
                        <kwd>Keyword 1</kwd>
                        <kwd>Keyword 2</kwd>
                    </kwd-group>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = ArticleLangValidation(xml_tree).validate_article_lang()

        expected = [
            {
                'title': 'abstract element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//abstract/@xml:lang',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'pt',
                'got_value': 'pt',
                'message': 'Got pt expected pt',
                'advice': None

            },
            {
                'title': 'abstract element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//abstract/@xml:lang',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': 'en',
                'got_value': 'pt',
                'message': 'Got pt expected en',
                'advice': 'Provide abstract in the language \'en\''

            },
            {
                'title': 'kwd-group element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//kwd-group/@xml:lang',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'pt',
                'got_value': 'pt',
                'message': 'Got pt expected pt',
                'advice': None

            },
            {
                'title': 'kwd-group element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//kwd-group/@xml:lang',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'en',
                'got_value': 'en',
                'message': 'Got en expected en',
                'advice': None

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

