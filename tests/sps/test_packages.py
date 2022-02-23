from unittest import TestCase

from packtools.sps.models import packages


class Test_get_component(TestCase):

    def test__eval_file_as_pdf(self):
        expected = {
            "component_id": "abcd-suppl01.pdf",
            "component_name": "abcd-suppl01",
            "file_path": "abcd-suppl01.pdf",
            "ftype": "pdf",
        }
        result = packages._eval_file(
            prefix="abcd", file_path="abcd-suppl01.pdf")
        self.assertEqual(expected, result)

    def test__eval_file_as_es_pdf(self):
        expected = {
            "component_id": "es",
            "file_path": "abcd-es.pdf",
        }
        result = packages._eval_file(
            prefix="abcd", file_path="abcd-es.pdf")
        self.assertEqual(expected, result)

    def test__eval_file_as_original_pdf(self):
        expected = {
            "component_id": "original",
            "file_path": "abcd.pdf",
        }
        result = packages._eval_file(
            prefix="abcd", file_path="abcd.pdf")
        self.assertEqual(expected, result)

    def test__eval_file_as_jpg(self):
        expected = {
            "component_id": "abcd-gf01.jpg",
            "component_name": "abcd-gf01",
            "file_path": "abcd-gf01.jpg",
            "ftype": "jpg",
        }
        result = packages._eval_file(
            prefix="abcd", file_path="abcd-gf01.jpg")
        self.assertEqual(expected, result)

    def test__eval_file_as_png(self):
        expected = {
            "component_id": "abcd-gf01.png",
            "component_name": "abcd-gf01",
            "file_path": "abcd-gf01.png",
            "ftype": "png",
        }
        result = packages._eval_file(
            prefix="abcd", file_path="abcd-gf01.png")
        self.assertEqual(expected, result)

    def test__eval_file_as_tif(self):
        expected = {
            "component_id": "abcd-gf01.tif",
            "component_name": "abcd-gf01",
            "file_path": "abcd-gf01.tif",
            "ftype": "tif",
        }
        result = packages._eval_file(
            prefix="abcd", file_path="abcd-gf01.tif")
        self.assertEqual(expected, result)

    def test__eval_file_returns_none(self):
        expected = None
        result = packages._eval_file(
            prefix="abcd", file_path="abcd-gf01.xml")
        self.assertEqual(expected, result)

    def test__eval_file_returns_none_because_prefix_doesnot_match(self):
        expected = None
        result = packages._eval_file(
            prefix="cd", file_path="abcd-gf01.xml")
        self.assertEqual(expected, result)


class Test_group_files_by_xml_filename(TestCase):

    def test__group_files_by_xml_filename(self):
        pkg1 = packages.Package("source", "name")
        pkg11 = packages.Package("source", "name")

        pkg11.xml = "a11.xml"
        pkg11._assets = {
            "a11-gf01-es.tiff": "a11-gf01-es.tiff",
            "a11-gf02-es.tiff": "a11-gf02-es.tiff",
            "a11-suppl-es.pdf": "a11-suppl-es.pdf",
        }
        pkg11._renditions = {
            "es": "a11-es.pdf",
            "original": "a11.pdf",
        }

        pkg1.xml = "a1.xml"
        pkg1._assets = {
            "a1-gf01.tiff": "a1-gf01.tiff",
            "a1-gf01.jpg": "a1-gf01.jpg",
            "a1-gf02.tiff": "a1-gf02.tiff",
        }
        pkg1._renditions = {
            "en": "a1-en.pdf",
            "original": "a1.pdf",
        }
        xmls = [
            "a1.xml", "a11.xml",
        ]
        files = [
            "a1-en.pdf",
            "a1-gf01.jpg",
            "a1-gf01.tiff",
            "a1-gf02.tiff",
            "a1.pdf",
            "a1.xml",
            "a11-es.pdf",
            "a11-gf01-es.tiff",
            "a11-gf02-es.tiff",
            "a11-suppl-es.pdf",
            "a11.pdf",
            "a11.xml",
        ]
        result = packages._group_files_by_xml_filename("source", xmls, files)
        self.assertEqual(pkg11.xml, result["a11"].xml)
        self.assertEqual(pkg11._assets, result["a11"]._assets)
        self.assertEqual(pkg11._renditions, result["a11"]._renditions)
        self.assertEqual(pkg1.xml, result["a1"].xml)
        self.assertEqual(pkg1._assets, result["a1"]._assets)
        self.assertEqual(pkg1._renditions, result["a1"]._renditions)


class TestZipFile(TestCase):

    def test_explore_zipfile_returns_zip_data(self):
        """
        2318-0889-tinf-33-e200071-gf01.tif
        2318-0889-tinf-33-e200071-gf03.tif
        2318-0889-tinf-33-e200071.pdf
        2318-0889-tinf-33-e200071-gf02.tif
        2318-0889-tinf-33-e200071-gf04.tif
        2318-0889-tinf-33-e200071.xml
        """
        pkg = packages.Package(
            "./tests/fixtures/package.zip", "package")
        pkg.xml = "2318-0889-tinf-33-e200071.xml"
        pkg._renditions = {
            "original": "2318-0889-tinf-33-e200071.pdf"
        }
        pkg._assets = {
            "2318-0889-tinf-33-e200071-gf01.tif":
                "2318-0889-tinf-33-e200071-gf01.tif",
            "2318-0889-tinf-33-e200071-gf02.tif":
                "2318-0889-tinf-33-e200071-gf02.tif",
            "2318-0889-tinf-33-e200071-gf03.tif":
                "2318-0889-tinf-33-e200071-gf03.tif",
            "2318-0889-tinf-33-e200071-gf04.tif":
                "2318-0889-tinf-33-e200071-gf04.tif",
        }
        result = packages._explore_zipfile(
            "./tests/fixtures/package.zip")
        self.assertEqual(
            pkg.xml,
            result["2318-0889-tinf-33-e200071"].xml)
        self.assertEqual(
            pkg._assets,
            result["2318-0889-tinf-33-e200071"]._assets)
        self.assertEqual(
            pkg._renditions,
            result["2318-0889-tinf-33-e200071"]._renditions)

    def test_explore_zipfile_with_subdir_returns_zip_data(self):
        """
        2318-0889-tinf-33-0121
        ├── 0103-3786-tinf-33-e200009.pdf
        ├── 0103-3786-tinf-33-e200009.xml
        ├── 2318-0889-tinf-33-e200025-gf01.tif
        ├── 2318-0889-tinf-33-e200025-gf02.tif
        ├── 2318-0889-tinf-33-e200025.pdf
        ├── 2318-0889-tinf-33-e200025.xml
        ├── 2318-0889-tinf-33-e200039-gf01.tif
        ├── 2318-0889-tinf-33-e200039.pdf
        ├── 2318-0889-tinf-33-e200039.xml
        ├── 2318-0889-tinf-33-e200050.pdf
        └── 2318-0889-tinf-33-e200050.xml
        """
        result = packages._explore_zipfile(
            "./tests/fixtures/package_with_subdir.zip")
        pkg_09 = packages.Package(
            "./tests/fixtures/package_with_subdir.zip", "package")
        pkg_09.xml = "2318-0889-tinf-33-0121/0103-3786-tinf-33-e200009.xml"
        pkg_09._renditions = {
            "original": "2318-0889-tinf-33-0121/0103-3786-tinf-33-e200009.pdf"
        }

        pkg_25 = packages.Package(
            "./tests/fixtures/package_with_subdir.zip", "package")
        pkg_25.xml = "2318-0889-tinf-33-0121/2318-0889-tinf-33-e200025.xml"
        pkg_25._renditions = {
            "original": "2318-0889-tinf-33-0121/2318-0889-tinf-33-e200025.pdf"
        }
        pkg_25._assets = {
            "2318-0889-tinf-33-e200025-gf01.tif":
                "2318-0889-tinf-33-0121/"
                "2318-0889-tinf-33-e200025-gf01.tif",
            "2318-0889-tinf-33-e200025-gf02.tif":
                "2318-0889-tinf-33-0121/"
                "2318-0889-tinf-33-e200025-gf02.tif"
        }

        pkg_39 = packages.Package(
            "./tests/fixtures/package_with_subdir.zip", "package")
        pkg_39.xml = "2318-0889-tinf-33-0121/2318-0889-tinf-33-e200039.xml"
        pkg_39._renditions = {
            "original": "2318-0889-tinf-33-0121/2318-0889-tinf-33-e200039.pdf"
        }
        pkg_39._assets = {
            "2318-0889-tinf-33-e200039-gf01.tif":
                "2318-0889-tinf-33-0121/"
                "2318-0889-tinf-33-e200039-gf01.tif"
        }

        pkg_50 = packages.Package(
            "./tests/fixtures/package_with_subdir.zip", "package")
        pkg_50.xml = "2318-0889-tinf-33-0121/2318-0889-tinf-33-e200050.xml"
        pkg_50._renditions = {
            "original": "2318-0889-tinf-33-0121/2318-0889-tinf-33-e200050.pdf"
        }

        self.assertEqual(
            pkg_09.xml,
            result["0103-3786-tinf-33-e200009"].xml)
        self.assertEqual(
            pkg_50.xml,
            result["2318-0889-tinf-33-e200050"].xml)
        self.assertEqual(
            pkg_39.xml,
            result["2318-0889-tinf-33-e200039"].xml)
        self.assertEqual(
            pkg_25.xml,
            result["2318-0889-tinf-33-e200025"].xml)

        self.assertEqual(
            pkg_09._assets,
            result["0103-3786-tinf-33-e200009"]._assets)
        self.assertEqual(
            pkg_50._assets,
            result["2318-0889-tinf-33-e200050"]._assets)
        self.assertEqual(
            pkg_39._assets,
            result["2318-0889-tinf-33-e200039"]._assets)
        self.assertEqual(
            pkg_25._assets,
            result["2318-0889-tinf-33-e200025"]._assets)

        self.assertEqual(
            pkg_09._renditions,
            result["0103-3786-tinf-33-e200009"]._renditions)
        self.assertEqual(
            pkg_50._renditions,
            result["2318-0889-tinf-33-e200050"]._renditions)
        self.assertEqual(
            pkg_39._renditions,
            result["2318-0889-tinf-33-e200039"]._renditions)
        self.assertEqual(
            pkg_25._renditions,
            result["2318-0889-tinf-33-e200025"]._renditions)


class TestFolder(TestCase):

    def test__explore_folder_returns_zip_data(self):
        """
        2318-0889-tinf-33-e200057.pdf
        2318-0889-tinf-33-e200057.xml
        2318-0889-tinf-33-e200068.xml
        2318-0889-tinf-33-e200068.pdf
        2318-0889-tinf-33-e200068-gf01.tif
        2318-0889-tinf-33-e200068-gf02.tif
        """
        result = packages._explore_folder("./tests/fixtures/package_folder")
        pkg1 = packages.Package("./tests/fixtures/package_folder", "folder")
        pkg1.xml = "2318-0889-tinf-33-e200057.xml"
        pkg1._renditions = {
            "original":
            "./tests/fixtures/package_folder/2318-0889-tinf-33-e200057.pdf"}

        pkg2 = packages.Package("./tests/fixtures/package_folder", "folder")
        pkg2.xml = "2318-0889-tinf-33-e200068.xml"
        pkg2._renditions = {
            "original":
            "./tests/fixtures/package_folder/2318-0889-tinf-33-e200068.pdf",
            "es":
            "./tests/fixtures/package_folder/2318-0889-tinf-33-e200068-es.pdf",
        }
        pkg2._assets = {
            "2318-0889-tinf-33-e200068-gf01.tif":
                "./tests/fixtures/package_folder/"
                "2318-0889-tinf-33-e200068-gf01.tif",
            "2318-0889-tinf-33-e200068-gf02.tif":
                "./tests/fixtures/package_folder/"
                "2318-0889-tinf-33-e200068-gf02.tif"
        }

        self.assertEqual(
            pkg1.xml,
            result["2318-0889-tinf-33-e200057"].xml
        )
        self.assertEqual(
            pkg1._assets,
            result["2318-0889-tinf-33-e200057"]._assets
        )
        self.assertEqual(
            pkg1._renditions,
            result["2318-0889-tinf-33-e200057"]._renditions
        )

        self.assertEqual(
            pkg2.xml,
            result["2318-0889-tinf-33-e200068"].xml
        )
        self.assertEqual(
            pkg2._assets,
            result["2318-0889-tinf-33-e200068"]._assets
        )
        self.assertEqual(
            pkg2._renditions,
            result["2318-0889-tinf-33-e200068"]._renditions
        )
