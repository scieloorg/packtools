import unittest
from lxml import etree as ET
from packtools.sps.utils import xml_utils

from packtools.sps.formats.pubmed import (
    xml_pubmed_article_set,
    xml_pubmed_dtd_header,
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
    xml_pubmed_title_reference_list,
    xml_pubmed_citations,
    xml_pubmed_abstract,
    xml_pubmed_other_abstract,
    xml_pubmed_copyright_information,
    pipeline_pubmed,
)


class PipelinePubmed(unittest.TestCase):
    maxDiff = None

    def get_expected_dtd_header(self):
        return b'''<!DOCTYPE ArticleSet PUBLIC "-//NLM//DTD PubMed 2.8//EN" "https://dtd.nlm.nih.gov/ncbi/pubmed/in/PubMed.dtd">\n<ArticleSet/>\n'''
    
    def get_expected_article_pipe(self):
        return b'''<!DOCTYPE ArticleSet PUBLIC "-//NLM//DTD PubMed 2.8//EN" "https://dtd.nlm.nih.gov/ncbi/pubmed/in/PubMed.dtd">\n<ArticleSet>\n  <Article/>\n</ArticleSet>\n'''
    
    def get_xml_pubmed_base(self):
        return ET.fromstring(
            '<ArticleSet>'
            '<Article>'
            '<Journal/>'
            '</Article>'
            '</ArticleSet>'
        )

    def get_expected_xml_base(self):
        return ET.tostring(self.get_xml_pubmed_base(), encoding="utf-8").decode("utf-8")

    def get_expected_report(self, missing_tag, validation_errors, tag_path):
        return  {
            "missing_tags": missing_tag,
            "validation_errors": validation_errors,
            "tag_path": tag_path,
        }

    def test_xml_pubmed_dtd_header(self):
        expected = self.get_expected_dtd_header()
        xml = xml_pubmed_article_set()
        xml = xml_pubmed_dtd_header(xml_pubmed=xml)
        xml_str = ET.tostring(xml, pretty_print=True, encoding="UTF-8")
        self.assertEqual(xml_str, expected)

    def test_xml_pubmed_article_pipe(self):
        expected = self.get_expected_article_pipe()
        xml = xml_pubmed_article_set()
        xml_pubmed = xml_pubmed_dtd_header(xml_pubmed=xml)
        xml_pubmed_article_pipe(xml_pubmed=xml_pubmed)
        obtained = ET.tostring(xml, encoding="utf-8", pretty_print=True)

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_journal_pipe(self):
        str_pubmed = b'''\n<ArticleSet>\n  <Article/>\n</ArticleSet>\n'''
        xml_pubmed = ET.fromstring(str_pubmed)
        expected = self.get_xml_pubmed_base()
        xml_pubmed_journal_pipe(xml_pubmed=xml_pubmed)
        
        obtained = ET.tostring(xml_pubmed, encoding="utf-8", pretty_print=True)

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_publisher_name_pipe(self):
        expected = (
            '<ArticleSet>'
            '<Article>'
            '<Journal>'
            '<PublisherName>Colégio Brasileiro de Cirurgia Digestiva</PublisherName>'
            '</Journal>'
            '</Article>'
            '</ArticleSet>'
        )
        xml_pubmed = self.get_xml_pubmed_base()
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

        xml_pubmed_publisher_name_pipe(xml_pubmed, xml_tree, report={})

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_missing_publisher_name(self):
        expected_report = self.get_expected_report(
            missing_tag="PublisherName",
            validation_errors="Value not found in SciELO XML for PublisherName",
            tag_path=".//journal-meta//publisher//publisher-name",
        )
        expected_xml = self.get_expected_xml_base()
        xml_pubmed = self.get_xml_pubmed_base()
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
        report = {}
        xml_pubmed_publisher_name_pipe(xml_pubmed, xml_tree, report=report)

        obtained_xml = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained_xml, expected_xml)
        self.assertEqual(expected_report, report)

    def test_xml_pubmed_journal_title_pipe(self):
        expected = (
            '<ArticleSet>'
            '<Article>'
            '<Journal>'
            '<JournalTitle>ABCD, arq. bras. cir. dig.</JournalTitle>'
            '</Journal>'
            '</Article>'
            '</ArticleSet>'
        )
        xml_pubmed = self.get_xml_pubmed_base()
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

        xml_pubmed_journal_title_pipe(xml_pubmed, xml_tree, report={})

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_missing_journal_title_pipe(self):
        expected_report = self.get_expected_report(
            missing_tag="JournalTitle",
            validation_errors="Value not found in SciELO XML for JournalTitle",
            tag_path='.//journal-meta//journal-title-group//abbrev-journal-title[@abbrev-type="publisher"]',
        )
        expected_xml = self.get_expected_xml_base()
        xml_pubmed = self.get_xml_pubmed_base()
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

        report = {}
        xml_pubmed_journal_title_pipe(xml_pubmed, xml_tree, report=report)

        obtained_xml = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained_xml, expected_xml)
        self.assertEqual(expected_report, report)

    def test_xml_pubmed_issn_pipe(self):
        expected = (
            '<ArticleSet>'
            '<Article>'
            '<Journal>'
            '<Issn>1678-2674</Issn>'
            '</Journal>'
            '</Article>'
            '</ArticleSet>'
        )
        xml_pubmed = self.get_xml_pubmed_base()
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

        xml_pubmed_issn_pipe(xml_pubmed, xml_tree, report={})

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_missing_issn_pipe(self):
        expected_report = self.get_expected_report(
            missing_tag="Issn",
            validation_errors="Value not found for Issn",
            tag_path='.//journal-meta//issn',            
        )
        expected_xml = self.get_expected_xml_base()
        xml_pubmed = self.get_xml_pubmed_base()
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '</front>'
            '</article>'
        )

        report = {}
        xml_pubmed_issn_pipe(xml_pubmed, xml_tree, report=report)

        obtained_xml = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained_xml, expected_xml)
        self.assertEqual(expected_report, report)

    def test_xml_pubmed_volume_pipe(self):
        expected = (
            '<ArticleSet>'
            '<Article>'
            '<Journal>'
            '<Volume>37</Volume>'
            '</Journal>'
            '</Article>'
            '</ArticleSet>'
        )
        xml_pubmed = self.get_xml_pubmed_base()
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

        xml_pubmed_volume_pipe(xml_pubmed, xml_tree, report={})

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")
        self.assertEqual(obtained, expected)

    def test_xml_pubmed_missing_volume_pipe(self):
        expected_report = self.get_expected_report(
            missing_tag="Volume",
            validation_errors="Volume in PubMed XML is required if Issue is empty",
            tag_path='.//front/article-meta/volume',            
        )
        expected_xml = self.get_expected_xml_base()
        xml_pubmed = self.get_xml_pubmed_base()
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

        report = {}
        xml_pubmed_volume_pipe(xml_pubmed, xml_tree, report=report)

        obtained_xml = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained_xml, expected_xml)
        self.assertEqual(expected_report, report)

    def test_xml_pubmed_issue_pipe(self):
        expected = (
            '<ArticleSet>'
            '<Article>'
            '<Journal>'
            '<Issue>11</Issue>'
            '</Journal>'
            '</Article>'
            '</ArticleSet>'
        )
        xml_pubmed = self.get_xml_pubmed_base()
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

        xml_pubmed_issue_pipe(xml_pubmed, xml_tree, report={})

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_missing_issue_pipe(self):
        expected_report = self.get_expected_report(
            missing_tag="Issue",
            validation_errors="Issue in PubMed XML is required if Volume is empty",
            tag_path='.//front/article-meta/issue',
        )            
        expected_xml = self.get_expected_xml_base()
        xml_pubmed = self.get_xml_pubmed_base()
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

        report = {}
        xml_pubmed_issue_pipe(xml_pubmed, xml_tree, report=report)

        obtained_xml = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained_xml, expected_xml)
        self.assertEqual(expected_report, report)

    def test_xml_pubmed_pub_date_pipe(self):
        expected = (
            '<ArticleSet>'
            '<Article>'
            '<Journal>'
            '<PubDate PubStatus="epublish">'
            '<Year>2023</Year>'
            '<Month>01</Month>'
            '<Day>06</Day>'
            '</PubDate>'
            '</Journal>'
            '</Article>'
            '</ArticleSet>'
        )
        xml_pubmed = self.get_xml_pubmed_base()
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<article-meta>'
            '<pub-date publication-format="electronic" date-type="pub">'
            '<day>06</day>'
            '<month>01</month>'
            '<season>Jan-Feb</season>'
            '<year>2023</year>'
            '</pub-date>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_pub_date_pipe(xml_pubmed, xml_tree, report={})

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_pub_date_pipe_missing_month(self):
        expected_report = self.get_expected_report(
            missing_tag="Month",
            validation_errors="Month is Required if the Day tag is present.",
            tag_path=".//pub-date",            
        )
        expected_xml = self.get_expected_xml_base()
        xml_pubmed = self.get_xml_pubmed_base()
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

        report = {}
        xml_pubmed_pub_date_pipe(xml_pubmed, xml_tree, report=report)

        obtained_xml = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained_xml, expected_xml)
        self.assertEqual(expected_report, report)

    def test_xml_pubmed_pub_date_pipe_missing_year(self):
        expected_report = self.get_expected_report(
            missing_tag="Year",
            validation_errors="Value not found in SciELO XML for Year",
            tag_path=".//pub-date",         
        )        
        expected_xml = self.get_expected_xml_base()
        xml_pubmed = self.get_xml_pubmed_base()
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<front>'
            '<article-meta>'
            '<pub-date publication-format="electronic" date-type="pub">'
            '</pub-date>'
            '</article-meta>'
            '</front>'
            '</article>'
        )
        report = {}
        xml_pubmed_pub_date_pipe(xml_pubmed, xml_tree, report=report)

        obtained_xml = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained_xml, expected_xml)
        self.assertEqual(expected_report, report)

    def test_xml_pubmed_pub_date_pipe_missing_pub_date(self):
        expected_report = self.get_expected_report(
            missing_tag="PubDate",
            validation_errors="PubDate is required",
            tag_path='.//pub-date',      
        )
        expected_xml = self.get_expected_xml_base()
        xml_pubmed = self.get_xml_pubmed_base()
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
        report = {}
        xml_pubmed_pub_date_pipe(xml_pubmed, xml_tree, report=report)

        obtained_xml = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained_xml, expected_xml)
        self.assertEqual(expected_report, report)

    def test_xml_pubmed_article_title_pipe(self):
        expected = (
            '<ArticleSet>'
            '<Article>'
            '<Journal/>'
            '<ArticleTitle>'
            'Spontaneous Coronary Artery Dissection: Are There Differences between Men and Women?'
            '</ArticleTitle>'
            '</Article>'
            '</ArticleSet>'
        )
        xml_pubmed = self.get_xml_pubmed_base()
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

    def test_xml_pubmed_vernacular_title_pipe(self):
        expected = (
            '<ArticleSet>'
            '<Article>'
            '<VernacularTitle>'
            'Dissecção Espontânea da Artéria Coronária: Existem Diferenças entre Homens e Mulheres?'
            '</VernacularTitle>'
            '</Article>'
            '</ArticleSet>'
        )
        xml_pubmed = ET.fromstring(
            '<ArticleSet>'
            '<Article/>'
            '</ArticleSet>'
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

    def test_xml_pubmed_first_page_pipe(self):
        expected = (
            '<ArticleSet>'
            '<Article>'
            '<FirstPage LZero="save">e2022440</FirstPage>'
            '</Article>'
            '</ArticleSet>'
        )
        xml_pubmed = ET.fromstring(
            '<ArticleSet>'
            '<Article/>'
            '</ArticleSet>'
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

    def test_xml_pubmed_first_page_pipe_missing_first_page(self):
        expected_report = self.get_expected_report(
            missing_tag="ELocationID",
            validation_errors="FirstPage is Required if ELocationID is not present",
            tag_path=".//front/article-meta/elocation-id",
        )
        expected_xml = self.get_expected_xml_base()
        xml_pubmed = self.get_xml_pubmed_base()
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
        report = {}
        xml_pubmed_pub_date_pipe(xml_pubmed, xml_tree, report=report)

        obtained_xml = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained_xml, expected_xml)
        self.assertEqual(expected_report, report)

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

    def test_xml_pubmed_elocation_pipe_missing_ELocationID(self):
        expected_report = self.get_expected_report(
            missing_tag="ELocationID",
            validation_errors="ELocationID is Required if FirstPage is not present",
            tag_path='.//article-id',
        )
        expected_xml = self.get_expected_xml_base()
        xml_pubmed = self.get_xml_pubmed_base()
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
        report = {}
        xml_pubmed_elocation_pipe(xml_pubmed, xml_tree, report=report)

        obtained_xml = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained_xml, expected_xml)
        self.assertEqual(expected_report, report)

    def test_xml_pubmed_language_pipe(self):
        expected = (
            '<ArticleSet>'
            '<Article>'
            '<Language>PT</Language>'
            '<Language>EN</Language>'
            '</Article>'
            '</ArticleSet>'
        )
        xml_pubmed = ET.fromstring(
            '<ArticleSet>'
            '<Article/>'
            '</ArticleSet>'
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
            '<ArticleSet>'
            '<Article>'
            '<Language>PT</Language>'
            '</Article>'
            '</ArticleSet>'
        )
        xml_pubmed = ET.fromstring(
            '<ArticleSet>'
            '<Article/>'
            '</ArticleSet>'
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

    def test_xml_pubmed_article_id(self):
        expected = (
            '<ArticleSet>'
            '<Article>'
            '<ArticleIdList>'
            '<ArticleId IdType="pii">S0066-782X2023000100501</ArticleId>'
            '<ArticleId IdType="doi">10.36660/abc.20210550</ArticleId>'
            '</ArticleIdList>'
            '</Article>'
            '</ArticleSet>'
        )
        xml_pubmed = ET.fromstring(
            '<ArticleSet>'
            '<Article/>'
            '</ArticleSet>'
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

    def test_xml_pubmed_article_id_without_pii(self):
        expected = (
            '<Article>'
            '<ArticleIdList>'
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
            '<article-id pub-id-type="other">00501</article-id>'
            '<article-id pub-id-type="doi">10.36660/abc.20210550</article-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_article_id(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_article_id_without_doi(self):
        expected = (
            '<Article>'
            '<ArticleIdList>'
            '<ArticleId IdType="pii">S0066-782X2023000100501</ArticleId>'
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
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_article_id(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_article_id_without_all_ids(self):
        expected = (
            '<Article/>'
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
            '<article-id pub-id-type="other">00501</article-id>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_article_id(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_history(self):
        expected = (
            '<ArticleSet>'
            '<Article>'
            '<History>'
            '<PubDate PubStatus="received">'
            '<Year>2021</Year>'
            '<Month>06</Month>'
            '<Day>22</Day>'
            '</PubDate>'
            '<PubDate PubStatus="accepted">'
            '<Year>2022</Year>'
            '<Month>06</Month>'
            '<Day>15</Day>'
            '</PubDate>'
            '<PubDate PubStatus="revised">'
            '<Year>2022</Year>'
            '<Month>06</Month>'
            '<Day>15</Day>'    
            '</PubDate>'        
            '<PubDate PubStatus="ecollection">'
            '<Year>2023</Year>'
            '</PubDate>'    
            '</History>'
            '</Article>'
            '</ArticleSet>'
        )
        xml_pubmed = ET.fromstring(
            '<ArticleSet>'
            '<Article/>'
            '</ArticleSet>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="letter" dtd-version="1.1" specific-use="sps-1.9" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<pub-date date-type="pub" publication-format="electronic">'
            '<day>09</day>'
            '<month>01</month>'
            '<year>2023</year>'
            '</pub-date>'
            '<pub-date date-type="collection" publication-format="electronic">'
            '<year>2023</year>'
            '</pub-date>'
            '<history>'
            '<date date-type="received">'
            '<day>22</day>'
            '<month>06</month>'
            '<year>2021</year>'
            '</date>'
            '<date date-type="rev-recd">'
            '<day>12</day>'
            '<month>03</month>'
            '<year>2022</year>'
            '</date>'
            '<date date-type="accepted">'
            '<day>15</day>'
            '<month>06</month>'
            '<year>2022</year>'
            '</date>'
            '<date date-type="rev-recd">'
            '<day>15</day>'
            '<month>06</month>'
            '<year>2022</year>'
            '</date>'   
            '</history>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_history(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")
        self.assertEqual(obtained, expected)

    def test_xml_pubmed_object_list_keyword(self):
        expected = (
            '<Article>'
            '<ObjectList>'
            '<Object Type="keyword">'
            '<Param Name="value">Arteries Dissection</Param>'
            '</Object>'
            '<Object Type="keyword">'
            '<Param Name="value">Acute Coronary Syndrome</Param>'
            '</Object>'
            '</ObjectList>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article/>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" article-type="letter" dtd-version="1.1" s'
            'pecific-use="sps-1.9" xml:lang="pt">'
            '<front>'
            '<article-meta>'
            '<kwd-group xml:lang="pt">'
            '<kwd>Dissecção das Artérias</kwd>'
            '<kwd>Síndrome Coronariana Aguda</kwd>'
            '</kwd-group>'
            '</article-meta>'
            '</front>'
            '<sub-article article-type="translation" id="TRen" xml:lang="en">'
            '<front-stub>'
            '<kwd-group xml:lang="en">'
            '<kwd>Arteries Dissection</kwd>'
            '<kwd>Acute Coronary Syndrome</kwd>'
            '</kwd-group>'
            '</front-stub>'
            '</sub-article>'
            '</article>'
        )

        xml_pubmed_object_list(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_title_reference_list(self):
        expected = (
            '<Article>'
            '<ReferenceList>'
            '<Title>REFERENCES</Title>'
            '</ReferenceList>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article />'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<back>'
            '<ref-list>'
            '<title>REFERENCES</title>'
            '</ref-list>'
            '</back>'
            '</article>'
        )

        xml_pubmed_title_reference_list(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_without_title_reference_list(self):
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
            '<back>'
            '<ref-list/>'
            '</back>'
            '</article>'
        )

        xml_pubmed_title_reference_list(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_citations(self):
        self.maxDiff = None
        expected = (
            '<Article>'
            '<ReferenceList>'
            '<Reference>'
            '<Citation>'
            'ALLAN JD. 1976. The University of Chicago life history patterns in zooplankton. Am Nat 110: 165-180. '
            'https://10.2307/2459885.'
            '</Citation>'
            '<ArticleIdList>'
            '<ArticleId IdType="pubmed">00000000</ArticleId>'
            '<ArticleId IdType="pmcid">11111111</ArticleId>'
            '</ArticleIdList>'
            '</Reference>'
            '<Reference>'
            '<Citation>'
            '2. Kwon JA, Jeon W, Park EC, Kim JH, Kim SJ, Yoo KB, et al. Effects of disease detection on changes in '
            'smoking behavior. '
            'Yonsei Med J. 2015;56(4): 1143-9. DOI:https://doi.org/10.3349/ymj.2015.56.4.1143'
            '</Citation>'
            '<ArticleIdList>'
            '<ArticleId IdType="pubmed">22222222</ArticleId>'
            '<ArticleId IdType="pmcid">33333333</ArticleId>'
            '</ArticleIdList>'
            '</Reference>'
            '</ReferenceList>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article>'
            '<ReferenceList/>'
            '</Article>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<back>'
            '<ref-list>'
            '<title>REFERENCES</title>'
            '<ref id="B1">'
            '<label>1.</label>'
            '<mixed-citation>ALLAN JD. 1976. The University of Chicago life history patterns in zooplankton. Am Nat 110: 165-180. https://10.2307/2459885.</mixed-citation>'
            '<element-citation publication-type="journal">'
            '<person-group person-group-type="author">'
            '<name>'
            '<surname>ALLAN</surname>'
            '<given-names>JD</given-names>'
            '</name>'
            '</person-group>'
            '<article-title>The University of Chicago life history patterns in zooplankton</article-title>'
            '<source>Am Nat</source>'
            '<year>1976</year>'
            '<volume>110</volume>'
            '<page-range>165-180</page-range>'
            '<pub-id pub-id-type="pmid">00000000</pub-id>'
            '<pub-id pub-id-type="pmcid">11111111</pub-id>'
            '</element-citation>'
            '</ref>'
            '<ref id="B2">'
            '<label>2.</label>'
            '<mixed-citation>'
            '2. Kwon JA, Jeon W, Park EC, Kim JH, Kim SJ, Yoo KB, et al. Effects of disease detection on changes in smoking behavior. Yonsei Med J. 2015;56(4): 1143-9. DOI:'
            '<ext-link ext-link-type="uri" xlink:href="https://doi.org/10.3349/ymj.2015.56.4.1143">https://doi.org/10.3349/ymj.2015.56.4.1143</ext-link>'
            '</mixed-citation>'
            '<element-citation publication-type="journal">'
            '<person-group person-group-type="author">'
            '<name>'
            '<surname>Kwon</surname>'
            '<given-names>JA</given-names>'
            '</name>'
            '<name>'
            '<surname>Jeon</surname>'
            '<given-names>W</given-names>'
            '</name>'
            '<name>'
            '<surname>Park</surname>'
            '<given-names>EC</given-names>'
            '</name>'
            '<name>'
            '<surname>Kim</surname>'
            '<given-names>JH</given-names>'
            '</name>'
            '<name>'
            '<surname>Kim</surname>'
            '<given-names>SJ</given-names>'
            '</name>'
            '<name>'
            '<surname>Yoo</surname>'
            '<given-names>KB</given-names>'
            '</name>'
            '<etal/>'
            '</person-group>'
            '<article-title>Effects of disease detection on changes in smoking behavior</article-title>'
            '<source>Yonsei Med J.</source>'
            '<year>2015</year>'
            '<volume>56</volume>'
            '<issue>4</issue>'
            '<fpage>1143</fpage>'
            '<lpage>9</lpage>'
            '<pub-id pub-id-type="pmid">22222222</pub-id>'
            '<pub-id pub-id-type="pmcid">33333333</pub-id>'
            '<comment>'
            'DOI:'
            '<ext-link ext-link-type="uri" xlink:href="https://doi.org/10.3349/ymj.2015.56.4.1143">https://doi.org/10.3349/ymj.2015.56.4.1143</ext-link>'
            '</comment>'
            '</element-citation>'
            '</ref>'
            '</ref-list>'
            '</back>'
            '</article>'
        )

        xml_pubmed_citations(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_without_citations(self):
        expected = (
            '<Article>'
            '<ReferenceList/>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article>'
            '<ReferenceList/>'
            '</Article>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<back/>'
            '</article>'
        )

        xml_pubmed_citations(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_citations_without_article_list_id(self):
        expected = (
            '<Article>'
            '<ReferenceList>'
            '<Reference>'
            '<Citation>'
            'ALLAN JD. 1976. The University of Chicago life history patterns in zooplankton. Am Nat 110: 165-180. '
            'https://10.2307/2459885.'
            '</Citation>'
            '</Reference>'
            '<Reference>'
            '<Citation>'
            '2. Kwon JA, Jeon W, Park EC, Kim JH, Kim SJ, Yoo KB, et al. Effects of disease detection on changes in '
            'smoking behavior. '
            'Yonsei Med J. 2015;56(4): 1143-9. DOI:https://doi.org/10.3349/ymj.2015.56.4.1143'
            '</Citation>'
            '</Reference>'
            '</ReferenceList>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article>'
            '<ReferenceList/>'
            '</Article>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">'
            '<back>'
            '<ref-list>'
            '<title>REFERENCES</title>'
            '<ref id="B1">'
            '<label>1.</label>'
            '<mixed-citation>ALLAN JD. 1976. The University of Chicago life history patterns in zooplankton. Am Nat 110: 165-180. https://10.2307/2459885.</mixed-citation>'
            '<element-citation publication-type="journal">'
            '<person-group person-group-type="author">'
            '<name>'
            '<surname>ALLAN</surname>'
            '<given-names>JD</given-names>'
            '</name>'
            '</person-group>'
            '<article-title>The University of Chicago life history patterns in zooplankton</article-title>'
            '<source>Am Nat</source>'
            '<year>1976</year>'
            '<volume>110</volume>'
            '<page-range>165-180</page-range>'
            '</element-citation>'
            '</ref>'
            '<ref id="B2">'
            '<label>2.</label>'
            '<mixed-citation>'
            '2. Kwon JA, Jeon W, Park EC, Kim JH, Kim SJ, Yoo KB, et al. Effects of disease detection on changes in smoking behavior. Yonsei Med J. 2015;56(4): 1143-9. DOI:'
            '<ext-link ext-link-type="uri" xlink:href="https://doi.org/10.3349/ymj.2015.56.4.1143">https://doi.org/10.3349/ymj.2015.56.4.1143</ext-link>'
            '</mixed-citation>'
            '<element-citation publication-type="journal">'
            '<person-group person-group-type="author">'
            '<name>'
            '<surname>Kwon</surname>'
            '<given-names>JA</given-names>'
            '</name>'
            '<name>'
            '<surname>Jeon</surname>'
            '<given-names>W</given-names>'
            '</name>'
            '<name>'
            '<surname>Park</surname>'
            '<given-names>EC</given-names>'
            '</name>'
            '<name>'
            '<surname>Kim</surname>'
            '<given-names>JH</given-names>'
            '</name>'
            '<name>'
            '<surname>Kim</surname>'
            '<given-names>SJ</given-names>'
            '</name>'
            '<name>'
            '<surname>Yoo</surname>'
            '<given-names>KB</given-names>'
            '</name>'
            '<etal/>'
            '</person-group>'
            '<article-title>Effects of disease detection on changes in smoking behavior</article-title>'
            '<source>Yonsei Med J.</source>'
            '<year>2015</year>'
            '<volume>56</volume>'
            '<issue>4</issue>'
            '<fpage>1143</fpage>'
            '<lpage>9</lpage>'
            '<comment>'
            'DOI:'
            '<ext-link ext-link-type="uri" xlink:href="https://doi.org/10.3349/ymj.2015.56.4.1143">https://doi.org/10.3349/ymj.2015.56.4.1143</ext-link>'
            '</comment>'
            '</element-citation>'
            '</ref>'
            '</ref-list>'
            '</back>'
            '</article>'
        )

        xml_pubmed_citations(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_abstract_without_sections(self):
        self.maxDiff = None
        expected = (
            '<ArticleSet>'
            '<Article>'
            '<Abstract>'
            'Patterns of beta diversity of plankton communities in rivers have been mainly determined by '
            'hydrological factors that alter the dispersion and composition of species and traits. Rotifers in the '
            'Guamá River (eastern Amazonian River) were sampled (monthly between October 2017 and June 2019) to '
            'analyze the temporal variation of taxonomic and functional beta diversity and its partitions (turnover '
            'and nestedness) as well as the effects of temporal, environmental, and seasonal dissimilarities. '
            'Taxonomic turnover and functional nestedness over time were observed as well as functional '
            'homogenization, which was arguably due to the hypereutrophic condition of the river. There were no '
            'seasonal differences in taxonomic and functional beta diversity probably due the low environmental '
            'dissimilarity. This study demonstrated that this Guamá River stretch presented low environmental '
            'dissimilarity and hypereutrophic waters, which benefited the establishment of a community of species '
            'with high taxonomic turnover over time, but with low functional dissimilarity and loss of some functions '
            'related to the functional traits evaluated in the ecosystem. It is important to point out that temporal '
            'studies should evaluate both taxonomic and functional aspects of communities, mainly because the effect '
            'of environmental changes may be more noticeable at the functional level of communities.'
            '</Abstract>'
            '</Article>'
            '</ArticleSet>'
        )
        xml_pubmed = ET.fromstring(
            '<ArticleSet>'
            '<Article/>'
            '</ArticleSet>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en"> '
            '<front>'
            '<article-meta>'
            '<abstract>'
            '<title>Abstract</title>'
            '<p>Patterns of beta diversity of plankton communities in rivers have been mainly determined by '
            'hydrological factors that alter the dispersion and composition of species and traits. Rotifers in the '
            'Guamá River (eastern Amazonian River) were sampled (monthly between October 2017 and June 2019) to '
            'analyze the temporal variation of taxonomic and functional beta diversity and its partitions (turnover '
            'and nestedness) as well as the effects of temporal, environmental, and seasonal dissimilarities. '
            'Taxonomic turnover and functional nestedness over time were observed as well as functional '
            'homogenization, which was arguably due to the hypereutrophic condition of the river. There were no '
            'seasonal differences in taxonomic and functional beta diversity probably due the low environmental '
            'dissimilarity. This study demonstrated that this Guamá River stretch presented low environmental '
            'dissimilarity and hypereutrophic waters, which benefited the establishment of a community of species '
            'with high taxonomic turnover over time, but with low functional dissimilarity and loss of some functions '
            'related to the functional traits evaluated in the ecosystem. It is important to point out that temporal '
            'studies should evaluate both taxonomic and functional aspects of communities, mainly because the effect '
            'of environmental changes may be more noticeable at the functional level of communities. </p> '
            '</abstract>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_abstract(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_abstract_with_sections(self):
        expected = (
            '<ArticleSet>'
            '<Article>'
            '<Abstract>'
            '<AbstractText Label="BACKGROUND">Hydatid disease, a parasitic infestation caused by Echinococcus granulosus larvae, is an infectious disease endemic in different areas, such as India, Australia, and South America. The liver is well known as the organ most commonly affected by hydatid disease and may present a wide variety of complications such as hepatothoracic hydatid transit, cyst superinfection, intra-abdominal dissemination, and communication of the biliary cyst with extravasation of parasitic material into the bile duct, also called cholangiohydatidosis. Humans are considered an intermediate host, exposed to these larvae by hand-to-mouth contamination of the feces of infected dogs.</AbstractText>'
            '<AbstractText Label="AIM">This study aimed to highlight the role of endoscopic retrograde cholangiopancreatography in patients with acute cholangitis secondary to cholangiohydatidosis.</AbstractText>'
            '<AbstractText Label="METHODS">Considering the imaging findings in a 36-year-old female patient with computed tomography and magnetic resonance imaging showing a complex cystic lesion in liver segment VI, with multiple internal vesicles and a wall defect cyst that communicates with the intrahepatic biliary tree, endoscopic biliary drainage was performed by endoscopic retrograde cholangiopancreatography with papillotomy, leading to the discharge of multiple obstructive cysts and hydatid sand from the main bile duct.</AbstractText>'
            '<AbstractText Label="RESULTS">Clinical and laboratory findings improved after drainage, with hospital discharge under oral antiparasitic treatment before complete surgical resection of the hepatic hydatid cyst.</AbstractText>'
            '<AbstractText Label="CONCLUSIONS">Endoscopic retrograde cholangiopancreatography is a safe and useful method for the treatment of biliary complications of hepatic hydatid disease and should be considered the first-line procedure for biliary drainage in cases of cholangiohydatid disease involving secondary acute cholangitis.</AbstractText>'
            '</Abstract>'
            '</Article>'
            '</ArticleSet>'
        )
        xml_pubmed = ET.fromstring(
            '<ArticleSet>'
            '<Article/>'
            '</ArticleSet>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en"> '
            '<front>'
            '<article-meta>'
            '<abstract>'
            '<title>ABSTRACT</title>'
            '<sec>'
            '<title>BACKGROUND:</title>'
            '<p>Hydatid disease, a parasitic infestation caused by Echinococcus granulosus larvae, is an infectious disease endemic in different areas, such as India, Australia, and South America. The liver is well known as the organ most commonly affected by hydatid disease and may present a wide variety of complications such as hepatothoracic hydatid transit, cyst superinfection, intra-abdominal dissemination, and communication of the biliary cyst with extravasation of parasitic material into the bile duct, also called cholangiohydatidosis. Humans are considered an intermediate host, exposed to these larvae by hand-to-mouth contamination of the feces of infected dogs.</p>'
            '</sec>'
            '<sec>'
            '<title>AIM:</title>'
            '<p>This study aimed to highlight the role of endoscopic retrograde cholangiopancreatography in patients with acute cholangitis secondary to cholangiohydatidosis.</p>'
            '</sec>'
            '<sec>'
            '<title>METHODS:</title>'
            '<p>Considering the imaging findings in a 36-year-old female patient with computed tomography and magnetic resonance imaging showing a complex cystic lesion in liver segment VI, with multiple internal vesicles and a wall defect cyst that communicates with the intrahepatic biliary tree, endoscopic biliary drainage was performed by endoscopic retrograde cholangiopancreatography with papillotomy, leading to the discharge of multiple obstructive cysts and hydatid sand from the main bile duct.</p>'
            '</sec>'
            '<sec>'
            '<title>RESULTS:</title>'
            '<p>Clinical and laboratory findings improved after drainage, with hospital discharge under oral antiparasitic treatment before complete surgical resection of the hepatic hydatid cyst.</p>'
            '</sec>'
            '<sec>'
            '<title>CONCLUSIONS:</title>'
            '<p>Endoscopic retrograde cholangiopancreatography is a safe and useful method for the treatment of biliary complications of hepatic hydatid disease and should be considered the first-line procedure for biliary drainage in cases of cholangiohydatid disease involving secondary acute cholangitis.</p>'
            '</sec>'
            '</abstract>'
            '<trans-abstract xml:lang="pt">'
            '<title>RESUMO</title>'
            '<sec>'
            '<title>RACIONAL:</title>'
            '<p>A doença hidática, uma infestação parasitária causada pelas larvas de Echinococcus granulosus, é uma doença infecciosa endêmica em diferentes áreas como Índia, Austrália e América do Sul. O fígado é conhecido como o órgão mais comumente afetado pela hidatidose, podendo apresentar uma grande variedade de complicações como trânsito hidático hepato-torácico, superinfecção do cisto, disseminação intra-abdominal e comunicação do cisto biliar com extravasamento de material parasitário para o ducto biliar ou também chamada de colangio-hidatidose O ser humano é considerado um hospedeiro intermediário, exposto a essas larvas pela contaminação mão-boca das fezes de cães infectados.</p>'
            '</sec>'
            '<sec>'
            '<title>OBJETIVO:</title>'
            '<p>Destacar o papel da endoscópica por colangiopancreatografia retrógrada em pacientes com colangite aguda secundária à colangio-hidatidose.</p>'
            '</sec>'
            '<sec>'
            '<title>MÉTODOS:</title>'
            '<p>Considerando os achados de imagem, em paciente feminina de 36 anos de idade, com imagens de tomografia computadorizada e ressonância magnética mostrando uma lesão cística complexa no segmento hepático VI, com múltiplas vesículas internas e um defeito de parede cística que se comunica com a árvore biliar intra-hepática foi realizada drenagem biliar endoscópica por colangiopancreatografia retrógrada com papilotomia, levando à descarga de múltiplos cistos obstrutivos e areia hidática da via biliar principal.</p>'
            '</sec>'
            '<sec>'
            '<title>RESULTADOS:</title>'
            '<p>Os achados clínicos e laboratoriais melhoraram após a drenagem, com alta hospitalar sob tratamento antiparasitário oral antes da ressecção cirúrgica completa do cisto hidático hepático.</p>'
            '</sec>'
            '<sec>'
            '<title>CONCLUSÕES:</title>'
            '<p>A endoscópica por colangiopancreatografia retrógrada é um método seguro e útil para o tratamento das complicações biliares da hidatidose hepática, devendo ser considerado o procedimento de primeira linha para drenagem biliar nos casos de colangio-hidatidose que envolve colangite aguda secundária.</p>'
            '</sec>'
            '</trans-abstract>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_abstract(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_abstract_without_abstract(self):
        expected = (
            '<Article/>'
        )
        xml_pubmed = ET.fromstring(
            '<Article/>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en"> '
            '<front>'
            '<article-meta>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_abstract(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)

    def test_xml_pubmed_other_abstract(self):
        expected = (
            '<Article>'
            '<OtherAbstract Language="pt">'
            '<AbstractText Label="RACIONAL">A doença hidática, uma infestação parasitária causada pelas larvas de Echinococcus granulosus, é uma doença infecciosa endêmica em diferentes áreas como Índia, Austrália e América do Sul. O fígado é conhecido como o órgão mais comumente afetado pela hidatidose, podendo apresentar uma grande variedade de complicações como trânsito hidático hepato-torácico, superinfecção do cisto, disseminação intra-abdominal e comunicação do cisto biliar com extravasamento de material parasitário para o ducto biliar ou também chamada de colangio-hidatidose O ser humano é considerado um hospedeiro intermediário, exposto a essas larvas pela contaminação mão-boca das fezes de cães infectados.</AbstractText>'
            '<AbstractText Label="OBJETIVO">Destacar o papel da endoscópica por colangiopancreatografia retrógrada em pacientes com colangite aguda secundária à colangio-hidatidose.</AbstractText>'
            '<AbstractText Label="MÉTODOS">Considerando os achados de imagem, em paciente feminina de 36 anos de idade, com imagens de tomografia computadorizada e ressonância magnética mostrando uma lesão cística complexa no segmento hepático VI, com múltiplas vesículas internas e um defeito de parede cística que se comunica com a árvore biliar intra-hepática foi realizada drenagem biliar endoscópica por colangiopancreatografia retrógrada com papilotomia, levando à descarga de múltiplos cistos obstrutivos e areia hidática da via biliar principal.</AbstractText>'
            '<AbstractText Label="RESULTADOS">Os achados clínicos e laboratoriais melhoraram após a drenagem, com alta hospitalar sob tratamento antiparasitário oral antes da ressecção cirúrgica completa do cisto hidático hepático.</AbstractText>'
            '<AbstractText Label="CONCLUSÕES">A endoscópica por colangiopancreatografia retrógrada é um método seguro e útil para o tratamento das complicações biliares da hidatidose hepática, devendo ser considerado o procedimento de primeira linha para drenagem biliar nos casos de colangio-hidatidose que envolve colangite aguda secundária.</AbstractText>'
            '</OtherAbstract>'
            '</Article>'
        )
        xml_pubmed = ET.fromstring(
            '<Article/>'
        )
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en"> '
            '<front>'
            '<article-meta>'
            '<abstract>'
            '<title>ABSTRACT</title>'
            '<sec>'
            '<title>BACKGROUND:</title>'
            '<p>Hydatid disease, a parasitic infestation caused by Echinococcus granulosus larvae, is an infectious disease endemic in different areas, such as India, Australia, and South America. The liver is well known as the organ most commonly affected by hydatid disease and may present a wide variety of complications such as hepatothoracic hydatid transit, cyst superinfection, intra-abdominal dissemination, and communication of the biliary cyst with extravasation of parasitic material into the bile duct, also called cholangiohydatidosis. Humans are considered an intermediate host, exposed to these larvae by hand-to-mouth contamination of the feces of infected dogs.</p>'
            '</sec>'
            '<sec>'
            '<title>AIM:</title>'
            '<p>This study aimed to highlight the role of endoscopic retrograde cholangiopancreatography in patients with acute cholangitis secondary to cholangiohydatidosis.</p>'
            '</sec>'
            '<sec>'
            '<title>METHODS:</title>'
            '<p>Considering the imaging findings in a 36-year-old female patient with computed tomography and magnetic resonance imaging showing a complex cystic lesion in liver segment VI, with multiple internal vesicles and a wall defect cyst that communicates with the intrahepatic biliary tree, endoscopic biliary drainage was performed by endoscopic retrograde cholangiopancreatography with papillotomy, leading to the discharge of multiple obstructive cysts and hydatid sand from the main bile duct.</p>'
            '</sec>'
            '<sec>'
            '<title>RESULTS:</title>'
            '<p>Clinical and laboratory findings improved after drainage, with hospital discharge under oral antiparasitic treatment before complete surgical resection of the hepatic hydatid cyst.</p>'
            '</sec>'
            '<sec>'
            '<title>CONCLUSIONS:</title>'
            '<p>Endoscopic retrograde cholangiopancreatography is a safe and useful method for the treatment of biliary complications of hepatic hydatid disease and should be considered the first-line procedure for biliary drainage in cases of cholangiohydatid disease involving secondary acute cholangitis.</p>'
            '</sec>'
            '</abstract>'
            '<trans-abstract xml:lang="pt">'
            '<title>RESUMO</title>'
            '<sec>'
            '<title>RACIONAL:</title>'
            '<p>A doença hidática, uma infestação parasitária causada pelas larvas de Echinococcus granulosus, é uma doença infecciosa endêmica em diferentes áreas como Índia, Austrália e América do Sul. O fígado é conhecido como o órgão mais comumente afetado pela hidatidose, podendo apresentar uma grande variedade de complicações como trânsito hidático hepato-torácico, superinfecção do cisto, disseminação intra-abdominal e comunicação do cisto biliar com extravasamento de material parasitário para o ducto biliar ou também chamada de colangio-hidatidose O ser humano é considerado um hospedeiro intermediário, exposto a essas larvas pela contaminação mão-boca das fezes de cães infectados.</p>'
            '</sec>'
            '<sec>'
            '<title>OBJETIVO:</title>'
            '<p>Destacar o papel da endoscópica por colangiopancreatografia retrógrada em pacientes com colangite aguda secundária à colangio-hidatidose.</p>'
            '</sec>'
            '<sec>'
            '<title>MÉTODOS:</title>'
            '<p>Considerando os achados de imagem, em paciente feminina de 36 anos de idade, com imagens de tomografia computadorizada e ressonância magnética mostrando uma lesão cística complexa no segmento hepático VI, com múltiplas vesículas internas e um defeito de parede cística que se comunica com a árvore biliar intra-hepática foi realizada drenagem biliar endoscópica por colangiopancreatografia retrógrada com papilotomia, levando à descarga de múltiplos cistos obstrutivos e areia hidática da via biliar principal.</p>'
            '</sec>'
            '<sec>'
            '<title>RESULTADOS:</title>'
            '<p>Os achados clínicos e laboratoriais melhoraram após a drenagem, com alta hospitalar sob tratamento antiparasitário oral antes da ressecção cirúrgica completa do cisto hidático hepático.</p>'
            '</sec>'
            '<sec>'
            '<title>CONCLUSÕES:</title>'
            '<p>A endoscópica por colangiopancreatografia retrógrada é um método seguro e útil para o tratamento das complicações biliares da hidatidose hepática, devendo ser considerado o procedimento de primeira linha para drenagem biliar nos casos de colangio-hidatidose que envolve colangite aguda secundária.</p>'
            '</sec>'
            '</trans-abstract>'
            '</article-meta>'
            '</front>'
            '</article>'
        )

        xml_pubmed_other_abstract(xml_pubmed, xml_tree)

        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")

        self.assertEqual(obtained, expected)


    def test_xml_pubmed_copyright(self):
        xml_tree = ET.fromstring(
            '<article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en"> '
            '<front>'
            '<article-meta>'
            '<permissions>'
            '<copyright-statement>Copyright © 2014 SciELO</copyright-statement>'
            '</permissions>'
            '</article-meta>'
            '</front>'
            '</article>'
        )
        xml_pubmed = ET.fromstring(
            '<ArticleSet>'
            '<Article/>'
            '</ArticleSet>'
        )

        expected = (
            '<ArticleSet>'
            '<Article>'
            '<CopyrightInformation>Copyright © 2014 SciELO</CopyrightInformation>'
            '</Article>'
            '</ArticleSet>'
        )
        xml_pubmed_copyright_information(xml_pubmed, xml_tree)
        obtained = ET.tostring(xml_pubmed, encoding="utf-8").decode("utf-8")
        
        self.assertEqual(obtained, expected)


class PipelinePubmedTest(unittest.TestCase):
    def test_pipeline_pubmed(self,):
        xml_file = ET.parse("/home/samuelv/Desktop/scielo/packtools/packtools/tests/sps/fixtures/formats/pubmed/S0066-782X2024000600303.xml")
        report = {}
        xml = pipeline_pubmed(xml_tree=xml_file, report=report)
        import ipdb; ipdb.set_trace()

if __name__ == '__main__':
    unittest.main()
