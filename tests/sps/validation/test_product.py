"""
Unit tests for <product> validation according to SPS 1.10.

Tests cover:
- @product-type attribute presence and value
- <source> element presence
- Consistency with @article-type="book-review"
- Recommended elements (author, publisher-name, year)
- Multiple products
- Edge cases
"""
import unittest
from lxml import etree

from packtools.sps.validation.product import ProductValidation, ArticleProductValidation


def filter_results(results):
    """Filter out None values from validator results."""
    return [r for r in results if r is not None]


class TestProductTypePresence(unittest.TestCase):
    """Tests for @product-type attribute presence (CRITICAL)."""

    def _get_validator(self, xml_content, rules=None):
        xmltree = etree.fromstring(xml_content)
        rules = rules or {"product_type_presence_error_level": "CRITICAL"}
        validator = ArticleProductValidation(xmltree, rules)
        products = list(validator.products_model.products)
        if products:
            return ProductValidation(products[0], rules)
        return None

    def test_product_type_book_ok(self):
        """<product> with @product-type="book" should be OK."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_product_type_presence()
        self.assertEqual(result["response"], "OK")

    def test_product_type_missing_critical(self):
        """<product> without @product-type should be CRITICAL."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product>
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_product_type_presence()
        self.assertEqual(result["response"], "CRITICAL")
        self.assertIsNotNone(result["advice"])
        self.assertIsNotNone(result["adv_text"])

    def test_product_type_empty_critical(self):
        """<product> with empty @product-type should be CRITICAL."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="">
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_product_type_presence()
        self.assertEqual(result["response"], "CRITICAL")

    def test_product_type_spaces_only_critical(self):
        """<product> with @product-type containing only spaces should be CRITICAL."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="   ">
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_product_type_presence()
        self.assertEqual(result["response"], "CRITICAL")


class TestProductTypeValue(unittest.TestCase):
    """Tests for @product-type value validation (ERROR)."""

    def _get_validator(self, xml_content, rules=None):
        xmltree = etree.fromstring(xml_content)
        rules = rules or {
            "product_type_value_error_level": "ERROR",
            "product_type_list": ["book"],
        }
        validator = ArticleProductValidation(xmltree, rules)
        products = list(validator.products_model.products)
        if products:
            return ProductValidation(products[0], rules)
        return None

    def test_product_type_book_ok(self):
        """@product-type="book" should be OK."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_product_type_value()
        self.assertEqual(result["response"], "OK")

    def test_product_type_other_error(self):
        """@product-type="other" should be ERROR."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="other">
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_product_type_value()
        self.assertEqual(result["response"], "ERROR")
        self.assertIn("other", result["advice"])

    def test_product_type_journal_error(self):
        """@product-type="journal" should be ERROR."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="journal">
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_product_type_value()
        self.assertEqual(result["response"], "ERROR")

    def test_product_type_uppercase_book_error(self):
        """@product-type="Book" (uppercase) should be ERROR."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="Book">
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_product_type_value()
        self.assertEqual(result["response"], "ERROR")

    def test_product_type_all_uppercase_book_error(self):
        """@product-type="BOOK" (all uppercase) should be ERROR."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="BOOK">
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_product_type_value()
        self.assertEqual(result["response"], "ERROR")

    def test_product_type_absent_returns_none(self):
        """Missing @product-type should return None (handled by presence check)."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product>
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_product_type_value()
        self.assertIsNone(result)

    def test_product_type_empty_returns_none(self):
        """Empty @product-type should return None (handled by presence check)."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="">
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_product_type_value()
        self.assertIsNone(result)


class TestSourcePresence(unittest.TestCase):
    """Tests for <source> element presence (CRITICAL)."""

    def _get_validator(self, xml_content, rules=None):
        xmltree = etree.fromstring(xml_content)
        rules = rules or {"source_presence_error_level": "CRITICAL"}
        validator = ArticleProductValidation(xmltree, rules)
        products = list(validator.products_model.products)
        if products:
            return ProductValidation(products[0], rules)
        return None

    def test_source_present_ok(self):
        """<product> with <source> should be OK."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_source_presence()
        self.assertEqual(result["response"], "OK")

    def test_source_with_special_characters_ok(self):
        """<source> with special characters should be OK."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>La comunidad filosófica: manifiesto por una universidad popular</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_source_presence()
        self.assertEqual(result["response"], "OK")

    def test_source_missing_critical(self):
        """<product> without <source> should be CRITICAL."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <publisher-name>Oxford University Press</publisher-name>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_source_presence()
        self.assertEqual(result["response"], "CRITICAL")

    def test_source_empty_critical(self):
        """<source> with empty content should be CRITICAL."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source></source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_source_presence()
        self.assertEqual(result["response"], "CRITICAL")

    def test_source_spaces_only_critical(self):
        """<source> with only spaces should be CRITICAL."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>   </source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_source_presence()
        self.assertEqual(result["response"], "CRITICAL")

    def test_product_empty_critical(self):
        """Empty <product> should have CRITICAL for missing source."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_source_presence()
        self.assertEqual(result["response"], "CRITICAL")


class TestArticleTypeConsistency(unittest.TestCase):
    """Tests for article-type consistency (ERROR)."""

    def _get_validator(self, xml_content, rules=None):
        xmltree = etree.fromstring(xml_content)
        rules = rules or {"article_type_consistency_error_level": "ERROR"}
        validator = ArticleProductValidation(xmltree, rules)
        products = list(validator.products_model.products)
        if products:
            return ProductValidation(products[0], rules)
        return None

    def test_book_review_article_type_ok(self):
        """<product> with article-type="book-review" should be OK."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_article_type_consistency()
        self.assertEqual(result["response"], "OK")

    def test_research_article_type_error(self):
        """<product> with article-type="research-article" should be ERROR."""
        xml = """
        <article article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_article_type_consistency()
        self.assertEqual(result["response"], "ERROR")
        self.assertIn("research-article", result["advice"])

    def test_review_article_type_error(self):
        """<product> with article-type="review-article" should be ERROR."""
        xml = """
        <article article-type="review-article" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_article_type_consistency()
        self.assertEqual(result["response"], "ERROR")

    def test_no_article_type_error(self):
        """<product> without article-type in <article> should be ERROR."""
        xml = """
        <article xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_article_type_consistency()
        self.assertEqual(result["response"], "ERROR")


class TestAuthorPresence(unittest.TestCase):
    """Tests for author person-group presence (WARNING)."""

    def _get_validator(self, xml_content, rules=None):
        xmltree = etree.fromstring(xml_content)
        rules = rules or {"author_presence_error_level": "WARNING"}
        validator = ArticleProductValidation(xmltree, rules)
        products = list(validator.products_model.products)
        if products:
            return ProductValidation(products[0], rules)
        return None

    def test_author_present_ok(self):
        """<product> with author person-group should be OK."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <person-group person-group-type="author">
                            <name>
                                <surname>Smith</surname>
                                <given-names>John</given-names>
                            </name>
                        </person-group>
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_author_presence()
        self.assertEqual(result["response"], "OK")

    def test_author_missing_warning(self):
        """<product> without author person-group should be WARNING."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book Title</source>
                        <publisher-name>Publisher</publisher-name>
                        <year>2020</year>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_author_presence()
        self.assertEqual(result["response"], "WARNING")

    def test_multiple_authors_ok(self):
        """<product> with multiple authors should be OK."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <person-group person-group-type="author">
                            <name>
                                <surname>Silva</surname>
                                <given-names>João</given-names>
                            </name>
                            <name>
                                <surname>Santos</surname>
                                <given-names>Maria</given-names>
                            </name>
                        </person-group>
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_author_presence()
        self.assertEqual(result["response"], "OK")

    def test_editor_only_warning(self):
        """<product> with only editor person-group (no author) should be WARNING."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <person-group person-group-type="editor">
                            <name>
                                <surname>Oliveira</surname>
                                <given-names>Carlos</given-names>
                            </name>
                        </person-group>
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_author_presence()
        self.assertEqual(result["response"], "WARNING")

    def test_translator_only_warning(self):
        """<product> with only translator person-group (no author) should be WARNING."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <person-group person-group-type="translator">
                            <name>
                                <surname>Castro</surname>
                                <given-names>Antonia</given-names>
                            </name>
                        </person-group>
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_author_presence()
        self.assertEqual(result["response"], "WARNING")


class TestPublisherNamePresence(unittest.TestCase):
    """Tests for <publisher-name> presence (WARNING)."""

    def _get_validator(self, xml_content, rules=None):
        xmltree = etree.fromstring(xml_content)
        rules = rules or {"publisher_name_presence_error_level": "WARNING"}
        validator = ArticleProductValidation(xmltree, rules)
        products = list(validator.products_model.products)
        if products:
            return ProductValidation(products[0], rules)
        return None

    def test_publisher_name_present_ok(self):
        """<product> with <publisher-name> should be OK."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book Title</source>
                        <publisher-name>Oxford University Press</publisher-name>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_publisher_name_presence()
        self.assertEqual(result["response"], "OK")

    def test_publisher_name_missing_warning(self):
        """<product> without <publisher-name> should be WARNING."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <person-group person-group-type="author">
                            <name>
                                <surname>Smith</surname>
                                <given-names>John</given-names>
                            </name>
                        </person-group>
                        <source>Book Title</source>
                        <year>2020</year>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_publisher_name_presence()
        self.assertEqual(result["response"], "WARNING")


class TestYearPresence(unittest.TestCase):
    """Tests for <year> presence (WARNING)."""

    def _get_validator(self, xml_content, rules=None):
        xmltree = etree.fromstring(xml_content)
        rules = rules or {"year_presence_error_level": "WARNING"}
        validator = ArticleProductValidation(xmltree, rules)
        products = list(validator.products_model.products)
        if products:
            return ProductValidation(products[0], rules)
        return None

    def test_year_present_ok(self):
        """<product> with <year> should be OK."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book Title</source>
                        <year>2020</year>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_year_presence()
        self.assertEqual(result["response"], "OK")

    def test_year_missing_warning(self):
        """<product> without <year> should be WARNING."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <person-group person-group-type="author">
                            <name>
                                <surname>Smith</surname>
                                <given-names>John</given-names>
                            </name>
                        </person-group>
                        <source>Book Title</source>
                        <publisher-name>Publisher</publisher-name>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_year_presence()
        self.assertEqual(result["response"], "WARNING")


class TestProductValidateAll(unittest.TestCase):
    """Tests for the validate() method that runs all validations."""

    def _get_results(self, xml_content, rules=None):
        xmltree = etree.fromstring(xml_content)
        rules = rules or {
            "product_type_presence_error_level": "CRITICAL",
            "product_type_value_error_level": "ERROR",
            "source_presence_error_level": "CRITICAL",
            "article_type_consistency_error_level": "ERROR",
            "author_presence_error_level": "WARNING",
            "publisher_name_presence_error_level": "WARNING",
            "year_presence_error_level": "WARNING",
            "product_type_list": ["book"],
        }
        validator = ArticleProductValidation(xmltree, rules)
        return filter_results(validator.validate())

    def test_complete_product_all_ok(self):
        """Complete product with all elements should have all OK."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <person-group person-group-type="author">
                            <name>
                                <surname>ONFRAY</surname>
                                <given-names>Michel</given-names>
                            </name>
                        </person-group>
                        <source>La comunidad filosófica</source>
                        <publisher-name>Gedisa</publisher-name>
                        <publisher-loc>Barcelona</publisher-loc>
                        <year>2008</year>
                        <size units="pages">155</size>
                        <isbn>978-84-9784-252-5</isbn>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        results = self._get_results(xml)
        for result in results:
            self.assertEqual(result["response"], "OK", f"Failed for: {result['title']}")

    def test_minimal_product_with_warnings(self):
        """Minimal product (only source) should have warnings for missing recommended."""
        xml = """
        <article article-type="book-review" xml:lang="es">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Historia de la Filosofía Moderna</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        results = self._get_results(xml)
        responses = {r["title"]: r["response"] for r in results}

        self.assertEqual(responses["@product-type attribute"], "OK")
        self.assertEqual(responses["@product-type value"], "OK")
        self.assertEqual(responses["source element"], "OK")
        self.assertEqual(responses["article-type consistency"], "OK")
        self.assertEqual(responses["author in product"], "WARNING")
        self.assertEqual(responses["publisher-name in product"], "WARNING")
        self.assertEqual(responses["year in product"], "WARNING")

    def test_no_product_no_results(self):
        """Article without <product> should yield no results."""
        xml = """
        <article article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Research Paper</article-title>
                    </title-group>
                </article-meta>
            </front>
        </article>
        """
        results = self._get_results(xml)
        self.assertEqual(len(results), 0)

    def test_product_without_product_type_has_critical(self):
        """Product without @product-type should have CRITICAL."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product>
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        results = self._get_results(xml)
        type_results = [r for r in results if r["title"] == "@product-type attribute"]
        self.assertEqual(len(type_results), 1)
        self.assertEqual(type_results[0]["response"], "CRITICAL")

    def test_wrong_article_type_has_error(self):
        """Product with wrong article-type should have ERROR."""
        xml = """
        <article article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        results = self._get_results(xml)
        consistency_results = [r for r in results if r["title"] == "article-type consistency"]
        self.assertEqual(len(consistency_results), 1)
        self.assertEqual(consistency_results[0]["response"], "ERROR")


class TestMultipleProducts(unittest.TestCase):
    """Tests for articles with multiple <product> elements."""

    def _get_results(self, xml_content, rules=None):
        xmltree = etree.fromstring(xml_content)
        rules = rules or {
            "product_type_presence_error_level": "CRITICAL",
            "product_type_value_error_level": "ERROR",
            "source_presence_error_level": "CRITICAL",
            "article_type_consistency_error_level": "ERROR",
            "author_presence_error_level": "WARNING",
            "publisher_name_presence_error_level": "WARNING",
            "year_presence_error_level": "WARNING",
            "product_type_list": ["book"],
        }
        validator = ArticleProductValidation(xmltree, rules)
        return filter_results(validator.validate())

    def test_two_products_ok(self):
        """Article with two valid products should yield results for both."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <person-group person-group-type="author">
                            <name>
                                <surname>Smith</surname>
                                <given-names>John</given-names>
                            </name>
                        </person-group>
                        <source>Introduction to Philosophy</source>
                        <publisher-name>Oxford University Press</publisher-name>
                        <year>2019</year>
                    </product>
                    <product product-type="book">
                        <person-group person-group-type="author">
                            <name>
                                <surname>Jones</surname>
                                <given-names>Mary</given-names>
                            </name>
                        </person-group>
                        <source>Advanced Philosophy</source>
                        <publisher-name>Cambridge University Press</publisher-name>
                        <year>2020</year>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        results = self._get_results(xml)
        # Each product yields 7 validations, all OK
        self.assertEqual(len(results), 14)
        for result in results:
            self.assertEqual(result["response"], "OK", f"Failed for: {result['title']}")

    def test_three_products_ok(self):
        """Article with three products should yield results for all three."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book One</source>
                    </product>
                    <product product-type="book">
                        <source>Book Two</source>
                    </product>
                    <product product-type="book">
                        <source>Book Three</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        results = self._get_results(xml)
        # 7 validations per product × 3 products = 21
        self.assertEqual(len(results), 21)


class TestPersonGroupTypes(unittest.TestCase):
    """Tests for person-group types within <product>."""

    def _get_validator(self, xml_content, rules=None):
        xmltree = etree.fromstring(xml_content)
        rules = rules or {"author_presence_error_level": "WARNING"}
        validator = ArticleProductValidation(xmltree, rules)
        products = list(validator.products_model.products)
        if products:
            return ProductValidation(products[0], rules)
        return None

    def test_author_person_group_ok(self):
        """<person-group person-group-type="author"> should satisfy author check."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <person-group person-group-type="author">
                            <name>
                                <surname>Smith</surname>
                                <given-names>John</given-names>
                            </name>
                        </person-group>
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_author_presence()
        self.assertEqual(result["response"], "OK")

    def test_editor_person_group_not_author(self):
        """<person-group person-group-type="editor"> should not satisfy author check."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <person-group person-group-type="editor">
                            <name>
                                <surname>Oliveira</surname>
                                <given-names>Carlos</given-names>
                            </name>
                        </person-group>
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_author_presence()
        self.assertEqual(result["response"], "WARNING")

    def test_author_and_translator_ok(self):
        """Author and translator person-groups together should be OK."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <person-group person-group-type="author">
                            <name>
                                <surname>ONFRAY</surname>
                                <given-names>Michel</given-names>
                            </name>
                        </person-group>
                        <person-group person-group-type="translator">
                            <name>
                                <surname>Castro</surname>
                                <given-names>Antonia</given-names>
                            </name>
                        </person-group>
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        validator = self._get_validator(xml)
        result = validator.validate_author_presence()
        self.assertEqual(result["response"], "OK")


class TestOptionalElements(unittest.TestCase):
    """Tests for optional elements in <product>."""

    def _get_model_products(self, xml_content):
        xmltree = etree.fromstring(xml_content)
        model = ArticleProductValidation(xmltree, {})
        return list(model.products_model.products)

    def test_product_with_isbn(self):
        """Product with ISBN should be extracted."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book Title</source>
                        <isbn>978-84-9784-252-5</isbn>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        products = self._get_model_products(xml)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["isbn"], "978-84-9784-252-5")

    def test_product_with_publisher_loc(self):
        """Product with publisher-loc should be extracted."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book Title</source>
                        <publisher-loc>Barcelona</publisher-loc>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        products = self._get_model_products(xml)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["publisher_loc"], "Barcelona")

    def test_product_with_size(self):
        """Product with size should be extracted."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book Title</source>
                        <size units="pages">155</size>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        products = self._get_model_products(xml)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["size"], "155")

    def test_product_without_optional_elements(self):
        """Product without optional elements should have None values."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        products = self._get_model_products(xml)
        self.assertEqual(len(products), 1)
        self.assertIsNone(products[0]["isbn"])
        self.assertIsNone(products[0]["publisher_loc"])
        self.assertIsNone(products[0]["size"])


class TestArticleProductModel(unittest.TestCase):
    """Tests for the ArticleProducts model."""

    def test_no_products(self):
        """Article without <product> should yield no products."""
        xml = """
        <article article-type="research-article" xml:lang="en">
            <front>
                <article-meta>
                    <title-group>
                        <article-title>Title</article-title>
                    </title-group>
                </article-meta>
            </front>
        </article>
        """
        from packtools.sps.models.product import ArticleProducts
        xmltree = etree.fromstring(xml)
        model = ArticleProducts(xmltree)
        products = list(model.products)
        self.assertEqual(len(products), 0)

    def test_one_product(self):
        """Article with one <product> should yield one product."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        from packtools.sps.models.product import ArticleProducts
        xmltree = etree.fromstring(xml)
        model = ArticleProducts(xmltree)
        products = list(model.products)
        self.assertEqual(len(products), 1)
        self.assertEqual(products[0]["product_type"], "book")
        self.assertEqual(products[0]["source"], "Book Title")
        self.assertEqual(products[0]["parent"], "article")
        self.assertEqual(products[0]["parent_article_type"], "book-review")
        self.assertEqual(products[0]["parent_lang"], "en")

    def test_product_person_groups(self):
        """Product with multiple person-groups should report all types."""
        xml = """
        <article article-type="book-review" xml:lang="pt">
            <front>
                <article-meta>
                    <product product-type="book">
                        <person-group person-group-type="author">
                            <name>
                                <surname>Author</surname>
                                <given-names>First</given-names>
                            </name>
                        </person-group>
                        <person-group person-group-type="translator">
                            <name>
                                <surname>Translator</surname>
                                <given-names>First</given-names>
                            </name>
                        </person-group>
                        <source>Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        from packtools.sps.models.product import ArticleProducts
        xmltree = etree.fromstring(xml)
        model = ArticleProducts(xmltree)
        products = list(model.products)
        self.assertEqual(len(products), 1)
        self.assertIn("author", products[0]["person_groups"])
        self.assertIn("translator", products[0]["person_groups"])
        self.assertTrue(products[0]["has_author"])


class TestResponseStructure(unittest.TestCase):
    """Tests for the validation response structure (i18n fields)."""

    def test_response_has_i18n_fields(self):
        """All responses should have msg_text, msg_params, adv_text, adv_params."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        xmltree = etree.fromstring(xml)
        rules = {
            "product_type_presence_error_level": "CRITICAL",
            "product_type_value_error_level": "ERROR",
            "source_presence_error_level": "CRITICAL",
            "article_type_consistency_error_level": "ERROR",
            "author_presence_error_level": "WARNING",
            "publisher_name_presence_error_level": "WARNING",
            "year_presence_error_level": "WARNING",
            "product_type_list": ["book"],
        }
        validator = ArticleProductValidation(xmltree, rules)
        results = filter_results(validator.validate())

        expected_keys = {
            "title", "parent", "parent_id", "parent_article_type",
            "parent_lang", "item", "sub_item", "validation_type",
            "response", "expected_value", "got_value", "message",
            "msg_text", "msg_params", "advice", "adv_text",
            "adv_params", "data",
        }

        for result in results:
            self.assertTrue(
                expected_keys.issubset(result.keys()),
                f"Missing keys in response for '{result.get('title', 'unknown')}': "
                f"{expected_keys - result.keys()}"
            )
            self.assertIn("msg_text", result)
            self.assertIn("msg_params", result)

    def test_error_response_has_advice(self):
        """Error responses should have non-None advice and adv_text."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product>
                        <source>Book Title</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        xmltree = etree.fromstring(xml)
        rules = {
            "product_type_presence_error_level": "CRITICAL",
            "product_type_value_error_level": "ERROR",
            "source_presence_error_level": "CRITICAL",
            "article_type_consistency_error_level": "ERROR",
            "author_presence_error_level": "WARNING",
            "publisher_name_presence_error_level": "WARNING",
            "year_presence_error_level": "WARNING",
            "product_type_list": ["book"],
        }
        validator = ArticleProductValidation(xmltree, rules)
        results = filter_results(validator.validate())

        error_results = [r for r in results if r["response"] != "OK"]
        self.assertTrue(len(error_results) > 0)
        for result in error_results:
            self.assertIsNotNone(result["advice"], f"No advice for {result['title']}")
            self.assertIsNotNone(result["adv_text"], f"No adv_text for {result['title']}")


class TestEdgeCases(unittest.TestCase):
    """Tests for edge cases."""

    def _get_results(self, xml_content, rules=None):
        xmltree = etree.fromstring(xml_content)
        rules = rules or {
            "product_type_presence_error_level": "CRITICAL",
            "product_type_value_error_level": "ERROR",
            "source_presence_error_level": "CRITICAL",
            "article_type_consistency_error_level": "ERROR",
            "author_presence_error_level": "WARNING",
            "publisher_name_presence_error_level": "WARNING",
            "year_presence_error_level": "WARNING",
            "product_type_list": ["book"],
        }
        validator = ArticleProductValidation(xmltree, rules)
        return filter_results(validator.validate())

    def test_source_with_subtitle_ok(self):
        """Source with colon/subtitle should be OK."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Main Title: A Subtitle</source>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        results = self._get_results(xml)
        source_results = [r for r in results if r["title"] == "source element"]
        self.assertEqual(source_results[0]["response"], "OK")

    def test_year_with_four_digits_ok(self):
        """Year with 4 digits should be OK."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book Title</source>
                        <year>2020</year>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        results = self._get_results(xml)
        year_results = [r for r in results if r["title"] == "year in product"]
        self.assertEqual(year_results[0]["response"], "OK")

    def test_isbn_format_not_validated(self):
        """ISBN format should not be validated (out of scope)."""
        xml = """
        <article article-type="book-review" xml:lang="en">
            <front>
                <article-meta>
                    <product product-type="book">
                        <source>Book Title</source>
                        <isbn>invalid-isbn</isbn>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        # Should not fail - ISBN format validation is out of scope
        results = self._get_results(xml)
        # No ISBN validation result should exist
        isbn_results = [r for r in results if "isbn" in r.get("title", "").lower()]
        self.assertEqual(len(isbn_results), 0)

    def test_product_with_editor_as_organizer(self):
        """Product with editor person-group (organizer) should be valid."""
        xml = """
        <article article-type="book-review" xml:lang="pt">
            <front>
                <article-meta>
                    <product product-type="book">
                        <person-group person-group-type="editor">
                            <name>
                                <surname>Oliveira</surname>
                                <given-names>Carlos</given-names>
                            </name>
                        </person-group>
                        <source>Coletânea de Artigos sobre Educação</source>
                        <publisher-loc>Rio de Janeiro</publisher-loc>
                        <publisher-name>Fundação Getúlio Vargas</publisher-name>
                        <year>2021</year>
                    </product>
                </article-meta>
            </front>
        </article>
        """
        results = self._get_results(xml)
        responses = {r["title"]: r["response"] for r in results}
        # Editor is not "author", so author validation should warn
        self.assertEqual(responses["author in product"], "WARNING")
        # All others should be OK
        self.assertEqual(responses["@product-type attribute"], "OK")
        self.assertEqual(responses["@product-type value"], "OK")
        self.assertEqual(responses["source element"], "OK")
        self.assertEqual(responses["publisher-name in product"], "OK")
        self.assertEqual(responses["year in product"], "OK")


if __name__ == "__main__":
    unittest.main()
