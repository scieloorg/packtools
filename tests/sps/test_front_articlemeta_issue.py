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


from unittest import TestCase

from lxml import etree

from packtools.sps.models.front_articlemeta_issue import ArticleMetaIssue


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
            <suppl>B</suppl>
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
        expected = {"year": "2003", "type": "collection"}
        self.assertDictEqual(expected, self.issue.collection_date)

    def test_fpage_seq(self):
        self.assertEqual("A", self.issue.fpage_seq)

    def test_elocation_id(self):
        self.assertEqual("123", self.issue.elocation_id)

    def test_suppl(self):
        self.assertEqual("B", self.issue.suppl)

    def test_number(self):
        self.assertEqual("1", self.issue.number)


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
