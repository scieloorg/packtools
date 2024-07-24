import os
from datetime import date
from tempfile import TemporaryDirectory
from unittest import TestCase
from unittest.mock import MagicMock, patch

from lxml import etree
from requests import HTTPError

from packtools.sps.pid_provider import xml_sps_lib


# Create your tests here.
class GetXmlItemsTest(TestCase):
    @patch("packtools.sps.pid_provider.xml_sps_lib.get_xml_items_from_zip_file")
    def test_zip(self, mock_get_xml_items_from_zip_file):
        result = xml_sps_lib.get_xml_items("file.zip")
        mock_get_xml_items_from_zip_file.assert_called_with("file.zip", None)

    @patch("packtools.sps.pid_provider.xml_sps_lib.get_xml_with_pre")
    @patch("packtools.sps.pid_provider.xml_sps_lib.open")
    def test_xml(self, mock_open, mock_get_xml_with_pre):
        mock_get_xml_with_pre.return_value = "retorno"
        result = xml_sps_lib.get_xml_items("file.xml")
        mock_open.assert_called_with("file.xml")
        self.assertListEqual(
            [{"filename": "file.xml", "xml_with_pre": "retorno"}], result
        )

    def test_not_xml_and_not_zip(self):
        with self.assertRaises(xml_sps_lib.GetXMLItemsError) as exc:
            result = xml_sps_lib.get_xml_items("file.txt")
        self.assertIn("file.txt", str(exc.exception))


class GetXmlItemsFromZipFile(TestCase):
    def test_bad_zip_file(self):
        # xmlsps.xml_sps_lib.GetXMLItemsFromZipFileError
        with self.assertRaises(xml_sps_lib.GetXMLItemsFromZipFileError) as exc:
            items = list(xml_sps_lib.get_xml_items_from_zip_file("not_found.zip"))
        self.assertIn("not_found.zip", str(exc.exception))

    def test_good_zip_file(self):
        items = xml_sps_lib.get_xml_items_from_zip_file(
            "./tests/sps/pid_provider/fixtures/artigo.xml.zip"
        )
        for item in items:
            self.assertEqual("artigo.xml", item["filename"])
            self.assertEqual(xml_sps_lib.XMLWithPre, type(item["xml_with_pre"]))


class CreateXmlZipFileTest(TestCase):
    def test_create_file(self):
        with TemporaryDirectory() as dirname:
            file_path = os.path.join(dirname, "file.zip")
            result = xml_sps_lib.create_xml_zip_file(file_path, "<article/>")
            self.assertEqual(True, result)

    @patch("packtools.sps.pid_provider.xml_sps_lib.ZipFile")
    def test_does_not_create_file(self, mock_ZipFile):
        with TemporaryDirectory() as dirname:
            mock_ZipFile.side_effect = OSError()
            file_path = os.path.join(dirname, "file.zip")
            with self.assertRaises(OSError):
                result = xml_sps_lib.create_xml_zip_file(file_path, "<article/>")


class GetXmlWithPreFromUriTest(TestCase):
    @patch("packtools.sps.pid_provider.xml_sps_lib.fetch_data")
    def test_get_xml_with_pre_from_uri(self, mock_get):
        class Resp:
            def __init__(self):
                self.content = b"<article/>"

        mock_get.return_value = Resp()
        result = xml_sps_lib.get_xml_with_pre_from_uri("URI")
        self.assertEqual(xml_sps_lib.XMLWithPre, type(result))

    @patch("packtools.sps.pid_provider.xml_sps_lib.fetch_data")
    def test_does_not_create_file(self, mock_get):
        mock_get.side_effect = HTTPError()
        with self.assertRaises(xml_sps_lib.GetXmlWithPreFromURIError) as exc:
            result = xml_sps_lib.get_xml_with_pre_from_uri("URI")
        self.assertIn("URI", str(exc.exception))


class GetXmlWithPreTest(TestCase):
    def test_get_xml_with_pre(self):
        result = xml_sps_lib.get_xml_with_pre("<article/>")
        self.assertEqual(xml_sps_lib.XMLWithPre, type(result))

    def test_does_not_return_xml_with_pre(self):
        with self.assertRaises(xml_sps_lib.GetXmlWithPreError):
            result = xml_sps_lib.get_xml_with_pre("<article")

    def test_empty_root_elem_and_incomplete_pre(self):
        with self.assertRaises(xml_sps_lib.GetXmlWithPreError) as exc:
            result = xml_sps_lib.get_xml_with_pre("<?proc<article/>")
        print(exc.exception)


class SplitProcessingInstructionDoctypeDeclarationAndXmlTest(TestCase):
    def test_processing_instruction_is_absent(self):
        result = xml_sps_lib.split_processing_instruction_doctype_declaration_and_xml(
            "any"
        )
        self.assertEqual("", result[0])
        self.assertEqual("any", result[1])

    def test_empty_root_elem(self):
        result = xml_sps_lib.split_processing_instruction_doctype_declaration_and_xml(
            "<?proc?><article/>"
        )
        self.assertEqual("<?proc?>", result[0])
        self.assertEqual("<article/>", result[1])

    def test_incomplete_root(self):
        result = xml_sps_lib.split_processing_instruction_doctype_declaration_and_xml(
            "<?proc?><article"
        )
        self.assertEqual("", result[0])
        self.assertEqual("<?proc?><article", result[1])

    def test_root_is_complete(self):
        result = xml_sps_lib.split_processing_instruction_doctype_declaration_and_xml(
            "<?proc?><article></article>"
        )
        self.assertEqual("<?proc?>", result[0])
        self.assertEqual("<article></article>", result[1])

    def test_mismatched_root(self):
        result = xml_sps_lib.split_processing_instruction_doctype_declaration_and_xml(
            "<?proc?><article2></article>"
        )
        self.assertEqual("", result[0])
        self.assertEqual("<?proc?><article2></article>", result[1])

    def test_empty_root_elem_and_incomplete_pre(self):
        result = xml_sps_lib.split_processing_instruction_doctype_declaration_and_xml(
            "<?proc<article/>"
        )
        self.assertEqual("", result[0])
        self.assertEqual("<?proc<article/>", result[1])

    def test_incomplete_root_and_incomplete_pre(self):
        result = xml_sps_lib.split_processing_instruction_doctype_declaration_and_xml(
            "<?proc<article"
        )
        self.assertEqual("", result[0])
        self.assertEqual("<?proc<article", result[1])

    def test_root_is_complete_and_incomplete_pre(self):
        result = xml_sps_lib.split_processing_instruction_doctype_declaration_and_xml(
            "<?proc<article></article>"
        )
        self.assertEqual("", result[0])
        self.assertEqual("<?proc<article></article>", result[1])


class XMLWithPreIdsTest(TestCase):
    def _get_xml_with_pre(self, v2=None, v3=None, aop_pid=None):
        xml_v2 = v2 and f'<article-id specific-use="scielo-v2">{v2}</article-id>' or ""
        xml_v3 = v3 and f'<article-id specific-use="scielo-v3">{v3}</article-id>' or ""
        xml_aop_pid = (
            aop_pid
            and f'<article-id pub-id-type="publisher-id" specific-use="previous-pid">{aop_pid}</article-id>'
            or ""
        )
        xml = f"""
        <article>
        <front>
        <article-meta>
        {xml_v2}
        {xml_v3}
        {xml_aop_pid}
        </article-meta>
        </front>
        </article>
        """
        return xml_sps_lib.XMLWithPre("", etree.fromstring(xml))

    def test_update_ids_v2_is_absent(self):
        xml_with_pre = self._get_xml_with_pre(v2=None)
        xml_with_pre.update_ids(v3="novo-v3", v2="novo", aop_pid=None)
        self.assertEqual("novo", xml_with_pre.v2)

    def test_update_ids_v3_is_absent(self):
        xml_with_pre = self._get_xml_with_pre(v3=None)
        xml_with_pre.update_ids(v3="novo", v2="novo-v2", aop_pid=None)
        self.assertEqual("novo", xml_with_pre.v3)

    def test_update_ids_aop_pid_is_absent(self):
        xml_with_pre = self._get_xml_with_pre(aop_pid=None)
        xml_with_pre.update_ids(v3="v3", v2="v2", aop_pid="novo")
        self.assertEqual("novo", xml_with_pre.aop_pid)

    def test_update_ids_v2_is_present_updating_is_forbidden(self):
        xml_with_pre = self._get_xml_with_pre(v2="current")
        with self.assertRaises(AttributeError) as exc:
            xml_with_pre.update_ids(v3="v3", v2="novo", aop_pid=None)
        self.assertIn("It is already set: current", str(exc.exception))

    def test_update_ids_v3_is_present_updating_is_allowed(self):
        xml_with_pre = self._get_xml_with_pre(v3="current")
        xml_with_pre.update_ids(v3="novo", v2="v2", aop_pid=None)
        self.assertEqual("novo", xml_with_pre.v3)

    def test_update_ids_aop_pid_is_present_updating_is_allowed(self):
        xml_with_pre = self._get_xml_with_pre(aop_pid="current")
        xml_with_pre.update_ids(v3="v3", v2="v2", aop_pid="novo")
        self.assertEqual("novo", xml_with_pre.aop_pid)

    def test_is_aop(self):
        xml_with_pre = self._get_xml_with_pre()
        self.assertTrue(xml_with_pre.is_aop)


class XMLWithPrePublicationDateTest(TestCase):
    def _get_xml_with_pre(self, date_type=None, year=None, month=None, day=None):
        xml_year = year and f"<year>{year}</year>" or ""
        xml_month = month and f"<month>{month}</month>" or ""
        xml_day = day and f"<day>{day}</day>" or ""
        xml_pub_date = ""
        xml_pub_date_close = ""
        if date_type:
            xml_pub_date = (
                f'<pub-date publication-format="electronic" date-type="{date_type}">'
            )
            xml_pub_date_close = "</pub-date>"
        xml = f"""
        <article>
        <front>
        <article-meta>
        {xml_pub_date}
        {xml_year}
        {xml_month}
        {xml_day}
        {xml_pub_date_close}
        </article-meta>
        </front>
        </article>
        """
        return xml_sps_lib.XMLWithPre("", etree.fromstring(xml))

    def test_article_publication_date_is_none(self):
        xml_with_pre = self._get_xml_with_pre()
        self.assertIsNone(xml_with_pre.article_publication_date)

    def test_article_publication_date_is_invalid(self):
        xml_with_pre = self._get_xml_with_pre("pub")
        with self.assertRaises(xml_sps_lib.XMLWithPreArticlePublicationDateError) as e:
            ign = xml_with_pre.article_publication_date

    def test_article_publication_date_is_invalid_missing_month(self):
        xml_with_pre = self._get_xml_with_pre("pub", "2023")
        with self.assertRaises(xml_sps_lib.XMLWithPreArticlePublicationDateError) as e:
            ign = xml_with_pre.article_publication_date

    def test_article_publication_date_is_invalid_missing_day(self):
        xml_with_pre = self._get_xml_with_pre("pub", "2023", "01")
        with self.assertRaises(xml_sps_lib.XMLWithPreArticlePublicationDateError) as e:
            ign = xml_with_pre.article_publication_date

    def test_article_publication_date_is_complete_but_invalid(self):
        xml_with_pre = self._get_xml_with_pre("pub", "2023", "02", "30")
        with self.assertRaises(xml_sps_lib.XMLWithPreArticlePublicationDateError) as e:
            ign = xml_with_pre.article_publication_date

    def test_article_publication_date_is_valid(self):
        xml_with_pre = self._get_xml_with_pre("pub", "2023", "1", "9")
        self.assertEqual("2023-01-09", xml_with_pre.article_publication_date)

    def test_article_publication_date_setter(self):
        xml_with_pre = self._get_xml_with_pre("pub", "2023", "1", "9")
        xml_with_pre.article_publication_date = {"year": "2024", "month": "1", "day": "2"}
        self.assertEqual("2024-01-02", xml_with_pre.article_publication_date)

    def test_article_publication_date_setter_with_missing_date_part(self):
        xml_with_pre = self._get_xml_with_pre("pub", "2023", "1", "9")

        with self.assertRaises(ValueError):
            xml_with_pre.article_publication_date = {"year": "2024", "day": "10"}

    def test_article_publication_date_setter_with_invalid_value(self):
        xml_with_pre = self._get_xml_with_pre("pub", "2023", "1", "9")

        with self.assertRaises(ValueError):
            xml_with_pre.article_publication_date = {"year": "2020", "month": "13", "day": "10"}


class XMLWithPreISSNTest(TestCase):
    def _get_xml_with_pre(self, eissn=None, pissn=None):
        xml_eissn = eissn and f'<issn pub-type="epub">{eissn}</issn>' or ""
        xml_pissn = pissn and f'<issn pub-type="ppub">{pissn}</issn>' or ""
        xml = f"""
        <article>
        <front>
        <journal-meta>
        {xml_eissn}
        {xml_pissn}
        </journal-meta>
        </front>
        </article>
        """
        return xml_sps_lib.XMLWithPre("", etree.fromstring(xml))

    def test_journal_issn_print(self):
        xml_with_pre = self._get_xml_with_pre(pissn="1234-0987")
        self.assertEqual(xml_with_pre.journal_issn_print, "1234-0987")

    def test_journal_issn_electronic(self):
        xml_with_pre = self._get_xml_with_pre(eissn="1234-0987")
        self.assertEqual(xml_with_pre.journal_issn_electronic, "1234-0987")


class XMLWithPreBodyTest(TestCase):
    def _get_xml_with_pre(self, body):
        xml = f"""
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>{body}</body>
            </article>
            """
        return xml_sps_lib.XMLWithPre("", etree.fromstring(xml))

    def test_body(self):
        body = """
        <p>No artigo <bold>Educação Bilíngue para alunos surdos: notas sobre a construção da linguagem argumentativa no aprendizado de Ciências</bold>, com número de DOI: http://dx.doi.org/10.1590/1678-460X202257175, publicado no periódico D.E.L.T.A., 38-1, 2022:202257175, deve-se considerar a adição da informação:</p>
        <p>Artigo em Libras: <ext-link ext-link-type="uri" xlink:href="https://youtu.be/frfspa_XnoE">https://youtu.be/frfspa_XnoE</ext-link> </p>
        <p>A adição da informação se faz necessária por mais de um motivo: (1) trata-se de um número temático sobre educação inclusiva e não seria realmente inclusiva se não incluíssemos ao menos um texto acessível aos surdos; e (2) temos autores surdos no grupo que atuou na escrita do número temático e esse texto é especificamente de um dos grupos de estudos surdos.</p>

        """
        xml_with_pre = self._get_xml_with_pre(body)
        self.assertEqual(
            "No artigo Educação Bilíngue para alunos surdos: notas sobre a construção da linguagem argumentativa no aprendizado de Ciências , com número de DOI: http://dx.doi.org/10.1590/1678-460X202257175, publicado no periódico D.E.L.T.A., 38-1, 2022:202257175, deve-se considerar a adição da informação: ",
            xml_with_pre.partial_body,
        )

    def test_body(self):
        xml_with_pre = self._get_xml_with_pre("")
        self.assertIsNone(xml_with_pre.partial_body)
