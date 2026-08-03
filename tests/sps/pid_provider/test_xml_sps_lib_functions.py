import os
import unittest
from tempfile import NamedTemporaryFile, TemporaryDirectory
from unittest import TestCase
from unittest.mock import MagicMock, mock_open, patch
from zipfile import ZIP_DEFLATED, ZipFile

from lxml import etree

from packtools.sps.pid_provider.xml_sps_lib import (
    GetXMLItemsError,
    XMLWithPre,
    get_xml_items,
    get_xml_with_pre_from_xml_file,
)

class TestGetXmlWithPreFromXmlFile(unittest.TestCase):

    @patch("packtools.sps.pid_provider.xml_sps_lib.get_xml_with_pre")
    @patch("builtins.open", new_callable=mock_open, read_data="<xml>conteudo utf-8</xml>")
    def test_get_xml_with_pre_from_xml_file_sucesso_utf8(
        self, mock_file_open, mock_get_xml_with_pre
    ):
        """Testa o fluxo de sucesso lendo o arquivo em UTF-8 de primeira."""
        path_ficticio = os.path.join("caminho", "falso", "artigo.xml")
        mock_xml_obj = XMLWithPre("", etree.fromstring("<article/>"))
        mock_get_xml_with_pre.return_value = mock_xml_obj

        resultado = get_xml_with_pre_from_xml_file(path_ficticio)

        # Garante que tentou abrir em utf-8
        mock_file_open.assert_called_once_with(path_ficticio, encoding="utf-8")
        mock_get_xml_with_pre.assert_called_once_with("<xml>conteudo utf-8</xml>")

        # Valida os atributos injetados no objeto XML
        self.assertEqual(mock_xml_obj.xml_file_path, path_ficticio)
        self.assertEqual(mock_xml_obj.filename, "artigo.xml")
        self.assertEqual(mock_xml_obj.xml_name, "artigo")

        # Valida o dicionário retornado
        self.assertEqual(
            resultado,
            {
                "xml_name": "artigo",
                "xml_with_pre": mock_xml_obj,
            },
        )

    @patch("packtools.sps.pid_provider.xml_sps_lib.get_xml_with_pre")
    @patch("builtins.open")
    def test_get_xml_with_pre_from_xml_file_fallback_encoding_iso(
        self, mock_file_open, mock_get_xml_with_pre
    ):
        """Testa se recorre ao iso-8859-1 caso ocorra erro ao abrir/ler em utf-8."""
        path_ficticio = "artigo_latin.xml"
        mock_xml_obj = MagicMock()
        mock_get_xml_with_pre.return_value = mock_xml_obj

        # Simula falha na 1ª abertura (utf-8) e sucesso na 2ª (iso-8859-1)
        handle_utf8 = mock_open(read_data="").return_value
        handle_utf8.read.side_effect = UnicodeDecodeError("utf-8", b"", 0, 1, "erro")
        
        handle_iso = mock_open(read_data="<xml>conteudo latin1</xml>").return_value

        mock_file_open.side_effect = [handle_utf8, handle_iso]

        resultado = get_xml_with_pre_from_xml_file(path_ficticio)

        # Verifica se tentou abrir com ambos os encodings
        self.assertEqual(mock_file_open.call_count, 2)
        mock_file_open.assert_any_call(path_ficticio, encoding="utf-8")
        mock_file_open.assert_any_call(path_ficticio, encoding="iso-8859-1")

        mock_get_xml_with_pre.assert_called_once_with("<xml>conteudo latin1</xml>")
        self.assertEqual(resultado["xml_name"], "artigo_latin")
        self.assertEqual(resultado["xml_with_pre"], mock_xml_obj)

    @patch("packtools.sps.pid_provider.xml_sps_lib.get_xml_with_pre")
    @patch("builtins.open", new_callable=mock_open, read_data="<xml>invalido")
    def test_get_xml_with_pre_from_xml_file_erro_no_parser(
        self, mock_file_open, mock_get_xml_with_pre
    ):
        """Testa o retorno do dicionário com informações de erro quando o parser falha."""
        path_ficticio = "documento_corrompido.xml"
        mock_get_xml_with_pre.side_effect = ValueError("Falha de Parse no XML")

        resultado = get_xml_with_pre_from_xml_file(path_ficticio)

        self.assertEqual(resultado["xml_name"], "documento_corrompido")
        self.assertEqual(resultado["error_message"], "Falha de Parse no XML")
        self.assertIn("ValueError", resultado["error_type"])
        self.assertIn("traceback", resultado)

    @patch("builtins.open", side_effect=FileNotFoundError("Arquivo inexistente"))
    def test_get_xml_with_pre_from_xml_file_erro_arquivo_nao_encontrado(self, mock_file_open):
        """Testa a captura de erro de arquivo inexistente em ambos os blocos try."""
        path_ficticio = "inexistente.xml"

        resultado = get_xml_with_pre_from_xml_file(path_ficticio)

        self.assertEqual(resultado["xml_name"], "inexistente")
        self.assertEqual(resultado["error_message"], "Arquivo inexistente")
        self.assertIn("FileNotFoundError", resultado["error_type"])
        self.assertIn("traceback", resultado)


class TestGetXmlItems(TestCase):
    """Testes para a função get_xml_items."""

    def test_get_xml_items_single_xml_file(self):
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <article><front><journal-meta><journal-id>abc</journal-id></journal-meta></front></article>"""

        with NamedTemporaryFile(
            suffix=".xml", mode="w", encoding="utf-8", delete=False
        ) as tmp:
            tmp.write(xml_content)
            tmp_path = tmp.name

        try:
            items = get_xml_items(tmp_path)
            self.assertEqual(len(items), 1)
            self.assertIn("xml_with_pre", items[0])
            self.assertEqual(items[0]["xml_with_pre"].filename, os.path.basename(tmp_path))
            self.assertEqual(items[0]["xml_with_pre"].xml_name, os.path.basename(tmp_path)[:-4])
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_get_xml_items_invalid_extension_raises_error(self):
        with NamedTemporaryFile(suffix=".txt", mode="w", delete=False) as tmp:
            tmp.write("invalid")
            tmp_path = tmp.name

        try:
            with self.assertRaises(GetXMLItemsError):
                get_xml_items(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    def test_get_xml_items_zip_file(self):
        xml_content = """<?xml version="1.0" encoding="utf-8"?>
        <article><front><journal-meta><journal-id>abc</journal-id></journal-meta></front></article>"""

        with TemporaryDirectory() as tmpdir:
            zip_path = os.path.join(tmpdir, "package.zip")
            with ZipFile(zip_path, "w", compression=ZIP_DEFLATED) as zf:
                zf.writestr("article1.xml", xml_content)

            items = list(get_xml_items(zip_path))
            self.assertEqual(len(items), 1)
            self.assertEqual(items[0]["xml_with_pre"].xml_name, "article1")
            self.assertEqual(items[0]["xml_with_pre"].filename, "article1.xml")
            self.assertIn("xml_with_pre", items[0])


if __name__ == "__main__":
    unittest.main()
