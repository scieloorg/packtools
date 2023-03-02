from unittest import TestCase

from lxml import etree

from packtools.sps.validation.article_toc_sections import ArticleTocSectionsValidation


class ArticleTocSectionsTest(TestCase):

    def test_validate_article_toc_sections(self):
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
                "es": "Nome da seção do artigo em espanhol",
                "en": "Nome da seção do sub-artigo em inglês"
            }
        expected = [
            {
                'object': 'article section title',
                'expected_value': "Nome da seção do artigo em espanhol",
                'obtained_value': "Nome da seção do artigo em espanhol",
                'result': True,
                'message': "OK, section titles match the document"
            },
            {
                'object': 'sub-article section title',
                'expected_value': "Nome da seção do sub-artigo em inglês",
                'obtained_value': "Nome da seção do sub-artigo em inglês",
                'result': True,
                'message': "OK, section titles match the document"
            }
        ]
        result_article_sections = self.article_toc_sections.validate_article_toc_sections(expected_section)

        self.assertIn(expected[0], result_article_sections)
        self.assertIn(expected[1], result_article_sections)

    def test_validate_article_toc_sections_no_sections(self):
        self.xmltree = etree.fromstring(
            """
            <article xml:lang="es">
            <front>
                <article-meta>
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
        expected_section = {}
        expected = [{
            'object': 'section title',
            'expected_value': "0 section titles",
            'obtained_value': "2 section titles",
            'result': False,
            'message': "ERROR, number of titles found is different from the expected number of titles"
        }]
        result_article_sections = self.article_toc_sections.validate_article_toc_sections(expected_section)

        self.assertListEqual(expected, result_article_sections)

    def test_validate_article_toc_sections_numbers_diff(self):
        self.xmltree = etree.fromstring(
            """
            <article xml:lang="es">
            <front>
                <article-meta>
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
            "es": "Nome da seção do artigo em espanhol",
            "en": "Nome da seção do sub-artigo em inglês",
            "pt": "Nome da seção do artigo em português"
        }
        expected = [{
            'object': 'section title',
            'expected_value': "3 section titles",
            'obtained_value': "2 section titles",
            'result': False,
            'message': "ERROR, number of titles found is different from the expected number of titles"
        }]
        result_article_sections = self.article_toc_sections.validate_article_toc_sections(expected_section)

        self.assertListEqual(expected, result_article_sections)

    def test_validade_article_title_is_different_from_section_titles(self):
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
                'expected_value': {
                    'es': 'Título do artigo em espanhol',
                    'en': 'Título do sub-artigo em inglês'
                },
                'obtained_value': {
                    "es": "Nome da seção do artigo em espanhol",
                    "en": "Nome da seção do sub-artigo em inglês",
                },
                'result': True,
                'message': 'OK, all section titles are different from the title of the article'
            }
        ]
        result_article_sections = self.article_toc_sections.validade_article_title_is_different_from_section_titles()

        self.assertListEqual(expected, result_article_sections)

    def test_validade_article_title_is_no_different_from_section_titles(self):
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
                        <article-title>Nome da seção do sub-artigo em inglês</article-title>
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
                'expected_value': {
                    'es': 'Título do artigo em espanhol',
                    'en': 'Nome da seção do sub-artigo em inglês'
                },
                'obtained_value': {
                    "es": "Nome da seção do artigo em espanhol",
                    "en": "Nome da seção do sub-artigo em inglês",
                },
                'result': False,
                'message': 'ERROR: Article title ("Nome da seção do sub-artigo em inglês") must not be the same'
                           ' as the section title ("Nome da seção do sub-artigo em inglês")'
            }
        ]
        result_article_sections = self.article_toc_sections.validade_article_title_is_different_from_section_titles()

        self.assertListEqual(expected, result_article_sections)
