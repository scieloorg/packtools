import unittest
from lxml import etree
from packtools.sps.validation.fn import XMLFnGroupValidation, FnValidation


class TestFnValidation(unittest.TestCase):
    def setUp(self):
        self.rules = {
            "fn_label_error_level": "WARNING",
            "fn_title_error_level": "CRITICAL",
            "fn_bold_error_level": "WARNING",
            "fn_type_error_level": "CRITICAL",
            "fn_type_expected_values": ["conflict", "coi-statement", "custom"],
            "conflict_error_level": "ERROR",
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

        # Check that edited-by validation exists (may be OK or CRITICAL depending on presence)
        edited_by = [r for r in results if r["title"] == "edited-by"]
        self.assertEqual(len(edited_by), 1)

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

        # Check that edited-by validation exists (may be OK or CRITICAL depending on presence)
        edited_by = [r for r in results if r["title"] == "edited-by"]
        self.assertEqual(len(edited_by), 1)

    def test_validate_fn_type_missing_in_fn_group(self):
        """Test Rule 3: @fn-type is mandatory for <fn> in <fn-group>"""
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


if __name__ == "__main__":
    unittest.main()
