import unittest

from lxml import etree

from packtools.sps.models.peer_review import PeerReview


class BasePeerReviewTestCase(unittest.TestCase):
    """Base test case with helper methods"""

    def create_peer_review_xml(self, is_article=True):
        """Helper method to create test XML"""
        xml = """<?xml version="1.0" encoding="utf-8"?>
        <{root_tag} article-type="reviewer-report" xml:lang="en" id="pr1">
            <front{front_suffix}>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <anonymous/>
                            <role specific-use="reviewer"/>
                            <xref ref-type="aff" rid="aff1"/>
                        </contrib>
                    </contrib-group>
                    <permissions>
                        <license license-type="open-access" 
                                xlink:href="http://creativecommons.org/licenses/by/4.0/"
                                xml:lang="en">
                            <license-p>This is an open access article.</license-p>
                        </license>
                    </permissions>
                    <custom-meta-group>
                        <custom-meta>
                            <meta-name>Review recommendation</meta-name>
                            <meta-value>accept</meta-value>
                        </custom-meta>
                    </custom-meta-group>
                    <related-article related-article-type="peer-reviewed-material"
                                    xlink:href="10.1590/123456789"
                                    ext-link-type="doi"/>
                    <history>
                        <date date-type="received">
                            <day>15</day>
                            <month>01</month>
                            <year>2024</year>
                        </date>
                        <date date-type="accepted">
                            <day>20</day>
                            <month>01</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front{front_suffix}>
            <body>
                <p>Review content here.</p>
            </body>
        </{root_tag}>
        """.format(
            root_tag="article" if is_article else "sub-article",
            front_suffix="" if is_article else "-stub",
        )
        return etree.fromstring(xml)


class TestPeerReviewArticle(BasePeerReviewTestCase):
    """Test PeerReview class with article-type peer reviews"""

    def setUp(self):
        """Set up article-type peer review for testing"""
        self.peer_review = PeerReview(self.create_peer_review_xml(is_article=True))

    def test_related_articles(self):
        """Test related_articles property"""
        related = list(self.peer_review.related_articles)
        self.assertEqual(len(related), 1)
        self.assertEqual(related[0]["related-article-type"], "peer-reviewed-material")
        self.assertEqual(related[0]["href"], "10.1590/123456789")
        self.assertEqual(related[0]["ext-link-type"], "doi")

    def test_contribs(self):
        """Test contribs property"""
        contribs = self.peer_review.contribs
        self.assertEqual(len(contribs), 1)
        self.assertEqual(contribs[0].get("contrib-type"), "author")
        self.assertIsNotNone(contribs[0].find(".//anonymous"))
        self.assertEqual(contribs[0].find(".//role").get("specific-use"), "reviewer")

    def test_history(self):
        """Test history property"""
        history = self.peer_review.history
        self.assertIn("received", history)
        self.assertIn("accepted", history)
        received = history["received"]
        self.assertEqual(received["year"], "2024")
        self.assertEqual(received["month"], "01")
        self.assertEqual(received["day"], "15")

    def test_license_code(self):
        """Test license_code property"""
        self.assertEqual(self.peer_review.license_code, "by")

    def test_custom_meta_items(self):
        """Test custom_meta_items property"""
        items = self.peer_review.custom_meta_items
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0].meta_name, "Review recommendation")
        self.assertEqual(items[0].meta_value, "accept")
        self.assertEqual(
            items[0].data,
            {"meta_name": "Review recommendation", "meta_value": "accept"},
        )


class TestPeerReviewSubArticle(BasePeerReviewTestCase):
    """Test PeerReview class with sub-article-type peer reviews"""

    def setUp(self):
        """Set up sub-article-type peer review for testing"""
        self.peer_review = PeerReview(self.create_peer_review_xml(is_article=False))

    def test_structure(self):
        """Test subarticle structure"""
        self.assertEqual(self.peer_review.tag, "sub-article")
        self.assertEqual(self.peer_review.article_type, "reviewer-report")
        self.assertEqual(self.peer_review.front.tag, "front-stub")


class TestEmptyPeerReview(unittest.TestCase):
    """Test PeerReview class with minimal content"""

    def setUp(self):
        """Set up peer review with minimal content"""
        xml = """
        <article article-type="reviewer-report">
            <front>
                <article-meta/>
            </front>
        </article>
        """
        self.review = PeerReview(etree.fromstring(xml))

    def test_empty_content(self):
        """Test behavior with minimal content"""
        self.assertIsNone(self.review.license_code)
        self.assertEqual(self.review.history, {})
        self.assertEqual(list(self.review.custom_meta_items), [])
        self.assertEqual(list(self.review.related_articles), [])


class TestMultipleMetadata(unittest.TestCase):
    """Test PeerReview class with multiple metadata items"""

    def setUp(self):
        """Set up peer review with multiple metadata"""
        xml = """
        <article article-type="reviewer-report">
            <front>
                <article-meta>
                    <custom-meta-group>
                        <custom-meta>
                            <meta-name>Review recommendation</meta-name>
                            <meta-value>accept</meta-value>
                        </custom-meta>
                        <custom-meta>
                            <meta-name>Review confidence</meta-name>
                            <meta-value>high</meta-value>
                        </custom-meta>
                    </custom-meta-group>
                </article-meta>
            </front>
        </article>
        """
        self.review = PeerReview(etree.fromstring(xml))

    def test_multiple_custom_meta(self):
        """Test multiple custom meta items"""
        items = self.review.custom_meta_items
        self.assertEqual(len(items), 2)
        meta_names = {item.meta_name for item in items}
        meta_values = {item.meta_value for item in items}
        self.assertEqual(meta_names, {"Review recommendation", "Review confidence"})
        self.assertEqual(meta_values, {"accept", "high"})


class TestMultipleHistoryDates(unittest.TestCase):
    """Test PeerReview class with multiple history dates"""

    def setUp(self):
        """Set up peer review with multiple history dates"""
        xml = """
        <article article-type="reviewer-report">
            <front>
                <article-meta>
                    <history>
                        <date date-type="received">
                            <day>15</day>
                            <month>01</month>
                            <year>2024</year>
                        </date>
                        <date date-type="accepted">
                            <day>20</day>
                            <month>01</month>
                            <year>2024</year>
                        </date>
                        <date date-type="rev-recd">
                            <day>18</day>
                            <month>01</month>
                            <year>2024</year>
                        </date>
                    </history>
                </article-meta>
            </front>
        </article>
        """
        self.review = PeerReview(etree.fromstring(xml))

    def test_multiple_dates(self):
        """Test multiple history dates"""
        history = self.review.history
        self.assertEqual(len(history), 3)
        date_types = {"received", "accepted", "rev-recd"}
        self.assertTrue(all(key in history for key in date_types))
        self.assertTrue(
            all(
                all(field in date for field in ["day", "month", "year"])
                for date in history.values()
            )
        )


class TestPeerReviewInheritance(unittest.TestCase):
    """Test PeerReview class inheritance from Fulltext"""

    def setUp(self):
        """Set up peer review for testing inheritance"""
        xml = """
        <article article-type="reviewer-report" xml:lang="en" id="pr1">
            <front>
                <article-meta/>
            </front>
        </article>
        """
        self.review = PeerReview(etree.fromstring(xml))

    def test_inheritance(self):
        """Test inheritance from Fulltext"""
        self.assertEqual(self.review.tag, "article")
        self.assertEqual(self.review.lang, "en")
        self.assertEqual(self.review.id, "pr1")
        self.assertEqual(self.review.article_type, "reviewer-report")
        self.assertEqual(
            self.review.attribs,
            {
                "tag": "article",
                "id": "pr1",
                "lang": "en",
                "article_type": "reviewer-report",
            },
        )


if __name__ == "__main__":
    unittest.main()
