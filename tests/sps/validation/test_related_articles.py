from unittest import TestCase, skip
from unittest.mock import Mock, patch

from lxml import etree
from packtools.sps.validation.related_articles import (
    XMLRelatedArticlesValidation,
    RelatedArticleValidation,
    FulltextRelatedArticlesValidation,
)


PARAMS = {
    "attrib_order_error_level": "INFO",
    "required_related_articles_error_level": "CRITICAL",
    "type_error_level": "CRITICAL",
    "ext_link_type_error_level": "CRITICAL",
    "uri_error_level": "CRITICAL",
    "uri_format_error_level": "CRITICAL",
    "doi_error_level": "CRITICAL",
    "doi_format_error_level": "CRITICAL",
    "id_error_level": "CRITICAL",
    "related_article_type_presence_error_level": "CRITICAL",
    "ext_link_type_presence_error_level": "CRITICAL",
    "related_article_type_value_error_level": "ERROR",
    "ext_link_type_value_error_level": "ERROR",
    "xlink_href_presence_error_level": "ERROR",
    "doi_preference_error_level": "WARNING",
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


class BaseRelatedArticleTest(TestCase):
    """Base test class with common setup"""

    def setUp(self):
        self.params = PARAMS


class TestRelatedArticlesValidation(BaseRelatedArticleTest):
    def setUp(self):
        super().setUp()

        self.xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="correction">
                <front>
                    <related-article related-article-type="corrected-article"/>
                </front>
            </article>"""

        self.xmltree = etree.fromstring(self.xml)

    @patch(
        "packtools.sps.validation.related_articles.FulltextRelatedArticlesValidation"
    )
    @patch("packtools.sps.validation.related_articles.FulltextRelatedArticles")
    def test_initialization(self, mock_fulltext, mock_validation):
        """Test if classes are properly initialized"""
        # Arrange
        mock_fulltext_instance = Mock()
        mock_fulltext.return_value = mock_fulltext_instance

        mock_validation_instance = Mock()
        mock_validation.return_value = mock_validation_instance

        # Act
        validator = XMLRelatedArticlesValidation(self.xmltree, self.params)

        # Assert
        mock_fulltext.assert_not_called()
        mock_validation.assert_called_once_with(self.xmltree.find("."), self.params)
        self.assertEqual(validator.params, self.params)

    @patch(
        "packtools.sps.validation.related_articles.FulltextRelatedArticlesValidation"
    )
    @patch("packtools.sps.validation.related_articles.FulltextRelatedArticles")
    def test_initialization_default_params(self, mock_fulltext, mock_validation):
        """Test initialization with default parameters"""
        # Act
        validator = XMLRelatedArticlesValidation(self.xmltree, self.params)

        # Assert
        self.assertEqual(validator.params, self.params)

    @patch(
        "packtools.sps.validation.related_articles.FulltextRelatedArticlesValidation"
    )
    @patch("packtools.sps.validation.related_articles.FulltextRelatedArticles")
    def test_validate_method_calls(self, mock_fulltext, mock_validation):
        """Test if validate method properly calls FulltextRelatedArticlesValidation.validate"""
        # Arrange
        mock_validation_instance = Mock()
        mock_validation.return_value = mock_validation_instance

        expected_results = [{"result": 1}, {"result": 2}]
        mock_validation_instance.validate.return_value = iter(expected_results)

        # Act
        validator = XMLRelatedArticlesValidation(self.xmltree, self.params)
        results = list(validator.validate())

        # Assert
        mock_validation_instance.validate.assert_called_once()
        self.assertEqual(results, expected_results)

    def test_integration_with_real_xml(self):
        """Test integration with real XML document"""
        # Arrange
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="correction">
                <front>
                    <related-article related-article-type="corrected-article" 
                                   ext-link-type="doi" 
                                   xlink:href="10.1000/xyz123"/>
                </front>
            </article>"""
        xmltree = etree.fromstring(xml)

        # Act
        validator = XMLRelatedArticlesValidation(xmltree, self.params)
        results = list(validator.validate())

        # Assert
        self.assertTrue(len(results) > 0)
        for result in results:
            self.assertIn("response", result)
            self.assertIn("validation_type", result)

    def test_multiple_related_articles(self):
        """Test validation with multiple related articles"""
        # Arrange
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="correction">
                <front>
                    <related-article related-article-type="corrected-article" id="ra1"/>
                    <related-article related-article-type="corrected-article" id="ra2"/>
                </front>
            </article>"""
        xmltree = etree.fromstring(xml)

        # Act
        validator = XMLRelatedArticlesValidation(xmltree, self.params)
        results = list(validator.validate())

        # Assert
        self.assertTrue(len(results) > 0)
        ids = [r.get("data", {}).get("id") for r in results if "data" in r]
        self.assertTrue(len(set(ids)) > 1)  # Should have multiple unique IDs

    def test_error_level_inheritance(self):
        """Test if error_level is properly inherited from params"""
        # Test with custom error level
        params = self.params.copy()
        validator = XMLRelatedArticlesValidation(self.xmltree, params)
        self.assertEqual(validator.params, params)

        # Test with default error level
        validator = XMLRelatedArticlesValidation(self.xmltree, {})
        self.assertEqual(validator.params, {})

    def test_empty_document(self):
        """Test validation with empty document"""
        # Arrange
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="correction">
                <front></front>
            </article>"""
        xmltree = etree.fromstring(xml)

        # Act
        validator = XMLRelatedArticlesValidation(xmltree, self.params)
        results = list(validator.validate())

        # Assert
        self.assertTrue(len(results) > 0)
        error_results = [r for r in results if r["response"] != "OK"]
        self.assertTrue(len(error_results) > 0)


class TestRelatedArticleTypeValidation(BaseRelatedArticleTest):
    def setUp(self):
        super().setUp()
        self.base_article = {
            "parent": "article",
            "parent_article_type": "correction",
            "original_article_type": "correction",
            "parent_id": None,
            "parent_lang": "en",
            "ext-link-type": "doi",
            "href": "10.1590/1808-057x202090350",
            "id": "ra1",
            "related-article-type": "corrected-article",
        }

    def test_validate_type_match(self):
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_type()

        self.assertIsNone(result)

    def test_validate_type_no_match(self):
        self.base_article.update(
            {
                "parent_article_type": "retraction",
                "original_article_type": "retraction",
                "related-article-type": "corrected-article",
            }
        )
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_type()

        self.assertEqual(result["response"], "CRITICAL")
        self.assertEqual(result["got_value"], "corrected-article")
        self.assertEqual(result["expected_value"], ["retracted-article"])
        self.assertIn("retraction", result["advice"])
        self.assertIn("corrected-article", result["advice"])


class TestRelatedArticleLinkValidation(BaseRelatedArticleTest):
    def setUp(self):
        super().setUp()
        self.base_article = {
            "parent": "article",
            "parent_article_type": "correction",
            "original_article_type": "correction",
            "parent_id": None,
            "parent_lang": "en",
            "ext-link-type": "doi",
            "href": "10.1590/example",
            "id": "ra1",
        }

    def test_validate_doi_link(self):
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_doi()

        self.assertIsNone(result)

    def test_validate_uri_link_valid(self):
        self.base_article.update(
            {"ext-link-type": "uri", "href": "http://example.com/article"}
        )
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_uri()

        self.assertIsNone(result)

    def test_validate_uri_link_invalid(self):
        self.base_article.update({"ext-link-type": "uri", "href": "invalid-uri"})
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_uri()

        self.assertEqual(result["response"], "CRITICAL")
        self.assertEqual(result["got_value"], "invalid-uri")
        self.assertEqual(
            result["expected_value"], "A valid URI format (e.g., http://example.com)"
        )
        self.assertTrue(result["advice"].startswith("Invalid URI format"))

    def test_validate_link_missing(self):
        del self.base_article["href"]
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_doi()

        self.assertEqual(result["response"], "CRITICAL")
        self.assertIsNone(result["got_value"])
        self.assertEqual(result["expected_value"], "A valid DOI")
        self.assertTrue(result["advice"].startswith("Provide a valid DOI"))


class TestRelatedArticleExtLinkTypeValidation(BaseRelatedArticleTest):
    def setUp(self):
        super().setUp()
        self.base_article = {
            "parent": "article",
            "parent_article_type": "correction",
            "original_article_type": "correction",
            "ext-link-type": "doi",
            "href": "10.1590/example",
            "id": "ra1",
        }

    def test_validate_ext_link_type_doi(self):
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_ext_link_type()

        self.assertIsNone(result)

    def test_validate_ext_link_type_uri(self):
        self.base_article["ext-link-type"] = "uri"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_ext_link_type()

        self.assertIsNone(result)

    def test_validate_ext_link_type_invalid(self):
        self.base_article["ext-link-type"] = "url"
        self.params["ext_link_type_error_level"] = "CRITICAL"

        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_ext_link_type()

        self.assertEqual(result["response"], "CRITICAL")
        self.assertEqual(result["got_value"], "url")
        self.assertEqual(result["expected_value"], ["doi", "uri"])
        self.assertIn("ext-link-type", result["advice"])


class TestRelatedArticleFullValidation(BaseRelatedArticleTest):
    def setUp(self):
        super().setUp()
        self.base_article = {
            "parent": "article",
            "parent_article_type": "correction",
            "original_article_type": "correction",
            "parent_id": None,
            "parent_lang": "en",
            "ext-link-type": "doi",
            "href": "10.1590/example",
            "id": "ra1",
            "related-article-type": "corrected-article",
        }

    def test_validate_all_pass_doi(self):
        validator = RelatedArticleValidation(self.base_article, self.params)
        results = validator.validate()
        # All validations should pass (no errors)
        error_results = [r for r in results if r["response"] != "OK"]
        self.assertEqual(len(error_results), 0)

    def test_validate_all_pass_uri(self):
        self.base_article.update(
            {"ext-link-type": "uri", "href": "http://example.com/article"}
        )
        validator = RelatedArticleValidation(self.base_article, self.params)
        results = validator.validate()

        self.assertEqual(len(results), 1)

    def test_validate_all_with_errors(self):
        self.base_article.update(
            {
                "ext-link-type": "url",
                "href": "invalid-uri",
                "related-article-type": "invalid-type",
            }
        )

        validator = RelatedArticleValidation(self.base_article, self.params)
        results = validator.validate()

        error_count = sum(1 for r in results if r["response"] == "CRITICAL")
        self.assertGreater(error_count, 0)


class TestRelatedArticleValidation(BaseRelatedArticleTest):
    def setUp(self):
        super().setUp()
        self.base_article = {
            "parent": "article",
            "parent_article_type": "correction",
            "original_article_type": "correction",
            "ext-link-type": "doi",
            "href": "10.1590/example",
            "id": "ra1",
            "related-article-type": "corrected-article",
        }

    def test_get_error_level_default(self):
        validator = RelatedArticleValidation(self.base_article, {})
        error_level = validator._get_error_level("any_type")
        self.assertEqual(error_level, "CRITICAL")

    def test_get_error_level_custom(self):
        params = {"custom_error_level": "CUSTOM"}
        validator = RelatedArticleValidation(self.base_article, params)
        error_level = validator._get_error_level("custom")
        self.assertEqual(error_level, "CUSTOM")

    def test_validate_type_response(self):
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_type()
        self.assertIsNone(result)

    def test_validate_uri_existence(self):
        self.base_article["ext-link-type"] = "uri"
        del self.base_article["href"]
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_uri()
        self.assertEqual(result["response"], "CRITICAL")

    def test_validate_uri_format(self):
        self.base_article.update({"ext-link-type": "uri", "href": "invalid-uri"})
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_uri()
        self.assertEqual(result["response"], "CRITICAL")

    def test_validate_doi_existence(self):
        del self.base_article["href"]
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_doi()
        self.assertEqual(result["response"], "CRITICAL")

    def test_validate_doi_format(self):
        self.base_article["href"] = "invalid-doi"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_doi()
        self.assertEqual(result["response"], "CRITICAL")


class TestMissingRequiredArticle(BaseRelatedArticleTest):
    """Test case for missing required related article"""

    def setUp(self):
        super().setUp()
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink"  article-type="correction" xml:lang="en" id="a1">
            <front><article-meta></article-meta></front>
        </article>"""

        self.validator = FulltextRelatedArticlesValidation(
            etree.fromstring(xml).find("."), self.params
        )

    def test_missing_required(self):
        results = list(self.validator.validate())
        self.assertEqual(len(results), 1)
        result = results[0]
        self.assertEqual(result["response"], "CRITICAL")
        self.assertEqual(result["validation_type"], "match")
        self.assertEqual(result["title"], "Required related articles")
        self.assertIn("corrected-article", result["expected_value"])
        self.assertEqual(result["got_value"], [])


class TestOptionalArticle(BaseRelatedArticleTest):
    """Test case for article with optional related articles"""

    def setUp(self):
        super().setUp()
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink"  article-type="research-article" xml:lang="en" id="a1">
            <front><article-meta></article-meta></front>
        </article>"""

        self.validator = FulltextRelatedArticlesValidation(
            etree.fromstring(xml).find("."), self.params
        )

    def test_optional_missing(self):
        results = list(self.validator.validate())
        self.assertEqual(len(results), 0)


class TestNestedValidation(BaseRelatedArticleTest):
    """Test case for nested structure with sub-articles"""

    def setUp(self):
        super().setUp()
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink"  article-type="research-article" xml:lang="en" id="a1">
            <front>
                <article-meta>
                    <related-article related-article-type="correction-forward" 
                                   ext-link-type="doi" 
                                   id="ra1">Main text</related-article>
                </article-meta>
            </front>
            <sub-article article-type="translation" xml:lang="pt" id="s1">
                <front-stub>
                    <related-article related-article-type="other-type" 
                                   ext-link-type="doi" 
                                   id="ra2">Translation text</related-article>
                </front-stub>
            </sub-article>
        </article>"""

        self.validator = FulltextRelatedArticlesValidation(
            etree.fromstring(xml).find("."), self.params
        )

    def test_nested_validation(self):
        results = list(self.validator.validate())

        # Find CRITICAL errors in translation sub-article
        translation_errors = [
            r
            for r in results
            if r["parent_article_type"] == "translation" and r["response"] == "CRITICAL"
        ]

        self.assertEqual(len(translation_errors), 2)
        type_error = [r for r in translation_errors if r["title"] == "Related article type"][0]
        self.assertEqual(type_error["validation_type"], "match")
        self.assertIn("correction-forward", type_error["expected_value"])


class TestValidStructure(BaseRelatedArticleTest):
    """Test case for valid structure with all required articles"""

    def setUp(self):
        super().setUp()
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink"  article-type="correction" xml:lang="en" id="a1">
            <front>
                <article-meta>
                    <related-article related-article-type="corrected-article" 
                                   ext-link-type="doi" 
                                   xlink:href="10.1590/dois"
                                   id="ra1">Correction text</related-article>
                </article-meta>
            </front>
            <sub-article article-type="translation" xml:lang="pt" id="s1">
                <front-stub>
                    <related-article related-article-type="corrected-article" 
                                   ext-link-type="doi" 
                                   xlink:href="10.1590/dois"
                                   id="ra2">Translation text</related-article>
                </front-stub>
            </sub-article>
        </article>"""

        self.validator = FulltextRelatedArticlesValidation(
            etree.fromstring(xml).find("."), self.params
        )

    def test_valid_structure(self):
        results = list(self.validator.validate())
        errors = [r for r in results if r["response"] != "OK"]
        self.assertEqual(len(errors), 2)


class TestMultipleSubArticles(BaseRelatedArticleTest):
    """Test case for multiple sub-articles with different requirements"""

    def setUp(self):
        super().setUp()
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink"  article-type="research-article" xml:lang="en" id="a1">
            <front>
                <article-meta>
                    <related-article related-article-type="correction-forward" 
                                   ext-link-type="doi" 
                                   xlink:href="10.1590/xxxx"
                                   id="ra1">Main text</related-article>
                </article-meta>
            </front>
            <sub-article article-type="translation" xml:lang="es" id="s1">
                <front-stub>
                    <related-article related-article-type="correction-forward" 
                                   id="ra2"
                                   xlink:href="10.1590/xxxx"
                                   ext-link-type="doi" 
                                   >Spanish translation</related-article>
                </front-stub>
            </sub-article>
            <sub-article article-type="translation" xml:lang="pt" id="s2">
                <front-stub>
                    <related-article related-article-type="other-type" 
                                   ext-link-type="doi" 
                                   xlink:href="10.1590/xxxx"
                                   id="ra3">Portuguese translation</related-article>
                </front-stub>
            </sub-article>
        </article>"""

        self.validator = FulltextRelatedArticlesValidation(
            etree.fromstring(xml).find("."), self.params
        )

    def test_multiple_sub_articles(self):
        results = list(self.validator.validate())

        # First sub-article should be valid
        spanish_errors = [
            r for r in results if r["parent_id"] == "s1" and r["response"] != "OK"
        ]
        self.assertEqual(len(spanish_errors), 0)

        # Second sub-article should have CRITICAL error for type mismatch
        portuguese_critical = [
            r for r in results if r["parent_id"] == "s2" and r["response"] == "CRITICAL"
        ]
        self.assertEqual(len(portuguese_critical), 1)


class TestOriginalArticleType(BaseRelatedArticleTest):
    """Test case for original_article_type inheritance"""

    def setUp(self):
        super().setUp()
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink"  article-type="research-article" xml:lang="en" id="a1">
            <sub-article article-type="translation" xml:lang="pt" id="s1">
                <front-stub>
                    <related-article related-article-type="correction-forward" 
                                   ext-link-type="doi" 
                                   id="ra1">Translation</related-article>
                </front-stub>
                <sub-article article-type="abstract" id="s2">
                    <front-stub>
                        <related-article related-article-type="abstract-of" 
                                       ext-link-type="doi" 
                                       id="ra2">Abstract</related-article>
                    </front-stub>
                </sub-article>
            </sub-article>
        </article>"""

        self.validator = FulltextRelatedArticlesValidation(
            etree.fromstring(xml).find("."), self.params
        )

    def test_original_article_type_inheritance(self):
        results = list(self.validator.validate())

        translation_data = [r for r in results if r["parent_id"] == "s1"][0]

        self.assertEqual(
            translation_data["data"].get("original_article_type"), "research-article"
        )


# ============================================================
# New tests for SPS 1.10 related-article validations
# ============================================================


class TestRelatedArticleTypePresence(BaseRelatedArticleTest):
    """Tests for validate_related_article_type_presence (CRITICAL)"""

    def setUp(self):
        super().setUp()
        self.base_article = {
            "parent": "article",
            "parent_article_type": "correction",
            "original_article_type": "correction",
            "parent_id": None,
            "parent_lang": "en",
            "ext-link-type": "doi",
            "href": "10.1590/example",
            "id": "ra1",
            "related-article-type": "corrected-article",
        }

    def test_related_article_type_present(self):
        """@related-article-type is present: should return None (OK)"""
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_presence()
        self.assertIsNone(result)

    def test_related_article_type_missing(self):
        """@related-article-type is missing: should return CRITICAL"""
        del self.base_article["related-article-type"]
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_presence()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "CRITICAL")
        self.assertIn("@related-article-type", result["sub_item"])

    def test_related_article_type_empty(self):
        """@related-article-type is empty string: should return CRITICAL"""
        self.base_article["related-article-type"] = ""
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_presence()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "CRITICAL")

    def test_related_article_type_whitespace_only(self):
        """@related-article-type is only spaces: should return CRITICAL"""
        self.base_article["related-article-type"] = "   "
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_presence()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "CRITICAL")

    def test_related_article_type_presence_has_i18n(self):
        """Presence validation should include i18n fields"""
        del self.base_article["related-article-type"]
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_presence()
        self.assertIsNotNone(result["adv_text"])
        self.assertIsNotNone(result["adv_params"])


class TestExtLinkTypePresence(BaseRelatedArticleTest):
    """Tests for validate_ext_link_type_presence (CRITICAL)"""

    def setUp(self):
        super().setUp()
        self.base_article = {
            "parent": "article",
            "parent_article_type": "correction",
            "original_article_type": "correction",
            "parent_id": None,
            "parent_lang": "en",
            "ext-link-type": "doi",
            "href": "10.1590/example",
            "id": "ra1",
            "related-article-type": "corrected-article",
        }

    def test_ext_link_type_present(self):
        """@ext-link-type is present: should return None (OK)"""
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_ext_link_type_presence()
        self.assertIsNone(result)

    def test_ext_link_type_missing(self):
        """@ext-link-type is missing: should return CRITICAL"""
        del self.base_article["ext-link-type"]
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_ext_link_type_presence()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "CRITICAL")
        self.assertIn("@ext-link-type", result["sub_item"])

    def test_ext_link_type_empty(self):
        """@ext-link-type is empty string: should return CRITICAL"""
        self.base_article["ext-link-type"] = ""
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_ext_link_type_presence()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "CRITICAL")

    def test_ext_link_type_whitespace_only(self):
        """@ext-link-type is only spaces: should return CRITICAL"""
        self.base_article["ext-link-type"] = "   "
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_ext_link_type_presence()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "CRITICAL")

    def test_ext_link_type_presence_has_i18n(self):
        """Presence validation should include i18n fields"""
        del self.base_article["ext-link-type"]
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_ext_link_type_presence()
        self.assertIsNotNone(result["adv_text"])
        self.assertIsNotNone(result["adv_params"])


class TestRelatedArticleTypeValue(BaseRelatedArticleTest):
    """Tests for validate_related_article_type_value (ERROR)"""

    def setUp(self):
        super().setUp()
        self.base_article = {
            "parent": "article",
            "parent_article_type": "correction",
            "original_article_type": "correction",
            "parent_id": None,
            "parent_lang": "en",
            "ext-link-type": "doi",
            "href": "10.1590/example",
            "id": "ra1",
        }

    def test_corrected_article(self):
        """corrected-article is a valid value"""
        self.base_article["related-article-type"] = "corrected-article"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNone(result)

    def test_correction_forward(self):
        """correction-forward is a valid value"""
        self.base_article["related-article-type"] = "correction-forward"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNone(result)

    def test_retracted_article(self):
        """retracted-article is a valid value"""
        self.base_article["related-article-type"] = "retracted-article"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNone(result)

    def test_retraction_forward(self):
        """retraction-forward is a valid value"""
        self.base_article["related-article-type"] = "retraction-forward"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNone(result)

    def test_partial_retraction(self):
        """partial-retraction is a valid value"""
        self.base_article["related-article-type"] = "partial-retraction"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNone(result)

    def test_addended_article(self):
        """addended-article is a valid value"""
        self.base_article["related-article-type"] = "addended-article"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNone(result)

    def test_addendum(self):
        """addendum is a valid value"""
        self.base_article["related-article-type"] = "addendum"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNone(result)

    def test_expression_of_concern(self):
        """expression-of-concern is a valid value"""
        self.base_article["related-article-type"] = "expression-of-concern"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNone(result)

    def test_object_of_concern(self):
        """object-of-concern is a valid value"""
        self.base_article["related-article-type"] = "object-of-concern"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNone(result)

    def test_commentary_article(self):
        """commentary-article is a valid value"""
        self.base_article["related-article-type"] = "commentary-article"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNone(result)

    def test_commentary(self):
        """commentary is a valid value"""
        self.base_article["related-article-type"] = "commentary"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNone(result)

    def test_reply(self):
        """reply is a valid value"""
        self.base_article["related-article-type"] = "reply"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNone(result)

    def test_letter(self):
        """letter is a valid value"""
        self.base_article["related-article-type"] = "letter"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNone(result)

    def test_reviewed_article(self):
        """reviewed-article is a valid value"""
        self.base_article["related-article-type"] = "reviewed-article"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNone(result)

    def test_reviewer_report(self):
        """reviewer-report is a valid value"""
        self.base_article["related-article-type"] = "reviewer-report"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNone(result)

    def test_preprint(self):
        """preprint is a valid value"""
        self.base_article["related-article-type"] = "preprint"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNone(result)

    def test_invalid_value_related(self):
        """'related' is not a valid value: should return ERROR"""
        self.base_article["related-article-type"] = "related"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], "related")

    def test_invalid_value_errata(self):
        """'errata' is not a valid value: should return ERROR"""
        self.base_article["related-article-type"] = "errata"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "ERROR")

    def test_uppercase_value(self):
        """'Corrected-Article' (uppercase) is not valid: should return ERROR"""
        self.base_article["related-article-type"] = "Corrected-Article"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], "Corrected-Article")

    def test_missing_attribute_returns_none(self):
        """Missing attribute should return None (validated by presence check)"""
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNone(result)

    def test_empty_attribute_returns_none(self):
        """Empty attribute should return None (validated by presence check)"""
        self.base_article["related-article-type"] = ""
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNone(result)

    def test_value_validation_has_i18n(self):
        """Value validation should include i18n fields"""
        self.base_article["related-article-type"] = "invalid"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_related_article_type_value()
        self.assertIsNotNone(result["adv_text"])
        self.assertIsNotNone(result["adv_params"])


class TestExtLinkTypeValue(BaseRelatedArticleTest):
    """Tests for validate_ext_link_type_value (ERROR)"""

    def setUp(self):
        super().setUp()
        self.base_article = {
            "parent": "article",
            "parent_article_type": "correction",
            "original_article_type": "correction",
            "parent_id": None,
            "parent_lang": "en",
            "href": "10.1590/example",
            "id": "ra1",
            "related-article-type": "corrected-article",
        }

    def test_doi_valid(self):
        """'doi' is valid for @ext-link-type"""
        self.base_article["ext-link-type"] = "doi"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_ext_link_type_value()
        self.assertIsNone(result)

    def test_uri_valid(self):
        """'uri' is valid for @ext-link-type"""
        self.base_article["ext-link-type"] = "uri"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_ext_link_type_value()
        self.assertIsNone(result)

    def test_url_invalid(self):
        """'url' is not valid: should return ERROR"""
        self.base_article["ext-link-type"] = "url"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_ext_link_type_value()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], "url")

    def test_link_invalid(self):
        """'link' is not valid: should return ERROR"""
        self.base_article["ext-link-type"] = "link"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_ext_link_type_value()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "ERROR")

    def test_uppercase_doi(self):
        """'DOI' (uppercase) is not valid: should return ERROR"""
        self.base_article["ext-link-type"] = "DOI"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_ext_link_type_value()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "ERROR")

    def test_uppercase_uri(self):
        """'URI' (uppercase) is not valid: should return ERROR"""
        self.base_article["ext-link-type"] = "URI"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_ext_link_type_value()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "ERROR")

    def test_missing_returns_none(self):
        """Missing @ext-link-type should return None (validated by presence check)"""
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_ext_link_type_value()
        self.assertIsNone(result)

    def test_empty_returns_none(self):
        """Empty @ext-link-type should return None (validated by presence check)"""
        self.base_article["ext-link-type"] = ""
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_ext_link_type_value()
        self.assertIsNone(result)


class TestXlinkHrefPresence(BaseRelatedArticleTest):
    """Tests for validate_xlink_href_presence (ERROR)"""

    def setUp(self):
        super().setUp()
        self.base_article = {
            "parent": "article",
            "parent_article_type": "correction",
            "original_article_type": "correction",
            "parent_id": None,
            "parent_lang": "en",
            "ext-link-type": "doi",
            "id": "ra1",
            "related-article-type": "corrected-article",
        }

    def test_xlink_href_present_doi(self):
        """@xlink:href present with DOI: should return None (OK)"""
        self.base_article["href"] = "10.1590/example"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_xlink_href_presence()
        self.assertIsNone(result)

    def test_xlink_href_present_url(self):
        """@xlink:href present with URL: should return None (OK)"""
        self.base_article["href"] = "https://example.com/article"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_xlink_href_presence()
        self.assertIsNone(result)

    def test_xlink_href_present_doi_prefix(self):
        """@xlink:href present with doi.org prefix: should return None (OK)"""
        self.base_article["href"] = "https://doi.org/10.1590/example"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_xlink_href_presence()
        self.assertIsNone(result)

    def test_xlink_href_missing(self):
        """@xlink:href missing: should return ERROR"""
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_xlink_href_presence()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "ERROR")
        self.assertIn("@xlink:href", result["sub_item"])

    def test_xlink_href_empty(self):
        """@xlink:href empty: should return ERROR"""
        self.base_article["href"] = ""
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_xlink_href_presence()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "ERROR")

    def test_xlink_href_whitespace_only(self):
        """@xlink:href only spaces: should return ERROR"""
        self.base_article["href"] = "   "
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_xlink_href_presence()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "ERROR")

    def test_xlink_href_presence_has_i18n(self):
        """Presence validation should include i18n fields"""
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_xlink_href_presence()
        self.assertIsNotNone(result["adv_text"])
        self.assertIsNotNone(result["adv_params"])


class TestDoiPreference(BaseRelatedArticleTest):
    """Tests for validate_doi_preference (WARNING)"""

    def setUp(self):
        super().setUp()
        self.base_article = {
            "parent": "article",
            "parent_article_type": "correction",
            "original_article_type": "correction",
            "parent_id": None,
            "parent_lang": "en",
            "href": "10.1590/example",
            "id": "ra1",
        }

    def test_corrected_article_with_doi_ok(self):
        """corrected-article with doi: should return None (preferred)"""
        self.base_article["related-article-type"] = "corrected-article"
        self.base_article["ext-link-type"] = "doi"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_doi_preference()
        self.assertIsNone(result)

    def test_corrected_article_with_uri_warning(self):
        """corrected-article with uri: should return WARNING"""
        self.base_article["related-article-type"] = "corrected-article"
        self.base_article["ext-link-type"] = "uri"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_doi_preference()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "WARNING")

    def test_preprint_with_doi_ok(self):
        """preprint with doi: should return None (preferred)"""
        self.base_article["related-article-type"] = "preprint"
        self.base_article["ext-link-type"] = "doi"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_doi_preference()
        self.assertIsNone(result)

    def test_preprint_with_uri_ok(self):
        """preprint with uri: should return None (allowed exception)"""
        self.base_article["related-article-type"] = "preprint"
        self.base_article["ext-link-type"] = "uri"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_doi_preference()
        self.assertIsNone(result)

    def test_reviewer_report_with_doi_ok(self):
        """reviewer-report with doi: should return None (preferred)"""
        self.base_article["related-article-type"] = "reviewer-report"
        self.base_article["ext-link-type"] = "doi"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_doi_preference()
        self.assertIsNone(result)

    def test_reviewer_report_with_uri_ok(self):
        """reviewer-report with uri: should return None (allowed exception)"""
        self.base_article["related-article-type"] = "reviewer-report"
        self.base_article["ext-link-type"] = "uri"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_doi_preference()
        self.assertIsNone(result)

    def test_retracted_article_with_uri_warning(self):
        """retracted-article with uri: should return WARNING"""
        self.base_article["related-article-type"] = "retracted-article"
        self.base_article["ext-link-type"] = "uri"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_doi_preference()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "WARNING")

    def test_addendum_with_uri_warning(self):
        """addendum with uri: should return WARNING"""
        self.base_article["related-article-type"] = "addendum"
        self.base_article["ext-link-type"] = "uri"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_doi_preference()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "WARNING")

    def test_doi_preference_warning_has_i18n(self):
        """DOI preference warning should include i18n fields"""
        self.base_article["related-article-type"] = "corrected-article"
        self.base_article["ext-link-type"] = "uri"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_doi_preference()
        self.assertIsNotNone(result["adv_text"])
        self.assertIsNotNone(result["adv_params"])

    def test_commentary_with_uri_warning(self):
        """commentary with uri: should return WARNING"""
        self.base_article["related-article-type"] = "commentary"
        self.base_article["ext-link-type"] = "uri"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_doi_preference()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "WARNING")

    def test_letter_with_uri_warning(self):
        """letter with uri: should return WARNING"""
        self.base_article["related-article-type"] = "letter"
        self.base_article["ext-link-type"] = "uri"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_doi_preference()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "WARNING")


class TestIdPresenceNew(BaseRelatedArticleTest):
    """Additional tests for validate_id_presence"""

    def setUp(self):
        super().setUp()
        self.base_article = {
            "parent": "article",
            "parent_article_type": "correction",
            "original_article_type": "correction",
            "parent_id": None,
            "parent_lang": "en",
            "ext-link-type": "doi",
            "href": "10.1590/example",
            "related-article-type": "corrected-article",
        }

    def test_id_present(self):
        """@id is present: should return None"""
        self.base_article["id"] = "ra1"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_id_presence()
        self.assertIsNone(result)

    def test_id_missing(self):
        """@id is missing: should return CRITICAL"""
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_id_presence()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "CRITICAL")

    def test_id_empty(self):
        """@id is empty: should return CRITICAL"""
        self.base_article["id"] = ""
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_id_presence()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "CRITICAL")

    def test_id_whitespace_only(self):
        """@id only spaces: should return CRITICAL"""
        self.base_article["id"] = "   "
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_id_presence()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "CRITICAL")

    def test_id_special_chars(self):
        """@id with special characters: should return None"""
        self.base_article["id"] = "r-1_a"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_id_presence()
        self.assertIsNone(result)

    def test_id_presence_has_i18n(self):
        """ID presence validation should include i18n fields"""
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_id_presence()
        self.assertIsNotNone(result["adv_text"])
        self.assertIsNotNone(result["adv_params"])


class TestAttribOrderNew(BaseRelatedArticleTest):
    """Additional tests for validate_attrib_order"""

    def setUp(self):
        super().setUp()
        self.base_article = {
            "parent": "article",
            "parent_article_type": "correction",
            "original_article_type": "correction",
            "parent_id": None,
            "parent_lang": "en",
            "ext-link-type": "doi",
            "href": "10.1590/example",
            "id": "ra1",
            "related-article-type": "corrected-article",
        }

    def test_correct_order(self):
        """Correct order should return None"""
        expected_order = [
            "related-article-type",
            "id",
            "{http://www.w3.org/1999/xlink}href",
            "ext-link-type",
        ]
        self.base_article["attribs"] = expected_order
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_attrib_order()
        self.assertIsNone(result)

    def test_wrong_order(self):
        """Wrong order should return INFO"""
        self.base_article["attribs"] = [
            "id",
            "related-article-type",
            "{http://www.w3.org/1999/xlink}href",
            "ext-link-type",
        ]
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_attrib_order()
        self.assertIsNotNone(result)
        self.assertEqual(result["response"], "INFO")

    def test_no_attrib_order_config(self):
        """Missing attrib_order config should return None"""
        params = dict(self.params)
        del params["attrib_order"]
        self.base_article["attribs"] = ["id", "related-article-type"]
        validator = RelatedArticleValidation(self.base_article, params)
        result = validator.validate_attrib_order()
        self.assertIsNone(result)

    def test_no_attribs_in_data(self):
        """Missing attribs in data should return None"""
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_attrib_order()
        self.assertIsNone(result)

    def test_attrib_order_has_i18n(self):
        """Attrib order validation should include i18n fields"""
        self.base_article["attribs"] = [
            "id",
            "related-article-type",
        ]
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_attrib_order()
        self.assertIsNotNone(result["adv_text"])
        self.assertIsNotNone(result["adv_params"])


class TestFullValidationWithAllNewRules(BaseRelatedArticleTest):
    """Tests for validate() with all new validations combined"""

    def setUp(self):
        super().setUp()
        self.valid_article = {
            "parent": "article",
            "parent_article_type": "correction",
            "original_article_type": "correction",
            "parent_id": None,
            "parent_lang": "en",
            "ext-link-type": "doi",
            "href": "10.1590/example",
            "id": "ra1",
            "related-article-type": "corrected-article",
        }

    def test_all_valid_no_errors(self):
        """Complete valid related-article should produce no errors"""
        validator = RelatedArticleValidation(self.valid_article, self.params)
        results = validator.validate()
        error_results = [r for r in results if r["response"] not in ("OK",)]
        self.assertEqual(len(error_results), 0)

    def test_all_attributes_empty(self):
        """All attributes empty should produce multiple CRITICAL errors"""
        article = dict(self.valid_article)
        article["related-article-type"] = ""
        article["id"] = ""
        article["ext-link-type"] = ""
        article["href"] = ""
        validator = RelatedArticleValidation(article, self.params)
        results = validator.validate()
        critical_results = [r for r in results if r["response"] == "CRITICAL"]
        self.assertGreater(len(critical_results), 0)

    def test_missing_all_attributes(self):
        """Missing all key attributes should produce errors"""
        article = {
            "parent": "article",
            "parent_article_type": "correction",
            "original_article_type": "correction",
            "parent_id": None,
            "parent_lang": "en",
        }
        validator = RelatedArticleValidation(article, self.params)
        results = validator.validate()
        error_results = [r for r in results if r["response"] not in ("OK",)]
        self.assertGreater(len(error_results), 0)


class TestXMLIntegrationNewValidations(BaseRelatedArticleTest):
    """Integration tests using XML parsing with new validations"""

    def test_preprint_with_uri_valid(self):
        """Preprint with URI should not produce warnings"""
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en" id="a1">
            <front>
                <article-meta>
                    <related-article related-article-type="preprint" 
                                   id="r1" 
                                   xlink:href="https://preprints.scielo.org/index.php/scielo/preprint/view/11166" 
                                   ext-link-type="uri"/>
                </article-meta>
            </front>
        </article>"""
        xmltree = etree.fromstring(xml)
        validator = XMLRelatedArticlesValidation(xmltree, self.params)
        results = list(validator.validate())
        warnings = [r for r in results if r["response"] == "WARNING"]
        self.assertEqual(len(warnings), 0)

    def test_corrected_article_with_doi_valid(self):
        """Errata with DOI should pass validations"""
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="correction" xml:lang="en" id="a1">
            <front>
                <article-meta>
                    <related-article related-article-type="corrected-article" 
                                   id="r1" 
                                   xlink:href="10.1590/123436773822" 
                                   ext-link-type="doi"/>
                </article-meta>
            </front>
        </article>"""
        xmltree = etree.fromstring(xml)
        validator = XMLRelatedArticlesValidation(xmltree, self.params)
        results = list(validator.validate())
        errors = [r for r in results if r["response"] in ("CRITICAL", "ERROR")]
        self.assertEqual(len(errors), 0)

    def test_missing_related_article_type_xml(self):
        """Missing @related-article-type in XML should produce CRITICAL"""
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="correction" xml:lang="en" id="a1">
            <front>
                <article-meta>
                    <related-article id="r1" 
                                   xlink:href="10.1590/123456" 
                                   ext-link-type="doi"/>
                </article-meta>
            </front>
        </article>"""
        xmltree = etree.fromstring(xml)
        validator = XMLRelatedArticlesValidation(xmltree, self.params)
        results = list(validator.validate())
        critical = [r for r in results if r["response"] == "CRITICAL"
                    and r["title"] == "Related article type presence"]
        self.assertEqual(len(critical), 1)

    def test_missing_id_xml(self):
        """Missing @id in XML should produce CRITICAL"""
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="correction" xml:lang="en" id="a1">
            <front>
                <article-meta>
                    <related-article related-article-type="corrected-article" 
                                   xlink:href="10.1590/123456" 
                                   ext-link-type="doi"/>
                </article-meta>
            </front>
        </article>"""
        xmltree = etree.fromstring(xml)
        validator = XMLRelatedArticlesValidation(xmltree, self.params)
        results = list(validator.validate())
        critical = [r for r in results if r["response"] == "CRITICAL"
                    and r["title"] == "Related article id"]
        self.assertEqual(len(critical), 1)

    def test_missing_ext_link_type_xml(self):
        """Missing @ext-link-type in XML should produce CRITICAL"""
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="correction" xml:lang="en" id="a1">
            <front>
                <article-meta>
                    <related-article related-article-type="corrected-article" 
                                   id="r1" 
                                   xlink:href="10.1590/123456"/>
                </article-meta>
            </front>
        </article>"""
        xmltree = etree.fromstring(xml)
        validator = XMLRelatedArticlesValidation(xmltree, self.params)
        results = list(validator.validate())
        critical = [r for r in results if r["response"] == "CRITICAL"
                    and r["title"] == "Related article ext-link-type presence"]
        self.assertEqual(len(critical), 1)

    def test_missing_xlink_href_xml(self):
        """Missing @xlink:href in XML should produce ERROR"""
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="correction" xml:lang="en" id="a1">
            <front>
                <article-meta>
                    <related-article related-article-type="corrected-article" 
                                   id="r1" 
                                   ext-link-type="doi"/>
                </article-meta>
            </front>
        </article>"""
        xmltree = etree.fromstring(xml)
        validator = XMLRelatedArticlesValidation(xmltree, self.params)
        results = list(validator.validate())
        errors = [r for r in results if r["response"] == "ERROR"
                  and r["title"] == "Related article xlink:href presence"]
        self.assertEqual(len(errors), 1)

    def test_invalid_related_article_type_xml(self):
        """Invalid @related-article-type in XML should produce ERROR"""
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="correction" xml:lang="en" id="a1">
            <front>
                <article-meta>
                    <related-article related-article-type="related" 
                                   id="r1" 
                                   xlink:href="10.1590/123456" 
                                   ext-link-type="doi"/>
                </article-meta>
            </front>
        </article>"""
        xmltree = etree.fromstring(xml)
        validator = XMLRelatedArticlesValidation(xmltree, self.params)
        results = list(validator.validate())
        errors = [r for r in results if r["response"] == "ERROR"
                  and r["title"] == "Related article type value"]
        self.assertEqual(len(errors), 1)

    def test_invalid_ext_link_type_xml(self):
        """Invalid @ext-link-type in XML should produce ERROR"""
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="correction" xml:lang="en" id="a1">
            <front>
                <article-meta>
                    <related-article related-article-type="corrected-article" 
                                   id="r1" 
                                   xlink:href="10.1590/123456" 
                                   ext-link-type="url"/>
                </article-meta>
            </front>
        </article>"""
        xmltree = etree.fromstring(xml)
        validator = XMLRelatedArticlesValidation(xmltree, self.params)
        results = list(validator.validate())
        errors = [r for r in results if r["response"] == "ERROR"
                  and r["title"] == "Related article ext-link-type value"]
        self.assertEqual(len(errors), 1)

    def test_uri_when_doi_preferred_xml(self):
        """Using URI for corrected-article should produce WARNING"""
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="correction" xml:lang="en" id="a1">
            <front>
                <article-meta>
                    <related-article related-article-type="corrected-article" 
                                   id="r1" 
                                   xlink:href="https://doi.org/10.1590/123456" 
                                   ext-link-type="uri"/>
                </article-meta>
            </front>
        </article>"""
        xmltree = etree.fromstring(xml)
        validator = XMLRelatedArticlesValidation(xmltree, self.params)
        results = list(validator.validate())
        warnings = [r for r in results if r["response"] == "WARNING"
                    and r["title"] == "Related article doi preference"]
        self.assertEqual(len(warnings), 1)

    def test_multiple_related_articles_xml(self):
        """Multiple related-articles in XML"""
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en" id="a1">
            <front>
                <article-meta>
                    <related-article related-article-type="commentary" 
                                   id="r1" 
                                   xlink:href="10.1590/123456720182998e" 
                                   ext-link-type="doi"/>
                    <related-article related-article-type="preprint" 
                                   id="r2" 
                                   xlink:href="https://preprints.scielo.org/view/123" 
                                   ext-link-type="uri"/>
                </article-meta>
            </front>
        </article>"""
        xmltree = etree.fromstring(xml)
        validator = XMLRelatedArticlesValidation(xmltree, self.params)
        results = list(validator.validate())
        # No critical or error level issues expected
        critical_or_error = [r for r in results if r["response"] in ("CRITICAL", "ERROR")]
        self.assertEqual(len(critical_or_error), 0)

    def test_no_related_articles_ok(self):
        """Article without related-article is OK (zero or more)"""
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en" id="a1">
            <front>
                <article-meta></article-meta>
            </front>
        </article>"""
        xmltree = etree.fromstring(xml)
        validator = XMLRelatedArticlesValidation(xmltree, self.params)
        results = list(validator.validate())
        self.assertEqual(len(results), 0)

    def test_related_article_in_front_stub(self):
        """related-article in front-stub (sub-article) should be validated"""
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="correction" xml:lang="en" id="a1">
            <front>
                <article-meta>
                    <related-article related-article-type="corrected-article" 
                                   id="r1" 
                                   xlink:href="10.1590/dois" 
                                   ext-link-type="doi"/>
                </article-meta>
            </front>
            <sub-article article-type="translation" xml:lang="pt" id="s1">
                <front-stub>
                    <related-article related-article-type="corrected-article" 
                                   id="r2" 
                                   xlink:href="10.1590/dois" 
                                   ext-link-type="doi"/>
                </front-stub>
            </sub-article>
        </article>"""
        xmltree = etree.fromstring(xml)
        validator = XMLRelatedArticlesValidation(xmltree, self.params)
        results = list(validator.validate())
        critical_or_error = [r for r in results if r["response"] in ("CRITICAL", "ERROR")]
        self.assertEqual(len(critical_or_error), 0)

    def test_reviewer_report_with_uri_xml(self):
        """reviewer-report with URI should not produce doi preference warning"""
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en" id="a1">
            <front>
                <article-meta>
                    <related-article related-article-type="reviewer-report" 
                                   id="r1" 
                                   xlink:href="https://example.com/review/123" 
                                   ext-link-type="uri"/>
                </article-meta>
            </front>
        </article>"""
        xmltree = etree.fromstring(xml)
        validator = XMLRelatedArticlesValidation(xmltree, self.params)
        results = list(validator.validate())
        warnings = [r for r in results if r["response"] == "WARNING"]
        self.assertEqual(len(warnings), 0)

    def test_preprint_with_doi_valid_xml(self):
        """Preprint with DOI is valid (doi is always preferred)"""
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en" id="a1">
            <front>
                <article-meta>
                    <related-article related-article-type="preprint" 
                                   id="r1" 
                                   xlink:href="10.12345/preprint.123" 
                                   ext-link-type="doi"/>
                </article-meta>
            </front>
        </article>"""
        xmltree = etree.fromstring(xml)
        validator = XMLRelatedArticlesValidation(xmltree, self.params)
        results = list(validator.validate())
        warnings = [r for r in results if r["response"] == "WARNING"]
        self.assertEqual(len(warnings), 0)

    def test_retraction_with_uri_warning_xml(self):
        """Retraction with URI should produce WARNING"""
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="retraction" xml:lang="en" id="a1">
            <front>
                <article-meta>
                    <related-article related-article-type="retracted-article" 
                                   id="r1" 
                                   xlink:href="https://doi.org/10.1590/original-article" 
                                   ext-link-type="uri"/>
                </article-meta>
            </front>
        </article>"""
        xmltree = etree.fromstring(xml)
        validator = XMLRelatedArticlesValidation(xmltree, self.params)
        results = list(validator.validate())
        warnings = [r for r in results if r["response"] == "WARNING"
                    and r["title"] == "Related article doi preference"]
        self.assertEqual(len(warnings), 1)


if __name__ == "__main__":
    unittest.main()
