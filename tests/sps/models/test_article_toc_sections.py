from unittest import TestCase

from lxml import etree

from packtools.sps.models.v2.article_toc_sections import ArticleTocSections


class ArticleTocSectionsTest(TestCase):

    def test_article_section(self):
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
                    <subj-group subj-group-type="heading">
                        <subject>Ciências da Saúde</subject>
                    </subj-group>
                    <title-group>
                        <article-title>Article title</article-title>
                    </title-group>
                </front-stub>
            </sub-article>        
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSections(self.xmltree)

        expected = [
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'original_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'section': 'Health Sciences',
                'subj_group_type': 'heading',
                'subsections': [],
                'subject': 'Health Sciences',
                'article_title': 'Título del artículo',
                'journal': None,
            },
            {
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'original_article_type': 'research-article',
                'parent_id': '01',
                'parent_lang': 'pt',
                'section': 'Ciências da Saúde',
                'subj_group_type': 'heading',
                'subsections': [],
                'subject': 'Ciências da Saúde',
                'article_title': 'Article title',
                'journal': None,
            }
        ]
        obtained = list(self.article_toc_sections.sections)

        self.assertEqual(len(obtained), 2)

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_article_section_without_heading(self):
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
                    <subj-group>
                        <subject>Ciências da Saúde</subject>
                    </subj-group>
                    <title-group>
                        <article-title>Article title</article-title>
                    </title-group>
                </front-stub>
            </sub-article>        
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSections(self.xmltree)

        expected = [
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'section': 'Health Sciences',
                'subj_group_type': None,
                'subsections': [],
                'original_article_type': 'research-article',
                'subject': 'Health Sciences',
                'article_title': 'Título del artículo',
                'journal': None,
            },
            {
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'section': 'Ciências da Saúde',
                'subj_group_type': None,
                'subsections': [],
                'original_article_type': 'research-article',
                'subject': 'Ciências da Saúde',
                'article_title': 'Article title',
                'journal': None,
            }
        ]
        obtained = list(self.article_toc_sections.sections)

        self.assertEqual(len(obtained), 2)

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_article_section_dict(self):
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
        self.article_toc_sections = ArticleTocSections(self.xmltree)

        expected = {
            'en': [
                {
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'section': 'Health Sciences',
                    'subj_group_type': 'heading',
                    'subsections': [],
                    'original_article_type': 'research-article',
                    'subject': 'Health Sciences',
                    'article_title': 'Título del artículo',
                    'journal': None,
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
                    'subsections': [],
                    'original_article_type': 'research-article',
                    'subject': 'Ciências da Saúde',
                    'article_title': 'Article title',
                    'journal': None,
                }
            ]
        }

        obtained = self.article_toc_sections.sections_dict

        self.assertDictEqual(obtained, expected)

    def test_article_section_empty_tag(self):
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
                            <subject></subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="pt">
                <front-stub>
                    <subj-group subj-group-type="heading">
                        <subject></subject>
                    </subj-group>
                    <title-group>
                        <article-title>Article title</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSections(self.xmltree)

        expected = [
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'section': '',
                'subj_group_type': 'heading',
                'subsections': [],
                'original_article_type': 'research-article',
                'subject': '',
                'article_title': 'Título del artículo',
                'journal': None,
            },
            {
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'section': '',
                'subj_group_type': 'heading',
                'subsections': [],
                'original_article_type': 'research-article',
                'subject': '',
                'article_title': 'Article title',
                'journal': None,
            }
        ]
        obtained = list(self.article_toc_sections.sections)

        self.assertEqual(len(obtained), 2)

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_article_section_missing_tag(self):
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

                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="pt">
                <front-stub>
                    <subj-group subj-group-type="heading">

                    </subj-group>
                    <title-group>
                        <article-title>Article title</article-title>
                    </title-group>
                </front-stub>
            </sub-article>
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSections(self.xmltree)

        expected = [
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'section': '',
                'subj_group_type': 'heading',
                'subsections': [],
                'original_article_type': 'research-article',
                'subject': '',
                'article_title': 'Título del artículo',
                'journal': None,
            },
            {
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'section': '',
                'subj_group_type': 'heading',
                'subsections': [],
                'original_article_type': 'research-article',
                'subject': '',
                'article_title': 'Article title',
                'journal': None,
            }
        ]

        obtained = list(self.article_toc_sections.sections)

        self.assertEqual(len(obtained), 2)

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_article_section_with_subsection(self):
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
                            <subj-group subj-group-type="heading">
                                <subject>Health Sciences Subsection</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="pt">
                <front-stub>
                    <subj-group subj-group-type="heading">
                        <subject>Ciências da Saúde</subject>
                        <subj-group subj-group-type="heading">
                            <subject>Subseção Ciências da Saúde</subject>
                        </subj-group>
                    </subj-group>
                    <title-group>
                        <article-title>Article title</article-title>
                    </title-group>
                </front-stub>
            </sub-article>        
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSections(self.xmltree)

        expected = [
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'section': 'Health Sciences',
                'subj_group_type': 'heading',
                'subsections': ['Health Sciences Subsection'],
                'original_article_type': 'research-article',
                'subject': 'Health Sciences',
                'article_title': 'Título del artículo',
                'journal': None,
            },
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'section': 'Health Sciences Subsection',
                'subj_group_type': 'heading',
                'subsections': [],
                'original_article_type': 'research-article',
                'subject': 'Health Sciences Subsection',
                'article_title': 'Título del artículo',
                'journal': None,
            },
            {
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'section': 'Ciências da Saúde',
                'subj_group_type': 'heading',
                'subsections': ['Subseção Ciências da Saúde'],
                'original_article_type': 'research-article',
                'subject': 'Ciências da Saúde',
                'article_title': 'Article title',
                'journal': None,
            },
            {
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'section': 'Subseção Ciências da Saúde',
                'subj_group_type': 'heading',
                'subsections': [],
                'original_article_type': 'research-article',
                'subject': 'Subseção Ciências da Saúde',
                'article_title': 'Article title',
                'journal': None,
            }
        ]
        obtained = list(self.article_toc_sections.sections)

        self.assertEqual(len(obtained), 4)

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_article_section_with_subsection_dict(self):
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
                            <subj-group subj-group-type="heading">
                                <subject>Health Sciences Subsection</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="pt">
                <front-stub>
                    <subj-group subj-group-type="heading">
                        <subject>Ciências da Saúde</subject>
                        <subj-group subj-group-type="heading">
                            <subject>Subseção Ciências da Saúde</subject>
                        </subj-group>
                    </subj-group>
                    <title-group>
                        <article-title>Article title</article-title>
                    </title-group>
                </front-stub>
            </sub-article>        
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSections(self.xmltree)

        expected = {
            "en": [
                {
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'section': 'Health Sciences',
                    'subj_group_type': 'heading',
                    'subsections': ['Health Sciences Subsection'],
                    'original_article_type': 'research-article',
                    'subject': 'Health Sciences',
                    'article_title': 'Título del artículo',
                    'journal': None,
                },
                {
                    'parent': 'article',
                    'parent_article_type': 'research-article',
                    'parent_id': None,
                    'parent_lang': 'en',
                    'section': 'Health Sciences Subsection',
                    'subj_group_type': 'heading',
                    'subsections': [],
                    'original_article_type': 'research-article',
                    'subject': 'Health Sciences Subsection',
                    'article_title': 'Título del artículo',
                    'journal': None,
                }
            ],
            "pt": [
                {
                    'parent': 'sub-article',
                    'parent_article_type': 'translation',
                    'parent_id': '01',
                    'parent_lang': 'pt',
                    'section': 'Ciências da Saúde',
                    'subj_group_type': 'heading',
                    'subsections': ['Subseção Ciências da Saúde'],
                    'original_article_type': 'research-article',
                    'subject': 'Ciências da Saúde',
                    'article_title': 'Article title',
                    'journal': None,
                },
                {
                    'parent': 'sub-article',
                    'parent_article_type': 'translation',
                    'parent_id': '01',
                    'parent_lang': 'pt',
                    'section': 'Subseção Ciências da Saúde',
                    'subj_group_type': 'heading',
                    'subsections': [],
                    'original_article_type': 'research-article',
                    'subject': 'Subseção Ciências da Saúde',
                    'article_title': 'Article title',
                    'journal': None,
                }
            ]
        }
        obtained = self.article_toc_sections.sections_dict

        self.assertEqual(len(obtained), 2)

        for lang, sections_list in obtained.items():
            for i, item in enumerate(sections_list):
                with self.subTest(lang):
                    self.assertDictEqual(expected[lang][i], item)
