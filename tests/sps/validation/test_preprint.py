import unittest

from packtools.sps.utils.xml_utils import get_xml_tree
from packtools.sps.models.v2.related_articles import RelatedArticles
from packtools.sps.validation.related_articles import RelatedArticleValidation


class PreprintValidationTest(unittest.TestCase):
    def test_preprint_validation_preprint(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <related-article id="pp1" related-article-type="preprint" ext-link-type="doi" xlink:href="10.1590/SciELOPreprints.1174"/>
            <history>
            <date date-type="preprint">
            <day>18</day>
            <month>10</month>
            <year>2002</year>
            </date>
            </history>
            </article-meta>
            </front>
            </article>
        """
        xml_tree = get_xml_tree(xml_str)

        related_article_dict = list(RelatedArticles(xml_tree).related_articles())[0]
        obtained = RelatedArticleValidation(
            related_article_dict
        ).validate_related_article_matches_article_type(
            expected_related_article_types=["preprint"]
        )

        expected = {
            "title": "Related article type validation",
            "parent": "article",
            "parent_article_type": "research-article",
            "parent_id": None,
            "parent_lang": "en",
            "item": "related-article",
            "sub_item": "related-article-type",
            "validation_type": "match",
            "response": "OK",
            "expected_value": ["preprint"],
            "got_value": "preprint",
            "message": "Got preprint, expected ['preprint']",
            "advice": None,
            "data": {
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "en",
                "ext-link-type": "doi",
                "href": "10.1590/SciELOPreprints.1174",
                "id": "pp1",
                "related-article-type": "preprint",
                "text": "",
                "full_tag": '<related-article id="pp1" '
                'related-article-type="preprint" ext-link-type="doi" '
                'xlink:href="10.1590/SciELOPreprints.1174"/>',
            },
        }

        self.assertDictEqual(expected, obtained)

    def test_preprint_validation_preprint_date(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <related-article id="pp1" related-article-type="preprint" ext-link-type="doi" xlink:href="10.1590/SciELOPreprints.1174"/>
            <history>
            <date date-type="preprint">
            <day>18</day>
            <month>10</month>
            <year>2002</year>
            </date>
            </history>
            </article-meta>
            </front>
            </article>
        """
        xml_tree = get_xml_tree(xml_str)

        related_article_dict = list(RelatedArticles(xml_tree).related_articles())[0]
        obtained = RelatedArticleValidation(related_article_dict).validate_history_date(
            expected_date_type="preprint",
            history_events={
                "preprint": {
                    "day": "18",
                    "month": "10",
                    "type": "preprint",
                    "year": "2022",
                }
            },
        )

        self.assertIsNone(obtained)

    def test_preprint_validation_preprint_date_not_ok(self):
        self.maxDiff = None
        xml_str = """
            <article xmlns:mml="http://www.w3.org/1998/Math/MathML" xmlns:xlink="http://www.w3.org/1999/xlink" 
            article-type="research-article" dtd-version="1.1" specific-use="sps-1.9" xml:lang="en">
            <front>
            <article-meta>
            <related-article id="pp1" related-article-type="preprint" ext-link-type="doi" xlink:href="10.1590/SciELOPreprints.1174"/>
            </article-meta>
            </front>
            </article>
        """
        xml_tree = get_xml_tree(xml_str)

        related_article_dict = list(RelatedArticles(xml_tree).related_articles())[0]
        obtained = RelatedArticleValidation(related_article_dict).validate_history_date(
            expected_date_type="preprint", history_events={}
        )

        expected = {
            "title": "history date",
            "parent": "article",
            "parent_id": None,
            "parent_article_type": "research-article",
            "parent_lang": "en",
            "item": "related-article / date",
            "sub_item": "@related-article-type=preprint / @date-type=preprint",
            "validation_type": "exist",
            "response": "ERROR",
            "expected_value": "preprint",
            "got_value": {},
            "message": "Got {}, expected preprint",
            "advice": "Provide the publication date of the preprint",
            "data": {},
        }

        self.assertDictEqual(expected, obtained)


if __name__ == "__main__":
    unittest.main()
