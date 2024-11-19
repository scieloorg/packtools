import unittest

from lxml import etree

from packtools.sps.formats.pdf.pipeline import xml as xml_pipe


class TestExtractAbstractData(unittest.TestCase):

    def test_extract_abstract_data_with_title_and_content(self):
        xml = etree.fromstring(
            '<article><abstract>'
            '<title>Abstract Title</title>'
            '<p>First paragraph.</p>'
            '<p>Second paragraph.</p>'
            '</abstract></article>'
        )
        expected = {
            'title': 'Abstract Title',
            'content': 'First paragraph. Second paragraph.'
        }
        result = xml_pipe.extract_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_abstract_data_with_title_only(self):
        xml = etree.fromstring(
            '<article><abstract>'
            '<title>Abstract Title</title>'
            '</abstract></article>'
        )
        expected = {
            'title': 'Abstract Title',
            'content': ''
        }
        result = xml_pipe.extract_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_abstract_data_with_content_only(self):
        xml = etree.fromstring(
            '<article><abstract>'
            '<p>First paragraph.</p>'
            '<p>Second paragraph.</p>'
            '</abstract></article>'
        )
        expected = {
            'title': '',
            'content': 'First paragraph. Second paragraph.'
        }
        result = xml_pipe.extract_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_abstract_data_empty_abstract(self):
        xml = etree.fromstring('<article><abstract></abstract></article>')
        expected = {
            'title': '',
            'content': ''
        }
        result = xml_pipe.extract_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_abstract_data_no_abstract(self):
        xml = etree.fromstring('<article></article>')
        expected = {
            'title': '',
            'content': ''
        }
        result = xml_pipe.extract_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_abstract_data_with_nested_elements(self):
        xml = etree.fromstring(
            '<article><abstract>'
            '<title>Abstract <italic>Title</italic></title>'
            '<p>First <bold>paragraph</bold>.</p>'
            '<p>Second <italic>paragraph</italic>.</p>'
            '</abstract></article>'
        )
        expected = {
            'title': 'Abstract Title',
            'content': 'First paragraph. Second paragraph.'
        }
        result = xml_pipe.extract_abstract_data(xml)
        self.assertEqual(result, expected)

class TestExtractArticleMainLanguage(unittest.TestCase):

    def test_extract_article_main_language_with_valid_lang(self):
        xmltree = etree.fromstring(
            '<article xmlns:xml="http://www.w3.org/XML/1998/namespace" xml:lang="en">'
            '<front><article-meta></article-meta></front>'
            '</article>'
        )
        expected = "en"
        result = xml_pipe.extract_article_main_language(xmltree)
        self.assertEqual(expected, result)

    def test_extract_article_main_language_without_lang(self):
        xmltree = etree.fromstring(
            '<article xmlns:xml="http://www.w3.org/XML/1998/namespace">'
            '<front><article-meta></article-meta></front>'
            '</article>'
        )
        result = xml_pipe.extract_article_main_language(xmltree)
        self.assertIsNone(result)

    def test_extract_article_main_language_with_custom_namespace(self):
        xmltree = etree.fromstring(
            '<article xmlns:custom="http://custom.namespace" custom:lang="pt">'
            '<front><article-meta></article-meta></front>'
            '</article>'
        )
        expected = "pt"
        result = xml_pipe.extract_article_main_language(
            xmltree, 
            namespaces={'xml': 'http://custom.namespace'}
        )
        self.assertEqual(expected, result)

    def test_extract_article_main_language_with_multiple_langs(self):
        xmltree = etree.fromstring(
            '<article xmlns:xml="http://www.w3.org/XML/1998/namespace" xml:lang="es">'
            '<front xml:lang="en"><article-meta></article-meta></front>'
            '</article>'
        )
        expected = "es"
        result = xml_pipe.extract_article_main_language(xmltree)
        self.assertEqual(expected, result)


class TestExtractArticleTitle(unittest.TestCase):

    def test_extract_article_title_basic(self):
        xml = etree.fromstring(
            '<article><article-meta>'
            '<article-title>Sample Title</article-title>'
            '</article-meta></article>'
        )
        result = xml_pipe.extract_article_title(xml)
        self.assertEqual(result, 'Sample Title')

    def test_extract_article_title_return_element(self):
        xml = etree.fromstring(
            '<article><article-meta>'
            '<article-title>Sample Title</article-title>'
            '</article-meta></article>'
        )
        result = xml_pipe.extract_article_title(xml, return_text=False)
        self.assertIsInstance(result, etree._Element)
        
    def test_extract_article_title_empty(self):
        xml = etree.fromstring(
            '<article><article-meta>'
            '<article-title></article-title>'
            '</article-meta></article>'
        )
        result = xml_pipe.extract_article_title(xml)
        self.assertEqual(result, '')

    def test_extract_article_title_with_formatting(self):
        xml = etree.fromstring(
            '<article><article-meta>'
            '<article-title>Title with <italic>formatting</italic></article-title>'
            '</article-meta></article>'
        )
        result = xml_pipe.extract_article_title(xml)
        self.assertEqual(result, 'Title with formatting')

    def test_extract_article_title_missing(self):
        xml = etree.fromstring('<article><article-meta></article-meta></article>')
        with self.assertRaises(AttributeError):
            xml_pipe.extract_article_title(xml)
class TestExtractCategory(unittest.TestCase):

    def setUp(self):
        self.xml_with_category = etree.fromstring("""
            <article>
                <article-meta>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject>Original Article</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </article>
        """)
        
        self.xml_without_category = etree.fromstring("""
            <article>
                <article-meta>
                    <article-categories>
                        <subj-group>
                            <subject>Other Content</subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </article>
        """)

    def test_extract_category_returns_text(self):
        result = xml_pipe.extract_category(self.xml_with_category)
        self.assertEqual(result, "Original Article")

    def test_extract_category_returns_element(self):
        result = xml_pipe.extract_category(self.xml_with_category, return_text=False)
        self.assertIsInstance(result, etree._Element)
        self.assertEqual(result.text, "Original Article")

    def test_extract_category_missing_category_raises_attribute_error(self):
        with self.assertRaises(AttributeError):
            xml_pipe.extract_category(self.xml_without_category)

    def test_extract_category_empty_xml_raises_attribute_error(self):
        empty_xml = etree.fromstring("<article></article>")
        with self.assertRaises(AttributeError):
            xml_pipe.extract_category(empty_xml)

    def test_extract_category_with_empty_subject(self):
        xml = etree.fromstring("""
            <article>
                <article-meta>
                    <article-categories>
                        <subj-group subj-group-type="heading">
                            <subject></subject>
                        </subj-group>
                    </article-categories>
                </article-meta>
            </article>
        """)
        result = xml_pipe.extract_category(xml)
        self.assertEqual(result, "")
