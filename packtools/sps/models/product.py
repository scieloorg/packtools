"""
Model for extracting <product> elements from XML documents.

<product> is used for marking book review references when related to a book
or book chapter. It should appear in articles with @article-type="book-review".

Example:
    <product product-type="book">
        <person-group person-group-type="author">
            <name>
                <surname>ONFRAY</surname>
                <given-names>Michel</given-names>
            </name>
        </person-group>
        <source>La comunidad filosófica</source>
        <publisher-name>Gedisa</publisher-name>
        <year>2008</year>
    </product>
"""


class ArticleProducts:
    """
    Extracts all <product> elements from an XML article document.

    Processes the main article's <article-meta> to extract product information.
    """

    def __init__(self, xmltree):
        """
        Initialize with XML tree.

        Parameters
        ----------
        xmltree : lxml.etree._Element
            The root element of the XML document
        """
        self.xmltree = xmltree

    @property
    def article_type(self):
        """Returns the article-type attribute from the root <article> element."""
        return self.xmltree.get("article-type")

    @property
    def article_lang(self):
        """Returns the xml:lang attribute from the root <article> element."""
        return self.xmltree.get("{http://www.w3.org/XML/1998/namespace}lang")

    @property
    def products(self):
        """
        Extract all <product> elements from article-meta.

        Yields
        ------
        dict
            Dictionary containing product information:
            - product_type: Value of @product-type attribute
            - source: Text content of <source> element
            - has_author: Whether <person-group person-group-type="author"> exists
            - has_publisher_name: Whether <publisher-name> exists
            - has_year: Whether <year> exists
            - person_groups: List of person-group types found
            - isbn: Text content of <isbn> element
            - publisher_loc: Text content of <publisher-loc> element
            - size: Text content of <size> element
            - parent: "article"
            - parent_id: None
            - parent_article_type: Article type attribute
            - parent_lang: Article language attribute
        """
        article_type = self.article_type
        article_lang = self.article_lang

        for product in self.xmltree.xpath(".//front/article-meta/product"):
            product_type = product.get("product-type")

            source_elem = product.find("source")
            source = None
            if source_elem is not None:
                source = (source_elem.text or "").strip() if source_elem.text else ""

            person_groups = []
            for pg in product.findall("person-group"):
                pg_type = pg.get("person-group-type")
                person_groups.append(pg_type)

            has_author = any(
                pg.get("person-group-type") == "author"
                for pg in product.findall("person-group")
            )

            publisher_name_elem = product.find("publisher-name")
            has_publisher_name = (
                publisher_name_elem is not None
                and bool((publisher_name_elem.text or "").strip())
            )

            year_elem = product.find("year")
            has_year = year_elem is not None and bool((year_elem.text or "").strip())

            isbn_elem = product.find("isbn")
            isbn = (isbn_elem.text or "").strip() if isbn_elem is not None else None

            publisher_loc_elem = product.find("publisher-loc")
            publisher_loc = (
                (publisher_loc_elem.text or "").strip()
                if publisher_loc_elem is not None
                else None
            )

            size_elem = product.find("size")
            size = (size_elem.text or "").strip() if size_elem is not None else None

            yield {
                "product_type": product_type,
                "source": source,
                "has_author": has_author,
                "has_publisher_name": has_publisher_name,
                "has_year": has_year,
                "person_groups": person_groups,
                "isbn": isbn,
                "publisher_loc": publisher_loc,
                "size": size,
                "parent": "article",
                "parent_id": None,
                "parent_article_type": article_type,
                "parent_lang": article_lang,
            }
