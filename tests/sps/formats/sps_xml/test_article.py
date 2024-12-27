import unittest
from lxml import etree as ET


from packtools.sps.formats.sps_xml.article import build_article_node


class TestBuildArticleNode(unittest.TestCase):
    def test_build_article_node(self):
        self.maxDiff = None
        article = build_article_node(
            data={
                'dtd-version': '1.1',
                'specific-use': 'sps-1.8',
                'article-type': 'research-article',
                'xml:lang': 'pt'
            },
            nodes=[
                    ET.fromstring('<front />'),
                    ET.fromstring('<body />'),
                    ET.fromstring('<back />'),
                    ET.fromstring('<sub-article />')
                ]
        )

        expected_xml_str = (
            '<article dtd-version="1.1" specific-use="sps-1.8" article-type="research-article" '
            'xml:lang="pt"><'
            'front/>'
            '<body/>'
            '<back/>'
            '<sub-article/>'
            '</article>'
        )
        generated_xml_str = ET.tostring(article, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_article_node_error_attribs(self):
        with self.assertRaises(KeyError) as e:
            build_article_node(
                data={
                    'specific-use': 'sps-1.8',
                    'article-type': 'research-article',
                    'xml:lang': 'pt'
                },
                nodes=None
            )
        self.assertEqual(str(e.exception), '"\'dtd-version\' is required"')

    def test_build_article_node_error_children(self):
        with self.assertRaises(ValueError) as e:
            build_article_node(
                data={
                    'dtd-version': '1.1',
                    'specific-use': 'sps-1.8',
                    'article-type': 'research-article',
                    'xml:lang': 'pt',
                },
                nodes=None
            )
        self.assertEqual(str(e.exception), "A list of children nodes is required")

if __name__ == '__main__':
    unittest.main()
