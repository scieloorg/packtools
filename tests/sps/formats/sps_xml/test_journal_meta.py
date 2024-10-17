import unittest
import xml.etree.ElementTree as ET
from packtools.sps.formats.sps_xml.journal_meta import build_journal_meta


class TestBuildJournalMeta(unittest.TestCase):

    def setUp(self):
        # Dados de exemplo para uso em testes
        self.data = {
            "journal_ids": {
                "nlm-ta": "Braz J Med Biol Res",
                "publisher-id": "bjmbr"
            },
            "journal_title": "Brazilian Journal of Medical and Biological Research",
            "abbrev_journal_title": "Braz. J. Med. Biol. Res.",
            "issn": {
                "epub": "1414-431X",
                "ppub": "0100-879X"
            },
            "publisher_name": "Associação Brasileira de Divulgação Científica"
        }
        self.journal_meta_elem = build_journal_meta(self.data)

    def test_journal_meta_structure(self):
        # Verifica se o elemento principal é <journal-meta>
        self.assertEqual(self.journal_meta_elem.tag, "journal-meta")

    def test_journal_meta_journal_ids(self):
        journal_ids = self.journal_meta_elem.findall("journal-id")
        self.assertEqual(len(journal_ids), 2)
        self.assertEqual(journal_ids[0].get("journal-id-type"), "nlm-ta")
        self.assertEqual(journal_ids[0].text, "Braz J Med Biol Res")
        self.assertEqual(journal_ids[1].get("journal-id-type"), "publisher-id")
        self.assertEqual(journal_ids[1].text, "bjmbr")

    def test_journal_meta_titles(self):
        journal_title_group = self.journal_meta_elem.find("journal-title-group")
        self.assertIsNotNone(journal_title_group)

        journal_title = journal_title_group.find("journal-title")
        self.assertEqual(journal_title.text, "Brazilian Journal of Medical and Biological Research")

        abbrev_title = journal_title_group.find("abbrev-journal-title")
        self.assertEqual(abbrev_title.text, "Braz. J. Med. Biol. Res.")
        self.assertEqual(abbrev_title.get("abbrev-type"), "publisher")

    def test_journal_meta_issn(self):
        issns = self.journal_meta_elem.findall("issn")
        self.assertEqual(len(issns), 2)
        self.assertEqual(issns[0].get("pub-type"), "epub")
        self.assertEqual(issns[0].text, "1414-431X")
        self.assertEqual(issns[1].get("pub-type"), "ppub")
        self.assertEqual(issns[1].text, "0100-879X")

    def test_journal_meta_publisher(self):
        publisher = self.journal_meta_elem.find("publisher")
        self.assertIsNotNone(publisher)

        publisher_name = publisher.find("publisher-name")
        self.assertEqual(publisher_name.text, "Associação Brasileira de Divulgação Científica")

    def test_journal_meta_as_string(self):
        # Gera o XML a partir dos dados válidos
        generated_xml_str = ET.tostring(self.journal_meta_elem, encoding="unicode", method="xml")

        # String XML esperada
        expected_xml_str = (
            '<journal-meta>'
            '<journal-id journal-id-type="nlm-ta">Braz J Med Biol Res</journal-id>'
            '<journal-id journal-id-type="publisher-id">bjmbr</journal-id>'
            '<journal-title-group>'
            '<journal-title>Brazilian Journal of Medical and Biological Research</journal-title>'
            '<abbrev-journal-title abbrev-type="publisher">Braz. J. Med. Biol. Res.</abbrev-journal-title>'
            '</journal-title-group>'
            '<issn pub-type="epub">1414-431X</issn>'
            '<issn pub-type="ppub">0100-879X</issn>'
            '<publisher>'
            '<publisher-name>Associação Brasileira de Divulgação Científica</publisher-name>'
            '</publisher>'
            '</journal-meta>'
        )

        # Comparar o XML gerado com a string esperada
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildJournalMetaNoneValues(unittest.TestCase):

    def setUp(self):
        self.empty_data = {
            "journal_ids": {
                "nlm-ta": None,
            },
            "journal_title": "",
            "abbrev_journal_title": "",
            "issn": {},
            "publisher_name": ""
        }

    def _build_and_compare(self, expected_xml_str):
        """Método auxiliar para construção e comparação do XML gerado"""
        journal_meta_elem = build_journal_meta(self.empty_data)
        generated_xml_str = ET.tostring(journal_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_journal_meta_empty_data(self):
        expected_xml_str = (
            '<journal-meta>'
            '<journal-id journal-id-type="nlm-ta" />'
            '<journal-title-group>'
            '<journal-title />'
            '<abbrev-journal-title abbrev-type="publisher" />'
            '</journal-title-group>'
            '<publisher>'
            '<publisher-name />'
            '</publisher>'
            '</journal-meta>'
        )
        self._build_and_compare(expected_xml_str)

    def test_journal_meta_without_journal_ids(self):
        self.maxDiff = None
        # Exclui journal_ids para testar a ausência
        self.empty_data.pop("journal_ids")
        expected_xml_str = (
            '<journal-meta>'
            '<journal-title-group>'
            '<journal-title />'
            '<abbrev-journal-title abbrev-type="publisher" />'
            '</journal-title-group>'
            '<publisher>'
            '<publisher-name />'
            '</publisher>'
            '</journal-meta>'
        )
        self._build_and_compare(expected_xml_str)

    def test_journal_meta_without_issn(self):
        # Exclui issn para testar a ausência
        self.empty_data.pop("issn")
        expected_xml_str = (
            '<journal-meta>'
            '<journal-id journal-id-type="nlm-ta" />'
            '<journal-title-group>'
            '<journal-title />'
            '<abbrev-journal-title abbrev-type="publisher" />'
            '</journal-title-group>'
            '<publisher>'
            '<publisher-name />'
            '</publisher>'
            '</journal-meta>'
        )
        self._build_and_compare(expected_xml_str)


if __name__ == '__main__':
    unittest.main()
