from unittest import TestCase

from lxml import etree

from packtools.sps.validation.article_toc_sections import ArticleTocSectionsValidation


class ArticleTocSectionsTest(TestCase):

    def test_validate_article_toc_sections_returns_ok(self):
        self.xmltree = etree.fromstring(
            """
            <article xml:lang="es">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título do artigo em espanhol</article-title>
                            <trans-title-group xml:lang="en">
                                <trans-title>Título do artigo em inglês</trans-title>
                            </trans-title-group>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                        <subject>Nome da seção do artigo em espanhol</subject>
                            <subj-group>
                            <subject>Food Safety</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                    <title-group>
                        <article-title>Título do artigo em espanhol</article-title>
                    </title-group>
                </article-meta>
            </front>
            <sub-article article-type="translation" xml:lang="en">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                        <subject>Nome da seção do sub-artigo em inglês</subject>
                            <subj-group>
                            <subject>Food Safety</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                    <title-group>
                        <article-title>HEDGING FUTURE CASH FLOWS WITH INTEREST-RATE FUTURES CONTRACTS: A DURATION AND
                         CONVEXITY ANALYSIS UNDER THE NELSON SIEGEL MODEL</article-title>
                    </title-group>
                </front-stub>
            </sub-article>        
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSectionsValidation(self.xmltree)
        expected_section = {
                "es": ["Nome da seção do artigo em espanhol"],
                "en": ["Nome da seção do sub-artigo em inglês"]
            }
        expected = [
            {
                'object': 'article section title',
                'expected_value': ["Nome da seção do artigo em espanhol"],
                'obtained_value': "Nome da seção do artigo em espanhol",
                'result': True,
                'message': "OK, section titles match the document"
            },
            {
                'object': 'sub-article section title',
                'expected_value': ["Nome da seção do sub-artigo em inglês"],
                'obtained_value': "Nome da seção do sub-artigo em inglês",
                'result': True,
                'message': "OK, section titles match the document"
            }
        ]
        result_article_sections = self.article_toc_sections.validate_article_toc_sections(expected_section)

        self.assertIn(expected[0], result_article_sections)
        self.assertIn(expected[1], result_article_sections)

    def test_validate_article_toc_sections_returns_error(self):
        self.xmltree = etree.fromstring(
            """
            <article xml:lang="es">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título do artigo em espanhol</article-title>
                            <trans-title-group xml:lang="en">
                                <trans-title>Título do artigo em inglês</trans-title>
                            </trans-title-group>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                        <subject>Nome da seção do artigo em espanhol</subject>
                            <subj-group>
                            <subject>Food Safety</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                    <title-group>
                        <article-title>Título do artigo em espanhol</article-title>
                    </title-group>
                </article-meta>
            </front>
            <sub-article article-type="translation" xml:lang="en">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                        <subject>Nome da seção do sub-artigo em inglês</subject>
                            <subj-group>
                            <subject>Food Safety</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                    <title-group>
                        <article-title>HEDGING FUTURE CASH FLOWS WITH INTEREST-RATE FUTURES CONTRACTS: A DURATION AND
                         CONVEXITY ANALYSIS UNDER THE NELSON SIEGEL MODEL</article-title>
                    </title-group>
                </front-stub>
            </sub-article>        
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSectionsValidation(self.xmltree)
        expected_section = {
            "es": ["Nome da seção do sub-artigo em espanhol"],
            "en": ["Nome da seção do artigo em inglês"]
        }
        expected = [
            {
                'object': 'article section title',
                'expected_value': ["Nome da seção do sub-artigo em espanhol"],
                'obtained_value': "Nome da seção do artigo em espanhol",
                'result': False,
                'message': "ERROR, section titles no match the document"
            },
            {
                'object': 'sub-article section title',
                'expected_value': ["Nome da seção do artigo em inglês"],
                'obtained_value': "Nome da seção do sub-artigo em inglês",
                'result': False,
                'message': "ERROR, section titles no match the document"
            }
        ]
        result_article_sections = self.article_toc_sections.validate_article_toc_sections(expected_section)

        self.assertIn(expected[0], result_article_sections)
        self.assertIn(expected[1], result_article_sections)

    def test_validate_article_toc_sections_returns_error_journal_has_no_section(self):
        self.xmltree = etree.fromstring(
            """
            <article xml:lang="es">
            <front>
                <article-meta>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                        <subject>Nome da seção do artigo em espanhol</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" xml:lang="en">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                        <subject>Nome da seção do sub-artigo em inglês</subject>
                        </subj-group>
                    </article-categories>
                </front-stub>
            </sub-article>        
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSectionsValidation(self.xmltree)
        # A revista publica somente seções em inglês.
        toc_section = {
            "en": ["Nome da seção do sub-artigo em inglês"]
        }
        expected = [
            {
                'object': 'article section title',
                'expected_value': None,
                'obtained_value': "Nome da seção do artigo em espanhol",
                'result': False,
                'message': "ERROR, section titles no match the document"
            },
            {
                'object': 'sub-article section title',
                'expected_value': ["Nome da seção do sub-artigo em inglês"],
                'obtained_value': "Nome da seção do sub-artigo em inglês",
                'result': True,
                'message': "OK, section titles match the document"
            }
        ]
        result_article_sections = self.article_toc_sections.validate_article_toc_sections(toc_section)
        for index, item in enumerate(expected):
            with self.subTest(index):
                self.assertIn(item, result_article_sections)
        # self.assertIn(expected[0], result_article_sections)
        # self.assertIn(expected[1], result_article_sections)

    def test_validade_article_title_is_different_from_section_titles_returns_ok(self):
        self.xmltree = etree.fromstring(
            """
            <article xml:lang="es">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título do artigo em espanhol</article-title>
                            <trans-title-group xml:lang="en">
                                <trans-title>Título do artigo em inglês</trans-title>
                            </trans-title-group>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                        <subject>Nome da seção do artigo em espanhol</subject>
                            <subj-group>
                            <subject>Food Safety</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                    <title-group>
                        <article-title>Título do artigo em espanhol</article-title>
                    </title-group>
                </article-meta>
            </front>
            <sub-article article-type="translation" xml:lang="en">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                        <subject>Nome da seção do sub-artigo em inglês</subject>
                            <subj-group>
                            <subject>Food Safety</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                    <title-group>
                        <article-title>Título do sub-artigo em inglês</article-title>
                    </title-group>
                </front-stub>
            </sub-article>        
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSectionsValidation(self.xmltree)
        expected = [
            {
                'object': 'section title',
                'article_title': {
                    'es': 'Título do artigo em espanhol',
                    'en': 'Título do sub-artigo em inglês'
                },
                'section_title': {
                    "es": "Nome da seção do artigo em espanhol",
                    "en": "Nome da seção do sub-artigo em inglês",
                },
                'result': True,
                'message': 'OK, all section titles are different from the title of the article'
            }
        ]
        result_article_sections = self.article_toc_sections.validade_article_title_is_different_from_section_titles()

        self.assertEqual(expected[0]['message'], result_article_sections[0]['message'])
        self.assertEqual(expected[0]['result'], result_article_sections[0]['result'])
        self.assertDictEqual(expected[0]['article_title'], result_article_sections[0]['article_title'])
        self.assertDictEqual(expected[0]['section_title'], result_article_sections[0]['section_title'])

    def test_validade_article_title_is_different_from_section_titles_returns_error(self):
        self.xmltree = etree.fromstring(
            """
            <article xml:lang="es">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Editorial</article-title>
                            <trans-title-group xml:lang="en">
                                <trans-title>Editorial</trans-title>
                            </trans-title-group>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                        <subject>Editorial</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" xml:lang="en">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                        <subject>Editorial</subject>
                        </subj-group>
                    </article-categories>
                    <title-group>
                        <article-title>Editorial</article-title>
                    </title-group>
                </front-stub>
            </sub-article>        
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSectionsValidation(self.xmltree)
        expected = [
            {
                'object': 'section title',
                'article_title': {
                    "es": "Editorial",
                    "en": "Editorial",
                },
                'section_title': {
                    "es": "Editorial",
                    "en": "Editorial",
                },
                'result': False,
                'message': 'ERROR: Article title ("Editorial") must not be the same'
                           ' as the section title ("Editorial")'
            }
        ]
        result_article_sections = self.article_toc_sections.validade_article_title_is_different_from_section_titles()

        self.assertListEqual(expected, result_article_sections)
