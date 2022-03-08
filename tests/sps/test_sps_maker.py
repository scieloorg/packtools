from unittest import TestCase, skip
from packtools.sps.exceptions import SPSXMLFileError
from packtools.sps.models import sps_package
from packtools.sps import sps_maker

import os
import zipfile


class Test_get_xml_uri_and_name(TestCase):

    def test__get_xml_uri_and_name(self):
        xml_sps = sps_package.SPS_Package("./tests/sps/fixtures/document2.xml")
        xml_uri = 'https://kernel.scielo.br/documents/ywDM7t6mxHzCRWp7kGF9rXQ'

        xml_uri_and_name = sps_maker._get_xml_uri_and_name(xml_sps, xml_uri)
        expected = {'name': '1414-431X-bjmbr-54-10-e11439.xml', 'uri': 'https://kernel.scielo.br/documents/ywDM7t6mxHzCRWp7kGF9rXQ'}

        self.assertDictEqual(expected, xml_uri_and_name)


class Test_get_assets_uris_and_names(TestCase):

    def test__get_assets_uris_and_names(self):
        xml_sps = sps_package.SPS_Package("./tests/sps/fixtures/document2.xml")

        assets_uris_and_names = sps_maker._get_assets_uris_and_names(xml_sps)
        expected = [
            {
                'uri': 'https://minio.scielo.br/documentstore/1414-431X/'
                    'ywDM7t6mxHzCRWp7kGF9rXQ/'
                    'fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg',
                'name': '1414-431X-bjmbr-54-10-e11439-gf01.jpg'},
            {
                'uri': 'https://minio.scielo.br/documentstore/1414-431X/'
                'ywDM7t6mxHzCRWp7kGF9rXQ/'
                '0c10c88b56f3f9b4f4eccfe9ddbca3fd581aac1b.jpg',
                'name': '1414-431X-bjmbr-54-10-e11439-gf01-scielo-267x140.jpg'},
            {
                'uri': 'https://minio.scielo.br/documentstore/1414-431X/'
                'ywDM7t6mxHzCRWp7kGF9rXQ/'
                'afd520e3ff23a23f2c973bbbaa26094e9e50f487.jpg',
                'name': '1414-431X-bjmbr-54-10-e11439-gf02.jpg'},
            {
                'uri': 'https://minio.scielo.br/documentstore/1414-431X/'
                'ywDM7t6mxHzCRWp7kGF9rXQ/'
                'c2e5f2b77881866ef9820b03e99b3fedbb14cb69.jpg',
                'name': '1414-431X-bjmbr-54-10-e11439-gf02-scielo-267x140.jpg'
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertEqual(item["uri"], assets_uris_and_names[i]['uri'])
                self.assertEqual(item["name"], assets_uris_and_names[i]['name'])


class Test_get_zip_filename(TestCase):

    def test__get_zip_filename(self):
        xml_sps = sps_package.SPS_Package("./tests/sps/fixtures/document2.xml")

        zip_filename = sps_maker._get_zip_filename(xml_sps)
        expected = '1414-431X-bjmbr-54-10-e11439.zip'

        self.assertEqual(expected, zip_filename)


class Test_zip_files(TestCase):

    def test__zip_files(self):
        xml_sps = sps_package.SPS_Package("./tests/sps/fixtures/document2.xml")
        uris_and_names = [
            {
                'uri': 'https://minio.scielo.br/documentstore/1414-431X/'
                    'ywDM7t6mxHzCRWp7kGF9rXQ/'
                    'fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg',
                'name' :'1414-431X-bjmbr-54-10-e11439-gf01.jpg'
            },
            {
                'uri': 'https://minio.scielo.br/documentstore/1414-431X/'
                    'ywDM7t6mxHzCRWp7kGF9rXQ/'
                    '0c10c88b56f3f9b4f4eccfe9ddbca3fd581aac1b.jpg',
                'name': '1414-431X-bjmbr-54-10-e11439-gf01-scielo-267x140.jpg'
            }
        ]
        expected_files_list = sorted([f['name'] for f in uris_and_names])

        zip_filename = sps_maker._get_zip_filename(xml_sps)
        zip_file_path = sps_maker._zip_files_from_uris_and_names(zip_filename, uris_and_names)
        zf_files_list = sorted([f.filename for f in zipfile.ZipFile(zip_file_path).filelist])

        for i, item in enumerate(expected_files_list):
            with self.subTest(i):
                self.assertEqual(item, zf_files_list[i])


class Test_get_xml_sps_from_uri(TestCase):

    def test_get_sps_package_from_uri_raises_xml_link_error(self):
        xml_uri = 'some-invalid-link'
        with self.assertRaises(sps_maker.exceptions.SPSXMLLinkError):
            sps_maker._get_xml_sps_from_uri(xml_uri)

    def test_get_sps_package_from_uri_raises_sps_load_to_xml_error(self):
        xml_uri = 'https://scielo.br'

        with self.assertRaises(sps_maker.exceptions.SPSLoadToXMLError):
            sps_maker._get_xml_sps_from_uri(xml_uri)

    def test_get_xml_sps_from_uri_raises_download_xml_error(self):
        xml_uri = 'https://kernel.scielo.br'

        with self.assertRaises(sps_maker.exceptions.SPSHTTPResourceNotFoundError):
            sps_maker._get_xml_sps_from_uri(xml_uri)


class Test_get_xml_sps_from_path(TestCase):

    def test_get_sps_package_from_path_file_error(self):
        xml_path = './tests/sps/fixtures/document_unavailable.xml'

        with self.assertRaises(sps_maker.exceptions.SPSXMLFileError):
            sps_maker._get_xml_sps_from_path(xml_path)

    def test_get_sps_package_from_path_without_content_error(self):
        xml_path = './tests/sps/fixtures/document4.xml'

        with self.assertRaises(sps_maker.exceptions.SPSXMLContentError):
            sps_maker._get_xml_sps_from_path(xml_path)

    def test_get_sps_package_from_path_with_invalid_content(self):
        xml_path = './tests/sps/fixtures/document5.xml'

        with self.assertRaises(sps_maker.exceptions.SPSLoadToXMLError):
            sps_maker._get_xml_sps_from_path(xml_path)

    def test_get_sps_package_from_path_success(self):
        xml_path = './tests/sps/fixtures/document2.xml'
        xml_sps = sps_maker._get_xml_sps_from_path(xml_path)

        self.assertEqual(xml_sps.doi, '10.1590/1414-431X2021e11439')


class Test_make_package_from_uris(TestCase):

    def test_make_package_from_uris_raises_xml_download_error(self):
        xml_uri = "https://minio.scielo.br/documentstore/1414-431X/"
        "ywDM7t6mxHzCRWp7kGF9rXQ/"
        "fd89fb6a2a0f973016f2de7ee2b64b51ca573999.xml"

        renditions_uris_and_names = [{
            "uri": "https://minio.scielo.br/documentstore/1414-431X/"
                "ywDM7t6mxHzCRWp7kGF9rXQ/"
                "fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg",
            "name": "1414-431X-bjmbr-54-10-e11439-gf01.jpg"
        }]

        with self.assertRaises(sps_maker.exceptions.SPSHTTPResourceNotFoundError):
            sps_maker.make_package_from_uris(xml_uri, renditions_uris_and_names)

    @skip("Exige conexão com VPN SciELO")
    def test_make_package_from_uris_without_renditions(self):
        xml_uri_kernel = 'http://kernel.scielo.br/documents/ywDM7t6mxHzCRWp7kGF9rXQ'
        package_metadata = sps_maker.make_package_from_uris(xml_uri_kernel)

        expected_files = set([
            "1414-431X-bjmbr-54-10-e11439.xml",
            '1414-431X-bjmbr-54-10-e11439-gf01.jpg',
            '1414-431X-bjmbr-54-10-e11439-gf01-scielo-267x140.jpg',
            '1414-431X-bjmbr-54-10-e11439-gf02.jpg',
            '1414-431X-bjmbr-54-10-e11439-gf02-scielo-267x140.jpg'
        ])

        with zipfile.ZipFile(package_metadata['zip']) as zf:
            self.assertSetEqual(
                expected_files,
                set(zf.namelist()),
            )

    @skip("Exige conexão com VPN SciELO")
    def test_make_package_from_uris_has_expected_files(self):
        xml_uri_kernel = 'http://kernel.scielo.br/documents/ywDM7t6mxHzCRWp7kGF9rXQ'
        renditions_uris_and_names = [{
            "uri": "https://minio.scielo.br/documentstore/1414-431X/"
                "ywDM7t6mxHzCRWp7kGF9rXQ/"
                "aed92928a9b5e04e17fa5777d83e8430b9f98f6d.pdf",
            "name": "1414-431X-bjmbr-54-10-e11439.pdf"
        }]

        package_metadata = sps_maker.make_package_from_uris(xml_uri_kernel, renditions_uris_and_names)

        expected_files = set([
            "1414-431X-bjmbr-54-10-e11439.pdf",
            "1414-431X-bjmbr-54-10-e11439.xml",
            '1414-431X-bjmbr-54-10-e11439-gf01.jpg',
            '1414-431X-bjmbr-54-10-e11439-gf01-scielo-267x140.jpg',
            '1414-431X-bjmbr-54-10-e11439-gf02.jpg',
            '1414-431X-bjmbr-54-10-e11439-gf02-scielo-267x140.jpg'
        ])

        with zipfile.ZipFile(package_metadata['zip']) as zf:
            self.assertSetEqual(
                expected_files,
                set(zf.namelist()),
            )


class Test_make_package_from_paths(TestCase):

    def test_make_package_from_paths_raises_xml_path_error(self):
        paths = {
            'xml': "unavailable-file.xml",
            'renditions': [],
            'assets': []
        }

        with self.assertRaises(sps_maker.exceptions.SPSXMLFileError):
            sps_maker.make_package_from_paths(paths)

    def test_make_package_from_paths_raises_missing_key_error(self):
        paths = {}

        with self.assertRaises(sps_maker.exceptions.SPSMakePackageFromPathsMissingKeyError):
            sps_maker.make_package_from_paths(paths)

    def test_make_package_from_paths_has_expected_files(self):
        paths = {
            'xml': './tests/sps/fixtures/article_content/ca7d37e62e72840c1715ba83dda9893424ad31ec_kernel.xml',
            'renditions': ['./tests/sps/fixtures/article_content/aed92928a9b5e04e17fa5777d83e8430b9f98f6d.pdf'],
            'assets': [
                './tests/sps/fixtures/article_content/0c10c88b56f3f9b4f4eccfe9ddbca3fd581aac1b.jpg',
                './tests/sps/fixtures/article_content/c2e5f2b77881866ef9820b03e99b3fedbb14cb69.jpg',
                './tests/sps/fixtures/article_content/fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg',
                './tests/sps/fixtures/article_content/afd520e3ff23a23f2c973bbbaa26094e9e50f487.jpg',
            ]
        }

        package_metadata = sps_maker.make_package_from_paths(paths)

        expected_files = set([
            'aed92928a9b5e04e17fa5777d83e8430b9f98f6d.pdf',
            '1414-431X-bjmbr-54-10-e11439.xml',
            '1414-431X-bjmbr-54-10-e11439-gf01-scielo-267x140.jpg',
            '1414-431X-bjmbr-54-10-e11439-gf02.jpg',
            '1414-431X-bjmbr-54-10-e11439-gf02-scielo-267x140.jpg',
            '1414-431X-bjmbr-54-10-e11439-gf01.jpg',
        ])

        with zipfile.ZipFile(package_metadata['zip']) as zf:
            self.assertSetEqual(
                expected_files,
                set(zf.namelist()),
            )


class Test_remove_invalid_uris(TestCase):

    def test_remove_invalid_uris(self):
        paths = [
            {"uri": "article_content/ca7d37e62e72840c1715ba83dda9893424ad31ec_kernel.xml", "name": ""},
            {"uri": "fixtures/article_content/fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg", "name": ""},
            {"uri": "https://minio.scielo.br/documentstore/1414-431X/", "name": ""},
            {"uri": "https://minio.scielo.br/documentstore/1414-431X/", "name": ""}
        ]

        expected = [
            {"uri": "https://minio.scielo.br/documentstore/1414-431X/", "name": ""},
            {"uri": "https://minio.scielo.br/documentstore/1414-431X/", "name": ""}
        ]

        obtained = sps_maker._remove_invalid_uris(paths)

        self.assertListEqual(expected, obtained)


class Test_check_keys_and_files(TestCase):

    def test_check_keys_and_files_success(self):
        paths = {
            'xml': './tests/sps/fixtures/article_content/ca7d37e62e72840c1715ba83dda9893424ad31ec_kernel.xml',
            'renditions': ['./tests/sps/fixtures/article_content/aed92928a9b5e04e17fa5777d83e8430b9f98f6d.pdf'],
            'assets': [
                './tests/sps/fixtures/article_content/0c10c88b56f3f9b4f4eccfe9ddbca3fd581aac1b.jpg',
                './tests/sps/fixtures/article_content/c2e5f2b77881866ef9820b03e99b3fedbb14cb69.jpg',
                './tests/sps/fixtures/article_content/fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg',
                './tests/sps/fixtures/article_content/afd520e3ff23a23f2c973bbbaa26094e9e50f487.jpg',
            ]
        }

        self.assertTrue(sps_maker._check_keys_and_files(paths))

    def test_check_keys_and_files_raises(self):
        paths = {
            "xml": "/home/user/fd89fb6a2a0f973016f2de7ee2b64b51ca573999.xml",
            "renditions": [
                "/home/user/aed92928a9b5e04e17fa5777d83e8430b9f98f6d.pdf",
                ...
            ],
            "assets": [
                "/home/user/fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg",
                ...,
            ]
        }

        with self.assertRaises(SPSXMLFileError):
            sps_maker._check_keys_and_files(paths)


class Test_get_canonical_files_paths(TestCase):

    def test_get_canonical_files_paths(self):
        xml_path = './tests/sps/fixtures/article_content/ca7d37e62e72840c1715ba83dda9893424ad31ec_kernel.xml'
        xml_sps = sps_maker._get_xml_sps_from_path(xml_path)
        paths = {
            'xml': './tests/sps/fixtures/article_content/ca7d37e62e72840c1715ba83dda9893424ad31ec_kernel.xml',
            'renditions': ['./tests/sps/fixtures/article_content/aed92928a9b5e04e17fa5777d83e8430b9f98f6d.pdf'],
            'assets': [
                './tests/sps/fixtures/article_content/0c10c88b56f3f9b4f4eccfe9ddbca3fd581aac1b.jpg',
                './tests/sps/fixtures/article_content/c2e5f2b77881866ef9820b03e99b3fedbb14cb69.jpg',
                './tests/sps/fixtures/article_content/fd89fb6a2a0f973016f2de7ee2b64b51ca573999.jpg',
                './tests/sps/fixtures/article_content/afd520e3ff23a23f2c973bbbaa26094e9e50f487.jpg',
            ]
        }

        expected_files_names = sorted([
            '1414-431X-bjmbr-54-10-e11439.xml',
            '1414-431X-bjmbr-54-10-e11439-gf01-scielo-267x140.jpg',
            '1414-431X-bjmbr-54-10-e11439-gf02-scielo-267x140.jpg',
            '1414-431X-bjmbr-54-10-e11439-gf01.jpg',
            '1414-431X-bjmbr-54-10-e11439-gf02.jpg',
            'aed92928a9b5e04e17fa5777d83e8430b9f98f6d.pdf'
        ])

        obtained_file_names = sorted([os.path.basename(f) for f in sps_maker._get_canonical_files_paths(xml_sps, paths)])

        self.assertListEqual(expected_files_names, obtained_file_names)
