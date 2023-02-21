from unittest import TestCase

from lxml import etree

from packtools.sps.models.article_toc_sections import ArticleTocSections


class ArticleTocSectionsTest(TestCase):
    def setUp(self):
        xml = ("""
        <article xml:lang="es">
        <front>
            <article-meta>
                <article-categories>
                    <subj-group subj-group-type="heading">
                    <subject>Scientific Communication</subject>
                        <subj-group>
                        <subject>Food Safety</subject>
                        </subj-group>
                    </subj-group>
                </article-categories>
            </article-meta>
        </front>
        </article>
        """)
        xmltree = etree.fromstring(xml)
        self.article_toc_sections = ArticleTocSections(xmltree)

    def test_subj_group_type(self):
        expected = 'Scientific Communication'
        self.assertEqual(expected, self.article_toc_sections.subj_group_type)

    def test_subj_group(self):
        expected = 'Food Safety'
        self.assertEqual(expected, self.article_toc_sections.subj_group)
