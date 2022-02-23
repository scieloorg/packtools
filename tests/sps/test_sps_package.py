
from packtools.sps.models.sps_package import (
    SPS_Package,
    Identity,
    SPS_Assets,
)
from packtools.sps.utils.xml_utils import (
    extract_number_and_supplment_from_issue_element,
    parse_issue,
    get_year_month_day,
    formatted_text
)
from packtools.sps.exceptions import NotAllowedtoChangeAttributeValueError

from unittest import TestCase, skip

from lxml import etree


class TestParseIssue(TestCase):
    """
    Estes testes são para explicitar a saída de
    parse_issue usando o contéudo de <issue></issue>
    """
    def test_parse_issue_for_5_parenteses_suppl(self):
        expected = "05-s0"
        result = parse_issue("5 (suppl)")
        self.assertEqual(expected, result)

    def test_parse_issue_for_5_Suppl(self):
        expected = "05-s0"
        result = parse_issue("5 Suppl")
        self.assertEqual(expected, result)

    def test_parse_issue_for_5_Suppl_1(self):
        expected = "05-s01"
        result = parse_issue("5 Suppl 1")
        self.assertEqual(expected, result)

    def test_parse_issue_for_5_spe(self):
        expected = "05-spe"
        result = parse_issue("5 spe")
        self.assertEqual(expected, result)

    def test_parse_issue_for_5_suppl(self):
        expected = "05-s0"
        result = parse_issue("5 suppl")
        self.assertEqual(expected, result)

    def test_parse_issue_for_5_suppl_1(self):
        expected = "05-s01"
        result = parse_issue("5 suppl 1")
        self.assertEqual(expected, result)

    def test_parse_issue_for_5_suppl_dot_1(self):
        expected = "05-s01"
        result = parse_issue("5 suppl. 1")
        self.assertEqual(expected, result)

    def test_parse_issue_for_25_Suppl_1(self):
        expected = "25-s01"
        result = parse_issue("25 Suppl 1")
        self.assertEqual(expected, result)

    def test_parse_issue_for_2_hyphen_5_suppl_1(self):
        expected = "2-5-s01"
        result = parse_issue("2-5 suppl 1")
        self.assertEqual(expected, result)

    def test_parse_issue_for_2spe(self):
        expected = "spe"
        result = parse_issue("2spe")
        self.assertEqual(expected, result)

    def test_parse_issue_for_Spe(self):
        expected = "spe"
        result = parse_issue("Spe")
        self.assertEqual(expected, result)

    def test_parse_issue_for_Supldot_1(self):
        expected = "s01"
        result = parse_issue("Supl. 1")
        self.assertEqual(expected, result)

    def test_parse_issue_for_Suppl(self):
        expected = "s0"
        result = parse_issue("Suppl")
        self.assertEqual(expected, result)

    def test_parse_issue_for_Suppl_12(self):
        expected = "s12"
        result = parse_issue("Suppl 12")
        self.assertEqual(expected, result)

    def test_parse_issue_for_s2(self):
        expected = "s2"
        result = parse_issue("s2")
        self.assertEqual(expected, result)

    def test_parse_issue_for_spe(self):
        expected = "spe"
        result = parse_issue("spe")
        self.assertEqual(expected, result)

    def test_parse_issue_for_special(self):
        expected = "spe"
        result = parse_issue("Especial")
        self.assertEqual(expected, result)

    def test_parse_issue_for_spe_1(self):
        expected = "spe01"
        result = parse_issue("spe 1")
        self.assertEqual(expected, result)

    def test_parse_issue_for_spe_pr(self):
        expected = "spepr"
        result = parse_issue("spe pr")
        self.assertEqual(expected, result)

    def test_parse_issue_for_spe2(self):
        expected = "spe"
        result = parse_issue("spe2")
        self.assertEqual(expected, result)

    def test_parse_issue_for_spedot2(self):
        expected = "spe"
        result = parse_issue("spe.2")
        self.assertEqual(expected, result)

    def test_parse_issue_for_supp_1(self):
        expected = "s01"
        result = parse_issue("supp 1")
        self.assertEqual(expected, result)

    def test_parse_issue_for_suppl(self):
        expected = "s0"
        result = parse_issue("suppl")
        self.assertEqual(expected, result)

    def test_parse_issue_for_suppl_1(self):
        expected = "s01"
        result = parse_issue("suppl 1")
        self.assertEqual(expected, result)

    def test_parse_issue_for_suppl_12(self):
        expected = "s12"
        result = parse_issue("suppl 12")
        self.assertEqual(expected, result)

    def test_parse_issue_for_suppl_1hyphen2(self):
        expected = "s1-2"
        result = parse_issue("suppl 1-2")
        self.assertEqual(expected, result)

    def test_parse_issue_for_suppldot_1(self):
        expected = "s01"
        result = parse_issue("suppl. 1")
        self.assertEqual(expected, result)

    @skip("Encontrado no sistema, porém fora do padrão aceitável")
    def test_parse_issue_for_spepr(self):
        expected = "spepr"
        result = parse_issue("spepr")
        self.assertEqual(expected, result)

    @skip("Encontrado no sistema, porém fora do padrão aceitável")
    def test_parse_issue_for_supp5_1(self):
        expected = "supp5-s01"
        result = parse_issue("supp5 1")
        self.assertEqual(expected, result)

    @skip("Encontrado no sistema, porém fora do padrão aceitável")
    def test_parse_issue_for_suppl_5_pr(self):
        expected = "5pr"
        result = parse_issue("suppl 5 pr")
        self.assertEqual(expected, result)


class TestSPSPackage(TestCase):
    """
    Estes testes são para explicitar a saída de
    SPS_Package.number e SPS_Package.supplement
    dado o valor de <issue></issue>
    """
    def get_sps_package(self, issue):
        xml_text = f"""
            <article><article-meta>
                <issue>{issue}</issue>
            </article-meta></article>
        """
        return SPS_Package(xml_text, "sps_package")

    def test_number_and_suppl_for_5_parenteses_suppl(self):
        expected = "5", "0"
        _sps_package = self.get_sps_package("5 (suppl)")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_5_Suppl(self):
        expected = "5", "0"
        _sps_package = self.get_sps_package("5 Suppl")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_5_Suppl_1(self):
        expected = "5", "1"
        _sps_package = self.get_sps_package("5 Suppl 1")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_5_spe(self):
        expected = "5spe", None
        _sps_package = self.get_sps_package("5 spe")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_5_suppl(self):
        expected = "5", "0"
        _sps_package = self.get_sps_package("5 suppl")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_5_suppl_1(self):
        expected = "5", "1"
        _sps_package = self.get_sps_package("5 suppl 1")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_5_suppl_dot_1(self):
        expected = "5", "1"
        _sps_package = self.get_sps_package("5 suppl. 1")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_25_Suppl_1(self):
        expected = "25", "1"
        _sps_package = self.get_sps_package("25 Suppl 1")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_2_hyphen_5_suppl_1(self):
        expected = "2-5", "1"
        _sps_package = self.get_sps_package("2-5 suppl 1")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_2spe(self):
        expected = "2spe", None
        _sps_package = self.get_sps_package("2spe")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_Spe(self):
        expected = "spe", None
        _sps_package = self.get_sps_package("Spe")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_Supldot_1(self):
        expected = None, "1"
        _sps_package = self.get_sps_package("Supl. 1")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_Suppl(self):
        expected = None, "0"
        _sps_package = self.get_sps_package("Suppl")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_Suppl_12(self):
        expected = None, "12"
        _sps_package = self.get_sps_package("Suppl 12")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_s2(self):
        expected = None, "2"
        _sps_package = self.get_sps_package("s2")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_spe(self):
        expected = "spe", None
        _sps_package = self.get_sps_package("spe")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_special(self):
        expected = "spe", None
        _sps_package = self.get_sps_package("Especial")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_spe_1(self):
        expected = "spe1", None
        _sps_package = self.get_sps_package("spe 1")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_spe_pr(self):
        expected = "spepr", None
        _sps_package = self.get_sps_package("spe pr")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_spe2(self):
        expected = "spe2", None
        _sps_package = self.get_sps_package("spe2")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_spedot2(self):
        expected = "spe2", None
        _sps_package = self.get_sps_package("spe.2")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    @skip("Encontrado no sistema, porém fora do padrão aceitável")
    def test_number_and_suppl_for_spepr(self):
        expected = "spepr", None
        _sps_package = self.get_sps_package("spepr")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_supp_1(self):
        expected = None, "1"
        _sps_package = self.get_sps_package("supp 1")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_suppl(self):
        expected = None, "0"
        _sps_package = self.get_sps_package("suppl")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_suppl_1(self):
        expected = None, "1"
        _sps_package = self.get_sps_package("suppl 1")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_suppl_12(self):
        expected = None, "12"
        _sps_package = self.get_sps_package("suppl 12")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_suppl_1hyphen2(self):
        expected = None, "1-2"
        _sps_package = self.get_sps_package("suppl 1-2")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    def test_number_and_suppl_for_suppldot_1(self):
        expected = None, "1"
        _sps_package = self.get_sps_package("suppl. 1")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    @skip("Encontrado no sistema, porém fora do padrão aceitável")
    def test_number_and_suppl_for_supp5_1(self):
        expected = "supp5", "1"
        _sps_package = self.get_sps_package("supp5 1")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)

    @skip("Encontrado no sistema, porém fora do padrão aceitável")
    def test_number_and_suppl_for_suppl_5_pr(self):
        expected = None, "5pr"
        _sps_package = self.get_sps_package("suppl 5 pr")
        result = _sps_package.number
        self.assertEqual(expected[0], result)
        result = _sps_package.supplement
        self.assertEqual(expected[1], result)


class TestExtractNumberAndSupplmentFromIssueElement(TestCase):
    """
    Extrai do conteúdo de <issue>xxxx</issue>, os valores number e suppl.
    Valores possíveis
    5 (suppl), 5 Suppl, 5 Suppl 1, 5 spe, 5 suppl, 5 suppl 1, 5 suppl. 1,
    25 Suppl 1, 2-5 suppl 1, 2spe, Spe, Supl. 1, Suppl, Suppl 12,
    s2, spe, spe 1, spe pr, spe2, spe.2, spepr, supp 1, supp5 1, suppl,
    suppl 1, suppl 5 pr, suppl 12, suppl 1-2, suppl. 1

    """
    def test_number_and_suppl_for_5_parenteses_suppl(self):
        expected = "5", "0"
        result = extract_number_and_supplment_from_issue_element("5 (suppl)")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_5_Suppl(self):
        expected = "5", "0"
        result = extract_number_and_supplment_from_issue_element("5 Suppl")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_5_Suppl_1(self):
        expected = "5", "1"
        result = extract_number_and_supplment_from_issue_element("5 Suppl 1")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_5_spe(self):
        expected = "5spe", None
        result = extract_number_and_supplment_from_issue_element("5 spe")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_5_suppl(self):
        expected = "5", "0"
        result = extract_number_and_supplment_from_issue_element("5 suppl")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_5_suppl_1(self):
        expected = "5", "1"
        result = extract_number_and_supplment_from_issue_element("5 suppl 1")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_5_suppl_dot_1(self):
        expected = "5", "1"
        result = extract_number_and_supplment_from_issue_element("5 suppl. 1")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_25_Suppl_1(self):
        expected = "25", "1"
        result = extract_number_and_supplment_from_issue_element("25 Suppl 1")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_2_hyphen_5_suppl_1(self):
        expected = "2-5", "1"
        result = extract_number_and_supplment_from_issue_element("2-5 suppl 1")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_2spe(self):
        expected = "2spe", None
        result = extract_number_and_supplment_from_issue_element("2spe")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_Spe(self):
        expected = "spe", None
        result = extract_number_and_supplment_from_issue_element("Spe")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_Supldot_1(self):
        expected = None, "1"
        result = extract_number_and_supplment_from_issue_element("Supl. 1")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_Suppl(self):
        expected = None, "0"
        result = extract_number_and_supplment_from_issue_element("Suppl")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_Suppl_12(self):
        expected = None, "12"
        result = extract_number_and_supplment_from_issue_element("Suppl 12")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_s2(self):
        expected = None, "2"
        result = extract_number_and_supplment_from_issue_element("s2")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_spe(self):
        expected = "spe", None
        result = extract_number_and_supplment_from_issue_element("spe")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_special(self):
        expected = "spe", None
        result = extract_number_and_supplment_from_issue_element("Especial")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_spe_1(self):
        expected = "spe1", None
        result = extract_number_and_supplment_from_issue_element("spe 1")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_spe_pr(self):
        expected = "spepr", None
        result = extract_number_and_supplment_from_issue_element("spe pr")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_spe2(self):
        expected = "spe2", None
        result = extract_number_and_supplment_from_issue_element("spe2")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_spedot2(self):
        expected = "spe2", None
        result = extract_number_and_supplment_from_issue_element("spe.2")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_supp_1(self):
        expected = None, "1"
        result = extract_number_and_supplment_from_issue_element("supp 1")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_suppl(self):
        expected = None, "0"
        result = extract_number_and_supplment_from_issue_element("suppl")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_suppl_1(self):
        expected = None, "1"
        result = extract_number_and_supplment_from_issue_element("suppl 1")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_suppl_12(self):
        expected = None, "12"
        result = extract_number_and_supplment_from_issue_element("suppl 12")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_suppl_1hyphen2(self):
        expected = None, "1-2"
        result = extract_number_and_supplment_from_issue_element("suppl 1-2")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_suppldot_1(self):
        expected = None, "1"
        result = extract_number_and_supplment_from_issue_element("suppl. 1")
        self.assertEqual(expected, result)

    @skip("Encontrado no sistema, porém fora do padrão aceitável")
    def test_number_and_suppl_for_spepr(self):
        expected = "spepr", None
        result = extract_number_and_supplment_from_issue_element("spepr")
        self.assertEqual(expected, result)

    @skip("Encontrado no sistema, porém fora do padrão aceitável")
    def test_number_and_suppl_for_supp5_1(self):
        expected = "supp5", "1"
        result = extract_number_and_supplment_from_issue_element("supp5 1")
        self.assertEqual(expected, result)

    @skip("Encontrado no sistema, porém fora do padrão aceitável")
    def test_number_and_suppl_for_suppl_5_pr(self):
        expected = None, "5pr"
        result = extract_number_and_supplment_from_issue_element("suppl 5 pr")
        self.assertEqual(expected, result)


class TestSPS_Package(TestCase):

    def setUp(self):
        self.xml_sps = SPS_Package("./tests/sps/fixtures/document.xml")
        self.xml_sps_3 = SPS_Package("./tests/sps/fixtures/document3.xml")

    def test_order(self):
        expected = 1
        result = self.xml_sps.order
        self.assertEqual(expected, result)

    def test_scielo_pid_v1(self):
        expected = None
        result = self.xml_sps.scielo_pid_v1
        self.assertEqual(expected, result)

    def test_set_scielo_pid_v1(self):
        expected = "v1"
        self.xml_sps.scielo_pid_v1 = "v1"
        self.assertEqual(expected, self.xml_sps.scielo_pid_v1)

    def test_scielo_pid_v2(self):
        expected = "S0036-36341997000100001"
        result = self.xml_sps.scielo_pid_v2
        self.assertEqual(expected, result)

    def test_set_scielo_pid_v2(self):
        with self.assertRaises(NotAllowedtoChangeAttributeValueError):
            self.xml_sps.scielo_pid_v2 = "xxxxx"

    def test_scielo_pid_v3(self):
        expected = None
        result = self.xml_sps.scielo_pid_v3
        self.assertEqual(expected, result)

    def test_set_scielo_pid_v3(self):
        expected = "V3"
        self.xml_sps.scielo_pid_v3 = "V3"
        self.assertEqual(expected, self.xml_sps.scielo_pid_v3)

    def test_aop_pid(self):
        expected = None
        result = self.xml_sps.aop_pid
        self.assertEqual(expected, result)

    def test_set_aop_pid(self):
        expected = "aoppid"
        self.xml_sps.aop_pid = "aoppid"
        self.assertEqual(expected, self.xml_sps.aop_pid)

    def test_doi(self):
        expected = '10.1590/S0036-36341997000100001'
        result = self.xml_sps.doi
        self.assertEqual(expected, result)

    def test_set_doi(self):
        expected = "doi"
        self.xml_sps.doi = "doi"
        self.assertEqual(expected, self.xml_sps.doi)

    def test_assets(self):
        expected = []
        result = self.xml_sps.assets.items
        self.assertEqual(expected, result)

    def test_document_pubdate(self):
        expected = ("1997", "01", "00")
        result = self.xml_sps.document_pubdate
        self.assertEqual(expected, result)

    def test_lang(self):
        expected = "es"
        result = self.xml_sps.lang
        self.assertEqual(expected, result)

    def test_article_type(self):
        expected = "editorial"
        result = self.xml_sps.article_type
        self.assertEqual(expected, result)

    def test_article_title(self):
        expected = "EDITORIAL <b>TEste</b> xdadfaf <math>xxx</math>"
        result = self.xml_sps.article_title
        self.assertEqual(expected, result)

    def test_article_titles(self):
        expected = {
            "es": "EDITORIAL <b>TEste</b> xdadfaf <math>xxx</math>"
        }
        result = self.xml_sps.article_titles
        self.assertEqual(expected, result)

    def test_abstract(self):
        expected = (
            "<p>Objective. The use of spirometric reference values specific to the "
            "population being tested is preferable. A study carried out in Puerto "
            "Rico is used here to develop nomograms for normal children and "
            "adolescents based on age and height, two variables that have been "
            "found to be good predictors of pulmonary function. Material and "
            "methods. The data for healthy individuals aged 5 to 18 were "
            "extracted (108 girls and 107 boys) from a larger study of "
            "spirometric measurements collected on 4 527 individuals attending "
            "medical services in Puerto Rico. Several models were tested for the "
            "prediction of FEV1, FVC and the ratio FEV1/FVC. The best models were "
            "selected for each gender, and <i>nomograms</i> were developed "
            "showing the fifth, twenty-fifth, fiftieth, seventy-fifth, and "
            "ninety-fifth percentile of the predicted values according to age and "
            "height separately. Results. The best models were those using the "
            "logarithm of the pulmonary function and the cube of height (R2= "
            "0.79-0.81), and age without transformation (R2= 0.73-0.77). "
            "Corresponding nomograms were developed based on these models. The "
            "ratio <sup>showed</sup> little variation for different ages and "
            "heights. Conclusions. Pulmonary function can be efficiently "
            "predicted by age and height. Nomograms provide a simple way to use "
            "spirometric references that can be incorporated to clinical practice."
            "</p>"
        )
        result = self.xml_sps_3.abstract
        self.assertEqual(expected, result)

    def test_abstracts(self):
        expected = {
            "es": (
                """<p>Objetivo. Desarrollar nomogramas espirométricos para niños y adolescentes portorriqueños, de acuerdo con edad y estatura. Material y métodos. Se extrajeron datos de individuos sanos de edades entre 5 y 18 años (108 niñas y 107 niños) de un estudio mayor, en el cual se recolectaron medidas espirométricas en 4 527 individuos que se presentaron en los servicios médicos en Puerto Rico. Se probaron varios modelos en la predicción del volumen de espiración forzada en un segundo (FEV1), de la capacidad vital forzada (CVF) y la razón VEF1/CVF. Se seleccionaron los mejores modelos para cada sexo y se desarrollaron los nomogramas mostrando los percentiles 5, 25, 50, 75 y 95 de los valores predichos por edad y estatura separadamente. Resultados. Los mejores modelos fueron aquellos con el logaritmo de la función pulmonar y el cubo de la estatura (R2= 0.79-0.81), y edad sin transformación (R2= 0.73-0.77); con base en estos se desarrollaron los nomogramas. La razón presentó poca variación entre las diferentes edades y estaturas. Conclusiones. La función pulmonar puede ser predicha eficientemente por la edad y la estatura. Los nomogramas permiten usar fácilmente los valores espirométricos de referencia incorporándolos en la práctica clínica.</p>"""
                ),
            "en": (
            "<p>Objective. The use of spirometric reference values specific to the "
            "population being tested is preferable. A study carried out in Puerto "
            "Rico is used here to develop nomograms for normal children and "
            "adolescents based on age and height, two variables that have been "
            "found to be good predictors of pulmonary function. Material and "
            "methods. The data for healthy individuals aged 5 to 18 were "
            "extracted (108 girls and 107 boys) from a larger study of "
            "spirometric measurements collected on 4 527 individuals attending "
            "medical services in Puerto Rico. Several models were tested for the "
            "prediction of FEV1, FVC and the ratio FEV1/FVC. The best models were "
            "selected for each gender, and <i>nomograms</i> were developed "
            "showing the fifth, twenty-fifth, fiftieth, seventy-fifth, and "
            "ninety-fifth percentile of the predicted values according to age and "
            "height separately. Results. The best models were those using the "
            "logarithm of the pulmonary function and the cube of height (R2= "
            "0.79-0.81), and age without transformation (R2= 0.73-0.77). "
            "Corresponding nomograms were developed based on these models. The "
            "ratio <sup>showed</sup> little variation for different ages and "
            "heights. Conclusions. Pulmonary function can be efficiently "
            "predicted by age and height. Nomograms provide a simple way to use "
            "spirometric references that can be incorporated to clinical practice."
            "</p>"
            )
        }
        result = self.xml_sps_3.abstracts
        self.assertEqual(expected['es'], result['es'])
        self.assertEqual(expected['en'], result['en'])

    def test_subject(self):
        expected = 'Original articles'
        result = self.xml_sps_3.subject
        self.assertEqual(expected, result)

    def test_subjects(self):
        expected = {'en': 'Original articles'}
        result = self.xml_sps_3.subjects
        self.assertEqual(expected, result)

    def test_article_ids(self):
        expected = {
            "v2": "S0036-36341997000100003",
            "v3": "JHVKpRBtgd47h5F6YDz6mSm",
            "other": [
                "S0036-36341997000100003",
            ]
        }
        result = self.xml_sps_3.article_ids
        for k, v in expected.items():
            with self.subTest(k):
                self.assertEqual(v, result[k])

    def test_authors(self):
        expected = [
            {
                "surname": "CHEN-MOK",
                "given_names": "MARIO",
                "orcid": None,
                "aff": "University of North Carolina",
            },
            {
                "surname": "BANGDIWALA",
                "given_names": "SHRIKANT I.",
                "orcid": None,
                "aff": "University of North Carolina",
            }
        ]
        result = self.xml_sps_3.authors
        self.assertEqual(expected, list(result))

    def test_affiliations(self):
        expected = {
            "aff01":
            "University of North Carolina"
        }
        result = self.xml_sps_3.affiliations
        self.assertEqual(expected, result)

    def test_languages(self):
        expected = ["es"]
        result = self.xml_sps.languages
        self.assertEqual(expected, result)

    def test_elocation_id(self):
        expected = None
        result = self.xml_sps.elocation_id
        self.assertEqual(expected, result)

    def test_fpage(self):
        expected = '11'
        result = self.xml_sps_3.fpage
        self.assertEqual(expected, result)

    def test_fpage_seq(self):
        expected = None
        result = self.xml_sps_3.fpage_seq
        self.assertEqual(expected, result)

    def test_lpage(self):
        expected = '15'
        result = self.xml_sps_3.lpage
        self.assertEqual(expected, result)

    def test_get_regular_abstract(self):
        result = self.xml_sps_3.get_regular_abstract(".//trans-abstract")
        self.assertEqual(None, result.get("abstract-type"))

    def test_assets_3(self):
        expected = [
            ('document3-xdadaf.jpg', etree.Element('graphic')),
        ]
        result = self.xml_sps_3.assets.items

        self.assertEqual(expected[0][0], result[0].filename)
        self.assertEqual(type(expected[0][1]), type(result[0].asset_node))


class Test_sps_package(TestCase):

    def test_get_year_month_day(self):
        expected = ("2020", "03", "01")
        root = etree.fromstring(
            "<root><date>"
            "<year>2020</year>"
            "<month>3</month>"
            "<day>1</day>"
            "</date></root>"
        )
        result = get_year_month_day(root.find("date"))
        self.assertEqual(expected, result)

    def test_formatted_text(self):
        expected = (
            "<p>"
            "Um teste <bold>2020</bold> ... <italic>3</italic>"
            "</p>"
        )
        root = etree.fromstring(
            "<root><p>"
            "Um teste <bold>2020</bold> ... <italic>3</italic>"
            "</p></root>"
        )
        result = formatted_text(root)
        self.assertEqual(expected, result)


class TestIdentity(TestCase):

    def setUp(self):
        self.xml_sps = SPS_Package(
            "./tests/sps/fixtures/document.xml")
        self.xml_sps_3 = SPS_Package(
            "./tests/sps/fixtures/document3.xml")
        self.identity = Identity(self.xml_sps._xmltree)
        self.identity_3 = Identity(self.xml_sps_3._xmltree)

    def test_package_name(self):
        expected = "0036-3634-spm-39-01-00001"
        result = self.identity.package_name
        self.assertEqual(expected, result)

    def test_package_name_3(self):
        expected = "0036-3634-spm-39-01-00011"
        result = self.identity_3.package_name
        self.assertEqual(expected, result)


class TestSPS_Assets(TestCase):

    def _create_assets(self, xml_text, v3="v3"):
        return SPS_Assets(SPS_Package(xml_text)._xmltree, v3)

    def test_assets_returns_alternatives(self):
        assets = self._create_assets(
        """<root xmlns:xlink="http://www.w3.org/1999/xlink">
            <article-meta><article-id pub-id-type="publisher-id" specific-use="scielo-v3">v3</article-id></article-meta>
            <fig id="f01">
               <label>Gráfico 1</label>
               <caption>
                  <title>Dominios compartidos por diputados y periodistas. Perfiles (junio 2018 – mayo 2019).</title>
               </caption>
               <alternatives>
               <graphic xlink:href="2318-0889-tinf-33-e200025-gf01.tif"/>
               <graphic xlink:href="2318-0889-tinf-33-e200025-gf01.jpg"/>
               <graphic xlink:href="2318-0889-tinf-33-e200025-gf01.png"/>
               </alternatives>
               <attrib>Fuente: Elaboración propia (2020).</attrib>
            </fig>
        </root>
        """)
        result = assets.items
        nodes = assets._xml_tree.xpath(
            ".//*[@xlink:href]",
            namespaces={"xlink": "http://www.w3.org/1999/xlink"}
            )
        expected = [
            {
                "xlink_href": "2318-0889-tinf-33-e200025-gf01.tif",
                "node": nodes[0],
                "uri": '',
                "tag": "fig",
                "id": "f01",
                "content_type": "",
                "suffix": "-gf01",
                "ext": ".tif",
            },
            {
                "xlink_href": "2318-0889-tinf-33-e200025-gf01.jpg",
                "node": nodes[1],
                "uri": '',
                "tag": "fig",
                "id": "f01",
                "content_type": "",
                "suffix": "-gf01",
                "ext": ".jpg",
            },
            {
                "xlink_href": "2318-0889-tinf-33-e200025-gf01.png",
                "node": nodes[2],
                "uri": '',
                "tag": "fig",
                "id": "f01",
                "content_type": "",
                "suffix": "-gf01",
                "ext": ".png",
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertEqual(item["uri"], result[i].uri)
                self.assertEqual(item["xlink_href"], result[i].filename)
                self.assertEqual(item["xlink_href"], result[i].xlink_href)
                self.assertEqual(item["tag"], result[i].tag)
                self.assertEqual(item["id"], result[i].id)
                self.assertEqual(item["content_type"], result[i].content_type)
                self.assertEqual(item["suffix"], result[i].suffix)
                self.assertEqual(item["ext"], result[i].ext)

    def test_assets_returns_2_figures(self):
        assets = self._create_assets(
        """<root xmlns:xlink="http://www.w3.org/1999/xlink">
            <article-meta><article-id pub-id-type="publisher-id" specific-use="scielo-v3">v3</article-id></article-meta>
            <fig id="f01">
               <label>Gráfico 1</label>
               <caption>
                  <title>Dominios compartidos por diputados y periodistas. Perfiles (junio 2018 – mayo 2019).</title>
               </caption>
               <graphic xlink:href="2318-0889-tinf-33-e200025-gf01.tif"/>
               <attrib>Fuente: Elaboración propia (2020).</attrib>
            </fig>
            <fig id="f02">
               <label>Gráfico 2</label>
               <caption>
                  <title>Dominios compartidos por diputados y periodistas. Veces (junio 2018 – mayo 2019).</title>
               </caption>
               <graphic xlink:href="2318-0889-tinf-33-e200025-gf02.tif"/>
               <attrib>Fuente: Elaboración propia (2020).</attrib>
            </fig>
        </root>
        """)
        result = assets.items
        nodes = assets._xml_tree.xpath(
            ".//*[@xlink:href]",
            namespaces={"xlink": "http://www.w3.org/1999/xlink"}
            )
        expected = [
            {
                "uri": "",
                "xlink_href": "2318-0889-tinf-33-e200025-gf01.tif",
                "node": nodes[0],
                "tag": "fig",
                "id": "f01",
                "content_type": "",
                "suffix": "-gf01",
                "ext": ".tif",
            },
            {
                "uri": "",
                "xlink_href": "2318-0889-tinf-33-e200025-gf02.tif",
                "node": nodes[1],
                "tag": "fig",
                "id": "f02",
                "content_type": "",
                "suffix": "-gf02",
                "ext": ".tif",
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertEqual(item["uri"], result[i].uri)
                self.assertEqual(item["xlink_href"], result[i].filename)
                self.assertEqual(item["xlink_href"], result[i].xlink_href)
                self.assertEqual(item["tag"], result[i].tag)
                self.assertEqual(item["id"], result[i].id)
                self.assertEqual(item["content_type"], result[i].content_type)
                self.assertEqual(item["suffix"], result[i].suffix)
                self.assertEqual(item["ext"], result[i].ext)

    def test_assets_returns_1_table(self):
        assets = self._create_assets(
        """<root xmlns:xlink="http://www.w3.org/1999/xlink">
            <article-meta><article-id pub-id-type="publisher-id" specific-use="scielo-v3">v3</article-id></article-meta>
            <table-wrap id="t01">
               <label>Gráfico 1</label>
               <caption>
                  <title>Dominios compartidos por diputados y periodistas. Perfiles (junio 2018 – mayo 2019).</title>
               </caption>
               <graphic xlink:href="2318-0889-tinf-33-e200025-gt01.tif"/>
               <attrib>Fuente: Elaboración propia (2020).</attrib>
            </table-wrap>
        </root>
        """)
        result = assets.items
        nodes = assets._xml_tree.xpath(
            ".//*[@xlink:href]",
            namespaces={"xlink": "http://www.w3.org/1999/xlink"}
            )
        expected = [
            {
                "xlink_href": "2318-0889-tinf-33-e200025-gt01.tif",
                "uri": '',
                "node": nodes[0],
                "tag": "table-wrap",
                "id": "t01",
                "content_type": "",
                "suffix": "-gt01",
                "ext": ".tif",
            },
        ]
        self.assertEqual(expected[0]["uri"], result[0].uri)
        self.assertEqual(expected[0]["xlink_href"], result[0].filename)
        self.assertEqual(expected[0]["xlink_href"], result[0].xlink_href)
        self.assertEqual(expected[0]["tag"], result[0].tag)
        self.assertEqual(expected[0]["id"], result[0].id)
        self.assertEqual(expected[0]["content_type"], result[0].content_type)
        self.assertEqual(expected[0]["suffix"], result[0].suffix)
        self.assertEqual(expected[0]["ext"], result[0].ext)

    def test_assets_returns_other_elements(self):
        assets = self._create_assets(
        """<root xmlns:xlink="http://www.w3.org/1999/xlink">
            <article-meta>
            <article-id pub-id-type="publisher-id"
            specific-use="scielo-v3">v3</article-id>
            </article-meta>
            <p>
               <inline-graphic xlink:href="2318-0889-tinf-33-e200025-g1.tif"/>
               <media xlink:href="2318-0889-tinf-33-e200025-g2.tif"/>
               <supplementary-material xlink:href="2318-0889-tinf-33-e200025-g3.tif"/>
               <inline-supplementary-material xlink:href="2318-0889-tinf-33-e200025-g4.tif"/>
            </p>
        </root>
        """)
        result = assets.items
        nodes = assets._xml_tree.xpath(
            ".//*[@xlink:href]",
            namespaces={"xlink": "http://www.w3.org/1999/xlink"}
            )
        expected = [
            {
                "xlink_href": "2318-0889-tinf-33-e200025-g1.tif",
                "node": nodes[0],
                "id": 1,
                "content_type": "",
                "suffix": "-g1",
                "ext": ".tif",
            },
            {
                "xlink_href": "2318-0889-tinf-33-e200025-g2.tif",
                "node": nodes[1],
                "id": 2,
                "content_type": "",
                "suffix": "-g2",
                "ext": ".tif",
            },
            {
                "xlink_href": "2318-0889-tinf-33-e200025-g3.tif",
                "node": nodes[2],
                "id": 3,
                "content_type": "",
                "suffix": "-g3",
                "ext": ".tif",
            },
            {
                "xlink_href": "2318-0889-tinf-33-e200025-g4.tif",
                "node": nodes[3],
                "id": 4,
                "content_type": "",
                "suffix": "-g4",
                "ext": ".tif",
            },
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertEqual(item["xlink_href"], result[i].xlink_href)
                self.assertEqual(item["node"], result[i].asset_node)
                self.assertEqual(item["id"], result[i]._id)
                self.assertEqual(item["content_type"], result[i].content_type)
                self.assertEqual(item["suffix"], result[i].suffix)
                self.assertEqual(item["ext"], result[i].ext)

    def test_assets_returns_empty_list(self):
        assets = self._create_assets(
        """<root xmlns:xlink="http://www.w3.org/1999/xlink">
            <article-meta>
            <article-id pub-id-type="publisher-id"
            specific-use="scielo-v3">v3</article-id>
            </article-meta>
            <p>
               <inline-graphic xlink:href="http://internet.net/2318-0889-tinf-33-e200025-g1.tif"/>
               <media xlink:href="http://internet.net/2318-0889-tinf-33-e200025-g2.tif"/>
               <supplementary-material xlink:href="http://internet.net/2318-0889-tinf-33-e200025-g3.tif"/>
               <inline-supplementary-material xlink:href="http://internet.net/2318-0889-tinf-33-e200025-g4.tif"/>
            </p>
        </root>
        """)
        result = assets.items
        nodes = assets._xml_tree.xpath(
            ".//*[@xlink:href]",
            namespaces={"xlink": "http://www.w3.org/1999/xlink"}
            )
        expected = []
        self.assertEqual(expected, result)


class TestRemoteToLocal(TestCase):

    def _create_xml_sps(self, xml_text):
        return SPS_Package(xml_text)

    def test_remote_to_local(self):
        xml_text = (
        """<root xmlns:xlink="http://www.w3.org/1999/xlink">
            <journal-meta>
                <journal-id pub-id-type="pub-id">tinf</journal-id>
                <issn pub-id-type="electronic">2318-0889</issn>
            </journal-meta>
            <article-meta>
            <volume>33</volume>
            <elocation-id>e200025</elocation-id>
            <article-id pub-id-type="publisher-id" specific-use="scielo-v3">PIDV3</article-id>
            </article-meta>
            <fig id="f01">
               <label>Gráfico 1</label>
               <caption>
                  <title>Dominios compartidos por diputados y periodistas. Perfiles (junio 2018 – mayo 2019).</title>
               </caption>
               <alternatives>
               <graphic xlink:href="https://minio.scielo.br/bla/bal/PIDV3/2318-0889-tinf-33-e200025-gf01.tif"/>
               <graphic xlink:href="https://minio.scielo.br/bla/bal/PIDV3/2318-0889-tinf-33-e200025-gf01.jpg"/>
               <graphic xlink:href="https://minio.scielo.br/bla/bal/PIDV3/2318-0889-tinf-33-e200025-gf01.png"/>
               </alternatives>
               <attrib>Fuente: Elaboración propia (2020).</attrib>
            </fig>
        </root>
        """)
        xml_sps = self._create_xml_sps(xml_text)
        xml_sps.assets.remote_to_local("2318-0889-tinf-33-e200025")
        expected = [
            ("https://minio.scielo.br/bla/bal/PIDV3/"
                "2318-0889-tinf-33-e200025-gf01.tif",
                "2318-0889-tinf-33-e200025-gf01.tif"),
            ("https://minio.scielo.br/bla/bal/PIDV3/"
                "2318-0889-tinf-33-e200025-gf01.jpg",
                "2318-0889-tinf-33-e200025-gf01.jpg"),
            ("https://minio.scielo.br/bla/bal/PIDV3/"
                "2318-0889-tinf-33-e200025-gf01.png",
                "2318-0889-tinf-33-e200025-gf01.png"),
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertEqual(
                    item[0], xml_sps.assets.items[i].uri
                )
                self.assertEqual(
                    item[1], xml_sps.assets.items[i].filename
                )
