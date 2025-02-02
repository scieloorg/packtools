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

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["validation_type"], "unexpected")
        self.assertIn("Replace fn/title by fn/label", results[0]["advice"])

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

        self.assertEqual(len(results), 1)  # Apenas fn2 deve gerar erro
        self.assertEqual(results[0]["validation_type"], "exist")
        self.assertIn("label", results[0]["advice"])

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

        self.assertEqual(len(results), 0)  # Nenhum erro esperado


if __name__ == "__main__":
    unittest.main()
