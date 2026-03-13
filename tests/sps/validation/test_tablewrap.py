import unittest
from lxml import etree

from packtools.sps.validation.tablewrap import ArticleTableWrapValidation, TableWrapValidation


class TableWrapValidationTest(unittest.TestCase):
    def test_validate_absent(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<p>Some text content without table wraps.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree, rules={"absent_error_level": "WARNING"}
            ).validate()
        )

        self.assertEqual(1, len(obtained))
        result = obtained[0]
        self.assertEqual("table-wrap presence", result["title"])
        self.assertEqual("WARNING", result["response"])
        self.assertEqual("table-wrap", result["item"])
        self.assertIsNone(result["data"])

    def test_validate_id(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<table-wrap>"
            "<label>Table 1</label>"
            "<caption><title>table caption</title></caption>"
            "<table><tbody><tr><td>data</td></tr></tbody></table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree, rules={"id_error_level": "CRITICAL"}
            ).validate()
        )

        # Find the id validation result
        id_results = [r for r in obtained if r["title"] == "id"]
        self.assertEqual(1, len(id_results))
        result = id_results[0]
        self.assertEqual("CRITICAL", result["response"])
        self.assertEqual("table-wrap", result["item"])
        self.assertEqual("id", result["sub_item"])
        self.assertIsNone(result["got_value"])

    def test_validate_id_present(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption><title>table caption</title></caption>"
            "<table><tbody><tr><td>data</td></tr></tbody></table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree, rules={"id_error_level": "CRITICAL"}
            ).validate()
        )

        id_results = [r for r in obtained if r["title"] == "id"]
        self.assertEqual(1, len(id_results))
        result = id_results[0]
        self.assertEqual("OK", result["response"])
        self.assertEqual("t01", result["got_value"])

    def test_validate_label_or_caption_both_missing(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<table><tbody><tr><td>data</td></tr></tbody></table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={"label_or_caption_error_level": "CRITICAL"},
            ).validate()
        )

        results = [r for r in obtained if r["title"] == "label or caption"]
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("CRITICAL", result["response"])
        self.assertIsNone(result["got_value"])

    def test_validate_label_or_caption_only_label(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<table><tbody><tr><td>data</td></tr></tbody></table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={"label_or_caption_error_level": "CRITICAL"},
            ).validate()
        )

        results = [r for r in obtained if r["title"] == "label or caption"]
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("OK", result["response"])

    def test_validate_label_or_caption_only_caption(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<caption><title>Risk factors</title></caption>"
            "<table><tbody><tr><td>data</td></tr></tbody></table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={"label_or_caption_error_level": "CRITICAL"},
            ).validate()
        )

        results = [r for r in obtained if r["title"] == "label or caption"]
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("OK", result["response"])

    def test_validate_label_or_caption_both_present(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption><title>Risk factors</title></caption>"
            "<table><tbody><tr><td>data</td></tr></tbody></table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={"label_or_caption_error_level": "CRITICAL"},
            ).validate()
        )

        results = [r for r in obtained if r["title"] == "label or caption"]
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("OK", result["response"])

    def test_validate_table_missing(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption><title>Table caption</title></caption>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={"table_error_level": "CRITICAL"},
            ).validate()
        )

        results = [r for r in obtained if r["title"] == "table"]
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("CRITICAL", result["response"])
        self.assertIsNone(result["got_value"])

    def test_validate_table_present(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption><title>Table caption</title></caption>"
            "<table><tbody><tr><td>data</td></tr></tbody></table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={"table_error_level": "CRITICAL"},
            ).validate()
        )

        results = [r for r in obtained if r["title"] == "table"]
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("OK", result["response"])

    def test_validate_required_alternatives(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption><title>Table caption</title></caption>"
            "<table><tbody><tr><td>data</td></tr></tbody></table>"
            '<graphic xlink:href="1980-5381-neco-28-02-579-gt05.svg"/>'
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={"alternatives_error_level": "CRITICAL"},
            ).validate()
        )

        results = [r for r in obtained if r["title"] == "alternatives"]
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("CRITICAL", result["response"])
        self.assertIsNone(result["got_value"])

    def test_validate_not_required_alternatives(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption><title>Table caption</title></caption>"
            "<alternatives>"
            "<table><tbody><tr><td>data</td></tr></tbody></table>"
            "</alternatives>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={"alternatives_error_level": "CRITICAL"},
            ).validate()
        )

        results = [r for r in obtained if r["title"] == "alternatives"]
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("CRITICAL", result["response"])
        self.assertEqual("alternatives", result["got_value"])


class TableWrapTrValidationTest(unittest.TestCase):
    """Tests for Rule #3: <tr> must not be a direct child of <table>."""

    def test_validate_tr_not_in_table_valid(self):
        """<tr> inside <tbody> is valid."""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption><title>Sample data</title></caption>"
            "<table>"
            "<tbody>"
            "<tr><td>Data 1</td><td>Data 2</td></tr>"
            "</tbody>"
            "</table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={"tr_in_table_error_level": "ERROR"},
            ).validate()
        )

        results = [r for r in obtained if r["title"] == "table structure"]
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("OK", result["response"])

    def test_validate_tr_in_table_invalid(self):
        """<tr> as direct child of <table> is invalid."""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption><title>Sample data</title></caption>"
            "<table>"
            "<tr><td>Data 1</td><td>Data 2</td></tr>"
            "</table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={"tr_in_table_error_level": "ERROR"},
            ).validate()
        )

        results = [r for r in obtained if r["title"] == "table structure"]
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("ERROR", result["response"])
        self.assertEqual("table/tr", result["sub_item"])


class TableWrapThValidationTest(unittest.TestCase):
    """Tests for Rule #4: <th> must only appear within <thead>."""

    def test_validate_th_in_thead_valid(self):
        """<th> inside <thead> is valid."""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption><title>Sample data</title></caption>"
            "<table>"
            "<thead><tr><th>Header 1</th><th>Header 2</th></tr></thead>"
            "<tbody><tr><td>Data 1</td><td>Data 2</td></tr></tbody>"
            "</table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={"th_in_thead_error_level": "ERROR"},
            ).validate()
        )

        results = [r for r in obtained if r["title"] == "th in thead"]
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("OK", result["response"])

    def test_validate_th_outside_thead_invalid(self):
        """<th> outside <thead> (e.g. in <tbody>) is invalid."""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption><title>Sample data</title></caption>"
            "<table>"
            "<tbody>"
            "<tr><th>Header 1</th><td>Data 1</td></tr>"
            "</tbody>"
            "</table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={"th_in_thead_error_level": "ERROR"},
            ).validate()
        )

        results = [r for r in obtained if r["title"] == "th in thead"]
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("ERROR", result["response"])
        self.assertEqual("th", result["sub_item"])


class TableWrapTdValidationTest(unittest.TestCase):
    """Tests for Rule #5: <td> must only appear within <tbody>."""

    def test_validate_td_in_tbody_valid(self):
        """<td> inside <tbody> is valid."""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption><title>Sample data</title></caption>"
            "<table>"
            "<thead><tr><th>Header 1</th></tr></thead>"
            "<tbody><tr><td>Data 1</td></tr></tbody>"
            "</table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={"td_in_tbody_error_level": "ERROR"},
            ).validate()
        )

        results = [r for r in obtained if r["title"] == "td in tbody"]
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("OK", result["response"])

    def test_validate_td_outside_tbody_invalid(self):
        """<td> outside <tbody> (e.g. in <thead>) is invalid."""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption><title>Sample data</title></caption>"
            "<table>"
            "<thead><tr><td>Header as td</td></tr></thead>"
            "<tbody><tr><td>Data 1</td></tr></tbody>"
            "</table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={"td_in_tbody_error_level": "ERROR"},
            ).validate()
        )

        results = [r for r in obtained if r["title"] == "td in tbody"]
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("ERROR", result["response"])
        self.assertEqual("td", result["sub_item"])


class TableWrapTbodyValidationTest(unittest.TestCase):
    """Tests for Rule #7: <tbody> must be present in <table>."""

    def test_validate_tbody_present(self):
        """<tbody> present in <table> is valid."""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption><title>Sample data</title></caption>"
            "<table>"
            "<tbody><tr><td>Data 1</td></tr></tbody>"
            "</table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={"tbody_error_level": "WARNING"},
            ).validate()
        )

        results = [r for r in obtained if r["title"] == "tbody"]
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("OK", result["response"])

    def test_validate_tbody_missing(self):
        """<tbody> missing from <table> is invalid."""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption><title>Sample data</title></caption>"
            "<table>"
            "<tr><td>Data 1</td></tr>"
            "</table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={"tbody_error_level": "WARNING"},
            ).validate()
        )

        results = [r for r in obtained if r["title"] == "tbody"]
        self.assertEqual(1, len(results))
        result = results[0]
        self.assertEqual("WARNING", result["response"])
        self.assertEqual("tbody", result["sub_item"])


class TableWrapCompleteValidationTest(unittest.TestCase):
    """Tests for fully valid table-wrap elements."""

    def test_fully_valid_table_wrap(self):
        """A fully valid table-wrap with all required elements should pass all validations."""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption><title>Sample data</title></caption>"
            "<table>"
            "<thead><tr><th>Header 1</th><th>Header 2</th></tr></thead>"
            "<tbody><tr><td>Data 1</td><td>Data 2</td></tr></tbody>"
            "</table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={},
            ).validate()
        )

        # All validations should pass (response == "OK")
        for result in obtained:
            self.assertEqual("OK", result["response"], f"Validation '{result['title']}' should pass but got {result['response']}")

    def test_valid_table_wrap_with_empty_title(self):
        """Table-wrap with empty <title/> inside <caption> should pass label_or_caption validation."""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption><title/></caption>"
            "<table>"
            "<tbody><tr><td>Data 1</td></tr></tbody>"
            "</table>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={},
            ).validate()
        )

        results = [r for r in obtained if r["title"] == "label or caption"]
        self.assertEqual(1, len(results))
        # label is present, so this should pass
        self.assertEqual("OK", results[0]["response"])

    def test_table_wrap_with_table_wrap_foot(self):
        """Table with table-wrap-foot should pass all validations."""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption><title>Results</title></caption>"
            "<table>"
            "<tbody><tr><td>Value 1</td><td>Value 2</td></tr></tbody>"
            "</table>"
            "<table-wrap-foot>"
            "<fn><p>Data are expressed as means.</p></fn>"
            "</table-wrap-foot>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={},
            ).validate()
        )

        for result in obtained:
            self.assertEqual("OK", result["response"], f"Validation '{result['title']}' should pass but got {result['response']}")


class TableWrapNoTableNisoValidationTest(unittest.TestCase):
    """Tests that NISO JATS validations are skipped when no <table> is present."""

    def test_no_table_skips_niso_validations(self):
        """When <table> is missing, NISO JATS validations (tr, th, td, tbody) should be skipped."""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:mml="http://www.w3.org/1998/Math/MathML" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<table-wrap id="t01">'
            "<label>Table 1</label>"
            "<caption><title>Table caption</title></caption>"
            "</table-wrap>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleTableWrapValidation(
                xml_tree=xml_tree,
                rules={},
            ).validate()
        )

        # NISO JATS validations should not be present since there's no <table>
        niso_titles = {"table structure", "th in thead", "td in tbody", "tbody"}
        niso_results = [r for r in obtained if r["title"] in niso_titles]
        self.assertEqual(0, len(niso_results))

        # But table validation should still report the missing table
        table_results = [r for r in obtained if r["title"] == "table"]
        self.assertEqual(1, len(table_results))
        self.assertNotEqual("OK", table_results[0]["response"])


if __name__ == "__main__":
    unittest.main()
