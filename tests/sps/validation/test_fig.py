import unittest
from lxml import etree

from packtools.sps.validation.fig import ArticleFigValidation


class FigValidationTest(unittest.TestCase):
    """Test suite for fig validation according to SPS 1.10 specification"""

    def setUp(self):
        """Set up common test rules"""
        self.maxDiff = None
        self.rules = {
            "article_types_requires": ["research-article"],
            "absent_error_level": "WARNING",
            "id_error_level": "CRITICAL",
            "graphic_error_level": "CRITICAL",
            "xlink_href_error_level": "CRITICAL",
            "file_extension_error_level": "ERROR",
            "fig_type_error_level": "ERROR",
            "xml_lang_in_fig_group_error_level": "ERROR",
            "accessibility_error_level": "WARNING",
            "alt_text_length_error_level": "WARNING",
            "allowed_file_extensions": ["jpg", "jpeg", "png", "tif", "tiff"],
            "allowed_fig_types": ["graphic", "chart", "diagram", "drawing", "illustration", "map"],
            "alt_text_max_length": 120
        }

    def test_fig_validation_no_fig_when_required(self):
        """Test validation when fig is required but absent"""
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<body>"
            "<p>Some text content without figures.</p>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(xml_tree, self.rules).validate())

        # Should return one validation error
        self.assertEqual(len(obtained), 1)
        self.assertEqual(obtained[0]["title"], "fig presence")
        self.assertEqual(obtained[0]["response"], "WARNING")
        self.assertEqual(obtained[0]["item"], "fig")

    def test_fig_validation_complete_valid_fig(self):
        """Test validation with a complete valid figure"""
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<body>"
            '<fig id="f01">'
            "<label>Figure 1</label>"
            "<caption><title>Test figure</title></caption>"
            '<graphic xlink:href="image.jpg">'
            "<alt-text>Brief description</alt-text>"
            "</graphic>"
            "</fig>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(xml_tree, self.rules).validate())

        # All validations should pass
        for result in obtained:
            self.assertEqual(result["response"], "OK", 
                           f"Validation '{result['title']}' failed: {result.get('advice')}")

    def test_fig_validation_missing_id(self):
        """Test Rule 1: Validate @id presence (CRITICAL)"""
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<body>"
            '<fig>'
            "<label>Figure 1</label>"
            "<caption><title>Test</title></caption>"
            '<graphic xlink:href="image.jpg"/>'
            "</fig>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(xml_tree, self.rules).validate())

        # Find the @id validation
        id_validation = [v for v in obtained if v["title"] == "@id"][0]
        self.assertEqual(id_validation["response"], "CRITICAL")
        self.assertEqual(id_validation["sub_item"], "@id")
        self.assertIsNone(id_validation["got_value"])

    def test_fig_validation_missing_graphic(self):
        """Test Rule 2: Validate <graphic> presence (CRITICAL)"""
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<body>"
            '<fig id="f01">'
            "<label>Figure 1</label>"
            "<caption><title>Test</title></caption>"
            "</fig>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(xml_tree, self.rules).validate())

        # Find the <graphic> validation
        graphic_validation = [v for v in obtained if v["title"] == "<graphic>"][0]
        self.assertEqual(graphic_validation["response"], "CRITICAL")
        self.assertEqual(graphic_validation["sub_item"], "graphic")
        self.assertIsNone(graphic_validation["got_value"])

    def test_fig_validation_missing_xlink_href(self):
        """Test Rule 3: Validate @xlink:href in <graphic> (CRITICAL)"""
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<body>"
            '<fig id="f01">'
            "<label>Figure 1</label>"
            "<caption><title>Test</title></caption>"
            '<graphic/>'
            "</fig>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(xml_tree, self.rules).validate())

        # Find the @xlink:href validation
        xlink_validation = [v for v in obtained if v["title"] == "@xlink:href"][0]
        self.assertEqual(xlink_validation["response"], "CRITICAL")
        self.assertEqual(xlink_validation["sub_item"], "@xlink:href")

    def test_fig_validation_invalid_file_extension(self):
        """Test Rule 4: Validate file extension (ERROR)"""
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<body>"
            '<fig id="f01">'
            "<label>Figure 1</label>"
            "<caption><title>Test</title></caption>"
            '<graphic xlink:href="image.bmp"/>'
            "</fig>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(xml_tree, self.rules).validate())

        # Find the file extension validation
        ext_validation = [v for v in obtained if v["title"] == "file extension"][0]
        self.assertEqual(ext_validation["response"], "ERROR")
        self.assertEqual(ext_validation["got_value"], "bmp")

    def test_fig_validation_svg_outside_alternatives(self):
        """Test Rule 4: SVG is only allowed inside <alternatives>"""
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<body>"
            '<fig id="f01">'
            "<label>Figure 1</label>"
            "<caption><title>Test</title></caption>"
            '<graphic xlink:href="image.svg"/>'
            "</fig>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(xml_tree, self.rules).validate())

        # Find the file extension validation
        ext_validation = [v for v in obtained if v["title"] == "file extension"][0]
        self.assertEqual(ext_validation["response"], "ERROR")
        self.assertEqual(ext_validation["got_value"], "svg")
        self.assertIn("only allowed inside <alternatives>", ext_validation["advice"])

    def test_fig_validation_svg_inside_alternatives(self):
        """Test Rule 4: SVG is allowed inside <alternatives>"""
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<body>"
            '<fig id="f01">'
            "<label>Figure 1</label>"
            "<caption><title>Test</title></caption>"
            "<alternatives>"
            '<graphic xlink:href="image.svg"/>'
            '<graphic xlink:href="image.jpg"/>'
            "</alternatives>"
            "</fig>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(xml_tree, self.rules).validate())

        # Find the file extension validation - should be OK
        ext_validation = [v for v in obtained if v["title"] == "file extension"][0]
        self.assertEqual(ext_validation["response"], "OK")

    def test_fig_validation_invalid_fig_type(self):
        """Test Rule 5: Validate @fig-type values (ERROR)"""
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<body>"
            '<fig id="f01" fig-type="photo">'
            "<label>Figure 1</label>"
            "<caption><title>Test</title></caption>"
            '<graphic xlink:href="image.jpg"/>'
            "</fig>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(xml_tree, self.rules).validate())

        # Find the @fig-type validation
        fig_type_validation = [v for v in obtained if v["title"] == "@fig-type"][0]
        self.assertEqual(fig_type_validation["response"], "ERROR")
        self.assertEqual(fig_type_validation["got_value"], "photo")

    def test_fig_validation_valid_fig_types(self):
        """Test Rule 5: All valid @fig-type values"""
        valid_types = ["graphic", "chart", "diagram", "drawing", "illustration", "map"]
        
        for fig_type in valid_types:
            with self.subTest(fig_type=fig_type):
                xml_tree = etree.fromstring(
                    f'<article xmlns:xlink="http://www.w3.org/1999/xlink" '
                    'article-type="research-article" xml:lang="pt">'
                    "<body>"
                    f'<fig id="f01" fig-type="{fig_type}">'
                    "<label>Figure 1</label>"
                    "<caption><title>Test</title></caption>"
                    '<graphic xlink:href="image.jpg"/>'
                    "</fig>"
                    "</body>"
                    "</article>"
                )
                obtained = list(ArticleFigValidation(xml_tree, self.rules).validate())

                # Find the @fig-type validation
                fig_type_validation = [v for v in obtained if v["title"] == "@fig-type"][0]
                self.assertEqual(fig_type_validation["response"], "OK")

    def test_fig_validation_missing_xml_lang_in_fig_group(self):
        """Test Rule 6: Validate @xml:lang in <fig> within <fig-group> (ERROR)"""
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<body>"
            '<fig-group id="fg01">'
            '<fig id="f01">'
            "<label>Figura 1</label>"
            "<caption><title>Test</title></caption>"
            '<graphic xlink:href="image.jpg"/>'
            "</fig>"
            "</fig-group>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(xml_tree, self.rules).validate())

        # Find the @xml:lang validation
        xml_lang_validation = [v for v in obtained if v["title"] == "@xml:lang in fig-group"][0]
        self.assertEqual(xml_lang_validation["response"], "ERROR")
        self.assertIsNone(xml_lang_validation["got_value"])

    def test_fig_validation_with_xml_lang_in_fig_group(self):
        """Test Rule 6: @xml:lang present in <fig> within <fig-group>"""
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="en">'
            "<body>"
            '<fig-group id="fg01">'
            '<fig id="f01" xml:lang="pt">'
            "<label>Figura 1</label>"
            "<caption><title>Test PT</title></caption>"
            '<graphic xlink:href="image.jpg"/>'
            "</fig>"
            '<fig id="f02" xml:lang="en">'
            "<label>Figure 1</label>"
            "<caption><title>Test EN</title></caption>"
            '<graphic xlink:href="image.jpg"/>'
            "</fig>"
            "</fig-group>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(xml_tree, self.rules).validate())

        # Find all @xml:lang validations - both should pass
        xml_lang_validations = [v for v in obtained if v["title"] == "@xml:lang in fig-group"]
        for validation in xml_lang_validations:
            self.assertEqual(validation["response"], "OK")

    def test_fig_validation_missing_accessibility(self):
        """Test Rule 7: Validate presence of alt-text or long-desc (WARNING)"""
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<body>"
            '<fig id="f01">'
            "<label>Figure 1</label>"
            "<caption><title>Test</title></caption>"
            '<graphic xlink:href="image.jpg"/>'
            "</fig>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(xml_tree, self.rules).validate())

        # Find the accessibility validation
        accessibility_validation = [v for v in obtained if v["title"] == "accessibility"][0]
        self.assertEqual(accessibility_validation["response"], "WARNING")
        self.assertIsNone(accessibility_validation["got_value"])

    def test_fig_validation_with_alt_text(self):
        """Test Rule 7: Figure with alt-text"""
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<body>"
            '<fig id="f01">'
            "<label>Figure 1</label>"
            "<caption><title>Test</title></caption>"
            '<graphic xlink:href="image.jpg">'
            "<alt-text>Brief description</alt-text>"
            "</graphic>"
            "</fig>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(xml_tree, self.rules).validate())

        # Find the accessibility validation
        accessibility_validation = [v for v in obtained if v["title"] == "accessibility"][0]
        self.assertEqual(accessibility_validation["response"], "OK")

    def test_fig_validation_with_long_desc(self):
        """Test Rule 7: Figure with long-desc"""
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<body>"
            '<fig id="f01">'
            "<label>Figure 1</label>"
            "<caption><title>Test</title></caption>"
            '<graphic xlink:href="image.jpg">'
            "<long-desc>Long detailed description for accessibility</long-desc>"
            "</graphic>"
            "</fig>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(xml_tree, self.rules).validate())

        # Find the accessibility validation
        accessibility_validation = [v for v in obtained if v["title"] == "accessibility"][0]
        self.assertEqual(accessibility_validation["response"], "OK")

    def test_fig_validation_alt_text_exceeds_length(self):
        """Test Rule 8: Validate alt-text character limit (WARNING)"""
        long_alt_text = "This is a very long alt text that exceeds the 120 character limit. " \
                       "It should trigger a warning because it's too long for accessibility purposes."
        
        xml_tree = etree.fromstring(
            f'<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<body>"
            '<fig id="f01">'
            "<label>Figure 1</label>"
            "<caption><title>Test</title></caption>"
            '<graphic xlink:href="image.jpg">'
            f"<alt-text>{long_alt_text}</alt-text>"
            "</graphic>"
            "</fig>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(xml_tree, self.rules).validate())

        # Find the alt-text length validation
        alt_text_validation = [v for v in obtained if v["title"] == "alt-text length"][0]
        self.assertEqual(alt_text_validation["response"], "WARNING")
        self.assertIn("characters", alt_text_validation["got_value"])

    def test_fig_validation_alt_text_within_length(self):
        """Test Rule 8: alt-text within character limit"""
        xml_tree = etree.fromstring(
            '<article xmlns:xlink="http://www.w3.org/1999/xlink" '
            'article-type="research-article" xml:lang="pt">'
            "<body>"
            '<fig id="f01">'
            "<label>Figure 1</label>"
            "<caption><title>Test</title></caption>"
            '<graphic xlink:href="image.jpg">'
            "<alt-text>Brief description within limit</alt-text>"
            "</graphic>"
            "</fig>"
            "</body>"
            "</article>"
        )
        obtained = list(ArticleFigValidation(xml_tree, self.rules).validate())

        # Find the alt-text length validation
        alt_text_validation = [v for v in obtained if v["title"] == "alt-text length"][0]
        self.assertEqual(alt_text_validation["response"], "OK")

    def test_fig_validation_all_file_extensions(self):
        """Test Rule 4: All allowed file extensions"""
        valid_extensions = ["jpg", "jpeg", "png", "tif", "tiff"]
        
        for ext in valid_extensions:
            with self.subTest(extension=ext):
                xml_tree = etree.fromstring(
                    f'<article xmlns:xlink="http://www.w3.org/1999/xlink" '
                    'article-type="research-article" xml:lang="pt">'
                    "<body>"
                    '<fig id="f01">'
                    "<label>Figure 1</label>"
                    "<caption><title>Test</title></caption>"
                    f'<graphic xlink:href="image.{ext}"/>'
                    "</fig>"
                    "</body>"
                    "</article>"
                )
                obtained = list(ArticleFigValidation(xml_tree, self.rules).validate())

                # Find the file extension validation
                ext_validation = [v for v in obtained if v["title"] == "file extension"][0]
                self.assertEqual(ext_validation["response"], "OK", 
                               f"Extension '{ext}' should be valid")


if __name__ == "__main__":
    unittest.main()
