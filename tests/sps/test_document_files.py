from unittest import TestCase
from unittest.mock import MagicMock, patch, ANY

from dsm.core import (
    document_files,
    sps_package,
)
from dsm.utils import packages


class MockArticle:

    def __init__(self, xml="xml"):
        self.xml = xml
        self.package_name = "package_name"


class Test_get_xml_to_zip(TestCase):

    @patch("dsm.core.document_files.requests.requests_get_content")
    def test__get_xml_to_zip(self, mock_get):
        with open("./tests/fixtures/document2.xml") as fp:
            mock_get.return_value = fp.read()
        mock_document = MockArticle()
        result = document_files._get_xml_to_zip(mock_document)

        expected = [
            ("https://minio.scielo.br/documentstore/1414-431X/"
                "ywDM7t6mxHzCRWp7kGF9rXQ/"
                "fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg",
                "1414-431X-bjmbr-54-10-e11439-gf01.jpg"),
            ("https://minio.scielo.br/documentstore/1414-431X/"
                "ywDM7t6mxHzCRWp7kGF9rXQ/"
                "0c10c88b56f3f9b4f4eccfe9ddbca3fd581aac1b.jpg",
                "1414-431X-bjmbr-54-10-e11439-gf01-scielo-267x140.jpg"),
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertEqual(item[0], result.assets.items[i].uri)
                self.assertEqual(item[1], result.assets.items[i].filename)


class Test_get_assets_to_zip(TestCase):

    @patch("dsm.core.document_files.requests.requests_get_content")
    def test__get_assets_to_zip(self, mock_get):
        with open("./tests/fixtures/document2.xml") as fp:
            mock_get.return_value = fp.read()
        mock_document = MockArticle()
        xml_sps = document_files._get_xml_to_zip(mock_document)
        uris_and_filenames = document_files._get_assets_to_zip(xml_sps)

        expected = [
            ("https://minio.scielo.br/documentstore/1414-431X/"
                "ywDM7t6mxHzCRWp7kGF9rXQ/"
                "fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg",
                "1414-431X-bjmbr-54-10-e11439-gf01.jpg"),
            ("https://minio.scielo.br/documentstore/1414-431X/"
                "ywDM7t6mxHzCRWp7kGF9rXQ/"
                "0c10c88b56f3f9b4f4eccfe9ddbca3fd581aac1b.jpg",
                "1414-431X-bjmbr-54-10-e11439-gf01-scielo-267x140.jpg"),
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertEqual(item[0], uris_and_filenames[i]["uri"])
                self.assertEqual(item[1], uris_and_filenames[i]["name"])


class Test_get_renditions_to_zip(TestCase):

    @patch("dsm.core.document_files.requests.requests_get_content")
    def test__get_renditions_to_zip(self, mock_get):
        with open("./tests/fixtures/document2.xml") as fp:
            mock_get.return_value = fp.read()
        mock_doc = MockArticle()
        mock_doc.pdfs = [
            {
                "filename": "1414-431X-bjmbr-54-10-e11439.pdf",
                "url": "https://minio.scielo.br/documentstore/1414-431X/"
                "ywDM7t6mxHzCRWp7kGF9rXQ/"
                "0987c88b56f3f9b4f4eccfe9ddbca3fd581aac1b.pdf"
            }
        ]
        uris_and_filenames = document_files._get_renditions_to_zip(mock_doc)

        expected = [
            ("https://minio.scielo.br/documentstore/1414-431X/"
                "ywDM7t6mxHzCRWp7kGF9rXQ/"
                "0987c88b56f3f9b4f4eccfe9ddbca3fd581aac1b.pdf",
                "1414-431X-bjmbr-54-10-e11439.pdf"),
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertEqual(item[0], uris_and_filenames[i]["uri"])
                self.assertEqual(item[1], uris_and_filenames[i]["name"])


class Test_zip_files(TestCase):

    @patch("dsm.core.document_files.requests.requests_get_content")
    def test__zip_files(self, mock_get):
        xml_sps = sps_package.SPS_Package("./tests/fixtures/document2.xml")
        uris_and_filenames = [
            ("https://minio.scielo.br/documentstore/1414-431X/"
                "ywDM7t6mxHzCRWp7kGF9rXQ/"
                "fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg",
                "1414-431X-bjmbr-54-10-e11439-gf01.jpg"),
            ("https://minio.scielo.br/documentstore/1414-431X/"
                "ywDM7t6mxHzCRWp7kGF9rXQ/"
                "0c10c88b56f3f9b4f4eccfe9ddbca3fd581aac1b.jpg",
                "1414-431X-bjmbr-54-10-e11439-gf01-scielo-267x140.jpg"),
            ("https://minio.scielo.br/documentstore/1414-431X/"
                "ywDM7t6mxHzCRWp7kGF9rXQ/"
                "0987c88b56f3f9b4f4eccfe9ddbca3fd581aac1b.pdf",
                "1414-431X-bjmbr-54-10-e11439.pdf"),
        ]
        #zip_file_path = document_files._zip_files(xml_sps, uri_and_file_items)
        # for i, item in enumerate(expected):
        #     with self.subTest(i):
        #         self.assertEqual(item[0], uris_and_filenames[i]["uri"])
        #         self.assertEqual(item[1], uris_and_filenames[i]["name"])


class Test_register_file(TestCase):

    def test__register_file(self):
        mock_files_storage = MagicMock()
        mock_files_storage.register = MagicMock()
        result = document_files._register_file(
            files_storage=mock_files_storage,
            files_storage_folder='folder',
            file_path='./testes/fixtures/document.xml',
            zip_file_path=None,
        )
        mock_files_storage.register.assert_called_with(
            './testes/fixtures/document.xml',
            "folder",
            'document.xml',
        )

    @patch("dsm.core.document_files.ZipFile")
    def test__register_file_from_zipfile(self, mock_zipfile):
        mock_files_storage = MagicMock()
        mock_files_storage.register = MagicMock()
        mock_files_storage.register.return_value = (
            'https://files_storage/folder/bla.xml'
        )
        expected = dict(
            uri='https://files_storage/folder/bla.xml',
            name='document.xml',
        )
        result = document_files._register_file(
            files_storage=mock_files_storage,
            files_storage_folder='folder',
            file_path='./testes/fixtures/document.xml',
            zip_file_path='./testes/fixtures/package.zip',
        )

        mock_zipfile.assert_called_with("./testes/fixtures/package.zip")
        mock_files_storage.register.assert_called_with(
            ANY,
            "folder",
            'document.xml',
        )
        self.assertEqual(expected, result)


class Test_register_xml(TestCase):

    def test__register_xml(self):
        xml_sps = sps_package.SPS_Package(
            "./tests/fixtures/document2.xml")
        mock_files_storage = MagicMock()
        mock_files_storage.register = MagicMock()
        mock_files_storage.register.return_value = (
            'https://files_storage/folder/bla.xml'
        )

        result = document_files.register_xml(
            files_storage=mock_files_storage,
            files_storage_folder='folder',
            xml_sps=xml_sps,
        )
        mock_files_storage.register.assert_called_with(
            ANY,
            "folder",
            "1414-431X-bjmbr-54-10-e11439.xml"
        )
        self.assertEqual(
            {
                "uri": 'https://files_storage/folder/bla.xml',
                "name": "1414-431X-bjmbr-54-10-e11439.xml"
            },
            result
        )


class Test_register_renditions(TestCase):

    def test__register_renditions(self):
        mock_files_storage = MagicMock()
        mock_files_storage.register = MagicMock()
        mock_files_storage.register.side_effect = (
            'https://files_storage/folder/a1-es.pdf',
            'https://files_storage/folder/a1.pdf',
        )

        pkgs = packages._explore_folder(
            "./tests/fixtures/package_folder"
        )

        expected = [
            {
                "filename": '2318-0889-tinf-33-e200068-es.pdf',
                "mimetype": 'application/pdf',
                "lang": "es",
                "original_fname": "es_a01.pdf",
                "url": 'https://files_storage/folder/a1-es.pdf',
                "size_bytes": 1456147,
            },
            {
                "filename": '2318-0889-tinf-33-e200068.pdf',
                "mimetype": 'application/pdf',
                "lang": "original",
                "original_fname": "a01.pdf",
                "url": 'https://files_storage/folder/a1.pdf',
                "size_bytes": 1456147,
            },
        ]
        result = document_files.register_renditions(
            files_storage=mock_files_storage,
            files_storage_folder='folder',
            doc_package=pkgs['2318-0889-tinf-33-e200068'],
            classic_website_filename="a01.pdf",
        )
        self.assertListEqual(expected, result)


class Test_register_assets(TestCase):

    def test__register_assets(self):
        mock_files_storage = MagicMock()
        mock_files_storage.register = MagicMock()
        mock_files_storage.register.side_effect = (
            'https://files_storage/folder/a1-gf01.tif',
            'https://files_storage/folder/a1-gf02.tif',
        )
        pkgs = packages._explore_folder(
            "./tests/fixtures/package_folder"
        )
        expected = [
            {
                "filename": '2318-0889-tinf-33-e200068-gf01.tif',
                "uri": 'https://files_storage/folder/a1-gf01.tif',
            },
            {
                "filename": '2318-0889-tinf-33-e200068-gf02.tif',
                "uri": 'https://files_storage/folder/a1-gf02.tif',
            },
        ]
        xml_sps = sps_package.SPS_Package(
            "./tests/fixtures/package_folder/2318-0889-tinf-33-e200068.xml"
        )
        document_files.register_assets(
            files_storage=mock_files_storage,
            files_storage_folder='folder',
            assets_in_xml=xml_sps.assets.items,
            doc_package=pkgs['2318-0889-tinf-33-e200068'],
        )
        for i, asset in enumerate(xml_sps.assets.items):
            with self.subTest(i):
                self.assertEqual(expected[i]['uri'], asset.uri)
                self.assertEqual(expected[i]['filename'], asset.filename)
