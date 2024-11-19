import unittest
import xml.etree.ElementTree as ET
from packtools.sps.formats.sps_xml.front import build_front


class TestBuildFront(unittest.TestCase):
    def test_build_front(self):
        self.maxDiff = None
        node = {
            "journal-meta": ET.fromstring(
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
            ),
            "article-meta": ET.fromstring(
                '<article-meta>'
                '<article-id pub-id-type="doi">10.1016/j.bjane.2019.01.003</article-id>'
                '<article-id pub-id-type="other">00603</article-id>'
                '</article-meta>'
            )
        }
        expected_xml_str = (
            '<front>'
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
                '<article-meta>'
                    '<article-id pub-id-type="doi">10.1016/j.bjane.2019.01.003</article-id>'
                    '<article-id pub-id-type="other">00603</article-id>'
                '</article-meta>'
            '</front>'
        )
        aff_elem = build_front(node)
        generated_xml_str = ET.tostring(aff_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_front_journal_meta_None(self):
        node = {
            "journal-meta": None,
            "article-meta": ET.fromstring(
                '<article-meta>'
                '<article-id pub-id-type="doi">10.1016/j.bjane.2019.01.003</article-id>'
                '<article-id pub-id-type="other">00603</article-id>'
                '</article-meta>'
            )
        }
        with self.assertRaises(ValueError) as e:
            build_front(node)
        self.assertEqual(str(e.exception), "journal-meta and article-meta nodes are required.")

    def test_build_front_article_meta_None(self):
        node = {
            "journal-meta": ET.fromstring(
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
            ),
            "article-meta": None
        }
        with self.assertRaises(ValueError) as e:
            build_front(node)
        self.assertEqual(str(e.exception), "journal-meta and article-meta nodes are required.")