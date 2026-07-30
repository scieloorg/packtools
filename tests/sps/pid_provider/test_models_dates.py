import unittest
from lxml import etree

from packtools.sps.pid_provider.models.dates import format_date, Date, ArticleDates, XMLWithPreArticlePublicationDateError


class TestFormatDate(unittest.TestCase):

    def test_format_date_sucesso(self):
        self.assertEqual(format_date(year="2022", month="4", day="5"), "2022-04-05")
        self.assertEqual(format_date(year=2022, month=12, day=20), "2022-12-20")

    def test_format_date_invalida_gera_excecao(self):
        # Fevereiro não tem dia 30
        with self.assertRaises(XMLWithPreArticlePublicationDateError) as cm:
            format_date(year="2022", month="02", day="30")
        
        self.assertIn("Unable to format_date", str(cm.exception))

    def test_format_date_tipos_invalidos_gera_excecao(self):
        with self.assertRaises(XMLWithPreArticlePublicationDateError):
            format_date(year=None, month="04", day="20")


class TestDateClass(unittest.TestCase):

    def test_date_com_date_type_explicito(self):
        node = etree.fromstring('<pub-date date-type="pub"><year>2022</year><day>01</day></pub-date>')
        d = Date(node)
        self.assertEqual(d.date_type, "pub")
        self.assertEqual(d.data, {"year": "2022", "day": "01", "type": "pub"})

    def test_date_inferir_pub_por_presenca_de_day(self):
        node = etree.fromstring('<pub-date><year>2022</year><day>10</day></pub-date>')
        d = Date(node)
        self.assertEqual(d.date_type, "pub")

    def test_date_inferir_collection_sem_day(self):
        node = etree.fromstring('<pub-date><year>2022</year></pub-date>')
        d = Date(node)
        self.assertEqual(d.date_type, "collection")

    def test_date_isoformat(self):
        node = etree.fromstring('<pub-date date-type="pub"><year>2022</year><month>4</month><day>20</day></pub-date>')
        d = Date(node)
        self.assertEqual(d.isoformat, "2022-04-20")


class TestArticleDatesClass(unittest.TestCase):

    def setUp(self):
        self.xml_str = """<article>
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
              <history>
                <date date-type="received">
                  <day>18</day>
                  <month>10</month>
                  <year>2002</year>
                </date>
                <date date-type="accepted">
                  <day>20</day>
                  <month>12</month>
                  <year>2002</year>
                </date>
              </history>
            </article-meta>
          </front>
        </article>
        """
        self.sample_xml = etree.fromstring(self.xml_str.encode('utf-8'))

    def test_article_date_e_epub_date(self):
        dates = ArticleDates(self.sample_xml)
        expected = {'year': '2022', 'month': '04', 'day': '20', 'type': 'pub'}
        
        self.assertEqual(dates.article_date, expected)
        self.assertEqual(dates.epub_date, expected)
        self.assertEqual(dates.article_year, "2022")

    def test_article_date_isoformat_sucesso(self):
        dates = ArticleDates(self.sample_xml)
        self.assertEqual(dates.article_date_isoformat, "2022-04-20")

    def test_article_date_isoformat_falha_levanta_excecao(self):
        # XML sem parâmetros necessários (day/month) para montar o isoformat
        xml = etree.fromstring('<article><front><pub-date date-type="pub"><year>2022</year></pub-date></front></article>')
        dates = ArticleDates(xml)
        
        with self.assertRaises(XMLWithPreArticlePublicationDateError):
            _ = dates.article_date_isoformat

    def test_collection_date_e_collection_year(self):
        dates = ArticleDates(self.sample_xml)
        expected = {'year': '2003', 'type': 'collection'}
        
        self.assertEqual(dates.collection_date, expected)
        self.assertEqual(dates.collection_year, "2003")

    def test_pub_dates_lista_todas_as_datas(self):
        dates = ArticleDates(self.sample_xml)
        result = dates.pub_dates
        
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0], {'year': '2022', 'month': '04', 'day': '20', 'type': 'pub'})
        self.assertEqual(result[1], {'year': '2003', 'type': 'collection'})

    def test_xml_sem_datas(self):
        xml_vazio = etree.fromstring('<article><front></front></article>')
        dates = ArticleDates(xml_vazio)

        self.assertIsNone(dates.article_date)
        self.assertIsNone(dates.article_year)
        self.assertIsNone(dates.collection_date)
        self.assertIsNone(dates.collection_year)
        self.assertEqual(dates.pub_dates, [])

    def test_xml_com_pub_type_alternativo(self):
        # Valida se as rotas de XPath com pub-type="epub" funcionam
        xml_alt = etree.fromstring('''
        <article>
            <front>
                <pub-date pub-type="epub"><year>2021</year><month>01</month><day>15</day></pub-date>
            </front>
        </article>
        ''')
        dates = ArticleDates(xml_alt)
        self.assertEqual(dates.article_year, "2021")
        self.assertEqual(dates.article_date_isoformat, "2021-01-15")


if __name__ == '__main__':
    unittest.main()