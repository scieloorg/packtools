from unittest import TestCase
from lxml import etree

from packtools.sps.models.v2.article_xref import Xref, Id, Xrefs, Ids, ArticleXref


class XrefTest(TestCase):
    def setUp(self):
        self.xml_tree = etree.fromstring(
            """
            <article>
                <article-meta>
                    <p><xref ref-type="aff" rid="aff1">1</xref></p>
                    <aff id="aff1">
                        <p>affiliation</p>
                    </aff>
                </article-meta>
            </article>
            """
        )
        self.node = self.xml_tree.xpath(".//xref")[0]
        self.xref = Xref(self.node)

    def test_ref_type(self):
        self.assertEqual(self.xref.xref_type, "aff")

    def test_rid(self):
        self.assertEqual(self.xref.xref_rid, "aff1")

    def test_parent(self):
        self.assertEqual(self.xref.xref_parent, "p")

    def test_text(self):
        self.assertEqual(self.xref.xref_text, "1")

    def test_data(self):
        obtained = {"ref-type": "aff", "rid": "aff1", "text": "1", "parent-tag": "p"}
        self.assertDictEqual(self.xref.data, obtained)


class IdTest(TestCase):
    def setUp(self):
        self.xml_tree = etree.fromstring(
            """
            <article>
                <article-meta>
                    <p><xref ref-type="aff" rid="aff1">1</xref></p>
                    <aff id="aff1">
                        <p>affiliation</p>
                    </aff>
                </article-meta>
            </article>
            """
        )
        self.node = self.xml_tree.xpath(".//aff")[0]
        self.node_id = Id(self.node)

    def test_node_id(self):
        self.assertEqual(self.node_id.node_id, "aff1")

    def test_node_tag(self):
        self.assertEqual(self.node_id.node_tag, "aff")

    def test_data(self):
        obtained = {"tag": "aff", "id": "aff1"}
        self.assertDictEqual(self.node_id.data, obtained)


class XrefsTest(TestCase):
    def setUp(self):
        self.xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.1" specific-use="sps-1.9" article-type="research-article" xml:lang="en">
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
        self.xrefs = Xrefs(
            self.xml_tree.xpath(".")[0], "en", "research-article", "article", None
        )

    def test_xrefs(self):
        obtained = list(self.xrefs.xrefs())
        expected = [
            {
                "parent": "article",
                "parent-tag": "p",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "ref-type": "aff",
                "rid": "aff1",
                "text": "1",
            },
            {
                "parent": "article",
                "parent-tag": "p",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "ref-type": "fig",
                "rid": "fig1",
                "text": "1",
            },
            {
                "parent": "article",
                "parent-tag": "p",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "ref-type": "table",
                "rid": "table1",
                "text": "1",
            },
        ]
        self.assertEqual(len(obtained), 3)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


class IdsTest(TestCase):
    def setUp(self):
        self.xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.1" specific-use="sps-1.9" article-type="research-article" xml:lang="en">
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
        self.ids = Ids(
            self.xml_tree.xpath(".")[0], "en", "research-article", "article", None
        )

    def test_ids(self):
        obtained = list(self.ids.ids())
        expected = [
            {
                "id": "aff1",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "tag": "aff",
            },
            {
                "id": "fig1",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "tag": "fig",
            },
            {
                "id": "table1",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "tag": "table",
            },
        ]
        self.assertEqual(len(obtained), 3)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


class ArticleXrefTest(TestCase):
    def setUp(self):
        self.xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
                     dtd-version="1.1" specific-use="sps-1.9" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <p><xref ref-type="aff" rid="aff1">1</xref></p>
                        <aff id="aff1">
                            <p>affiliation</p>
                        </aff>
                    </article-meta>
                </front>
            
                <sub-article article-type="translation" xml:lang="es">
                    <front-stub>
                        <contrib-group>
                            <contrib contrib-type="author">
                                <name>
                                    <surname>García</surname>
                                    <given-names>Juan</given-names>
                                </name>
                                <xref ref-type="aff" rid="aff2">2</xref>
                            </contrib>
                        </contrib-group>
                        <aff id="aff2">
                            <institution>Universidad Ejemplo</institution>
                        </aff>
                    </front-stub>
                </sub-article>
            </article>

            """
        )
        self.article_xref = ArticleXref(self.xml_tree)

    def test_all_ids(self):
        obtained = list(self.article_xref.all_ids())
        expected = [
            {
                "id": "aff1",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "tag": "aff",
            },
            {
                "id": "aff2",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": None,
                "parent_lang": "es",
                "tag": "aff",
            },
        ]
        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_all_xref_rids(self):
        obtained = list(self.article_xref.all_xref_rids())
        expected = [
            {
                "parent": "article",
                "parent-tag": "p",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "ref-type": "aff",
                "rid": "aff1",
                "text": "1",
            },
            {
                "parent": "sub-article",
                "parent-tag": "contrib",
                "parent_article_type": "translation",
                "parent_id": None,
                "parent_lang": "es",
                "ref-type": "aff",
                "rid": "aff2",
                "text": "2",
            },
        ]
        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_article_ids(self):
        obtained = list(self.article_xref.article_ids())
        expected = [
            {
                "id": "aff1",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "tag": "aff",
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_article_xref_rids(self):
        obtained = list(self.article_xref.article_xref_rids())
        expected = [
            {
                "parent": "article",
                "parent-tag": "p",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "ref-type": "aff",
                "rid": "aff1",
                "text": "1",
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_sub_article_translation_ids(self):
        obtained = list(self.article_xref.sub_article_translation_ids())
        expected = [
            {
                "id": "aff2",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": None,
                "parent_lang": "es",
                "tag": "aff",
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_sub_article_translation_xref_rids(self):
        obtained = list(self.article_xref.sub_article_translation_xref_rids())
        expected = [
            {
                "parent": "sub-article",
                "parent-tag": "contrib",
                "parent_article_type": "translation",
                "parent_id": None,
                "parent_lang": "es",
                "ref-type": "aff",
                "rid": "aff2",
                "text": "2",
            }
        ]
        self.assertEqual(len(obtained), 1)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_sub_article_non_translation_ids(self):
        obtained = list(self.article_xref.sub_article_non_translation_ids())
        self.assertEqual(len(obtained), 0)

    def test_sub_article_non_translation_xref_rids(self):
        obtained = list(self.article_xref.sub_article_non_translation_xref_rids())
        self.assertEqual(len(obtained), 0)
