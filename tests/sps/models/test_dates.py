import unittest
from datetime import date
from unittest.mock import Mock, MagicMock, patch
from lxml import etree

from packtools.sps.models.dates import ArticleDates, Date, FulltextDates, get_days


class TestDate(unittest.TestCase):
    """Testes originais da classe Date"""
    
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
            "season": None,
            "type": "pub",
            "display": "2024-01-15",
            "is_complete": True,
            "parts": {"year": "2024", "season": None, "month": "01", "day": "15"},
        }
        self.assertEqual(date_obj.data, expected_data)

        # Test partial date
        partial_date_obj = Date(self.partial_date_node)
        expected_partial_data = {
            "year": "2024",
            "month": "01",
            "day": None,
            "season": None,
            "type": "pub",
            "display": "2024-01",
            "is_complete": False,
            "parts": {"year": "2024", "season": None, "month": "01", "day": None},
        }
        self.assertEqual(partial_date_obj.data, expected_partial_data)

    def test_str_representation(self):
        date_obj = Date(self.basic_date_node)
        self.assertEqual(str(date_obj), "2024-01-15")

        season_date_obj = Date(self.season_date_node)
        self.assertEqual(str(season_date_obj), "Spring/2024")

        partial_date_obj = Date(self.partial_date_node)
        self.assertEqual(str(partial_date_obj), "2024-01")

    def test_get_date_complete(self):
        """Testa get_date com data completa"""
        date_obj = Date(self.basic_date_node)
        result = date_obj.get_date()
        
        self.assertIn("date", result)
        self.assertNotIn("estimated", result)
        self.assertEqual(result["date"], date(2024, 1, 15))

    def test_get_date_missing_day(self):
        """Testa get_date com dia faltando"""
        date_obj = Date(self.partial_date_node)
        result = date_obj.get_date()
        
        self.assertIn("date", result)
        self.assertIn("estimated", result)
        self.assertTrue(result["estimated"])
        self.assertEqual(result["date"], date(2024, 1, 15))  # usa default_day=15

    def test_get_date_missing_month_and_day(self):
        """Testa get_date com mês e dia faltando"""
        node = etree.fromstring("<pub-date><year>2024</year></pub-date>")
        date_obj = Date(node)
        result = date_obj.get_date()
        
        self.assertIn("date", result)
        self.assertIn("estimated", result)
        self.assertTrue(result["estimated"])
        self.assertEqual(result["date"], date(2024, 6, 15))  # usa defaults

    def test_get_date_custom_defaults(self):
        """Testa get_date com valores padrão customizados"""
        node = etree.fromstring("<pub-date><year>2024</year></pub-date>")
        date_obj = Date(node)
        result = date_obj.get_date(default_day=1, default_month=12)
        
        self.assertIn("date", result)
        self.assertTrue(result["estimated"])
        self.assertEqual(result["date"], date(2024, 12, 1))

    def test_get_estimated_date_complete(self):
        """Testa get_estimated_date com data completa"""
        date_obj = Date(self.basic_date_node)
        result = date_obj.get_estimated_date()
        
        self.assertEqual(result, date(2024, 1, 15))

    def test_get_estimated_date_missing_day(self):
        """Testa get_estimated_date sem dia"""
        date_obj = Date(self.partial_date_node)
        result = date_obj.get_estimated_date(default_day=10)
        
        self.assertEqual(result, date(2024, 1, 10))

    def test_get_estimated_date_missing_month_and_day(self):
        """Testa get_estimated_date sem mês e dia"""
        node = etree.fromstring("<pub-date><year>2024</year></pub-date>")
        date_obj = Date(node)
        result = date_obj.get_estimated_date(default_day=25, default_month=8)
        
        self.assertEqual(result, date(2024, 8, 25))

    def test_get_estimated_date_invalid(self):
        """Testa get_estimated_date com data inválida"""
        date_obj = Date(self.invalid_date_node)
        result = date_obj.get_estimated_date()
        
        self.assertIsNone(result)


class TestArticleDates(unittest.TestCase):
    """Testes originais da classe ArticleDates"""
    
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
        # Verifica se a propriedade "data" e "history_dates_dict" estão disponíveis via delegação
        self.assertIsNotNone(self.article_dates.data)
        self.assertIsNotNone(self.article_dates.history_dates_dict)
        with self.assertRaises(AttributeError):
            _ = self.article_dates.nonexistent_attribute

    def test_fulltext_dates_iteration(self):
        dates = list(self.article_dates.fulltext_dates)
        self.assertEqual(len(dates), 3)  # Artigo principal + tradução + artigo suplementar

        # Testa datas do artigo principal
        main_dates = dates[0]
        self.assertIsNotNone(main_dates.epub_date)
        self.assertIsNotNone(main_dates.collection_date)

        # Testa datas da tradução
        translation_dates = dates[1]
        self.assertIsNotNone(translation_dates.epub_date)

        # Testa datas do artigo suplementar
        suppl_dates = dates[2]
        self.assertIsNotNone(suppl_dates.epub_date)


class TestFulltextDates(unittest.TestCase):
    """Testes originais da classe FulltextDates"""
    
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
                        <date date-type="accepted">
                            <year>2024</year>
                            <month>01</month>
                            <day>10</day>
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
        translations = self.fulltext_dates.data["translations"]
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
        not_translations = self.fulltext_dates.data["not_translations"]
        self.assertEqual(len(not_translations), 1)
        self.assertIn("s01pt", not_translations)

        report_dates = not_translations["s01pt"]
        self.assertEqual(report_dates["article_date"]["year"], "2024")
        self.assertEqual(report_dates["article_date"]["month"], "03")
        self.assertEqual(report_dates["article_date"]["day"], "01")

        parent_data = report_dates["parent"]
        self.assertEqual(parent_data["parent_article_type"], "reviewer-report")
        self.assertEqual(parent_data["parent_id"], "s01pt")
        self.assertEqual(parent_data["parent_lang"], "pt")

        history = self.fulltext_dates.data["history_dates_by_event"]
        self.assertIn("received", history)
        self.assertEqual(history["received"]["year"], "2023")
        self.assertEqual(history["received"]["month"], "12")
        self.assertEqual(history["received"]["day"], "01")
        self.assertIn("accepted", history)
        self.assertEqual(history["accepted"]["year"], "2024")
        self.assertEqual(history["accepted"]["month"], "01")
        self.assertEqual(history["accepted"]["day"], "10")

    def test_data_property(self):
        data = self.fulltext_dates.data
        self.assertIn("parent", data)
        self.assertIn("pub", data)
        self.assertIn("article_date", data)
        self.assertIn("collection_date", data)
        self.assertIn("history_dates", data)
        self.assertIn("translations", data)
        self.assertIn("not_translations", data)

        parent = data["parent"]
        self.assertEqual(parent["parent_lang"], "pt")
        self.assertEqual(parent["parent_article_type"], "research-article")

        translations = data["translations"]
        self.assertEqual(len(translations), 2)
        self.assertIn("en", translations)
        self.assertIn("es", translations)

        not_translations = data["not_translations"]
        self.assertEqual(len(not_translations), 1)
        self.assertIn("s01pt", not_translations)

    def test_items_property(self):
        items = list(self.fulltext_dates.items)
        self.assertEqual(len(items), 4)  # Artigo principal + 2 traduções + 1 artigo suplementar
        main_item = items[0]
        self.assertIn("pub", main_item)
        self.assertIn("article_date", main_item)
        self.assertIn("collection_date", main_item)
        self.assertIn("history_dates", main_item)
        parent = main_item["parent"]
        self.assertEqual(parent["parent_lang"], "pt")
        self.assertEqual(parent["parent_article_type"], "research-article")

    def test_get_peer_reviewed_stats_complete(self):
        """Testa get_peer_reviewed_stats com todas as datas"""
        stats = self.fulltext_dates.get_peer_reviewed_stats()
        
        self.assertEqual(stats["received_date"], date(2023, 12, 1))
        self.assertEqual(stats["accepted_date"], date(2024, 1, 10))
        self.assertEqual(stats["published_date"], date(2024, 1, 15))
        self.assertEqual(stats["days_from_received_to_accepted"], 40)
        self.assertEqual(stats["days_from_accepted_to_published"], 5)
        self.assertEqual(stats["days_from_received_to_published"], 45)
        self.assertFalse(stats.get("estimated_days_from_received_to_accepted", False))
        self.assertFalse(stats.get("estimated_days_from_accepted_to_published", False))
        self.assertFalse(stats.get("estimated_days_from_received_to_published", False))

    def test_get_peer_reviewed_stats_with_estimated_dates(self):
        """Testa get_peer_reviewed_stats com datas estimadas"""
        # Cria XML com datas parciais que precisarão de estimativa
        xml_with_partial_dates = """
        <article>
            <front>
                <article-meta>
                    <pub-date date-type="pub">
                        <year>2024</year>
                        <month>01</month>
                    </pub-date>
                    <history>
                        <date date-type="received">
                            <year>2023</year>
                            <month>12</month>
                        </date>
                        <date date-type="accepted">
                            <year>2024</year>
                            <month>01</month>
                            <day>10</day>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        xmltree = etree.fromstring(xml_with_partial_dates)
        fulltext = FulltextDates(xmltree.find("."))
        stats = fulltext.get_peer_reviewed_stats()
        
        # Verifica que as datas estimadas foram marcadas
        self.assertTrue(stats["estimated_days_from_received_to_accepted"])
        self.assertTrue(stats["estimated_days_from_accepted_to_published"])
        self.assertTrue(stats["estimated_days_from_received_to_published"])

    def test_get_peer_reviewed_stats_missing_dates(self):
        """Testa get_peer_reviewed_stats com datas faltando"""
        xml_no_history = """
        <article>
            <front>
                <article-meta>
                    <pub-date date-type="pub">
                        <year>2024</year>
                        <month>01</month>
                        <day>15</day>
                    </pub-date>
                </article-meta>
            </front>
        </article>
        """
        xmltree = etree.fromstring(xml_no_history)
        fulltext = FulltextDates(xmltree.find("."))
        stats = fulltext.get_peer_reviewed_stats()
        
        self.assertIsNone(stats["received_date"])
        self.assertIsNone(stats["accepted_date"])
        self.assertEqual(stats["published_date"], date(2024, 1, 15))
        self.assertIsNone(stats["days_from_received_to_accepted"])
        self.assertIsNone(stats["days_from_accepted_to_published"])
        self.assertIsNone(stats["days_from_received_to_published"])

    def test_get_peer_reviewed_stats_custom_defaults(self):
        """Testa get_peer_reviewed_stats com valores padrão customizados"""
        xml_with_partial = """
        <article>
            <front>
                <article-meta>
                    <history>
                        <date date-type="received">
                            <year>2023</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        xmltree = etree.fromstring(xml_with_partial)
        fulltext = FulltextDates(xmltree.find("."))
        stats = fulltext.get_peer_reviewed_stats(default_month=12, default_day=31)
        
        # Verifica que os valores padrão foram aplicados
        self.assertEqual(stats["received_date"], date(2023, 12, 31))
        self.assertTrue(stats.get("estimated_days_from_received_to_accepted") or 
                       stats.get("estimated_days_from_received_to_accepted") is None)


class TestGetDays(unittest.TestCase):
    """Testes para a função get_days"""
    
    def test_valid_dates(self):
        """Testa cálculo com datas válidas"""
        start = date(2024, 1, 1)
        end = date(2024, 1, 10)
        result = get_days(start, end)
        self.assertEqual(result, 9)
    
    def test_same_date(self):
        """Testa quando as datas são iguais"""
        start = date(2024, 1, 1)
        end = date(2024, 1, 1)
        result = get_days(start, end)
        self.assertEqual(result, 0)
    
    def test_negative_days(self):
        """Testa quando a data final é anterior à inicial"""
        start = date(2024, 1, 10)
        end = date(2024, 1, 1)
        result = get_days(start, end)
        self.assertEqual(result, -9)
    
    def test_none_start_date(self):
        """Testa com data inicial None"""
        end = date(2024, 1, 10)
        result = get_days(None, end)
        self.assertIsNone(result)
    
    def test_none_end_date(self):
        """Testa com data final None"""
        start = date(2024, 1, 1)
        result = get_days(start, None)
        self.assertIsNone(result)
    
    def test_both_none(self):
        """Testa com ambas as datas None"""
        result = get_days(None, None)
        self.assertIsNone(result)
    
    def test_invalid_types(self):
        """Testa com tipos inválidos"""
        result = get_days("2024-01-01", "2024-01-10")
        self.assertIsNone(result)
    
    def test_year_difference(self):
        """Testa cálculo com diferença de anos"""
        start = date(2023, 12, 31)
        end = date(2024, 1, 1)
        result = get_days(start, end)
        self.assertEqual(result, 1)
    
    def test_leap_year(self):
        """Testa cálculo incluindo ano bissexto"""
        start = date(2024, 2, 28)
        end = date(2024, 3, 1)
        result = get_days(start, end)
        self.assertEqual(result, 2)  # 2024 é bissexto
        
        start = date(2023, 2, 28)
        end = date(2023, 3, 1)
        result = get_days(start, end)
        self.assertEqual(result, 1)  # 2023 não é bissexto


if __name__ == '__main__':
    unittest.main()