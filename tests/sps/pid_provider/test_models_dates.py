import unittest
from unittest import TestCase
from unittest.mock import patch

from lxml import etree
from packtools.sps.pid_provider.models.dates import (
    ArticleDates,
    Date,
    XMLWithPreArticlePublicationDateError,
    format_date,
)
from packtools.sps.pid_provider.xml_sps_lib import (
    XMLWithPre,
)


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
        node = etree.fromstring(
            '<pub-date date-type="pub"><year>2022</year><day>01</day></pub-date>'
        )
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
        node = etree.fromstring(
            '<pub-date date-type="pub"><year>2022</year><month>4</month><day>20</day></pub-date>'
        )
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
        self.sample_xml = etree.fromstring(self.xml_str.encode("utf-8"))

    def test_article_date_e_epub_date(self):
        dates = ArticleDates(self.sample_xml)
        expected = {"year": "2022", "month": "04", "day": "20", "type": "pub"}

        self.assertEqual(dates.article_date, expected)
        self.assertEqual(dates.epub_date, expected)
        self.assertEqual(dates.article_year, "2022")

    def test_article_date_isoformat_sucesso(self):
        dates = ArticleDates(self.sample_xml)
        self.assertEqual(dates.article_date_isoformat, "2022-04-20")

    def test_article_date_isoformat_falha_levanta_excecao(self):
        # XML sem parâmetros necessários (day/month) para montar o isoformat
        xml = etree.fromstring(
            '<article><front><pub-date date-type="pub"><year>2022</year></pub-date></front></article>'
        )
        dates = ArticleDates(xml)

        with self.assertRaises(XMLWithPreArticlePublicationDateError):
            _ = dates.article_date_isoformat

    def test_collection_date_e_collection_year(self):
        dates = ArticleDates(self.sample_xml)
        expected = {"year": "2003", "type": "collection"}

        self.assertEqual(dates.collection_date, expected)
        self.assertEqual(dates.collection_year, "2003")

    def test_pub_dates_lista_todas_as_datas(self):
        dates = ArticleDates(self.sample_xml)
        result = dates.pub_dates

        self.assertEqual(len(result), 2)
        self.assertEqual(
            result[0], {"year": "2022", "month": "04", "day": "20", "type": "pub"}
        )
        self.assertEqual(result[1], {"year": "2003", "type": "collection"})

    def test_xml_sem_datas(self):
        xml_vazio = etree.fromstring("<article><front></front></article>")
        dates = ArticleDates(xml_vazio)

        self.assertIsNone(dates.article_date)
        self.assertIsNone(dates.article_year)
        self.assertIsNone(dates.collection_date)
        self.assertIsNone(dates.collection_year)
        self.assertEqual(dates.pub_dates, [])

    def test_xml_com_pub_type_alternativo(self):
        # Valida se as rotas de XPath com pub-type="epub" funcionam
        xml_alt = etree.fromstring(
            """
        <article>
            <front>
                <pub-date pub-type="epub"><year>2021</year><month>01</month><day>15</day></pub-date>
            </front>
        </article>
        """
        )
        dates = ArticleDates(xml_alt)
        self.assertEqual(dates.article_year, "2021")
        self.assertEqual(dates.article_date_isoformat, "2021-01-15")


class TestPublicationDates(TestCase):
    """Testes para get_complete_publication_date e article_publication_date."""

    def test_get_complete_publication_date_isoformat_success(self):
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <article>
          <front>
            <article-meta>
              <pub-date date-type="pub" publication-format="electronic">
                <day>15</day>
                <month>08</month>
                <year>2023</year>
              </pub-date>
            </article-meta>
          </front>
        </article>"""

        xml_obj = next(XMLWithPre.create(xml_content=xml_content))
        self.assertEqual(xml_obj.get_complete_publication_date(), "2023-08-15")

    def test_get_complete_publication_date_fallback_to_defaults(self):
        # Quando faltam mês e dia no dicionário de datas, usa default_month e default_day
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <article>
          <front>
            <article-meta>
              <pub-date date-type="collection">
                <year>2022</year>
              </pub-date>
            </article-meta>
          </front>
        </article>"""

        xml_obj = next(XMLWithPre.create(xml_content=xml_content))
        # Mês padrão (6) e Dia padrão (15)
        self.assertEqual(
            xml_obj.get_complete_publication_date(default_month=6, default_day=15),
            "2022-06-15",
        )

    def test_get_complete_publication_date_missing_year_raises_exception(self):
        # Sem data ou sem chave de ano válida deve lançar XMLWithPreArticlePublicationDateError
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <article>
          <front>
            <article-meta>
            </article-meta>
          </front>
        </article>"""

        xml_obj = next(XMLWithPre.create(xml_content=xml_content))
        with self.assertRaises(XMLWithPreArticlePublicationDateError):
            xml_obj.get_complete_publication_date()

    def test_article_publication_date_isoformat_success(self):
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <article>
          <front>
            <article-meta>
              <pub-date date-type="pub">
                <day>01</day>
                <month>12</month>
                <year>2021</year>
              </pub-date>
            </article-meta>
          </front>
        </article>"""

        xml_obj = next(XMLWithPre.create(xml_content=xml_content))
        self.assertEqual(xml_obj.article_publication_date, "2021-12-01")

    def test_article_publication_date_fallback_to_pub_year(self):
        # Caso ocorra erro ao tentar extrair a data completa em ISO, faz o fallback para pub_year
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <article>
          <front>
            <article-meta>
              <pub-date date-type="collection">
                <year>2020</year>
              </pub-date>
            </article-meta>
          </front>
        </article>"""

        xml_obj = next(XMLWithPre.create(xml_content=xml_content))
        self.assertEqual(xml_obj.article_publication_date, "2020")


class TestArticlePublicationDateSetter(TestCase):
    """Suíte de testes para a propriedade setter article_publication_date em XMLWithPre."""

    def _get_xml_with_pre(self, xml_content):
        return next(XMLWithPre.create(xml_content=xml_content))

    def test_setter_with_valid_string_format(self):
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <article>
            <front>
                <article-meta>
                    <pub-date date-type="pub">
                        <day>01</day>
                        <month>01</month>
                        <year>2020</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>"""

        xml_obj = self._get_xml_with_pre(xml_content)
        xml_obj.article_publication_date = "2023-08-15"

        node = xml_obj.xmltree.find(".//article-meta/pub-date")
        self.assertEqual(node.findtext("year"), "2023")
        self.assertEqual(node.findtext("month"), "08")
        self.assertEqual(node.findtext("day"), "15")

    def test_setter_with_valid_dict_format(self):
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <article>
            <front>
                <article-meta>
                    <pub-date date-type="pub">
                        <day>01</day>
                        <month>01</month>
                        <year>2020</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>"""

        xml_obj = self._get_xml_with_pre(xml_content)
        xml_obj.article_publication_date = {
            "year": "2022",
            "month": "05",
            "day": "10",
        }

        node = xml_obj.xmltree.find(".//article-meta/pub-date")
        self.assertEqual(node.findtext("year"), "2022")
        self.assertEqual(node.findtext("month"), "05")
        self.assertEqual(node.findtext("day"), "10")

    def test_setter_converts_epub_ppub_and_creates_new_pub_date(self):
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <article>
            <front>
                <article-meta>
                    <pub-date pub-type="epub-ppub">
                        <day>01</day>
                        <month>01</month>
                        <year>2020</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>"""

        xml_obj = self._get_xml_with_pre(xml_content)
        xml_obj.article_publication_date = "2024-03-20"

        # Verifica se o nó antigo trocou pub-type para collection
        collection_node = xml_obj.xmltree.find(".//pub-date[@pub-type='collection']")
        self.assertIsNotNone(collection_node)

        # Verifica se o novo nó foi criado com pub-type="epub" (por causa da presenca de @pub-type)
        new_node = xml_obj.xmltree.find(".//pub-date[@pub-type='epub']")
        self.assertIsNotNone(new_node)
        self.assertEqual(new_node.findtext("year"), "2024")
        self.assertEqual(new_node.findtext("month"), "03")
        self.assertEqual(new_node.findtext("day"), "20")

    def test_setter_creates_new_node_recent_pattern_when_none_exists(self):
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <article>
            <front>
                <article-meta>
                    <article-id pub-id-type="publisher-id">S0101-0101</article-id>
                </article-meta>
            </front>
        </article>"""

        xml_obj = self._get_xml_with_pre(xml_content)
        xml_obj.article_publication_date = "2023-11-05"

        node = xml_obj.xmltree.find(".//article-meta/pub-date")
        self.assertIsNotNone(node)
        self.assertEqual(node.get("date-type"), "pub")
        self.assertEqual(node.get("publication-format"), "electronic")
        self.assertEqual(node.findtext("year"), "2023")
        self.assertEqual(node.findtext("month"), "11")
        self.assertEqual(node.findtext("day"), "05")

    def test_setter_creates_new_node_legacy_pattern_when_pub_type_present(self):
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <article>
            <front>
                <article-meta>
                    <pub-date pub-type="ppub">
                        <year>2010</year>
                    </pub-date>
                </article-meta>
            </front>
        </article>"""

        xml_obj = self._get_xml_with_pre(xml_content)
        xml_obj.article_publication_date = "2021-07-01"

        new_node = xml_obj.xmltree.find(".//pub-date[@pub-type='epub']")
        self.assertIsNotNone(new_node)
        self.assertEqual(new_node.findtext("year"), "2021")

    def test_setter_inserts_node_before_following_siblings_if_no_preceding(self):
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <article>
            <front>
                <article-meta>
                    <volume>10</volume>
                    <issue>2</issue>
                </article-meta>
            </front>
        </article>"""

        xml_obj = self._get_xml_with_pre(xml_content)
        xml_obj.article_publication_date = "2022-09-15"

        article_meta = xml_obj.xmltree.find(".//article-meta")
        children = [child.tag for child in article_meta]
        self.assertEqual(children[0], "pub-date")
        self.assertEqual(children[1], "volume")

    def test_setter_appends_node_if_no_preceding_or_following_siblings_match(self):
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <article>
            <front>
                <article-meta>
                </article-meta>
            </front>
        </article>"""

        xml_obj = self._get_xml_with_pre(xml_content)
        xml_obj.article_publication_date = "2020-01-01"

        article_meta = xml_obj.xmltree.find(".//article-meta")
        self.assertEqual(len(article_meta), 1)
        self.assertEqual(article_meta[0].tag, "pub-date")

    def test_setter_raises_exception_on_invalid_string(self):
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <article><front><article-meta></article-meta></front></article>"""

        xml_obj = self._get_xml_with_pre(xml_content)

        invalid_values = [
            "2023-13-01",  # mês inválido
            "invalid-date",  # string arbitrária
            "2023-01",  # sem o dia
            None,
            12345,
        ]

        for val in invalid_values:
            with self.subTest(val=val):
                with self.assertRaises(XMLWithPreArticlePublicationDateError):
                    xml_obj.article_publication_date = val


if __name__ == "__main__":
    unittest.main()