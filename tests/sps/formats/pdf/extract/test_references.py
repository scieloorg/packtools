import unittest

from lxml import etree

from packtools.sps.formats.pdf.extract import references


class TestExtractReferencesData(unittest.TestCase):

    def test_extract_references_data_empty_xml(self):
        xmltree = etree.fromstring("<root></root>")
        expected = {'title': 'References', 'references': []}
        result = references.extract_references_data(xmltree)
        self.assertEqual(expected, result)

    def test_extract_references_data_with_empty_ref_list(self):
        xmltree = etree.fromstring("<root><ref-list></ref-list></root>")
        expected = {'title': 'References', 'references': []}
        result = references.extract_references_data(xmltree)
        self.assertEqual(expected, result)

    def test_extract_references_data_with_multiple_references(self):
        xml_content = """
            <root>
                <ref-list>
                    <ref>
                        <mixed-citation>Reference 1</mixed-citation>
                    </ref>
                    <ref>
                        <mixed-citation>Reference 2</mixed-citation>
                    </ref>
                </ref-list>
            </root>
        """
        xmltree = etree.fromstring(xml_content)
        result = references.extract_references_data(xmltree)
        self.assertEqual('References', result['title'])
        self.assertEqual(2, len(result['references']))
        self.assertEqual('Reference 1', result['references'][0].text)
        self.assertEqual('Reference 2', result['references'][1].text)

    def test_extract_references_data_with_nested_ref_list(self):
        xml_content = """
            <root>
                <article>
                    <back>
                        <ref-list>
                            <ref>
                                <mixed-citation>Nested Reference</mixed-citation>
                            </ref>
                        </ref-list>
                    </back>
                </article>
            </root>
        """
        xmltree = etree.fromstring(xml_content)
        result = references.extract_references_data(xmltree)
        self.assertEqual(1, len(result['references']))
        self.assertEqual('Nested Reference', result['references'][0].text)

    def test_extract_references_data_without_mixed_citation(self):
        xml_content = """
            <root>
                <ref-list>
                    <ref>
                        <element-citation>Citation without mixed</element-citation>
                    </ref>
                </ref-list>
            </root>
        """
        xmltree = etree.fromstring(xml_content)
        result = references.extract_references_data(xmltree)
        self.assertEqual(0, len(result['references']))
