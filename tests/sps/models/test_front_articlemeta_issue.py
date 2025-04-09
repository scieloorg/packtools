"""<article>
<front>
    <article-meta>
      <pub-date publication-format="electronic" date-type="pub">
        <day>20</day>
        <month>04</month>
        <year>2022</year>
      </pub-date>
      <pub-date publication-format="electronic" date-type="collection">
        <year>2003</year>
      </pub-date>
      <volume>4</volume>
      <issue>1</issue>
      <fpage>108</fpage>
      <lpage>123</lpage>
    </article-meta>
  </front>
</article>
"""


from unittest import TestCase, skip

from lxml import etree

from packtools.sps.models.front_articlemeta_issue import (
    ArticleMetaIssue,
    extract_number_and_supplement_from_issue_element,
)


def _get_xml(articlemeta_content=None):
    if articlemeta_content is None:
        articlemeta_content = (
            """
            <pub-date publication-format="electronic" date-type="pub">
                <day>20</day>
                <month>04</month>
                <year>2022</year>
            </pub-date>
            <pub-date publication-format="electronic" date-type="collection">
                <year>2003</year>
            </pub-date>
            <volume>4</volume>
            <issue>1</issue>
            <supplement>B</supplement>
            <fpage seq="A">108</fpage>
            <lpage>123</lpage>
            <elocation-id>123</elocation-id>
            """
        )
    return (
        f"""
        <article>
        <front>
            <article-meta>
              {articlemeta_content}
            </article-meta>
          </front>
        </article>
        """
    )


class ArticleMetaIssueTest(TestCase):

    def setUp(self):
        self.xmltree = etree.fromstring(_get_xml())
        self.issue = ArticleMetaIssue(self.xmltree)

    def test_volume(self):
        self.assertEqual("4", self.issue.volume)

    def test_issue(self):
        self.assertEqual("1", self.issue.issue)

    def test_fpage(self):
        self.assertEqual("108", self.issue.fpage)

    def test_lpage(self):
        self.assertEqual("123", self.issue.lpage)

    def test_collection_date(self):
        expected = {
            'display': '2003',
            'is_complete': False,
            'parts': {'day': None, 'month': None, 'season': None, 'year': '2003'},
            'type': 'collection',
            'year': '2003'
        }

        self.assertDictEqual(expected, self.issue.collection_date)

    def test_fpage_seq(self):
        self.assertEqual("A", self.issue.fpage_seq)

    def test_elocation_id(self):
        self.assertEqual("123", self.issue.elocation_id)

    def test_suppl(self):
        self.assertEqual("B", self.issue.suppl)

    def test_number(self):
        self.assertEqual("1", self.issue.number)

    def test_data(self):
        expected = {
            "volume": "4",
            "number": "1",
            "suppl": "B",
            "fpage": "108",
            "fpage_seq": "A",
            "lpage": "123",
            "elocation_id": "123",
            "pub_year": "2003",
        }
        self.assertEqual(expected, self.issue.data)


class ArticleMetaIssueWithAbsentDataTest(TestCase):

    def setUp(self):
        self.xmltree = etree.fromstring(_get_xml(""))
        self.issue = ArticleMetaIssue(self.xmltree)

    def test_volume(self):
        self.assertIsNone(self.issue.volume)

    def test_issue(self):
        self.assertIsNone(self.issue.issue)

    def test_fpage(self):
        self.assertIsNone(self.issue.fpage)

    def test_lpage(self):
        self.assertIsNone(self.issue.lpage)

    def test_collection_date(self):
        self.assertIsNone(self.issue.collection_date)

    def test_fpage_seq(self):
        self.assertIsNone(self.issue.fpage_seq)

    def test_elocation_id(self):
        self.assertIsNone(self.issue.elocation_id)

    def test_suppl(self):
        self.assertIsNone(self.issue.suppl)

    def test_number(self):
        self.assertIsNone(self.issue.number)

    def test_data(self):
        expected = {}
        self.assertEqual(expected, self.issue.data)


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
        result = extract_number_and_supplement_from_issue_element("5 (suppl)")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_5_Suppl(self):
        expected = "5", "0"
        result = extract_number_and_supplement_from_issue_element("5 Suppl")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_5_Suppl_1(self):
        expected = "5", "1"
        result = extract_number_and_supplement_from_issue_element("5 Suppl 1")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_5_spe(self):
        expected = "5spe", None
        result = extract_number_and_supplement_from_issue_element("5 spe")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_5_suppl(self):
        expected = "5", "0"
        result = extract_number_and_supplement_from_issue_element("5 suppl")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_5_suppl_1(self):
        expected = "5", "1"
        result = extract_number_and_supplement_from_issue_element("5 suppl 1")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_5_suppl_dot_1(self):
        expected = "5", "1"
        result = extract_number_and_supplement_from_issue_element("5 suppl. 1")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_25_Suppl_1(self):
        expected = "25", "1"
        result = extract_number_and_supplement_from_issue_element("25 Suppl 1")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_2_hyphen_5_suppl_1(self):
        expected = "2-5", "1"
        result = extract_number_and_supplement_from_issue_element("2-5 suppl 1")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_2spe(self):
        expected = "2spe", None
        result = extract_number_and_supplement_from_issue_element("2spe")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_Spe(self):
        expected = "spe", None
        result = extract_number_and_supplement_from_issue_element("Spe")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_Supldot_1(self):
        expected = None, "1"
        result = extract_number_and_supplement_from_issue_element("Supl. 1")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_Suppl(self):
        expected = None, "0"
        result = extract_number_and_supplement_from_issue_element("Suppl")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_Suppl_12(self):
        expected = None, "12"
        result = extract_number_and_supplement_from_issue_element("Suppl 12")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_s2(self):
        expected = None, "2"
        result = extract_number_and_supplement_from_issue_element("s2")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_spe(self):
        expected = "spe", None
        result = extract_number_and_supplement_from_issue_element("spe")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_special(self):
        expected = "spe", None
        result = extract_number_and_supplement_from_issue_element("Especial")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_spe_1(self):
        expected = "spe1", None
        result = extract_number_and_supplement_from_issue_element("spe 1")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_spe_pr(self):
        expected = "spepr", None
        result = extract_number_and_supplement_from_issue_element("spe pr")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_spe2(self):
        expected = "spe2", None
        result = extract_number_and_supplement_from_issue_element("spe2")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_spedot2(self):
        expected = "spe2", None
        result = extract_number_and_supplement_from_issue_element("spe.2")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_supp_1(self):
        expected = None, "1"
        result = extract_number_and_supplement_from_issue_element("supp 1")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_suppl(self):
        expected = None, "0"
        result = extract_number_and_supplement_from_issue_element("suppl")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_suppl_1(self):
        expected = None, "1"
        result = extract_number_and_supplement_from_issue_element("suppl 1")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_suppl_12(self):
        expected = None, "12"
        result = extract_number_and_supplement_from_issue_element("suppl 12")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_suppl_1hyphen2(self):
        expected = None, "1-2"
        result = extract_number_and_supplement_from_issue_element("suppl 1-2")
        self.assertEqual(expected, result)

    def test_number_and_suppl_for_suppldot_1(self):
        expected = None, "1"
        result = extract_number_and_supplement_from_issue_element("suppl. 1")
        self.assertEqual(expected, result)

    @skip("Encontrado no sistema, porém fora do padrão aceitável")
    def test_number_and_suppl_for_spepr(self):
        expected = "spepr", None
        result = extract_number_and_supplement_from_issue_element("spepr")
        self.assertEqual(expected, result)

    @skip("Encontrado no sistema, porém fora do padrão aceitável")
    def test_number_and_suppl_for_supp5_1(self):
        expected = "supp5", "1"
        result = extract_number_and_supplement_from_issue_element("supp5 1")
        self.assertEqual(expected, result)

    @skip("Encontrado no sistema, porém fora do padrão aceitável")
    def test_number_and_suppl_for_suppl_5_pr(self):
        expected = None, "5pr"
        result = extract_number_and_supplement_from_issue_element("suppl 5 pr")
        self.assertEqual(expected, result)