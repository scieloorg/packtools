import unittest
from lxml import etree
from packtools.sps.validation.author_notes import XMLAuthorNotesValidation


class TestAuthorNotesFnValidation(unittest.TestCase):
    def setUp(self):
        self.rules = {
            "corresp_bold_error_level": "CRITICAL",
            "corresp_title_error_level": "CRITICAL",
            "corresp_label_error_level": "WARNING",
            "fn_bold_error_level": "CRITICAL",
            "fn_title_error_level": "CRITICAL",
            "fn_label_error_level": "WARNING",
            "current-aff_error_level": "CRITICAL",
            "con_error_level": "CRITICAL",
            "fn_type_error_level": "CRITICAL",
            "fn_type_expected_values": [
                "abbr",
                "com",
                "coi-statement",
                "conflict",
                "corresp",
                "custom",
                "deceased",
                "edited-by",
                "equal",
                "financial-disclosure",
                "on-leave",
                "other",
                "participating-researchers",
                "present-address",
                "presented-at",
                "presented-by",
                "previously-at",
                "study-group-members",
                "supplementary-material",
                "supported-by"
            ]
        }

    def test_validate_current_affiliation_attrib_type_deprecation(self):
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <author-notes>
                            <corresp id="c01">
                                <label>*</label>
                            </corresp>
                            <fn fn-type="current-aff">
                                <label>*</label>
                                <p>Current affiliation details.</p>
                            </fn>
                        </author-notes>
                    </article-meta>
                </front>
            </article>
        ''')
        obtained = list(
            XMLAuthorNotesValidation(xml_tree, self.rules).validate()
        )

        # Filter for relevant validations
        fn_type_value = [item for item in obtained if item["title"] == "@fn-type value in author-notes"]
        current_aff_deprecation = [item for item in obtained if item["title"] == "unexpected current-aff"]
        
        self.assertEqual(len(fn_type_value), 1)
        self.assertEqual(fn_type_value[0]["validation_type"], "value in list")
        self.assertEqual(fn_type_value[0]["response"], "ERROR")

        self.assertEqual(len(current_aff_deprecation), 1)
        self.assertEqual(current_aff_deprecation[0]["validation_type"], "unexpected")
        self.assertEqual(current_aff_deprecation[0]["response"], "CRITICAL")

    def test_validate_contribution_attrib_type_deprecation(self):
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <author-notes>
                            <corresp id="c01">
                                <label>*</label>
                            </corresp>
                            <fn fn-type="con">
                                <label>*</label>
                                <p>Lead Author</p>
                            </fn>
                        </author-notes>
                    </article-meta>
                </front>
            </article>
        ''')
        obtained = list(
            XMLAuthorNotesValidation(xml_tree, self.rules).validate()
        )
        
        # Filter for relevant validations
        fn_type_value = [item for item in obtained if item["title"] == "@fn-type value in author-notes"]
        con_deprecation = [item for item in obtained if item["title"] == "unexpected con"]
        
        self.assertEqual(len(fn_type_value), 1)
        self.assertEqual(fn_type_value[0]["validation_type"], "value in list")
        self.assertEqual(fn_type_value[0]["response"], "ERROR")

        self.assertEqual(len(con_deprecation), 1)
        self.assertEqual(con_deprecation[0]["validation_type"], "unexpected")
        self.assertEqual(con_deprecation[0]["response"], "CRITICAL")

    def test_validate_corresp_label_presence(self):
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <author-notes>
                            <corresp>
                                <p>Corresponding author details.</p>
                            </corresp>
                        </author-notes>
                    </article-meta>
                </front>
            </article>
        ''')
        obtained = list(XMLAuthorNotesValidation(xml_tree, self.rules).validate())

        # Filtrar somente as validações relacionadas a corresp/label
        obtained = [item for item in obtained if item["item"] == "corresp" and item["sub_item"] == "label"]
        self.assertEqual(len(obtained), 1)
        self.assertEqual(obtained[0]["response"], "WARNING")
        self.assertIn("corresp label", obtained[0]["advice"])

    def test_validate_corresp_title_unexpected(self):
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <author-notes>
                            <corresp>
                                <title>Correspondence</title>
                            </corresp>
                        </author-notes>
                    </article-meta>
                </front>
            </article>
        ''')
        obtained = list(XMLAuthorNotesValidation(xml_tree, self.rules).validate())

        # Filtrar somente as validações relacionadas a corresp/title
        obtained = [item for item in obtained if
                    item["item"] == "corresp" and item["sub_item"] == "unexpected title"]
        self.assertEqual(len(obtained), 1)
        self.assertEqual(obtained[0]["response"], "CRITICAL")
        self.assertIn("Replace <corresp><title> with <corresp><label>", obtained[0]["advice"])

    def test_validate_fn_type_attribute_expected_value(self):
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <author-notes>
                            <corresp id="c01">
                                <label>*</label>
                            </corresp>
                            <fn fn-type="conflict">
                                <label>*</label>
                                <p>Conflict of interest statement.</p>
                            </fn>
                        </author-notes>
                    </article-meta>
                </front>
            </article>
        ''')
        obtained = list(
            XMLAuthorNotesValidation(xml_tree, self.rules).validate()
        )
        # Should have error because 'conflict' is not in SPS 1.10 allowed values for author-notes
        fn_type_errors = [item for item in obtained if item["title"] == "@fn-type value in author-notes"]
        self.assertEqual(len(fn_type_errors), 1)
        self.assertEqual(fn_type_errors[0]["response"], "ERROR")

    def test_validate_fn_type_missing_in_author_notes(self):
        """Test Rule 1: @fn-type is mandatory for <fn> in <author-notes>"""
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <author-notes>
                            <fn>
                                <label>*</label>
                                <p>Author note without fn-type.</p>
                            </fn>
                        </author-notes>
                    </article-meta>
                </front>
            </article>
        ''')
        obtained = list(XMLAuthorNotesValidation(xml_tree, self.rules).validate())
        
        # Filter for fn-type presence validation
        fn_type_presence = [item for item in obtained if item["title"] == "@fn-type attribute presence"]
        self.assertEqual(len(fn_type_presence), 1)
        self.assertEqual(fn_type_presence[0]["response"], "CRITICAL")
        self.assertIn("Add mandatory @fn-type attribute", fn_type_presence[0]["advice"])

    def test_validate_fn_type_invalid_value_in_author_notes(self):
        """Test Rule 2: @fn-type must be from allowed list for author-notes"""
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <author-notes>
                            <fn fn-type="funding">
                                <label>*</label>
                                <p>Funding information.</p>
                            </fn>
                        </author-notes>
                    </article-meta>
                </front>
            </article>
        ''')
        obtained = list(XMLAuthorNotesValidation(xml_tree, self.rules).validate())
        
        # Filter for fn-type value validation
        fn_type_value = [item for item in obtained if item["title"] == "@fn-type value in author-notes"]
        self.assertEqual(len(fn_type_value), 1)
        self.assertEqual(fn_type_value[0]["response"], "ERROR")
        self.assertIn("not valid for <fn> in <author-notes>", fn_type_value[0]["advice"])

    def test_validate_fn_type_valid_values_in_author_notes(self):
        """Test that valid @fn-type values pass validation"""
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <author-notes>
                            <fn fn-type="abbr">
                                <label>*</label>
                                <p>Abbreviation.</p>
                            </fn>
                            <fn fn-type="coi-statement">
                                <label>**</label>
                                <p>Conflict of interest.</p>
                            </fn>
                        </author-notes>
                    </article-meta>
                </front>
            </article>
        ''')
        obtained = list(XMLAuthorNotesValidation(xml_tree, self.rules).validate())
        
        # Should not have errors for fn-type value
        fn_type_errors = [item for item in obtained if item["title"] == "@fn-type value in author-notes"]
        self.assertEqual(len(fn_type_errors), 0)

    def test_validate_corresp_type_recommendation(self):
        """Test Rule 8: Warn when using @fn-type='corresp'"""
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <author-notes>
                            <fn fn-type="corresp">
                                <label>*</label>
                                <p>Corresponding author.</p>
                            </fn>
                        </author-notes>
                    </article-meta>
                </front>
            </article>
        ''')
        obtained = list(XMLAuthorNotesValidation(xml_tree, self.rules).validate())
        
        # Filter for corresp recommendation
        corresp_rec = [item for item in obtained if item["title"] == "corresp element recommendation"]
        self.assertEqual(len(corresp_rec), 1)
        self.assertEqual(corresp_rec[0]["response"], "WARNING")
        self.assertIn("<corresp> element instead", corresp_rec[0]["advice"])

    def test_validate_author_notes_uniqueness_single(self):
        """Test that single <author-notes> passes validation"""
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <author-notes>
                            <fn fn-type="abbr">
                                <label>*</label>
                                <p>Note.</p>
                            </fn>
                        </author-notes>
                    </article-meta>
                </front>
            </article>
        ''')
        obtained = list(XMLAuthorNotesValidation(xml_tree, self.rules).validate())
        
        # Should not have uniqueness errors
        uniqueness_errors = [item for item in obtained if "uniqueness" in item["title"]]
        self.assertEqual(len(uniqueness_errors), 0)

    def test_validate_author_notes_uniqueness_multiple(self):
        """Test Rule 4: <author-notes> should appear at most once"""
        xml_tree = etree.fromstring('''
            <article xmlns:xlink="http://www.w3.org/1999/xlink" article-type="research-article" xml:lang="pt">
                <front>
                    <article-meta>
                        <author-notes>
                            <fn fn-type="abbr">
                                <label>*</label>
                                <p>Note 1.</p>
                            </fn>
                        </author-notes>
                        <author-notes>
                            <fn fn-type="coi-statement">
                                <label>**</label>
                                <p>Note 2.</p>
                            </fn>
                        </author-notes>
                    </article-meta>
                </front>
            </article>
        ''')
        obtained = list(XMLAuthorNotesValidation(xml_tree, self.rules).validate())
        
        # Filter for uniqueness validation
        uniqueness_errors = [item for item in obtained if item["title"] == "author-notes uniqueness"]
        self.assertEqual(len(uniqueness_errors), 1)
        self.assertEqual(uniqueness_errors[0]["response"], "ERROR")
        self.assertIn("at most once", uniqueness_errors[0]["advice"])


if __name__ == "__main__":
    unittest.main()
