import unittest
from lxml import etree

from packtools.sps.models.alternatives import ArticleAlternatives, Alternative


class AlternativesTest(unittest.TestCase):
    def setUp(self):
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
                <body>
                    <table-wrap id="t5">
                        <alternatives>
                            <graphic xlink:href="nomedaimagemdatabela.svg"/>
                            <table />
                        </alternatives>
                    </table-wrap>
                </body>
                <sub-article article-type="translation" xml:lang="en" id="TRen">
                    <body>
                        <fig>
                            <alternatives>
                                <graphic xlink:href="nomedaimagemdatabela.svg"/>
                                <media />
                            </alternatives>
                        </fig>
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
        expected = ["graphic", "table"]
        self.assertListEqual(obtained, expected)

    def test_alternatives(self):
        obtained = list(ArticleAlternatives(self.xmltree).alternatives())
        expected = [
            {
                'alternative_children': ['graphic', 'table'],
                'alternative_parent': 'table-wrap',
                'parent': 'article',
                'parent_id': None
            },
            {
                'alternative_children': ['graphic', 'media'],
                'alternative_parent': 'fig',
                'parent': 'sub-article',
                'parent_id': 'TRen'
            }
        ]
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(item, obtained[i])


if __name__ == '__main__':
    unittest.main()
