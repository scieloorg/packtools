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

# Assumindo que XMLWithPre está disponível
# from your_module import XMLWithPre


# Create your tests here.
class GetXmlItemsTest(TestCase):
    @patch("packtools.sps.pid_provider.xml_sps_lib.get_xml_items_from_zip_file")
    def test_zip(self, mock_get_xml_items_from_zip_file):
        result = xml_sps_lib.get_xml_items("file.zip")
        mock_get_xml_items_from_zip_file.assert_called_with("file.zip", None)

    def test_xml(self):
        with TemporaryDirectory() as temp_dir:
            xml_file = os.path.join(temp_dir, "file.xml")
            with open(xml_file, "w") as fp:
                fp.write("<root/>")
            result = xml_sps_lib.get_xml_items(xml_file)
        self.assertEqual("file.xml", result[0]["filename"])
        self.assertIsInstance(result[0]["xml_with_pre"], XMLWithPre)

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
            "./tests/sps/fixtures/package.zip"
        )
        for item in items:
            self.assertEqual("2318-0889-tinf-33-e200071.xml", item["filename"])
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
        mock_get.return_value = b"<article/>"
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
        xml_with_pre.update_ids(
            v3="1234567890123456789012a", v2="1234567890123456789012b", aop_pid=None
        )
        self.assertEqual("1234567890123456789012b", xml_with_pre.v2)

    def test_update_ids_v3_is_absent(self):
        xml_with_pre = self._get_xml_with_pre(v3=None)
        xml_with_pre.update_ids(
            v3="1234567890123456789012c", v2="1234567890123456789012d", aop_pid=None
        )
        self.assertEqual("1234567890123456789012c", xml_with_pre.v3)

    def test_update_ids_aop_pid_is_absent(self):
        xml_with_pre = self._get_xml_with_pre(aop_pid=None)
        xml_with_pre.update_ids(
            v3="1234567890123456789012e",
            v2="1234567890123456789012f",
            aop_pid="1234567890123456789012g",
        )
        self.assertEqual("1234567890123456789012g", xml_with_pre.aop_pid)

    def test_update_ids_v2_is_present_updating_is_forbidden(self):
        xml_with_pre = self._get_xml_with_pre(v2="1234567890123456789012h")
        xml_with_pre.update_ids(
            v3="1234567890123456789012i", v2="1234567890123456789012j", aop_pid=None
        )
        self.assertEqual("1234567890123456789012j", xml_with_pre.v2)

    def test_update_ids_v3_is_present_updating_is_allowed(self):
        xml_with_pre = self._get_xml_with_pre(v3="1234567890123456789012k")
        xml_with_pre.update_ids(
            v3="1234567890123456789012l", v2="1234567890123456789012m", aop_pid=None
        )
        self.assertEqual("1234567890123456789012l", xml_with_pre.v3)

    def test_update_ids_aop_pid_is_present_updating_is_allowed(self):
        xml_with_pre = self._get_xml_with_pre(aop_pid="1234567890123456789012n")
        xml_with_pre.update_ids(
            v3="1234567890123456789012o",
            v2="1234567890123456789012p",
            aop_pid="1234567890123456789012q",
        )
        self.assertEqual("1234567890123456789012q", xml_with_pre.aop_pid)

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
        xml_with_pre.article_publication_date = {
            "year": "2024",
            "month": "1",
            "day": "2",
        }
        self.assertEqual("2024-01-02", xml_with_pre.article_publication_date)

    def test_article_publication_date_setter_with_missing_date_part(self):
        xml_with_pre = self._get_xml_with_pre("pub", "2023", "1", "9")

        with self.assertRaises(ValueError):
            xml_with_pre.article_publication_date = {"year": "2024", "day": "10"}

    def test_article_publication_date_setter_with_invalid_value(self):
        xml_with_pre = self._get_xml_with_pre("pub", "2023", "1", "9")

        with self.assertRaises(ValueError):
            xml_with_pre.article_publication_date = {
                "year": "2020",
                "month": "13",
                "day": "10",
            }


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


class TestXMLWithPreArticleTitles(unittest.TestCase):
    """Testes para a propriedade article_titles da classe XMLWithPre"""

    def create_xml_file(self, xml_content, temp_dir, filename="test.xml"):
        """Helper para criar arquivo XML temporário"""
        xml_path = os.path.join(temp_dir, filename)

        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml_content)

        return xml_path

    def create_zip_with_xml(
        self, xml_content, temp_dir, xml_filename="article.xml", zip_filename="test.zip"
    ):
        """Helper para criar arquivo ZIP com XML"""
        zip_path = os.path.join(temp_dir, zip_filename)

        with zipfile.ZipFile(zip_path, "w") as zf:
            zf.writestr(xml_filename, xml_content)

        return zip_path

    def test_article_titles_single_title(self):
        """Testa extração de um único título de artigo"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Test Article Title</article-title>
                    </title-group>
                </article-meta>
            </front>
        </article>"""

        with TemporaryDirectory() as temp_dir:
            xml_path = self.create_xml_file(xml_content, temp_dir)

            xml_instances = list(XMLWithPre.create(path=xml_path))
            self.assertTrue(
                len(xml_instances) > 0, "Nenhuma instância XMLWithPre foi criada"
            )

            xml_with_pre = xml_instances[0]
            titles = xml_with_pre.article_titles

            expected = ["Test Article Title"]
            self.assertEqual(titles, expected)

    def test_article_titles_multiple_titles_with_translations(self):
        """Testa extração de múltiplos títulos incluindo traduções"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
                <article-meta>
                    <title-group>
                        <article-title xml:lang="en">Original English Title</article-title>
                        <trans-title-group xml:lang="pt">
                            <trans-title>Título Traduzido em Português</trans-title>
                        </trans-title-group>
                        <trans-title-group xml:lang="es">
                            <trans-title>Título Traducido en Español</trans-title>
                        </trans-title-group>
                    </title-group>
                </article-meta>
            </front>
        </article>"""

        with TemporaryDirectory() as temp_dir:
            xml_path = self.create_xml_file(xml_content, temp_dir)

            xml_instances = list(XMLWithPre.create(path=xml_path))
            xml_with_pre = xml_instances[0]
            titles = xml_with_pre.article_titles

            expected = [
                "Original English Title",
                "Título Traduzido em Português",
                "Título Traducido en Español",
            ]
            self.assertEqual(sorted(titles), sorted(expected))

    def test_article_titles_with_markup(self):
        """Testa extração de títulos que contêm markup XML"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Study of <italic>Escherichia coli</italic> and <bold>COVID-19</bold> interaction</article-title>
                    </title-group>
                </article-meta>
            </front>
        </article>"""

        with TemporaryDirectory() as temp_dir:
            xml_path = self.create_xml_file(xml_content, temp_dir)

            xml_instances = list(XMLWithPre.create(path=xml_path))
            xml_with_pre = xml_instances[0]
            titles = xml_with_pre.article_titles

            expected = ["Study of Escherichia coli and COVID-19 interaction"]
            self.assertEqual(titles, expected)

    def test_article_titles_front_stub(self):
        """Testa extração de títulos em front-stub"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front-stub>
                <title-group>
                    <article-title>Title in Front Stub</article-title>
                    <trans-title xml:lang="pt">Título no Front Stub</trans-title>
                </title-group>
            </front-stub>
        </article>"""

        with TemporaryDirectory() as temp_dir:
            xml_path = self.create_xml_file(xml_content, temp_dir)

            xml_instances = list(XMLWithPre.create(path=xml_path))
            xml_with_pre = xml_instances[0]
            titles = xml_with_pre.article_titles

            expected = ["Title in Front Stub", "Título no Front Stub"]
            self.assertEqual(sorted(titles), sorted(expected))

    def test_article_titles_empty(self):
        """Testa comportamento quando não há títulos"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
                <article-meta>
                </article-meta>
            </front>
        </article>"""

        with TemporaryDirectory() as temp_dir:
            xml_path = self.create_xml_file(xml_content, temp_dir)

            xml_instances = list(XMLWithPre.create(path=xml_path))
            xml_with_pre = xml_instances[0]
            titles = xml_with_pre.article_titles

            expected = []
            self.assertEqual(titles, expected)

    def test_article_titles_from_zip(self):
        """Testa extração de títulos de arquivo XML dentro de ZIP"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Title from ZIP file</article-title>
                    </title-group>
                </article-meta>
            </front>
        </article>"""

        with TemporaryDirectory() as temp_dir:
            zip_path = self.create_zip_with_xml(xml_content, temp_dir)

            xml_instances = list(XMLWithPre.create(path=zip_path))
            xml_with_pre = xml_instances[0]
            titles = xml_with_pre.article_titles

            expected = ["Title from ZIP file"]
            self.assertEqual(titles, expected)


class TestXMLWithPreAuthors(unittest.TestCase):
    """Testes para a propriedade authors da classe XMLWithPre"""

    def create_xml_file(self, xml_content, temp_dir, filename="test.xml"):
        """Helper para criar arquivo XML temporário"""
        xml_path = os.path.join(temp_dir, filename)

        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml_content)

        return xml_path

    def test_authors_single_person(self):
        """Testa extração de um único autor pessoa"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Silva</surname>
                                <given-names>João</given-names>
                            </name>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>"""

        with TemporaryDirectory() as temp_dir:
            xml_path = self.create_xml_file(xml_content, temp_dir)

            xml_instances = list(XMLWithPre.create(path=xml_path))
            xml_with_pre = xml_instances[0]
            authors = xml_with_pre.authors

            expected = {"person": [{"surname": "Silva"}], "collab": None}
            self.assertEqual(authors, expected)

    def test_authors_multiple_persons(self):
        """Testa extração de múltiplos autores pessoa"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Silva</surname>
                                <given-names>João</given-names>
                            </name>
                        </contrib>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Santos</surname>
                                <given-names>Maria</given-names>
                            </name>
                        </contrib>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Oliveira</surname>
                                <given-names>Pedro</given-names>
                            </name>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>"""

        with TemporaryDirectory() as temp_dir:
            xml_path = self.create_xml_file(xml_content, temp_dir)
            xml_instances = list(XMLWithPre.create(path=xml_path))
            xml_with_pre = xml_instances[0]
            authors = xml_with_pre.authors

            expected = {
                "person": [
                    {"surname": "Silva"},
                    {"surname": "Santos"},
                    {"surname": "Oliveira"},
                ],
                "collab": None,
            }
            self.assertEqual(authors, expected)

    def test_authors_collaboration(self):
        """Testa extração de autor colaboração"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <collab>
                                <named-content content-type="program">COVID-19 Research Consortium</named-content>
                            </collab>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>"""

        with TemporaryDirectory() as temp_dir:
            xml_path = os.path.join(temp_dir, "article.xml")
            with open(xml_path, "w") as fp:
                fp.write(xml_content)
            xml_instances = list(XMLWithPre.create(path=xml_path))
            xml_with_pre = xml_instances[0]
            authors = xml_with_pre.authors

            expected = {"person": [], "collab": "COVID-19 Research Consortium"}
            self.assertEqual(authors, expected)

    def test_authors_simple_collaboration(self):
        """Testa extração de colaboração simples (sem named-content)"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <collab>Research Group XYZ</collab>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>"""

        with TemporaryDirectory() as temp_dir:
            xml_path = os.path.join(temp_dir, "article.xml")
            with open(xml_path, "w") as fp:
                fp.write(xml_content)
            xml_instances = list(XMLWithPre.create(path=xml_path))
            xml_with_pre = xml_instances[0]
            authors = xml_with_pre.authors

            expected = {"person": [], "collab": "Research Group XYZ"}
            self.assertEqual(authors, expected)

    def test_authors_mixed_person_and_collab(self):
        """Testa extração mista de autores pessoa e colaboração"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Silva</surname>
                                <given-names>João</given-names>
                            </name>
                        </contrib>
                        <contrib contrib-type="author">
                            <collab>Research Group XYZ</collab>
                        </contrib>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Santos</surname>
                                <given-names>Maria</given-names>
                            </name>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>"""

        with TemporaryDirectory() as temp_dir:
            xml_path = os.path.join(temp_dir, "article.xml")
            with open(xml_path, "w") as fp:
                fp.write(xml_content)
            xml_instances = list(XMLWithPre.create(path=xml_path))
            xml_with_pre = xml_instances[0]
            authors = xml_with_pre.authors

            expected = {
                "person": [{"surname": "Silva"}, {"surname": "Santos"}],
                "collab": "Research Group XYZ",
            }
            self.assertEqual(authors, expected)

    def test_authors_no_contrib_group(self):
        """Testa comportamento quando não há contrib-group"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
                <article-meta>
                </article-meta>
            </front>
        </article>"""

        with TemporaryDirectory() as temp_dir:
            xml_path = os.path.join(temp_dir, "article.xml")
            with open(xml_path, "w") as fp:
                fp.write(xml_content)
            xml_instances = list(XMLWithPre.create(path=xml_path))
            xml_with_pre = xml_instances[0]
            authors = xml_with_pre.authors

            expected = {}
            self.assertEqual(authors, expected)

    def test_authors_empty_contrib_group(self):
        """Testa comportamento com contrib-group vazio"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
                <article-meta>
                    <contrib-group>
                    </contrib-group>
                </article-meta>
            </front>
        </article>"""

        with TemporaryDirectory() as temp_dir:
            xml_path = os.path.join(temp_dir, "article.xml")
            with open(xml_path, "w") as fp:
                fp.write(xml_content)
            xml_instances = list(XMLWithPre.create(path=xml_path))
            xml_with_pre = xml_instances[0]
            authors = xml_with_pre.authors

            expected = {"person": [], "collab": None}
            self.assertEqual(authors, expected)


class TestXMLWithPreIntegration(unittest.TestCase):
    """Testes de integração das propriedades article_titles e authors"""

    def create_xml_file(self, xml_content, filename="test.xml"):
        """Helper para criar arquivo XML temporário"""
        temp_dir = mkdtemp()
        xml_path = os.path.join(temp_dir, filename)

        with open(xml_path, "w", encoding="utf-8") as f:
            f.write(xml_content)

        return xml_path, temp_dir

    def cleanup_temp_dir(self, temp_dir):
        """Helper para limpar diretório temporário"""
        import shutil

        shutil.rmtree(temp_dir, ignore_errors=True)

    def test_complete_article_parsing(self):
        """Testa parsing completo de um artigo com títulos e autores"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
                <article-meta>
                    <title-group>
                        <article-title xml:lang="en">Impact of Climate Change on Biodiversity</article-title>
                        <trans-title-group xml:lang="pt">
                            <trans-title>Impacto das Mudanças Climáticas na Biodiversidade</trans-title>
                        </trans-title-group>
                    </title-group>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Johnson</surname>
                                <given-names>Alice</given-names>
                            </name>
                        </contrib>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Brown</surname>
                                <given-names>Robert</given-names>
                            </name>
                        </contrib>
                        <contrib contrib-type="author">
                            <collab>International Climate Research Group</collab>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>"""

        with TemporaryDirectory() as temp_dir:
            xml_path = os.path.join(temp_dir, "article.xml")
            with open(xml_path, "w") as fp:
                fp.write(xml_content)
            xml_instances = list(XMLWithPre.create(path=xml_path))
            xml_with_pre = xml_instances[0]

            # Test article_titles
            titles = xml_with_pre.article_titles
            expected_titles = [
                "Impact of Climate Change on Biodiversity",
                "Impacto das Mudanças Climáticas na Biodiversidade",
            ]
            self.assertEqual(sorted(titles), sorted(expected_titles))

            # Test authors
            authors = xml_with_pre.authors
            expected_authors = {
                "person": [
                    {"surname": "Johnson"},
                    {"surname": "Brown"},
                ],
                "collab": "International Climate Research Group",
            }
            self.assertEqual(authors, expected_authors)

    def test_property_caching(self):
        """Testa se as propriedades são corretamente cacheadas"""
        xml_content = """<?xml version="1.0" encoding="UTF-8"?>
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Test Caching</article-title>
                    </title-group>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Test</surname>
                                <given-names>Author</given-names>
                            </name>
                        </contrib>
                    </contrib-group>
                </article-meta>
            </front>
        </article>"""

        with TemporaryDirectory() as temp_dir:
            xml_path = os.path.join(temp_dir, "article.xml")
            with open(xml_path, "w") as fp:
                fp.write(xml_content)
            xml_instances = list(XMLWithPre.create(path=xml_path))
            xml_with_pre = xml_instances[0]

            # Primeira chamada - deve processar
            titles_1 = xml_with_pre.article_titles
            authors_1 = xml_with_pre.authors

            # Segunda chamada - deve usar cache
            titles_2 = xml_with_pre.article_titles
            authors_2 = xml_with_pre.authors

            # Deve retornar os mesmos valores
            self.assertEqual(titles_1, titles_2)
            self.assertEqual(authors_1, authors_2)

            # Deve ter usado cache (mesma referência)
            self.assertIs(titles_1, titles_2)
            self.assertIs(authors_1, authors_2)
