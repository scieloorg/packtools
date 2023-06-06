import unittest
from lxml import etree as ET

from packtools.sps.formats.pubmed import (
    xml_pubmed_article_pipe,
    xml_pubmed_journal_pipe,
    xml_pubmed_publisher_name_pipe,
    xml_pubmed_journal_title_pipe,
    xml_pubmed_issn_pipe,
    xml_pubmed_volume_pipe,
    xml_pubmed_issue_pipe,
    xml_pubmed_pub_date_pipe,
    xml_pubmed_article_title_pipe,
    xml_pubmed_first_page_pipe,
    xml_pubmed_elocation_pipe,
    xml_pubmed_language_pipe,
)


class PipelinePubmed(unittest.TestCase):
    def test_xml_pubmed_article_pipe(self):
        expected = (
            '<Article/>'
        )

        obtained = ET.tostring(xml_pubmed_article_pipe(), encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_journal_pipe(self):
        expected = (
            '<Article>'
            '<Journal/>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article/>'
        )

        xml_pubmed_journal_pipe(xml_pubmed)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_publisher_name_pipe(self):
        expected = (
            '<Article>'
            '<Journal>'
            '<PublisherName>Colégio Brasileiro de Cirurgia Digestiva</PublisherName>'
            '</Journal>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article>'
            '<Journal/>'
            '</Article>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<journal-meta>'
            '<publisher>'
            '<publisher-name>Colégio Brasileiro de Cirurgia Digestiva</publisher-name>'
            '</publisher>'
            '</journal-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_publisher_name_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_publisher_name_pipe_without_publisher(self):
        expected = (
            '<Article>'
            '<Journal/>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article>'
            '<Journal/>'
            '</Article>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<journal-meta>'
            '</journal-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_publisher_name_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_journal_title_pipe(self):
        expected = (
            '<Article>'
            '<Journal>'
            '<JournalTitle>ABCD, arq. bras. cir. dig.</JournalTitle>'
            '</Journal>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article>'
            '<Journal/>'
            '</Article>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<journal-meta>'
            '<journal-title-group>'
            '<journal-title>ABCD. Arquivos Brasileiros de Cirurgia Digestiva (São Paulo)</journal-title>'
            '<abbrev-journal-title abbrev-type="publisher">ABCD, arq. bras. cir. dig.</abbrev-journal-title>'
            '</journal-title-group>'
            '</journal-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_journal_title_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_journal_title_pipe_without_title(self):
        expected = (
            '<Article>'
            '<Journal/>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article>'
            '<Journal/>'
            '</Article>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<journal-meta>'
            '</journal-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_journal_title_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_issn_pipe(self):
        expected = (
            '<Article>'
            '<Journal>'
            '<Issn>1678-2674</Issn>'
            '</Journal>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article>'
            '<Journal/>'
            '</Article>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<journal-meta>'
            '<issn pub-type="ppub">0102-8650</issn>'
            '<issn pub-type="epub">1678-2674</issn>'
            '</journal-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_issn_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

