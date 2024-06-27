from unittest import TestCase
from lxml import etree

from packtools.sps.models.article_xref import ArticleXref
from packtools.sps.utils import xml_utils


class ArticleXrefTest(TestCase):
    def test_all_ids(self):
        self.xmltree = etree.fromstring(
            """
            <article>
                <article-meta>
                    <p><xref ref-type="aff" rid="aff1">1</xref></p>     
                    <aff id="aff1">
                        <p>affiliation</p>
                    </aff>

                    <p><xref ref-type="fig" rid="fig1">1</xref></p>     
                    <fig id="fig1">
                        <p>figure</p>
                    </fig>

                    <p><xref ref-type="table" rid="table1">1</xref></p>     
                    <table id="table1">
                        <p>table</p>
                    </table>
                </article-meta>
            </article>
            """
        )
        self.article_xref = ArticleXref(self.xmltree)
        expected = {'aff1', 'fig1', 'table1'}
        obtained = self.article_xref.all_ids
        self.assertEqual(expected, obtained)

    def test_all_xref_rids(self):
        self.xmltree = etree.fromstring(
            """
            <article>
                <article-meta>
                    <p><xref ref-type="aff" rid="aff1">1</xref></p>     
                    <aff id="aff1">
                        <p>affiliation</p>
                    </aff>

                    <p><xref ref-type="fig" rid="fig1">1</xref></p>     
                    <fig id="fig1">
                        <p>figure</p>
                    </fig>

                    <p><xref ref-type="table" rid="table1">1</xref></p>     
                    <table id="table1">
                        <p>table</p>
                    </table>
                </article-meta>
            </article>
            """
        )
        self.article_xref = ArticleXref(self.xmltree)
        expected = {'aff1', 'fig1', 'table1'}
        obtained = self.article_xref.all_xref_rids
        self.assertEqual(expected, obtained)

    def test_data(self):
        self.maxDiff = None
        xmltree = xml_utils.get_xml_tree('tests/samples/0034-8910-rsp-48-2-0296.xml')
        self.article_xref = ArticleXref(xmltree)
        expected = [
            {
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'en',
                'ids': [
                    ('aff', 'aff1'),
                    ('aff', 'aff2'),
                    ('aff', 'aff3'),
                    ('aff', 'aff4'),
                    ('aff', 'aff5')
                ],
                'rids': ['aff1', 'aff2', 'aff3', 'aff4', 'aff5']
            }
        ]
        obtained = list(self.article_xref.data())
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])
