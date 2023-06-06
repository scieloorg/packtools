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

    def test_xml_pubmed_issn_pipe_without_issn(self):
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
            '</front>'
            '</article>'
        )

        xml_pubmed_issn_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_volume_pipe(self):
        expected = (
            '<Article>'
            '<Journal>'
            '<Volume>37</Volume>'
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
            '<article-meta>'
            '<volume>37</volume>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_volume_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_volume_pipe_without_volume(self):
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
            '<article-meta>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_volume_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_issue_pipe(self):
        expected = (
            '<Article>'
            '<Journal>'
            '<Issue>11</Issue>'
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
            '<article-meta>'
            '<issue>11</issue>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_issue_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_issue_pipe_without_issue(self):
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
            '<article-meta>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_issue_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_pub_date_pipe(self):
        expected = (
            '<Article>'
            '<Journal>'
            '<PubDate PubStatus="epublish">'
            '<Year>2023</Year>'
            '<Month>01</Month>'
            '<Day>06</Day>'
            '</PubDate>'
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
            '<article-meta>'
            '<pub-date publication-format="electronic" date-type="pub">'
            '<day>06</day>'
            '<month>01</month>'
            '<year>2023</year>'
            '</pub-date>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_pub_date_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_pub_date_pipe_without_day(self):
        expected = (
            '<Article>'
            '<Journal>'
            '<PubDate PubStatus="epublish">'
            '<Year>2023</Year>'
            '<Month>01</Month>'
            '</PubDate>'
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
            '<article-meta>'
            '<pub-date publication-format="electronic" date-type="pub">'
            '<month>01</month>'
            '<year>2023</year>'
            '</pub-date>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_pub_date_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_pub_date_pipe_without_month(self):
        expected = (
            '<Article>'
            '<Journal>'
            '<PubDate PubStatus="epublish">'
            '<Year>2023</Year>'
            '<Day>06</Day>'
            '</PubDate>'
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
            '<article-meta>'
            '<pub-date publication-format="electronic" date-type="pub">'
            '<day>06</day>'
            '<year>2023</year>'
            '</pub-date>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_pub_date_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_pub_date_pipe_without_year(self):
        expected = (
            '<Article>'
            '<Journal>'
            '<PubDate PubStatus="epublish">'
            '<Month>01</Month>'
            '<Day>06</Day>'
            '</PubDate>'
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
            '<article-meta>'
            '<pub-date publication-format="electronic" date-type="pub">'
            '<day>06</day>'
            '<month>01</month>'
            '</pub-date>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_pub_date_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_pub_date_pipe_without_date(self):
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
            '<article-meta>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_pub_date_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_article_title_pipe(self):
        expected = (
            '<Article>'
            '<ArticleTitle>'
            'The mechanism study of inhibition effect of prepared Radix Rehmanniainon combined with Radix Astragali '
            'osteoporosis through PI3K-AKT signaling pathway'
            '</ArticleTitle>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article/>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<article-meta>'
            '<title-group>'
            '<article-title>'
            'The mechanism study of inhibition effect of prepared Radix Rehmanniainon combined with Radix Astragali '
            'osteoporosis through PI3K-AKT signaling pathway</article-title>'
            '</title-group>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_article_title_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_article_title_pipe_without_title(self):
        expected = (
            '<Article/>'
        )
        xml_pubmed = ET.fromstring(
            '<Article/>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<article-meta>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_article_title_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_first_page_pipe(self):
        expected = (
            '<Article>'
            '<FirstPage LZero="save">e2022440</FirstPage>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article/>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<article-meta>'
            '<elocation-id>e2022440</elocation-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_first_page_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_first_page_pipe_without_first_page(self):
        expected = (
            '<Article/>'
        )
        xml_pubmed = ET.fromstring(
            '<Article/>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<article-meta>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_first_page_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_elocation_pipe(self):
        expected = (
            '<Article>'
            '<ELocationID EIdType="pii">S0001-37652022000501309</ELocationID>'
            '<ELocationID EIdType="doi">10.1590/0001-3765202220201894</ELocationID>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article/>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<article-meta>'
            '<article-id specific-use="scielo-v3" pub-id-type="publisher-id">5HVjkrtdDn6BmBNP5fxP38p</article-id>'
            '<article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0001-37652022000501309</article-id>'
            '<article-id pub-id-type="other">01309</article-id>'
            '<article-id pub-id-type="doi">10.1590/0001-3765202220201894</article-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_elocation_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_language_pipe(self):
        expected = (
            '<Article>'
            '<Language>PT</Language>'
            '<Language>EN</Language>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article/>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="letter" dtd-version="1.1" specific-use="sps-1.9" '
            'xml:lang="pt">'
            '<sub-article article-type="translation" id="TRen" xml:lang="en">'
            '</sub-article>'
            '</article>'
        )

        xml_pubmed_language_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_language_pipe_one_lang(self):
        expected = (
            '<Article>'
            '<Language>PT</Language>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article/>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="letter" dtd-version="1.1" specific-use="sps-1.9" '
            'xml:lang="pt">'
            '</article>'
        )

        xml_pubmed_language_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_language_pipe_without_lang(self):
        expected = (
            '<Article/>'
        )
        xml_pubmed = ET.fromstring(
            '<Article/>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="letter" dtd-version="1.1" specific-use="sps-1.9">'
            '</article>'
        )

        xml_pubmed_language_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)


if __name__ == '__main__':
    unittest.main()
