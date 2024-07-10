import unittest
from lxml import etree as ET
from packtools.sps.models.peer_review import PeerReview, CustomMeta

class PeerReviewArticleTest(unittest.TestCase):
    def setUp(self):
        xml_success = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" 
                     xmlns:mml="http://www.w3.org/1998/Math/MathML"
                     dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
                <front>
                    <article-meta>
                        <custom-meta-group>
                            <custom-meta>
                                <meta-name>peer-review-recommendation</meta-name>
                                <meta-value>accept</meta-value>
                            </custom-meta>
                        </custom-meta-group>
                    </article-meta>
                </front>
            </article>
        """
        xml_fail = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" 
                     xmlns:mml="http://www.w3.org/1998/Math/MathML"
                     dtdversion="1.3" specific-use="sps-1.10" xml:lang="en">
                <front>
                    <article-meta>
                        <custom-meta-group>
                            <custom-meta>
                                <meta-name></meta-name>
                                <meta-value></meta-value>
                            </custom-meta>
                        </custom-meta-group>
                    </article-meta>
                </front>
            </article>
        """

        self.custom_meta_success = CustomMeta(ET.fromstring(xml_success))
        self.peer_review_success = PeerReview(ET.fromstring(xml_success))
        self.custom_meta_fail = CustomMeta(ET.fromstring(xml_fail))

    def test_meta_name_success(self):
        expected = 'peer-review-recommendation'
        obtained = self.custom_meta_success.meta_name
        self.assertEqual(expected, obtained)

    def test_meta_name_fail(self):
        obtained = self.custom_meta_fail.meta_name
        self.assertIsNone(obtained)

    def test_meta_value_success(self):
        expected = 'accept'
        obtained = self.custom_meta_success.meta_value
        self.assertEqual(expected, obtained)

    def test_meta_value_fail(self):
        obtained = self.custom_meta_fail.meta_value
        self.assertIsNone(obtained)

    def test_custom_meta_data(self):
        obtained = list(self.peer_review_success.data)
        expected = [
            {
                'parent': 'article',
                'parent_article_type': 'reviewer-report',
                'parent_id': None,
                'parent_lang': 'en',
                'meta_name': 'peer-review-recommendation',
                'meta_value': 'accept'
            }
        ]
        self.assertEqual(expected, obtained)


if __name__ == '__main__':
    unittest.main()
