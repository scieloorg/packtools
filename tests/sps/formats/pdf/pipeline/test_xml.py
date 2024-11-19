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


class TestExtractKeywordsData(unittest.TestCase):

    def test_extract_keywords_data_basic(self):
        xml = etree.fromstring(
            '<article>'
            '<kwd-group xml:lang="en">'
            '<title>Keywords</title>'
            '<kwd>Keyword1</kwd>'
            '<kwd>Keyword2</kwd>'
            '</kwd-group>'
            '</article>'
        )
        expected = {
            'title': 'Keywords',
            'keywords': 'Keyword1, Keyword2'
        }
        result = xml_pipe.extract_keywords_data(xml)
        self.assertEqual(result, expected)

    def test_extract_keywords_data_no_keywords(self):
        xml = etree.fromstring(
            '<article>'
            '<kwd-group xml:lang="en">'
            '<title>Keywords</title>'
            '</kwd-group>'
            '</article>'
        )
        expected = {
            'title': 'Keywords',
            'keywords': ''
        }
        result = xml_pipe.extract_keywords_data(xml)
        self.assertEqual(result, expected)

    def test_extract_keywords_data_no_title(self):
        xml = etree.fromstring(
            '<article>'
            '<kwd-group xml:lang="en">'
            '<kwd>Keyword1</kwd>'
            '<kwd>Keyword2</kwd>'
            '</kwd-group>'
            '</article>'
        )
        expected = {
            'title': '',
            'keywords': 'Keyword1, Keyword2'
        }
        result = xml_pipe.extract_keywords_data(xml)
        self.assertEqual(result, expected)

    def test_extract_keywords_data_different_language(self):
        xml = etree.fromstring(
            '<article>'
            '<kwd-group xml:lang="es">'
            '<title>Palabras clave</title>'
            '<kwd>Palabra1</kwd>'
            '<kwd>Palabra2</kwd>'
            '</kwd-group>'
            '</article>'
        )
        expected = {
            'title': 'Palabras clave',
            'keywords': 'Palabra1, Palabra2'
        }
        result = xml_pipe.extract_keywords_data(xml, lang='es')
        self.assertEqual(result, expected)

    def test_extract_keywords_data_no_kwd_group(self):
        xml = etree.fromstring('<article></article>')
        expected = {
            'title': '',
            'keywords': ''
        }
        result = xml_pipe.extract_keywords_data(xml)
        self.assertEqual(result, expected)




class TestExtractSupplementaryData(unittest.TestCase):

    def test_empty_xml_tree(self):
        xml = etree.fromstring("<root></root>")
        result = xml_pipe.extract_supplementary_data(xml)
        expected = {'title': 'Supplementary Material', 'elements': []}
        self.assertEqual(expected, result)

    def test_single_app_group_with_text(self):
        xml = etree.fromstring(
            "<root><app-group><app>Sample text content</app></app-group></root>"
        )
        result = xml_pipe.extract_supplementary_data(xml)
        expected = {
            'title': 'Supplementary Material',
            'elements': [{'content': 'Sample text content', 'type': 'text'}]
        }
        self.assertEqual(expected, result)

    def test_multiple_app_groups(self):
        xml = etree.fromstring(
            "<root>"
            "<app-group><app>Text 1</app></app-group>"
            "<app-group><app>Text 2</app></app-group>"
            "</root>"
        )
        result = xml_pipe.extract_supplementary_data(xml)
        expected = {
            'title': 'Supplementary Material',
            'elements': [
                {'content': 'Text 1', 'type': 'text'},
                {'content': 'Text 2', 'type': 'text'}
            ]
        }
        self.assertEqual(expected, result)

    def test_app_group_with_table(self):
        xml = etree.fromstring(
            "<root>"
            "<app-group>"
            "<app>"
            "<table-wrap>"
            "<label>Table 1</label>"
            "<caption><title>Sample Table</title></caption>"
            "</table-wrap>"
            "</app>"
            "</app-group>"
            "</root>"
        )
        result = xml_pipe.extract_supplementary_data(xml)
        self.assertEqual('Supplementary Material', result['title'])
        self.assertEqual(1, len(result['elements']))
        self.assertEqual('table', result['elements'][0]['type'])

    def test_mixed_content_app_group(self):
        xml = etree.fromstring(
            "<root>"
            "<app-group>"
            "<app>Text content</app>"
            "<app><table-wrap><label>Table 1</label></table-wrap></app>"
            "<app>More text</app>"
            "</app-group>"
            "</root>"
        )
        result = xml_pipe.extract_supplementary_data(xml)
        self.assertEqual(3, len(result['elements']))
        self.assertEqual('text', result['elements'][0]['type'])
        self.assertEqual('table', result['elements'][1]['type'])
        self.assertEqual('text', result['elements'][2]['type'])


class TestExtractTableData(unittest.TestCase):

    def test_extract_table_data_complete(self):
        xml_str = """
            <table-wrap>
                <label>Table 1</label>
                <title>Sample Data</title>
                <table>
                    <thead>
                        <tr><th>Name</th><th>Age</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>John</td><td>25</td></tr>
                        <tr><td>Jane</td><td>30</td></tr>
                    </tbody>
                </table>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        expected = {
            'label': 'Table 1',
            'title': 'Sample Data',
            'headers': [['Name', 'Age']],
            'rows': [['John', '25'], ['Jane', '30']]
        }
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual(expected, result)

    def test_extract_table_data_no_label_no_title(self):
        xml_str = """
            <table-wrap>
                <table>
                    <thead>
                        <tr><th>Col1</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Data1</td></tr>
                    </tbody>
                </table>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        expected = {
            'label': '',
            'title': '',
            'headers': [['Col1']],
            'rows': [['Data1']]
        }
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual(expected, result)

    def test_extract_table_data_empty_table(self):
        xml_str = """
            <table-wrap>
                <label>Table 2</label>
                <title>Empty Table</title>
                <table>
                    <thead></thead>
                    <tbody></tbody>
                </table>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        expected = {
            'label': 'Table 2',
            'title': 'Empty Table',
            'headers': [],
            'rows': []
        }
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual(expected, result)

    def test_extract_table_data_no_table(self):
        xml_str = """
            <table-wrap>
                <label>Table 3</label>
                <title>Missing Table</title>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        expected = {
            'label': 'Table 3',
            'title': 'Missing Table',
            'headers': [],
            'rows': []
        }
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual(expected, result)

    def test_extract_table_data_multiple_header_rows(self):
        xml_str = """
            <table-wrap>
                <table>
                    <thead>
                        <tr><th>Col1</th><th>Col2</th></tr>
                        <tr><th>SubCol1</th><th>SubCol2</th></tr>
                    </thead>
                    <tbody>
                        <tr><td>Val1</td><td>Val2</td></tr>
                    </tbody>
                </table>
            </table-wrap>
        """
        table_wrap = etree.fromstring(xml_str)
        expected = {
            'label': '',
            'title': '',
            'headers': [['Col1', 'Col2'], ['SubCol1', 'SubCol2']],
            'rows': [['Val1', 'Val2']]
        }
        result = xml_pipe.extract_table_data(table_wrap)
        self.assertEqual(expected, result)


class TestExtractTransAbstractData(unittest.TestCase):

    def test_extract_trans_abstract_data_basic(self):
        xml = etree.fromstring(
            '<article>'
            '<trans-abstract xml:lang="en">'
            '<title>English Abstract</title>'
            '<p>First paragraph.</p>'
            '<p>Second paragraph.</p>'
            '</trans-abstract>'
            '</article>'
        )
        expected = [
            {
                'lang': 'en',
                'title': 'English Abstract',
                'content': 'First paragraph. Second paragraph.'
            }
        ]
        result = xml_pipe.extract_trans_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_trans_abstract_data_multiple_abstracts(self):
        xml = etree.fromstring(
            '<article>'
            '<trans-abstract xml:lang="en">'
            '<title>English Abstract</title>'
            '<p>First paragraph.</p>'
            '</trans-abstract>'
            '<trans-abstract xml:lang="es">'
            '<title>Resumen en Español</title>'
            '<p>Primer párrafo.</p>'
            '</trans-abstract>'
            '</article>'
        )
        expected = [
            {
                'lang': 'en',
                'title': 'English Abstract',
                'content': 'First paragraph.'
            },
            {
                'lang': 'es',
                'title': 'Resumen en Español',
                'content': 'Primer párrafo.'
            }
        ]
        result = xml_pipe.extract_trans_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_trans_abstract_data_no_abstracts(self):
        xml = etree.fromstring('<article></article>')
        expected = []
        result = xml_pipe.extract_trans_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_trans_abstract_data_empty_abstract(self):
        xml = etree.fromstring(
            '<article>'
            '<trans-abstract xml:lang="en">'
            '<title></title>'
            '<p></p>'
            '</trans-abstract>'
            '</article>'
        )
        expected = [
            {
                'lang': 'en',
                'title': '',
                'content': ''
            }
        ]
        result = xml_pipe.extract_trans_abstract_data(xml)
        self.assertEqual(result, expected)

    def test_extract_trans_abstract_data_custom_namespace(self):
        xml = etree.fromstring(
            '<article xmlns:custom="http://custom.namespace">'
            '<trans-abstract custom:lang="fr">'
            '<title>Résumé en Français</title>'
            '<p>Premier paragraphe.</p>'
            '</trans-abstract>'
            '</article>'
        )
        expected = [
            {
                'lang': 'fr',
                'title': 'Résumé en Français',
                'content': 'Premier paragraphe.'
            }
        ]
        result = xml_pipe.extract_trans_abstract_data(
            xml, 
            namespaces={'xml': 'http://custom.namespace'}
        )
        self.assertEqual(result, expected)
