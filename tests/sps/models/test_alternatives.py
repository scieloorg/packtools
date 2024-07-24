import unittest
from lxml import etree

from packtools.sps.models.alternatives import ArticleAlternatives, Alternative


class AlternativesTest(unittest.TestCase):
    def setUp(self):
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
                <front>
                    <table-wrap id="t5">
                        <alternatives>
                            <alt_1_front />
                            <alt_2_front />
                        </alternatives>
                    </table-wrap>
                </front>
                <body>
                    <table-wrap id="t5">
                        <alternatives>
                            <alt_1_body />
                            <alt_2_body />
                        </alternatives>
                    </table-wrap>
                </body>
                <back>
                    <table-wrap id="t5">
                        <alternatives>
                            <alt_1_back />
                            <alt_2_back />
                        </alternatives>
                    </table-wrap>
                </back>
                <sub-article article-type="translation" xml:lang="en" id="TRen">
                    <body>
                        <table-wrap id="t5">
                            <alternatives>
                                <alt_1_sub-article />
                                <alt_2_sub-article />
                            </alternatives>
                        </table-wrap>
                    </body>
                </sub-article>
            </article>
            """
        )

    def test_alternative_parent(self):
        node = self.xmltree.xpath(".//alternatives")[0]
        alternative = Alternative(node)
        obtained = alternative.parent
        expected = "table-wrap"
        self.assertEqual(obtained, expected)

    def test_alternative_children(self):
        node = self.xmltree.xpath(".//alternatives")[0]
        alternative = Alternative(node)
        obtained = list(alternative.children)
        expected = ['alt_1_front', 'alt_2_front']
        self.assertListEqual(obtained, expected)

    def test_alternatives(self):
        obtained = list(ArticleAlternatives(self.xmltree).alternatives())
        expected = [
            {
                'alternative_children': ['alt_1_front', 'alt_2_front'],
                'alternative_parent': 'table-wrap',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article'
            },
            {
                'alternative_children': ['alt_1_body', 'alt_2_body'],
                'alternative_parent': 'table-wrap',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article'
            },
            {
                'alternative_children': ['alt_1_back', 'alt_2_back'],
                'alternative_parent': 'table-wrap',
                'parent': 'article',
                'parent_id': None,
                'parent_article_type': 'research-article'
            },
            {
                'alternative_children': ['alt_1_sub-article', 'alt_2_sub-article'],
                'alternative_parent': 'table-wrap',
                'parent': 'sub-article',
                'parent_id': 'TRen',
                'parent_article_type': 'translation'
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


if __name__ == '__main__':
    unittest.main()
