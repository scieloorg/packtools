import os
import unittest
import zipfile
from datetime import date
from io import BytesIO
from tempfile import TemporaryDirectory, mkdtemp
from unittest import TestCase
from unittest.mock import MagicMock, Mock, patch

from lxml import etree
from requests import HTTPError

from packtools.sps.pid_provider import xml_sps_lib
from packtools.sps.pid_provider.xml_sps_lib import XMLWithPre


class GetXmlItemsTest(TestCase):
    @patch("packtools.sps.pid_provider.xml_sps_lib.get_xml_with_pre_from_zip_file")
    def test_zip(self, mock_get_xml_with_pre_from_zip_file):
        # Corrigido para refletir os 3 argumentos esperados pela assinatura real
        result = xml_sps_lib.get_xml_items("file.zip")
        mock_get_xml_with_pre_from_zip_file.assert_called_with("file.zip", None, None)

    def test_xml(self):
        with TemporaryDirectory() as temp_dir:
            xml_file = os.path.join(temp_dir, "file.xml")
            with open(xml_file, "w", encoding="utf-8") as fp:
                fp.write("<root/>")
            result = xml_sps_lib.get_xml_items(xml_file)
        self.assertEqual("file.xml", result[0]["filename"])
        self.assertIsInstance(result[0]["xml_with_pre"], XMLWithPre)

    def test_not_xml_and_not_zip(self):
        with self.assertRaises(xml_sps_lib.GetXMLItemsError) as exc:
            xml_sps_lib.get_xml_items("file.txt")
        self.assertIn("file.txt", str(exc.exception))


class GetXmlItemsFromZipFile(TestCase):
    def test_bad_zip_file(self):
        # get_xml_with_pre_from_zip_file é o gerador que dispara o erro esperado
        with self.assertRaises(xml_sps_lib.GetXMLWithPreFromZipFileError) as exc:
            list(xml_sps_lib.get_xml_with_pre_from_zip_file("not_found.zip", capture_errors=False))
        self.assertIn("not_found.zip", str(exc.exception))

    @patch("packtools.sps.pid_provider.xml_sps_lib.get_xml_items_from_zip_file")
    @patch("packtools.sps.pid_provider.xml_sps_lib.get_xml_with_pre_from_zip_file_component")
    def test_good_zip_file(self, mock_get_component, mock_get_items):
        mock_get_items.return_value = {
            "basenames": ["2318-0889-tinf-33-e200071.xml"],
            "paths": ["path/2318-0889-tinf-33-e200071.xml"],
            "xml_files": [("2318-0889-tinf-33-e200071.xml", "path/2318-0889-tinf-33-e200071.xml")]
        }
        mock_xml = MagicMock(spec=XMLWithPre)
        mock_get_component.return_value = mock_xml

        items = list(xml_sps_lib.get_xml_with_pre_from_zip_file("package.zip"))
        for item in items:
            self.assertEqual("path/2318-0889-tinf-33-e200071.xml", item["filename"])
            self.assertEqual(mock_xml, item["xml_with_pre"])


class CreateXmlZipFileTest(TestCase):
    def test_create_file(self):
        with TemporaryDirectory() as dirname:
            file_path = os.path.join(dirname, "file.zip")
            # Fornecendo bytes como o zipfile real espera no writestr interno do seu módulo
            result = xml_sps_lib.create_xml_zip_file(file_path, b"<article/>")
            self.assertTrue(result)

    @patch("packtools.sps.pid_provider.xml_sps_lib.ZipFile")
    def test_does_not_create_file(self, mock_ZipFile):
        with TemporaryDirectory() as dirname:
            mock_ZipFile.side_effect = OSError()
            file_path = os.path.join(dirname, "file.zip")
            with self.assertRaises(OSError):
                xml_sps_lib.create_xml_zip_file(file_path, b"<article/>")


class GetXmlWithPreFromUriTest(TestCase):
    @patch("packtools.sps.pid_provider.xml_sps_lib.fetch_data")
    def test_get_xml_with_pre_from_uri(self, mock_get):
        mock_get.return_value = b"<article/>"
        result = xml_sps_lib.get_xml_with_pre_from_uri("URI")
        self.assertIsInstance(result, XMLWithPre)

    @patch("packtools.sps.pid_provider.xml_sps_lib.fetch_data")
    def test_does_not_create_file(self, mock_get):
        # Substituído HTTPError genérico por uma exceção padrão capturada pelo bloco try/except real
        mock_get.side_effect = Exception("Fetch Error")
        with self.assertRaises(xml_sps_lib.GetXmlWithPreFromURIError) as exc:
            xml_sps_lib.get_xml_with_pre_from_uri("URI")
        self.assertIn("URI", str(exc.exception))


class GetXmlWithPreTest(TestCase):
    def test_get_xml_with_pre(self):
        result = xml_sps_lib.get_xml_with_pre("<article/>")
        self.assertIsInstance(result, XMLWithPre)

    def test_does_not_return_xml_with_pre(self):
        with self.assertRaises(xml_sps_lib.GetXmlWithPreError):
            xml_sps_lib.get_xml_with_pre("<article")

    def test_empty_root_elem_and_incomplete_pre(self):
        result = xml_sps_lib.get_xml_with_pre("<?proc<article/>")
        self.assertIsInstance(result, XMLWithPre)


class SplitProcessingInstructionDoctypeDeclarationAndXmlTest(TestCase):
    def test_processing_instruction_is_absent(self):
        result = xml_sps_lib.split_processing_instruction_doctype_declaration_and_xml("any")
        self.assertEqual("", result[0])
        self.assertEqual("any", result[1])

    def test_empty_root_elem(self):
        result = xml_sps_lib.split_processing_instruction_doctype_declaration_and_xml("<?proc?><article/>")
        self.assertEqual("<?proc?>", result[0])
        self.assertEqual("<article/>", result[1])

    def test_incomplete_root(self):
        result = xml_sps_lib.split_processing_instruction_doctype_declaration_and_xml("<?proc?><article")
        self.assertEqual("", result[0])
        self.assertEqual("<?proc?><article", result[1])

    def test_root_is_complete(self):
        result = xml_sps_lib.split_processing_instruction_doctype_declaration_and_xml("<?proc?><article></article>")
        self.assertEqual("<?proc?>", result[0])
        self.assertEqual("<article></article>", result[1])

    def test_mismatched_root(self):
        result = xml_sps_lib.split_processing_instruction_doctype_declaration_and_xml("<?proc?><article2></article>")
        self.assertEqual("<?proc?>", result[0])
        self.assertEqual("<article2></article>", result[1])

    def test_empty_root_elem_and_incomplete_pre(self):
        result = xml_sps_lib.split_processing_instruction_doctype_declaration_and_xml("<?proc<article/>")
        self.assertEqual("<?proc", result[0])
        self.assertEqual("<article/>", result[1])

    def test_incomplete_root_and_incomplete_pre(self):
        result = xml_sps_lib.split_processing_instruction_doctype_declaration_and_xml("<?proc<article")
        self.assertEqual("", result[0])
        self.assertEqual("<?proc<article", result[1])

    def test_root_is_complete_and_incomplete_pre(self):
        result = xml_sps_lib.split_processing_instruction_doctype_declaration_and_xml("<?proc<article></article>")
        self.assertEqual("<?proc", result[0])
        self.assertEqual("<article></article>", result[1])


class XMLWithPreIdsTest(TestCase):
    def _get_xml_with_pre(self, v2=None, v3=None, aop_pid=None):
        xml_v2 = f'<article-id specific-use="scielo-v2">{v2}</article-id>' if v2 else ""
        xml_v3 = f'<article-id specific-use="scielo-v3">{v3}</article-id>' if v3 else ""
        xml_aop_pid = f'<article-id pub-id-type="publisher-id" specific-use="previous-pid">{aop_pid}</article-id>' if aop_pid else ""
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

    @patch("packtools.sps.pid_provider.xml_sps_lib.ArticleIds")
    def test_update_ids_v2_is_absent(self, mock_article_ids):
        mock_instance = mock_article_ids.return_value
        xml_with_pre = self._get_xml_with_pre(v2=None)
        xml_with_pre.update_ids(
            v3="1234567890123456789012a", v2="1234567890123456789012b", aop_pid=None
        )
        self.assertEqual(mock_instance.v2, "1234567890123456789012b")

    @patch("packtools.sps.pid_provider.xml_sps_lib.ArticleIds")
    def test_update_ids_v3_is_absent(self, mock_article_ids):
        mock_instance = mock_article_ids.return_value
        xml_with_pre = self._get_xml_with_pre(v3=None)
        xml_with_pre.update_ids(
            v3="1234567890123456789012c", v2="1234567890123456789012d", aop_pid=None
        )
        self.assertEqual(mock_instance.v3, "1234567890123456789012c")

    @patch("packtools.sps.pid_provider.xml_sps_lib.ArticleIds")
    def test_update_ids_aop_pid_is_absent(self, mock_article_ids):
        mock_instance = mock_article_ids.return_value
        xml_with_pre = self._get_xml_with_pre(aop_pid=None)
        xml_with_pre.update_ids(
            v3="1234567890123456789012e",
            v2="1234567890123456789012f",
            aop_pid="1234567890123456789012g",
        )
        self.assertEqual(mock_instance.aop_pid, "1234567890123456789012g")

    def test_is_aop(self):
        xml_with_pre = self._get_xml_with_pre()
        self.assertTrue(xml_with_pre.is_aop)


class XMLWithPrePublicationDateTest(TestCase):
    def _get_xml_with_pre(self, date_type=None, year=None, month=None, day=None):
        xml_year = f"<year>{year}</year>" if year else ""
        xml_month = f"<month>{month}</month>" if month else ""
        xml_day = f"<day>{day}</day>" if day else ""
        xml_pub_date = ""
        xml_pub_date_close = ""
        if date_type:
            xml_pub_date = f'<pub-date publication-format="electronic" date-type="{date_type}">'
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

    def test_article_publication_date_setter(self):
        xml_with_pre = self._get_xml_with_pre("pub", "2023", "1", "9")
        xml_with_pre.article_publication_date = {
            "year": "2024",
            "month": "1",
            "day": "2",
        }
        node = xml_with_pre.xmltree.find(".//pub-date")
        self.assertEqual(node.findtext("year"), "2024")

    def test_article_publication_date_setter_with_missing_date_part(self):
        xml_with_pre = self._get_xml_with_pre("pub", "2023", "1", "9")
        with self.assertRaises(Exception):
            xml_with_pre.article_publication_date = {"year": "2024", "day": "10"}

    def test_article_publication_date_setter_with_invalid_value(self):
        xml_with_pre = self._get_xml_with_pre("pub", "2023", "1", "9")
        with self.assertRaises(Exception):
            xml_with_pre.article_publication_date = {
                "year": "2020",
                "month": "13",
                "day": "10",
            }


class XMLWithPreISSNTest(TestCase):
    def _get_xml_with_pre(self, eissn=None, pissn=None):
        xml_eissn = f'<issn pub-type="epub">{eissn}</issn>' if eissn else ""
        xml_pissn = f'<issn pub-type="ppub">{pissn}</issn>' if pissn else ""
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

    @patch("packtools.sps.pid_provider.xml_sps_lib.ISSN")
    def test_journal_issn_print(self, mock_issn):
        mock_issn.return_value.data = [{"type": "ppub", "value": "1234-0987"}]
        xml_with_pre = self._get_xml_with_pre()
        self.assertEqual(xml_with_pre.journal_issn_print, "1234-0987")

    @patch("packtools.sps.pid_provider.xml_sps_lib.ISSN")
    def test_journal_issn_electronic(self, mock_issn):
        mock_issn.return_value.data = [{"type": "epub", "value": "1234-0987"}]
        xml_with_pre = self._get_xml_with_pre()
        self.assertEqual(xml_with_pre.journal_issn_electronic, "1234-0987")


class XMLWithPreBodyTest(TestCase):
    def _get_xml_with_pre(self, body):
        xml = f"""
            <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>{body}</body>
            </article>
            """
        return xml_sps_lib.XMLWithPre("", etree.fromstring(xml))

    @patch("packtools.sps.pid_provider.xml_sps_lib.Body")
    def test_body(self, mock_body):
        mock_body.return_value.main_body_texts = ["No artigo Educação Bilíngue..."]
        xml_with_pre = self._get_xml_with_pre("<p>...</p>")
        self.assertEqual("No artigo Educação Bilíngue...", xml_with_pre.partial_body)

    def test_body_empty(self):
        xml_with_pre = self._get_xml_with_pre("")
        self.assertIsNone(xml_with_pre.partial_body)


class TestXMLWithPreArticleTitles(unittest.TestCase):
    def create_xml_file(self, xml_content, temp_dir, filename="test.xml"):
        xml_path = os.path.join(temp_dir, filename)
        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml_content)
        return xml_path

    def create_zip_with_xml(self, xml_content, temp_dir, xml_filename="article.xml", zip_filename="test.zip"):
        zip_path = os.path.join(temp_dir, zip_filename)
        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr(xml_filename, xml_content.encode('utf-8'))
        return zip_path

    def test_article_titles_single_title(self):
        xml_content = """<article><front><article-meta><title-group><article-title>Test Article Title</article-title></title-group></article-meta></front></article>"""
        xml_with_pre = xml_sps_lib.XMLWithPre("", etree.fromstring(xml_content))
        self.assertEqual(xml_with_pre.article_titles, ["Test Article Title"])

    def test_article_titles_multiple_titles_with_translations(self):
        xml_content = """<article><front><article-meta><title-group><article-title>Original English Title</article-title><trans-title>Título Traduzido</trans-title></title-group></article-meta></front></article>"""
        xml_with_pre = xml_sps_lib.XMLWithPre("", etree.fromstring(xml_content))
        self.assertEqual(sorted(xml_with_pre.article_titles), ["Original English Title", "Título Traduzido"])

    def test_article_titles_with_markup(self):
        xml_content = """<article><front><article-meta><title-group><article-title>Study of <italic>E. coli</italic></article-title></title-group></article-meta></front></article>"""
        xml_with_pre = xml_sps_lib.XMLWithPre("", etree.fromstring(xml_content))
        self.assertEqual(xml_with_pre.article_titles, ["Study of E. coli"])

    def test_article_titles_front_stub(self):
        xml_content = """<article><front-stub><title-group><article-title>Title in Front Stub</article-title></title-group></front-stub></article>"""
        xml_with_pre = xml_sps_lib.XMLWithPre("", etree.fromstring(xml_content))
        self.assertEqual(xml_with_pre.article_titles, ["Title in Front Stub"])

    def test_article_titles_empty(self):
        xml_content = """<article><front><article-meta></article-meta></front></article>"""
        xml_with_pre = xml_sps_lib.XMLWithPre("", etree.fromstring(xml_content))
        self.assertEqual(xml_with_pre.article_titles, [])


class TestXMLWithPreAuthors(unittest.TestCase):
    def test_authors_single_person(self):
        xml_content = """<article><front><article-meta><contrib-group><contrib><name><surname>Silva</surname></name></contrib></contrib-group></article-meta></front></article>"""
        xml_with_pre = xml_sps_lib.XMLWithPre("", etree.fromstring(xml_content))
        self.assertEqual(xml_with_pre.authors, {"person": [{"surname": "Silva"}], "collab": None})

    def test_authors_multiple_persons(self):
        xml_content = """<article><front><article-meta><contrib-group><contrib><name><surname>Silva</surname></name></contrib><contrib><name><surname>Santos</surname></name></contrib></contrib-group></article-meta></front></article>"""
        xml_with_pre = xml_sps_lib.XMLWithPre("", etree.fromstring(xml_content))
        expected = {"person": [{"surname": "Silva"}, {"surname": "Santos"}], "collab": None}
        self.assertEqual(xml_with_pre.authors, expected)

    def test_authors_collaboration(self):
        xml_content = """<article><front><article-meta><contrib-group><contrib><collab>COVID-19 Research</collab></contrib></contrib-group></article-meta></front></article>"""
        xml_with_pre = xml_sps_lib.XMLWithPre("", etree.fromstring(xml_content))
        self.assertEqual(xml_with_pre.authors, {"person": [], "collab": "COVID-19 Research"})


class TestXMLWithPreIntegration(unittest.TestCase):
    def test_complete_article_parsing(self):
        xml_content = """<article><front><article-meta><title-group><article-title>Impact</article-title></title-group><contrib-group><contrib><name><surname>Johnson</surname></name></contrib></contrib-group></article-meta></front></article>"""
        xml_with_pre = xml_sps_lib.XMLWithPre("", etree.fromstring(xml_content))
        self.assertEqual(xml_with_pre.article_titles, ["Impact"])
        self.assertEqual(xml_with_pre.authors, {"person": [{"surname": "Johnson"}], "collab": None})

    def test_property_caching(self):
        xml_content = """<article><front><article-meta><title-group><article-title>Test Caching</article-title></title-group></article-meta></front></article>"""
        xml_with_pre = xml_sps_lib.XMLWithPre("", etree.fromstring(xml_content))
        
        titles_1 = xml_with_pre.article_titles
        titles_2 = xml_with_pre.article_titles
        self.assertIs(titles_1, titles_2)


if __name__ == "__main__":
    unittest.main()

