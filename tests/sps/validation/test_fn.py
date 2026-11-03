import unittest

from lxml import etree

from packtools.sps.validation.basefn import BaseFnValidation
from packtools.sps.validation.fn import XMLFnGroupValidation, FnValidation
from packtools.sps.validation.xml_validations import (
    validate_fns,
    validate_open_science_actions,
)
from packtools.sps.validation.xml_validator_rules import get_default_rules


class TestFnValidation(unittest.TestCase):
    def setUp(self):
        self.rules = {
            "fn_label_error_level": "WARNING",
            "fn_title_error_level": "CRITICAL",
            "fn_bold_error_level": "WARNING",
            "fn_type_error_level": "CRITICAL",
            "fn_type_expected_values": ["conflict", "coi-statement", "custom"],
            "conflict_error_level": "ERROR",
            "edited_by_error_level": "CRITICAL",
            "edited_by_required_article_types": ["research-article", "case-report"],
        }

    def test_validate_fn(self):
        xml_tree = etree.fromstring('''
            <fn id="f1" fn-type="conflict">
                <label>*</label>
                <title>Conflict of Interest</title>
                <p>This is a footnote.</p>
            </fn>
        ''')
        fn = {
            "fn_id": xml_tree.get("id"),
            "fn_type": xml_tree.get("fn-type"),
            "fn_label": xml_tree.findtext("label"),
            "fn_title": xml_tree.findtext("title"),
            "fn_text": xml_tree.findtext("p"),
        }
        validator = FnValidation(fn, self.rules, 1.0)
        results = validator.validate()

        self.assertEqual(len(results), 5)

        self.assertEqual(results[0]["title"], "label")
        self.assertEqual(results[0]["response"], "OK")
        self.assertIsNone(results[0]["advice"])

        self.assertEqual(results[1]["title"], "unexpected title element")
        self.assertEqual(results[1]["response"], "CRITICAL")
        self.assertEqual(results[1]["advice"], 'Replace <fn><title> with <fn><label>')

        self.assertEqual(results[2]["title"], "unexpected bold element")
        self.assertEqual(results[2]["response"], "OK")
        self.assertIsNone(results[2]["advice"])

        self.assertEqual(results[3]["title"], "fn-type value")
        self.assertEqual(results[3]["response"], "OK")
        self.assertIsNone(results[3]["advice"])

        self.assertEqual(results[4]["title"], "conflict of interest declaration")
        self.assertEqual(results[4]["response"], "OK")
        self.assertIsNone(results[4]["advice"])

    def test_base_fn_invalid_advices_i18n(self):
        validator = BaseFnValidation(
            {
                "fn_label": None,
                "fn_title": "Title",
                "fn_bold": "Label",
                "fn_type": "invalid",
            },
            self.rules,
            1.3,
        )
        conflict_validator = BaseFnValidation(
            {"fn_type": "conflict"},
            self.rules,
            1.3,
        )

        results = [
            validator.validate_label(),
            validator.validate_title(),
            validator.validate_bold(),
            validator.validate_type(),
            conflict_validator.validate_conflict(),
        ]

        for result in results:
            self.assertEqual(
                result["adv_text"].format(**result["adv_params"]),
                result["advice"],
            )

    def test_validate_group(self):
        xml_tree = etree.fromstring('''
            <article>
                <front>
                    <fn-group>
                        <fn id="f1" fn-type="conflict">
                            <label>1</label>
                            <p>Footnote 1 content.</p>
                        </fn>
                        <fn id="f2" fn-type="custom">
                            <p>Footnote 2 content.</p>
                        </fn>
                    </fn-group>
                </front>
            </article>
        ''')
        validator = XMLFnGroupValidation(xml_tree, self.rules)
        results = list(validator.validate())

        # Check for specific validations
        label_warnings = [r for r in results if r["title"] == "label" and r["response"] == "WARNING"]
        self.assertEqual(len(label_warnings), 1)
        self.assertEqual(label_warnings[0]["advice"], 'Mark footnote label with <fn><label>')

        edited_by = [r for r in results if r["title"] == "edited-by"]
        self.assertEqual(len(edited_by), 0)

    def test_validate_edited_by_i18n(self):
        xml_tree = etree.fromstring('<article article-type="research-article"/>')
        validator = XMLFnGroupValidation(xml_tree, self.rules)

        result = list(validator.validate_edited_by())[0]

        self.assertEqual(
            result["adv_text"].format(**result["adv_params"]),
            result["advice"],
        )

    def test_validate_sub_article(self):
        xml_tree = etree.fromstring('''
            <article>
                <sub-article>
                    <fn-group>
                        <fn id="f1" fn-type="conflict">
                            <label>1</label>
                            <p>Footnote 1 content.</p>
                        </fn>
                    </fn-group>
                </sub-article>
            </article>
        ''')
        validator = XMLFnGroupValidation(xml_tree, self.rules)
        results = list(validator.validate())

        edited_by = [r for r in results if r["title"] == "edited-by"]
        self.assertEqual(len(edited_by), 0)

    def test_validate_fn_type_missing_in_fn_group(self):
        """Test Rule 3: @fn-type is mandatory for <fn> in <fn-group>

        Also verifies Anomaly 1 fix: when @fn-type is missing in fn-group,
        only the specific presence validation should fire, not the generic
        validate_type from basefn.py.
        """
        xml_tree = etree.fromstring('''
            <article>
                <front>
                    <fn-group>
                        <fn id="f1">
                            <label>1</label>
                            <p>Footnote without fn-type.</p>
                        </fn>
                    </fn-group>
                </front>
            </article>
        ''')
        validator = XMLFnGroupValidation(xml_tree, self.rules)
        results = list(validator.validate())

        # Filter for fn-type presence validation
        fn_type_presence = [item for item in results if item["title"] == "@fn-type attribute presence in fn-group"]
        self.assertEqual(len(fn_type_presence), 1)
        self.assertEqual(fn_type_presence[0]["response"], "CRITICAL")
        self.assertIn("Add mandatory @fn-type attribute", fn_type_presence[0]["advice"])

        # Verify no double firing: the generic "fn-type value" error should NOT fire
        # when fn-type is missing (None) in fn-group context
        fn_type_value = [item for item in results if item["title"] == "fn-type value"]
        self.assertEqual(len(fn_type_value), 0)

    def test_validate_fn_group_uniqueness_single(self):
        """Test that single <fn-group> passes validation"""
        xml_tree = etree.fromstring('''
            <article>
                <front>
                    <fn-group>
                        <fn id="f1" fn-type="conflict">
                            <label>1</label>
                            <p>Footnote 1.</p>
                        </fn>
                    </fn-group>
                </front>
            </article>
        ''')
        validator = XMLFnGroupValidation(xml_tree, self.rules)
        results = list(validator.validate())
        
        # Should not have uniqueness errors
        uniqueness_errors = [item for item in results if "uniqueness" in item["title"]]
        self.assertEqual(len(uniqueness_errors), 0)

    def test_validate_fn_group_uniqueness_multiple(self):
        """Test Rule 6: <fn-group> should appear at most once"""
        xml_tree = etree.fromstring('''
            <article>
                <front>
                    <fn-group>
                        <fn id="f1" fn-type="conflict">
                            <label>1</label>
                            <p>Footnote 1.</p>
                        </fn>
                    </fn-group>
                </front>
                <body>
                    <fn-group>
                        <fn id="f2" fn-type="custom">
                            <label>2</label>
                            <p>Footnote 2.</p>
                        </fn>
                    </fn-group>
                </body>
            </article>
        ''')
        validator = XMLFnGroupValidation(xml_tree, self.rules)
        results = list(validator.validate())
        
        # Filter for uniqueness validation
        uniqueness_errors = [item for item in results if item["title"] == "fn-group uniqueness"]
        self.assertEqual(len(uniqueness_errors), 1)
        self.assertEqual(uniqueness_errors[0]["response"], "ERROR")
        self.assertIn("at most once", uniqueness_errors[0]["advice"])

    def test_validate_fn_in_table_wrap_foot(self):
        """Test that <fn> in <table-wrap-foot> does not require @fn-type"""
        xml_tree = etree.fromstring('''
            <article>
                <body>
                    <table-wrap>
                        <table-wrap-foot>
                            <fn id="t1fn1">
                                <label>a</label>
                                <p>Table footnote without fn-type.</p>
                            </fn>
                        </table-wrap-foot>
                    </table-wrap>
                </body>
            </article>
        ''')
        validator = XMLFnGroupValidation(xml_tree, self.rules)
        results = list(validator.validate())
        
        # Should not have fn-type presence errors for table footnotes
        fn_type_presence = [item for item in results if "@fn-type attribute presence" in item["title"]]
        self.assertEqual(len(fn_type_presence), 0)


class TestValidateFnsDefaultRules(unittest.TestCase):
    def setUp(self):
        self.params = get_default_rules()

    def _fn_type_results(self, fn_type):
        xml_tree = etree.fromstring(f'''
            <article article-type="research-article" xml:lang="en">
                <back>
                    <fn-group>
                        <fn fn-type="{fn_type}" specific-use="data-available" id="fn1">
                            <label>Data Availability Statement</label>
                            <p>The data are available at the repository.</p>
                        </fn>
                    </fn-group>
                </back>
            </article>
        ''')
        results = list(validate_fns(xml_tree, self.params))
        return [item for item in results if item["title"] == "fn-type value"]

    def test_fn_type_data_availability_in_fn_group_is_valid(self):
        fn_type_value = self._fn_type_results("data-availability")
        self.assertEqual(len(fn_type_value), 1)
        self.assertEqual(fn_type_value[0]["response"], "OK")

    def test_fn_type_data_availability_misspelled_is_invalid(self):
        fn_type_value = self._fn_type_results("data availability")
        self.assertEqual(len(fn_type_value), 1)
        self.assertEqual(fn_type_value[0]["response"], "CRITICAL")


if __name__ == "__main__":
    unittest.main()


class TestValidateEditedBy(unittest.TestCase):
    def setUp(self):
        self.rules = {
            "fn_type_error_level": "CRITICAL",
            "fn_type_expected_values": [],
            "edited_by_error_level": "CRITICAL",
            "edited_by_required_article_types": [
                "data-article",
                "brief-report",
                "case-report",
                "rapid-communication",
                "research-article",
                "review-article",
            ],
        }

    def _validate(self, xml):
        validator = XMLFnGroupValidation(etree.fromstring(xml), self.rules)
        return list(validator.validate_edited_by())

    def test_required_article_types_without_edited_by(self):
        for article_type in self.rules["edited_by_required_article_types"]:
            with self.subTest(article_type=article_type):
                results = self._validate(f"""
                    <article article-type="{article_type}">
                        <front><article-meta>
                            <author-notes><fn fn-type="conflict"><p>None</p></fn></author-notes>
                        </article-meta></front>
                    </article>
                """)
                self.assertEqual(len(results), 1)
                self.assertEqual(results[0]["response"], "CRITICAL")
                self.assertIsNone(results[0]["got_value"])
                self.assertIn(article_type, results[0]["advice"])

    def test_required_article_type_with_edited_by(self):
        results = self._validate("""
            <article article-type="research-article">
                <front><article-meta>
                    <author-notes>
                        <fn fn-type="edited-by"><label>Editor:</label><p>Ana Silva</p></fn>
                    </author-notes>
                </article-meta></front>
            </article>
        """)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
        self.assertEqual(len(results[0]["data"]), 1)

    def test_optional_article_types_have_no_result(self):
        for article_type in ("editorial", "letter", "correction", "reviewer-report"):
            with self.subTest(article_type=article_type):
                results = self._validate(f'<article article-type="{article_type}"/>')
                self.assertEqual(results, [])

    def test_edited_by_outside_author_notes_is_not_accepted(self):
        results = self._validate("""
            <article article-type="research-article">
                <back>
                    <fn-group><fn fn-type="edited-by"><p>Ana Silva</p></fn></fn-group>
                </back>
            </article>
        """)
        self.assertEqual(results[0]["response"], "CRITICAL")

    def test_edited_by_only_in_sub_article_is_not_accepted(self):
        results = self._validate("""
            <article article-type="research-article">
                <front><article-meta/></front>
                <sub-article article-type="translation" xml:lang="pt">
                    <front-stub>
                        <author-notes><fn fn-type="edited-by"><p>Ana Silva</p></fn></author-notes>
                    </front-stub>
                </sub-article>
            </article>
        """)
        self.assertEqual(results[0]["response"], "CRITICAL")

    def test_default_rules_report_edited_by_once_in_open_science(self):
        params = get_default_rules()
        xml_tree = etree.fromstring('<article article-type="case-report"/>')

        open_science = [
            item for item in validate_open_science_actions(xml_tree, params)
            if item["title"] == "edited-by"
        ]
        fns = [
            item for item in validate_fns(xml_tree, params)
            if item["title"] == "edited-by"
        ]

        self.assertEqual(len(open_science), 1)
        self.assertEqual(open_science[0]["response"], "CRITICAL")
        self.assertEqual(fns, [])
