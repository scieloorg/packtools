from unittest import TestCase

from lxml import etree
from packtools.sps.validation.article_xref import ArticleXrefValidation


class ArticleXrefValidationTest(TestCase):

    def test_validate_rids_matches(self):
        self.maxDiff = None
        self.xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" 
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <p><xref ref-type="aff" rid="aff1">1</xref></p>     
                        <aff id="aff1">
                            <p>affiliation</p>
                        </aff>
    
                        <p><xref ref-type="fig" rid="fig1">1</xref></p>     
                        <fig id="fig1">
                            <p>figure</p>
                        </fig>
    
                        <p><xref ref-type="table" rid="table1">1</xref></p>     
                        <table id="table1">
                            <p>table</p>
                        </table>
                    </article-meta>
                </front>
            </article>
            """
        )
        obtained = list(ArticleXrefValidation(self.xml_tree).validate_xref_rid_has_corresponding_element_id())

        expected = [
            {
                "title": "xref[@rid] -> *[@id]",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "item": "xref",
                "sub_item": "@rid",
                "validation_type": "match",
                "response": "OK",
                "expected_value": "aff1",
                "got_value": "aff1",
                "message": "Got aff1, expected aff1",
                "advice": None,
                "data": {"element_name": "aff", "ref-type": "aff", "rid": "aff1", "text": "1"},
            },
            {
                "title": "xref[@rid] -> *[@id]",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "item": "xref",
                "sub_item": "@rid",
                "validation_type": "match",
                "response": "OK",
                "expected_value": "fig1",
                "got_value": "fig1",
                "message": "Got fig1, expected fig1",
                "advice": None,
                "data": {"element_name": "fig", "ref-type": "fig", "rid": "fig1", "text": "1"},
            },
            {
                "title": "xref[@rid] -> *[@id]",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "item": "xref",
                "sub_item": "@rid",
                "validation_type": "match",
                "response": "OK",
                "expected_value": "table1",
                "got_value": "table1",
                "message": "Got table1, expected table1",
                "advice": None,
                "data": {"element_name": "table-wrap", "ref-type": "table", "rid": "table1", "text": "1"},
            },
        ]
        self.assertEqual(len(obtained), 3)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_rids_no_matches(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <p><xref ref-type="aff" rid="aff1">1</xref></p>
                        <aff id="aff1">
                            <p>affiliation</p>
                        </aff>

                        <p><xref ref-type="fig" rid="fig1">1</xref></p>
                        <fig id="fig1">
                            <p>figure</p>
                        </fig>

                        <p><xref ref-type="table" rid="table1">1</xref></p>
                    </article-meta>
                </front>
            </article>
            """
        )
        self.article_xref = ArticleXrefValidation(self.xmltree)

        expected = [
            {
                "title": "xref[@rid] -> *[@id]",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "item": "xref",
                "sub_item": "@rid",
                "validation_type": "match",
                "response": "OK",
                "expected_value": "aff1",
                "got_value": "aff1",
                "message": "Got aff1, expected aff1",
                "advice": None,
                "data": {"element_name": "aff", "ref-type": "aff", "rid": "aff1", "text": "1"},
            },
            {
                "title": "xref[@rid] -> *[@id]",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "item": "xref",
                "sub_item": "@rid",
                "validation_type": "match",
                "response": "OK",
                "expected_value": "fig1",
                "got_value": "fig1",
                "message": "Got fig1, expected fig1",
                "advice": None,
                "data": {"element_name": "fig", "ref-type": "fig", "rid": "fig1", "text": "1"},
            },
            {
                "title": "xref[@rid] -> *[@id]",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "item": "xref",
                "sub_item": "@rid",
                "validation_type": "match",
                "response": "ERROR",
                "expected_value": "table1",
                "got_value": None,
                "message": "Got None, expected table1",
                "advice": 'Check if xref[@rid="table1"] is correct or insert the missing table-wrap[@id="table1"]',
                "data": {"element_name": "table-wrap", "ref-type": "table", "rid": "table1", "text": "1"},
            },
        ]
        obtained = list(self.article_xref.validate_xref_rid_has_corresponding_element_id())
        self.assertEqual(len(obtained), 3)
        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)

    def test_validate_ids_matches(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <p><xref ref-type="aff" rid="aff1">1</xref></p>
                        <aff id="aff1">
                            <p>affiliation</p>
                        </aff>

                        <p><xref ref-type="fig" rid="fig1">1</xref></p>
                        <fig id="fig1">
                            <p>figure</p>
                        </fig>

                        <p><xref ref-type="table" rid="table1">1</xref></p>
                        <table-wrap id="table1">
                            <p>table</p>
                        </table-wrap>
                    </article-meta>
                </front>
            </article>
            """
        )
        self.article_xref = ArticleXrefValidation(self.xmltree)

        obtained = list(self.article_xref.validate_element_id_has_corresponding_xref_rid())

        self.assertEqual(["OK", "OK", "OK"], [item["response"] for item in obtained])

        expected = [
            None,
            None,
            None
        ]
        for i, item in enumerate(obtained):
            self.assertEqual(expected[i], item["advice"])

    def test_validate_ids_no_matches(self):
        self.maxDiff = None
        self.xmltree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML"
            dtd-version="1.0" article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <p><xref ref-type="aff" rid="aff1">1</xref></p>
                        <aff id="aff1">
                            <p>affiliation</p>
                        </aff>

                        <p><xref ref-type="fig" rid="fig1">1</xref></p>
                        <fig id="fig1">
                            <p>figure</p>
                        </fig>

                        <table-wrap id="table1">
                            <p>table</p>
                        </table-wrap>
                    </article-meta>
                </front>
            </article>
            """
        )
        self.article_xref = ArticleXrefValidation(self.xmltree)

        expected = [
            {
                "title": "*[@id] -> xref[@rid]",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "item": "aff",
                "sub_item": "@id",
                "validation_type": "match",
                "response": "OK",
                "expected_value": "aff1",
                "got_value": "aff1",
                "message": "Got aff1, expected aff1",
                "advice": None,
                "data": {
                    "id": "aff1",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "tag": "aff",
                },
            },
            {
                "title": "*[@id] -> xref[@rid]",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "item": "fig",
                "sub_item": "@id",
                "validation_type": "match",
                "response": "OK",
                "expected_value": "fig1",
                "got_value": "fig1",
                "message": "Got fig1, expected fig1",
                "advice": None,
                "data": {
                    "id": "fig1",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "tag": "fig",
                },
            },
            {
                "title": "*[@id] -> xref[@rid]",
                "parent": "article",
                "parent_article_type": "research-article",
                "parent_id": None,
                "parent_lang": "pt",
                "item": "table-wrap",
                "sub_item": "@id",
                "validation_type": "match",
                "response": "ERROR",
                "expected_value": "table1",
                "got_value": None,
                "message": "Got None, expected table1",
                "advice": 'Check if table-wrap[@id="table1"] is correct or insert the missing xref[@rid="table1"]',
                "data": {
                    "id": "table1",
                    "parent": "article",
                    "parent_article_type": "research-article",
                    "parent_id": None,
                    "parent_lang": "pt",
                    "tag": "table-wrap",
                },
            },
        ]

        obtained = list(self.article_xref.validate_element_id_has_corresponding_xref_rid())

        for i, item in enumerate(expected):
            with self.subTest(i):
                self.assertDictEqual(obtained[i], item)
