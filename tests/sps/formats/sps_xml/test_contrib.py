import unittest
import xml.etree.ElementTree as ET
from packtools.sps.formats.sps_xml.contrib import build_contrib_author  # Substitua 'your_module' pelo nome do seu arquivo


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

    def test_contrib_author_structure(self):
        # Gera o XML a partir dos dados válidos
        contrib_elem = build_contrib_author(self.valid_data)

        # Verifica se o elemento principal é <contrib> e se tem o atributo correto
        self.assertEqual(contrib_elem.tag, "contrib")
        self.assertEqual(contrib_elem.get("contrib-type"), "author")

        # Verifica os elementos <contrib-id> para ORCID e Scopus
        contrib_ids = contrib_elem.findall("contrib-id")
        self.assertEqual(len(contrib_ids), 2)
        self.assertEqual(contrib_ids[0].get("contrib-id-type"), "orcid")
        self.assertEqual(contrib_ids[0].text, "0000-0001-8528-2091")
        self.assertEqual(contrib_ids[1].get("contrib-id-type"), "scopus")
        self.assertEqual(contrib_ids[1].text, "24771926600")

        # Verifica os elementos <name>, <surname>, e <given-names>
        name_elem = contrib_elem.find("name")
        self.assertIsNotNone(name_elem)

        surname_elem = name_elem.find("surname")
        self.assertEqual(surname_elem.text, "Einstein")

        given_names_elem = name_elem.find("given-names")
        self.assertEqual(given_names_elem.text, "Albert")

        # Verifica o <xref> para afiliação
        xref_elem = contrib_elem.find("xref")
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

    def test_contrib_author_with_null_values(self):
        # Dados com valores nulos (None)
        null_data = {
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

        # Gera o XML a partir dos dados nulos
        contrib_elem = build_contrib_author(null_data)

        # Converte o elemento XML em uma string
        generated_xml_str = ET.tostring(contrib_elem, encoding="unicode", method="xml")

        # String XML esperada para dados nulos
        expected_xml_str = (
            '<contrib contrib-type="author">'
            '<name>'
            '<surname />'
            '<given-names />'
            '</name>'
            '</contrib>'
        )

        # Verifica se o XML gerado corresponde à string esperada
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


if __name__ == '__main__':
    unittest.main()
