from unittest import TestCase

from packtools.sps.models.package import PackageWithErrata


class PackageTest(TestCase):
    def test_package_with_errata_is_valid(self):
        zip_path = ('./tests/sps/fixtures/package_errata.zip')
        obtained = PackageWithErrata(zip_path)
        self.assertTrue(obtained.is_valid())
