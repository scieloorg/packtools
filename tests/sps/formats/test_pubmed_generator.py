import os
import sys
import tempfile
import unittest
import zipfile

from lxml import etree as ET

from packtools.sps.formats.pubmed_generator import get_xml_trees_and_errors, main

SAMPLE_1 = os.path.join(
    os.path.dirname(__file__), "..", "..", "samples", "0034-7094-rba-69-03-0227.xml"
)
SAMPLE_2 = os.path.join(
    os.path.dirname(__file__), "..", "..", "samples", "example.xml"
)


class GetXmlTreesAndErrors(unittest.TestCase):
    def test_single_xml_file(self):
        xml_trees, errors = get_xml_trees_and_errors(SAMPLE_1)

        self.assertEqual(len(xml_trees), 1)
        self.assertEqual(errors, [])
        self.assertEqual(xml_trees[0].tag, "article")

    def test_zip_package_with_multiple_articles(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            zip_path = os.path.join(tmp_dir, "package.zip")
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.write(SAMPLE_1, arcname="article1.xml")
                zf.write(SAMPLE_2, arcname="article2.xml")

            xml_trees, errors = get_xml_trees_and_errors(zip_path)

        self.assertEqual(len(xml_trees), 2)
        self.assertEqual(errors, [])
        self.assertTrue(all(xml_tree.tag == "article" for xml_tree in xml_trees))

    def test_zip_package_skips_invalid_xml_and_reports_error(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            zip_path = os.path.join(tmp_dir, "package.zip")
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.write(SAMPLE_1, arcname="valid.xml")
                zf.writestr("invalid.xml", "this is not xml")

            xml_trees, errors = get_xml_trees_and_errors(zip_path)

        self.assertEqual(len(xml_trees), 1)
        self.assertEqual(len(errors), 1)
        self.assertEqual(errors[0].get("filename"), "invalid.xml")
        self.assertIsNotNone(errors[0].get("error"))


class Main(unittest.TestCase):
    def test_main_writes_article_set_from_single_xml_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            output_path = os.path.join(tmp_dir, "out.xml")
            argv = sys.argv
            try:
                sys.argv = [
                    "pubmed_generator",
                    "-i", SAMPLE_1,
                    "-o", output_path,
                ]
                main()
            finally:
                sys.argv = argv

            with open(output_path, encoding="utf-8") as fp:
                content = fp.read()

        self.assertIn("<!DOCTYPE ArticleSet", content)
        self.assertEqual(content.count("<Article>"), 1)
        # garante que o XML gerado é bem formado
        ET.fromstring(content.encode("utf-8"))

    def test_main_writes_article_set_from_zip_package(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            zip_path = os.path.join(tmp_dir, "package.zip")
            with zipfile.ZipFile(zip_path, "w") as zf:
                zf.write(SAMPLE_1, arcname="article1.xml")
                zf.write(SAMPLE_2, arcname="article2.xml")

            output_path = os.path.join(tmp_dir, "out.xml")
            argv = sys.argv
            try:
                sys.argv = [
                    "pubmed_generator",
                    "-i", zip_path,
                    "-o", output_path,
                ]
                main()
            finally:
                sys.argv = argv

            with open(output_path, encoding="utf-8") as fp:
                content = fp.read()

        self.assertIn("<!DOCTYPE ArticleSet", content)
        self.assertEqual(content.count("<Article>"), 2)
        ET.fromstring(content.encode("utf-8"))


if __name__ == "__main__":
    unittest.main()
