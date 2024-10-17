import unittest
import xml.etree.ElementTree as ET
from packtools.sps.formats.sps_xml.contrib import build_contrib_author


class TestBuildContribAuthor(unittest.TestCase):

    def setUp(self):
        # Dados de exemplo para o teste com valores válidos
        self.valid_data = {
            "contrib_type": "author",
            "contrib_ids": {
                "orcid": "0000-0001-8528-2091",
                "scopus": "24771926600"
            },
            "surname": "Einstein",
            "given_names": "Albert",
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
        self.assertEqual(surname_elem.text, "Einstein")
        self.assertEqual(given_names_elem.text, "Albert")

    def test_contrib_author_affiliations(self):
        xref_elems = self.contrib_elem.findall("xref")
        self.assertEqual(len(xref_elems), 1)
        xref_elem = xref_elems[0]
        self.assertEqual(xref_elem.get("ref-type"), "aff")
        self.assertEqual(xref_elem.get("rid"), "aff1")
        self.assertEqual(xref_elem.text, "1")

    def test_contrib_author_as_string(self):
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
            '</name>'
            '<xref ref-type="aff" rid="aff1">1</xref>'
            '</contrib>'
        )

        # Comparar o XML gerado com a string esperada
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildContribAuthorNoneValues(unittest.TestCase):

    def setUp(self):
        # Dados de exemplo para o teste com valores nulos
        self.valid_data = {
            "contrib_type": None,
            "contrib_ids": {
                "orcid": None,
                "scopus": None
            },
            "surname": None,
            "given_names": None,
            "affiliations": [
                {"rid": None, "text": None}
            ]
        }

    def _build_and_compare(self, expected_xml_str):
        """Método auxiliar para construção e comparação do XML gerado"""
        contrib_elem = build_contrib_author(self.valid_data)
        generated_xml_str = ET.tostring(contrib_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_contrib_author_with_all_null_values(self):
        expected_xml_str = (
            '<contrib contrib-type="">'
            '<contrib-id contrib-id-type="orcid" />'
            '<contrib-id contrib-id-type="scopus" />'
            '<name>'
            '<surname />'
            '<given-names />'
            '</name>'
            '</contrib>'
        )
        self._build_and_compare(expected_xml_str)

    def test_contrib_author_without_contrib_id(self):
        self.valid_data.pop("contrib_ids")
        expected_xml_str = (
            '<contrib contrib-type="">'
            '<name>'
            '<surname />'
            '<given-names />'
            '</name>'
            '</contrib>'
        )
        self._build_and_compare(expected_xml_str)

    def test_contrib_author_without_contrib_id_type(self):
        self.valid_data["contrib_ids"].pop("orcid")
        expected_xml_str = (
            '<contrib contrib-type="">'
            '<contrib-id contrib-id-type="scopus" />'
            '<name>'
            '<surname />'
            '<given-names />'
            '</name>'
            '</contrib>'
        )
        self._build_and_compare(expected_xml_str)

    def test_contrib_author_without_contrib_ids(self):
        self.valid_data.pop("contrib_ids")
        expected_xml_str = (
            '<contrib contrib-type="">'
            '<name>'
            '<surname />'
            '<given-names />'
            '</name>'
            '</contrib>'
        )
        self._build_and_compare(expected_xml_str)

    def test_contrib_author_without_surname(self):
        self.valid_data.pop("surname")
        expected_xml_str = (
            '<contrib contrib-type="">'
            '<contrib-id contrib-id-type="orcid" />'
            '<contrib-id contrib-id-type="scopus" />'
            '<name>'
            '<given-names />'
            '</name>'
            '</contrib>'
        )
        self._build_and_compare(expected_xml_str)


if __name__ == '__main__':
    unittest.main()
