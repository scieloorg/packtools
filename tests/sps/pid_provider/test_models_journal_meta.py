import unittest

from lxml import etree

from packtools.sps.pid_provider.models.journal_meta import Acronym


class TestAcronymJournalAcronSetter(unittest.TestCase):

    def test_setter_atualiza_journal_id_existente(self):
        xmltree = etree.fromstring(
            """<article><front><journal-meta>
            <journal-id journal-id-type="publisher-id">tinf</journal-id>
            <journal-id journal-id-type="nlm-ta">Rev Saude Publica</journal-id>
            </journal-meta></front></article>"""
        )
        acronym = Acronym(xmltree)

        acronym.text = "newacron"

        self.assertEqual(acronym.text, "newacron")
        self.assertEqual(acronym.text, "newacron")
        self.assertEqual(
            xmltree.findtext(
                './/journal-meta/journal-id[@journal-id-type="nlm-ta"]'
            ),
            "Rev Saude Publica",
        )

    def test_setter_cria_journal_id_quando_ausente(self):
        xmltree = etree.fromstring(
            "<article><front><journal-meta></journal-meta></front></article>"
        )
        acronym = Acronym(xmltree)

        self.assertIsNone(acronym.text)

        acronym.text = "brandnew"

        node = xmltree.find(
            './/journal-meta/journal-id[@journal-id-type="publisher-id"]'
        )
        self.assertIsNotNone(node)
        self.assertEqual(node.text, "brandnew")
        self.assertEqual(acronym.text, "brandnew")

    def test_setter_cria_journal_id_como_primeiro_filho(self):
        xmltree = etree.fromstring(
            """<article><front><journal-meta>"""
            """<journal-id journal-id-type="nlm-ta">Rev Saude Publica</journal-id>"""
            """<issn pub-type="epub">2318-0889</issn>"""
            """</journal-meta></front></article>"""
        )
        acronym = Acronym(xmltree)

        acronym.text = "brandnew"

        journal_meta = xmltree.find(".//journal-meta")
        first = journal_meta[0]
        self.assertEqual(first.tag, "journal-id")
        self.assertEqual(first.get("journal-id-type"), "publisher-id")
        self.assertEqual(first.text, "brandnew")
        self.assertEqual(journal_meta[1].get("journal-id-type"), "nlm-ta")
        self.assertEqual(len(journal_meta.findall("journal-id")), 2)

    def test_setter_aplica_strip(self):
        xmltree = etree.fromstring(
            "<article><front><journal-meta></journal-meta></front></article>"
        )
        acronym = Acronym(xmltree)

        acronym.text = "  acron \n"

        self.assertEqual(acronym.text, "acron")

    def test_setter_rejeita_valor_vazio(self):
        xml = (
            """<article><front><journal-meta>"""
            """<journal-id journal-id-type="publisher-id">tinf</journal-id>"""
            """</journal-meta></front></article>"""
        )
        for value in (None, "", "   "):
            with self.subTest(value=value):
                xmltree = etree.fromstring(xml)
                acronym = Acronym(xmltree)
                with self.assertRaises(ValueError):
                    acronym.text = value
                self.assertEqual(acronym.text, "tinf")

    def test_setter_sem_journal_meta_levanta_value_error(self):
        xmltree = etree.fromstring("<article><front></front></article>")
        acronym = Acronym(xmltree)

        with self.assertRaises(ValueError) as cm:
            acronym.text = "acron"
        self.assertIn("journal-meta", str(cm.exception))

    def test_setter_atualiza_journal_id_nao_filho_direto(self):
        xmltree = etree.fromstring(
            """<article><front><journal-meta><wrapper>"""
            """<journal-id journal-id-type="publisher-id">old</journal-id>"""
            """</wrapper></journal-meta></front></article>"""
        )
        acronym = Acronym(xmltree)

        acronym.text = "new"

        nodes = xmltree.findall(
            './/journal-id[@journal-id-type="publisher-id"]'
        )
        self.assertEqual(len(nodes), 1)
        self.assertEqual(acronym.text, "new")
