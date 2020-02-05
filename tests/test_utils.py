#coding: utf-8
from __future__ import unicode_literals
import unittest
import zipfile
import tempfile
import os
import io
import shutil

from PIL import Image

from packtools import utils, exceptions


try:
    from unittest import mock
except:
    import mock


BASE_XML = b"""<?xml version="1.0" encoding="UTF-8"?>
<article xmlns:xlink="http://www.w3.org/1999/xlink"
     dtd-version="1.0"
     article-type="research-article"
     xml:lang="en">
<front>
<article-meta>
</article-meta>
</front>
<body>
<sec>
  <p>The Eh measurements... <xref ref-type="disp-formula" rid="e01">equation 1</xref>(in mV):</p>
  <disp-formula id="e01">
    <graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif"/>
  </disp-formula>
  <p>We also used an... <inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff"/>.</p>
</sec>
<fig id="f03">
    <label>Fig. 3</label>
    <caption>
        <title>titulo da imagem</title>
    </caption>
    <alternatives>
        <graphic xlink:href="1234-5678-rctb-45-05-0110-gf03.tiff"/>
        <graphic xlink:href="1234-5678-rctb-45-05-0110-gf03.png" specific-use="scielo-web"/>
        <graphic xlink:href="1234-5678-rctb-45-05-0110-gf03.thumbnail.jpg" specific-use="scielo-web" content-type="scielo-267x140"/>
    </alternatives>
</fig>
<p>We also used an ... based on the equation:<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e04.tif"/>.</p>
</body>
</article>"""


def create_image_file(filename, format):
    new_image = Image.new("RGB", (50, 50))
    new_image.save(filename, format)


class CachedMethodTests(unittest.TestCase):
    def test_without_params(self):

        class A(object):
            def __init__(self):
                self.counter = 0

            @utils.cachedmethod
            def foo(self):
                self.counter += 1
                return 'bar'

        a = A()
        self.assertEqual(a.counter, 0)

        self.assertEqual(a.foo(), 'bar')
        self.assertEqual(a.counter, 1)

        self.assertEqual(a.foo(), 'bar')
        self.assertEqual(a.counter, 1)

    def test_with_params(self):

        class A(object):
            def __init__(self):
                self.counter = 0

            @utils.cachedmethod
            def sum(self, a, b):
                self.counter += 1
                return a + b

        a = A()
        self.assertEqual(a.counter, 0)

        self.assertEqual(a.sum(2, 2), 4)
        self.assertEqual(a.counter, 1)

        self.assertEqual(a.sum(2, 3), 5)
        self.assertEqual(a.counter, 2)

        self.assertEqual(a.sum(2, 2), 4)
        self.assertEqual(a.counter, 2)


class XrayTests(unittest.TestCase):

    def _make_test_archive(self, arch_data):
        fp = tempfile.NamedTemporaryFile()
        with zipfile.ZipFile(fp, 'w') as zipfp:
            for archive, data in arch_data:
                zipfp.writestr(archive, data)

        return fp

    def test_members_are_shown(self):
        arch = self._make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>'),
             ('jar.xml', u'<root><name>bar</name></root>')])

        with utils.Xray.fromfile(arch.name) as xray:
            self.assertEqual(sorted(xray.show_members()),
                    sorted(['bar.xml', 'jar.xml']))

    def test_get_members_returns_empty(self):
        arch = self._make_test_archive([])

        with utils.Xray.fromfile(arch.name) as xray:
            self.assertEqual(xray.show_members(), [])

    def test_get_file(self):
        arch = self._make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>'),
             ('jar.xml', u'<root><name>bar</name></root>')])

        with utils.Xray.fromfile(arch.name) as xray:
            member = xray.get_file('bar.xml')
            self.assertEqual(member.read(), b'<root><name>bar</name></root>')

    def test_get_file_for_nonexisting_member(self):
        arch = self._make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>'),
             ('jar.xml', u'<root><name>bar</name></root>')])

        with utils.Xray.fromfile(arch.name) as xray:
            self.assertRaises(ValueError, lambda: xray.get_file('foo.xml'))

    def test_show_sorted_members(self):
        arch = self._make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>'),
             ('jar.xml', u'<root><name>bar</name></root>')])

        with utils.Xray.fromfile(arch.name) as xray:
            self.assertEqual(xray.show_sorted_members(),
                    {'xml': ['bar.xml', 'jar.xml']})

    def test_show_sorted_members_is_caseinsensitive(self):
        arch = self._make_test_archive(
            [('bar.xml', u'<root><name>bar</name></root>'),
             ('jar.XML', u'<root><name>bar</name></root>')])

        with utils.Xray.fromfile(arch.name) as xray:
            self.assertEqual(xray.show_sorted_members(),
                    {'xml': ['bar.xml', 'jar.XML']})


class ResolveSchematronFilepathTests(unittest.TestCase):
    def setUp(self):
        from packtools.catalogs import catalog
        self.sch_schemas = catalog.SCH_SCHEMAS

    def test_builtin_lookup(self):
        for name, path in self.sch_schemas.items():
            self.assertEqual(utils.resolve_schematron_filepath('@'+name), path)

    def test_resolve_unsupported_types(self):
        self.assertRaises(TypeError,
                lambda: utils.resolve_schematron_filepath(None))

    def test_non_existing_builtin(self):
        self.assertRaises(ValueError, 
                lambda: utils.resolve_schematron_filepath('@notexists'))

    def test_existing_filepath(self):
        path = list(self.sch_schemas.values())[0]  # get the first item
        self.assertEqual(utils.resolve_schematron_filepath(path), path)

    def test_non_existing_filepath(self):
        path = list(self.sch_schemas.values())[0] + '.notexists'
        self.assertRaises(ValueError, 
                lambda: utils.resolve_schematron_filepath(path))


class TestWebImageGenerator(unittest.TestCase):
    def setUp(self):
        self.extracted_package = tempfile.mkdtemp(".")
        image_files = (
            ("image_tiff_1.tiff", "TIFF"),
            ("image_tiff_2.tif", "TIFF"),
            ("image_jpg_3.jpg", "JPEG"),
        )
        for image_filename, format in image_files:
            image_file_path = os.path.join(self.extracted_package, image_filename)
            create_image_file(image_file_path, format)

    def tearDown(self):
        shutil.rmtree(self.extracted_package)

    def test_create_WebImageGenerator(self):
        web_image_generator = utils.WebImageGenerator(
            "image_tiff_1.tiff", self.extracted_package
        )
        self.assertEqual(
            web_image_generator.image_file_path,
            os.path.join(self.extracted_package, "image_tiff_1.tiff"),
        )

    def test_convert2png(self):
        web_image_generator = utils.WebImageGenerator(
            "image_tiff_2.tif", self.extracted_package
        )
        web_image_generator.convert2png()
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.extracted_package,
                    os.path.splitext("image_tiff_2.tif")[0] + ".png",
                )
            )
        )

    def test_create_thumbnail(self):
        filename = os.path.join(self.extracted_package, "image_tiff_1.png")
        create_image_file(filename, "PNG")

        web_image_generator = utils.WebImageGenerator(
            "image_tiff_1.png", self.extracted_package
        )
        web_image_generator.create_thumbnail()
        thumbnail_filename = os.path.splitext(filename)[0] + ".thumbnail.jpg"
        self.assertTrue(os.path.exists(thumbnail_filename))


class TestXMLWebOptimiser(unittest.TestCase):
    def setUp(self):
        self.xml_file = utils.XML(io.BytesIO(BASE_XML))
        self.xml_filename = "1234-5678-rctb-45-05-0110.xml"
        self.xml_web_optimiser = utils.XMLWebOptimiser(self.xml_file, self.xml_filename)

    def test_create_XMLWebOptimiser(self):
        self.assertEqual(self.xml_web_optimiser.xml_file, self.xml_file)
        self.assertEqual(self.xml_web_optimiser.xml_filename, self.xml_filename)

    def test_get_all_images_to_optimise(self):
        images = self.xml_web_optimiser._get_all_images_to_optimise()
        expected = [
            "1234-5678-rctb-45-05-0110-e01.tif",
            "1234-5678-rctb-45-05-0110-e02.tiff",
            "1234-5678-rctb-45-05-0110-e04.tif",
        ]
        result = [image for image in images]
        self.assertEqual(len(result), len(expected))
        for image, expected_filename in zip(result, expected):
            image_filename, image_element = image
            self.assertEqual(expected_filename, image_filename)

    def test_get_all_images_to_thumbnail(self):
        images = self.xml_web_optimiser._get_all_images_to_thumbnail()

        expected = ["1234-5678-rctb-45-05-0110-e01.tif"]
        result = [image for image in images]
        self.assertEqual(len(result), len(expected))
        for image, expected_filename in zip(result, expected):
            image_filename, image_element = image
            self.assertEqual(expected_filename, image_filename)

    @mock.patch("packtools.utils.LOGGER")
    def test_get_optimised_xml_get_image_error(self, MockLogger):
        def mock_get_optimised_image(filename):
            if "1234-5678-rctb-45-05-0110-e02.tiff" in filename:
                raise exceptions.SPPackageError(
                    "Error reading 1234-5678-rctb-45-05-0110-e02.tiff"
                )
            return os.path.splitext(filename)[0] + ".png"

        def mock_get_image_thumbnail(filename):
            if "1234-5678-rctb-45-05-0110-e01.tif" in filename:
                raise exceptions.SPPackageError(
                    "Error reading 1234-5678-rctb-45-05-0110-e01.tif"
                )
            return os.path.splitext(filename)[0] + ".thumbnail.jpg"

        expected = [
            ("1234-5678-rctb-45-05-0110-e01.png",),
            (
                "1234-5678-rctb-45-05-0110-gf03.png",
                "1234-5678-rctb-45-05-0110-gf03.thumbnail.jpg",
            ),
            ("1234-5678-rctb-45-05-0110-e04.png",),
        ]
        xml_result = self.xml_web_optimiser.get_optimised_xml(
            mock_get_optimised_image, mock_get_image_thumbnail
        )
        MockLogger.error.assert_any_call(
            "Error optimising image: %s",
            "Error reading 1234-5678-rctb-45-05-0110-e02.tiff",
        )
        MockLogger.error.assert_any_call(
            "Error creating image thumbnail: %s",
            "Error reading 1234-5678-rctb-45-05-0110-e01.tif",
        )
        for alternatives, expected_files in zip(
            xml_result.findall("//alternatives"), expected
        ):
            path = './graphic[@specific-use="scielo-web"]|./inline-graphic[@specific-use="scielo-web"]'
            for image, expected_href in zip(alternatives.xpath(path), expected_files):
                self.assertEqual(
                    image.attrib["{http://www.w3.org/1999/xlink}href"], expected_href
                )

    def test_get_optimised_xml_ok(self):
        def mock_get_optimised_image(filename):
            return os.path.splitext(filename)[0] + ".png"

        def mock_get_image_thumbnail(filename):
            return os.path.splitext(filename)[0] + ".thumbnail.jpg"

        expected = [
            (
                "1234-5678-rctb-45-05-0110-e01.png",
                "1234-5678-rctb-45-05-0110-e01.thumbnail.jpg",
            ),
            ("1234-5678-rctb-45-05-0110-e02.png",),
            (
                "1234-5678-rctb-45-05-0110-gf03.png",
                "1234-5678-rctb-45-05-0110-gf03.thumbnail.jpg",
            ),
            ("1234-5678-rctb-45-05-0110-e04.png",),
        ]
        xml_result = self.xml_web_optimiser.get_optimised_xml(
            mock_get_optimised_image, mock_get_image_thumbnail
        )
        for alternatives, expected_files in zip(
            xml_result.findall("//alternatives"), expected
        ):
            path = './graphic[@specific-use="scielo-web"]|./inline-graphic[@specific-use="scielo-web"]'
            for image, expected_href in zip(alternatives.xpath(path), expected_files):
                self.assertEqual(
                    image.attrib["{http://www.w3.org/1999/xlink}href"], expected_href
                )


class TestSPPackage(unittest.TestCase):
    def setUp(self):
        self.temp_package_dir = tempfile.mkdtemp(".")
        self.temp_img_dir = tempfile.mkdtemp(".")
        self.tmp_package = os.path.join(self.temp_package_dir, "sps_package.zip")
        self.extracted_package = os.path.splitext(self.tmp_package)[0]
        self.optimised_package = self.extracted_package + "_optimised.zip"

        with zipfile.ZipFile(self.tmp_package, "a") as self.archive:
            xml_file_path = os.path.join(self.temp_img_dir, "somedocument.xml")
            with open(xml_file_path, "wb") as xml_file:
                xml_file.write(BASE_XML)
            self.archive.write(xml_file_path, "somedocument.xml")
            image_files = (
                ("1234-5678-rctb-45-05-0110-e01.tif", "TIFF"),
                ("1234-5678-rctb-45-05-0110-e02.tiff", "TIFF"),
                ("1234-5678-rctb-45-05-0110-gf03.tiff", "TIFF"),
                ("1234-5678-rctb-45-05-0110-gf03.png", "PNG"),
                ("1234-5678-rctb-45-05-0110-gf03.thumbnail.jpg", "JPEG"),
                ("1234-5678-rctb-45-05-0110-e04.tif", "TIFF"),
            )
            for image_filename, format in image_files:
                image_file_path = os.path.join(self.temp_img_dir, image_filename)
                create_image_file(image_file_path, format)
                self.archive.write(image_file_path, image_filename)

        self.archive = zipfile.ZipFile(self.tmp_package)
        self.sp_package = utils.SPPackage(self.archive, self.extracted_package)

    def tearDown(self):
        self.archive.close()
        shutil.rmtree(self.temp_package_dir)
        shutil.rmtree(self.temp_img_dir)

    def test_create_SPPackage(self):
        self.assertEqual(self.sp_package._package_file, self.archive)
        self.assertEqual(self.sp_package._extracted_package, self.extracted_package)

    def test_from_file(self):
        package = utils.SPPackage.from_file(self.tmp_package)
        self.assertIsInstance(package, utils.SPPackage)

    def test_from_file_receives_extracted_directory(self):
        package = utils.SPPackage.from_file(self.tmp_package, "/tmp/test")
        self.assertEqual(package._extracted_package, "/tmp/test")

    def test_optimise_xml_to_web_optimised_images(self):
        self.sp_package._optimise_xml_to_web(
            utils.XML(io.BytesIO(BASE_XML)), "somedocument.xml"
        )

        expected = [
            "1234-5678-rctb-45-05-0110-e01.png",
            "1234-5678-rctb-45-05-0110-e02.png",
            "1234-5678-rctb-45-05-0110-e04.png",
        ]
        for file in expected:
            self.assertTrue(os.path.exists(os.path.join(self.extracted_package, file)))
        self.assertFalse(
            os.path.exists(
                os.path.join(
                    self.extracted_package, "1234-5678-rctb-45-05-0110-gf03.png"
                )
            )
        )

    def test_optimise_xml_to_web_optimises_xmls(self):
        self.sp_package._optimise_xml_to_web(
            utils.XML(io.BytesIO(BASE_XML)), "somedocument.xml"
        )
        self.assertTrue(
            os.path.exists(os.path.join(self.extracted_package, "somedocument.xml"))
        )
        expected = [
            "1234-5678-rctb-45-05-0110-e01.png",
            "1234-5678-rctb-45-05-0110-e01.thumbnail.jpg",
            "1234-5678-rctb-45-05-0110-e02.png",
            "1234-5678-rctb-45-05-0110-gf03.png",
            "1234-5678-rctb-45-05-0110-gf03.thumbnail.jpg",
            "1234-5678-rctb-45-05-0110-e04.png",
        ]
        path = '//graphic[@specific-use="scielo-web"]|//inline-graphic[@specific-use="scielo-web"]'
        xml_file_path = os.path.join(self.extracted_package, "somedocument.xml")
        xml_file = utils.XML(xml_file_path)
        for image_element, expected_href in zip(xml_file.xpath(path), expected):
            self.assertEqual(
                image_element.attrib["{http://www.w3.org/1999/xlink}href"],
                expected_href,
            )

    def test_optimise_image_raises_error_if_error_extracting_file(self):
        inexistent_file = "inexistent_file.tiff"
        web_image_generator = utils.WebImageGenerator(
            "inexistent_file.tiff", self.extracted_package
        )
        with self.assertRaises(exceptions.SPPackageError) as exc_info:
            self.sp_package._optimise_image(
                inexistent_file, web_image_generator.convert2png
            )

    def test_optimise_creates_optimised_zip(self):
        self.sp_package.optimise()
        self.assertTrue(os.path.exists(self.optimised_package))
        self.assertTrue(len(os.listdir(self.extracted_package)) > 0)

    def test_optimise_deletes_aux_directory_if_preserve_files_false(self):
        self.sp_package.optimise(preserve_files=False)
        self.assertTrue(os.path.exists(self.optimised_package))
        self.assertFalse(os.path.exists(self.extracted_package))

    def test_optimise_creates_optimised_zip_with_given_path(self):
        given_zip_path = self.extracted_package + "_test.zip"
        self.sp_package.optimise(new_package_file_path=given_zip_path)
        self.assertTrue(os.path.exists(given_zip_path))

    def test_optimise_creates_zip_with_files(self):
        self.sp_package.optimise()

        optimised_images = [
            "1234-5678-rctb-45-05-0110-e01.png",
            "1234-5678-rctb-45-05-0110-e01.thumbnail.jpg",
            "1234-5678-rctb-45-05-0110-e02.png",
            "1234-5678-rctb-45-05-0110-gf03.png",
            "1234-5678-rctb-45-05-0110-gf03.thumbnail.jpg",
            "1234-5678-rctb-45-05-0110-e04.png",
        ]
        with zipfile.ZipFile(self.optimised_package) as zf:
            self.assertTrue(set(self.archive.namelist()).issubset(set(zf.namelist())))
            self.assertTrue(set(optimised_images).issubset(set(zf.namelist())))

    def test_optimise_updates_xmls(self):
        self.sp_package.optimise()

        expected = [
            "1234-5678-rctb-45-05-0110-e01.png",
            "1234-5678-rctb-45-05-0110-e01.thumbnail.jpg",
            "1234-5678-rctb-45-05-0110-e02.png",
            "1234-5678-rctb-45-05-0110-gf03.png",
            "1234-5678-rctb-45-05-0110-gf03.thumbnail.jpg",
            "1234-5678-rctb-45-05-0110-e04.png",
        ]
        with zipfile.ZipFile(self.optimised_package) as zf:
            xml_file = utils.XML(io.BytesIO(zf.read("somedocument.xml")))
            path = '//graphic[@specific-use="scielo-web"]|//inline-graphic[@specific-use="scielo-web"]'
            for image_element, expected_href in zip(xml_file.xpath(path), expected):
                self.assertEqual(
                    image_element.attrib["{http://www.w3.org/1999/xlink}href"],
                    expected_href,
                )
