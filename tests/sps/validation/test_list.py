import unittest
from lxml import etree

from packtools.sps.validation.list import ArticleListValidation


class ListValidationTest(unittest.TestCase):
    def test_list_validation_valid_bullet_list(self):
        """Test valid bullet list with all required attributes"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<list list-type="bullet">'
            "    <title>Nam commodo</title>"
            "    <list-item>"
            "        <p>Morbi luctus elit enim.</p>"
            "    </list-item>"
            "    <list-item>"
            "        <p>Nullam nunc leo.</p>"
            "    </list-item>"
            "</list>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleListValidation(
                xml_tree,
                {
                    "list_type_presence_error_level": "CRITICAL",
                    "list_type_value_error_level": "ERROR",
                    "min_list_items_error_level": "ERROR",
                    "label_in_list_item_error_level": "WARNING",
                    "empty_list_item_error_level": "WARNING",
                    "missing_title_error_level": "INFO",
                },
            ).validate()
        )

        # All validations should pass (response = "OK")
        for item in obtained:
            with self.subTest(item["title"]):
                self.assertEqual(item["response"], "OK")

    def test_list_validation_missing_list_type(self):
        """Test list without @list-type attribute (CRITICAL error)"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            "<list>"
            "    <list-item>"
            "        <p>Item 1.</p>"
            "    </list-item>"
            "    <list-item>"
            "        <p>Item 2.</p>"
            "    </list-item>"
            "</list>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleListValidation(
                xml_tree,
                {
                    "list_type_presence_error_level": "CRITICAL",
                    "list_type_value_error_level": "ERROR",
                    "min_list_items_error_level": "ERROR",
                    "label_in_list_item_error_level": "WARNING",
                },
            ).validate()
        )

        # Check that list_type presence validation failed
        list_type_validation = [
            item for item in obtained if item["title"] == "@list-type presence"
        ][0]
        self.assertEqual(list_type_validation["response"], "CRITICAL")
        self.assertIsNone(list_type_validation["got_value"])
        self.assertIn("Add list-type attribute", list_type_validation["advice"])

    def test_list_validation_empty_list_type(self):
        """Test list with empty @list-type attribute (CRITICAL error)"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<list list-type="">'
            "    <list-item>"
            "        <p>Item 1.</p>"
            "    </list-item>"
            "    <list-item>"
            "        <p>Item 2.</p>"
            "    </list-item>"
            "</list>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleListValidation(
                xml_tree,
                {
                    "list_type_presence_error_level": "CRITICAL",
                    "list_type_value_error_level": "ERROR",
                },
            ).validate()
        )

        # Check that list_type presence validation failed
        list_type_validation = [
            item for item in obtained if item["title"] == "@list-type presence"
        ][0]
        self.assertEqual(list_type_validation["response"], "CRITICAL")
        self.assertEqual(list_type_validation["got_value"], '""')
        self.assertIn("cannot be empty", list_type_validation["advice"])

    def test_list_validation_invalid_list_type_value(self):
        """Test list with invalid @list-type value (ERROR)"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<list list-type="numbered">'
            "    <list-item>"
            "        <p>Item 1.</p>"
            "    </list-item>"
            "    <list-item>"
            "        <p>Item 2.</p>"
            "    </list-item>"
            "</list>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleListValidation(
                xml_tree,
                {
                    "list_type_presence_error_level": "CRITICAL",
                    "list_type_value_error_level": "ERROR",
                },
            ).validate()
        )

        # Check that list_type value validation failed
        list_type_value_validation = [
            item for item in obtained if item["title"] == "@list-type value"
        ][0]
        self.assertEqual(list_type_value_validation["response"], "ERROR")
        self.assertEqual(list_type_value_validation["got_value"], "numbered")
        self.assertIn('"numbered" is not allowed', list_type_value_validation["advice"])

    def test_list_validation_only_one_list_item(self):
        """Test list with only one <list-item> (ERROR)"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<list list-type="bullet">'
            "    <list-item>"
            "        <p>Only one item.</p>"
            "    </list-item>"
            "</list>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleListValidation(
                xml_tree,
                {
                    "min_list_items_error_level": "ERROR",
                },
            ).validate()
        )

        # Check that min list items validation failed
        min_items_validation = [
            item for item in obtained if item["title"] == "minimum list items"
        ][0]
        self.assertEqual(min_items_validation["response"], "ERROR")
        self.assertIn("at least 2", min_items_validation["advice"])

    def test_list_validation_with_label_in_list_item(self):
        """Test list with <label> in <list-item> (WARNING)"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<list list-type="bullet">'
            "    <list-item>"
            "        <label>•</label>"
            "        <p>Item with label.</p>"
            "    </list-item>"
            "    <list-item>"
            "        <label>•</label>"
            "        <p>Another item with label.</p>"
            "    </list-item>"
            "</list>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleListValidation(
                xml_tree,
                {
                    "label_in_list_item_error_level": "WARNING",
                },
            ).validate()
        )

        # Check that label validation failed
        label_validation = [
            item for item in obtained if item["title"] == "no label in list-item"
        ][0]
        self.assertEqual(label_validation["response"], "WARNING")
        self.assertIn("For accessibility", label_validation["advice"])

    def test_list_validation_empty_list_items(self):
        """Test list with empty <list-item> elements (WARNING)"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<list list-type="bullet">'
            "    <list-item>"
            "        <p>Item with content.</p>"
            "    </list-item>"
            "    <list-item>"
            "    </list-item>"
            "</list>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleListValidation(
                xml_tree,
                {
                    "empty_list_item_error_level": "WARNING",
                },
            ).validate()
        )

        # Check that empty list item validation failed
        empty_items_validation = [
            item for item in obtained if item["title"] == "list-item has content"
        ][0]
        self.assertEqual(empty_items_validation["response"], "WARNING")
        self.assertIn("empty <list-item>", empty_items_validation["advice"])

    def test_list_validation_all_list_types(self):
        """Test that all valid list-type values are accepted"""
        valid_types = [
            "order",
            "bullet",
            "alpha-lower",
            "alpha-upper",
            "roman-lower",
            "roman-upper",
            "simple",
        ]

        for list_type in valid_types:
            with self.subTest(list_type=list_type):
                xml_tree = etree.fromstring(
                    f'<article xmlns:xlink="http://www.w3.org/1999/xlink" '
                    f'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
                    f"<body>"
                    f'<list list-type="{list_type}">'
                    f"    <list-item>"
                    f"        <p>Item 1.</p>"
                    f"    </list-item>"
                    f"    <list-item>"
                    f"        <p>Item 2.</p>"
                    f"    </list-item>"
                    f"</list>"
                    f"</body>"
                    f"</article>"
                )
                obtained = list(
                    ArticleListValidation(
                        xml_tree,
                        {
                            "list_type_value_error_level": "ERROR",
                        },
                    ).validate()
                )

                # Check that list_type value validation passed
                list_type_value_validation = [
                    item for item in obtained if item["title"] == "@list-type value"
                ][0]
                self.assertEqual(list_type_value_validation["response"], "OK")

    def test_list_validation_nested_list(self):
        """Test nested lists are validated independently"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<list list-type="order">'
            "    <title>Vivamus cursus</title>"
            "    <list-item>"
            "        <p>Nullam gravida tellus.</p>"
            '        <list list-type="bullet">'
            "            <list-item>"
            "                <p>Sub-item 1.</p>"
            "            </list-item>"
            "            <list-item>"
            "                <p>Sub-item 2.</p>"
            "            </list-item>"
            "        </list>"
            "    </list-item>"
            "    <list-item>"
            "        <p>Donec pulvinar odio.</p>"
            "    </list-item>"
            "</list>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleListValidation(
                xml_tree,
                {
                    "list_type_presence_error_level": "CRITICAL",
                    "list_type_value_error_level": "ERROR",
                },
            ).validate()
        )

        # Should validate both parent and nested list
        # Count how many lists were validated (should be 2)
        list_type_validations = [
            item for item in obtained if item["title"] == "@list-type presence"
        ]
        self.assertEqual(len(list_type_validations), 2)
        
        # Both should pass
        for validation in list_type_validations:
            self.assertEqual(validation["response"], "OK")

    def test_list_validation_no_title_recommendation(self):
        """Test that missing title generates INFO-level recommendation"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<list list-type="bullet">'
            "    <list-item>"
            "        <p>Item without title.</p>"
            "    </list-item>"
            "    <list-item>"
            "        <p>Another item.</p>"
            "    </list-item>"
            "</list>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleListValidation(
                xml_tree,
                {
                    "missing_title_error_level": "INFO",
                },
            ).validate()
        )

        # Check that title recommendation is present (but passes validation)
        title_validation = [
            item for item in obtained if item["title"] == "list title recommendation"
        ][0]
        # This is a recommendation, so it should pass but have advice
        self.assertEqual(title_validation["response"], "OK")
        # Since it's just a recommendation with INFO level, it should still pass

    def test_list_validation_with_title_present(self):
        """Test that having a title is recognized"""
        self.maxDiff = None
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'dtd-version="1.0" article-type="research-article" xml:lang="pt">'
            "<body>"
            '<list list-type="bullet">'
            "    <title>My List Title</title>"
            "    <list-item>"
            "        <p>Item with title.</p>"
            "    </list-item>"
            "    <list-item>"
            "        <p>Another item.</p>"
            "    </list-item>"
            "</list>"
            "</body>"
            "</article>"
        )
        obtained = list(
            ArticleListValidation(
                xml_tree,
                {
                    "missing_title_error_level": "INFO",
                },
            ).validate()
        )

        # Check that title validation recognizes the title
        title_validation = [
            item for item in obtained if item["title"] == "list title recommendation"
        ][0]
        self.assertEqual(title_validation["response"], "OK")
        self.assertIn("<title> present", title_validation["got_value"])


if __name__ == "__main__":
    unittest.main()
