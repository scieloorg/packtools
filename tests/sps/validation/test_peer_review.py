import unittest
from lxml import etree

from packtools.sps.validation.peer_review import PeerReviewValidation


class ArticleAuthorsValidationTest(unittest.TestCase):
    def setUp(self):
        xml = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
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
                     </title-group>
                     <contrib-group>
                        <contrib contrib-type="author">
                           <name>
                              <surname>Doe</surname>
                              <given-names>Jane X</given-names>
                           </name>
                           <role specific-use="reviewer">Reviewer</role>
                           <xref ref-type="aff" rid="aff1" />
                        </contrib>
                     </contrib-group>
                     <aff id="aff1">...</aff>
                     <history>
                        <date date-type="reviewer-report-received">
                           <day>10</day>
                           <month>01</month>
                           <year>2022</year>
                        </date>
                     </history>
                     <permissions>...</permissions>
                     <related-article related-article-type="peer-reviewed-material" id="r01" xlink:href="10.1590/abd1806-4841.20142998" ext-link-type="doi" />
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
                  </sec>
               </body>
            <sub-article article-type="reviewer-report" id="s1" xml:lang="en">
               <front-stub>
                  <article-id pub-id-type="doi">10.1590/123456720182998OPR</article-id>
                  <article-categories>
                     <subj-group subj-group-type="heading">
                        <subject>Peer-Review</subject>
                     </subj-group>
                     ...
                  </article-categories>
                  <title-group>
                     <article-title>Open Peer Review: article X</article-title>
                  </title-group>
                  <contrib-group>
                     <contrib contrib-type="author">
                        <name>
                           <surname>Doe</surname>
                           <given-names>Jane X.</given-names>
                        </name>
                        <role specific-use="reviewer">Reviewer</role>
                        <xref ref-type="aff" rid="aff1" />
                     </contrib>
                  </contrib-group>
                  <aff id="aff1">...</aff>
                  <history>
                     <date date-type="reviewer-report-received">
                        <day>10</day>
                        <month>01</month>
                        <year>2022</year>
                     </date>
                  </history>
                  <permissions>...</permissions>
                  <custom-meta-group>
                     <custom-meta>
                        <meta-name>peer-review-recommendation</meta-name>
                        <meta-value>accept</meta-value>
                     </custom-meta>
                  </custom-meta-group>
                  ...
               </front-stub>
               <body>
                  <sec>
                     <title>Reviewer</title>
                     <p>Vivamus elementum sapien tellus, a suscipit elit auctor in. Cras est nisl,
            egestas non ultrices ut, fringilla
            eu magna. Morbi ullamcorper et diam a elementum. Phasellus vitae diam eget
            arcu dignissim ultrices. Mauris
            tempor orci metus, a finibus augue viverra id. Phasellus vitae metus quis
            metus ultrices venenatis. Integer risus
            massa, sodales in luctus eget, facilisis at ante. Aliquam pulvinar elit
            venenatis libero auctor vestibulum.</p>
                     <p>Sed in laoreet sem. Morbi vel imperdiet magna. Curabitur a velit maximus,
            volutpat metus in, posuere
            sem. Etiam eget lacus lorem. Nulla facilisi. Phasellus in mi urna. Donec
            finibus, erat non pharetra dignissim, arcu
            neque vestibulum enim, vel mollis orci nisl sit amet mauris. Nullam ac iaculis
            leo. Morbi lobortis arcu velit, at aliquet
            metus faucibus id.</p>
                  </sec>
               </body>
            </sub-article>
            </article>
            """
        self.xmltree_success = etree.fromstring(xml)

    def test_contrib_type_validation_success(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Peer review validation',
                'item': './contrib',
                'sub-item': '@contrib-type',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'author',
                'got_value': 'author',
                'message': 'Got author, expected author',
                'advice': None
            }
        ]
        obtained = list(PeerReviewValidation(self.xmltree_success).contrib_type_validation(
            contrib_type='author',
            contrib_type_list=['author']
        ))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_contrib_type_validation_fail(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Peer review validation',
                'item': './contrib',
                'sub-item': '@contrib-type',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': 'author',
                'got_value': 'reader',
                'message': 'Got reader, expected author',
                'advice': 'provide one item of this list: author',
            }
        ]
        obtained = list(PeerReviewValidation(self.xmltree_success).contrib_type_validation(
            contrib_type='reader',
            contrib_type_list=['author']
        ))
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_specific_use_validation_success(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Peer review validation',
                'item': './role',
                'sub-item': '@specific-use',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'reviewer | editor',
                'got_value': 'reviewer',
                'message': f'Got reviewer, expected reviewer | editor',
                'advice': None
            }
        ]
        obtained = list(PeerReviewValidation(self.xmltree_success).role_specific_use_validation(
            specific_use=["reviewer"],
            specific_use_list=["reviewer", "editor"]
        ))
        self.assertEqual(expected, obtained)

    def test_specific_use_validation_fail(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Peer review validation',
                'item': './role',
                'sub-item': '@specific-use',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': 'reviewer | editor',
                'got_value': 'reader',
                'message': 'Got reader, expected reviewer | editor',
                'advice': 'provide one item of this list: reviewer | editor'
            }
        ]
        obtained = list(PeerReviewValidation(self.xmltree_success).role_specific_use_validation(
            specific_use=["reader"],
            specific_use_list=["reviewer", "editor"]
        ))
        self.assertEqual(expected, obtained)

    def test_date_type_validation_success(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Peer review validation',
                'item': './date',
                'sub-item': '@date-type',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'reviewer-report-received',
                'got_value': 'reviewer-report-received',
                'message': 'Got reviewer-report-received, expected reviewer-report-received',
                'advice': None
            }
        ]
        obtained = list(PeerReviewValidation(self.xmltree_success).date_type_validation(
            date_types=["reviewer-report-received"],
            date_type_list=["reviewer-report-received"]
        ))
        self.assertEqual(expected, obtained)

    def test_date_type_validation_fail(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Peer review validation',
                'item': './date',
                'sub-item': '@date-type',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': 'reviewer-report-received',
                'got_value': 'accepted',
                'message': 'Got accepted, expected reviewer-report-received',
                'advice': 'provide one item of this list: reviewer-report-received'
            }
        ]
        obtained = list(PeerReviewValidation(self.xmltree_success).date_type_validation(
            date_types=["accepted"],
            date_type_list=["reviewer-report-received"]
        ))
        self.assertEqual(expected, obtained)

    def test_custom_meta_name_validation_success(self):
        self.maxDiff = None
        xml = etree.fromstring(
            ''' 
            <article>
            <article-meta>
            <custom-meta-group>
            <custom-meta>
            <meta-name>peer-review-recommendation</meta-name>
            <meta-value>accept</meta-value>
            </custom-meta>
            </custom-meta-group>
            </article-meta>
            </article>
            '''
        )
        expected = [
            {
                'title': 'Peer review validation',
                'item': './/custom-meta-group//custom-meta',
                'sub-item': 'meta-name',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'peer-review-recommendation',
                'got_value': 'peer-review-recommendation',
                'message': 'Got peer-review-recommendation, expected peer-review-recommendation',
                'advice': None
            }
        ]
        obtained = list(PeerReviewValidation(self.xmltree_success).custom_meta_name_validation(xml))
        self.assertEqual(expected, obtained)

    def test_custom_meta_name_validation_fail(self):
        self.maxDiff = None
        xml = etree.fromstring(
            ''' 
            <article>
            <article-meta>
            <custom-meta-group>
            <custom-meta>
            
            <meta-value>accept</meta-value>
            </custom-meta>
            </custom-meta-group>
            </article-meta>
            </article>
            '''
        )
        expected = [
            {
                'title': 'Peer review validation',
                'item': './/custom-meta-group//custom-meta',
                'sub-item': 'meta-name',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'a value for <custom-meta>',
                'got_value': None,
                'message': 'Got None, expected a value for <custom-meta>',
                'advice': 'provide a value for <custom-meta>',
            }
        ]
        obtained = list(PeerReviewValidation(self.xmltree_success).custom_meta_name_validation(xml))
        self.assertEqual(expected, obtained)

    def test_custom_meta_value_validation_success(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Peer review validation',
                'item': './/custom-meta-group//custom-meta',
                'sub-item': 'meta-value',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'revision | major-revision | minor-revision | reject | reject-with-resubmit | accept '
                                  '| formal-accept | accept-in-principle',
                'got_value': 'revision',
                'message': 'Got revision, expected revision | major-revision | minor-revision | reject | '
                           'reject-with-resubmit | accept | formal-accept | accept-in-principle',
                'advice': None
            }
        ]
        obtained = list(PeerReviewValidation(self.xmltree_success).custom_meta_value_validation(
            meta_values=['revision'],
            meta_value_list=['revision', 'major-revision', 'minor-revision', 'reject', 'reject-with-resubmit', 'accept',
                             'formal-accept', 'accept-in-principle']
        ))
        self.assertEqual(expected, obtained)

    def test_custom_meta_value_validation_fail(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Peer review validation',
                'item': './/custom-meta-group//custom-meta',
                'sub-item': 'meta-value',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': 'revision | major-revision | minor-revision | reject | reject-with-resubmit | accept '
                                  '| formal-accept | accept-in-principle',
                'got_value': 'accepted',
                'message': 'Got accepted, expected revision | major-revision | minor-revision | reject | '
                           'reject-with-resubmit | accept | formal-accept | accept-in-principle',
                'advice': 'provide one item of this list: revision | major-revision | minor-revision | reject | '
                          'reject-with-resubmit | accept | formal-accept | accept-in-principle',
            }
        ]
        obtained = list(PeerReviewValidation(self.xmltree_success).custom_meta_value_validation(
            meta_values=['accepted'],
            meta_value_list=['revision', 'major-revision', 'minor-revision', 'reject', 'reject-with-resubmit', 'accept',
                             'formal-accept', 'accept-in-principle']
        ))
        self.assertEqual(expected, obtained)

    def test_related_article_type_validation_success(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Peer review validation',
                'item': './/related-article',
                'sub-item': '@related-article-type',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'peer-reviewed-material',
                'got_value': 'peer-reviewed-material',
                'message': 'Got peer-reviewed-material, expected peer-reviewed-material',
                'advice': None
            }
        ]
        obtained = list(PeerReviewValidation(self.xmltree_success).related_article_type_validation(
            related_article_types=["peer-reviewed-material"],
            related_article_type_list=["peer-reviewed-material"]
        ))
        self.assertEqual(expected, obtained)

    def test_related_article_type_validation_fail(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Peer review validation',
                'item': './/related-article',
                'sub-item': '@related-article-type',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': 'peer-reviewed-material',
                'got_value': 'peer-reviewed',
                'message': 'Got peer-reviewed, expected peer-reviewed-material',
                'advice': 'provide one item of this list: peer-reviewed-material'
            }
        ]
        obtained = list(PeerReviewValidation(self.xmltree_success).related_article_type_validation(
            related_article_types=["peer-reviewed"],
            related_article_type_list=["peer-reviewed-material"]
        ))
        self.assertEqual(expected, obtained)

    def test_related_article_xlink_href_validation_success(self):
        self.maxDiff = None
        xml = etree.fromstring(
            ''' 
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
            <article-meta>
            <related-article related-article-type="peer-reviewed-material" id="r01" xlink:href="10.1590/abd1806-4841.20142998" ext-link-type="doi" />
            </article-meta>
            </article>
            '''
        )
        expected = [
            {
                'title': 'Peer review validation',
                'item': './/related-article',
                'sub-item': '@xlink:href',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '10.1590/abd1806-4841.20142998',
                'got_value': '10.1590/abd1806-4841.20142998',
                'message': 'Got 10.1590/abd1806-4841.20142998, expected 10.1590/abd1806-4841.20142998',
                'advice': None
            }
        ]
        obtained = list(PeerReviewValidation(self.xmltree_success).related_article_xlink_href_validation(xml))
        self.assertEqual(expected, obtained)

    def test_related_article_xlink_href_validation_fail(self):
        self.maxDiff = None
        xml = etree.fromstring(
            ''' 
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
            <article-meta>
            <related-article related-article-type="peer-reviewed-material" id="r01" ext-link-type="doi" />
            </article-meta>
            </article>
            '''
        )
        expected = [
            {
                'title': 'Peer review validation',
                'item': './/related-article',
                'sub-item': '@xlink:href',
                'validation_type': 'exist',
                'response': 'ERROR',
                'expected_value': 'a value for <related-article @xlink:href>',
                'got_value': None,
                'message': 'Got None, expected a value for <related-article @xlink:href>',
                'advice': 'provide a value for <related-article @xlink:href>',
            }
        ]
        obtained = list(PeerReviewValidation(self.xmltree_success).related_article_xlink_href_validation(xml))
        self.assertEqual(expected, obtained)

    def test_related_article_ext_link_type_validation_success(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Peer review validation',
                'item': './/related-article',
                'sub-item': '@ext-link-type',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'doi',
                'got_value': 'doi',
                'message': 'Got doi, expected doi',
                'advice': None
            }
        ]
        obtained = list(PeerReviewValidation(self.xmltree_success).related_article_ext_link_type_validation(
            link_types=['doi'],
            link_type_list=['doi']
        ))
        self.assertEqual(expected, obtained)

    def test_related_article_ext_link_type_validation_fail(self):
        self.maxDiff = None
        expected = [
            {
                'title': 'Peer review validation',
                'item': './/related-article',
                'sub-item': '@ext-link-type',
                'validation_type': 'value in list',
                'response': 'ERROR',
                'expected_value': 'doi',
                'got_value': 'uri',
                'message': 'Got uri, expected doi',
                'advice': 'provide one item of this list: doi'
            }
        ]
        obtained = list(PeerReviewValidation(self.xmltree_success).related_article_ext_link_type_validation(
            link_types=['uri'],
            link_type_list=['doi']
        ))
        self.assertEqual(expected, obtained)

    def test_peer_review_validation(self):
        self.maxDiff = None
        obtained = list(PeerReviewValidation(
            self.xmltree_success,
            contrib_type_list=['author'],
            specific_use_list=["reviewer", "editor"],
            date_type_list=["reviewer-report-received"],
            meta_value_list=['revision', 'major-revision', 'minor-revision', 'reject', 'reject-with-resubmit', 'accept',
                             'formal-accept', 'accept-in-principle'],
            related_article_type_list=["peer-reviewed-material"],
            link_type_list=['doi']
        ).peer_review_validation())
        expected = [
            {
                'title': 'Peer review validation',
                'item': './contrib',
                'sub-item': '@contrib-type',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'author',
                'got_value': 'author',
                'message': 'Got author, expected author',
                'advice': None
            },
            {
                'title': 'Peer review validation',
                'item': './role',
                'sub-item': '@specific-use',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'reviewer | editor',
                'got_value': 'reviewer',
                'message': f'Got reviewer, expected reviewer | editor',
                'advice': None
            },
            {
                'title': 'Peer review validation',
                'item': './date',
                'sub-item': '@date-type',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'reviewer-report-received',
                'got_value': 'reviewer-report-received',
                'message': 'Got reviewer-report-received, expected reviewer-report-received',
                'advice': None
            },
            {
                'title': 'Peer review validation',
                'item': './/custom-meta-group//custom-meta',
                'sub-item': 'meta-name',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'peer-review-recommendation',
                'got_value': 'peer-review-recommendation',
                'message': 'Got peer-review-recommendation, expected peer-review-recommendation',
                'advice': None
            },
            {
                'title': 'Peer review validation',
                'item': './/custom-meta-group//custom-meta',
                'sub-item': 'meta-value',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'revision | major-revision | minor-revision | reject | reject-with-resubmit | accept '
                                  '| formal-accept | accept-in-principle',
                'got_value': 'accept',
                'message': 'Got accept, expected revision | major-revision | minor-revision | reject | '
                           'reject-with-resubmit | accept | formal-accept | accept-in-principle',
                'advice': None
            },
            {
                'title': 'Peer review validation',
                'item': './contrib',
                'sub-item': '@contrib-type',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'author',
                'got_value': 'author',
                'message': 'Got author, expected author',
                'advice': None
            },
            {
                'title': 'Peer review validation',
                'item': './role',
                'sub-item': '@specific-use',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'reviewer | editor',
                'got_value': 'reviewer',
                'message': f'Got reviewer, expected reviewer | editor',
                'advice': None
            },
            {
                'title': 'Peer review validation',
                'item': './date',
                'sub-item': '@date-type',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'reviewer-report-received',
                'got_value': 'reviewer-report-received',
                'message': 'Got reviewer-report-received, expected reviewer-report-received',
                'advice': None
            },
            {
                'title': 'Peer review validation',
                'item': './/custom-meta-group//custom-meta',
                'sub-item': 'meta-name',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': 'peer-review-recommendation',
                'got_value': 'peer-review-recommendation',
                'message': 'Got peer-review-recommendation, expected peer-review-recommendation',
                'advice': None
            },
            {
                'title': 'Peer review validation',
                'item': './/custom-meta-group//custom-meta',
                'sub-item': 'meta-value',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'revision | major-revision | minor-revision | reject | reject-with-resubmit | accept '
                                  '| formal-accept | accept-in-principle',
                'got_value': 'accept',
                'message': 'Got accept, expected revision | major-revision | minor-revision | reject | '
                           'reject-with-resubmit | accept | formal-accept | accept-in-principle',
                'advice': None
            },
            {
                'title': 'Peer review validation',
                'item': './/related-article',
                'sub-item': '@related-article-type',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'peer-reviewed-material',
                'got_value': 'peer-reviewed-material',
                'message': 'Got peer-reviewed-material, expected peer-reviewed-material',
                'advice': None
            },
            {
                'title': 'Peer review validation',
                'item': './/related-article',
                'sub-item': '@xlink:href',
                'validation_type': 'exist',
                'response': 'OK',
                'expected_value': '10.1590/abd1806-4841.20142998',
                'got_value': '10.1590/abd1806-4841.20142998',
                'message': 'Got 10.1590/abd1806-4841.20142998, expected 10.1590/abd1806-4841.20142998',
                'advice': None
            },
            {
                'title': 'Peer review validation',
                'item': './/related-article',
                'sub-item': '@ext-link-type',
                'validation_type': 'value in list',
                'response': 'OK',
                'expected_value': 'doi',
                'got_value': 'doi',
                'message': 'Got doi, expected doi',
                'advice': None
            }
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)


if __name__ == '__main__':
    unittest.main()
