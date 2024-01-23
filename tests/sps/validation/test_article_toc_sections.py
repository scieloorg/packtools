from unittest import TestCase

from lxml import etree

from packtools.sps.validation.article_toc_sections import ArticleTocSectionsValidation


class ArticleTocSectionsTest(TestCase):

    def test_validate_article_toc_sections_success(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xml:lang="es">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título do artigo em espanhol</article-title>
                    </title-group>
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
                'title': 'Article section title validation',
                'xpath': ".//article-meta//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': ['Nome da seção do artigo em espanhol'],
                'got_value': ['Nome da seção do artigo em espanhol'],
                'message': 'Got [\'Nome da seção do artigo em espanhol\'] expected [\'Nome da seção do artigo em espanhol\']',
                'advice': None
            },
            {
                'title': 'Sub-article section title validation',
                'xpath': ".//sub-article[@article-type='translation']//front-stub//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': ['Nome da seção do sub-artigo em inglês'],
                'got_value': ['Nome da seção do sub-artigo em inglês'],
                'message': 'Got [\'Nome da seção do sub-artigo em inglês\'] expected [\'Nome da seção do sub-artigo em inglês\']',
                'advice': None
            }
        ]
        obtained = self.article_toc_sections.validate_article_toc_sections(expected_section)

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_toc_sections_fail_sections_missing(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xml:lang="es">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título do artigo em espanhol</article-title>
                    </title-group>
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
                "pt": ["Nome da seção do artigo em português"],
                "fr": ["Nome da seção do sub-artigo em francês"]
            }
        expected = [
            {
                'title': 'Article or sub-article section title validation',
                'xpath': ".//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': ['Nome da seção do artigo em português'],
                'got_value': None,
                'message': 'Got None expected [\'Nome da seção do artigo em português\']',
                'advice': "Provide sections as expected: ['Nome da seção do artigo em português']"
            },
            {
                'title': 'Article or sub-article section title validation',
                'xpath': ".//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': ['Nome da seção do sub-artigo em francês'],
                'got_value': None,
                'message': 'Got None expected [\'Nome da seção do sub-artigo em francês\']',
                'advice': "Provide sections as expected: ['Nome da seção do sub-artigo em francês']"
            }
        ]
        obtained = self.article_toc_sections.validate_article_toc_sections(expected_section)

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_toc_sections_fail(self):
        self.maxDiff = None
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
                'title': 'Article section title validation',
                'xpath': ".//article-meta//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': ['Nome da seção do sub-artigo em espanhol'],
                'got_value': ['Nome da seção do artigo em espanhol'],
                'message': 'Got [\'Nome da seção do artigo em espanhol\'] expected [\'Nome da seção do sub-artigo em espanhol\']',
                'advice': "Provide sections as expected: ['Nome da seção do sub-artigo em espanhol']"
            },
            {
                'title': 'Sub-article section title validation',
                'xpath': ".//sub-article[@article-type='translation']//front-stub//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': ['Nome da seção do artigo em inglês'],
                'got_value': ['Nome da seção do sub-artigo em inglês'],
                'message': 'Got [\'Nome da seção do sub-artigo em inglês\'] expected [\'Nome da seção do artigo em inglês\']',
                'advice': "Provide sections as expected: ['Nome da seção do artigo em inglês']"
            }
        ]
        obtained = self.article_toc_sections.validate_article_toc_sections(expected_section)

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_toc_sections_fail_journal_has_no_section(self):
        self.maxDiff = None
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
        expected_section = {
            "en": ["Nome da seção do sub-artigo em inglês"]
        }
        expected = [
            {
                'title': 'Sub-article section title validation',
                'xpath': ".//sub-article[@article-type='translation']//front-stub//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': ['Nome da seção do sub-artigo em inglês'],
                'got_value': ['Nome da seção do sub-artigo em inglês'],
                'message': 'Got [\'Nome da seção do sub-artigo em inglês\'] expected [\'Nome da seção do sub-artigo em inglês\']',
                'advice': None
            }
        ]
        obtained = self.article_toc_sections.validate_article_toc_sections(expected_section)

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validade_article_title_is_different_from_section_titles_success(self):
        self.maxDiff = None
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
                'title': 'Article section title validation',
                'xpath': ".//article-meta//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'article title different from section titles',
                'got_value': 'article title different from section titles',
                'message': "Article title: Título do artigo em espanhol, section titles: ['Nome da seção do artigo em espanhol']",
                'advice': None
            },
            {
                'title': 'Sub-article section title validation',
                'xpath': ".//sub-article[@article-type='translation']//front-stub//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': 'article title different from section titles',
                'got_value': 'article title different from section titles',
                'message': "Article title: Título do sub-artigo em inglês, section titles: ['Nome da seção do sub-artigo em inglês']",
                'advice': None
            }
        ]
        obtained = self.article_toc_sections.validade_article_title_is_different_from_section_titles()

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validade_article_title_is_different_from_section_titles_fail(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xml:lang="es">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Editorial</article-title>
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
                'title': 'Article section title validation',
                'xpath': ".//article-meta//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': 'article title different from section titles',
                'got_value': 'article title same as section titles',
                'message': "Article title: Editorial, section titles: ['Editorial']",
                'advice': 'Provide different titles between article and sections'
            },
            {
                'title': 'Sub-article section title validation',
                'xpath': ".//sub-article[@article-type='translation']//front-stub//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': 'article title different from section titles',
                'got_value': 'article title same as section titles',
                'message': "Article title: Editorial, section titles: ['Editorial']",
                'advice': 'Provide different titles between article and sections'
            }
        ]
        obtained = self.article_toc_sections.validade_article_title_is_different_from_section_titles()

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)
