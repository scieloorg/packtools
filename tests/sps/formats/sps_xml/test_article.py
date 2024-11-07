import unittest
from xml.etree.ElementTree import Element

from packtools.sps.formats.sps_xml.article import build_article_node


class TestBuildArticleNode(unittest.TestCase):
    def test_build_article_node(self):
        article_node = build_article_node(
            article_data={
                'dtd-version': '1.1',
                'specific-use': 'sps-1.8',
                'article-type': 'research-article',
                'xml:lang': 'pt'
            }
        )

        self.assertIsInstance(article_node, Element)

        self.assertEqual(article_node.tag, 'article')

        expected_attributes = {
            'xmlns:xlink': 'http://www.w3.org/1999/xlink',
            'xmlns:mml': 'http://www.w3.org/1998/Math/MathML',
            'dtd-version': '1.1',
            'specific-use': 'sps-1.8',
            'article-type': 'research-article',
            'xml:lang': 'pt'
        }

        self.assertDictEqual(article_node.attrib, expected_attributes)

    def test_build_article_node_error(self):
        with self.assertRaises(KeyError) as e:
            build_article_node(
                article_data={
                    'specific-use': 'sps-1.8',
                    'article-type': 'research-article',
                    'xml:lang': 'pt'
                }
            )
        self.assertEqual(str(e.exception), '"\'dtd-version\' is required"')


if __name__ == '__main__':
    unittest.main()
