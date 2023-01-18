from unittest import TestCase

from packtools.sps.models.package import (
    PackageWithErrata,
    PackageErratumHasNoArticleXMLFileError,
    PackageErratumHasNoErrataXMLFileError,
    PackageErratumHasUnexpectedQuantityOfXMLFilesError
 )


class PackageTest(TestCase):
    def test_package_with_errata_xml_files_are_compatible(self):
        zip_path = './tests/sps/fixtures/errata_packages/with_compatible_xml_files.zip'
        obtained = PackageWithErrata(zip_path)
        self.assertTrue(obtained.is_valid())

    def test_package_with_errata_xml_files_are_incompatible(self):
        zip_path = './tests/sps/fixtures/errata_packages/with_incompatible_xml_files.zip'
        obtained = PackageWithErrata(zip_path)
        self.assertFalse(obtained.is_valid())

    def test_package_with_errata_raises_unexpected_quantity_of_xml_files_error(self):
        zip_path = './tests/sps/fixtures/errata_packages/with_three_xml_files.zip'

        with self.assertRaises(PackageErratumHasUnexpectedQuantityOfXMLFilesError):
            PackageWithErrata(zip_path)

    def test_package_with_errata_raises_no_errata_xml_file_error(self):
        zip_path = './tests/sps/fixtures/errata_packages/without_errata_xml.zip'
        
        with self.assertRaises(PackageErratumHasNoErrataXMLFileError):
            PackageWithErrata(zip_path)

    def test_package_with_errata_raises_no_article_xml_file_error(self):
        zip_path = './tests/sps/fixtures/errata_packages/without_article_xml.zip'
        
        with self.assertRaises(PackageErratumHasNoArticleXMLFileError):
            PackageWithErrata(zip_path)
