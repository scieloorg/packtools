import unittest
from lxml import etree as ET
from packtools.sps.formats.sps_xml.ref import build_ref


class TestBuildRefAttribsRequired(unittest.TestCase):
    def test_build_ref_attribs_required(self):
        data = {
            "ref-id": "B1",
            "publication-type": "journal",
        }
        expected_xml_str = (
            '<ref id="B1">'
            '<element-citation publication-type="journal"/>'
            '</ref>'
        )
        ref_elem = build_ref(data)
        generated_xml_str = ET.tostring(ref_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_ref_id_None(self):
        data = {
            "ref-id": None,
            "publication-type": "journal",
        }

        with self.assertRaises(ValueError) as e:
            build_ref(data)
        self.assertEqual(str(e.exception), "attribute ref-id is required")

    def test_build_ref_publication_type_None(self):
        data = {
            "ref-id": "B1",
            "publication-type": None
        }

        with self.assertRaises(ValueError) as e:
            build_ref(data)
        self.assertEqual(str(e.exception), "attribute publication-type is required")


class TestBuildRefSubElements(unittest.TestCase):
    def test_build_ref_sub_elements(self):
        data = {
            "ref-id": "B1",
            "label": "1",
            "mixed-citation": "Aires M, Paz AA, Perosa CT. Situação de saúde...",
            "publication-type": "journal",
            "article-title": "Situação de saúde e grau de...",
            "source": "Rev Gaucha Enferm",
            "publisher-loc": "Rio de Janeiro",
            "year": "2009",
            "volume": "30",
            "issue": "3",
            "fpage": "192",
            "lpage": "199"
        }
        expected_xml_str = (
            '<ref id="B1">'
            '<label>1</label>'
            '<mixed-citation>Aires M, Paz AA, Perosa CT. Situação de saúde...</mixed-citation>'
            '<element-citation publication-type="journal">'
            '<article-title>Situação de saúde e grau de...</article-title>'
            '<source>Rev Gaucha Enferm</source>'
            '<publisher-loc>Rio de Janeiro</publisher-loc>'
            '<year>2009</year>'
            '<volume>30</volume>'
            '<issue>3</issue>'
            '<fpage>192</fpage>'
            '<lpage>199</lpage>'
            '</element-citation>'
            '</ref>'
        )
        ref_elem = build_ref(data)
        generated_xml_str = ET.tostring(ref_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_ref_sub_elements_None(self):
        data = {
            "ref-id": "B1",
            "publication-type": "journal",
            "label": None,
            "mixed-citation": None,
            "article-title": None,
            "source": None
        }
        expected_xml_str = (
            '<ref id="B1">'
            '<element-citation publication-type="journal"/>'
            '</ref>'
        )
        ref_elem = build_ref(data)
        generated_xml_str = ET.tostring(ref_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildRefExtLink(unittest.TestCase):
    def test_build_ref_ext_link(self):
        self.maxDiff = None
        data = {
            "ref-id": "B1",
            "publication-type": "journal",
            "ext-link": [
                {
                    "ext-link-type": "uri",
                    "xlink:href": "http://socialsciences.scielo.org",
                    "text": "http://socialsciences.scielo.org"
                }
            ]
        }
        expected_xml_str = (
            '<ref id="B1">'
            '<element-citation publication-type="journal">'
            '<ext-link xmlns:ns0="http://www.w3.org/1999/xlink" '
            'ext-link-type="uri" ns0:href="http://socialsciences.scielo.org">'
            'http://socialsciences.scielo.org</ext-link>'
            '</element-citation>'
            '</ref>'
        )
        ref_elem = build_ref(data)
        generated_xml_str = ET.tostring(ref_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_ref_ext_link_None(self):
        data = {
            "ref-id": "B1",
            "publication-type": "journal",
            "ext-link": None
        }
        expected_xml_str = (
            '<ref id="B1">'
            '<element-citation publication-type="journal"/>'
            '</ref>'
        )
        ref_elem = build_ref(data)
        generated_xml_str = ET.tostring(ref_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_ref_ext_link_attribs_None(self):
        data = {
            "ref-id": "B1",
            "publication-type": "journal",
            "ext-link": [
                {
                    "ext-link-type": None,
                    "xlink:href": None,
                    "text": "http://socialsciences.scielo.org"
                }
            ]
        }
        with self.assertRaises(ValueError) as e:
            build_ref(data)
        self.assertEqual(str(e.exception), "ext-link-type and xlink:href are required")

    def test_build_ref_ext_link_text_None(self):
        data = {
            "ref-id": "B1",
            "publication-type": "journal",
            "ext-link": [
                {
                    "ext-link-type": "uri",
                    "xlink:href": "http://socialsciences.scielo.org",
                    "text": None
                }
            ]
        }
        expected_xml_str = (
            '<ref id="B1">'
            '<element-citation publication-type="journal"/>'
            '</ref>'
        )
        ref_elem = build_ref(data)
        generated_xml_str = ET.tostring(ref_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_ref_ext_link_in_comment(self):
        self.maxDiff = None
        data = {
            "ref-id": "B1",
            "publication-type": "journal",
            "ext-link": [
                {
                    "ext-link-type": "uri",
                    "xlink:href": "http://socialsciences.scielo.org",
                    "text": "http://socialsciences.scielo.org",
                    "comment": "Disponível em: "
                }
            ]
        }
        expected_xml_str = (
            '<ref id="B1">'
            '<element-citation publication-type="journal">'
            '<comment>Disponível em: <ext-link xmlns:ns0="http://www.w3.org/1999/xlink" '
            'ext-link-type="uri" ns0:href="http://socialsciences.scielo.org">'
            'http://socialsciences.scielo.org</ext-link></comment>'
            '</element-citation>'
            '</ref>'
        )
        ref_elem = build_ref(data)
        generated_xml_str = ET.tostring(ref_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildRefPubId(unittest.TestCase):
    def test_build_ref_pub_id(self):
        data = {
            "ref-id": "B1",
            "publication-type": "journal",
            "pub-ids": [
                {
                    "pub-id-type": "pmid",
                    "text": "15867408"
                }
            ]
        }
        expected_xml_str = (
            '<ref id="B1">'
            '<element-citation publication-type="journal">'
            '<pub-id pub-id-type="pmid">15867408</pub-id>'
            '</element-citation>'
            '</ref>'
        )
        ref_elem = build_ref(data)
        generated_xml_str = ET.tostring(ref_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_ref_pub_id_None(self):
        data = {
            "ref-id": "B1",
            "publication-type": "journal",
            "pub-ids": None
        }
        expected_xml_str = (
            '<ref id="B1">'
            '<element-citation publication-type="journal"/>'
            '</ref>'
        )
        ref_elem = build_ref(data)
        generated_xml_str = ET.tostring(ref_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_ref_pub_id_attribs_None(self):
        data = {
            "ref-id": "B1",
            "publication-type": "journal",
            "pub-ids": [
                {
                    "pub-id-type": None,
                    "text": "15867408"
                }
            ]
        }
        with self.assertRaises(ValueError) as e:
            build_ref(data)
        self.assertEqual(str(e.exception), "pub-id-type is required")

    def test_build_ref_ext_link_text_None(self):
        data = {
            "ref-id": "B1",
            "publication-type": "journal",
            "pub-ids": [
                {
                    "pub-id-type": "pmid",
                    "text": None
                }
            ]
        }
        expected_xml_str = (
            '<ref id="B1">'
            '<element-citation publication-type="journal"/>'
            '</ref>'
        )
        ref_elem = build_ref(data)
        generated_xml_str = ET.tostring(ref_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildDateInCitation(unittest.TestCase):
    def test_build_ref_date_in_citation(self):
        data = {
            "ref-id": "B1",
            "publication-type": "journal",
            "dates-in-citation": [
                {
                    "content-type": "updated",
                    "text": "2006 Jul 20"
                }
            ]
        }
        expected_xml_str = (
            '<ref id="B1">'
            '<element-citation publication-type="journal">'
            '<date-in-citation content-type="updated">2006 Jul 20</date-in-citation>'
            '</element-citation>'
            '</ref>'
        )
        ref_elem = build_ref(data)
        generated_xml_str = ET.tostring(ref_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_ref_date_in_citation_None(self):
        data = {
            "ref-id": "B1",
            "publication-type": "journal",
            "dates-in-citation": None
        }
        expected_xml_str = (
            '<ref id="B1">'
            '<element-citation publication-type="journal"/>'
            '</ref>'
        )
        ref_elem = build_ref(data)
        generated_xml_str = ET.tostring(ref_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_ref_date_in_citation_attribs_None(self):
        data = {
            "ref-id": "B1",
            "publication-type": "journal",
            "dates-in-citation": [
                {
                    "content-type": None,
                    "text": "2006 Jul 20"
                }
            ]
        }
        with self.assertRaises(ValueError) as e:
            build_ref(data)
        self.assertEqual(str(e.exception), "content-type is required")

    def test_build_ref_date_in_citation_text_None(self):
        data = {
            "ref-id": "B1",
            "publication-type": "journal",
            "dates-in-citation": [
                {
                    "content-type": "updated",
                    "text": None
                }
            ]
        }
        expected_xml_str = (
            '<ref id="B1">'
            '<element-citation publication-type="journal"/>'
            '</ref>'
        )
        ref_elem = build_ref(data)
        generated_xml_str = ET.tostring(ref_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildRefPersonGroup(unittest.TestCase):
    def test_build_ref_person_group(self):
        data = {
            "ref-id": "B1",
            "publication-type": "journal",
        }
        node = {
           "person-group": [
               ET.fromstring(
                   '<person-group person-group-type="author">'
                   '<name>'
                   '<surname>Einstein</surname>'
                   '<given-names>Albert</given-names>'
                   '<prefix>Prof.</prefix>'
                   '<suffix>Neto</suffix>'
                   '</name>'
                   '</person-group>'
               )
           ]
        }
        expected_xml_str = (
            '<ref id="B1">'
            '<element-citation publication-type="journal">'
            '<person-group person-group-type="author">'
            '<name>'
            '<surname>Einstein</surname>'
            '<given-names>Albert</given-names>'
            '<prefix>Prof.</prefix>'
            '<suffix>Neto</suffix>'
            '</name>'
            '</person-group>'
            '</element-citation>'
            '</ref>'
        )
        ref_elem = build_ref(data, node)
        generated_xml_str = ET.tostring(ref_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())
