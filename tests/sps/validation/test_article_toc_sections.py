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
                        <article-title>Título del artículo</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Artículo</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="en">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Article</subject>
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
                "es": ["Artículo", "Editorial", "Carta"],
                "en": ["Article", "Editorial", "Letter"]
            }
        expected = [
            {
                'title': 'Sub-article (id=01) section title validation',
                'xpath': ".//sub-article[@article-type='translation']//front-stub//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['Article', 'Editorial', 'Letter'],
                'got_value': 'Article',
                'message': "Got Article expected one of ['Article', 'Editorial', 'Letter']",
                'advice': None
            },
            {
                'title': 'Article section title validation',
                'xpath': ".//article-meta//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['Artículo', 'Editorial', 'Carta'],
                'got_value': 'Artículo',
                'message': "Got Artículo expected one of ['Artículo', 'Editorial', 'Carta']",
                'advice': None
            }
        ]
        obtained = self.article_toc_sections.validate_article_toc_sections(expected_section)

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_toc_sections_fail_sections_not_obtained(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xml:lang="es">
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
                "es": ["Artículo", "Editorial", "Carta"],
                "en": ["Article", "Editorial", "Letter"]
            }
        expected = [
            {
                'title': 'Article or sub-article section title validation',
                'xpath': ".//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': ['Article', 'Editorial', 'Letter'],
                'got_value': None,
                'message': "Got None expected one of ['Article', 'Editorial', 'Letter']",
                'advice': 'Provide missing section for language: en'
            },
            {
                'title': 'Article or sub-article section title validation',
                'xpath': ".//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': ['Artículo', 'Editorial', 'Carta'],
                'got_value': None,
                'message': "Got None expected one of ['Artículo', 'Editorial', 'Carta']",
                'advice': 'Provide missing section for language: es'
            }
        ]
        obtained = self.article_toc_sections.validate_article_toc_sections(expected_section)

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_toc_sections_fail_section_obtained_not_in_expected(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
             <article xml:lang="es">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título del artículo</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>artículo</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="en">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>article</subject>
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
            "es": ["Artículo", "Editorial", "Carta"],
            "en": ["Article", "Editorial", "Letter"]
        }
        expected = [
            {
                'title': 'Sub-article (id=01) section title validation',
                'xpath': ".//sub-article[@article-type='translation']//front-stub//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': ['Article', 'Editorial', 'Letter'],
                'got_value': 'article',
                'message': "Got article expected one of ['Article', 'Editorial', 'Letter']",
                'advice': 'Provide missing section for language: en'
            },
            {
                'title': 'Article section title validation',
                'xpath': ".//article-meta//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': ['Artículo', 'Editorial', 'Carta'],
                'got_value': 'artículo',
                'message': "Got artículo expected one of ['Artículo', 'Editorial', 'Carta']",
                'advice': 'Provide missing section for language: es',
            }
        ]
        obtained = self.article_toc_sections.validate_article_toc_sections(expected_section)

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_toc_sections_fail_one_section_not_expected(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xml:lang="es">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título del artículo</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Artículo</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="en">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Article</subject>
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
            "en": ["Article", "Editorial", "Letter"]
        }
        expected = [
            {
                'title': 'Sub-article (id=01) section title validation',
                'xpath': ".//sub-article[@article-type='translation']//front-stub//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': ['Article', 'Editorial', 'Letter'],
                'got_value': 'Article',
                'message': "Got Article expected one of ['Article', 'Editorial', 'Letter']",
                'advice': None
            },
            {
                'title': 'Article or sub-article section title validation',
                'xpath': ".//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': None,
                'got_value': 'Artículo',
                'message': 'Got Artículo expected None',
                'advice': "Remove .//subj-group[@subj-group-type='heading']/subject for language: es",
            }
        ]
        obtained = self.article_toc_sections.validate_article_toc_sections(expected_section)

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_toc_sections_fail_all_sections_not_expected(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xml:lang="es">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Título del artículo</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Artículo</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="en">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Article</subject>
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
        expected_section = {}
        expected = [
            {
                'title': 'Article or sub-article section title validation',
                'xpath': ".//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': None,
                'got_value': 'Article',
                'message': 'Got Article expected None',
                'advice': "Remove .//subj-group[@subj-group-type='heading']/subject for language: en",
            },
            {
                'title': 'Article or sub-article section title validation',
                'xpath': ".//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': None,
                'got_value': 'Artículo',
                'message': 'Got Artículo expected None',
                'advice': "Remove .//subj-group[@subj-group-type='heading']/subject for language: es",
            }
        ]
        obtained = self.article_toc_sections.validate_article_toc_sections(expected_section)

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)

    def test_validate_article_toc_sections_fail_sections_not_obtained_and_not_expected(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xml:lang="es">
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
        expected_section = {}
        expected = [
            {
                'title': 'Article or sub-article section title validation',
                'xpath': ".//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': None,
                'got_value': None,
                'message': 'Got None expected None',
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
                        <article-title>Título del artículo</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Artículo</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="en">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Article</subject>
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
                'title': 'Article section title validation',
                'xpath': ".//article-meta//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': "'Título del artículo' (article title) different from 'Artículo' (section titles)",
                'got_value': "article title: 'Título del artículo', section titles: 'Artículo'",
                'message': 'article and section titles are different',
                'advice': None
            },
            {
                'title': 'Sub-article (id=01) section title validation',
                'xpath': ".//sub-article[@article-type='translation']//front-stub//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'match',
                'response': 'OK',
                'expected_value': "'Article title' (article title) different from 'Article' (section titles)",
                'got_value': "article title: 'Article title', section titles: 'Article'",
                'message': 'article and section titles are different',
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
                        <article-title>Artículo</article-title>
                    </title-group>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Artículo</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="en">
                <front-stub>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Article</subject>
                        </subj-group>
                    </article-categories>
                    <title-group>
                        <article-title>Article</article-title>
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
                'expected_value': "'Artículo' (article title) different from 'Artículo' (section titles)",
                'got_value': "article title: 'Artículo', section titles: 'Artículo'",
                'message': 'article and section titles are the same',
                'advice': "Provide different titles for article and section (subj-group[@subj-group-type='heading']/subject)",
            },
            {
                'title': 'Sub-article (id=01) section title validation',
                'xpath': ".//sub-article[@article-type='translation']//front-stub//subj-group[@subj-group-type='heading']/subject",
                'validation_type': 'match',
                'response': 'ERROR',
                'expected_value': "'Article' (article title) different from 'Article' (section titles)",
                'got_value': "article title: 'Article', section titles: 'Article'",
                'message': 'article and section titles are the same',
                'advice': "Provide different titles for article and section (subj-group[@subj-group-type='heading']/subject)",
            }
        ]
        obtained = self.article_toc_sections.validade_article_title_is_different_from_section_titles()

        for i, item in enumerate(obtained):
            with self.subTest(i):
                self.assertDictEqual(expected[i], item)
