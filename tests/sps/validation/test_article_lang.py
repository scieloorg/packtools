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

    def test_validate_article_lang_fail_kwd_group_does_not_match(self):
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
                    <kwd-group xml:lang="en">
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
                'response': 'ERROR',
                'expected_value': 'pt',
                'got_value': 'en',
                'message': 'Got en expected pt',
                'advice': 'Provide kwd-group in the language \'pt\''

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

    def test_validate_article_lang_without_title(self):
        self.maxDiff = None
        xml_str = """
        <article  xml:lang="pt">
            <front>
                <article-meta>
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
                'title': 'title element lang attribute validation',
                'xpath': './/article-title/@xml:lang',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'title for the article',
                'got_value': None,
                'message': 'Got None expected title for the article',
                'advice': 'Provide a title in the language \'pt\'',
            }
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_lang_without_abstract(self):
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
                'xpath': './/abstract/@xml:lang',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'abstract for the article',
                'got_value': None,
                'message': 'Got None expected abstract for the article',
                'advice': 'Provide a abstract in the language \'pt | en\''

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_lang_without_kwd_group(self):
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
                </article-meta>
            </front>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = ArticleLangValidation(xml_tree).validate_article_lang()

        expected = [
            {
                'title': 'kwd-group element lang attribute validation',
                'xpath': './/kwd-group/@xml:lang',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'keywords for the article',
                'got_value': None,
                'message': 'Got None expected keywords for the article',
                'advice': 'Provide a kwd-group in the language \'pt | en\''

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_lang_with_title_only(self):
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
                </article-meta>
            </front>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = ArticleLangValidation(xml_tree).validate_article_lang()

        expected = []
        self.assertEqual(list(obtained), expected)


if __name__ == '__main__':
    unittest.main()
