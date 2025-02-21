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

        self.assertEqual(len(results), 9)

        self.assertEqual(results[4]["title"], "label")
        self.assertEqual(results[4]["response"], "WARNING")
        self.assertEqual(results[4]["advice"], 'Mark footnote label with <fn><label>')

        self.assertEqual(results[8]["title"], "edited-by")
        self.assertEqual(results[8]["response"], "CRITICAL")
        self.assertEqual(results[8]["advice"], 'Add mandatory value for <fn fn-type="edited-by"> to indicate the '
                                               'responsible editor for the purpose of Open Science practice.')

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

        self.assertEqual(len(results), 1)

        self.assertEqual(results[0]["title"], "edited-by")
        self.assertEqual(results[0]["response"], "CRITICAL")
        self.assertEqual(results[0]["advice"], 'Add mandatory value for <fn fn-type="edited-by"> to indicate the '
                                               'responsible editor for the purpose of Open Science practice.')


if __name__ == "__main__":
    unittest.main()
