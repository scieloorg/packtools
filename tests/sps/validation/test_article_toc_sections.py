from unittest import TestCase

from lxml import etree

from packtools.sps.utils import xml_utils
from packtools.sps.validation.article_toc_sections import ArticleTocSectionsValidation
from packtools.sps.validation.exceptions import ValidationExpectedTocSectionsException


class ArticleTocSectionsTest(TestCase):
    def test_validate_article_toc_sections_success(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título del artículo</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Health Sciences</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="pt">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Ciências da Saúde</subject>
                        </subj-group>
                    </article-categories>
                    <title-group>
                        <article-title>Article title</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSectionsValidation(self.xmltree)
        expected_section = {
                "en": ["Health Sciences"],
                "pt": ["Ciências da Saúde"]
            }
        expected = [
            {
                'title': 'Document section title validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'Health Sciences',
                'got_value': 'Health Sciences',
                'message': "Got Health Sciences, expected one of ['Health Sciences']",
                'advice': None,
                'data': {
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'section': 'Health Sciences',
                    'subj_group_type': 'heading',
                    'subsections': []
                }
            },
            {
                'title': 'Document section title validation',
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'Ciências da Saúde',
                'got_value': 'Ciências da Saúde',
                'message': "Got Ciências da Saúde, expected one of ['Ciências da Saúde']",
                'advice': None,
                'data': {
                    'parent': 'sub-article',
                    'parent_article_type': 'translation',
                    'parent_id': '01',
                    'parent_lang': 'pt',
                    'section': 'Ciências da Saúde',
                    'subj_group_type': 'heading',
                    'subsections': []
                }
            },
        ]
        obtained = list(self.article_toc_sections.validate_article_toc_sections(expected_section))

        self.assertEqual(len(obtained), 2)

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_article_toc_sections_fail_sections_not_obtained(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="es">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título del artículo</article-title>
                    </title-group>
                    <article-categories>

                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="en">
                <front-stub>
                    <title-group>
                        <article-title>Article title</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSectionsValidation(self.xmltree)
        expected_section = {
            "en": "Health Sciences",
            "pt": "Ciências da Saúde"
        }

        obtained = list(self.article_toc_sections.validate_article_toc_sections(expected_section))

        self.assertEqual(len(obtained), 0)

    def test_validate_article_toc_sections_fail_section_obtained_not_in_expected(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título del artículo</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Health Sciences</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="pt">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Ciências da Saúde</subject>
                        </subj-group>
                    </article-categories>
                    <title-group>
                        <article-title>Article title</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSectionsValidation(self.xmltree)
        expected_section = {
            "en": ["Article"],
            "pt": ["Artigo"]
        }
        expected = [
            {
                'title': 'Document section title validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'value in list',
                'response': 'CRITICAL',
                'expected_value': "one of ['Article']",
                'got_value': 'Health Sciences',
                'message': "Got Health Sciences, expected one of ['Article']",
                'advice': 'Provide missing section for language: en',
                'data': {
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'section': 'Health Sciences',
                    'subj_group_type': 'heading',
                    'subsections': []
                }
            },
            {
                'title': 'Document section title validation',
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'value in list',
                'response': 'CRITICAL',
                'expected_value': "one of ['Artigo']",
                'got_value': 'Ciências da Saúde',
                'message': "Got Ciências da Saúde, expected one of ['Artigo']",
                'advice': 'Provide missing section for language: pt',
                'data': {
                    'parent': 'sub-article',
                    'parent_article_type': 'translation',
                    'parent_id': '01',
                    'parent_lang': 'pt',
                    'section': 'Ciências da Saúde',
                    'subj_group_type': 'heading',
                    'subsections': []
                }
            },
        ]
        obtained = list(self.article_toc_sections.validate_article_toc_sections(expected_section))

        self.assertEqual(len(obtained), 2)

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_article_toc_sections_fail_one_section_not_expected(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título del artículo</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Health Sciences</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="pt">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Ciências da Saúde</subject>
                        </subj-group>
                    </article-categories>
                    <title-group>
                        <article-title>Article title</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSectionsValidation(self.xmltree)
        expected_section = {
            "en": ["Article"],
            "pt": ["Ciências da Saúde"]
        }
        expected = [
            {
                'title': 'Document section title validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'value in list',
                'response': 'CRITICAL',
                'expected_value': "one of ['Article']",
                'got_value': 'Health Sciences',
                'message': "Got Health Sciences, expected one of ['Article']",
                'advice': 'Provide missing section for language: en',
                'data': {
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'section': 'Health Sciences',
                    'subj_group_type': 'heading',
                    'subsections': []
                }
            },
            {
                'title': 'Document section title validation',
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'Ciências da Saúde',
                'got_value': 'Ciências da Saúde',
                'message': "Got Ciências da Saúde, expected one of ['Ciências da Saúde']",
                'advice': None,
                'data': {
                    'parent': 'sub-article',
                    'parent_article_type': 'translation',
                    'parent_id': '01',
                    'parent_lang': 'pt',
                    'section': 'Ciências da Saúde',
                    'subj_group_type': 'heading',
                    'subsections': []
                }
            },
        ]
        obtained = list(self.article_toc_sections.validate_article_toc_sections(expected_section))

        self.assertEqual(len(obtained), 2)

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_article_toc_sections_fail_all_sections_not_expected(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título del artículo</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Health Sciences</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="pt">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Ciências da Saúde</subject>
                        </subj-group>
                    </article-categories>
                    <title-group>
                        <article-title>Article title</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSectionsValidation(self.xmltree)
        expected_section = {
            "en": ["Article"],
            "pt": ["Artigo"]
        }
        expected = [
            {
                'title': 'Document section title validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'value in list',
                'response': 'CRITICAL',
                'expected_value': "one of ['Article']",
                'got_value': 'Health Sciences',
                'message': "Got Health Sciences, expected one of ['Article']",
                'advice': 'Provide missing section for language: en',
                'data': {
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'section': 'Health Sciences',
                    'subj_group_type': 'heading',
                    'subsections': []
                }
            },
            {
                'title': 'Document section title validation',
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'value in list',
                'response': 'CRITICAL',
                'expected_value': "one of ['Artigo']",
                'got_value': 'Ciências da Saúde',
                'message': "Got Ciências da Saúde, expected one of ['Artigo']",
                'advice': 'Provide missing section for language: pt',
                'data': {
                    'parent': 'sub-article',
                    'parent_article_type': 'translation',
                    'parent_id': '01',
                    'parent_lang': 'pt',
                    'section': 'Ciências da Saúde',
                    'subj_group_type': 'heading',
                    'subsections': []
                }
            },
        ]
        obtained = list(self.article_toc_sections.validate_article_toc_sections(expected_section))

        self.assertEqual(len(obtained), 2)

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_article_toc_sections_fail_sections_not_obtained_and_not_expected(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título del artículo</article-title>
                    </title-group>

                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="pt">
                <front-stub>

                    <title-group>
                        <article-title>Article title</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
            </article>
            """
        )

        self.article_toc_sections = ArticleTocSectionsValidation(self.xmltree)
        with self.assertRaises(ValidationExpectedTocSectionsException) as context:
            obtained = list(self.article_toc_sections.validate_article_toc_sections())

        self.assertEqual(str(context.exception), "Function requires a dict of expected toc sections.")

    def test_validade_article_title_is_different_from_section_titles_success(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Health Sciences Studies</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Health Sciences</subject>
                            <subj-group subj-group-type="heading">
                                <subject>Public Health</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="pt">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Ciências da Saúde</subject>
                            <subj-group subj-group-type="heading">
                                <subject>Saúde Pública</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                    <title-group>
                        <article-title>Estudos sobre Ciências da Saúde</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSectionsValidation(self.xmltree)

        expected = [
            {
                'title': 'Document title must not be similar to section title',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': "article title: 'Health Sciences Studies', section titles: 'Health Sciences'",
                'got_value': "article title: 'Health Sciences Studies', section titles: 'Health Sciences'",
                'message': "Got article title: 'Health Sciences Studies', section titles: 'Health Sciences', "
                           "expected 'Health Sciences Studies' (article title) different from 'Health Sciences' ("
                           "section titles)",
                'advice': None,
                'data': {
                    'en': [
                        {
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'parent_id': None,
                            'parent_lang': 'en',
                            'section': 'Health Sciences',
                            'subj_group_type': 'heading',
                            'subsections': ['Public Health']
                        },
                        {
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'parent_id': None,
                            'parent_lang': 'en',
                            'section': 'Public Health',
                            'subj_group_type': 'heading',
                            'subsections': []
                        }
                    ],
                    'pt': [
                        {
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': '01',
                            'parent_lang': 'pt',
                            'section': 'Ciências da Saúde',
                            'subj_group_type': 'heading',
                            'subsections': ['Saúde Pública']
                        },
                        {
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': '01',
                            'parent_lang': 'pt',
                            'section': 'Saúde Pública',
                            'subj_group_type': 'heading',
                            'subsections': []
                        }
                    ]
                },
            },
            {
                'title': 'Document title must not be similar to section title',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': "article title: 'Health Sciences Studies', section titles: 'Public Health'",
                'got_value': "article title: 'Health Sciences Studies', section titles: 'Public Health'",
                'message': "Got article title: 'Health Sciences Studies', section titles: 'Public Health', "
                           "expected 'Health Sciences Studies' (article title) different from 'Public Health' ("
                           "section titles)",
                'advice': None,
                'data': {
                    'en': [
                        {
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'parent_id': None,
                            'parent_lang': 'en',
                            'section': 'Health Sciences',
                            'subj_group_type': 'heading',
                            'subsections': ['Public Health']
                        },
                        {
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'parent_id': None,
                            'parent_lang': 'en',
                            'section': 'Public Health',
                            'subj_group_type': 'heading',
                            'subsections': []
                        }
                    ],
                    'pt': [
                        {
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': '01',
                            'parent_lang': 'pt',
                            'section': 'Ciências da Saúde',
                            'subj_group_type': 'heading',
                            'subsections': ['Saúde Pública']
                        },
                        {
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': '01',
                            'parent_lang': 'pt',
                            'section': 'Saúde Pública',
                            'subj_group_type': 'heading',
                            'subsections': []
                        }
                    ]
                },
            },
            {
                'title': 'Document title must not be similar to section title',
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': "article title: 'Estudos sobre Ciências da Saúde', section titles: 'Ciências da Saúde'",
                'got_value': "article title: 'Estudos sobre Ciências da Saúde', section titles: 'Ciências da Saúde'",
                'message': "Got article title: 'Estudos sobre Ciências da Saúde', section titles: 'Ciências da "
                           "Saúde', expected 'Estudos sobre Ciências da Saúde' (article title) different from "
                           "'Ciências da Saúde' (section titles)",
                'advice': None,
                'data': {
                    'en': [
                        {
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'parent_id': None,
                            'parent_lang': 'en',
                            'section': 'Health Sciences',
                            'subj_group_type': 'heading',
                            'subsections': ['Public Health']
                        },
                        {
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'parent_id': None,
                            'parent_lang': 'en',
                            'section': 'Public Health',
                            'subj_group_type': 'heading',
                            'subsections': []
                        }
                    ],
                    'pt': [
                        {
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': '01',
                            'parent_lang': 'pt',
                            'section': 'Ciências da Saúde',
                            'subj_group_type': 'heading',
                            'subsections': ['Saúde Pública']
                        },
                        {
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': '01',
                            'parent_lang': 'pt',
                            'section': 'Saúde Pública',
                            'subj_group_type': 'heading',
                            'subsections': []
                        }
                    ]
                },
            },
            {
                'title': 'Document title must not be similar to section title',
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': "article title: 'Estudos sobre Ciências da Saúde', section titles: 'Saúde Pública'",
                'got_value': "article title: 'Estudos sobre Ciências da Saúde', section titles: 'Saúde Pública'",
                'message': "Got article title: 'Estudos sobre Ciências da Saúde', section titles: 'Saúde Pública', "
                           "expected 'Estudos sobre Ciências da Saúde' (article title) different from "
                           "'Saúde Pública' (section titles)",
                'advice': None,
                'data': {
                    'en': [
                        {
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'parent_id': None,
                            'parent_lang': 'en',
                            'section': 'Health Sciences',
                            'subj_group_type': 'heading',
                            'subsections': ['Public Health']
                        },
                        {
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'parent_id': None,
                            'parent_lang': 'en',
                            'section': 'Public Health',
                            'subj_group_type': 'heading',
                            'subsections': []
                        }
                    ],
                    'pt': [
                        {
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': '01',
                            'parent_lang': 'pt',
                            'section': 'Ciências da Saúde',
                            'subj_group_type': 'heading',
                            'subsections': ['Saúde Pública']
                        },
                        {
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': '01',
                            'parent_lang': 'pt',
                            'section': 'Saúde Pública',
                            'subj_group_type': 'heading',
                            'subsections': []
                        }
                    ]
                },
            },
        ]
        obtained = list(self.article_toc_sections.validade_article_title_is_different_from_section_titles())

        self.assertEqual(len(obtained), 4)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validade_article_title_is_different_from_section_titles_fail(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Health Sciences</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Health Sciences</subject>
                            <subj-group subj-group-type="heading">
                                <subject>Public Health</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="pt">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Ciências da Saúde</subject>
                            <subj-group subj-group-type="heading">
                                <subject>Saúde Pública</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                    <title-group>
                        <article-title>Ciências da Saúde</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSectionsValidation(self.xmltree)

        expected = [
            {
                'title': 'Document title must not be similar to section title',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': "'Health Sciences' (article title) different from 'Health Sciences' ("
                                  "section titles)",
                'got_value': "article title: 'Health Sciences', section titles: 'Health Sciences'",
                'message': "Got article title: 'Health Sciences', section titles: 'Health Sciences', "
                           "expected 'Health Sciences' (article title) different from 'Health Sciences' ("
                           "section titles)",
                'advice': "Provide different titles for article and section (subj-group[@subj-group-type='heading']/subject)",
                'data': {
                    'en': [
                        {
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'parent_id': None,
                            'parent_lang': 'en',
                            'section': 'Health Sciences',
                            'subj_group_type': 'heading',
                            'subsections': ['Public Health']
                        },
                        {
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'parent_id': None,
                            'parent_lang': 'en',
                            'section': 'Public Health',
                            'subj_group_type': 'heading',
                            'subsections': []
                        }
                    ],
                    'pt': [
                        {
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': '01',
                            'parent_lang': 'pt',
                            'section': 'Ciências da Saúde',
                            'subj_group_type': 'heading',
                            'subsections': ['Saúde Pública']
                        },
                        {
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': '01',
                            'parent_lang': 'pt',
                            'section': 'Saúde Pública',
                            'subj_group_type': 'heading',
                            'subsections': []
                        }
                    ]
                },
            },
            {
                'title': 'Document title must not be similar to section title',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': "article title: 'Health Sciences', section titles: 'Public Health'",
                'got_value': "article title: 'Health Sciences', section titles: 'Public Health'",
                'message': "Got article title: 'Health Sciences', section titles: 'Public Health', "
                           "expected 'Health Sciences' (article title) different from 'Public Health' ("
                           "section titles)",
                'advice': None,
                'data': {
                    'en': [
                        {
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'parent_id': None,
                            'parent_lang': 'en',
                            'section': 'Health Sciences',
                            'subj_group_type': 'heading',
                            'subsections': ['Public Health']
                        },
                        {
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'parent_id': None,
                            'parent_lang': 'en',
                            'section': 'Public Health',
                            'subj_group_type': 'heading',
                            'subsections': []
                        }
                    ],
                    'pt': [
                        {
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': '01',
                            'parent_lang': 'pt',
                            'section': 'Ciências da Saúde',
                            'subj_group_type': 'heading',
                            'subsections': ['Saúde Pública']
                        },
                        {
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': '01',
                            'parent_lang': 'pt',
                            'section': 'Saúde Pública',
                            'subj_group_type': 'heading',
                            'subsections': []
                        }
                    ]
                },
            },
            {
                'title': 'Document title must not be similar to section title',
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': "'Ciências da Saúde' (article title) different from 'Ciências da "
                                  "Saúde' (section titles)",
                'got_value': "article title: 'Ciências da Saúde', section titles: 'Ciências da Saúde'",
                'message': "Got article title: 'Ciências da Saúde', section titles: 'Ciências da "
                           "Saúde', expected 'Ciências da Saúde' (article title) different from "
                           "'Ciências da Saúde' (section titles)",
                'advice': "Provide different titles for article and section (subj-group[@subj-group-type='heading']/subject)",
                'data': {
                    'en': [
                        {
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'parent_id': None,
                            'parent_lang': 'en',
                            'section': 'Health Sciences',
                            'subj_group_type': 'heading',
                            'subsections': ['Public Health']
                        },
                        {
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'parent_id': None,
                            'parent_lang': 'en',
                            'section': 'Public Health',
                            'subj_group_type': 'heading',
                            'subsections': []
                        }
                    ],
                    'pt': [
                        {
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': '01',
                            'parent_lang': 'pt',
                            'section': 'Ciências da Saúde',
                            'subj_group_type': 'heading',
                            'subsections': ['Saúde Pública']
                        },
                        {
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': '01',
                            'parent_lang': 'pt',
                            'section': 'Saúde Pública',
                            'subj_group_type': 'heading',
                            'subsections': []
                        }
                    ]
                },
            },
            {
                'title': 'Document title must not be similar to section title',
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': "article title: 'Ciências da Saúde', section titles: 'Saúde Pública'",
                'got_value': "article title: 'Ciências da Saúde', section titles: 'Saúde Pública'",
                'message': "Got article title: 'Ciências da Saúde', section titles: 'Saúde Pública', expected 'Ciências da Saúde' (article title) different from "
                           "'Saúde Pública' (section titles)",
                'advice': None,
                'data': {
                    'en': [
                        {
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'parent_id': None,
                            'parent_lang': 'en',
                            'section': 'Health Sciences',
                            'subj_group_type': 'heading',
                            'subsections': ['Public Health']
                        },
                        {
                            'parent': 'article',
                            'parent_article_type': 'research-article',
                            'parent_id': None,
                            'parent_lang': 'en',
                            'section': 'Public Health',
                            'subj_group_type': 'heading',
                            'subsections': []
                        }
                    ],
                    'pt': [
                        {
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': '01',
                            'parent_lang': 'pt',
                            'section': 'Ciências da Saúde',
                            'subj_group_type': 'heading',
                            'subsections': ['Saúde Pública']
                        },
                        {
                            'parent': 'sub-article',
                            'parent_article_type': 'translation',
                            'parent_id': '01',
                            'parent_lang': 'pt',
                            'section': 'Saúde Pública',
                            'subj_group_type': 'heading',
                            'subsections': []
                        }
                    ]
                },
            },
        ]
        obtained = list(self.article_toc_sections.validade_article_title_is_different_from_section_titles())

        self.assertEqual(len(obtained), 4)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_article_toc_sections_more_then_one(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título del artículo</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Health Sciences</subject>
                            <subj-group>
                                <subject>Improper Subject</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="pt">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Ciências da Saúde</subject>
                            <subj-group>
                                <subject>Assunto Indevido</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                    <title-group>
                        <article-title>Article title</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSectionsValidation(self.xmltree)

        expected = [
            {
                'title': "Exceding subject-group/subject",
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'exist',
                'response': 'CRITICAL',
                'expected_value': 'only one subject per language',
                'got_value': 'Health Sciences | Improper Subject',
                'message': 'Got Health Sciences | Improper Subject, expected only one subject per language',
                'advice': "One subject per language. Current subjects (en): ['Health Sciences', 'Improper Subject'].",
                'data': [
                    {
                        'parent': 'article',
                        'parent_article_type': 'research-article',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'section': 'Health Sciences',
                        'subj_group_type': 'heading',
                        'subsections': ['Improper Subject']
                    },
                    {
                        'parent': 'article',
                        'parent_article_type': 'research-article',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'section': 'Improper Subject',
                        'subj_group_type': None,
                        'subsections': []
                    }
                ]
            },
            {
                'title': "Exceding subject-group/subject",
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'exist',
                'response': 'CRITICAL',
                'expected_value': 'only one subject per language',
                'got_value': 'Ciências da Saúde | Assunto Indevido',
                'message': 'Got Ciências da Saúde | Assunto Indevido, expected only one subject per language',
                'advice': "One subject per language. Current subjects (pt): ['Ciências da Saúde', 'Assunto Indevido'].",
                'data': [
                    {
                        'parent': 'sub-article',
                        'parent_article_type': 'translation',
                        'parent_id': '01',
                        'parent_lang': 'pt',
                        'section': 'Ciências da Saúde',
                        'subj_group_type': 'heading',
                        'subsections': ['Assunto Indevido']
                    },
                    {
                        'parent': 'sub-article',
                        'parent_article_type': 'translation',
                        'parent_id': '01',
                        'parent_lang': 'pt',
                        'section': 'Assunto Indevido',
                        'subj_group_type': None,
                        'subsections': []
                    }
                ]
            }
        ]
        obtained = list(self.article_toc_sections.validate_article_section_and_subsection_number())

        self.assertEqual(len(obtained), 2)

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_article_toc_sections_subj_group_type(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título del artículo</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group>
                            <subject>Health Sciences</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="pt">
                <front-stub>
                    <article-categories>
                        <subj-group>
                            <subject>Ciências da Saúde</subject>
                        </subj-group>
                    </article-categories>
                    <title-group>
                        <article-title>Article title</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSectionsValidation(self.xmltree)
        expected_section = {
                "en": ["Health Sciences"],
                "pt": ["Ciências da Saúde"]
            }
        expected = [
            {
                'title': "Attribute '@subj-group-type' validation",
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'subj-group',
                'sub_item': '@subj-group-type',
                'validation_type': 'match',
                'response': 'CRITICAL',
                'expected_value': 'heading',
                'got_value': None,
                'message': 'Got None, expected heading',
                'advice': "the value for '@subj-group-type' must be heading",
                'data': {
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'section': 'Health Sciences',
                    'subj_group_type': None,
                    'subsections': []
                }
            },
            {
                'title': 'Document section title validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'Health Sciences',
                'got_value': 'Health Sciences',
                'message': "Got Health Sciences, expected one of ['Health Sciences']",
                'advice': None,
                'data': {
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'section': 'Health Sciences',
                    'subj_group_type': None,
                    'subsections': []
                 }
            },
            {
                'title': "Attribute '@subj-group-type' validation",
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'item': 'subj-group',
                'sub_item': '@subj-group-type',
                'validation_type': 'match',
                'response': 'CRITICAL',
                'expected_value': 'heading',
                'got_value': None,
                'message': 'Got None, expected heading',
                'advice': "the value for '@subj-group-type' must be heading",
                'data': {
                    'parent': 'sub-article',
                    'parent_article_type': 'translation',
                    'parent_id': '01',
                    'parent_lang': 'pt',
                    'section': 'Ciências da Saúde',
                    'subj_group_type': None,
                    'subsections': []
                }
            },
            {
                'title': 'Document section title validation',
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'Ciências da Saúde',
                'got_value': 'Ciências da Saúde',
                'message': "Got Ciências da Saúde, expected one of ['Ciências da Saúde']",
                'advice': None,
                'data': {
                    'parent': 'sub-article',
                    'parent_article_type': 'translation',
                    'parent_id': '01',
                    'parent_lang': 'pt',
                    'section': 'Ciências da Saúde',
                    'subj_group_type': None,
                    'subsections': []
                }
            },
        ]
        obtained = list(self.article_toc_sections.validate_article_toc_sections(expected_section))

        self.assertEqual(len(obtained), 4)

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)
