import unittest
from unittest import skip

from lxml import etree

from packtools.sps.models.article_contribs import ArticleContribs, ContribGroup
from packtools.sps.models.article_dates import HistoryDates
from packtools.sps.models.peer_review import CustomMetaGroup
from packtools.sps.models.related_articles import RelatedItems

from packtools.sps.validation.peer_review import (
    AuthorPeerReviewValidation,
    DatePeerReviewValidation,
    CustomMetaPeerReviewValidation,
    RelatedArticleValidation,
    PeerReviewsValidation,
)


class ArticleAuthorsValidationTest(unittest.TestCase):
    @skip("Teste pendente de correção e/ou ajuste")
    def test_contrib_type_validation_success(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
                <front>
                <article-meta>
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
                </article-meta>
                </front>
            </article>
                """
        )
        expected = [
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "reviewer-report",
                "parent_lang": "en",
                "item": "contrib",
                "sub_item": "@contrib-type",
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["author"],
                "got_value": "author",
                "message": "Got author, expected ['author']",
                "advice": None,
                "data": {
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                    "contrib_full_name": "Jane X Doe",
                    "contrib_name": {"given-names": "Jane X", "surname": "Doe"},
                    "contrib_role": [
                        {
                            "content-type": None,
                            "specific-use": "reviewer",
                            "text": "Reviewer",
                        }
                    ],
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                },
            }
        ]
        contrib = list(ArticleContribs(self.xmltree).contribs)[0]
        obtained = list(
            AuthorPeerReviewValidation(
                contrib=contrib,
                contrib_type_list=["author"],
            ).contrib_type_validation
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    @skip("Teste pendente de correção e/ou ajuste")
    def test_contrib_type_validation_fail(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
                <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="compiler">
                            <name>
                                <surname>Doe</surname>
                                <given-names>Jane X</given-names>
                            </name>
                            <role specific-use="reviewer">Reviewer</role>
                            <xref ref-type="aff" rid="aff1" />
                        </contrib>
                    </contrib-group>
                </article-meta>
                </front>
            </article>
                """
        )
        expected = [
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "reviewer-report",
                "parent_lang": "en",
                "item": "contrib",
                "sub_item": "@contrib-type",
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": ["author"],
                "got_value": "compiler",
                "message": "Got compiler, expected ['author']",
                "advice": "provide one item of this list: ['author']",
                "data": {
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                    "contrib_full_name": "Jane X Doe",
                    "contrib_name": {"given-names": "Jane X", "surname": "Doe"},
                    "contrib_role": [
                        {
                            "content-type": None,
                            "specific-use": "reviewer",
                            "text": "Reviewer",
                        }
                    ],
                    "contrib_type": "compiler",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                },
            }
        ]
        contrib = list(ArticleContribs(self.xmltree).contribs)[0]
        obtained = list(
            AuthorPeerReviewValidation(
                contrib=contrib,
                contrib_type_list=["author"],
            ).contrib_type_validation
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    @skip("Teste pendente de correção e/ou ajuste")
    def test_specific_use_validation_success(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
                <front>
                <article-meta>
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
                </article-meta>
                </front>
            </article>
                """
        )
        expected = [
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "reviewer-report",
                "parent_lang": "en",
                "item": "role",
                "sub_item": "@specific-use",
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["reviewer", "editor"],
                "got_value": ["reviewer"],
                "message": "Got ['reviewer'], expected ['reviewer', 'editor']",
                "advice": None,
                "data": {
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                    "contrib_full_name": "Jane X Doe",
                    "contrib_name": {"given-names": "Jane X", "surname": "Doe"},
                    "contrib_role": [
                        {
                            "content-type": None,
                            "specific-use": "reviewer",
                            "text": "Reviewer",
                        }
                    ],
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                },
            }
        ]
        contrib = list(ArticleContribs(self.xmltree).contribs)[0]
        obtained = list(
            AuthorPeerReviewValidation(
                contrib=contrib,
                contrib_type_list=["author"],
                specific_use_list=["reviewer", "editor"],
            ).role_specific_use_validation
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    @skip("Teste pendente de correção e/ou ajuste")
    def test_specific_use_validation_fail(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
                <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Doe</surname>
                                <given-names>Jane X</given-names>
                            </name>
                            <role specific-use="review">Reviewer</role>
                            <xref ref-type="aff" rid="aff1" />
                        </contrib>
                    </contrib-group>
                </article-meta>
                </front>
            </article>
                """
        )
        expected = [
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "reviewer-report",
                "parent_lang": "en",
                "item": "role",
                "sub_item": "@specific-use",
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": ["reviewer", "editor"],
                "got_value": ["review"],
                "message": "Got ['review'], expected ['reviewer', 'editor']",
                "advice": "provide one item of this list: ['reviewer', 'editor']",
                "data": {
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                    "contrib_full_name": "Jane X Doe",
                    "contrib_name": {"given-names": "Jane X", "surname": "Doe"},
                    "contrib_role": [
                        {
                            "content-type": None,
                            "specific-use": "review",
                            "text": "Reviewer",
                        }
                    ],
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                },
            }
        ]
        contrib = list(ArticleContribs(self.xmltree).contribs)[0]
        obtained = list(
            AuthorPeerReviewValidation(
                contrib=contrib,
                contrib_type_list=["author"],
                specific_use_list=["reviewer", "editor"],
            ).role_specific_use_validation
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    @skip("Teste pendente de correção e/ou ajuste")
    def test_date_type_validation_success(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
                <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Doe</surname>
                                <given-names>Jane X</given-names>
                            </name>
                            <role specific-use="review">Reviewer</role>
                            <xref ref-type="aff" rid="aff1" />
                        </contrib>
                    </contrib-group>
                    <history>
                        <date date-type="reviewer-report-received">
                            <day>10</day>
                            <month>01</month>
                            <year>2022</year>
                        </date>
                    </history>
                </article-meta>
                </front>
            </article>
                """
        )
        expected = [
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "reviewer-report",
                "parent_lang": "en",
                "item": "date",
                "sub_item": "@date-type",
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["reviewer-report-received"],
                "got_value": "reviewer-report-received",
                "message": "Got reviewer-report-received, expected ['reviewer-report-received']",
                "advice": None,
                "data": {
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                    "article_date": None,
                    "collection_date": None,
                    "history": {
                        "reviewer-report-received": {
                            "day": "10",
                            "month": "01",
                            "type": "reviewer-report-received",
                            "year": "2022",
                        },
                    },
                },
            }
        ]
        date = list(HistoryDates(self.xmltree).history_dates())[0]
        obtained = list(
            DatePeerReviewValidation(
                date=date,
                date_type="reviewer-report-received",
                date_type_list=["reviewer-report-received"],
            ).date_type_validation
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    @skip("Teste pendente de correção e/ou ajuste")
    def test_date_type_validation_fail(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
                <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Doe</surname>
                                <given-names>Jane X</given-names>
                            </name>
                            <role specific-use="review">Reviewer</role>
                            <xref ref-type="aff" rid="aff1" />
                        </contrib>
                    </contrib-group>
                    <history>
                        <date date-type="accepted">
                            <day>10</day>
                            <month>01</month>
                            <year>2022</year>
                        </date>
                    </history>
                </article-meta>
                </front>
            </article>
                """
        )
        expected = [
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "reviewer-report",
                "parent_lang": "en",
                "item": "date",
                "sub_item": "@date-type",
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": ["reviewer-report-received"],
                "got_value": "accepted",
                "message": "Got accepted, expected ['reviewer-report-received']",
                "advice": "provide one item of this list: ['reviewer-report-received']",
                "data": {
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                    "article_date": None,
                    "collection_date": None,
                    "history": {
                        "accepted": {
                            "day": "10",
                            "month": "01",
                            "type": "accepted",
                            "year": "2022",
                        },
                    },
                },
            }
        ]
        date = list(HistoryDates(self.xmltree).history_dates())[0]
        obtained = list(
            DatePeerReviewValidation(
                date=date,
                date_type="accepted",
                date_type_list=["reviewer-report-received"],
            ).date_type_validation
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    @skip("Teste pendente de correção e/ou ajuste")
    def test_custom_meta_value_validation_success(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
                <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Doe</surname>
                                <given-names>Jane X</given-names>
                            </name>
                            <role specific-use="review">Reviewer</role>
                            <xref ref-type="aff" rid="aff1" />
                        </contrib>
                    </contrib-group>
                    <history>
                        <date date-type="reviewer-report-received">
                            <day>10</day>
                            <month>01</month>
                            <year>2022</year>
                        </date>
                    </history>
                    <custom-meta-group>
                        <custom-meta>
                           <meta-name>peer-review-recommendation</meta-name>
                           <meta-value>revision</meta-value>
                        </custom-meta>
                     </custom-meta-group>
                </article-meta>
                </front>
            </article>
                """
        )
        expected = [
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "reviewer-report",
                "parent_lang": "en",
                "item": "custom-meta",
                "sub_item": "meta-value",
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["revision", "major-revision"],
                "got_value": "revision",
                "message": "Got revision, expected ['revision', 'major-revision']",
                "advice": None,
                "data": {
                    "meta_name": "peer-review-recommendation",
                    "meta_value": "revision",
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                },
            }
        ]
        custom_meta = list(CustomMetaGroup(self.xmltree).data)[0]
        obtained = list(
            CustomMetaPeerReviewValidation(
                custom_meta=custom_meta, meta_value_list=["revision", "major-revision"]
            ).custom_meta_value_validation
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    @skip("Teste pendente de correção e/ou ajuste")
    def test_custom_meta_value_validation_fail(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
                <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Doe</surname>
                                <given-names>Jane X</given-names>
                            </name>
                            <role specific-use="review">Reviewer</role>
                            <xref ref-type="aff" rid="aff1" />
                        </contrib>
                    </contrib-group>
                    <history>
                        <date date-type="reviewer-report-received">
                            <day>10</day>
                            <month>01</month>
                            <year>2022</year>
                        </date>
                    </history>
                    <custom-meta-group>
                        <custom-meta>
                           <meta-name>peer-review-recommendation</meta-name>
                           <meta-value>accepted</meta-value>
                        </custom-meta>
                     </custom-meta-group>
                </article-meta>
                </front>
            </article>
                """
        )
        expected = [
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "reviewer-report",
                "parent_lang": "en",
                "item": "custom-meta",
                "sub_item": "meta-value",
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": ["revision", "major-revision"],
                "got_value": "accepted",
                "message": "Got accepted, expected ['revision', 'major-revision']",
                "advice": "provide one item of this list: ['revision', 'major-revision']",
                "data": {
                    "meta_name": "peer-review-recommendation",
                    "meta_value": "accepted",
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                },
            }
        ]
        custom_meta = list(CustomMetaGroup(self.xmltree).data)[0]
        obtained = list(
            CustomMetaPeerReviewValidation(
                custom_meta=custom_meta, meta_value_list=["revision", "major-revision"]
            ).custom_meta_value_validation
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_custom_meta_name_validation_success(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
                <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Doe</surname>
                                <given-names>Jane X</given-names>
                            </name>
                            <role specific-use="review">Reviewer</role>
                            <xref ref-type="aff" rid="aff1" />
                        </contrib>
                    </contrib-group>
                    <history>
                        <date date-type="reviewer-report-received">
                            <day>10</day>
                            <month>01</month>
                            <year>2022</year>
                        </date>
                    </history>
                    <custom-meta-group>
                        <custom-meta>
                           <meta-name>peer-review-recommendation</meta-name>
                           <meta-value>revision</meta-value>
                        </custom-meta>
                     </custom-meta-group>
                </article-meta>
                </front>
            </article>
                """
        )
        expected = [
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "reviewer-report",
                "parent_lang": "en",
                "item": "custom-meta",
                "sub_item": "meta-name",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "peer-review-recommendation",
                "got_value": "peer-review-recommendation",
                "message": "Got peer-review-recommendation, expected peer-review-recommendation",
                "advice": None,
                "data": {
                    "meta_name": "peer-review-recommendation",
                    "meta_value": "revision",
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                },
            }
        ]
        custom_meta = list(CustomMetaGroup(self.xmltree).data)[0]
        obtained = list(
            CustomMetaPeerReviewValidation(
                custom_meta=custom_meta, meta_value_list=["revision", "major-revision"]
            ).custom_meta_name_validation
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_custom_meta_name_validation_fail(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
                <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Doe</surname>
                                <given-names>Jane X</given-names>
                            </name>
                            <role specific-use="review">Reviewer</role>
                            <xref ref-type="aff" rid="aff1" />
                        </contrib>
                    </contrib-group>
                    <history>
                        <date date-type="reviewer-report-received">
                            <day>10</day>
                            <month>01</month>
                            <year>2022</year>
                        </date>
                    </history>
                    <custom-meta-group>
                        <custom-meta>
                           <meta-name></meta-name>
                           <meta-value>revision</meta-value>
                        </custom-meta>
                     </custom-meta-group>
                </article-meta>
                </front>
            </article>
                """
        )
        expected = [
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "reviewer-report",
                "parent_lang": "en",
                "item": "custom-meta",
                "sub_item": "meta-name",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": "a value for <custom-meta>",
                "got_value": None,
                "message": "Got None, expected a value for <custom-meta>",
                "advice": "provide a value for <custom-meta>",
                "data": {
                    "meta_name": None,
                    "meta_value": "revision",
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                },
            }
        ]
        custom_meta = list(CustomMetaGroup(self.xmltree).data)[0]
        obtained = list(
            CustomMetaPeerReviewValidation(
                custom_meta=custom_meta, meta_value_list=["revision", "major-revision"]
            ).custom_meta_name_validation
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    @skip("Teste pendente de correção e/ou ajuste")
    def test_related_article_type_validation_success(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
                <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Doe</surname>
                                <given-names>Jane X</given-names>
                            </name>
                            <role specific-use="review">Reviewer</role>
                            <xref ref-type="aff" rid="aff1" />
                        </contrib>
                    </contrib-group>
                    <history>
                        <date date-type="reviewer-report-received">
                            <day>10</day>
                            <month>01</month>
                            <year>2022</year>
                        </date>
                    </history>
                    <related-article related-article-type="peer-reviewed-material" id="r01" xlink:href="10.1590/abd1806-4841.20142998" ext-link-type="doi" />
                    <custom-meta-group>
                        <custom-meta>
                           <meta-name>peer-review-recommendation</meta-name>
                           <meta-value>revision</meta-value>
                        </custom-meta>
                     </custom-meta-group>
                </article-meta>
                </front>
            </article>
                """
        )
        expected = [
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_article_type": "reviewer-report",
                "parent_id": None,
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["peer-reviewed-material"],
                "got_value": "peer-reviewed-material",
                "message": "Got peer-reviewed-material, expected ['peer-reviewed-material']",
                "advice": None,
                "data": {
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                    "ext-link-type": "doi",
                    "id": "r01",
                    "related-article-type": "peer-reviewed-material",
                    "href": "10.1590/abd1806-4841.20142998",
                },
            }
        ]
        related_article = list(RelatedItems(self.xmltree).related_articles)[0]
        obtained = list(
            RelatedArticleValidation(
                related_article=related_article,
                related_article_type_list=["peer-reviewed-material"],
                link_type_list=["doi"],
            ).related_article_type_validation
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    @skip("Teste pendente de correção e/ou ajuste")
    def test_related_article_type_validation_fail(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
                <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Doe</surname>
                                <given-names>Jane X</given-names>
                            </name>
                            <role specific-use="review">Reviewer</role>
                            <xref ref-type="aff" rid="aff1" />
                        </contrib>
                    </contrib-group>
                    <history>
                        <date date-type="reviewer-report-received">
                            <day>10</day>
                            <month>01</month>
                            <year>2022</year>
                        </date>
                    </history>
                    <related-article related-article-type="major-revision" id="r01" xlink:href="10.1590/abd1806-4841.20142998" ext-link-type="doi" />
                    <custom-meta-group>
                        <custom-meta>
                           <meta-name>peer-review-recommendation</meta-name>
                           <meta-value>revision</meta-value>
                        </custom-meta>
                     </custom-meta-group>
                </article-meta>
                </front>
            </article>
            """
        )
        expected = [
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_article_type": "reviewer-report",
                "parent_id": None,
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": ["peer-reviewed-material"],
                "got_value": "major-revision",
                "message": "Got major-revision, expected ['peer-reviewed-material']",
                "advice": "provide one item of this list: ['peer-reviewed-material']",
                "data": {
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                    "ext-link-type": "doi",
                    "id": "r01",
                    "related-article-type": "major-revision",
                    "href": "10.1590/abd1806-4841.20142998",
                },
            }
        ]
        related_article = list(RelatedItems(self.xmltree).related_articles)[0]
        obtained = list(
            RelatedArticleValidation(
                related_article=related_article,
                related_article_type_list=["peer-reviewed-material"],
                link_type_list=["doi"],
            ).related_article_type_validation
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    @skip("Teste pendente de correção e/ou ajuste")
    def test_related_article_ext_link_type_validation_success(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
                <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Doe</surname>
                                <given-names>Jane X</given-names>
                            </name>
                            <role specific-use="review">Reviewer</role>
                            <xref ref-type="aff" rid="aff1" />
                        </contrib>
                    </contrib-group>
                    <history>
                        <date date-type="reviewer-report-received">
                            <day>10</day>
                            <month>01</month>
                            <year>2022</year>
                        </date>
                    </history>
                    <related-article related-article-type="peer-reviewed-material" id="r01" xlink:href="10.1590/abd1806-4841.20142998" ext-link-type="doi" />
                    <custom-meta-group>
                        <custom-meta>
                           <meta-name>peer-review-recommendation</meta-name>
                           <meta-value>revision</meta-value>
                        </custom-meta>
                     </custom-meta-group>
                </article-meta>
                </front>
            </article>
                """
        )
        expected = [
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_article_type": "reviewer-report",
                "parent_id": None,
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@ext-link-type",
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["doi"],
                "got_value": "doi",
                "message": "Got doi, expected ['doi']",
                "advice": None,
                "data": {
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                    "ext-link-type": "doi",
                    "id": "r01",
                    "related-article-type": "peer-reviewed-material",
                    "href": "10.1590/abd1806-4841.20142998",
                },
            }
        ]
        related_article = list(RelatedItems(self.xmltree).related_articles)[0]
        obtained = list(
            RelatedArticleValidation(
                related_article=related_article,
                related_article_type_list=["peer-reviewed-material"],
                link_type_list=["doi"],
            ).related_article_ext_link_type_validation
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    @skip("Teste pendente de correção e/ou ajuste")
    def test_related_article_ext_link_type_validation_fail(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
                <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Doe</surname>
                                <given-names>Jane X</given-names>
                            </name>
                            <role specific-use="review">Reviewer</role>
                            <xref ref-type="aff" rid="aff1" />
                        </contrib>
                    </contrib-group>
                    <history>
                        <date date-type="reviewer-report-received">
                            <day>10</day>
                            <month>01</month>
                            <year>2022</year>
                        </date>
                    </history>
                    <related-article related-article-type="peer-reviewed-material" id="r01" xlink:href="10.1590/abd1806-4841.20142998" ext-link-type="uri" />
                    <custom-meta-group>
                        <custom-meta>
                           <meta-name>peer-review-recommendation</meta-name>
                           <meta-value>revision</meta-value>
                        </custom-meta>
                     </custom-meta-group>
                </article-meta>
                </front>
            </article>
                """
        )
        expected = [
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_article_type": "reviewer-report",
                "parent_id": None,
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@ext-link-type",
                "validation_type": "value in list",
                "response": "ERROR",
                "expected_value": ["doi"],
                "got_value": "uri",
                "message": "Got uri, expected ['doi']",
                "advice": "provide one item of this list: ['doi']",
                "data": {
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                    "ext-link-type": "uri",
                    "id": "r01",
                    "related-article-type": "peer-reviewed-material",
                    "href": "10.1590/abd1806-4841.20142998",
                },
            }
        ]
        related_article = list(RelatedItems(self.xmltree).related_articles)[0]
        obtained = list(
            RelatedArticleValidation(
                related_article=related_article,
                related_article_type_list=["peer-reviewed-material"],
                link_type_list=["doi"],
            ).related_article_ext_link_type_validation
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_related_article_xlink_href_validation_success(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
                <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Doe</surname>
                                <given-names>Jane X</given-names>
                            </name>
                            <role specific-use="review">Reviewer</role>
                            <xref ref-type="aff" rid="aff1" />
                        </contrib>
                    </contrib-group>
                    <history>
                        <date date-type="reviewer-report-received">
                            <day>10</day>
                            <month>01</month>
                            <year>2022</year>
                        </date>
                    </history>
                    <related-article related-article-type="peer-reviewed-material" id="r01" xlink:href="10.1590/abd1806-4841.20142998" ext-link-type="doi" />
                    <custom-meta-group>
                        <custom-meta>
                           <meta-name>peer-review-recommendation</meta-name>
                           <meta-value>revision</meta-value>
                        </custom-meta>
                     </custom-meta-group>
                </article-meta>
                </front>
            </article>
                """
        )
        expected = [
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_article_type": "reviewer-report",
                "parent_id": None,
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@xlink:href",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "10.1590/abd1806-4841.20142998",
                "got_value": "10.1590/abd1806-4841.20142998",
                "message": "Got 10.1590/abd1806-4841.20142998, expected 10.1590/abd1806-4841.20142998",
                "advice": None,
                "data": {
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                    "ext-link-type": "doi",
                    "id": "r01",
                    "related-article-type": "peer-reviewed-material",
                    "href": "10.1590/abd1806-4841.20142998",
                },
            }
        ]
        related_article = list(RelatedItems(self.xmltree).related_articles)[0]
        obtained = list(
            RelatedArticleValidation(
                related_article=related_article,
                related_article_type_list=["peer-reviewed-material"],
                link_type_list=["doi"],
            ).related_article_href_validation
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_related_article_xlink_href_validation_fail(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
                <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <name>
                                <surname>Doe</surname>
                                <given-names>Jane X</given-names>
                            </name>
                            <role specific-use="review">Reviewer</role>
                            <xref ref-type="aff" rid="aff1" />
                        </contrib>
                    </contrib-group>
                    <history>
                        <date date-type="reviewer-report-received">
                            <day>10</day>
                            <month>01</month>
                            <year>2022</year>
                        </date>
                    </history>
                    <related-article related-article-type="peer-reviewed-material" id="r01" ext-link-type="doi" />
                    <custom-meta-group>
                        <custom-meta>
                           <meta-name>peer-review-recommendation</meta-name>
                           <meta-value>revision</meta-value>
                        </custom-meta>
                     </custom-meta-group>
                </article-meta>
                </front>
            </article>
                """
        )
        expected = [
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_article_type": "reviewer-report",
                "parent_id": None,
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@xlink:href",
                "validation_type": "exist",
                "response": "ERROR",
                "expected_value": "a value for <related-article @xlink:href>",
                "got_value": None,
                "message": "Got None, expected a value for <related-article @xlink:href>",
                "advice": "provide a value for <related-article @xlink:href>",
                "data": {
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                    "ext-link-type": "doi",
                    "id": "r01",
                    "related-article-type": "peer-reviewed-material",
                },
            }
        ]
        related_article = list(RelatedItems(self.xmltree).related_articles)[0]
        obtained = list(
            RelatedArticleValidation(
                related_article=related_article,
                related_article_type_list=["peer-reviewed-material"],
                link_type_list=["doi"],
            ).related_article_href_validation
        )

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    @skip("Teste pendente de correção e/ou ajuste")
    def test_peer_review_validation(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
                <front>
                <article-meta>
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
                    <history>
                        <date date-type="reviewer-report-received">
                            <day>10</day>
                            <month>01</month>
                            <year>2022</year>
                        </date>
                    </history>
                    <related-article related-article-type="peer-reviewed-material" id="r01" xlink:href="10.1590/abd1806-4841.20142998" ext-link-type="doi" />
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
        )
        obtained = list(
            PeerReviewsValidation(
                self.xmltree,
                contrib_type_list=["author"],
                specific_use_list=["reviewer", "editor"],
                date_type_list=["reviewer-report-received"],
                meta_value_list=["accept", "formal-accept"],
                related_article_type_list=["peer-reviewed-material"],
                link_type_list=["doi"],
            ).validate()
        )
        expected = [
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "reviewer-report",
                "parent_lang": "en",
                "item": "contrib",
                "sub_item": "@contrib-type",
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["author"],
                "got_value": "author",
                "message": "Got author, expected ['author']",
                "advice": None,
                "data": {
                    "contrib_full_name": "Jane X Doe",
                    "contrib_name": {"given-names": "Jane X", "surname": "Doe"},
                    "contrib_role": [
                        {
                            "content-type": None,
                            "specific-use": "reviewer",
                            "text": "Reviewer",
                        }
                    ],
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                },
            },
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "reviewer-report",
                "parent_lang": "en",
                "item": "role",
                "sub_item": "@specific-use",
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["reviewer", "editor"],
                "got_value": ["reviewer"],
                "message": "Got ['reviewer'], expected ['reviewer', 'editor']",
                "advice": None,
                "data": {
                    "contrib_full_name": "Jane X Doe",
                    "contrib_name": {"given-names": "Jane X", "surname": "Doe"},
                    "contrib_role": [
                        {
                            "content-type": None,
                            "specific-use": "reviewer",
                            "text": "Reviewer",
                        }
                    ],
                    "contrib_type": "author",
                    "contrib_xref": [{"ref_type": "aff", "rid": "aff1", "text": None}],
                },
            },
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "reviewer-report",
                "parent_lang": "en",
                "item": "date",
                "sub_item": "@date-type",
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["reviewer-report-received"],
                "got_value": "reviewer-report-received",
                "message": "Got reviewer-report-received, expected ['reviewer-report-received']",
                "advice": None,
                "data": {
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                    "article_date": None,
                    "collection_date": None,
                    "history": {
                        "reviewer-report-received": {
                            "day": "10",
                            "month": "01",
                            "type": "reviewer-report-received",
                            "year": "2022",
                        },
                    },
                },
            },
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "reviewer-report",
                "parent_lang": "en",
                "item": "custom-meta",
                "sub_item": "meta-name",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "peer-review-recommendation",
                "got_value": "peer-review-recommendation",
                "message": "Got peer-review-recommendation, expected peer-review-recommendation",
                "advice": None,
                "data": {
                    "meta_name": "peer-review-recommendation",
                    "meta_value": "accept",
                },
            },
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_id": None,
                "parent_article_type": "reviewer-report",
                "parent_lang": "en",
                "item": "custom-meta",
                "sub_item": "meta-value",
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["accept", "formal-accept"],
                "got_value": "accept",
                "message": "Got accept, expected ['accept', 'formal-accept']",
                "advice": None,
                "data": {
                    "meta_name": "peer-review-recommendation",
                    "meta_value": "accept",
                },
            },
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_article_type": "reviewer-report",
                "parent_id": None,
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@related-article-type",
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["peer-reviewed-material"],
                "got_value": "peer-reviewed-material",
                "message": "Got peer-reviewed-material, expected ['peer-reviewed-material']",
                "advice": None,
                "data": {
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                    "ext-link-type": "doi",
                    "id": "r01",
                    "related-article-type": "peer-reviewed-material",
                    "href": "10.1590/abd1806-4841.20142998",
                    "text": "",
                },
            },
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_article_type": "reviewer-report",
                "parent_id": None,
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@xlink:href",
                "validation_type": "exist",
                "response": "OK",
                "expected_value": "10.1590/abd1806-4841.20142998",
                "got_value": "10.1590/abd1806-4841.20142998",
                "message": "Got 10.1590/abd1806-4841.20142998, expected 10.1590/abd1806-4841.20142998",
                "advice": None,
                "data": {
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                    "ext-link-type": "doi",
                    "id": "r01",
                    "related-article-type": "peer-reviewed-material",
                    "href": "10.1590/abd1806-4841.20142998",
                    "text": "",
                },
            },
            {
                "title": "Peer review validation",
                "parent": "article",
                "parent_article_type": "reviewer-report",
                "parent_id": None,
                "parent_lang": "en",
                "item": "related-article",
                "sub_item": "@ext-link-type",
                "validation_type": "value in list",
                "response": "OK",
                "expected_value": ["doi"],
                "got_value": "doi",
                "message": "Got doi, expected ['doi']",
                "advice": None,
                "data": {
                    "parent": "article",
                    "parent_article_type": "reviewer-report",
                    "parent_id": None,
                    "parent_lang": "en",
                    "ext-link-type": "doi",
                    "id": "r01",
                    "related-article-type": "peer-reviewed-material",
                    "href": "10.1590/abd1806-4841.20142998",
                    "text": "",
                },
            },
        ]

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_peer_review_keys_validation(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            dtdversion="1.3" specific-use="sps-1.10" article-type="reviewer-report" xml:lang="en">
                <front>
                <article-meta>
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
                    <history>
                        <date date-type="reviewer-report-received">
                            <day>10</day>
                            <month>01</month>
                            <year>2022</year>
                        </date>
                    </history>
                    <related-article related-article-type="peer-reviewed-material" id="r01" xlink:href="10.1590/abd1806-4841.20142998" ext-link-type="doi" />
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
        )
        validations = PeerReviewsValidation(
            self.xmltree,
            contrib_type_list=["author"],
            specific_use_list=["reviewer", "editor"],
            date_type_list=["reviewer-report-received"],
            meta_value_list=["accept", "formal-accept"],
            related_article_type_list=["peer-reviewed-material"],
            link_type_list=["doi"],
        )

        obtained_dicts = list(validations.validate())

        expected_keys = [
            "title",
            "parent",
            "parent_id",
            "item",
            "sub_item",
            "validation_type",
            "response",
            "expected_value",
            "got_value",
            "message",
            "advice",
        ]

        for expected_key in expected_keys:
            for item, obtained_dict in enumerate(obtained_dicts):
                with self.subTest(f"{expected_key} ({item})"):
                    self.assertIn(expected_key, obtained_dict.keys())


if __name__ == "__main__":
    unittest.main()
