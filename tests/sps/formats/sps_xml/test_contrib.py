import unittest
import xml.etree.ElementTree as ET
from packtools.sps.formats.sps_xml.contrib import build_contrib_author


class TestBuildContribAuthor(unittest.TestCase):

    def setUp(self):
        # Dados de exemplo para o teste com valores válidos
        self.valid_data = {
            "contrib_type": "author",
            "orcid": "0000-0001-8528-2091",
            "scopus": "24771926600",
            "prefix": "Prof.",
            "surname": "Einstein",
            "given_names": "Albert",
            "suffix": "Neto",
            "affiliations": [
                {"rid": "aff1", "text": "1"}
            ]
        }
        self.contrib_elem = build_contrib_author(self.valid_data)

    def test_contrib_author_contrib_type(self):
        # Combinação de verificação da estrutura e do valor de contrib-type
        contrib_type = self.contrib_elem.get("contrib-type")
        self.assertIsNotNone(contrib_type)
        self.assertEqual(contrib_type, "author")

    def test_contrib_author_ids(self):
        contrib_ids = self.contrib_elem.findall("contrib-id")
        self.assertEqual(len(contrib_ids), 2)
        self.assertEqual(contrib_ids[0].get("contrib-id-type"), "orcid")
        self.assertEqual(contrib_ids[0].text, "0000-0001-8528-2091")
        self.assertEqual(contrib_ids[1].get("contrib-id-type"), "scopus")
        self.assertEqual(contrib_ids[1].text, "24771926600")

    def test_contrib_author_name(self):
        name_elem = self.contrib_elem.find("name")
        self.assertIsNotNone(name_elem)
        surname_elem = name_elem.find("surname")
        given_names_elem = name_elem.find("given-names")
        prefix_elem = name_elem.find("prefix")
        suffix_elem = name_elem.find("suffix")
        self.assertEqual(surname_elem.text, "Einstein")
        self.assertEqual(given_names_elem.text, "Albert")
        self.assertEqual(prefix_elem.text, "Prof.")
        self.assertEqual(suffix_elem.text, "Neto")

    def test_contrib_author_affiliations(self):
        xref_elems = self.contrib_elem.findall("xref")
        self.assertEqual(len(xref_elems), 1)
        xref_elem = xref_elems[0]
        self.assertEqual(xref_elem.get("ref-type"), "aff")
        self.assertEqual(xref_elem.get("rid"), "aff1")
        self.assertEqual(xref_elem.text, "1")

    def test_contrib_author_collab(self):
        data = {
            "contrib_type": "author",
            "collab": "The Brazil Flora Group"
        }
        contrib_elem = build_contrib_author(data)
        self.assertEqual(len(contrib_elem), 1)
        self.assertEqual(contrib_elem.get("contrib-type"), "author")
        self.assertEqual(contrib_elem.find("collab").text, "The Brazil Flora Group")

    def test_contrib_author_as_string(self):
        self.maxDiff = None
        # Gera o XML a partir dos dados válidos
        contrib_elem = build_contrib_author(self.valid_data)

        # Converte o elemento XML em uma string
        generated_xml_str = ET.tostring(contrib_elem, encoding="unicode", method="xml")

        # String XML esperada
        expected_xml_str = (
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0001-8528-2091</contrib-id>'
            '<contrib-id contrib-id-type="scopus">24771926600</contrib-id>'
            '<name>'
            '<surname>Einstein</surname>'
            '<given-names>Albert</given-names>'
            '<prefix>Prof.</prefix>'
            '<suffix>Neto</suffix>'
            '</name>'
            '<xref ref-type="aff" rid="aff1">1</xref>'
            '</contrib>'
        )

        # Comparar o XML gerado com a string esperada
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildContribAuthorNoneValues(unittest.TestCase):
    """
        {
            "contrib_type": None,
            "orcid": None,
            "scopus": None,
            "surname": None,
            "given_names": None,
            "affiliations": [
                {"rid": None, "text": None}
            ]
        }
    """

    def test_contrib_author_contrib_type_None(self):
        data = {
            "contrib_type": None
        }

        with self.assertRaises(NameError) as e:
            build_contrib_author(data)

        self.assertEqual(str(e.exception), "contrib-type is required")

    def test_contrib_author_contrib_ids_None(self):
        data = {
            "contrib_type": "author",
            "scopus": None
        }
        expected_xml_str = (
            '<contrib contrib-type="author" />'
        )
        contrib_elem = build_contrib_author(data)
        generated_xml_str = ET.tostring(contrib_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_contrib_author_contrib_surname_None(self):
        # vale para os demais elementos em <name>
        data = {
            "contrib_type": "author",
            "surname": None,
        }
        expected_xml_str = (
            '<contrib contrib-type="author" />'
        )
        contrib_elem = build_contrib_author(data)
        generated_xml_str = ET.tostring(contrib_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_contrib_author_contrib_affiliations_None(self):
        data = {
            "contrib_type": "author",
            "affiliations": None,
        }
        expected_xml_str = (
            '<contrib contrib-type="author" />'
        )
        contrib_elem = build_contrib_author(data)
        generated_xml_str = ET.tostring(contrib_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


if __name__ == '__main__':
    unittest.main()
