"""
Tests for GraphicValidation class according to SPS 1.10 specification.

Tests validation of <graphic> and <inline-graphic> elements including:
- @id attribute (required for both)
- @xlink:href attribute (required)
- File extensions
- SVG only in <alternatives>
- Accessibility elements
"""

import unittest
from lxml import etree
from packtools.sps.models.graphic import XmlGraphic
from packtools.sps.validation.graphic import GraphicValidation


class TestGraphicValidation(unittest.TestCase):
    """Test validations for <graphic> and <inline-graphic> elements per SPS 1.10."""
    
    def setUp(self):
        """Set up validation parameters for each test."""
        self.params = {
            "media_attributes_error_level": "CRITICAL",
            "xlink_href_error_level": "ERROR",
            "valid_extension": ["jpg", "png", "tif", "tiff", "jpeg", "svg"],
            "svg_error_level": "ERROR",
            "alt_text_exist_error_level": "WARNING",
            "alt_text_content_error_level": "CRITICAL",
            "alt_text_media_restriction_error_level": "ERROR",
            "alt_text_duplication_error_level": "WARNING",
            "decorative_alt_text_error_level": "INFO",
            "long_desc_exist_error_level": "WARNING",
            "long_desc_content_error_level": "CRITICAL",
            "long_desc_minimum_length_error_level": "ERROR",
            "long_desc_media_restriction_error_level": "ERROR",
            "long_desc_duplication_error_level": "WARNING",
            "long_desc_occurrence_error_level": "ERROR",
            "long_desc_null_incompatibility_error_level": "WARNING",
            "xref_transcript_error_level": "WARNING",
            "transcript_error_level": "WARNING",
            "content_type_error_level": "CRITICAL",
            "speaker_speech_error_level": "WARNING",
            "structure_error_level": "CRITICAL",
            "content_types": ["machine-generated"],
        }

    # ========== Tests for @id validation (Rules 1 & 3) ==========
    
    def test_graphic_with_id_is_valid(self):
        """Test that <graphic> with @id attribute passes validation."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <fig id="f1">
                    <graphic id="g1" xlink:href="image.jpg">
                        <alt-text>Test</alt-text>
                    </graphic>
                </fig>
            </body>
        </article>
        """
        tree = etree.fromstring(xml_content.encode())
        graphics_data = list(XmlGraphic(tree).data)
        
        validator = GraphicValidation(graphics_data[0], self.params)
        result = validator.validate_id()
        
        self.assertEqual(result["response"], "OK")
        self.assertEqual(result["got_value"], "g1")

    def test_graphic_without_id_fails(self):
        """Test that <graphic> without @id attribute fails with CRITICAL error."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <fig id="f1">
                    <graphic xlink:href="image.jpg"/>
                </fig>
            </body>
        </article>
        """
        tree = etree.fromstring(xml_content.encode())
        graphics_data = list(XmlGraphic(tree).data)
        
        validator = GraphicValidation(graphics_data[0], self.params)
        result = validator.validate_id()
        
        self.assertEqual(result["response"], "CRITICAL")
        self.assertIsNone(result["got_value"])
        self.assertIn("Add id=", result["advice"])

    def test_inline_graphic_with_id_is_valid(self):
        """Test that <inline-graphic> with @id attribute passes validation."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    Text with <inline-graphic id="ig1" xlink:href="inline.png"/> image.
                </p>
            </body>
        </article>
        """
        tree = etree.fromstring(xml_content.encode())
        graphics_data = list(XmlGraphic(tree).data)
        
        validator = GraphicValidation(graphics_data[0], self.params)
        result = validator.validate_id()
        
        self.assertEqual(result["response"], "OK")
        self.assertEqual(result["got_value"], "ig1")

    def test_inline_graphic_without_id_fails(self):
        """Test that <inline-graphic> without @id fails per SPS 1.10 (Rule 3)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <inline-graphic xlink:href="inline.png"/>
                </p>
            </body>
        </article>
        """
        tree = etree.fromstring(xml_content.encode())
        graphics_data = list(XmlGraphic(tree).data)
        
        validator = GraphicValidation(graphics_data[0], self.params)
        result = validator.validate_id()
        
        self.assertEqual(result["response"], "CRITICAL")
        self.assertIsNone(result["got_value"])

    # ========== Tests for @xlink:href validation (Rules 2 & 4) ==========

    def test_graphic_with_valid_extension_jpg(self):
        """Test that <graphic> with .jpg extension passes validation."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <fig id="f1">
                    <graphic id="g1" xlink:href="image.jpg">
                        <alt-text>Test</alt-text>
                    </graphic>
                </fig>
            </body>
        </article>
        """
        tree = etree.fromstring(xml_content.encode())
        graphics_data = list(XmlGraphic(tree).data)
        
        validator = GraphicValidation(graphics_data[0], self.params)
        result = validator.validate_xlink_href()
        
        self.assertEqual(result["response"], "OK")
        self.assertEqual(result["got_value"], "image.jpg")

    def test_graphic_with_valid_extension_jpeg(self):
        """Test that <graphic> with .jpeg extension passes validation."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <fig id="f1">
                    <graphic id="g1" xlink:href="photo.jpeg">
                        <alt-text>Test</alt-text>
                    </graphic>
                </fig>
            </body>
        </article>
        """
        tree = etree.fromstring(xml_content.encode())
        graphics_data = list(XmlGraphic(tree).data)
        
        validator = GraphicValidation(graphics_data[0], self.params)
        result = validator.validate_xlink_href()
        
        self.assertEqual(result["response"], "OK")

    def test_graphic_with_valid_extension_png(self):
        """Test that <graphic> with .png extension passes validation."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <fig id="f1">
                    <graphic id="g1" xlink:href="image.png">
                        <alt-text>Test</alt-text>
                    </graphic>
                </fig>
            </body>
        </article>
        """
        tree = etree.fromstring(xml_content.encode())
        graphics_data = list(XmlGraphic(tree).data)
        
        validator = GraphicValidation(graphics_data[0], self.params)
        result = validator.validate_xlink_href()
        
        self.assertEqual(result["response"], "OK")

    def test_graphic_with_valid_extension_tif(self):
        """Test that <graphic> with .tif extension passes validation."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <fig id="f1">
                    <graphic id="g1" xlink:href="image.tif">
                        <alt-text>Test</alt-text>
                    </graphic>
                </fig>
            </body>
        </article>
        """
        tree = etree.fromstring(xml_content.encode())
        graphics_data = list(XmlGraphic(tree).data)
        
        validator = GraphicValidation(graphics_data[0], self.params)
        result = validator.validate_xlink_href()
        
        self.assertEqual(result["response"], "OK")

    def test_graphic_with_valid_extension_tiff(self):
        """Test that <graphic> with .tiff extension passes validation."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <fig id="f1">
                    <graphic id="g1" xlink:href="image.tiff">
                        <alt-text>Test</alt-text>
                    </graphic>
                </fig>
            </body>
        </article>
        """
        tree = etree.fromstring(xml_content.encode())
        graphics_data = list(XmlGraphic(tree).data)
        
        validator = GraphicValidation(graphics_data[0], self.params)
        result = validator.validate_xlink_href()
        
        self.assertEqual(result["response"], "OK")

    def test_inline_graphic_with_valid_extension(self):
        """Test that <inline-graphic> with valid extension passes validation."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <inline-graphic id="ig1" xlink:href="inline.png"/>
                </p>
            </body>
        </article>
        """
        tree = etree.fromstring(xml_content.encode())
        graphics_data = list(XmlGraphic(tree).data)
        
        validator = GraphicValidation(graphics_data[0], self.params)
        result = validator.validate_xlink_href()
        
        self.assertEqual(result["response"], "OK")

    def test_graphic_with_invalid_extension_fails(self):
        """Test that <graphic> with invalid extension fails validation."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <fig id="f1">
                    <graphic id="g1" xlink:href="document.pdf">
                        <alt-text>Test</alt-text>
                    </graphic>
                </fig>
            </body>
        </article>
        """
        tree = etree.fromstring(xml_content.encode())
        graphics_data = list(XmlGraphic(tree).data)
        
        validator = GraphicValidation(graphics_data[0], self.params)
        result = validator.validate_xlink_href()
        
        self.assertEqual(result["response"], "ERROR")
        self.assertEqual(result["got_value"], "document.pdf")

    # ========== Tests for SVG in alternatives validation (Rule 7) ==========

    def test_svg_in_alternatives_is_valid(self):
        """Test that .svg file inside <alternatives> passes validation."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <fig id="f1">
                    <alternatives>
                        <graphic id="g1" xlink:href="vector.svg">
                            <alt-text>Test</alt-text>
                        </graphic>
                        <graphic id="g2" xlink:href="raster.jpg">
                            <alt-text>Test</alt-text>
                        </graphic>
                    </alternatives>
                </fig>
            </body>
        </article>
        """
        tree = etree.fromstring(xml_content.encode())
        graphics_data = list(XmlGraphic(tree).data)
        
        # Test first graphic (svg)
        validator = GraphicValidation(graphics_data[0], self.params)
        results = list(validator.validate_svg_in_alternatives())
        
        # Should have one result for svg check
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_svg_not_in_alternatives_fails(self):
        """Test that .svg file NOT inside <alternatives> fails validation (Rule 7)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <fig id="f1">
                    <graphic id="g1" xlink:href="image.svg"/>
                </fig>
            </body>
        </article>
        """
        tree = etree.fromstring(xml_content.encode())
        graphics_data = list(XmlGraphic(tree).data)
        
        validator = GraphicValidation(graphics_data[0], self.params)
        results = list(validator.validate_svg_in_alternatives())
        
        # Should fail validation
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")
        self.assertIn("alternatives", results[0]["advice"].lower())

    def test_non_svg_not_in_alternatives_is_valid(self):
        """Test that non-.svg file NOT in <alternatives> passes validation."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <fig id="f1">
                    <graphic id="g1" xlink:href="image.jpg">
                        <alt-text>Test</alt-text>
                    </graphic>
                </fig>
            </body>
        </article>
        """
        tree = etree.fromstring(xml_content.encode())
        graphics_data = list(XmlGraphic(tree).data)
        
        validator = GraphicValidation(graphics_data[0], self.params)
        results = list(validator.validate_svg_in_alternatives())
        
        # Should not generate any results (no svg to check)
        self.assertEqual(len(results), 0)

    def test_svg_case_insensitive(self):
        """Test that SVG validation is case-insensitive (.SVG, .Svg, .svg)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <fig id="f1">
                    <graphic id="g1" xlink:href="image.SVG"/>
                </fig>
            </body>
        </article>
        """
        tree = etree.fromstring(xml_content.encode())
        graphics_data = list(XmlGraphic(tree).data)
        
        validator = GraphicValidation(graphics_data[0], self.params)
        results = list(validator.validate_svg_in_alternatives())
        
        # Should fail even with uppercase .SVG
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")

    # ========== Integration tests ==========

    def test_complete_validation_all_valid(self):
        """Test complete validation with all rules passing."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <fig id="f1">
                    <graphic id="g1" xlink:href="image.jpg">
                        <alt-text>Description of the image</alt-text>
                    </graphic>
                </fig>
            </body>
        </article>
        """
        tree = etree.fromstring(xml_content.encode())
        graphics_data = list(XmlGraphic(tree).data)
        
        validator = GraphicValidation(graphics_data[0], self.params)
        results = [r for r in validator.validate() if r is not None]
        
        # All critical checks should pass
        critical_checks = [r for r in results if r.get("title") in ["@id", "@xlink:href validation"]]
        for check in critical_checks:
            self.assertEqual(check["response"], "OK")

    def test_complete_validation_multiple_failures(self):
        """Test complete validation with multiple rule violations."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <fig id="f1">
                    <graphic xlink:href="image.svg"/>
                </fig>
            </body>
        </article>
        """
        tree = etree.fromstring(xml_content.encode())
        graphics_data = list(XmlGraphic(tree).data)
        
        validator = GraphicValidation(graphics_data[0], self.params)
        results = [r for r in validator.validate() if r is not None]
        
        # Should have multiple failures
        failures = [r for r in results if r.get("response") not in ["OK", None]]
        
        # At minimum: missing @id and svg not in alternatives
        failure_titles = [r.get("title") for r in failures]
        self.assertIn("@id", failure_titles)
        self.assertIn("SVG in alternatives", failure_titles)


if __name__ == "__main__":
    unittest.main()
