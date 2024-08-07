from unittest import TestCase

from lxml import etree

from packtools.sps.utils import xml_utils
from packtools.sps.validation.article_toc_sections import ArticleTocSectionsValidation


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
                            <subj-group subj-group-type="sub-heading">
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
                            <subj-group subj-group-type="sub-heading">
                                <subject>Saúde Pública</subject>
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
        expected_section = {
                "en": ["Health Sciences"],
                "pt": ["Ciências da Saúde"]
            }
        expected = [
            {
                'title': 'Article section title validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['Health Sciences'],
                'got_value': 'Health Sciences',
                'message': "Got Health Sciences, expected ['Health Sciences']",
                'advice': None,
                'data': {
                    'en': {
                        'parent': 'article',
                        'parent_article_type': 'research-article',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'text': 'Health Sciences'
                    },
                    'pt': {
                        'parent': 'sub-article',
                        'parent_article_type': 'translation',
                        'parent_id': '01',
                        'parent_lang': 'pt',
                        'text': 'Ciências da Saúde'
                    }
                },
            },
            {
                'title': 'Sub-article (id=01) section title validation',
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['Ciências da Saúde'],
                'got_value': 'Ciências da Saúde',
                'message': "Got Ciências da Saúde, expected ['Ciências da Saúde']",
                'advice': None,
                'data': {
                    'en': {
                        'parent': 'article',
                        'parent_article_type': 'research-article',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'text': 'Health Sciences'
                    },
                    'pt': {
                        'parent': 'sub-article',
                        'parent_article_type': 'translation',
                        'parent_id': '01',
                        'parent_lang': 'pt',
                        'text': 'Ciências da Saúde'
                    }
                },
            },
        ]
        obtained = list(self.article_toc_sections.validate_article_toc_sections(expected_section))

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_article_toc_sections_fail_sections_not_obtained(self):
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

                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" xml:lang="en">
                <front-stub>
                    <article-categories>

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
                'title': 'Article or sub-article section title validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'exist',
                'response': 'CRITICAL',
                'expected_value': {'en': ['Health Sciences'], 'pt': ['Ciências da Saúde']},
                'got_value': {},
                'message': "Got {}, expected {'en': ['Health Sciences'], 'pt': ['Ciências da Saúde']}",
                'advice': 'Provide a subject value for <subj-group subj-group-type="heading">',
                'data': {},
            }
        ]
        obtained = list(self.article_toc_sections.validate_article_toc_sections(expected_section))

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

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
                            <subj-group subj-group-type="sub-heading">
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
                            <subj-group subj-group-type="sub-heading">
                                <subject>Saúde Pública</subject>
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
        expected_section = {
            "en": ["Article"],
            "pt": ["Artigo"]
        }
        expected = [
            {
                'title': 'Article section title validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'value in list',
                'response': 'CRITICAL',
                'expected_value': ['Article'],
                'got_value': 'Health Sciences',
                'message': "Got Health Sciences, expected ['Article']",
                'advice': 'Provide missing section for language: en',
                'data': {
                    'en': {
                        'parent': 'article',
                        'parent_article_type': 'research-article',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'text': 'Health Sciences'
                    },
                    'pt': {
                        'parent': 'sub-article',
                        'parent_article_type': 'translation',
                        'parent_id': '01',
                        'parent_lang': 'pt',
                        'text': 'Ciências da Saúde'
                    }
                },
            },
            {
                'title': 'Sub-article (id=01) section title validation',
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'value in list',
                'response': 'CRITICAL',
                'expected_value': ['Artigo'],
                'got_value': 'Ciências da Saúde',
                'message': "Got Ciências da Saúde, expected ['Artigo']",
                'advice': 'Provide missing section for language: pt',
                'data': {
                    'en': {
                        'parent': 'article',
                        'parent_article_type': 'research-article',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'text': 'Health Sciences'
                    },
                    'pt': {
                        'parent': 'sub-article',
                        'parent_article_type': 'translation',
                        'parent_id': '01',
                        'parent_lang': 'pt',
                        'text': 'Ciências da Saúde'
                    }
                },
            },
        ]
        obtained = list(self.article_toc_sections.validate_article_toc_sections(expected_section))

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
                            <subj-group subj-group-type="sub-heading">
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
                            <subj-group subj-group-type="sub-heading">
                                <subject>Saúde Pública</subject>
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
        expected_section = {
            "en": ["Article"],
            "pt": ["Ciências da Saúde"]
        }
        expected = [
            {
                'title': 'Article section title validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'value in list',
                'response': 'CRITICAL',
                'expected_value': ['Article'],
                'got_value': 'Health Sciences',
                'message': "Got Health Sciences, expected ['Article']",
                'advice': 'Provide missing section for language: en',
                'data': {
                    'en': {
                        'parent': 'article',
                        'parent_article_type': 'research-article',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'text': 'Health Sciences'
                    },
                    'pt': {
                        'parent': 'sub-article',
                        'parent_article_type': 'translation',
                        'parent_id': '01',
                        'parent_lang': 'pt',
                        'text': 'Ciências da Saúde'
                    }
                },
            },
            {
                'title': 'Sub-article (id=01) section title validation',
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['Ciências da Saúde'],
                'got_value': 'Ciências da Saúde',
                'message': "Got Ciências da Saúde, expected ['Ciências da Saúde']",
                'advice': None,
                'data': {
                    'en': {
                        'parent': 'article',
                        'parent_article_type': 'research-article',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'text': 'Health Sciences'
                    },
                    'pt': {
                        'parent': 'sub-article',
                        'parent_article_type': 'translation',
                        'parent_id': '01',
                        'parent_lang': 'pt',
                        'text': 'Ciências da Saúde'
                    }
                },
            },
        ]
        obtained = list(self.article_toc_sections.validate_article_toc_sections(expected_section))

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
                            <subj-group subj-group-type="sub-heading">
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
                            <subj-group subj-group-type="sub-heading">
                                <subject>Saúde Pública</subject>
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
        expected_section = {
            "en": ["Article"],
            "pt": ["Artigo"]
        }
        expected = [
            {
                'title': 'Article section title validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'value in list',
                'response': 'CRITICAL',
                'expected_value': ['Article'],
                'got_value': 'Health Sciences',
                'message': "Got Health Sciences, expected ['Article']",
                'advice': 'Provide missing section for language: en',
                'data': {
                    'en': {
                        'parent': 'article',
                        'parent_article_type': 'research-article',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'text': 'Health Sciences'
                    },
                    'pt': {
                        'parent': 'sub-article',
                        'parent_article_type': 'translation',
                        'parent_id': '01',
                        'parent_lang': 'pt',
                        'text': 'Ciências da Saúde'
                    }
                },
            },
            {
                'title': 'Sub-article (id=01) section title validation',
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'value in list',
                'response': 'CRITICAL',
                'expected_value': ['Artigo'],
                'got_value': 'Ciências da Saúde',
                'message': "Got Ciências da Saúde, expected ['Artigo']",
                'advice': 'Provide missing section for language: pt',
                'data': {
                    'en': {
                        'parent': 'article',
                        'parent_article_type': 'research-article',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'text': 'Health Sciences'
                    },
                    'pt': {
                        'parent': 'sub-article',
                        'parent_article_type': 'translation',
                        'parent_id': '01',
                        'parent_lang': 'pt',
                        'text': 'Ciências da Saúde'
                    }
                },
            },
        ]
        obtained = list(self.article_toc_sections.validate_article_toc_sections(expected_section))

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
        expected_section = {}
        expected = [
            {
                'title': 'Article or sub-article section title validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'exist',
                'response': 'CRITICAL',
                'expected_value': {},
                'got_value': {},
                'message': 'Got {}, expected {}',
                'advice': 'Provide a subject value for <subj-group subj-group-type="heading">',
                'data': {},
            }
        ]
        obtained = list(self.article_toc_sections.validate_article_toc_sections(expected_section))

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

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
                            <subj-group subj-group-type="sub-heading">
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
                            <subj-group subj-group-type="sub-heading">
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
                'title': 'Article or sub-article section title validation',
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': "'Health Sciences Studies' (article title) different from 'Health Sciences' ("
                                  "section titles)",
                'got_value': "article title: 'Health Sciences Studies', section titles: 'Health Sciences'",
                'message': "Got article title: 'Health Sciences Studies', section titles: 'Health Sciences', "
                           "expected 'Health Sciences Studies' (article title) different from 'Health Sciences' ("
                           "section titles)",
                'advice': None,
                'data': {
                    'en': {
                        'parent': 'article',
                        'parent_article_type': 'research-article',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'text': 'Health Sciences'
                    },
                    'pt': {
                        'parent': 'sub-article',
                        'parent_article_type': 'translation',
                        'parent_id': '01',
                        'parent_lang': 'pt',
                        'text': 'Ciências da Saúde'
                    }
                },
            },
            {
                'title': 'Sub-article (id=01) section title validation',
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': "'Estudos sobre Ciências da Saúde' (article title) different from 'Ciências da "
                                  "Saúde' (section titles)",
                'got_value': "article title: 'Estudos sobre Ciências da Saúde', section titles: 'Ciências da Saúde'",
                'message': "Got article title: 'Estudos sobre Ciências da Saúde', section titles: 'Ciências da "
                           "Saúde', expected 'Estudos sobre Ciências da Saúde' (article title) different from "
                           "'Ciências da Saúde' (section titles)",
                'advice': None,
                'data': {
                    'en': {
                        'parent': 'article',
                        'parent_article_type': 'research-article',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'text': 'Health Sciences'
                    },
                    'pt': {
                        'parent': 'sub-article',
                        'parent_article_type': 'translation',
                        'parent_id': '01',
                        'parent_lang': 'pt',
                        'text': 'Ciências da Saúde'
                    }
                },
            },
        ]
        obtained = list(self.article_toc_sections.validade_article_title_is_different_from_section_titles())

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
                            <subj-group subj-group-type="sub-heading">
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
                            <subj-group subj-group-type="sub-heading">
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
                'title': 'Article or sub-article section title validation',
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
                    'en': {
                        'parent': 'article',
                        'parent_article_type': 'research-article',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'text': 'Health Sciences'
                    },
                    'pt': {
                        'parent': 'sub-article',
                        'parent_article_type': 'translation',
                        'parent_id': '01',
                        'parent_lang': 'pt',
                        'text': 'Ciências da Saúde'
                    }
                },
            },
            {
                'title': 'Sub-article (id=01) section title validation',
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
                    'en': {
                        'parent': 'article',
                        'parent_article_type': 'research-article',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'text': 'Health Sciences'
                    },
                    'pt': {
                        'parent': 'sub-article',
                        'parent_article_type': 'translation',
                        'parent_id': '01',
                        'parent_lang': 'pt',
                        'text': 'Ciências da Saúde'
                    }
                },
            },
        ]
        obtained = list(self.article_toc_sections.validade_article_title_is_different_from_section_titles())

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_article_toc_sections_to_fix_bug(self):
        self.maxDiff = None
        self.xmltree = xml_utils.get_xml_tree('tests/samples/1518-8787-rsp-56-37.xml')

        self.article_toc_sections = ArticleTocSectionsValidation(self.xmltree)
        expected_section = {
             "en": ["Comments"],
             "pt": ["Comentários"]
        }
        expected = [
            {
                'title': 'Article section title validation',
                'parent': 'article',
                'parent_article_type': 'other',
                'parent_id': None,
                'parent_lang': 'en',
                'item': 'subj-group',
                'sub_item': 'subject',
                'validation_type': 'value in list',
                'response': 'OK',
                'got_value': 'Comments',
                'expected_value': ['Comments'],
                'message': "Got Comments, expected ['Comments']",
                'advice': None,
                'data': {
                    'en': {
                        'parent': 'article',
                        'parent_article_type': 'other',
                        'parent_id': None,
                        'parent_lang': 'en',
                        'text': 'Comments'
                    }
                },
            }
        ]
        obtained = list(self.article_toc_sections.validate_article_toc_sections(expected_section))

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

        self.assertEqual(len(obtained), 1)
