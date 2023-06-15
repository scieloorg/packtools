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
    xml_pubmed_author_list,
    xml_pubmed_publication_type,
    xml_pubmed_article_id,
    xml_pubmed_history,
    xml_pubmed_vernacular_title_pipe,
    xml_pubmed_object_list,
)


class PipelinePubmed(unittest.TestCase):
    maxDiff = None

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
            'Spontaneous Coronary Artery Dissection: Are There Differences between Men and Women?'
            '</ArticleTitle>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article/>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" article-type="letter" '
            'dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<title-group>'
            '<article-title>Dissecção Espontânea da Artéria Coronária: Existem Diferenças entre Homens e Mulheres?</article-title>'
            '</title-group>'
            '</article-meta>'
            '</front>'
            '<sub-article article-type="translation" id="TRen" xml:lang="en">'
            '<front-stub>'
            '<title-group>'
            '<article-title>Spontaneous Coronary Artery Dissection: Are There Differences between Men and Women?</article-title>'
            '</title-group>'
            '</front-stub>'
            '</sub-article>'
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

    def test_xml_pubmed_vernacular_title_pipe(self):
        expected = (
            '<Article>'
            '<VernacularTitle>'
            'Dissecção Espontânea da Artéria Coronária: Existem Diferenças entre Homens e Mulheres?'
            '</VernacularTitle>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article/>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" article-type="letter" '
            'dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<title-group>'
            '<article-title>Dissecção Espontânea da Artéria Coronária: Existem Diferenças entre Homens e Mulheres?</article-title>'
            '</title-group>'
            '</article-meta>'
            '</front>'
            '<sub-article article-type="translation" id="TRen" xml:lang="en">'
            '<front-stub>'
            '<title-group>'
            '<article-title>Spontaneous Coronary Artery Dissection: Are There Differences between Men and Women?</article-title>'
            '</title-group>'
            '</front-stub>'
            '</sub-article>'
            '</article>'
        )

        xml_pubmed_vernacular_title_pipe(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_vernacular_title_pipe_without_title(self):
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

        xml_pubmed_vernacular_title_pipe(xml_pubmed, xml_tree)

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

    def test_xml_pubmed_author_list(self):
        expected = (
            '<Article>'
            '<AuthorList>'
            '<Author>'
            '<FirstName>EWERTTON S.</FirstName>'
            '<LastName>GADELHA</LastName>'
            '<Affiliation>Museu Emilio Goeldi, Programa de Pós-Graduação em Biodiversidade e Evolução, Av. Perimetral, 1901, 66077-830 Belém, PA, Brazil</Affiliation>'
            '<Identifier Source="orcid">http://orcid.org/0000-0002-5741-6547</Identifier>'
            '</Author>'
            '<Author>'
            '<FirstName>BÁRBARA</FirstName>'
            '<LastName>DUNCK</LastName>'
            '<AffiliationInfo>'
            '<Affiliation>Universidade Federal do Pará (UFPA), Programa de Pós-Graduação em Ecologia - PPGECO, Laboratório de Ecologia de Produtores Primários, Rua Augusto Corrêa, 1, 66075-110 Belém, PA, Brazil </Affiliation>'
            '</AffiliationInfo>'
            '<AffiliationInfo>'
            '<Affiliation>Universidade Federal Rural da Amazônia (UFRA), Instituto Socioambiental e de Recursos Hídricos, Av. Tancredo Neves, 2501, 66077-830 Belém, PA, Brazil </Affiliation>'
            '</AffiliationInfo>'
            '<Identifier Source="orcid">http://orcid.org/0000-0003-0608-0614</Identifier>'
            '</Author>'
            '<Author>'
            '<FirstName>NADSON R.</FirstName>'
            '<LastName>SIMÕES</LastName>'
            '<Affiliation>Universidade Federal do Sul da Bahia, Programa de Pós-Graduação em Ciências e Tecnologias Ambientais, Rodovia Ilhéus, Km 22, 45604-811 Itabuna, BA, Brazil</Affiliation>'
            '<Identifier Source="orcid">http://orcid.org/0000-0002-4577-9033</Identifier>'
            '</Author>'
            '<Author>'
            '<FirstName>EDUARDO T.</FirstName>'
            '<LastName>PAES</LastName>'
            '<Affiliation>Universidade Federal Rural da Amazônia (UFRA), Instituto Socioambiental e de Recursos Hídricos, Av. Tancredo Neves, 2501, 66077-830 Belém, PA, Brazil </Affiliation>'
            '<Identifier Source="orcid">http://orcid.org/0000-0002-9429-2598</Identifier>'
            '</Author>'
            '<Author>'
            '<FirstName>ALBERTO</FirstName>'
            '<LastName>AKAMA</LastName>'
            '<Affiliation>Museu Emilio Goeldi, Programa de Pós-Graduação em Biodiversidade e Evolução, Av. Perimetral, 1901, 66077-830 Belém, PA, Brazil</Affiliation>'
            '<Identifier Source="orcid">http://orcid.org/0000-0003-0209-770X</Identifier>'
            '</Author>'
            '</AuthorList>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article/>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" '
            'dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<article-meta>'
            '<article-id specific-use="scielo-v3" pub-id-type="publisher-id">5HVjkrtdDn6BmBNP5fxP38p</article-id>'
            '<article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0001-37652022000501309</article-id>'
            '<article-id pub-id-type="doi">10.1590/0001-3765202220201894</article-id>'
            '<contrib-group>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-5741-6547</contrib-id>'
            '<name>'
            '<surname>GADELHA</surname>'
            '<given-names>EWERTTON S.</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff1">'
            '<sup>1</sup>'
            '</xref>'
            '<role>led the study</role>'
            '</contrib>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0003-0608-0614</contrib-id>'
            '<name>'
            '<surname>DUNCK</surname>'
            '<given-names>BÁRBARA</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff2">'
            '<sup>2</sup>'
            '</xref>'
            '<xref ref-type="aff" rid="aff3">'
            '<sup>3</sup>'
            '</xref>'
            '<role>conceptualization, methodology, formal analysis, writing - original draft, writing review and editing</role>'
            '</contrib>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-4577-9033</contrib-id>'
            '<name>'
            '<surname>SIMÕES</surname>'
            '<given-names>NADSON R.</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff4">'
            '<sup>4</sup>'
            '</xref>'
            '<role>conceptualization, methodology, writing - review and editing</role>'
            '</contrib>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0002-9429-2598</contrib-id>'
            '<name>'
            '<surname>PAES</surname>'
            '<given-names>EDUARDO T.</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff3">'
            '<sup>3</sup>'
            '</xref>'
            '<role>methodology, supervision, writing - review and editing</role>'
            '</contrib>'
            '<contrib contrib-type="author">'
            '<contrib-id contrib-id-type="orcid">0000-0003-0209-770X</contrib-id>'
            '<name>'
            '<surname>AKAMA</surname>'
            '<given-names>ALBERTO</given-names>'
            '</name>'
            '<xref ref-type="aff" rid="aff1">'
            '<sup>1</sup>'
            '</xref>'
            '<role>supervision, writing - review and editing</role>'
            '</contrib>'
            '</contrib-group>'
            '<aff id="aff1">'
            '<label>'
            '<sup>1</sup>'
            '</label>'
            '<institution content-type="orgname">Museu Emilio Goeldi</institution>'
            '<institution content-type="orgdiv1">Programa de Pós-Graduação em Biodiversidade e Evolução</institution>'
            '<addr-line>'
            '<named-content content-type="city">Belém</named-content>'
            '<named-content content-type="state">PA</named-content>'
            '</addr-line>'
            '<country country="BR">Brazil</country>'
            '<institution content-type="original">Museu Emilio Goeldi, Programa de Pós-Graduação em Biodiversidade e Evolução, Av. Perimetral, 1901, 66077-830 Belém, PA, Brazil</institution>'
            '</aff>'
            '<aff id="aff2">'
            '<label>'
            '<sup>2</sup>'
            '</label>'
            '<institution content-type="orgname">Universidade Federal do Pará (UFPA)</institution>'
            '<institution content-type="orgdiv1">Programa de Pós-Graduação em Ecologia - PPGECO</institution>'
            '<addr-line>'
            '<named-content content-type="city">Belém</named-content>'
            '<named-content content-type="state">PA</named-content>'
            '</addr-line>'
            '<country country="BR">Brazil</country>'
            '<institution content-type="original">Universidade Federal do Pará (UFPA), Programa de Pós-Graduação em Ecologia - PPGECO, Laboratório de Ecologia de Produtores Primários, Rua Augusto Corrêa, 1, 66075-110 Belém, PA, Brazil </institution>'
            '</aff>'
            '<aff id="aff3">'
            '<label>'
            '<sup>3</sup>'
            '</label>'
            '<institution content-type="orgname">Universidade Federal Rural da Amazônia (UFRA)</institution>'
            '<institution content-type="orgdiv1">Instituto Socioambiental e de Recursos Hídricos</institution>'
            '<addr-line>'
            '<named-content content-type="city">Belém</named-content>'
            '<named-content content-type="state">PA</named-content>'
            '</addr-line>'
            '<country country="BR">Brazil</country>'
            '<institution content-type="original">Universidade Federal Rural da Amazônia (UFRA), Instituto Socioambiental e de Recursos Hídricos, Av. Tancredo Neves, 2501, 66077-830 Belém, PA, Brazil </institution>'
            '</aff>'
            '<aff id="aff4">'
            '<label>'
            '<sup>4</sup>'
            '</label>'
            '<institution content-type="orgname">Universidade Federal do Sul da Bahia</institution>'
            '<institution content-type="orgdiv1">Programa de Pós-Graduação em Ciências e Tecnologias Ambientais</institution>'
            '<addr-line>'
            '<named-content content-type="city">Itabuna</named-content>'
            '<named-content content-type="state">BA</named-content>'
            '</addr-line>'
            '<country country="BR">Brazil</country>'
            '<institution content-type="original">Universidade Federal do Sul da Bahia, Programa de Pós-Graduação em Ciências e Tecnologias Ambientais, Rodovia Ilhéus, Km 22, 45604-811 Itabuna, BA, Brazil</institution>'
            '</aff>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_author_list(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_author_list_without_author(self):
        expected = (
            '<Article/>'
        )
        xml_pubmed = ET.fromstring(
            '<Article/>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" '
            'dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<article-meta>'
            '<article-id specific-use="scielo-v3" pub-id-type="publisher-id">5HVjkrtdDn6BmBNP5fxP38p</article-id>'
            '<article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0001-37652022000501309</article-id>'
            '<article-id pub-id-type="doi">10.1590/0001-3765202220201894</article-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_author_list(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_publication_type(self):
        # TODO
        # Originalmente, espera-se que o valor da tag <PublicationType> seja Journal Article
        # Nos arquivos de exemplo há somente a referencia a Research Article, o qual foi utilizado
        expected = (
            '<Article>'
            '<PublicationType>Research Article</PublicationType>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article/>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '</article>'
        )

        xml_pubmed_publication_type(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_publication_type_without_type(self):
        expected = (
            '<Article/>'
        )
        xml_pubmed = ET.fromstring(
            '<Article/>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '</article>'
        )

        xml_pubmed_publication_type(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_article_id(self):
        expected = (
            '<Article>'
            '<ArticleIdList>'
            '<ArticleId IdType="pii">S0066-782X2023000100501</ArticleId>'
            '<ArticleId IdType="doi">10.36660/abc.20210550</ArticleId>'
            '</ArticleIdList>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article/>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="letter" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<article-id specific-use="scielo-v3" pub-id-type="publisher-id">6LBrxmZwBqzgcwcCzgQQwzL</article-id>'
            '<article-id specific-use="scielo-v2" pub-id-type="publisher-id">S0066-782X2023000100501</article-id>'
            '<article-id pub-id-type="other">00501</article-id>'
            '<article-id pub-id-type="doi">10.36660/abc.20210550</article-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_article_id(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)


if __name__ == '__main__':
    unittest.main()
