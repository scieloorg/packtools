from unittest import TestCase
from unittest.mock import patch
from zipfile import ZipFile

from dsm.utils import files


@patch("dsm.utils.files.requests_get")
class TestDownloadFilesAndCreateZipfile(TestCase):

    def test_download_files_and_create_zip_file_returns_files_info(
            self, mock_get):
        mock_get.side_effect = [
            b"image content"
        ]
        uri_and_file_items = [
            dict(
                uri="https://minio.scielo.br/documentstore/1414-431X/"
                "ywDM7t6mxHzCRWp7kGF9rXQ/"
                "fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg",
                name="1414-431X-bjmbr-54-10-e11439-gf01.jpg"),
        ]
        result = files.download_files_and_create_zip_file(
            zip_path="./tests/fixtures/new_package.zip",
            uri_and_file_items=uri_and_file_items,
        )
        self.assertEqual(
            [
                {
                    "uri":
                        "https://minio.scielo.br/documentstore/1414-431X/"
                        "ywDM7t6mxHzCRWp7kGF9rXQ/"
                        "fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg",
                    "name": '1414-431X-bjmbr-54-10-e11439-gf01.jpg',
                },
            ],
            result
        )

    def test_download_files_and_create_zip_file_create_files(self, mock_get):
        mock_get.side_effect = [
            b"image content",
            b"image content",
        ]
        uri_and_file_items = [
            {
                "uri":
                    "https://minio.scielo.br/documentstore/1414-431X/"
                    "ywDM7t6mxHzCRWp7kGF9rXQ/"
                    "fd89fb6a2a0f973016f2de7ee2b64b51ca573999.xml",
                "name": "document2_local.xml"
            },
            {
                "uri":
                    "https://minio.scielo.br/documentstore/1414-431X/"
                    "ywDM7t6mxHzCRWp7kGF9rXQ/"
                    "fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg",
                "name": "1414-431X-bjmbr-54-10-e11439-gf01.jpg"
            },
        ]
        files.download_files_and_create_zip_file(
            zip_path="./tests/fixtures/new_package.zip",
            uri_and_file_items=uri_and_file_items,
        )
        with ZipFile("./tests/fixtures/new_package.zip") as zf:
            self.assertListEqual([
                "document2_local.xml",
                "1414-431X-bjmbr-54-10-e11439-gf01.jpg",
                ],
                zf.namelist(),
            )
            self.assertEqual(
                b"image content",
                zf.read("1414-431X-bjmbr-54-10-e11439-gf01.jpg"),
            )

    def test_download_files_and_create_zip_file(self, mock_get):
        mock_get.side_effect = [
            b"image content",
            FileNotFoundError("Arquivo não encontrado"),
        ]
        uri_and_file_items = [
            dict(
                uri="https://minio.scielo.br/documentstore/1414-431X/"
                "ywDM7t6mxHzCRWp7kGF9rXQ/"
                "fd89fb6a2a0f973016f2de7ee2b64b51ca573999.xml",
                name="document2_local.xml",
            ),
            dict(
                uri="https://minio.scielo.br/documentstore/1414-431X/"
                "ywDM7t6mxHzCRWp7kGF9rXQ/"
                "fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg",
                name="1414-431X-bjmbr-54-10-e11439-gf01.jpg",
            ),
        ]
        result = files.download_files_and_create_zip_file(
            zip_path="./tests/fixtures/new_package.zip",
            uri_and_file_items=uri_and_file_items,
        )
        self.assertEqual(
            [
                {
                    "uri":
                        "https://minio.scielo.br/documentstore/1414-431X/"
                        "ywDM7t6mxHzCRWp7kGF9rXQ/"
                        "fd89fb6a2a0f973016f2de7ee2b64b51ca573999.xml",
                    "name": 'document2_local.xml',
                },
                {
                    "uri":
                        "https://minio.scielo.br/documentstore/1414-431X/"
                        "ywDM7t6mxHzCRWp7kGF9rXQ/"
                        "fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg",
                    "name": '1414-431X-bjmbr-54-10-e11439-gf01.jpg',
                    "error": "Arquivo não encontrado",
                },
            ],
            result
        )
