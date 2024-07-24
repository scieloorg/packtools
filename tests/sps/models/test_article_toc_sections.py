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
                            <subj-group subj-group-type="sub-heading">
                                <subject>Public Health</subject>
                            </subj-group>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="01" xml:lang="pt">
                <front-stub>
                    <subj-group subj-group-type="heading">
                        <subject>Ciências da Saúde</subject>
                        <subj-group subj-group-type="sub-heading">
                            <subject>Saúde Pública</subject>
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
                'text': 'Health Sciences'
            },
            {
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'text': 'Ciências da Saúde'
            },
        ]
        obtained = list(self.article_toc_sections.sections)

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
        self.article_toc_sections = ArticleTocSections(self.xmltree)

        expected = {
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
        }

        obtained = self.article_toc_sections.sections_dict

        self.assertDictEqual(obtained, expected)

    def test_sub_sections(self):
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
        self.article_toc_sections = ArticleTocSections(self.xmltree)

        expected = [
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'text': 'Public Health'
            }
        ]
        obtained = list(self.article_toc_sections.sub_sections)

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_sub_sections_dict(self):
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
        self.article_toc_sections = ArticleTocSections(self.xmltree)

        expected = {
            'en': {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'text': 'Public Health'
            },
            'pt': {
                'parent': 'sub-article',
                'parent_article_type': 'translation',
                'parent_id': '01',
                'parent_lang': 'pt',
                'text': 'Saúde Pública'
            }
        }
        obtained = self.article_toc_sections.sub_sections_dict

        self.assertDictEqual(obtained, expected)
