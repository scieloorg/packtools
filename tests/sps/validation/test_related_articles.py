from unittest import TestCase, skip
from unittest.mock import Mock, patch

from lxml import etree
from packtools.sps.models.related_articles import Fulltext
from packtools.sps.validation.related_articles import (
    RelatedArticlesValidation,
    RelatedArticleValidation,
    FulltextValidation,
)


class BaseRelatedArticleTest(TestCase):
    """Base test class with common setup"""

    def setUp(self):
        self.params = {
            "requirement_error_level": "CRICRI",
            "type_error_level": "CRICRI",
            "ext_link_type_error_level": "CRICRI",
            "uri_error_level": "CRICRI",
            "uri_format_error_level": "CRICRI",
            "doi_error_level": "CRICRI",
            "doi_format_error_level": "CRICRI",
            "id_error_level": "CRICRI",
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

    @patch("packtools.sps.validation.related_articles.FulltextValidation")
    @patch("packtools.sps.validation.related_articles.Fulltext")
    def test_initialization(self, mock_fulltext, mock_validation):
        """Test if classes are properly initialized"""
        # Arrange
        mock_fulltext_instance = Mock()
        mock_fulltext.return_value = mock_fulltext_instance

        mock_validation_instance = Mock()
        mock_validation.return_value = mock_validation_instance

        # Act
        validator = RelatedArticlesValidation(self.xmltree, self.params)

        # Assert
        mock_fulltext.assert_called_once_with(self.xmltree.find("."))
        mock_validation.assert_called_once_with(mock_fulltext_instance, self.params)
        self.assertEqual(validator.params, self.params)
        self.assertEqual(validator.error_level, "ERROR")

    @patch("packtools.sps.validation.related_articles.FulltextValidation")
    @patch("packtools.sps.validation.related_articles.Fulltext")
    def test_initialization_default_params(self, mock_fulltext, mock_validation):
        """Test initialization with default parameters"""
        # Act
        validator = RelatedArticlesValidation(self.xmltree)

        # Assert
        self.assertEqual(validator.params, {})
        self.assertEqual(validator.error_level, "ERROR")

    @patch("packtools.sps.validation.related_articles.FulltextValidation")
    @patch("packtools.sps.validation.related_articles.Fulltext")
    def test_validate_method_calls(self, mock_fulltext, mock_validation):
        """Test if validate method properly calls FulltextValidation.validate"""
        # Arrange
        mock_validation_instance = Mock()
        mock_validation.return_value = mock_validation_instance

        expected_results = [{"result": 1}, {"result": 2}]
        mock_validation_instance.validate.return_value = iter(expected_results)

        # Act
        validator = RelatedArticlesValidation(self.xmltree, self.params)
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
        validator = RelatedArticlesValidation(xmltree, self.params)
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
        validator = RelatedArticlesValidation(xmltree, self.params)
        results = list(validator.validate())

        # Assert
        self.assertTrue(len(results) > 0)
        ids = [r.get("data", {}).get("id") for r in results if "data" in r]
        self.assertTrue(len(set(ids)) > 1)  # Should have multiple unique IDs

    def test_error_level_inheritance(self):
        """Test if error_level is properly inherited from params"""
        # Test with custom error level
        params = self.params.copy()
        params["error_level"] = "CUSTOM_ERROR"
        validator = RelatedArticlesValidation(self.xmltree, params)
        self.assertEqual(validator.error_level, "CUSTOM_ERROR")

        # Test with default error level
        validator = RelatedArticlesValidation(self.xmltree, {})
        self.assertEqual(validator.error_level, "ERROR")

    def test_empty_document(self):
        """Test validation with empty document"""
        # Arrange
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="correction">
                <front></front>
            </article>"""
        xmltree = etree.fromstring(xml)

        # Act
        validator = RelatedArticlesValidation(xmltree, self.params)
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
                "related-article-type": "corrected-article",
            }
        )
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_type()

        self.assertEqual(result["response"], "CRICRI")
        self.assertEqual(result["got_value"], "corrected-article")
        self.assertEqual(result["expected_value"], ["retracted-article"])
        self.assertTrue(result["advice"].startswith("The article-type: retraction"))


class TestRelatedArticleLinkValidation(BaseRelatedArticleTest):
    def setUp(self):
        super().setUp()
        self.base_article = {
            "parent": "article",
            "parent_article_type": "correction",
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

        self.assertEqual(result["response"], "CRICRI")
        self.assertEqual(result["got_value"], "invalid-uri")
        self.assertEqual(
            result["expected_value"], "A valid URI format (e.g., http://example.com)"
        )
        self.assertTrue(result["advice"].startswith("Invalid URI format"))

    def test_validate_link_missing(self):
        del self.base_article["href"]
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_doi()

        self.assertEqual(result["response"], "CRICRI")
        self.assertIsNone(result["got_value"])
        self.assertEqual(result["expected_value"], "A valid DOI")
        self.assertTrue(result["advice"].startswith("Provide a valid DOI"))


class TestRelatedArticleExtLinkTypeValidation(BaseRelatedArticleTest):
    def setUp(self):
        super().setUp()
        self.base_article = {
            "parent": "article",
            "parent_article_type": "correction",
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
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_ext_link_type()

        self.assertEqual(result["response"], "CRICRI")
        self.assertEqual(result["got_value"], "url")
        self.assertEqual(result["expected_value"], ["doi", "uri"])
        self.assertTrue(result["advice"].startswith("The ext-link-type"))


class TestRelatedArticleFullValidation(BaseRelatedArticleTest):
    def setUp(self):
        super().setUp()
        self.base_article = {
            "parent": "article",
            "parent_article_type": "correction",
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

        self.assertEqual(len(results), 0)

    def test_validate_all_pass_uri(self):
        self.base_article.update(
            {"ext-link-type": "uri", "href": "http://example.com/article"}
        )
        validator = RelatedArticleValidation(self.base_article, self.params)
        results = validator.validate()

        self.assertEqual(len(results), 0)

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

        error_count = sum(1 for r in results if r["response"] == "CRICRI")
        self.assertGreater(error_count, 0)


class TestRelatedArticleValidation(BaseRelatedArticleTest):
    def setUp(self):
        super().setUp()
        self.base_article = {
            "parent": "article",
            "parent_article_type": "correction",
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
        self.assertEqual(result["response"], "CRICRI")

    def test_validate_uri_format(self):
        self.base_article.update({"ext-link-type": "uri", "href": "invalid-uri"})
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_uri()
        self.assertEqual(result["response"], "CRICRI")

    def test_validate_doi_existence(self):
        del self.base_article["href"]
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_doi()
        self.assertEqual(result["response"], "CRICRI")

    def test_validate_doi_format(self):
        self.base_article["href"] = "invalid-doi"
        validator = RelatedArticleValidation(self.base_article, self.params)
        result = validator.validate_doi()
        self.assertEqual(result["response"], "CRICRI")


class BaseFulltextValidationTest(TestCase):
    """Base test class with common setup for validation tests"""

    def setUp(self):
        self.params = {
            "ext_link_type_list": ["doi", "uri"],
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
                    ],
                },
            },
        }


class TestMissingRequiredArticle(BaseFulltextValidationTest):
    """Test case for missing required related article"""

    def setUp(self):
        super().setUp()
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink"  article-type="correction" xml:lang="en" id="a1">
            <front><article-meta></article-meta></front>
        </article>"""

        self.fulltext = Fulltext(etree.fromstring(xml).find("."))
        self.validator = FulltextValidation(self.fulltext, self.params)

    def test_missing_required(self):
        results = list(self.validator.validate())
        self.assertEqual(len(results), 1)

        result = results[0]
        self.assertEqual(result["response"], "CRITICAL")
        self.assertEqual(result["validation_type"], "match")
        self.assertEqual(result["title"], "Required related articles")
        self.assertIn("corrected-article", result["expected_value"])
        self.assertEqual(result["got_value"], [])


class TestOptionalArticle(BaseFulltextValidationTest):
    """Test case for article with optional related articles"""

    def setUp(self):
        super().setUp()
        xml = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink"  article-type="research-article" xml:lang="en" id="a1">
            <front><article-meta></article-meta></front>
        </article>"""

        self.fulltext = Fulltext(etree.fromstring(xml))
        self.validator = FulltextValidation(self.fulltext, self.params)

    def test_optional_missing(self):
        results = list(self.validator.validate())
        self.assertEqual(len(results), 0)


class TestNestedValidation(BaseFulltextValidationTest):
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

        self.fulltext = Fulltext(etree.fromstring(xml))
        self.validator = FulltextValidation(self.fulltext, self.params)

    def test_nested_validation(self):
        results = list(self.validator.validate())

        # Find errors in translation sub-article
        translation_errors = [
            r
            for r in results
            if r["parent_article_type"] == "translation" and r["response"] == "CRITICAL"
        ]

        self.assertEqual(len(translation_errors), 1)
        error = translation_errors[0]
        self.assertEqual(error["validation_type"], "match")
        self.assertIn("correction-forward", error["expected_value"])


class TestValidStructure(BaseFulltextValidationTest):
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

        self.fulltext = Fulltext(etree.fromstring(xml).find("."))
        self.validator = FulltextValidation(self.fulltext, self.params)

    def test_valid_structure(self):
        results = list(self.validator.validate())
        print(results)
        errors = [r for r in results if r["response"] != "OK"]
        self.assertEqual(len(errors), 0)


class TestMultipleSubArticles(BaseFulltextValidationTest):
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
                                   ext-link-type="doi" 
                                   xlink:href="10.1590/xxxx"
                                   id="ra2">Spanish translation</related-article>
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

        self.fulltext = Fulltext(etree.fromstring(xml))
        self.validator = FulltextValidation(self.fulltext, self.params)

    def test_multiple_sub_articles(self):
        results = list(self.validator.validate())

        # First sub-article should be valid
        spanish_errors = [
            r for r in results if r["parent_id"] == "s1" and r["response"] != "OK"
        ]
        self.assertEqual(len(spanish_errors), 0)

        # Second sub-article should have error
        portuguese_errors = [
            r for r in results if r["parent_id"] == "s2" and r["response"] == "CRITICAL"
        ]
        self.assertEqual(len(portuguese_errors), 1)


class TestOriginalArticleType(BaseFulltextValidationTest):
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

        self.fulltext = Fulltext(etree.fromstring(xml))
        self.validator = FulltextValidation(self.fulltext, self.params)

    def test_original_article_type_inheritance(self):
        results = list(self.validator.validate())

        translation_data = [r for r in results if r["parent_id"] == "s1"][0]

        self.assertEqual(
            translation_data["data"].get("original_article_type"), "research-article"
        )


if __name__ == "__main__":
    unittest.main()
