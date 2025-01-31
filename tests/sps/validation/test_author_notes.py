import unittest
from lxml import etree
from packtools.sps.validation.author_notes import ArticleAuthorNotesValidation


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
            ArticleAuthorNotesValidation(xml_tree, self.rules).validate()
        )

        self.assertEqual(len(obtained), 2)

        self.assertEqual(obtained[0]["validation_type"], "value in list")
        self.assertEqual(obtained[0]["response"], "CRITICAL")
        self.assertEqual(obtained[0]["advice"],"Select one of ['abbr', 'com', 'coi-statement', 'conflict', "
                                               "'corresp', 'custom', 'deceased', 'edited-by', 'equal', "
                                               "'financial-disclosure', 'on-leave', 'other', "
                                               "'participating-researchers', 'present-address', 'presented-at', "
                                               "'presented-by', 'previously-at', 'study-group-members', "
                                               "'supplementary-material', 'supported-by']")

        self.assertEqual(obtained[1]["validation_type"], "unexpected")
        self.assertEqual(obtained[1]["response"], "CRITICAL")
        self.assertEqual(obtained[1]["advice"], "Use '<bio>' instead of @fn-type='current-aff'")

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
            ArticleAuthorNotesValidation(xml_tree, self.rules).validate()
        )
        self.assertEqual(len(obtained), 2)

        self.assertEqual(obtained[0]["validation_type"], "value in list")
        self.assertEqual(obtained[0]["response"], "CRITICAL")
        self.assertEqual(obtained[0]["advice"], "Select one of ['abbr', 'com', 'coi-statement', 'conflict', "
                                               "'corresp', 'custom', 'deceased', 'edited-by', 'equal', "
                                               "'financial-disclosure', 'on-leave', 'other', "
                                               "'participating-researchers', 'present-address', 'presented-at', "
                                               "'presented-by', 'previously-at', 'study-group-members', "
                                               "'supplementary-material', 'supported-by']")

        self.assertEqual(obtained[1]["validation_type"], "unexpected")
        self.assertEqual(obtained[1]["response"], "CRITICAL")
        self.assertEqual(obtained[1]["advice"], "Use '<role>' instead of @fn-type='con'")

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
        obtained = list(ArticleAuthorNotesValidation(xml_tree, self.rules).validate())

        # Filtrar somente as validações relacionadas a corresp/label
        obtained = [item for item in obtained if item["item"] == "corresp" and item["sub_item"] == "label"]
        self.assertEqual(len(obtained), 1)
        self.assertEqual(obtained[0]["response"], "WARNING")
        self.assertIn("Check if corresp label is present", obtained[0]["advice"])

    def test_validate_corresp_title_unexpected(self):
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
            obtained = list(ArticleAuthorNotesValidation(xml_tree, self.rules).validate())

            # Filtrar somente as validações relacionadas a corresp/title
            obtained = [item for item in obtained if
                        item["item"] == "corresp" and item["sub_item"] == "unexpected title"]
            self.assertEqual(len(obtained), 1)
            self.assertEqual(obtained[0]["response"], "ERROR")
            self.assertIn("Replace corresp/title by corresp/label", obtained[0]["advice"])

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
            ArticleAuthorNotesValidation(xml_tree, self.rules).validate()
        )
        self.assertEqual(len(obtained), 0)  # No errors expected


if __name__ == "__main__":
    unittest.main()
