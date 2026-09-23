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

        acronym.journal_acron = "newacron"

        self.assertEqual(acronym.journal_acron, "newacron")
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

        self.assertIsNone(acronym.journal_acron)

        acronym.journal_acron = "brandnew"

        node = xmltree.find(
            './/journal-meta/journal-id[@journal-id-type="publisher-id"]'
        )
        self.assertIsNotNone(node)
        self.assertEqual(node.text, "brandnew")
        self.assertEqual(acronym.journal_acron, "brandnew")
