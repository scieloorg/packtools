import unittest

from lxml import etree as ET

from packtools.sps.models.peer_review import PeerReview


class PeerReviewArticleTest(unittest.TestCase):
    def setUp(self):
        xmltree = ET.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" 
            xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
            <front>
            <article-meta>
            <article-id pub-id-type="doi">10.1590/123456720182998OPR</article-id>
            <article-categories>
            <subj-group subj-group-type="heading">
            <subject>Peer-Review</subject>
            </subj-group>
            </article-categories>
            <title-group>
            <article-title>Open Peer Review: article X</article-title>
            </title-group><contrib-group>
            <contrib contrib-type="author">
            <name>
            <surname>Doe</surname>
            <given-names>Jane X</given-names>
            </name>
            <role specific-use="reviewer">Reviewer</role>
            <xref ref-type="aff" rid="aff1"/>
            </contrib>
            </contrib-group>
            <aff id="aff1"> ... </aff>
            <history>
            <date date-type="reviewer-report-received">
            <day>10</day>
            <month>01</month>
            <year>2022</year>
            </date>
            </history>
            <permissions> ... </permissions>
            <related-article related-article-type="peer-reviewed-material" id="r01"
            xlink:href="10.1590/abd1806-4841.20142998" ext-link-type="doi"/>
            <custom-meta-group>
            <custom-meta>
            <meta-name>peer-review-recommendation</meta-name>
            <meta-value>accept</meta-value>
            </custom-meta>
            </custom-meta-group>
            </article-meta>
            </front>
            <body>
            <sec>
            <title>Reviewer</title>
            <p>Vivamus elementum sapien tellus, a suscipit elit auctor in. Cras est nisl,
            egestas
            non ultrices ut, fringilla eu magna. Morbi ullamcorper et diam a elementum.
            Phasellus vitae diam eget arcu dignissim ultrices.</p>
            <p>Sed in laoreet sem. Morbi vel imperdiet magna. Curabitur a velit maximus,
            volutpat
            metus in, posuere sem. Etiam eget lacus lorem. Nulla facilisi..</p>
            </sec></body>
            </article>
            """)
        self.peer_review_success = PeerReview(xmltree)

        xmltree = ET.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" 
            xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtdversion="1.3" specific-use="sps-1.10" xml:lang="en">
            <front>
            <article-meta>
            
            <article-categories>
            <subj-group subj-group-type="heading">
            <subject>Peer-Review</subject>
            </subj-group>
            </article-categories>
            <contrib-group>
            <contrib>
            <name>
            <surname>Doe</surname>
            <given-names>Jane X</given-names>
            </name>
            <role>Reviewer</role>
            <xref ref-type="aff" rid="aff1"/>
            </contrib>
            </contrib-group>
            <aff id="aff1"> ... </aff>
            <history>
            
            </history>
            <permissions> ... </permissions>
            <related-article related-article-type="peer-reviewed-material" id="r01"
            xlink:href="10.1590/abd1806-4841.20142998" ext-link-type="doi"/>
            
            </article-meta>
            </front>
            <body>
            <sec>
            <title>Reviewer</title>
            <p>Vivamus elementum sapien tellus, a suscipit elit auctor in. Cras est nisl,
            egestas
            non ultrices ut, fringilla eu magna. Morbi ullamcorper et diam a elementum.
            Phasellus vitae diam eget arcu dignissim ultrices.</p>
            <p>Sed in laoreet sem. Morbi vel imperdiet magna. Curabitur a velit maximus,
            volutpat
            metus in, posuere sem. Etiam eget lacus lorem. Nulla facilisi..</p>
            </sec></body>
            </article>
            """)
        self.peer_review_fail = PeerReview(xmltree)

    def test_meta_name_success(self):
        expected = ['peer-review-recommendation']
        obtained = list(self.peer_review_success.meta_names)
        self.assertEqual(expected, obtained)

    def test_meta_name_fail(self):
        obtained = list(self.peer_review_fail.meta_names)
        self.assertEqual(obtained, [])

    def test_meta_value_success(self):
        expected = ['accept']
        obtained = list(self.peer_review_success.meta_values)
        self.assertEqual(expected, obtained)

    def test_meta_value_fail(self):
        obtained = list(self.peer_review_fail.meta_values)
        self.assertEqual(obtained, [])


if __name__ == '__main__':
    unittest.main()
