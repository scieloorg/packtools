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

from packtools.sps.models.dates import (
    ArticleDates,
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


class ArticleDatesCollectionFrom1_8Test(TestCase):

    def setUp(self):
        pub_dates = ("""
            <pub-date date-type="collection"><year>2023</year></pub-date>
        """)
        self.xmltree = etree.fromstring(_get_xml(pub_dates))
        self.xml_dates = ArticleDates(self.xmltree)

    def test_article_date_is_none(self):
        self.assertIsNone(self.xml_dates.article_date)

    def test_collection_date_year(self):
        self.assertEqual("2023", self.xml_dates.collection_date["year"])

    def test_collection_date_month(self):
        self.assertIsNone(self.xml_dates.collection_date.get("month"))


class ArticleDatesCollectionBefore1_8Test(TestCase):

    def setUp(self):
        pub_dates = ("""
            <pub-date pub-type="epub-ppub"><year>2023</year></pub-date>
        """)
        self.xmltree = etree.fromstring(_get_xml(pub_dates))
        self.xml_dates = ArticleDates(self.xmltree)

    def test_article_date_is_none(self):
        self.assertIsNone(self.xml_dates.article_date)

    def test_collection_date_year(self):
        self.assertEqual("2023", self.xml_dates.collection_date["year"])

    def test_collection_date_month(self):
        self.assertIsNone(self.xml_dates.collection_date.get("month"))


class ArticleDatesArticleFrom1_8Test(TestCase):

    def setUp(self):
        pub_dates = ("""
            <pub-date date-type="pub"><year>2023</year><month>02</month><day>20</day></pub-date>
        """)
        self.xmltree = etree.fromstring(_get_xml(pub_dates))
        self.xml_dates = ArticleDates(self.xmltree)

    def test_collection_date_is_none(self):
        self.assertIsNone(self.xml_dates.collection_date)

    def test_article_date_year(self):
        self.assertEqual("2023", self.xml_dates.article_date["year"])

    def test_article_date_month(self):
        self.assertEqual("02", self.xml_dates.article_date["month"])

    def test_article_date_day(self):
        self.assertEqual("20", self.xml_dates.article_date["day"])



class ArticleDatesArticleBefore1_8Test(TestCase):

    def setUp(self):
        pub_dates = ("""
            <pub-date pub-type="epub"><year>2023</year><month>02</month><day>20</day></pub-date>
        """)
        self.xmltree = etree.fromstring(_get_xml(pub_dates))
        self.xml_dates = ArticleDates(self.xmltree)

    def test_collection_date_is_none(self):
        self.assertIsNone(self.xml_dates.collection_date)

    def test_article_date_year(self):
        self.assertEqual("2023", self.xml_dates.article_date["year"])

    def test_article_date_month(self):
        self.assertEqual("02", self.xml_dates.article_date["month"])

    def test_article_date_day(self):
        self.assertEqual("20", self.xml_dates.article_date["day"])
