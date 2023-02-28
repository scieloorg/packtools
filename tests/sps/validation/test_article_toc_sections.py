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
                        <article-title>HEDGING FUTURE CASH FLOWS WITH INTEREST-RATE FUTURES CONTRACTS: A DURATION AND CONVEXITY ANALYSIS UNDER THE NELSON SIEGEL MODEL</article-title>
                    </title-group>
                </front-stub>
            </sub-article>        
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSectionsValidation(self.xmltree)
        expected_section = {
                "es": "Nome da seção do artigo em espanhol"
            }
        expected = [
            {
                'object': 'article section title',
                'expected_value': "Nome da seção do artigo em espanhol",
                'obtained_value': "Nome da seção do artigo em espanhol",
                'result': True,
                'message': "OK, section titles match the document"
            }
        ]
        result_article_sections = list(self.article_toc_sections.validate_article_toc_sections(expected_section))

        self.assertIn(expected[0], result_article_sections)

    def test_validate_sub_article_toc_sections(self):
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
                        <article-title>HEDGING FUTURE CASH FLOWS WITH INTEREST-RATE FUTURES CONTRACTS: A DURATION AND CONVEXITY ANALYSIS UNDER THE NELSON SIEGEL MODEL</article-title>
                    </title-group>
                </front-stub>
            </sub-article>        
            </article>
            """
        )
        self.article_toc_sections = ArticleTocSectionsValidation(self.xmltree)
        expected_section = {
                "en": "Nome da seção do sub-artigo em inglês"
            }
        expected = [
            {
                'object': 'sub-article section title',
                'expected_value': "Nome da seção do sub-artigo em inglês",
                'obtained_value': "Nome da seção do sub-artigo em inglês",
                'result': True,
                'message': "OK, section titles match the document"
            }
        ]
        result_sub_article_sections = list(self.article_toc_sections.validate_sub_article_toc_sections(expected_section))

        self.assertIn(expected[0], result_sub_article_sections)
