from unittest import TestCase, skip
from lxml import etree

from packtools.sps.models.v2.article_xref import Xref, Id, Ids, ArticleXref


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

    def test_text(self):
        self.assertEqual(self.xref.xref_text, "1")

    @skip("Teste pendente de correção e/ou ajuste")
    def test_data(self):
        obtained = {"ref-type": "aff", "rid": "aff1", "text": "1"}
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

    def test_str_main_tag(self):
        self.assertEqual(
            self.node_id.str_main_tag,
            '<aff id="aff1">'
        )

    def test_str(self):
        self.assertEqual(
            str(self.node_id),
            """<?xml version='1.0' encoding='utf-8'?>
<aff id="aff1">
                        <p>affiliation</p>
                    </aff>
                """
        )

    def test_xml_1(self):
        self.maxDiff = None
        result = self.node_id.xml(doctype=None, pretty_print=True, xml_declaration=True)
        expected = """<?xml version='1.0' encoding='utf-8'?>
<aff id="aff1">
                        <p>affiliation</p>
                    </aff>
                
"""
        self.assertEqual(result, expected)

    def test_xml_2(self):
        self.maxDiff = None
        result = self.node_id.xml(doctype=None, pretty_print=True, xml_declaration=None)
        expected = """<aff id="aff1">
                        <p>affiliation</p>
                    </aff>
                
"""
        self.assertEqual(result, expected)

    def test_xml_3(self):
        self.maxDiff = None
        result = self.node_id.xml(doctype=None, pretty_print=None, xml_declaration=None)
        expected = """<aff id="aff1">
                        <p>affiliation</p>
                    </aff>"""
        self.assertEqual(result.strip(), expected)


class IdsTest(TestCase):
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
                        
                        <aff id="aff2">
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
                </front>
            </article>
            """
        )
        self.ids = Ids(self.xml_tree)

    def test_ids(self):
        obtained = list(self.ids.ids(element_name="aff"))
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
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "tag": "aff",
            }
        ]
        self.assertEqual(len(obtained), 2)
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
                        <aff id="aff2">
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
                        <aff id="aff3">
                            <institution>Universidad Ejemplo</institution>
                        </aff>
                        <aff id="aff4">
                            <institution>Universidad Ejemplo</institution>
                        </aff>
                    </front-stub>
                </sub-article>
            </article>

            """
        )
        self.article_xref = ArticleXref(self.xml_tree)

    def test_all_ids(self):
        obtained = self.article_xref.all_ids(element_name="aff")
        expected = {
            "aff1": [
                {
                    "id": "aff1",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "tag": "aff",
                }
            ],
            "aff2": [
                {
                    "id": "aff2",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "en",
                    "tag": "aff",
                }
            ],
            "aff3": [
                {
                    "id": "aff3",
                    "parent": "sub-article",
                    "parent_article_type": "translation",
                    "parent_id": None,
                    "parent_lang": "es",
                    "tag": "aff",
                }
            ],
            "aff4": [
                {
                    "id": "aff4",
                    "parent": "sub-article",
                    "parent_article_type": "translation",
                    "parent_id": None,
                    "parent_lang": "es",
                    "tag": "aff",
                }
            ]
        }
        self.assertEqual(len(obtained), 4)
        for id, item in expected.items():
            for i, subitem in enumerate(item):
                with self.subTest(id):
                    self.assertDictEqual(subitem, obtained[id][i])

    @skip("Teste pendente de correção e/ou ajuste")
    def test_all_xref_rids(self):
        obtained = self.article_xref.all_xref_rids()
        expected = {
            "aff1": [
                {
                    "ref-type": "aff",
                    "rid": "aff1",
                    "text": "1",
                }
            ],
            "aff2": [
                {
                    "ref-type": "aff",
                    "rid": "aff2",
                    "text": "2",
                }
            ]
        }
        self.assertEqual(len(obtained), 2)
        for rid, item in expected.items():
            for i, subitem in enumerate(item):
                with self.subTest(rid):
                    self.assertDictEqual(subitem, obtained[rid][i])

    def test_article_ids(self):
        obtained = list(self.article_xref.article_ids(element_name="aff"))
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
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "tag": "aff",
            }
        ]
        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_sub_article_translation_ids(self):
        obtained = list(self.article_xref.sub_article_translation_ids(element_name="aff"))
        expected = [
            {
                "id": "aff3",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": None,
                "parent_lang": "es",
                "tag": "aff",
            },
            {
                "id": "aff4",
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": None,
                "parent_lang": "es",
                "tag": "aff",
            }
        ]
        self.assertEqual(len(obtained), 2)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])

    def test_sub_article_non_translation_ids(self):
        obtained = list(self.article_xref.sub_article_non_translation_ids(element_name="aff"))
        self.assertEqual(len(obtained), 0)
