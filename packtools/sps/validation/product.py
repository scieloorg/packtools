"""
Validation for <product> elements according to SPS 1.10 specification.

Implements validations for book review product elements to ensure:
- Mandatory attribute @product-type is present with value "book"
- Mandatory element <source> (book title) is present
- Consistency with @article-type="book-review"
- Recommended elements (author, publisher, year) are present

Reference: https://docs.google.com/document/d/1GTv4Inc2LS_AXY-ToHT3HmO66UT0VAHWJNOIqzBNSgA/edit?tab=t.0#heading=h.product
"""
import gettext

from packtools.sps.models.product import ArticleProducts
from packtools.sps.validation.utils import build_response

_ = gettext.gettext


class ProductValidation:
    """
    Validates a single <product> element.

    Parameters
    ----------
    data : dict
        Product data dictionary from ArticleProducts.products
    rules : dict
        Validation rules with error levels
    """

    def __init__(self, data, rules):
        self.data = data
        self.rules = rules

    @property
    def parent(self):
        """Returns parent context dict for build_response."""
        return {
            "parent": self.data.get("parent"),
            "parent_id": self.data.get("parent_id"),
            "parent_article_type": self.data.get("parent_article_type"),
            "parent_lang": self.data.get("parent_lang"),
        }

    def validate_product_type_presence(self):
        """
        Validate presence of @product-type attribute (CRITICAL).

        SPS Rule: @product-type is mandatory in all <product> elements.

        Returns
        -------
        dict
            Validation result
        """
        error_level = self.rules.get("product_type_presence_error_level", "CRITICAL")
        product_type = self.data.get("product_type")
        is_valid = bool(product_type and product_type.strip())

        advice_text = _(
            'Add @product-type attribute to <product>.'
            ' Expected value: "book"'
        )
        advice_params = {}

        return build_response(
            title="@product-type attribute",
            parent=self.parent,
            item="product",
            sub_item="@product-type",
            validation_type="exist",
            is_valid=is_valid,
            expected='@product-type attribute present with value "book"',
            obtained=product_type,
            advice=advice_text,
            data=self.data,
            error_level=error_level,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_product_type_value(self):
        """
        Validate that @product-type has value "book" (ERROR).

        SPS Rule: @product-type must be "book" for book reviews.
        Only runs when @product-type is present (non-empty).

        Returns
        -------
        dict or None
            Validation result, or None if @product-type is absent
        """
        error_level = self.rules.get("product_type_value_error_level", "ERROR")
        product_type = self.data.get("product_type")
        expected_values = self.rules.get("product_type_list", ["book"])

        # Skip if product_type is absent (handled by validate_product_type_presence)
        if not product_type or not product_type.strip():
            return None

        is_valid = product_type in expected_values

        advice_text = _(
            'Replace @product-type="{product_type}" with "book".'
            " Valid values: {allowed_values}"
        )
        advice_params = {
            "product_type": product_type,
            "allowed_values": ", ".join(expected_values),
        }

        return build_response(
            title="@product-type value",
            parent=self.parent,
            item="product",
            sub_item="@product-type",
            validation_type="value in list",
            is_valid=is_valid,
            expected=", ".join(expected_values),
            obtained=product_type,
            advice=advice_text.format(**advice_params),
            data=self.data,
            error_level=error_level,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_source_presence(self):
        """
        Validate presence of <source> element (CRITICAL).

        SPS Rule: <source> (book title) is mandatory in <product>.

        Returns
        -------
        dict
            Validation result
        """
        error_level = self.rules.get("source_presence_error_level", "CRITICAL")
        source = self.data.get("source")

        is_valid = source is not None and bool(source.strip())

        advice_text = _(
            "Add <source> element with the book title inside <product>"
        )
        advice_params = {}

        return build_response(
            title="source element",
            parent=self.parent,
            item="product",
            sub_item="source",
            validation_type="exist",
            is_valid=is_valid,
            expected="<source> element with book title",
            obtained=source,
            advice=advice_text,
            data=self.data,
            error_level=error_level,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_article_type_consistency(self):
        """
        Validate consistency between <product> and @article-type (ERROR).

        SPS Rule: When <product> is present, <article> should have
        @article-type="book-review".

        Returns
        -------
        dict
            Validation result
        """
        error_level = self.rules.get("article_type_consistency_error_level", "ERROR")
        article_type = self.data.get("parent_article_type")

        is_valid = article_type == "book-review"

        advice_text = _(
            '<product> is present but @article-type="{article_type}".'
            ' For book reviews, use @article-type="book-review" in <article>'
        )
        advice_params = {"article_type": article_type}

        return build_response(
            title="article-type consistency",
            parent=self.parent,
            item="product",
            sub_item="@article-type",
            validation_type="value",
            is_valid=is_valid,
            expected="book-review",
            obtained=article_type,
            advice=advice_text.format(**advice_params),
            data=self.data,
            error_level=error_level,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_author_presence(self):
        """
        Validate presence of author person-group (WARNING).

        SPS Rule: Recommended that <product> contains
        <person-group person-group-type="author">.

        Returns
        -------
        dict
            Validation result
        """
        error_level = self.rules.get("author_presence_error_level", "WARNING")
        has_author = self.data.get("has_author", False)

        advice_text = _(
            "Add <person-group person-group-type=\"author\"> with the"
            " author(s) of the reviewed book inside <product>"
        )
        advice_params = {}

        return build_response(
            title="author in product",
            parent=self.parent,
            item="product",
            sub_item="person-group",
            validation_type="exist",
            is_valid=has_author,
            expected='<person-group person-group-type="author">',
            obtained=str(has_author),
            advice=advice_text,
            data=self.data,
            error_level=error_level,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_publisher_name_presence(self):
        """
        Validate presence of <publisher-name> element (WARNING).

        SPS Rule: Recommended that <product> contains <publisher-name>.

        Returns
        -------
        dict
            Validation result
        """
        error_level = self.rules.get("publisher_name_presence_error_level", "WARNING")
        has_publisher = self.data.get("has_publisher_name", False)

        advice_text = _(
            "Add <publisher-name> element with the publisher name"
            " inside <product> for bibliographic completeness"
        )
        advice_params = {}

        return build_response(
            title="publisher-name in product",
            parent=self.parent,
            item="product",
            sub_item="publisher-name",
            validation_type="exist",
            is_valid=has_publisher,
            expected="<publisher-name>",
            obtained=str(has_publisher),
            advice=advice_text,
            data=self.data,
            error_level=error_level,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate_year_presence(self):
        """
        Validate presence of <year> element (WARNING).

        SPS Rule: Recommended that <product> contains <year>.

        Returns
        -------
        dict
            Validation result
        """
        error_level = self.rules.get("year_presence_error_level", "WARNING")
        has_year = self.data.get("has_year", False)

        advice_text = _(
            "Add <year> element with the publication year"
            " inside <product> for bibliographic completeness"
        )
        advice_params = {}

        return build_response(
            title="year in product",
            parent=self.parent,
            item="product",
            sub_item="year",
            validation_type="exist",
            is_valid=has_year,
            expected="<year>",
            obtained=str(has_year),
            advice=advice_text,
            data=self.data,
            error_level=error_level,
            advice_text=advice_text,
            advice_params=advice_params,
        )

    def validate(self):
        """
        Run all product validations.

        Returns
        -------
        list
            List of validation results (None values filtered out)
        """
        validations = [
            self.validate_product_type_presence,
            self.validate_product_type_value,
            self.validate_source_presence,
            self.validate_article_type_consistency,
            self.validate_author_presence,
            self.validate_publisher_name_presence,
            self.validate_year_presence,
        ]
        return [response for validate in validations if (response := validate())]


class ArticleProductValidation:
    """
    Validates all <product> elements in an XML article.

    Parameters
    ----------
    xmltree : lxml.etree._Element
        The root element of the XML document
    rules : dict
        Validation rules with error levels
    """

    def __init__(self, xmltree, rules):
        if not hasattr(xmltree, "get"):
            raise ValueError("xmltree must be a valid XML object.")
        if not isinstance(rules, dict):
            raise ValueError("rules must be a dictionary containing error levels.")

        self.xmltree = xmltree
        self.rules = rules
        self.products_model = ArticleProducts(xmltree)

    def validate(self):
        """
        Validate all product elements.

        Yields
        ------
        dict
            Validation results for each product element
        """
        products = list(self.products_model.products)

        for product_data in products:
            yield from ProductValidation(product_data, self.rules).validate()
