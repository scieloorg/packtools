import unittest

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.validation.article_lang import (
    ArticleLangValidation,
    get_element_langs,
    _elements_exist
)
from packtools.sps.models import article_titles, article_abstract, kwd_group


class AuxiliaryFunctionsTest(unittest.TestCase):
    def test_get_title_langs(self):
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
            <sub-article article-type="translation" id="TRen" xml:lang="en">
                 <front-stub>
                     <title-group>
                         <article-title xml:lang="en">Title in english</article-title>
                     </title-group>
                 <abstract xml:lang="en">
                     Abstract in english
                 </abstract>
                 <kwd-group xml:lang="en">
                     <kwd>Keyword 1</kwd>
                     <kwd>Keyword 2</kwd>
                 </kwd-group>
                 </front-stub>
             </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)
        article_title = article_titles.ArticleTitles(xml_tree).data

        obtained = get_element_langs(article_title)

        expected = [
            {
                'element_name': 'article',
                'lang': 'pt',
                'id': 'main'
            },
            {
                'element_name': 'article',
                'lang': 'en',
                'id': 'trans'
            },
            {
                'element_name': 'sub-article',
                'lang': 'en',
                'id': 'TRen'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_get_abstract_langs(self):
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
            <sub-article article-type="translation" id="TRen" xml:lang="en">
                 <front-stub>
                     <title-group>
                         <article-title xml:lang="en">Title in english</article-title>
                     </title-group>
                     <abstract xml:lang="en">
                         Abstract in english
                     </abstract>
                     <kwd-group xml:lang="en">
                         <kwd>Keyword 1</kwd>
                         <kwd>Keyword 2</kwd>
                     </kwd-group>
                 </front-stub>
             </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)
        abstract = article_abstract.Abstract(xml_tree).get_abstracts()

        obtained = get_element_langs(abstract)

        expected = [
            {
                'element_name': 'article',
                'lang': 'pt',
                'id': 'main'
            },
            {
                'element_name': 'article',
                'lang': 'en',
                'id': 'trans'
            },
            {
                'element_name': 'sub-article',
                'lang': 'en',
                'id': 'TRen'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_get_keyword_langs(self):
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
            <sub-article article-type="translation" id="TRen" xml:lang="en">
                 <front-stub>
                     <title-group>
                         <article-title xml:lang="en">Title in english</article-title>
                     </title-group>
                 <abstract xml:lang="en">
                     Abstract in english
                 </abstract>
                 <kwd-group xml:lang="en">
                     <kwd>Keyword 1</kwd>
                     <kwd>Keyword 2</kwd>
                 </kwd-group>
                 </front-stub>
             </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)
        kwd = kwd_group.KwdGroup(xml_tree).extract_kwd_data_with_lang_text_by_article_type(None)

        obtained = get_element_langs(kwd)

        expected = [
            {
                'element_name': 'article',
                'lang': 'pt',
                'id': 'main'
            },
            {
                'element_name': 'article',
                'lang': 'en',
                'id': 'main'
            },
            {
                'element_name': 'sub-article',
                'lang': 'en',
                'id': 'TRen'
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test__elements_exist(self):
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
            <sub-article article-type="translation" id="TRen" xml:lang="en">
                 <front-stub>
                     <title-group>
                         <article-title xml:lang="en">Title in english</article-title>
                     </title-group>
                 <abstract xml:lang="en">
                     Abstract in english
                 </abstract>
                 <kwd-group xml:lang="en">
                     <kwd>Keyword 1</kwd>
                     <kwd>Keyword 2</kwd>
                 </kwd-group>
                 </front-stub>
             </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)
        title = {
                'element_name': 'article',
                'lang': 'en',
                'id': 'main'
            }
        title_object = article_titles.ArticleTitles(xml_tree)
        abstracts = get_element_langs(article_abstract.Abstract(xml_tree).get_abstracts(style='inline'))
        keywords = get_element_langs(kwd_group.KwdGroup(xml_tree).extract_kwd_data_with_lang_text_by_article_type(None))

        obtained = _elements_exist(title, title_object, abstracts, keywords)

        expected = (True, True, None, None, None)

        self.assertEqual(expected, obtained)

    def test__elements_exist_missing_title(self):
        self.maxDiff = None
        xml_str = """
        <article  xml:lang="pt">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título em português</article-title>
                    </title-group>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)
        title = {
            'element_name': 'article',
            'lang': 'en',
            'id': 'main'
        }
        title_object = article_titles.ArticleTitles(xml_tree)
        abstracts = get_element_langs(article_abstract.Abstract(xml_tree).get_abstracts(style='inline'))
        keywords = get_element_langs(kwd_group.KwdGroup(xml_tree).extract_kwd_data_with_lang_text_by_article_type(None))

        obtained = _elements_exist(title, title_object, abstracts, keywords)

        expected = (False, True, 'title', './/article-title/@xml:lang', 'title for the article')

        self.assertEqual(expected, obtained)

    def test__elements_exist_missing_abstract(self):
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
        title = {
            'element_name': 'article',
            'lang': 'pt',
            'id': 'main'
        }
        title_object = article_titles.ArticleTitles(xml_tree)
        abstracts = get_element_langs(article_abstract.Abstract(xml_tree).get_abstracts(style='inline'))
        keywords = get_element_langs(kwd_group.KwdGroup(xml_tree).extract_kwd_data_with_lang_text_by_article_type(None))

        obtained = _elements_exist(title, title_object, abstracts, keywords)

        expected = (False, True, 'abstract', './/abstract/@xml:lang', 'abstract for the article')

        self.assertEqual(expected, obtained)

    def test__elements_exist_missing_kwd(self):
        self.maxDiff = None
        xml_str = """
        <article  xml:lang="pt">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título em português</article-title>
                    </title-group>
                    <abstract><p>Resumo em português</p></abstract>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)
        title = {
            'element_name': 'article',
            'lang': 'pt',
            'id': 'main'
        }
        title_object = article_titles.ArticleTitles(xml_tree)
        abstracts = get_element_langs(article_abstract.Abstract(xml_tree).get_abstracts(style='inline'))
        keywords = get_element_langs(kwd_group.KwdGroup(xml_tree).extract_kwd_data_with_lang_text_by_article_type(None))

        obtained = _elements_exist(title, title_object, abstracts, keywords)

        expected = (False, True, 'kwd-group', './/kwd-group/@xml:lang', 'keywords for the article')

        self.assertEqual(expected, obtained)

    def test__elements_exist_is_required(self):
        self.maxDiff = None
        xml_str = """
        <article  xml:lang="pt">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título em português</article-title>
                    </title-group>
                </article-meta>
            </front>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)
        title = {
            'element_name': 'article',
            'lang': 'pt',
            'id': 'main'
        }
        title_object = article_titles.ArticleTitles(xml_tree)
        abstracts = get_element_langs(article_abstract.Abstract(xml_tree).get_abstracts(style='inline'))
        keywords = get_element_langs(kwd_group.KwdGroup(xml_tree).extract_kwd_data_with_lang_text_by_article_type(None))

        obtained = _elements_exist(title, title_object, abstracts, keywords)

        expected = (True, False, None, None, None)

        self.assertEqual(expected, obtained)


class ArticleLangTest(unittest.TestCase):
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
                'title': 'article title element lang attribute validation',
                'xpath': './/article-title/@xml:lang',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'title for the article',
                'got_value': None,
                'message': 'Got None expected title for the article',
                'advice': 'Provide title in the \'pt\' language for article (main)'
            }
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_sub_article_lang_without_title(self):
        self.maxDiff = None
        xml_str = """
        <article  xml:lang="pt">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título em português</article-title>
                    </title-group>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
                <front-stub>
                    <abstract xml:lang="en">
                        Abstract in english
                    </abstract>
                    <kwd-group xml:lang="en">
                        <kwd>Keyword 1</kwd>
                        <kwd>Keyword 2</kwd>
                    </kwd-group>
                </front-stub>
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = ArticleLangValidation(xml_tree).validate_article_lang()

        expected = [
            {
                'title': 'sub-article title element lang attribute validation',
                'xpath': './/article-title/@xml:lang',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'title for the sub-article',
                'got_value': None,
                'message': 'Got None expected title for the sub-article',
                'advice': 'Provide title in the \'en\' language for sub-article (TRen)'
            }
        ]

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

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
                'title': 'article abstract element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//abstract/@xml:lang',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'pt',
                'got_value': 'pt',
                'message': 'Got pt expected pt',
                'advice': None

            },
            {
                'title': 'article kwd-group element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//kwd-group/@xml:lang',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'pt',
                'got_value': 'pt',
                'message': 'Got pt expected pt',
                'advice': None

            },
            {
                'title': 'article abstract element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//abstract/@xml:lang',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'en',
                'got_value': 'en',
                'message': 'Got en expected en',
                'advice': None

            },
            {
                'title': 'article kwd-group element lang attribute validation',
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

    def test_validate_sub_article_lang_success(self):
        self.maxDiff = None
        xml_str = """
        <article xml:lang="pt">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título em português</article-title>
                    </title-group>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
                <front-stub>
                    <title-group>
                        <article-title xml:lang="en">Title in english</article-title>
                    </title-group>
                    <abstract xml:lang="en">
                        Abstract in english
                    </abstract>
                    <kwd-group xml:lang="en">
                        <kwd>Keyword 1</kwd>
                        <kwd>Keyword 2</kwd>
                    </kwd-group>
                </front-stub>
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = ArticleLangValidation(xml_tree).validate_article_lang()

        expected = [
            {
                'title': 'sub-article abstract element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//abstract/@xml:lang',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'en',
                'got_value': 'en',
                'message': 'Got en expected en',
                'advice': None

            },
            {
                'title': 'sub-article kwd-group element lang attribute validation',
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
                    <trans-abstract xml:lang="es">Abstract in english</trans-abstract>
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
                'title': 'article abstract element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//abstract/@xml:lang',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'pt',
                'got_value': 'pt',
                'message': 'Got pt expected pt',
                'advice': None

            },
            {
                'title': 'article kwd-group element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//kwd-group/@xml:lang',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'pt',
                'got_value': 'pt',
                'message': 'Got pt expected pt',
                'advice': None

            },
            {
                'title': 'article abstract element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//abstract/@xml:lang',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': 'en',
                'got_value': None,
                'message': 'Got None expected en',
                'advice': "Provide abstract in the 'en' language for article (trans)",

            },
            {
                'title': 'article kwd-group element lang attribute validation',
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

    def test_validate_sub_article_lang_fail_abstract_does_not_match(self):
        self.maxDiff = None
        xml_str = """
        <article>
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título em português</article-title>
                    </title-group>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
                <front-stub>
                    <title-group>
                        <article-title xml:lang="en">Title in english</article-title>
                    </title-group>
                <abstract xml:lang="pt">
                    Abstract in english
                </abstract>
                <kwd-group xml:lang="en">
                    <kwd>Keyword 1</kwd>
                    <kwd>Keyword 2</kwd>
                </kwd-group>
                </front-stub>
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = ArticleLangValidation(xml_tree).validate_article_lang()

        expected = [
            {
                'title': 'sub-article abstract element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//abstract/@xml:lang',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': 'en',
                'got_value': None,
                'message': 'Got None expected en',
                'advice': "Provide abstract in the 'en' language for sub-article (TRen)",

            },
            {
                'title': 'sub-article kwd-group element lang attribute validation',
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
                'title': 'article abstract element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//abstract/@xml:lang',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'pt',
                'got_value': 'pt',
                'message': 'Got pt expected pt',
                'advice': None

            },
            {
                'title': 'article kwd-group element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//kwd-group/@xml:lang',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': 'pt',
                'got_value': None,
                'message': 'Got None expected pt',
                'advice': "Provide kwd-group in the 'pt' language for article (main)",

            },
            {
                'title': 'article abstract element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//abstract/@xml:lang',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'en',
                'got_value': 'en',
                'message': 'Got en expected en',
                'advice': None

            },
            {
                'title': 'article kwd-group element lang attribute validation',
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

    def test_validate_sub_article_lang_fail_kwd_group_does_not_match(self):
        self.maxDiff = None
        xml_str = """
        <article>
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título em português</article-title>
                    </title-group>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
                <front-stub>
                    <title-group>
                        <article-title xml:lang="en">Title in english</article-title>
                    </title-group>
                <abstract xml:lang="en">
                    Abstract in english
                </abstract>
                <kwd-group xml:lang="pt">
                    <kwd>Keyword 1</kwd>
                    <kwd>Keyword 2</kwd>
                </kwd-group>
                </front-stub>
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = ArticleLangValidation(xml_tree).validate_article_lang()

        expected = [
            {
                'title': 'sub-article abstract element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//abstract/@xml:lang',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'en',
                'got_value': 'en',
                'message': 'Got en expected en',
                'advice': None

            },
            {
                'title': 'sub-article kwd-group element lang attribute validation',
                'xpath': './/article-title/@xml:lang .//kwd-group/@xml:lang',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': 'en',
                'got_value': None,
                'message': 'Got None expected en',
                'advice': "Provide kwd-group in the 'en' language for sub-article (TRen)",

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
                'title': 'article abstract element lang attribute validation',
                'xpath': './/abstract/@xml:lang',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'abstract for the article',
                'got_value': None,
                'message': 'Got None expected abstract for the article',
                'advice': "Provide abstract in the 'pt' language for article (main)",

            },
            {
                'title': 'article abstract element lang attribute validation',
                'xpath': './/abstract/@xml:lang',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'abstract for the article',
                'got_value': None,
                'message': 'Got None expected abstract for the article',
                'advice': "Provide abstract in the 'en' language for article (trans)",
            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_sub_article_lang_without_abstract(self):
        self.maxDiff = None
        xml_str = """
        <article  xml:lang="pt">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título em português</article-title>
                    </title-group>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
                <front-stub>
                    <title-group>
                        <article-title xml:lang="en">Title in english</article-title>
                    </title-group>
                    <kwd-group xml:lang="en">
                        <kwd>Keyword 1</kwd>
                        <kwd>Keyword 2</kwd>
                    </kwd-group>
                </front-stub>
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = ArticleLangValidation(xml_tree).validate_article_lang()

        expected = [
            {
                'title': 'sub-article abstract element lang attribute validation',
                'xpath': './/abstract/@xml:lang',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'abstract for the sub-article',
                'got_value': None,
                'message': 'Got None expected abstract for the sub-article',
                'advice': "Provide abstract in the 'en' language for sub-article (TRen)",
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
                'title': 'article kwd-group element lang attribute validation',
                'xpath': './/kwd-group/@xml:lang',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'keywords for the article',
                'got_value': None,
                'message': 'Got None expected keywords for the article',
                'advice': "Provide kwd-group in the 'pt' language for article (main)"

            },
            {
                'title': 'article kwd-group element lang attribute validation',
                'xpath': './/kwd-group/@xml:lang',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'keywords for the article',
                'got_value': None,
                'message': 'Got None expected keywords for the article',
                'advice': "Provide kwd-group in the 'en' language for article (trans)"

            }
        ]
        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_sub_article_lang_without_kwd_group(self):
        self.maxDiff = None
        xml_str = """
        <article  xml:lang="pt">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título em português</article-title>
                    </title-group>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="TRen" xml:lang="en">
                <front-stub>
                    <title-group>
                        <article-title xml:lang="en">Title in english</article-title>
                    </title-group>
                    <abstract xml:lang="en">
                        Abstract in english
                    </abstract>
                </front-stub>
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = ArticleLangValidation(xml_tree).validate_article_lang()

        expected = [
            {
                'title': 'sub-article kwd-group element lang attribute validation',
                'xpath': './/kwd-group/@xml:lang',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'keywords for the sub-article',
                'got_value': None,
                'message': 'Got None expected keywords for the sub-article',
                'advice': "Provide kwd-group in the 'en' language for sub-article (TRen)",
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

    def test_validate_sub_article_lang_with_title_only(self):
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
            <sub-article article-type="translation" id="TRen" xml:lang="en">
                <front-stub>
                    <title-group>
                        <article-title xml:lang="en">Title in english</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
        </article>
        """
        xml_tree = get_xml_tree(xml_str)

        obtained = ArticleLangValidation(xml_tree).validate_article_lang()

        expected = []
        self.assertEqual(list(obtained), expected)


if __name__ == '__main__':
    unittest.main()
