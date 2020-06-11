#coding: utf-8
from __future__ import unicode_literals
import unittest
import zipfile
import tempfile
import os
import io
import shutil

try:
    from unittest import mock
except:
    import mock

from PIL import Image, ImageFile
from lxml import etree

from packtools import utils, exceptions


BASE_XML = """<?xml version="1.0" encoding="UTF-8"?>
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
    {}
  </disp-formula>
  <p>We also used an... {}.</p>
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
        self.assertEqual(web_image_generator.filename, "image_tiff_1.tiff")
        self.assertIsNone(web_image_generator._image_object)
        self.assertEqual(
            web_image_generator.image_file_path,
            os.path.join(self.extracted_package, "image_tiff_1.tiff"),
        )
        self.assertEqual(web_image_generator.png_filename, "image_tiff_1.png")
        self.assertEqual(
            web_image_generator.thumbnail_filename, "image_tiff_1.thumbnail.jpg"
        )

    def test_create_WebImageGenerator_with_invalid_image_bytes(self):
        mocked_bytes = "This is not an image".encode("utf-8")
        with self.assertRaises(exceptions.WebImageGeneratorError) as exc_info:
            utils.WebImageGenerator("image_tiff_1.tiff", ".", mocked_bytes)
        self.assertEqual(
            str(exc_info.exception),
            'Error reading image "image_tiff_1.tiff": cannot parse this image',
        )

    def test_create_WebImageGenerator_with_file_bytes(self):
        mocked_image_io = io.BytesIO()
        mocked_image = Image.new("RGB", (10, 10))
        mocked_image.save(mocked_image_io, "TIFF")
        web_image_generator = utils.WebImageGenerator(
            "image_tiff_2.tiff", ".", mocked_image_io.getvalue()
        )
        self.assertEqual(web_image_generator.filename, "image_tiff_2.tiff")
        self.assertEqual(web_image_generator.image_file_path, "./image_tiff_2.tiff")
        self.assertEqual(web_image_generator.png_filename, "image_tiff_2.png")
        self.assertEqual(
            web_image_generator.thumbnail_filename, "image_tiff_2.thumbnail.jpg"
        )
        self.assertEqual(
            web_image_generator._image_object.tobytes(), mocked_image.tobytes()
        )

    @mock.patch.object(ImageFile.Parser, "feed")
    def test__get_image_object_large_image_file_security_error(
        self, mk_img_parser_feed
    ):
        mk_img_parser_feed.side_effect = Image.DecompressionBombError("ERROR!")
        mocked_image_io = io.BytesIO()
        mocked_image = Image.new("RGB", (10, 10))
        mocked_image.save(mocked_image_io, "TIFF")
        web_image_generator = utils.WebImageGenerator("image_tiff_2.tiff", ".")
        with self.assertRaises(exceptions.WebImageGeneratorError) as exc_info:
            web_image_generator._get_image_object(mocked_image_io.getvalue())
        self.assertEqual(
            str(exc_info.exception),
            'Error reading image "image_tiff_2.tiff": ERROR!',
        )

    def test_convert2png_file_does_not_exist(self):
        web_image_generator = utils.WebImageGenerator(
            "no_file.tif", self.extracted_package
        )
        with self.assertRaises(exceptions.WebImageGeneratorError) as exc_info:
            web_image_generator.convert2png()
        self.assertIn("Error opening image file ", str(exc_info.exception))
        self.assertIn("no_file.tif", str(exc_info.exception))
        self.assertFalse(
            os.path.exists(os.path.join(self.extracted_package, "no_file.png"))
        )

    def test_convert2png_no_image_file(self):
        text_file_path = os.path.join(self.extracted_package, "file.txt")
        with open(text_file_path, "w") as fp:
            fp.write("Text file content.")

        web_image_generator = utils.WebImageGenerator(
            "file.txt", self.extracted_package
        )
        with self.assertRaises(exceptions.WebImageGeneratorError) as exc_info:
            web_image_generator.convert2png()
        self.assertIn("Error opening image file ", str(exc_info.exception))
        self.assertIn("file.txt", str(exc_info.exception))
        self.assertFalse(
            os.path.exists(os.path.join(self.extracted_package, "file.png"))
        )

    def test_convert2png_ok(self):
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

    def test_convert2png_to_destination_path(self):
        destination_path = tempfile.mkdtemp(".")
        web_image_generator = utils.WebImageGenerator(
            "image_tiff_2.tif", self.extracted_package
        )
        web_image_generator.convert2png(destination_path)

        is_conversion_ok = os.path.exists(
            os.path.join(
                destination_path,
                os.path.splitext("image_tiff_2.tif")[0] + ".png",
            )
        )
        shutil.rmtree(destination_path)
        self.assertTrue(is_conversion_ok)

    def test_create_thumbnail_file_does_not_exist(self):
        web_image_generator = utils.WebImageGenerator(
            "no_file.tif", self.extracted_package
        )
        with self.assertRaises(exceptions.WebImageGeneratorError) as exc_info:
            web_image_generator.create_thumbnail()
        self.assertIn("Error opening image file ", str(exc_info.exception))
        self.assertIn("no_file.tif", str(exc_info.exception))
        self.assertFalse(
            os.path.exists(os.path.join(self.extracted_package, "no_file.png"))
        )

    def test_create_thumbnail_no_image_file(self):
        text_file_path = os.path.join(self.extracted_package, "file.txt")
        with open(text_file_path, "w") as fp:
            fp.write("Text file content.")

        web_image_generator = utils.WebImageGenerator(
            "file.txt", self.extracted_package
        )
        with self.assertRaises(exceptions.WebImageGeneratorError) as exc_info:
            web_image_generator.create_thumbnail()
        self.assertIn("Error opening image file ", str(exc_info.exception))
        self.assertIn("file.txt", str(exc_info.exception))
        self.assertFalse(
            os.path.exists(os.path.join(self.extracted_package, "file.png"))
        )

    def test_create_thumbnail_ok(self):
        filename = os.path.join(self.extracted_package, "image_tiff_1.png")
        create_image_file(filename, "PNG")

        web_image_generator = utils.WebImageGenerator(
            "image_tiff_1.png", self.extracted_package
        )
        web_image_generator.create_thumbnail()
        thumbnail_filename = os.path.splitext(filename)[0] + ".thumbnail.jpg"
        self.assertTrue(os.path.exists(thumbnail_filename))

    def test_create_thumbnail_to_destination_path(self):
        destination_path = tempfile.mkdtemp(".")
        filename = os.path.join(self.extracted_package, "image_tiff_1.png")
        create_image_file(filename, "PNG")

        web_image_generator = utils.WebImageGenerator(
            "image_tiff_1.png", self.extracted_package
        )
        web_image_generator.create_thumbnail()
        thumbnail_filename = os.path.splitext(filename)[0] + ".thumbnail.jpg"
        is_thumbnail_ok = os.path.exists(thumbnail_filename)
        shutil.rmtree(destination_path)
        self.assertTrue(is_thumbnail_ok)

    def test_get_png_bytes_no_image_object(self):
        web_image_generator = utils.WebImageGenerator(
            "image_tiff_1.tiff", self.extracted_package
        )
        with self.assertRaises(exceptions.WebImageGeneratorError) as exc_info:
            web_image_generator.get_png_bytes()
        self.assertEqual(
            str(exc_info.exception),
            'Error optimising image bytes from "image_tiff_1.tiff": '
            "no original file bytes was given.",
        )

    def test_get_png_bytes_ok(self):
        mocked_image_io = io.BytesIO()
        mocked_image = Image.new("RGB", (10, 10))
        mocked_image.save(mocked_image_io, "TIFF")
        parser = ImageFile.Parser()
        parser.feed(mocked_image_io.getvalue())
        web_image_generator = utils.WebImageGenerator(
            "image_tiff_1.tiff", self.extracted_package
        )
        web_image_generator._image_object = parser.close()

        result = web_image_generator.get_png_bytes()

        image_expected = io.BytesIO()
        image_copy = web_image_generator._image_object.copy()
        image_copy.save(image_expected, "PNG")
        self.assertEqual(result, image_expected.getvalue())

    def test_get_thumbnail_bytes_no_image_object(self):
        web_image_generator = utils.WebImageGenerator(
            "image_tiff_1.tiff", self.extracted_package
        )
        with self.assertRaises(exceptions.WebImageGeneratorError) as exc_info:
            web_image_generator.get_thumbnail_bytes()
        self.assertEqual(
            str(exc_info.exception),
            'Error optimising image bytes from "image_tiff_1.tiff": '
            "no original file bytes was given.",
        )

    def test_get_thumbnail_bytes_ok(self):
        mocked_image_io = io.BytesIO()
        mocked_image = Image.new("RGB", (10, 10))
        mocked_image.save(mocked_image_io, "TIFF")
        parser = ImageFile.Parser()
        parser.feed(mocked_image_io.getvalue())
        web_image_generator = utils.WebImageGenerator(
            "image_tiff_1.tiff", self.extracted_package
        )
        web_image_generator._image_object = parser.close()

        result = web_image_generator.get_thumbnail_bytes()

        image_expected = io.BytesIO()
        image_copy = web_image_generator._image_object.copy()
        image_copy.thumbnail(web_image_generator.thumbnail_size)
        image_copy.save(image_expected, "JPEG")
        self.assertEqual(result, image_expected.getvalue())


class TestXMLWebOptimiser(unittest.TestCase):
    def setUp(self):
        graphic_01 = '<graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif"/>'
        graphic_02 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff"/>'
        self.xml_file = BASE_XML.format(graphic_01, graphic_02).encode("utf-8")
        self.xml_filename = "1234-5678-rctb-45-05-0110.xml"
        self.work_dir = tempfile.mkdtemp()
        self.image_filenames = [
            "1234-5678-rctb-45-05-0110-e01.tif",
            "1234-5678-rctb-45-05-0110-e02.tiff",
            "1234-5678-rctb-45-05-0110-gf03.tiff",
            "1234-5678-rctb-45-05-0110-gf03.png",
            "1234-5678-rctb-45-05-0110-gf03.thumbnail.jpg",
            "1234-5678-rctb-45-05-0110-e04.tif",
        ]
        image_format_seq = ["TIFF", "TIFF", "TIFF", "PNG", "JPEG", "TIFF"]
        for filename, format in zip(self.image_filenames, image_format_seq):
            image_file_path = os.path.join(self.work_dir, filename)
            create_image_file(image_file_path, format)
        xml_file_path = os.path.join(self.work_dir, self.xml_filename)
        with open(xml_file_path, "wb") as fp:
            fp.write(self.xml_file)

        self.xml_web_optimiser = utils.XMLWebOptimiser(
            self.xml_filename,
            self.image_filenames,
            self.mocked_read_file,
            self.work_dir,
        )

    def tearDown(self):
        shutil.rmtree(self.work_dir)

    def mocked_read_file(self, filename):
        file_path = os.path.join(self.work_dir, filename)
        with open(file_path, "rb") as fp:
            return fp.read()

    def test_get_all_graphic_images_from_xml(self):
        expected = {
            "1234-5678-rctb-45-05-0110-e01.tif",
            "1234-5678-rctb-45-05-0110-e02.tiff",
            "1234-5678-rctb-45-05-0110-gf03.tiff",
            "1234-5678-rctb-45-05-0110-gf03.png",
            "1234-5678-rctb-45-05-0110-gf03.thumbnail.jpg",
            "1234-5678-rctb-45-05-0110-e04.tif",
        }
        result = self.xml_web_optimiser._get_all_graphic_images_from_xml(
            self.image_filenames
        )
        for graphic_filename, expected_filename in zip(result, expected):
            self.assertEqual(graphic_filename, expected_filename)

    def test_create_XMLWebOptimiser(self):
        self.assertEqual(self.xml_web_optimiser.filename, self.xml_filename)
        self.assertEqual(self.xml_web_optimiser.work_dir, self.work_dir)
        self.assertEqual(self.xml_web_optimiser._optimised_assets, [])
        self.assertEqual(self.xml_web_optimiser._assets_thumbnails, [])
        self.assertFalse(self.xml_web_optimiser.stop_if_error)
        self.assertEqual(self.xml_web_optimiser._read_file, self.mocked_read_file)
        self.assertEqual(
            etree.tostring(self.xml_web_optimiser._xml_file),
            etree.tostring(utils.XML(io.BytesIO(self.xml_file))),
        )
        self.assertEqual(self.xml_web_optimiser._image_filenames, set(self.image_filenames))

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
            self.assertEqual(image_filename, expected_filename)

    def test_get_all_images_to_thumbnail(self):
        images = self.xml_web_optimiser._get_all_images_to_thumbnail()

        expected = ["1234-5678-rctb-45-05-0110-e01.tif"]
        result = [image for image in images]
        self.assertEqual(len(result), len(expected))
        for image, expected_filename in zip(result, expected):
            image_filename, image_element = image
            self.assertEqual(image_filename, expected_filename)

    def test_get_optimised_image_with_filename_no_existing_file_in_image_filenames(
        self,
    ):
        def dummy_optimise(filename):
            return None

        new_filename = self.xml_web_optimiser._get_optimised_image_with_filename(
            "1234-5678-rctb-45-05-0110-no-file.tif", dummy_optimise
        )
        self.assertEqual(len(self.xml_web_optimiser._optimised_assets), 0)
        self.assertIsNone(new_filename)

    def test_add_optimised_image_no_existing_file_in_source(self):
        def mocked_read_file_exception(filename):
            raise exceptions.SPPackageError("File not found")

        self.xml_web_optimiser._read_file = mocked_read_file_exception
        new_filename = self.xml_web_optimiser._add_optimised_image(
            "1234-5678-rctb-45-05-0110-e01.tif"
        )
        self.assertEqual(len(self.xml_web_optimiser._optimised_assets), 0)
        self.assertIsNone(new_filename)

    def test_add_optimised_image_ok(self):
        new_filename = self.xml_web_optimiser._add_optimised_image(
            "1234-5678-rctb-45-05-0110-e01.tif"
        )
        self.assertEqual(len(self.xml_web_optimiser._optimised_assets), 1)
        filename, file_bytes = self.xml_web_optimiser._optimised_assets[0]
        self.assertEqual(filename, "1234-5678-rctb-45-05-0110-e01.png")
        self.assertIsNotNone(file_bytes)

    def test_add_assets_thumbnails_no_existing_file_in_source(self):
        def mocked_read_file_exception(filename):
            raise exceptions.SPPackageError("File not found")

        self.xml_web_optimiser._read_file = mocked_read_file_exception
        new_filename = self.xml_web_optimiser._add_assets_thumbnails(
            "1234-5678-rctb-45-05-0110-e01.tif"
        )
        self.assertEqual(len(self.xml_web_optimiser._assets_thumbnails), 0)
        self.assertIsNone(new_filename)

    def test_add_assets_thumbnails(self):
        new_filename = self.xml_web_optimiser._add_assets_thumbnails(
            "1234-5678-rctb-45-05-0110-e01.tif"
        )
        self.assertEqual(len(self.xml_web_optimiser._assets_thumbnails), 1)
        filename, file_bytes = self.xml_web_optimiser._assets_thumbnails[0]
        self.assertEqual(filename, "1234-5678-rctb-45-05-0110-e01.thumbnail.jpg")
        self.assertIsNotNone(file_bytes)

    def test_get_xml_file_ok(self):
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
        xml_result = self.xml_web_optimiser.get_xml_file()
        xml_etree = etree.fromstring(xml_result)
        for alternatives, expected_files in zip(
            xml_etree.findall(".//alternatives"), expected
        ):
            path = './graphic[@specific-use="scielo-web"]|./inline-graphic[@specific-use="scielo-web"]'
            for image, expected_href in zip(alternatives.xpath(path), expected_files):
                self.assertEqual(
                    image.attrib["{http://www.w3.org/1999/xlink}href"], expected_href
                )

    def test_get_optimised_assets_no_optimised_assets(self):
        self.xml_web_optimiser._optimised_assets = []
        result = self.xml_web_optimiser.get_optimised_assets()
        optimised_assets = [image_generator for image_generator in result]
        self.assertEqual(len(optimised_assets), 0)

    def test_get_optimised_assets_ok(self):
        self.xml_web_optimiser.get_xml_file()
        result = self.xml_web_optimiser.get_optimised_assets()

        optimised_assets = [image for image in result]
        self.assertEqual(len(optimised_assets), 3)
        expected_filenames = [
            "1234-5678-rctb-45-05-0110-e01.png",
            "1234-5678-rctb-45-05-0110-e02.png",
            "1234-5678-rctb-45-05-0110-e04.png",
        ]
        for optimised_asset, expected_filename in zip(
            optimised_assets, expected_filenames
        ):
            image_filename, image_bytes = optimised_asset
            self.assertEqual(image_filename, expected_filename)
            self.assertIsNotNone(image_bytes)

    def test_get_assets_thumbnails_no_assets_thumbnails(self):
        self.xml_web_optimiser._assets_thumbnails = []
        result = self.xml_web_optimiser.get_assets_thumbnails()
        assets_thumbnails = [image_generator for image_generator in result]
        self.assertEqual(len(assets_thumbnails), 0)

    def test_get_assets_thumbnails_get_thumbnail_bytes_raises_exception(self):
        self.xml_web_optimiser._optimised_assets = [
            utils.WebImageGenerator("1234-5678-rctb-45-05-0110-e01.tif", "."),
        ]
        result = self.xml_web_optimiser.get_assets_thumbnails()
        assets_thumbnails = [image_generator for image_generator in result]
        self.assertEqual(len(assets_thumbnails), 0)

    def test_get_assets_thumbnails_ok(self):
        self.xml_web_optimiser.get_xml_file()
        result = self.xml_web_optimiser.get_assets_thumbnails()

        assets_thumbnails = [image for image in result]
        self.assertEqual(len(assets_thumbnails), 1)
        image_filename, image_bytes = assets_thumbnails[0]
        self.assertEqual(image_filename, "1234-5678-rctb-45-05-0110-e01.thumbnail.jpg")
        self.assertIsNotNone(image_bytes)


class TestXMLWebOptimiserGraphicsWithNoFileExtention(unittest.TestCase):
    def setUp(self):
        graphic_01 = '<graphic xlink:href="1234-5678-rctb-45-05-0110-e01"/>'
        graphic_02 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02"/>'
        self.xml_file = BASE_XML.format(graphic_01, graphic_02).encode("utf-8")
        self.xml_filename = "1234-5678-rctb-45-05-0110.xml"
        self.work_dir = tempfile.mkdtemp()
        self.image_filenames = [
            "1234-5678-rctb-45-05-0110-e01.tif",
            "1234-5678-rctb-45-05-0110-e02.tiff",
            "1234-5678-rctb-45-05-0110-gf03.tiff",
            "1234-5678-rctb-45-05-0110-gf03.png",
            "1234-5678-rctb-45-05-0110-gf03.thumbnail.jpg",
            "1234-5678-rctb-45-05-0110-e04.tif",
        ]
        image_format_seq = ["TIFF", "TIFF", "TIFF", "PNG", "JPEG", "TIFF"]
        for filename, format in zip(self.image_filenames, image_format_seq):
            image_file_path = os.path.join(self.work_dir, filename)
            create_image_file(image_file_path, format)
        xml_file_path = os.path.join(self.work_dir, self.xml_filename)
        with open(xml_file_path, "wb") as fp:
            fp.write(self.xml_file)

        self.xml_web_optimiser = utils.XMLWebOptimiser(
            self.xml_filename,
            self.image_filenames,
            self.mocked_read_file,
            self.work_dir,
        )

    def tearDown(self):
        shutil.rmtree(self.work_dir)

    def mocked_read_file(self, filename):
        file_path = os.path.join(self.work_dir, filename)
        with open(file_path, "rb") as fp:
            return fp.read()

    def test_get_all_graphic_images_from_xml(self):
        expected = {
            "1234-5678-rctb-45-05-0110-e01.tif",
            "1234-5678-rctb-45-05-0110-e02.tiff",
            "1234-5678-rctb-45-05-0110-gf03.tiff",
            "1234-5678-rctb-45-05-0110-gf03.png",
            "1234-5678-rctb-45-05-0110-gf03.thumbnail.jpg",
            "1234-5678-rctb-45-05-0110-e04.tif",
        }
        result = self.xml_web_optimiser._get_all_graphic_images_from_xml(
            self.image_filenames
        )
        for graphic_filename, expected_filename in zip(result, expected):
            self.assertEqual(graphic_filename, expected_filename)

    def test_get_all_images_to_optimise(self):
        images = self.xml_web_optimiser._get_all_images_to_optimise()
        expected = [
            "1234-5678-rctb-45-05-0110-e01",
            "1234-5678-rctb-45-05-0110-e02",
            "1234-5678-rctb-45-05-0110-e04.tif",
        ]
        result = [image for image in images]
        self.assertEqual(len(result), len(expected))
        for image, expected_filename in zip(result, expected):
            image_filename, image_element = image
            self.assertEqual(image_filename, expected_filename)

    def test_get_all_images_to_thumbnail(self):
        images = self.xml_web_optimiser._get_all_images_to_thumbnail()

        expected = ["1234-5678-rctb-45-05-0110-e01"]
        result = [image for image in images]
        self.assertEqual(len(result), len(expected))
        for image, expected_filename in zip(result, expected):
            image_filename, image_element = image
            self.assertEqual(image_filename, expected_filename)

    def test_get_xml_file_ok(self):
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
        xml_result = self.xml_web_optimiser.get_xml_file()
        xml_etree = etree.fromstring(xml_result)
        for alternatives, expected_files in zip(
            xml_etree.findall(".//alternatives"), expected
        ):
            path = './graphic[@specific-use="scielo-web"]|./inline-graphic[@specific-use="scielo-web"]'
            for image, expected_href in zip(alternatives.xpath(path), expected_files):
                self.assertEqual(
                    image.attrib["{http://www.w3.org/1999/xlink}href"], expected_href
                )


class TestXMLWebOptimiserValidations(unittest.TestCase):
    def setUp(self):
        self.xml_filename = "1234-5678-rctb-45-05-0110.xml"
        self.work_dir = tempfile.mkdtemp()
        self.image_filenames = [
            "a01-gf01.jpg",
            "1234-5678-rctb-45-05-0110-e01.jpg",
            "a02-e01.gif",
            "1234-5678-rctb-45-05-0110-e02.gif",
            "a03tb01.png",
            "1234-5678-rctb-45-05-0110-gf03.tiff",
            "1234-5678-rctb-45-05-0110-gf03.png",
            "a04gf01.tiff",
            "a04gf02.tiff",
            "1234-5678-rctb-45-05-0110-gf03.thumbnail.jpg",
            "1234-5678-rctb-45-05-0110-e04.tif",
        ]
        image_format_seq = ["JPEG", "GIF", "TIFF", "PNG", "JPEG", "TIFF"]
        for filename, format in zip(self.image_filenames, image_format_seq):
            image_file_path = os.path.join(self.work_dir, filename)
            create_image_file(image_file_path, format)

    def tearDown(self):
        shutil.rmtree(self.work_dir)

    def mocked_read_file(self, filename):
        file_path = os.path.join(self.work_dir, filename)
        with open(file_path, "rb") as fp:
            return fp.read()

    def test_get_all_graphic_images_from_xml(self):
        graphic_01 = '<graphic xlink:href="1234-5678-rctb-45-05-0110-e01.jpg"/>'
        graphic_02 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.gif"/>'
        xml_file = BASE_XML.format(graphic_01, graphic_02).encode("utf-8")
        xml_file_path = os.path.join(self.work_dir, self.xml_filename)
        with open(xml_file_path, "wb") as fp:
            fp.write(xml_file)

        xml_web_optimiser = utils.XMLWebOptimiser(
            self.xml_filename,
            self.image_filenames,
            self.mocked_read_file,
            self.work_dir,
        )
        result = xml_web_optimiser._get_all_graphic_images_from_xml(
            self.image_filenames
        )
        expected = {
            "1234-5678-rctb-45-05-0110-e01.jpg",
            "1234-5678-rctb-45-05-0110-e02.gif",
            "1234-5678-rctb-45-05-0110-gf03.tiff",
            "1234-5678-rctb-45-05-0110-gf03.png",
            "1234-5678-rctb-45-05-0110-gf03.thumbnail.jpg",
            "1234-5678-rctb-45-05-0110-e04.tif",
        }
        for graphic_filename, expected_filename in zip(result, expected):
            self.assertEqual(graphic_filename, expected_filename)

    def test_get_all_images_to_optimise_does_not_return_optimised_images(self):
        graphic_01 = '<graphic xlink:href="1234-5678-rctb-45-05-0110-e01.jpg"/>'
        graphic_02 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.gif"/>'
        xml_file = BASE_XML.format(graphic_01, graphic_02).encode("utf-8")
        xml_file_path = os.path.join(self.work_dir, self.xml_filename)
        with open(xml_file_path, "wb") as fp:
            fp.write(xml_file)

        xml_web_optimiser = utils.XMLWebOptimiser(
            self.xml_filename,
            self.image_filenames,
            self.mocked_read_file,
            self.work_dir,
        )
        images = xml_web_optimiser._get_all_images_to_optimise()
        expected = ["1234-5678-rctb-45-05-0110-e04.tif"]
        result = [image for image in images]
        self.assertEqual(len(result), len(expected))
        image_filename, __ = result[0]
        self.assertEqual(expected[0], image_filename)

    def test_get_all_images_to_thumbnail_does_not_return_images_with_thumbnail(self):
        graphic_01 = ""
        graphic_02 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.gif"/>'
        xml_file = BASE_XML.format(graphic_01, graphic_02).encode("utf-8")
        xml_file_path = os.path.join(self.work_dir, self.xml_filename)
        with open(xml_file_path, "wb") as fp:
            fp.write(xml_file)

        xml_web_optimiser = utils.XMLWebOptimiser(
            self.xml_filename,
            self.image_filenames,
            self.mocked_read_file,
            self.work_dir,
        )
        images = xml_web_optimiser._get_all_images_to_thumbnail()
        result = [image for image in images]
        self.assertEqual(len(result), 0)

    def test_add_alternative_to_alternatives_tag_add_image_tags_to_new_alternatives(
        self,
    ):
        xml_file = BASE_XML.format("", "").encode("utf-8")
        xml_file_path = os.path.join(self.work_dir, self.xml_filename)
        with open(xml_file_path, "wb") as fp:
            fp.write(xml_file)
        xml_web_optimiser = utils.XMLWebOptimiser(
            self.xml_filename,
            self.image_filenames,
            self.mocked_read_file,
            self.work_dir,
        )
        XML_TAG = """<article xmlns:xlink="http://www.w3.org/1999/xlink">
            <fig id="f03">
                <label>Fig. 3</label>
                <caption>
                    <title>titulo da imagem</title>
                </caption>
                <graphic xlink:href="1234-5678-rctb-45-05-0110-gf03.tiff"/>
            </fig>
        </article>"""
        xml_tag = etree.fromstring(
            XML_TAG, etree.XMLParser(remove_blank_text=True, no_network=True)
        )
        xml_web_optimiser._xml_file = xml_tag
        image_element = xml_tag.find(".//graphic")
        alternative_attr_values = (
            (
                "{http://www.w3.org/1999/xlink}href",
                "1234-5678-rctb-45-05-0110-gf03.png",
            ),
            ("specific-use", "scielo-web"),
        )
        xml_web_optimiser._add_alternative_to_alternatives_tag(
            image_element, alternative_attr_values
        )
        self.assertIsNone(xml_tag.find("fig/graphic"))
        alternatives_tags = xml_tag.findall("fig/alternatives")
        self.assertIsNotNone(alternatives_tags)
        expected_hrefs = [
            "1234-5678-rctb-45-05-0110-gf03.tiff",
            "1234-5678-rctb-45-05-0110-gf03.png",
        ]
        for image_element in alternatives_tags[0].getchildren():
            self.assertEqual(image_element.tag, "graphic")

    def test_add_alternative_to_alternatives_tag_add_image_tags_to_existing_alternatives(
        self,
    ):
        xml_file = BASE_XML.format("", "").encode("utf-8")
        xml_file_path = os.path.join(self.work_dir, self.xml_filename)
        with open(xml_file_path, "wb") as fp:
            fp.write(xml_file)
        xml_web_optimiser = utils.XMLWebOptimiser(
            self.xml_filename,
            self.image_filenames,
            self.mocked_read_file,
            self.work_dir,
        )
        XML_TAG = """<article xmlns:xlink="http://www.w3.org/1999/xlink">
            <p>Bla, bla, bla
                <alternatives>
                    <inline-graphic xlink:href="1234-5678-rctb-45-05-0110-gf03.tiff"/>
                    <inline-graphic xlink:href="1234-5678-rctb-45-05-0110-gf03.png" specific-use="scielo-web"/>
                </alternatives>
            </p>
        </article>"""
        xml_tag = etree.fromstring(
            XML_TAG, etree.XMLParser(remove_blank_text=True, no_network=True)
        )
        xml_web_optimiser._xml_file = xml_tag
        image_element = xml_tag.find(".//inline-graphic")
        alternative_attr_values = (
            (
                "{http://www.w3.org/1999/xlink}href",
                "1234-5678-rctb-45-05-0110-gf03.gif",
            ),
            ("specific-use", "scielo-web"),
        )
        xml_web_optimiser._add_alternative_to_alternatives_tag(
            image_element, alternative_attr_values
        )
        self.assertIsNone(xml_tag.find("p/inline-graphic"))
        alternatives_tags = xml_tag.findall("p/alternatives")
        self.assertIsNotNone(alternatives_tags)
        self.assertEqual(len(alternatives_tags), 1)
        expected_hrefs = [
            "1234-5678-rctb-45-05-0110-gf03.tiff",
            "1234-5678-rctb-45-05-0110-gf03.png",
            "1234-5678-rctb-45-05-0110-gf03.gif",
        ]
        for image_element in alternatives_tags[0].getchildren():
            self.assertEqual(image_element.tag, "inline-graphic")

    def test_get_optimised_xml_no_reader_file(self):
        graphic_01 = '<graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif"/>'
        graphic_02 = '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff"/>'
        xml_file = BASE_XML.format(graphic_01, graphic_02).encode("utf-8")
        xml_file_path = os.path.join(self.work_dir, self.xml_filename)
        with open(xml_file_path, "wb") as fp:
            fp.write(xml_file)

        with self.assertRaises(exceptions.XMLWebOptimiserError) as exc_info:
            xml_web_optimiser = utils.XMLWebOptimiser(
                self.xml_filename, self.image_filenames, None, self.work_dir,
            )
        self.assertEqual(
            str(exc_info.exception),
            "Error instantiating XMLWebOptimiser: read_file cannot be None",
        )


class TestSPPackage(unittest.TestCase):
    def setUp(self):
        self.temp_package_dir = tempfile.mkdtemp(".")
        self.temp_img_dir = tempfile.mkdtemp(".")
        self.tmp_package = os.path.join(self.temp_package_dir, "sps_package.zip")
        self.extracted_package = os.path.splitext(self.tmp_package)[0]
        self.optimised_package = self.extracted_package + "_optimised.zip"
        self.xml_filename = "somedocument.xml"

        with zipfile.ZipFile(self.tmp_package, "w") as self.archive:
            xml_file_path = os.path.join(self.temp_img_dir, self.xml_filename)
            with open(xml_file_path, "wb") as xml_file:
                graphic_01 = '<graphic xlink:href="1234-5678-rctb-45-05-0110-e01.tif"/>'
                graphic_02 = (
                    '<inline-graphic xlink:href="1234-5678-rctb-45-05-0110-e02.tiff"/>'
                )
                xml_content = BASE_XML.format(graphic_01, graphic_02)
                xml_file.write(xml_content.encode("utf-8"))
            self.archive.write(xml_file_path, self.xml_filename)
            self.archive.write(xml_file_path, "1234-5678-rctb-45-05-0110.pdf")
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
            xml_file = utils.XML(io.BytesIO(zf.read(self.xml_filename)))
            path = '//graphic[@specific-use="scielo-web"]|//inline-graphic[@specific-use="scielo-web"]'
            for image_element, expected_href in zip(xml_file.xpath(path), expected):
                self.assertEqual(
                    image_element.attrib["{http://www.w3.org/1999/xlink}href"],
                    expected_href,
                )
