from unittest import TestCase, skip
from lxml import etree

from packtools.sps.models.v2.article_xref import Xref, Element, XMLCrossReference


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

    def test_data(self):
        obtained = {
            'content': '1',
            'elem_name': 'aff',
            'elem_xml': '<aff id="aff1">',
            'ref-type': 'aff',
            'rid': 'aff1',
            'tag_and_attribs': '<xref ref-type="aff" rid="aff1">',
            'text': '1'
        }
        self.assertDictEqual(self.xref.data, obtained)


class ElementTest(TestCase):
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
        self.elem = Element(self.node)

    def test_node_id(self):
        self.assertEqual(self.elem.node_id, "aff1")

    def test_node_tag(self):
        self.assertEqual(self.elem.node_tag, "aff")

    def test_data(self):
        obtained = {
            'id': 'aff1',
            'tag': 'aff',
            'tag_and_attribs': '<aff id="aff1">',
            'tag_id': '<aff id="aff1">',
            'xref_xml': '<xref ref-type="aff" rid="aff1">'
        }
        self.assertDictEqual(self.elem.data, obtained)

    def test_str_tag_and_attribs(self):
        self.assertEqual(self.elem.tag_and_attribs, '<aff id="aff1">')

    def test_str(self):
        result = str(self.elem)
        self.assertIn('<aff id="aff1">', result)
        self.assertIn('<p>affiliation</p>', result)

    def test_xml_with_declaration(self):
        result = self.elem.xml(doctype=None, pretty_print=True, xml_declaration=True)
        self.assertIn('<?xml version=', result)

    def test_xml_no_declaration(self):
        result = self.elem.xml(doctype=None, pretty_print=True, xml_declaration=False)
        self.assertIn('<aff id="aff1">', result)


class XMLCrossReferenceTest(TestCase):
    def setUp(self):
        self.xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
                     dtd-version="1.1" specific-use="sps-1.9" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <p><xref ref-type="aff" rid="aff1">1</xref></p>
                        <aff id="aff1"><p>affiliation</p></aff>
                        <aff id="aff2"><p>affiliation</p></aff>
                        <p><xref ref-type="fig" rid="fig1">2</xref></p>
                        <fig id="fig1"><p>figure</p></fig>
                        <p><xref ref-type="table" rid="table1">3</xref></p>
                        <table id="table1"><p>table</p></table>
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
                        <aff id="aff3"><institution>Universidad Ejemplo</institution></aff>
                        <aff id="aff4"><institution>Universidad Ejemplo</institution></aff>
                    </front-stub>
                </sub-article>
            </article>
            """
        )
        self.xref = XMLCrossReference(self.xml_tree)

    def test_elems_by_id(self):
        results = self.xref.elems_by_id(element_name="aff")
        self.assertEqual(len(results), 4)
        self.assertIn("aff1", results)
        self.assertIn("aff2", results)
        self.assertIn("aff3", results)
        self.assertIn("aff4", results)

    def test_xrefs_by_rid(self):
        results = self.xref.xrefs_by_rid()
        self.assertEqual(len(results), 4)
        self.assertIn("aff1", results)
        self.assertIn("aff2", results)
        self.assertIn("fig1", results)
        self.assertIn("table1", results)
        self.assertEqual(results["aff1"][0]["ref-type"], "aff")
        self.assertEqual(results["fig1"][0]["ref-type"], "fig")
