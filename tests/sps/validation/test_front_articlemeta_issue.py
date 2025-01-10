from unittest import TestCase
from lxml import etree

from packtools.sps.validation.front_articlemeta_issue import (
    IssueValidation,
    PaginationValidation,
)


class IssueTest(TestCase):
    def test_volume_matches(self):
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue>4</issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        expected = {
            "title": "volume",
            "parent": "article",
            "parent_article_type": None,
            "parent_id": None,
            "parent_lang": None,
            "response": "OK",
            "item": "volume",
            "sub_item": None,
            "validation_type": "format",
            "expected_value": "56",
            "got_value": "56",
            "advice": None,
            "message": "Got 56, expected 56",
            "data": {"volume": "56", "number": "4"},
        }

        validator = IssueValidation(
            xml_tree, params={"volume_format_error_level": "INFO"}
        )

        obtained = validator.validate_volume_format("INFO")

        self.assertDictEqual(obtained, expected)

    def test_volume_no_matches(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume> 56 </volume>
                        <issue>4</issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        expected = {
            "title": "volume",
            "parent": "article",
            "parent_article_type": None,
            "parent_id": None,
            "parent_lang": None,
            "response": "ERROR",
            "item": "volume",
            "sub_item": None,
            "validation_type": "format",
            "expected_value": "alphanumeric value",
            "got_value": " 56 ",
            "advice": "Consulte SPS documentation to complete volume element",
            "message": "Got  56 , expected alphanumeric value",
            "data": {"volume": " 56 ", "number": "4"},
        }

        validator = IssueValidation(
            xml_tree, params={"volume_format_error_level": "ERROR"}
        )

        obtained = validator.validate_volume_format("ERROR")

        self.assertDictEqual(obtained, expected)

    def test_volume_there_is_tag_there_is_no_value(self):
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume></volume>
                        <issue>4</issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        validator = IssueValidation(
            xml_tree, params={"volume_format_error_level": "ERROR"}
        )

        obtained = validator.validate_volume_format("ERROR")

        self.assertIsNone(obtained)

    def test_volume_there_is_no_tag_there_is_no_value(self):
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <issue>4</issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        validator = IssueValidation(
            xml_tree, params={"volume_format_error_level": "INFO"}
        )

        obtained = validator.validate_volume_format("INFO")

        self.assertIsNone(obtained)

    def test_validate_article_issue_without_value(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                    </article-meta>
                </front>
            </article>
            """
        )

        validator = IssueValidation(
            xml_tree, params={"issue_format_error_level": "WARNING"}
        )

        obtained = validator.validate_number_format("WARNING")

        self.assertIsNone(obtained)

    def test_validate_article_issue_out_of_pattern_value(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <issue>vol 4</issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        expected = {
            "title": "number",
            "parent": "article",
            "parent_article_type": None,
            "parent_id": None,
            "parent_lang": None,
            "response": "OK",
            "item": "number",
            "sub_item": None,
            "validation_type": "format",
            "expected_value": "vol4",
            "got_value": "vol4",
            "message": "Got vol4, expected vol4",
            "advice": None,
            "data": {"number": "vol4"},
        }

        validator = IssueValidation(
            xml_tree, params={"issue_format_error_level": "ERROR"}
        )

        obtained = validator.validate_number_format("ERROR")

        self.assertDictEqual(expected, obtained)

    def test_validate_article_issue_number_success(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue>4</issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        expected = {
            "title": "number",
            "parent": "article",
            "parent_article_type": None,
            "parent_id": None,
            "parent_lang": None,
            "response": "OK",
            "item": "number",
            "sub_item": None,
            "validation_type": "format",
            "expected_value": "4",
            "got_value": "4",
            "message": "Got 4, expected 4",
            "advice": None,
            "data": {"number": "4", "volume": "56"},
        }

        validator = IssueValidation(
            xml_tree, params={"issue_format_error_level": "WARNING"}
        )

        obtained = validator.validate_number_format("WARNING")

        self.assertDictEqual(expected, obtained)

    def test_validate_article_issue_number_there_is_tag_there_is_no_value(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue></issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        validator = IssueValidation(
            xml_tree, params={"issue_format_error_level": "WARNING"}
        )

        obtained = validator.validate_number_format("WARNING")

        self.assertIsNone(obtained)

    def test_validate_article_issue_number_there_is_no_tag_there_is_no_value(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                    </article-meta>
                </front>
            </article>
            """
        )

        validator = IssueValidation(
            xml_tree, params={"issue_format_error_level": "WARNING"}
        )

        obtained = validator.validate_number_format("WARNING")

        self.assertIsNone(obtained)

    def test_validate_article_issue_number_start_with_zero(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue>04</issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        expected = {
            "title": "number",
            "parent": "article",
            "parent_article_type": None,
            "parent_id": None,
            "parent_lang": None,
            "response": "ERROR",
            "item": "number",
            "sub_item": None,
            "validation_type": "format",
            "expected_value": "4",
            "got_value": "04",
            "message": "Got 04, expected 4",
            "advice": "Consulte SPS documentation to complete issue element",
            "data": {"number": "04", "volume": "56"},
        }

        validator = IssueValidation(
            xml_tree, params={"issue_format_error_level": "ERROR"}
        )

        obtained = validator.validate_number_format("ERROR")

        self.assertDictEqual(expected, obtained)

    def test_validate_article_issue_number_value_is_not_numeric(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue>4a</issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        expected = {
            "title": "number",
            "parent": "article",
            "parent_article_type": None,
            "parent_id": None,
            "parent_lang": None,
            "response": "OK",
            "item": "number",
            "sub_item": None,
            "validation_type": "format",
            "expected_value": "4a",
            "got_value": "4a",
            "message": "Got 4a, expected 4a",
            "advice": None,
            "data": {"number": "4a", "volume": "56"},
        }

        validator = IssueValidation(
            xml_tree, params={"issue_format_error_level": "WARNING"}
        )

        obtained = validator.validate_number_format("WARNING")

        self.assertDictEqual(expected, obtained)

    def test_validate_article_issue_special_number(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue>spa 1</issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        expected = {
            "title": "special or supplement",
            "parent": "article",
            "parent_article_type": None,
            "parent_id": None,
            "parent_lang": None,
            "response": "WARNING",
            "item": "issue",
            "sub_item": "special or supplement",
            "validation_type": "format",
            "expected_value": ["suppl 1", "spe 1"],
            "got_value": {"type": "spa", "type_valid_format": False, "type_value": "1"},
            "message": "Got {'type_value': '1', 'type': 'spa', 'type_valid_format': False}, expected ['suppl 1', 'spe 1']",
            "advice": "Consulte SPS documentation to complete issue element",
            "data": {"issue": "spa 1"},
        }

        validator = IssueValidation(
            xml_tree, params={"issue_format_error_level": "WARNING"}
        )

        obtained = validator.validate_issue_format("WARNING")

        self.assertDictEqual(expected, obtained)

    def test_validate_article_issue_special_number_with_dot(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue>spe.1</issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        validator = IssueValidation(
            xml_tree, params={"issue_format_error_level": "ERROR"}
        )

        obtained = validator.validate_issue_format("ERROR")

        self.assertIsNone(obtained)

    def test_validate_article_issue_special_number_with_space(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue> spe 1</issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        expected = {
            "title": "special or supplement",
            "parent": "article",
            "parent_article_type": None,
            "parent_id": None,
            "parent_lang": None,
            "response": "OK",
            "item": "issue",
            "sub_item": "special or supplement",
            "validation_type": "format",
            "expected_value": ["spe 1"],
            "got_value": {"type": "spe", "type_valid_format": True, "type_value": "1"},
            "message": "Got {'type_value': '1', 'type': 'spe', 'type_valid_format': True}, expected ['spe 1']",
            "advice": None,
            "data": {"issue": " spe 1"},
        }

        validator = IssueValidation(
            xml_tree, params={"issue_format_error_level": "ERROR"}
        )

        obtained = validator.validate_issue_format("ERROR")

        self.assertDictEqual(expected, obtained)

    def test_validate_article_issue_supplement(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue>suppl 1</issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        expected = {
            "title": "special or supplement",
            "parent": "article",
            "parent_article_type": None,
            "parent_id": None,
            "parent_lang": None,
            "response": "OK",
            "item": "issue",
            "sub_item": "special or supplement",
            "validation_type": "format",
            "expected_value": ["suppl 1"],
            "got_value": {
                "type": "suppl",
                "type_valid_format": True,
                "type_value": "1",
            },
            "message": "Got {'type_value': '1', 'type': 'suppl', 'type_valid_format': True}, expected ['suppl 1']",
            "advice": None,
            "data": {"issue": "suppl 1"},
        }

        validator = IssueValidation(
            xml_tree, params={"issue_format_error_level": "WARNING"}
        )

        obtained = validator.validate_issue_format("WARNING")

        self.assertDictEqual(expected, obtained)

    def test_validate_article_issue_supplement_with_dot(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue>suppl a.</issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        expected = {
            "title": "special or supplement",
            "parent": "article",
            "parent_article_type": None,
            "parent_id": None,
            "parent_lang": None,
            "response": "OK",
            "item": "issue",
            "sub_item": "special or supplement",
            "validation_type": "format",
            "expected_value": ["suppl a."],
            "got_value": {
                "type": "suppl",
                "type_valid_format": True,
                "type_value": "a.",
            },
            "message": "Got {'type_value': 'a.', 'type': 'suppl', 'type_valid_format': True}, expected ['suppl a.']",
            "advice": None,
            "data": {"issue": "suppl a."},
        }

        validator = IssueValidation(
            xml_tree, params={"issue_format_error_level": "ERROR"}
        )

        obtained = validator.validate_issue_format("ERROR")

        self.assertDictEqual(expected, obtained)

    def test_validate_article_issue_supplement_number_starts_with_zero(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue>suppl 04</issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        expected = {
            "title": "special or supplement",
            "parent": "article",
            "parent_article_type": None,
            "parent_id": None,
            "parent_lang": None,
            "response": "OK",
            "item": "issue",
            "sub_item": "special or supplement",
            "validation_type": "format",
            "expected_value": ["suppl 04"],
            "got_value": {
                "type": "suppl",
                "type_valid_format": True,
                "type_value": "04",
            },
            "message": "Got {'type_value': '04', 'type': 'suppl', 'type_valid_format': True}, expected ['suppl 04']",
            "advice": None,
            "data": {"issue": "suppl 04"},
        }

        validator = IssueValidation(
            xml_tree, params={"issue_format_error_level": "ERROR"}
        )

        obtained = validator.validate_issue_format("ERROR")

        self.assertDictEqual(expected, obtained)

    def test_validate_article_issue_number_supplement(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue>4 suppl 1</issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        expected = {
            "title": "special or supplement",
            "parent": "article",
            "parent_article_type": None,
            "parent_id": None,
            "parent_lang": None,
            "response": "OK",
            "item": "issue",
            "sub_item": "special or supplement",
            "validation_type": "format",
            "expected_value": ["4 suppl 1"],
            "got_value": {
                "number": "4",
                "type": "suppl",
                "type_valid_format": True,
                "type_value": "1",
            },
            "message": "Got {'number': '4', 'type_value': '1', 'type': 'suppl', 'type_valid_format': True}, expected ['4 suppl 1']",
            "advice": None,
            "data": {"issue": "4 suppl 1"},
        }

        validator = IssueValidation(
            xml_tree, params={"issue_format_error_level": "WARNING"}
        )

        obtained = validator.validate_issue_format("WARNING")

        self.assertDictEqual(expected, obtained)

    def test_validate_article_issue_number_supplement_with_dot_and_space(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue> a suppl b.</issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        expected = {
            "title": "special or supplement",
            "parent": "article",
            "parent_article_type": None,
            "parent_id": None,
            "parent_lang": None,
            "response": "OK",
            "item": "issue",
            "sub_item": "special or supplement",
            "validation_type": "format",
            "expected_value": ["a suppl b."],
            "got_value": {
                "number": "a",
                "type": "suppl",
                "type_valid_format": True,
                "type_value": "b.",
            },
            "message": "Got {'number': 'a', 'type_value': 'b.', 'type': 'suppl', 'type_valid_format': True}, expected ['a suppl b.']",
            "advice": None,
            "data": {"issue": " a suppl b."},
        }

        validator = IssueValidation(
            xml_tree, params={"issue_format_error_level": "ERROR"}
        )

        obtained = validator.validate_issue_format("ERROR")

        self.assertDictEqual(expected, obtained)

    def test_suppl_matches(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue>4</issue>
                        <supplement>2</supplement>
                    </article-meta>
                </front>
            </article>
            """
        )

        expected = {
            "title": "supplement",
            "parent": "article",
            "parent_article_type": None,
            "parent_id": None,
            "parent_lang": None,
            "response": "OK",
            "item": "supplement",
            "sub_item": None,
            "validation_type": "format",
            "expected_value": "2",
            "got_value": "2",
            "message": "Got 2, expected 2",
            "advice": None,
            "data": {"number": "4", "suppl": "2", "volume": "56"},
        }

        validator = IssueValidation(
            xml_tree, params={"supplement_format_error_level": "INFO"}
        )

        obtained = validator.validate_supplement_format("INFO")

        self.assertDictEqual(expected, obtained)

    def test_suppl_no_matches(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue>4</issue>
                        <supplement>2b</supplement>
                    </article-meta>
                </front>
            </article>
            """
        )

        expected = {
            "title": "supplement",
            "parent": "article",
            "parent_article_type": None,
            "parent_id": None,
            "parent_lang": None,
            "response": "OK",
            "item": "supplement",
            "sub_item": None,
            "validation_type": "format",
            "expected_value": "2b",
            "got_value": "2b",
            "message": "Got 2b, expected 2b",
            "advice": None,
            "data": {"number": "4", "suppl": "2b", "volume": "56"},
        }

        validator = IssueValidation(
            xml_tree, params={"supplement_format_error_level": "ERROR"}
        )

        obtained = validator.validate_supplement_format("ERROR")

        self.assertDictEqual(expected, obtained)

    def test_suppl_implicit(self):
        self.maxDiff = None  # Permite exibir diferenças detalhadas em caso de falha
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue>4 suppl 2</issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        expected = {
            "title": "special or supplement",
            "parent": "article",
            "parent_article_type": None,
            "parent_id": None,
            "parent_lang": None,
            "response": "OK",
            "item": "issue",
            "sub_item": "special or supplement",
            "validation_type": "format",
            "expected_value": ["4 suppl 2"],
            "got_value": {
                "number": "4",
                "type": "suppl",
                "type_valid_format": True,
                "type_value": "2",
            },
            "message": "Got {'number': '4', 'type_value': '2', 'type': 'suppl', 'type_valid_format': True}, expected ['4 suppl 2']",
            "advice": None,
            "data": {"issue": "4 suppl 2"},
        }

        validator = IssueValidation(
            xml_tree, params={"supplement_format_error_level": "INFO"}
        )

        obtained = validator.validate_issue_format("INFO")

        self.assertDictEqual(expected, obtained)

    def test_suppl_without_suppl(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue>4</issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        validator = IssueValidation(
            xml_tree, params={"supplement_format_error_level": "INFO"}
        )

        obtained = validator.validate_supplement_format("INFO")

        self.assertIsNone(obtained)

    def test_validate_article_issue(self):
        self.maxDiff = None
        xml_tree = etree.fromstring(
            """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                        <issue>4 suppl 1</issue>
                    </article-meta>
                </front>
            </article>
            """
        )

        expected = [
            {
                "title": "volume",
                "parent": "article",
                "parent_article_type": None,
                "parent_id": None,
                "parent_lang": None,
                "response": "OK",
                "item": "volume",
                "sub_item": None,
                "validation_type": "format",
                "expected_value": "56",
                "got_value": "56",
                "message": "Got 56, expected 56",
                "advice": None,
                "data": {"number": "4", "suppl": "1", "volume": "56"},
            },
            {
                "title": "number",
                "parent": "article",
                "parent_article_type": None,
                "parent_id": None,
                "parent_lang": None,
                "response": "OK",
                "item": "number",
                "sub_item": None,
                "validation_type": "format",
                "expected_value": "4",
                "got_value": "4",
                "message": "Got 4, expected 4",
                "advice": None,
                "data": {"number": "4", "suppl": "1", "volume": "56"},
            },
            {
                "title": "supplement",
                "parent": "article",
                "parent_article_type": None,
                "parent_id": None,
                "parent_lang": None,
                "response": "OK",
                "item": "supplement",
                "sub_item": None,
                "validation_type": "format",
                "expected_value": "1",
                "got_value": "1",
                "message": "Got 1, expected 1",
                "advice": None,
                "data": {"number": "4", "suppl": "1", "volume": "56"},
            },
            {
                "title": "special or supplement",
                "parent": "article",
                "parent_article_type": None,
                "parent_id": None,
                "parent_lang": None,
                "response": "OK",
                "item": "issue",
                "sub_item": "special or supplement",
                "validation_type": "format",
                "expected_value": ["4 suppl 1"],
                "got_value": {
                    "number": "4",
                    "type": "suppl",
                    "type_valid_format": True,
                    "type_value": "1",
                },
                "message": "Got {'number': '4', 'type_value': '1', 'type': 'suppl', 'type_valid_format': True}, expected ['4 suppl 1']",
                "advice": None,
                "data": {"issue": "4 suppl 1"},
            },
            {
                "title": "registered issue",
                "parent": "article",
                "parent_article_type": None,
                "parent_id": None,
                "parent_lang": None,
                "response": "OK",
                "item": "volume, number, supplement",
                "sub_item": None,
                "validation_type": "value in list",
                "expected_value": [{"volume": "56", "number": "4", "supplement": "1"}],
                "got_value": {"volume": "56", "number": "4", "supplement": "1"},
                "message": "Got {'volume': '56', 'number': '4', 'supplement': '1'}, expected [{'volume': '56', 'number': '4', 'supplement': '1'}]",
                "advice": None,
                "data": {"issue": {"volume": "56", "number": "4", "supplement": "1"}},
            },
        ]

        validator = IssueValidation(
            xml_tree,
            params={
                "volume_format_error_level": "INFO",
                "issue_format_error_level": "INFO",
                "supplement_format_error_level": "INFO",
                "number_format_error_level": "INFO",
                "expected_issues_error_level": "INFO",
                "journal_data": {
                    "issues": [{"volume": "56", "number": "4", "supplement": "1"}]
                },
            },
        )

        obtained = list(validator.validate())

        self.assertEqual(len(obtained), len(expected))

        for i, item in enumerate(expected):
            with self.subTest(i=i):
                self.assertDictEqual(obtained[i], item)


class PaginationTest(TestCase):
    def test_validation_pages(self):
        self.maxDiff = None
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = etree.fromstring(xml)

        expected = {
            "title": "Pagination",
            "parent": "article",
            "parent_article_type": None,
            "parent_id": None,
            "parent_lang": None,
            "item": "elocation-id | fpage / lpage",
            "sub_item": "elocation-id | fpage / lpage",
            "validation_type": "match",
            "response": "CRITICAL",
            "expected_value": "elocation-id or fpage + lpage",
            "got_value": "elocation-id: None, fpage: None, lpage: None",
            "message": "Got elocation-id: None, fpage: None, lpage: None, expected elocation-id or fpage + lpage",
            "advice": "Provide elocation-id or fpage + lpage",
            "data": {"volume": "56"},
        }

        obtained = PaginationValidation(xml_tree).validate("CRITICAL")

        self.assertDictEqual(expected, obtained)

    def test_validation_e_location(self):
        self.maxDiff = None
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <volume>56</volume>
                    </article-meta>
                </front>
            </article>
            """
        xml_tree = etree.fromstring(xml)

        expected = {
            "title": "Pagination",
            "parent": "article",
            "parent_article_type": None,
            "parent_id": None,
            "parent_lang": None,
            "item": "elocation-id | fpage / lpage",
            "sub_item": "elocation-id | fpage / lpage",
            "validation_type": "match",
            "response": "CRITICAL",
            "expected_value": "elocation-id or fpage + lpage",
            "got_value": "elocation-id: None, fpage: None, lpage: None",
            "message": "Got elocation-id: None, fpage: None, lpage: None, expected elocation-id or fpage + lpage",
            "advice": "Provide elocation-id or fpage + lpage",
            "data": {"volume": "56"},
        }

        obtained = PaginationValidation(xml_tree).validate("CRITICAL")

        self.assertDictEqual(expected, obtained)

    def test_validation_pages_and_e_location_exists_fail(self):
        self.maxDiff = None
        xml = """
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="en">
                <front>
                    <article-meta>
                        <elocation-id>e51467</elocation-id>
                        <fpage>220</fpage>
                        <lpage>240</lpage>
                    </article-meta>
                </front>
            </article>
            """

        xml_tree = etree.fromstring(xml)

        obtained = PaginationValidation(xml_tree).validate("CRITICAL")

        self.assertIsNone(obtained)
