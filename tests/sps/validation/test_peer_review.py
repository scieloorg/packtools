from unittest import TestCase, skip

from lxml import etree

from packtools.sps.models.article_contribs import ArticleContribs, ContribGroup
from packtools.sps.models.article_dates import HistoryDates
from packtools.sps.models.related_articles import RelatedItems
from packtools.sps.validation.peer_review import (
    CustomMetaPeerReviewValidation,
    PeerReviewValidation,
    XMLPeerReviewValidation,
)

ARTICLE_DATES_RULES = {
    "day_format_error_level": "CRITICAL",
    "month_format_error_level": "CRITICAL",
    "year_format_error_level": "CRITICAL",
    "format_error_level": "CRITICAL",
    "value_error_level": "CRITICAL",
    "limit_error_level": "CRITICAL",
    "unexpected_events_error_level": "CRITICAL",
    "missing_events_error_level": "CRITICAL",
    "history_order_error_level": "CRITICAL",
    "required_events": ["received", "accepted"],
    "pre_pub_ordered_events": ["preprint", "received", "revised", "accepted"],
    "pos_pub_ordered_events": ["pub", "corrected", "retracted"],
    "parent": {"parent": None},
    "required_history_events_for_related_article_type": {
        "correction-forward": "corrected",
        "addendum": "corrected",
        "commentary-article": "commented",
        "correction": "corrected",
        "letter": None,
        "partial-retraction": "retracted",
        "retraction": "retracted",
        "response": None,
        "peer-reviewed-article": None,
        "preprint": "preprint",
        "updated-article": "updated",
        "companion": None,
        "republished-article": "republished",
        "corrected-article": "corrected",
        "expression-of-concern": None,
    },
    "required_history_events_for_article_type": {
        "reviewer-report": "reviewer-report-received",
    },
    "limit_date": None,
}
RELATED_ARTICLE_RULES = {
    "attrib_order_error_level": "CRITICAL",
    "required_related_articles_error_level": "CRITICAL",
    "type_error_level": "CRITICAL",
    "ext_link_type_error_level": "CRITICAL",
    "uri_error_level": "CRITICAL",
    "uri_format_error_level": "CRITICAL",
    "doi_error_level": "CRITICAL",
    "doi_format_error_level": "CRITICAL",
    "id_error_level": "CRITICAL",
    "ext_link_type_list": ["doi", "uri"],
    "attrib_order": [
        "related-article-type",
        "id",
        "{http://www.w3.org/1999/xlink}href",
        "ext-link-type",
    ],
    "required_history_events": {
        "preprint": "preprint",
        "correction-forward": "corrected",
    },
    "article-types-and-related-article-types": {
        "correction": {
            "required_related_article_types": ["corrected-article"],
            "acceptable_related_article_types": [],
        },
        "research-article": {
            "required_related_article_types": [],
            "acceptable_related_article_types": [
                "correction-forward",
                "retraction-forward",
                "partial-retraction",
                "addendum",
                "commentary",
                "reviewer-report",
                "preprint",
            ],
        },
        "review-article": {
            "required_related_article_types": [],
            "acceptable_related_article_types": [
                "correction-forward",
                "retraction-forward",
                "partial-retraction",
                "addendum",
                "commentary",
                "reviewer-report",
                "preprint",
            ],
        },
        "case-report": {
            "required_related_article_types": [],
            "acceptable_related_article_types": [
                "correction-forward",
                "retraction-forward",
                "partial-retraction",
                "addendum",
                "commentary",
                "reviewer-report",
                "preprint",
            ],
        },
        "brief-report": {
            "required_related_article_types": [],
            "acceptable_related_article_types": [
                "correction-forward",
                "retraction-forward",
                "partial-retraction",
                "addendum",
                "commentary",
                "reviewer-report",
                "preprint",
            ],
        },
        "data-article": {
            "required_related_article_types": [],
            "acceptable_related_article_types": [
                "correction-forward",
                "retraction-forward",
                "partial-retraction",
                "addendum",
                "commentary",
                "reviewer-report",
                "preprint",
            ],
        },
        "retraction": {
            "required_related_article_types": ["retracted-article"],
            "acceptable_related_article_types": [],
        },
        "partial-retraction": {
            "required_related_article_types": ["retracted-article"],
            "acceptable_related_article_types": [],
        },
        "addendum": {
            "required_related_article_types": ["article"],
            "acceptable_related_article_types": [],
        },
        "article-commentary": {
            "required_related_article_types": ["commentary-article"],
            "acceptable_related_article_types": [],
        },
        "letter": {
            "required_related_article_types": [],
            "acceptable_related_article_types": ["article", "letter"],
        },
        "reply": {
            "required_related_article_types": ["letter"],
            "acceptable_related_article_types": [],
        },
        "editorial": {
            "required_related_article_types": [],
            "acceptable_related_article_types": [
                "correction-forward",
                "retraction-forward",
                "partial-retraction",
                "addendum",
                "commentary",
            ],
        },
        "reviewer-report": {
            "required_related_article_types": ["peer-reviewed-material"],
            "acceptable_related_article_types": [],
        },
        "preprint": {
            "required_related_article_types": [],
            "acceptable_related_article_types": ["article"],
        },
    },
}

ARTICLE_TYPE_RULES = {
    "article_type_error_level": "CRITICAL",
    "article_type_vs_subject_expected_similarity": "1",
    "article_type_vs_subject_expected_similarity_error_level": "WARNING",
    "article_type_vs_subject_target_article_types": ["letter"],
    "article_type_list": [
        "addendum",
        "article-commentary",
        "book-review",
        "brief-report",
        "case-report",
        "correction",
        "editorial",
        "data-article",
        "letter",
        "obituary",
        "partial-retraction",
        "product-review",
        "rapid-communication",
        "reply",
        "research-article",
        "retraction",
        "review-article",
        "reviewer-report",
        "other",
    ],
    "article_types_requires": [
        "case-report",
        "research-article",
        "review-article",
    ],
}

PEER_REVIEW_RULES = {
    "article_type_list": ["reviewer-report"],
    "required_events": [
        "reviewer-report-received",
    ],
    "pre_pub_ordered_events": [
        "reviewer-report-received",
    ],
    "date_type_list": [
        "accepted",
        "editor-assigned",
        "editor-decision",
        "published",
        "received",
        "reviewer-report-received",
        "reviewer-report-sent",
        "revision-received",
        "revision-requested",
        "revised",
    ],
    "meta_value_list": [
        "revision",
        "major-revision",
        "minor-revision",
        "reject",
        "reject-with-resubmit",
        "accept",
        "formal-accept",
        "accept-in-principle",
    ],
    "related_article_type_list": ["peer-reviewed-material"],
    "meta_name_error_level": "CRITICAL",
    "meta_value_error_level": "CRITICAL",
    "meta_value_list_error_level": "WARNING",
    "affiliations_error_level": "",
    "credit_taxonomy_terms_and_urls": [],
    "contrib_role_specific_use_error_level": "CRITICAL",
    "contrib_role_specific_use_list": ["reviewer", "editor"],
}

CONTRIB_RULES = {
    "contrib_role_error_level": "CRITICAL",
    "credit_taxonomy_terms_and_urls_error_level": "CRITICAL",
    "orcid_format_error_level": "CRITICAL",
    "orcid_is_registered_error_level": "ERROR",
    "collab_list_error_level": "CRITICAL",
    "name_error_level": "CRITICAL",
    "collab_error_level": "CRITICAL",
    "name_or_collab_error_level": "CRITICAL",
    "affiliations_error_level": "CRITICAL",
    "orcid_is_unique_error_level": "CRITICAL",
    "contrib_type_list": ["author"],
    "contrib_role_specific_use_list": [],
    "contrib_role_specific_use_error_level": "CRITICAL",
    "credit_taxonomy_terms_and_urls": [],
    "affiliations_error_level": "",
}

PARAMS = {}
PARAMS.update(CONTRIB_RULES)
PARAMS.update(ARTICLE_DATES_RULES)
PARAMS.update(RELATED_ARTICLE_RULES)
PARAMS.update(ARTICLE_TYPE_RULES)
PARAMS.update(PEER_REVIEW_RULES)


class BasePeerReviewTest(TestCase):
    """Base test class with common utilities"""

    def setUp(self):
        self.params = {
            "article_type_list": ["reviewer-report"],
            "date_type_list": [
                "accepted",
                "editor-assigned",
                "editor-decision",
                "published",
                "received",
                "reviewer-report-received",
                "reviewer-report-sent",
                "revision-received",
                "revision-requested",
                "revised",
            ],
            "meta_value_list": [
                "revision",
                "major-revision",
                "minor-revision",
                "reject",
                "reject-with-resubmit",
                "accept",
                "formal-accept",
                "accept-in-principle",
            ],
            "related_article_type_list": ["peer-reviewed-material"],
            "contrib_type_list": ["reviewer", "editor"],
        }

    def _count_validation_errors(self, results, error_level="CRITICAL"):
        """Helper method to count validation errors of specific level"""
        return sum(1 for r in results if r["response"] == error_level)


class TestArticlePeerReview(BasePeerReviewTest):
    """Test cases for peer review as article"""

    def setUp(self):
        super().setUp()
        self.xml = """
        <article  xmlns:xlink="http://www.w3.org/1999/xlink" article-type="reviewer-report" xml:lang="en">
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <anonymous/>
                            <role specific-use="reviewer"/>
                        </contrib>
                    </contrib-group>
                    <permissions>
                        <license license-type="open-access" 
                                xlink:href="http://creativecommons.org/licenses/by/4.0/"
                                xml:lang="en">
                            <license-p>This is an open access article.</license-p>
                        </license>
                    </permissions>
                    <history>
                        <date date-type="reviewer-report-received">
                            <day>15</day>
                            <month>01</month>
                            <year>2024</year>
                        </date>
                    </history>
                    <custom-meta-group>
                        <custom-meta>
                            <meta-name>Review recommendation</meta-name>
                            <meta-value>accept</meta-value>
                        </custom-meta>
                    </custom-meta-group>
                </article-meta>
            </front>
        </article>
        """
        self.node = etree.fromstring(self.xml)
        self.validator = PeerReviewValidation(self.node, PARAMS)

    def test_valid_article_type(self):
        """Test article type validation"""
        errors = list(self.validator.validate_article_type())
        self.assertEqual(len(errors), 0)

    def test_valid_contributor(self):
        """Test contributor validation"""
        errors = list(self.validator.validate_contribs())
        # content-type (credit)
        self.assertEqual(len(errors), 0)

    def test_valid_history_dates(self):
        """Test history dates validation"""
        errors = list(self.validator.validate_history_dates())
        self.assertEqual(len(errors), 0)

    def test_valid_custom_meta(self):
        """Test custom meta validation"""
        errors = list(self.validator.validate_custom_meta())
        self.assertEqual(len(errors), 0)


class TestSubArticlePeerReview(BasePeerReviewTest):
    """Test cases for peer review as sub-article"""

    def setUp(self):
        super().setUp()
        self.xml = """
        <article  xmlns:xlink="http://www.w3.org/1999/xlink">
            <front>
                <article-meta/>
            </front>
            <sub-article article-type="reviewer-report" xml:lang="en">
                <front-stub>
                    <contrib-group>
                        <contrib contrib-type="author">
                            <anonymous/>
                            <role specific-use="reviewer"/>
                        </contrib>
                    </contrib-group>
                    <permissions>
                        <license license-type="open-access" 
                                xlink:href="http://creativecommons.org/licenses/by/4.0/"
                                xml:lang="en">
                            <license-p>This is an open access article.</license-p>
                        </license>
                    </permissions>
                    <history>
                        <date date-type="reviewer-report-received">
                            <day>15</day>
                            <month>01</month>
                            <year>2024</year>
                        </date>
                    </history>
                    <custom-meta-group>
                        <custom-meta>
                            <meta-name>Review recommendation</meta-name>
                            <meta-value>accept</meta-value>
                        </custom-meta>
                    </custom-meta-group>
                    <related-article related-article-type="peer-reviewed-material"
                                   xlink:href="10.1590/123456789"
                                   ext-link-type="doi"/>
                </front-stub>
            </sub-article>
        </article>
        """
        self.node = etree.fromstring(self.xml).find(".")
        self.validator = XMLPeerReviewValidation(self.node, PARAMS)

    def test_valid_sub_article(self):
        """Test overall sub-article validation"""
        errors = list(self.validator.validate())
        self.assertEqual(len(errors), 2)
        self.assertIn(
            "Set related-article attributes in this", errors[0]["advice"]
        )
        self.assertIn("Add id attribute", errors[1]["advice"])


class TestInvalidPeerReview(BasePeerReviewTest):
    """Test cases for invalid peer reviews"""

    def setUp(self):
        super().setUp()
        self.xml = """
        <article  xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <contrib-group>
                        <contrib contrib-type="editor">
                            <name>
                                <surname>Smith</surname>
                                <given-names>John</given-names>
                            </name>
                            <role specific-use="invalid-role"/>
                        </contrib>
                    </contrib-group>
                    <custom-meta-group>
                        <custom-meta>
                            <meta-name>Review recommendation</meta-name>
                            <meta-value>invalid-recommendation</meta-value>
                        </custom-meta>
                    </custom-meta-group>
                </article-meta>
            </front>
        </article>
        """
        self.node = etree.fromstring(self.xml)
        self.validator = PeerReviewValidation(self.node, PARAMS)

    def test_invalid_article_type(self):
        """Test article type validation with invalid type"""
        errors = list(self.validator.validate_article_type())
        self.assertEqual(1, len(errors))

    def test_invalid_contributor_type(self):
        """Test contributor validation with invalid type"""
        errors = list(self.validator.validate_contribs())
        self.assertEqual(2, len(errors))

    def test_missing_history_dates(self):
        """Test history dates validation with missing dates"""
        errors = list(self.validator.validate_history_dates())
        self.assertEqual(1, len(errors))


class TestCustomMetaValidation(BasePeerReviewTest):
    """Test cases for custom meta validation"""

    def setUp(self):
        super().setUp()
        self.xml_template = """
        <article  xmlns:xlink="http://www.w3.org/1999/xlink" article-type="reviewer-report" xml:lang="en">
            <front>
                <article-meta>
                    <custom-meta-group>
                        {}
                    </custom-meta-group>
                </article-meta>
            </front>
        </article>
        """

    def test_missing_meta_name(self):
        """Test validation with missing meta-name"""
        xml = self.xml_template.format(
            """
            <custom-meta>
                <meta-value>accept</meta-value>
            </custom-meta>
        """
        )
        validator = PeerReviewValidation(
            etree.fromstring(xml).find("."), PARAMS
        )
        errors = list(validator.validate_custom_meta())
        self.assertTrue(any(e["response"] == "CRITICAL" for e in errors))

    def test_missing_meta_value(self):
        """Test validation with missing meta-value"""
        xml = self.xml_template.format(
            """
            <custom-meta>
                <meta-name>Review recommendation</meta-name>
            </custom-meta>
        """
        )
        validator = PeerReviewValidation(
            etree.fromstring(xml).find("."), PARAMS
        )
        errors = list(validator.validate_custom_meta())
        self.assertTrue(any(e["response"] == "CRITICAL" for e in errors))


class TestRelatedArticlesValidation(BasePeerReviewTest):
    """Test cases for related articles validation"""

    def setUp(self):
        super().setUp()
        self.xml = """
        <article  xmlns:xlink="http://www.w3.org/1999/xlink" article-type="reviewer-report" xml:lang="en">
            <front>
                <article-meta>
                    <related-article related-article-type="peer-reviewed-material"
                                   xlink:href="10.1590/123456789"
                                   ext-link-type="doi"/>
                </article-meta>
            </front>
        </article>
        """
        self.node = etree.fromstring(self.xml).find(".")
        self.validator = PeerReviewValidation(self.node, PARAMS)

    def test_valid_related_article(self):
        """Test valid related article validation"""
        errors = list(self.validator.validate_related_articles())
        self.assertIn(
            "Set related-article attributes in this", errors[0]["advice"]
        )
        self.assertIn("Add id attribute", errors[1]["advice"])
        self.assertEqual(len(errors), 2)

    def test_invalid_related_article_type(self):
        """Test invalid related article type"""
        xml = self.xml.replace("peer-reviewed-material", "invalid-type")
        validator = PeerReviewValidation(
            etree.fromstring(xml).find("."), PARAMS
        )
        errors = list(validator.validate_related_articles())

        expected = [
            {
                "got_value": ["invalid-type"],
                "expected_value": ["peer-reviewed-material"],
                "advice": """Article type "reviewer-report" requires related articles of types: ['peer-reviewed-material']""",
                "response": "CRITICAL",
            },
            {
                "got_value": [
                    "related-article-type",
                    "{http://www.w3.org/1999/xlink}href",
                    "ext-link-type",
                ],
                "expected_value": [
                    "related-article-type",
                    "id",
                    "{http://www.w3.org/1999/xlink}href",
                    "ext-link-type",
                ],
                "advice": """Set related-article attributes in this order ['related-article-type', 'id', '{http://www.w3.org/1999/xlink}href', 'ext-link-type']""",
                "response": "CRITICAL",
            },
            {
                "got_value": "invalid-type",
                "expected_value": ["peer-reviewed-material"],
                "advice": """The article-type: reviewer-report does not match the related-article-type: invalid-type, provide one of the following items: ['peer-reviewed-material']""",
                "response": "CRITICAL",
            },
            {
                "got_value": None,
                "expected_value": "A non-empty ID",
                "advice": "Add id attribute to related-article",
                "response": "CRITICAL",
            },
        ]
        self.assertEqual(len(errors), 4)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertEqual(item["got_value"], errors[i]["got_value"])
                self.assertEqual(
                    item["expected_value"], errors[i]["expected_value"]
                )
                self.assertEqual(item["advice"], errors[i]["advice"])
                self.assertEqual(item["response"], errors[i]["response"])
