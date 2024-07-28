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

from packtools.sps.models.article_dates import (
    ArticleDates,
    HistoryDates,
)

from packtools.sps.utils import xml_utils


def _get_xml(articlemeta_content=None):
    if articlemeta_content is None:
        articlemeta_content = """
            <pub-date publication-format="electronic" date-type="pub">
                <day>20</day>
                <month>04</month>
                <year>2022</year>
            </pub-date>
            <pub-date publication-format="electronic" date-type="collection">
                <year>2003</year>
            </pub-date>
            """
    return f"""
        <article>
        <front>
            <article-meta>
              {articlemeta_content}
            </article-meta>
          </front>
        </article>
        """


class ArticleDatesCollectionFrom1_8Test(TestCase):

    def setUp(self):
        pub_dates = """
            <pub-date date-type="collection"><year>2023</year></pub-date>
        """
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
        pub_dates = """
            <pub-date pub-type="epub-ppub"><year>2023</year></pub-date>
        """
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
        pub_dates = """
            <pub-date date-type="pub"><year>2023</year><month>02</month><day>20</day></pub-date>
        """
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
        pub_dates = """
            <pub-date pub-type="epub"><year>2023</year><month>02</month><day>20</day></pub-date>
        """
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


class ArticleDatesArticleBefore1_8EpubIncompleteTest(TestCase):

    def setUp(self):
        pub_dates = """
            <pub-date pub-type="epub"><year>2023</year><month>02</month></pub-date>
        """
        self.xmltree = etree.fromstring(_get_xml(pub_dates))
        self.xml_dates = ArticleDates(self.xmltree)

    def test_article_date_is_none(self):
        self.assertIsNone(self.xml_dates.article_date)

    def test_collection_date_year(self):
        self.assertEqual("2023", self.xml_dates.collection_date["year"])

    def test_collection_date_month(self):
        self.assertEqual("02", self.xml_dates.collection_date["month"])

    def test_collection_date_day(self):
        self.assertIsNone(self.xml_dates.collection_date.get("day"))


class HistoryDatesTest(TestCase):
    def test_article_history(self):
        self.maxDiff = None
        xml_history_date = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <pub-date date-type="pub" publication-format="electronic">
                            <day>01</day>
                            <month>01</month>
                            <year>2023</year>
                        </pub-date>
                        <pub-date date-type="collection" publication-format="electronic">
                        <year>2023</year>
                    </pub-date>
                        <history>
                            <date date-type="received">
                                <day>05</day>
                                <month>01</month>
                                <year>1998</year>
                            </date>
                            <date date-type="rev-request">
                                <day>14</day>
                                <month>03</month>
                                <year>1998</year>
                            </date>
                            <date date-type="rev-recd">
                                <day>24</day>
                                <month>05</month>
                                <year>1998</year>
                            </date>
                            <date date-type="accepted">
                                <day>06</day>
                                <month>06</month>
                                <year>1998</year>
                            </date>
                            <date date-type="corrected">
                                <day>01</day>
                                <month>06</month>
                                <year>2012</year>
                            </date>
                        </history>
                    </article-meta>
                </front>
            </article>
            """
        )

        obtained = list(HistoryDates(xml_history_date).history_dates())

        expected = [
            {
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                'article_date': {'day': '01', 'month': '01', 'type': 'pub', 'year': '2023'},
                'collection_date': {'type': 'collection', 'year': '2023'},
                "history": {
                    "accepted": {
                        "day": "06",
                        "month": "06",
                        "type": "accepted",
                        "year": "1998",
                    },
                    "corrected": {
                        "day": "01",
                        "month": "06",
                        "type": "corrected",
                        "year": "2012",
                    },
                    "received": {
                        "day": "05",
                        "month": "01",
                        "type": "received",
                        "year": "1998",
                    },
                    "rev-recd": {
                        "day": "24",
                        "month": "05",
                        "type": "rev-recd",
                        "year": "1998",
                    },
                    "rev-request": {
                        "day": "14",
                        "month": "03",
                        "type": "rev-request",
                        "year": "1998",
                    },
                }
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_subarticle_history(self):
        self.maxDiff = None
        xml_history_date = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <pub-date date-type="pub" publication-format="electronic">
                            <day>01</day>
                            <month>01</month>
                            <year>2023</year>
                        </pub-date>
                        <pub-date date-type="collection" publication-format="electronic">
                            <year>2023</year>
                        </pub-date>
                    </article-meta>
                </front>
                <sub-article article-type="translation" id="TRen" xml:lang="en">
		            <front-stub>
                        <history>
                            <date date-type="received">
                                <day>05</day>
                                <month>01</month>
                                <year>1998</year>
                            </date>
                            <date date-type="rev-request">
                                <day>14</day>
                                <month>03</month>
                                <year>1998</year>
                            </date>
                            <date date-type="rev-recd">
                                <day>24</day>
                                <month>05</month>
                                <year>1998</year>
                            </date>
                            <date date-type="accepted">
                                <day>06</day>
                                <month>06</month>
                                <year>1998</year>
                            </date>
                            <date date-type="corrected">
                                <day>01</day>
                                <month>06</month>
                                <year>2012</year>
                            </date>
                        </history>
                    </front-stub>
                </sub-article>
            </article>
            """
        )

        obtained = list(HistoryDates(xml_history_date).history_dates())

        expected = [
            {
                "parent": "sub-article",
                "parent_article_type": "translation",
                "parent_id": "TRen",
                "parent_lang": "en",
                'article_date': {'day': '01', 'month': '01', 'type': 'pub', 'year': '2023'},
                'collection_date': {'type': 'collection', 'year': '2023'},
                "history": {
                    "accepted": {
                        "day": "06",
                        "month": "06",
                        "type": "accepted",
                        "year": "1998",
                    },
                    "corrected": {
                        "day": "01",
                        "month": "06",
                        "type": "corrected",
                        "year": "2012",
                    },
                    "received": {
                        "day": "05",
                        "month": "01",
                        "type": "received",
                        "year": "1998",
                    },
                    "rev-recd": {
                        "day": "24",
                        "month": "05",
                        "type": "rev-recd",
                        "year": "1998",
                    },
                    "rev-request": {
                        "day": "14",
                        "month": "03",
                        "type": "rev-request",
                        "year": "1998",
                    },
                }
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_reviews_as_sub_article(self):
        self.maxDiff = None
        xml_history_date = xml_utils.get_xml_tree('tests/samples/artigo-com-traducao-e-pareceres-traduzidos.xml')

        obtained = list(HistoryDates(xml_history_date).history_dates())

        expected = [
            {
                'article_date': {'day': '09', 'month': '05', 'type': 'pub', 'year': '2023'},
                'collection_date': {'season': 'Apr-Jun', 'type': 'collection', 'year': '2023'},
                'history': {
                    'accepted': {
                        'day': '13',
                        'month': '03',
                        'type': 'accepted',
                        'year': '2023'
                    },
                    'received': {
                        'day': '16',
                        'month': '09',
                        'type': 'received',
                        'year': '2022'
                    }
                },
                'parent': 'article',
                'parent_article_type': 'research-article',
                'parent_id': None,
                'parent_lang': 'pt'
            },
            {
                'article_date': {'day': '09', 'month': '05', 'type': 'pub', 'year': '2023'},
                'collection_date': {'season': 'Apr-Jun', 'type': 'collection', 'year': '2023'},
                'history': {
                    'reviewer-report-received': {
                        'day': '11',
                        'month': '12',
                        'type': 'reviewer-report-received',
                        'year': '2022'
                    }
                },
                'parent': 'sub-article',
                'parent_article_type': 'reviewer-report',
                'parent_id': 's2',
                'parent_lang': 'pt'
            },
            {
                'article_date': {'day': '09', 'month': '05', 'type': 'pub', 'year': '2023'},
                'collection_date': {'season': 'Apr-Jun', 'type': 'collection', 'year': '2023'},
                'history': {
                    'reviewer-report-received': {
                        'day': '24',
                        'month': '12',
                        'type': 'reviewer-report-received',
                        'year': '2022'
                    }
                },
                'parent': 'sub-article',
                'parent_article_type': 'reviewer-report',
                'parent_id': 's3',
                'parent_lang': 'pt'
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)