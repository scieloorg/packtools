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

    def test_journal_meta_structure(self):
        # Gera o XML a partir dos dados
        journal_meta_elem = build_journal_meta(self.data)

        # Verifica se o elemento principal é <journal-meta>
        self.assertEqual(journal_meta_elem.tag, "journal-meta")

        # Verifica se <journal-id> elementos foram criados corretamente
        journal_ids = journal_meta_elem.findall("journal-id")
        self.assertEqual(len(journal_ids), 2)
        self.assertEqual(journal_ids[0].get("journal-id-type"), "nlm-ta")
        self.assertEqual(journal_ids[0].text, "Braz J Med Biol Res")
        self.assertEqual(journal_ids[1].get("journal-id-type"), "publisher-id")
        self.assertEqual(journal_ids[1].text, "bjmbr")

        # Verifica o grupo de títulos <journal-title-group>
        journal_title_group = journal_meta_elem.find("journal-title-group")
        self.assertIsNotNone(journal_title_group)

        # Verifica se <journal-title> foi criado corretamente
        journal_title = journal_title_group.find("journal-title")
        self.assertEqual(journal_title.text, "Brazilian Journal of Medical and Biological Research")

        # Verifica o título abreviado <abbrev-journal-title>
        abbrev_title = journal_title_group.find("abbrev-journal-title")
        self.assertEqual(abbrev_title.text, "Braz. J. Med. Biol. Res.")
        self.assertEqual(abbrev_title.get("abbrev-type"), "publisher")

        # Verifica os elementos <issn>
        issns = journal_meta_elem.findall("issn")
        self.assertEqual(len(issns), 2)
        self.assertEqual(issns[0].get("pub-type"), "epub")
        self.assertEqual(issns[0].text, "1414-431X")
        self.assertEqual(issns[1].get("pub-type"), "ppub")
        self.assertEqual(issns[1].text, "0100-879X")

        # Verifica o elemento <publisher> e <publisher-name>
        publisher = journal_meta_elem.find("publisher")
        self.assertIsNotNone(publisher)

        publisher_name = publisher.find("publisher-name")
        self.assertEqual(publisher_name.text, "Associação Brasileira de Divulgação Científica")

    def test_journal_meta_empty_data(self):
        # Testa com dados vazios
        empty_data = {
            "journal_ids": {},
            "journal_title": "",
            "abbrev_journal_title": "",
            "issn": {},
            "publisher_name": ""
        }
        journal_meta_elem = build_journal_meta(empty_data)

        # Verifica se os elementos principais são criados, mas sem conteúdo
        self.assertEqual(journal_meta_elem.tag, "journal-meta")
        self.assertEqual(len(journal_meta_elem.findall("journal-id")), 0)
        self.assertEqual(len(journal_meta_elem.findall("issn")), 0)

        # Verifica se o <journal-title-group> está presente, mas vazio
        journal_title_group = journal_meta_elem.find("journal-title-group")
        self.assertIsNotNone(journal_title_group)

        journal_title = journal_title_group.find("journal-title")
        self.assertEqual(journal_title.text, "")

        abbrev_title = journal_title_group.find("abbrev-journal-title")
        self.assertEqual(abbrev_title.text, "")
        self.assertEqual(abbrev_title.get("abbrev-type"), "publisher")

        # Verifica se o <publisher> foi criado, mas sem nome
        publisher = journal_meta_elem.find("publisher")
        self.assertIsNotNone(publisher)

        publisher_name = publisher.find("publisher-name")
        self.assertEqual(publisher_name.text, "")

    def test_journal_meta_as_string(self):
        self.maxDiff = None
        # Gera o XML a partir dos dados
        journal_meta_elem = build_journal_meta(self.data)

        # Converte o elemento XML em uma string
        generated_xml_str = ET.tostring(journal_meta_elem, encoding="unicode", method="xml")

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
        self.assertEqual(generated_xml_str, expected_xml_str)


if __name__ == '__main__':
    unittest.main()
