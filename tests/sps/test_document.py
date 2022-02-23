# from unittest import TestCase
# from unittest.mock import Mock

# from dsm.data import document
# from dsm.data import sps_package
# from opac_schema.v1 import models


# class TestDocument(TestCase):

#     def setUp(self):
#         self.xml_sps = sps_package.SPS_Package("./fixtures/document.xml")

    # def test_register_document(self):
    #     expected = None
    # article = Mock(spec=Article)
    #     result = document.register_document(
    #         xml_sps, package_files,
    #         files_storage, classic_website_filename=None,
    #         repeated_doc_pids=None,
    #         issue_data=None,
    #         document_order=None)
    #     self.assertEqual(expected, result)

    # def test__register_document_files(self):
    #     expected = None
    # article = Mock(spec=Article)
    #     result = document._register_document_files(xml_sps, package_files,
    #                          files_storage, classic_website_filename)
    #     self.assertEqual(expected, result)

    # def test__add_renditions(self):
    #     article = Mock(spec=Article)
    #     renditions = "RENDITIONS"
    #     document._add_renditions(article, renditions)
    #     self.assertEqual(renditions, article.pdfs)

    # def test__add_xml_url(self):
    #     expected = None
    #     article = Mock(spec=Article)
    #     result = document._add_xml_url(article, xml_url)
    #     self.assertEqual(expected, result)

    # def test__add_issue_data(self):
    #     expected = None
    #     article = Mock(spec=Article)
    #     result = document._add_issue_data(article, issue_id)
    #     self.assertEqual(expected, result)

    # def test__add_control_data(self):
    #     expected = None
    #     article = Mock(spec=Article)
    #     result = document._add_issue_data(article, issue_id)
    #     self.assertEqual(expected, result)

    # def test__add_ids(self):
    #     expected = None
    #     article = Mock(spec=Article)
    #     result = document._add_control_data(article, xml_sps, is_public=True)
    #     self.assertEqual(expected, result)

    # def test__register_xml_data(self):
    #     expected = None
    #     article = Mock(spec=Article)
    #     result = document._register_xml_data(article, xml_sps)
    #     self.assertEqual(expected, result)

    # def test__get_authors(self):
    #     expected = None
    #     article = Mock(spec=Article)
    #     result = document._get_authors(xml_sps)
    #     self.assertEqual(expected, result)

    # def test__get_authors_meta(self):
    #     expected = None
    #     article = Mock(spec=Article)
    #     result = document._get_authors_meta(xml_sps)
    #     self.assertEqual(expected, result)

    # def test__get_translated_titles(self):
    #     expected = None
    #     article = Mock(spec=Article)
    #     result = document._get_translated_titles(xml_sps)
    #     self.assertEqual(expected, result)

    # def test__get_sections(self):
    #     expected = None
    #     article = Mock(spec=Article)
    #     result = document._get_sections(xml_sps)
    #     self.assertEqual(expected, result)

    # def test__get_abstracts(self):
    #     expected = None
    #     article = Mock(spec=Article)
    #     result = document._get_abstracts(xml_sps)
    #     self.assertEqual(expected, result)

    # def test__get_keywords(self):
    #     expected = None
    #     article = Mock(spec=Article)
    #     result = document._get_keywords(xml_sps)
    #     self.assertEqual(expected, result)

    # def test__get_order(self):
    #     expected = None
    #     article = Mock(spec=Article)
    #     result = document._get_order(xml_sps, document_order)
    #     self.assertEqual(expected, result)

