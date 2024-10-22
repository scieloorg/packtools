import unittest
import xml.etree.ElementTree as ET
from packtools.sps.formats.sps_xml.article_meta import build_article_meta


class TestBuildArticleMetaPubId(unittest.TestCase):
    def test_build_article_article_id(self):
        data = {
            "pub_id_doi": "10.1016/j.bjane.2019.01.003",
            "pub_id_other": "00603"
        }
        expected_xml_str = (
            '<article-meta>'
            '<article-id pub-id-type="doi">10.1016/j.bjane.2019.01.003</article-id>'
            '<article-id pub-id-type="other">00603</article-id>'
            '</article-meta>'
        )
        article_meta_elem = build_article_meta(data)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_article_article_id_None(self):
        data = {
            "pub_id_doi": None,
            "pub_id_other": None
        }
        expected_xml_str = (
            '<article-meta />'
        )
        article_meta_elem = build_article_meta(data)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildArticleCategories(unittest.TestCase):
    def test_build_article_article_categories(self):
        data = {
            "article_subject": "Original Article"
        }
        expected_xml_str = (
            '<article-meta>'
            '<article-categories>'
            '<subj-group subj-group-type="heading">'
            '<subject>Original Article</subject>'
            '</subj-group></article-categories>'
            '</article-meta>'
        )
        article_meta_elem = build_article_meta(data)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_article_article_categories_None(self):
        data = {
            "article_subject": None
        }
        expected_xml_str = (
            '<article-meta />'
        )
        article_meta_elem = build_article_meta(data)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildArticleTitle(unittest.TestCase):
    def test_build_article_article_title(self):
        data = {
            "article_title": "Conocimientos de los pediatras sobre la laringomalacia",
            "trans_title": {
                "en": "Pediatrician knowledge about laryngomalacia",
            }
        }
        expected_xml_str = (
            '<article-meta>'
            '<title-group>'
            '<article-title>Conocimientos de los pediatras sobre la laringomalacia</article-title>'
            '<trans-title-group xml:lang="en">'
            '<trans-title>Pediatrician knowledge about laryngomalacia</trans-title>'
            '</trans-title-group>'
            '</title-group>'
            '</article-meta>'
        )
        article_meta_elem = build_article_meta(data)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_article_article_title_None(self):
        data = {
            "article_title": None,
            "trans_title": None
        }
        expected_xml_str = (
            '<article-meta />'
        )
        article_meta_elem = build_article_meta(data)
        generated_xml_str = ET.tostring(article_meta_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


