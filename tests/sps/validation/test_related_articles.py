import unittest

from lxml import etree

from packtools.sps.validation.related_articles import RelatedArticleValidation
from packtools.sps.models.v2.related_articles import RelatedArticles


class RelatedArticleValidationTest(unittest.TestCase):

    def test_related_article_matches_article_type_validation_match(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" xlink:href="10.1590/1808-057x202090350"/></article-meta>
            </front>
            </article>

            """
        )
        related_article_dict = list(RelatedArticles(xmltree).related_articles())[0]
        obtained = RelatedArticleValidation(
            related_article_dict
        ).validate_related_article_matches_article_type(
            expected_related_article_types=["corrected-article"]
        )

        expected = {
            "title": "Related article type validation",
            "parent": "article",
            "parent_article_type": "correction",
            "parent_id": None,
            "parent_lang": "en",
            "item": "related-article",
            "sub_item": "related-article-type",
            "validation_type": "match",
            "response": "OK",
            "expected_value": ["corrected-article"],
            "got_value": "corrected-article",
            "message": "Got corrected-article, expected ['corrected-article']",
            "advice": None,
            "data": {
                "parent": "article",
                "parent_article_type": "correction",
                "parent_id": None,
                "parent_lang": "en",
                "ext-link-type": "doi",
                "href": "10.1590/1808-057x202090350",
                "id": "ra1",
                "related-article-type": "corrected-article",
                "text": "",
                "full_tag": '<related-article ext-link-type="doi" id="ra1" '
                'related-article-type="corrected-article" '
                'xlink:href="10.1590/1808-057x202090350"/>',
            },
        }

        self.assertDictEqual(obtained, expected)

    def test_related_article_matches_article_type_validation_not_match(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="retraction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <related-article ext-link-type="doi" id="ra1" related-article-type="retraction-forward" xlink:href="10.1590/1808-057x202090350"/></article-meta>
            </front>
            </article>

            """
        )
        related_article_dict = list(RelatedArticles(xmltree).related_articles())[0]
        obtained = RelatedArticleValidation(
            related_article_dict
        ).validate_related_article_matches_article_type(
            expected_related_article_types=["retracted-article", "article-retracted"]
        )

        expected = {
            "title": "Related article type validation",
            "parent": "article",
            "parent_article_type": "retraction",
            "parent_id": None,
            "parent_lang": "en",
            "item": "related-article",
            "sub_item": "related-article-type",
            "validation_type": "match",
            "response": "ERROR",
            "expected_value": ["retracted-article", "article-retracted"],
            "got_value": "retraction-forward",
            "message": "Got retraction-forward, expected ['retracted-article', 'article-retracted']",
            "advice": "The article-type: retraction does not match the related-article-type: retraction-forward, "
            "provide one of the following items: ['retracted-article', 'article-retracted']",
            "data": {
                "parent": "article",
                "parent_article_type": "retraction",
                "parent_id": None,
                "parent_lang": "en",
                "ext-link-type": "doi",
                "href": "10.1590/1808-057x202090350",
                "id": "ra1",
                "related-article-type": "retraction-forward",
                "text": "",
                "full_tag": '<related-article ext-link-type="doi" id="ra1" '
                'related-article-type="retraction-forward" '
                'xlink:href="10.1590/1808-057x202090350"/>',
            },
        }

        self.assertDictEqual(obtained, expected)

    def test_related_article_has_doi(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="correction-forward" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" xlink:href="10.1590/1808-057x202090350"/></article-meta>
            </front>
            </article>

            """
        )
        related_article_dict = list(RelatedArticles(xmltree).related_articles())[0]
        obtained = RelatedArticleValidation(
            related_article_dict
        ).validate_related_article_doi()

        expected = {
            "title": "Related article doi validation",
            "parent": "article",
            "parent_article_type": "correction-forward",
            "parent_id": None,
            "parent_lang": "en",
            "item": "related-article",
            "sub_item": "xlink:href",
            "validation_type": "exist",
            "response": "OK",
            "expected_value": "10.1590/1808-057x202090350",
            "got_value": "10.1590/1808-057x202090350",
            "message": "Got 10.1590/1808-057x202090350, expected 10.1590/1808-057x202090350",
            "advice": None,
            "data": {
                "parent": "article",
                "parent_article_type": "correction-forward",
                "parent_id": None,
                "parent_lang": "en",
                "ext-link-type": "doi",
                "href": "10.1590/1808-057x202090350",
                "id": "ra1",
                "related-article-type": "corrected-article",
                "text": "",
                "full_tag": '<related-article ext-link-type="doi" id="ra1" '
                'related-article-type="corrected-article" '
                'xlink:href="10.1590/1808-057x202090350"/>',
            },
        }

        self.assertDictEqual(obtained, expected)

    def test_related_articles_does_not_have_doi(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="correction-forward" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <related-article ext-link-type="doi" id="ra1" related-article-type="corrected-article" /></article-meta>
            </front>
            </article>

            """
        )
        related_article_dict = list(RelatedArticles(xmltree).related_articles())[0]
        obtained = RelatedArticleValidation(
            related_article_dict
        ).validate_related_article_doi()

        expected = {
            "title": "Related article doi validation",
            "parent": "article",
            "parent_article_type": "correction-forward",
            "parent_id": None,
            "parent_lang": "en",
            "item": "related-article",
            "sub_item": "xlink:href",
            "validation_type": "exist",
            "response": "ERROR",
            "expected_value": "A valid DOI or URI for related-article/@xlink:href",
            "got_value": None,
            "message": "Got None, expected A valid DOI or URI for related-article/@xlink:href",
            "advice": 'Provide a valid DOI for <related-article ext-link-type="doi" id="ra1" '
            'related-article-type="corrected-article" /> ',
            "data": {
                "parent": "article",
                "parent_article_type": "correction-forward",
                "parent_id": None,
                "parent_lang": "en",
                "ext-link-type": "doi",
                "id": "ra1",
                "related-article-type": "corrected-article",
                "text": "",
                "href": None,
                "full_tag": '<related-article ext-link-type="doi" id="ra1" '
                'related-article-type="corrected-article"/>',
            },
        }

        self.assertDictEqual(obtained, expected)

    def test_related_articles_attribute_validation(self):
        self.maxDiff = None
        xmltree = etree.fromstring(
            """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink"
            article-type="correction" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <related-article related-article-type="corrected-article"/></article-meta>
            </front>
            </article>

            """
        )
        related_article_dict = list(RelatedArticles(xmltree).related_articles())[0]
        obtained = RelatedArticleValidation(
            related_article_dict
        ).validate_attrib_order_in_related_article_tag()

        expected = {
            "title": "attrib order in related article tag",
            "parent": "article",
            "parent_article_type": "correction",
            "parent_id": None,
            "parent_lang": "en",
            "item": "related-article",
            "sub_item": None,
            "validation_type": "match",
            "response": "ERROR",
            "expected_value": '<related-article related-article-type="TYPE" id="ID" xlink:href="HREF" ext-link-type="doi">',
            "got_value": '<related-article related-article-type="corrected-article"/>',
            "message": 'Got <related-article related-article-type="corrected-article"/>, expected '
            '<related-article related-article-type="TYPE" id="ID" xlink:href="HREF" '
            'ext-link-type="doi">',
            "advice": "Provide the attributes in the specified order",
            "data": {
                "parent": "article",
                "parent_article_type": "correction",
                "parent_id": None,
                "parent_lang": "en",
                "ext-link-type": None,
                "href": None,
                "id": None,
                "related-article-type": "corrected-article",
                "text": "",
                "full_tag": "<related-article "
                'related-article-type="corrected-article"/>',
            },
        }

        self.assertDictEqual(obtained, expected)


if __name__ == "__main__":
    unittest.main()
