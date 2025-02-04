from datetime import date
from unittest import TestCase, skip

from lxml import etree

from packtools.sps.models.dates import ArticleDates, Date, FulltextDates


class TestDate(TestCase):
    def setUp(self):
        # Basic date XML
        self.basic_date_xml = """
            <pub-date date-type="pub">
                <year>2024</year>
                <month>01</month>
                <day>15</day>
            </pub-date>
        """
        self.basic_date_node = etree.fromstring(self.basic_date_xml)

        # Season date XML
        self.season_date_xml = """
            <pub-date date-type="collection">
                <year>2024</year>
                <season>Spring</season>
            </pub-date>
        """
        self.season_date_node = etree.fromstring(self.season_date_xml)

        # Partial date XML (missing day)
        self.partial_date_xml = """
            <pub-date pub-type="epub">
                <year>2024</year>
                <month>01</month>
            </pub-date>
        """
        self.partial_date_node = etree.fromstring(self.partial_date_xml)

        # Invalid date XML
        self.invalid_date_xml = """
            <pub-date date-type="pub">
                <year>2024</year>
                <month>13</month>
                <day>32</day>
            </pub-date>
        """
        self.invalid_date_node = etree.fromstring(self.invalid_date_xml)

    def test_basic_date_initialization(self):
        date_obj = Date(self.basic_date_node)
        self.assertEqual(date_obj.year, "2024")
        self.assertEqual(date_obj.month, "01")
        self.assertEqual(date_obj.day, "15")
        self.assertEqual(date_obj.type, "pub")
        self.assertIsNone(date_obj.season)

    def test_season_date_initialization(self):
        date_obj = Date(self.season_date_node)
        self.assertEqual(date_obj.year, "2024")
        self.assertEqual(date_obj.season, "Spring")
        self.assertEqual(date_obj.type, "collection")
        self.assertIsNone(date_obj.month)
        self.assertIsNone(date_obj.day)

    def test_pub_type_initialization(self):
        date_obj = Date(self.partial_date_node)
        self.assertEqual(date_obj.type, "pub")

        # Test default collection type
        node = etree.fromstring("<pub-date><year>2024</year></pub-date>")
        date_obj = Date(node)
        self.assertEqual(date_obj.type, "collection")

    def test_date_data_property(self):
        date_obj = Date(self.basic_date_node)
        expected_data = {
            "year": "2024",
            "month": "01",
            "day": "15",
            "type": "pub",
            "display": "2024-01-15",
            "is_complete": True,
        }
        self.assertEqual(date_obj.data, expected_data)

        # Test partial date
        partial_date_obj = Date(self.partial_date_node)
        expected_partial_data = {
            "year": "2024",
            "month": "01",
            "type": "pub",
            "display": "2024-01",
            "is_complete": False,
        }
        self.assertEqual(partial_date_obj.data, expected_partial_data)

    def test_str_representation(self):
        date_obj = Date(self.basic_date_node)
        self.assertEqual(str(date_obj), "2024-01-15")

        season_date_obj = Date(self.season_date_node)
        self.assertEqual(str(season_date_obj), "Spring/2024")

        partial_date_obj = Date(self.partial_date_node)
        self.assertEqual(str(partial_date_obj), "2024-01")


class TestArticleDates(TestCase):
    def setUp(self):
        self.article_xml = """
        <article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <pub-date date-type="pub">
                        <year>2024</year>
                        <month>01</month>
                        <day>15</day>
                    </pub-date>
                    <pub-date date-type="collection">
                        <year>2024</year>
                        <month>03</month>
                    </pub-date>
                    <history>
                        <date date-type="received">
                            <year>2023</year>
                            <month>12</month>
                            <day>01</day>
                        </date>
                    </history>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="en" xml:lang="en">
                <front-stub>
                    <pub-date date-type="pub">
                        <year>2024</year>
                        <month>02</month>
                        <day>01</day>
                    </pub-date>
                </front-stub>
            </sub-article>
            <sub-article article-type="reviewer-report" id="suppl1" xml:lang="en">
                <front-stub>
                    <pub-date date-type="pub">
                        <year>2024</year>
                        <month>03</month>
                        <day>01</day>
                    </pub-date>
                    <history>
                        <date date-type="received">
                            <year>2024</year>
                            <month>01</month>
                            <day>20</day>
                        </date>
                        <date date-type="rev-recd">
                            <year>2024</year>
                            <month>02</month>
                            <day>15</day>
                        </date>
                        <date date-type="rev-request">
                            <year>2024</year>
                            <month>01</month>
                            <day>25</day>
                        </date>
                        <date date-type="accepted">
                            <year>2024</year>
                            <month>02</month>
                            <day>20</day>
                        </date>
                    </history>
                </front-stub>
            </sub-article>
        </article>
        """
        self.xmltree = etree.fromstring(self.article_xml)
        self.article_dates = ArticleDates(self.xmltree)

    def test_attribute_delegation(self):
        self.assertIsNotNone(self.article_dates.dates)
        self.assertIsNotNone(self.article_dates.history_dates_dict)

        with self.assertRaises(AttributeError):
            self.article_dates.nonexistent_attribute

    def test_fulltext_dates_iteration(self):
        dates = list(self.article_dates.fulltext_dates)
        self.assertEqual(
            len(dates), 3
        )  # Main article + translation + supplementary

        # Test main article dates
        main_dates = dates[0]
        self.assertIsNotNone(main_dates.epub_date)
        self.assertIsNotNone(main_dates.collection_date)

        # Test translation dates
        translation_dates = dates[1]
        self.assertIsNotNone(translation_dates.epub_date)

        # Test supplementary article dates
        suppl_dates = dates[2]
        self.assertIsNotNone(suppl_dates.epub_date)


class TestFulltextDates(TestCase):
    def setUp(self):
        self.article_xml = """
        <article article-type="research-article" xml:lang="pt">
            <front>
                <article-meta>
                    <pub-date date-type="pub">
                        <year>2024</year>
                        <month>01</month>
                        <day>15</day>
                    </pub-date>
                    <pub-date date-type="collection">
                        <year>2024</year>
                        <month>03</month>
                    </pub-date>
                    <history>
                        <date date-type="received">
                            <year>2023</year>
                            <month>12</month>
                            <day>01</day>
                        </date>
                    </history>
                </article-meta>
            </front>
            <sub-article article-type="translation" id="en" xml:lang="en">
                <front-stub>
                    <pub-date date-type="pub">
                        <year>2024</year>
                        <month>02</month>
                        <day>01</day>
                    </pub-date>
                </front-stub>
            </sub-article>
            <sub-article article-type="translation" id="es" xml:lang="es">
                <front-stub>
                    <pub-date date-type="pub">
                        <year>2024</year>
                        <month>02</month>
                        <day>15</day>
                    </pub-date>
                </front-stub>
            </sub-article>
            <sub-article article-type="reviewer-report" id="s01pt" xml:lang="pt">
                <front-stub>
                    <pub-date date-type="pub">
                        <year>2024</year>
                        <month>03</month>
                        <day>01</day>
                    </pub-date>
                    <history>
                        <date date-type="received">
                            <year>2024</year>
                            <month>11</month>
                            <day>20</day>
                        </date>
                    </history>
                </front-stub>
            </sub-article>
        </article>
        """
        self.xmltree = etree.fromstring(self.article_xml)
        self.fulltext_dates = FulltextDates(self.xmltree.find("."))

    def test_translations_property(self):
        translations = self.fulltext_dates.data["translations_data"]
        self.assertEqual(len(translations), 2)
        self.assertIn("en", translations)
        self.assertIn("es", translations)

        en_dates = translations["en"]
        self.assertEqual(en_dates["article_date"]["year"], "2024")
        self.assertEqual(en_dates["article_date"]["month"], "02")
        self.assertEqual(en_dates["article_date"]["day"], "01")

        parent_data = en_dates["parent"]
        self.assertEqual(parent_data["parent_lang"], "en")
        self.assertEqual(parent_data["parent_article_type"], "translation")
        self.assertEqual(parent_data["parent_id"], "en")

    def test_not_translations_property(self):
        not_translations = self.fulltext_dates.data["not_translations_data"]
        self.assertEqual(len(not_translations), 1)
        self.assertIn("s01pt", not_translations)

        # Test reviewer report dates
        report_dates = not_translations["s01pt"]

        # Test publication date
        self.assertEqual(report_dates["article_date"]["year"], "2024")
        self.assertEqual(report_dates["article_date"]["month"], "03")
        self.assertEqual(report_dates["article_date"]["day"], "01")

        # Test parent metadata
        parent_data = report_dates["parent"]
        self.assertEqual(parent_data["parent_article_type"], "reviewer-report")
        self.assertEqual(parent_data["parent_id"], "s01pt")
        self.assertEqual(parent_data["parent_lang"], "pt")

        # Test history dates
        history = self.fulltext_dates.data["history_dates_by_event"]

        # Test received date
        self.assertIn("received", history)
        self.assertEqual(history["received"]["year"], "2023")
        self.assertEqual(history["received"]["month"], "12")
        self.assertEqual(history["received"]["day"], "01")

        # Test review received date
        self.assertNotIn("rev-recd", history)
        # Test review request date
        self.assertNotIn("rev-request", history)

        # Test accepted date
        self.assertNotIn("accepted", history)

    def test_data_property(self):
        data = self.fulltext_dates.data

        # Test main structure
        self.assertIn("parent", data)
        self.assertIn("pub", data)
        self.assertIn("article_date", data)
        self.assertIn("collection_date", data)
        self.assertIn("history_dates", data)
        self.assertIn("translations_data", data)
        self.assertIn("not_translations_data", data)

        # Test parent data
        parent = data["parent"]
        self.assertEqual(parent["parent_lang"], "pt")
        self.assertEqual(parent["parent_article_type"], "research-article")

        # Test translations data
        translations = data["translations_data"]
        self.assertEqual(len(translations), 2)
        self.assertIn("en", translations)
        self.assertIn("es", translations)

        # Test non-translations data
        not_translations = data["not_translations_data"]
        self.assertEqual(len(not_translations), 1)
        self.assertIn("s01pt", not_translations)

    def test_items_property(self):
        items = list(self.fulltext_dates.items)
        self.assertEqual(
            len(items), 4
        )  # Main + 2 translations + 1 supplementary

        # Test main article data
        main_item = items[0]
        self.assertIn("pub", main_item)
        self.assertIn("article_date", main_item)
        self.assertIn("collection_date", main_item)
        self.assertIn("history_dates", main_item)

        # Test parent data
        parent = main_item["parent"]
        self.assertEqual(parent["parent_lang"], "pt")
        self.assertEqual(parent["parent_article_type"], "research-article")
