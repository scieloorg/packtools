"""
Unit tests for ext-link validation according to SPS 1.10.

Tests cover mandatory attributes, URL format, allowed values,
and accessibility requirements (descriptive text).
"""
import unittest
from lxml import etree

from packtools.sps.validation.ext_link import ExtLinkValidation


def filter_results(results):
    """Filter out None values from validator results."""
    return [r for r in results if r is not None]


class TestExtLinkValidation(unittest.TestCase):
    """Tests for ext-link element validations."""
    
    # ========== TESTS: @ext-link-type PRESENCE (CRITICAL) ==========
    
    def test_validate_ext_link_type_presence_valid(self):
        """Test valid ext-link with @ext-link-type attribute."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="uri" xlink:href="https://www.scielo.br/">
                        SciELO Brasil
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_ext_link_type_presence())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
    
    def test_validate_ext_link_type_presence_missing(self):
        """Test ext-link without @ext-link-type attribute (CRITICAL error)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link xlink:href="https://www.scielo.br/">
                        SciELO Brasil
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_ext_link_type_presence())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")
        self.assertIn("Add @ext-link-type attribute", results[0]["advice"])
        self.assertIsNotNone(results[0]["adv_text"])
        self.assertIsNotNone(results[0]["adv_params"])
        self.assertIn("text", results[0]["adv_params"])
    
    # ========== TESTS: @xlink:href PRESENCE (CRITICAL) ==========
    
    def test_validate_xlink_href_presence_valid(self):
        """Test valid ext-link with @xlink:href attribute."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="uri" xlink:href="https://www.scielo.br/">
                        SciELO Brasil
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_xlink_href_presence())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
    
    def test_validate_xlink_href_presence_missing(self):
        """Test ext-link without @xlink:href attribute (CRITICAL error)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="uri">
                        SciELO Brasil
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_xlink_href_presence())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")
        self.assertIn("Add @xlink:href attribute", results[0]["advice"])
        self.assertIsNotNone(results[0]["adv_text"])
        self.assertIsNotNone(results[0]["adv_params"])
    
    # ========== TESTS: @xlink:href FORMAT (ERROR) ==========
    
    def test_validate_xlink_href_format_valid_http(self):
        """Test @xlink:href with valid http:// URL."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="uri" xlink:href="http://www.scielo.br/">
                        SciELO Brasil
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_xlink_href_format())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
    
    def test_validate_xlink_href_format_valid_https(self):
        """Test @xlink:href with valid https:// URL."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="uri" xlink:href="https://www.scielo.br/">
                        SciELO Brasil
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_xlink_href_format())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
    
    def test_validate_xlink_href_format_invalid_no_protocol(self):
        """Test @xlink:href without protocol (ERROR)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="uri" xlink:href="www.scielo.br">
                        SciELO Brasil
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_xlink_href_format())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")
        self.assertIn("must start with http:// or https://", results[0]["advice"])
        self.assertIsNotNone(results[0]["adv_text"])
        self.assertIsNotNone(results[0]["adv_params"])
    
    def test_validate_xlink_href_format_skips_missing(self):
        """Test that format validation skips ext-links without @xlink:href."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="uri">
                        SciELO Brasil
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_xlink_href_format())
        
        # Should not validate format if href is missing
        self.assertEqual(len(results), 0)
    
    # ========== TESTS: @ext-link-type VALUE (ERROR) ==========
    
    def test_validate_ext_link_type_value_uri(self):
        """Test @ext-link-type="uri" (valid)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="uri" xlink:href="https://www.scielo.br/">
                        SciELO Brasil
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_ext_link_type_value())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
    
    def test_validate_ext_link_type_value_doi(self):
        """Test @ext-link-type="doi" (valid)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="doi" xlink:href="https://doi.org/10.1590/example">
                        DOI Link
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_ext_link_type_value())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
    
    def test_validate_ext_link_type_value_pmid(self):
        """Test @ext-link-type="pmid" (valid)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="pmid" xlink:href="https://pubmed.ncbi.nlm.nih.gov/12345/">
                        PubMed Link
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_ext_link_type_value())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
    
    def test_validate_ext_link_type_value_pmcid(self):
        """Test @ext-link-type="pmcid" (valid)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="pmcid" xlink:href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC123/">
                        PMC Link
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_ext_link_type_value())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
    
    def test_validate_ext_link_type_value_clinical_trial(self):
        """Test @ext-link-type="clinical-trial" (valid)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="clinical-trial" xlink:href="https://clinicaltrials.gov/study/NCT12345">
                        Clinical Trial
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_ext_link_type_value())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
    
    def test_validate_ext_link_type_value_invalid(self):
        """Test @ext-link-type with invalid value (ERROR)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="website" xlink:href="https://www.scielo.br/">
                        SciELO Brasil
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_ext_link_type_value())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")
        self.assertIn("Replace @ext-link-type", results[0]["advice"])
        self.assertIsNotNone(results[0]["adv_text"])
        self.assertIsNotNone(results[0]["adv_params"])
        self.assertIn("ext_link_type", results[0]["adv_params"])
    
    def test_validate_ext_link_type_value_skips_missing(self):
        """Test that value validation skips ext-links without @ext-link-type."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link xlink:href="https://www.scielo.br/">
                        SciELO Brasil
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_ext_link_type_value())
        
        # Should not validate value if type is missing
        self.assertEqual(len(results), 0)
    
    # ========== TESTS: DESCRIPTIVE TEXT (WARNING) ==========
    
    def test_validate_descriptive_text_valid(self):
        """Test ext-link with descriptive text (OK)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="uri" xlink:href="https://www.scielo.br/">
                        SciELO Brasil
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_descriptive_text())
        
        # Descriptive text should not yield any results (only invalid cases)
        self.assertEqual(len(results), 0)
    
    def test_validate_descriptive_text_generic_leia_mais(self):
        """Test ext-link with generic text 'leia mais' (WARNING)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="uri" xlink:href="https://www.scielo.br/">
                        Leia mais
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_descriptive_text())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "WARNING")
        self.assertIn("Replace generic text", results[0]["advice"])
        self.assertIsNotNone(results[0]["adv_text"])
        self.assertIsNotNone(results[0]["adv_params"])
    
    def test_validate_descriptive_text_generic_click_here(self):
        """Test ext-link with generic text 'click here' (WARNING)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="uri" xlink:href="https://www.scielo.br/">
                        click here
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_descriptive_text())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "WARNING")
        self.assertIn("Replace generic text", results[0]["advice"])
    
    def test_validate_descriptive_text_case_insensitive(self):
        """Test generic text detection is case-insensitive."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="uri" xlink:href="https://www.scielo.br/">
                        CLIQUE AQUI
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_descriptive_text())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "WARNING")
    
    def test_validate_descriptive_text_empty(self):
        """Test ext-link with empty text (skips validation)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="uri" xlink:href="https://www.scielo.br/"></ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_descriptive_text())
        
        # Empty text should be skipped
        self.assertEqual(len(results), 0)
    
    # ========== TESTS: @xlink:title WHEN GENERIC/URL (WARNING) ==========
    
    def test_validate_xlink_title_when_generic_text_with_title(self):
        """Test generic text with @xlink:title present (OK)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="uri" 
                              xlink:href="https://www.scielo.br/"
                              xlink:title="SciELO Scientific Library">
                        Leia mais
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_xlink_title_when_generic())
        
        # With xlink:title, should not yield results
        self.assertEqual(len(results), 0)
    
    def test_validate_xlink_title_when_generic_text_without_title(self):
        """Test generic text without @xlink:title (WARNING)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="uri" xlink:href="https://www.scielo.br/">
                        Leia mais
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_xlink_title_when_generic())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "WARNING")
        self.assertIn("Add @xlink:title attribute", results[0]["advice"])
        self.assertIsNotNone(results[0]["adv_text"])
        self.assertIsNotNone(results[0]["adv_params"])
        self.assertIn("reason", results[0]["adv_params"])
    
    def test_validate_xlink_title_when_url_text_with_title(self):
        """Test URL as text with @xlink:title present (OK)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="uri" 
                              xlink:href="https://example.com/path"
                              xlink:title="Example Website">
                        https://example.com/path
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_xlink_title_when_generic())
        
        # With xlink:title, should not yield results
        self.assertEqual(len(results), 0)
    
    def test_validate_xlink_title_when_url_text_without_title(self):
        """Test URL as text without @xlink:title (WARNING)."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="uri" xlink:href="https://example.com/path">
                        https://example.com/path
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_xlink_title_when_generic())
        
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "WARNING")
        self.assertIn("Add @xlink:title attribute", results[0]["advice"])
    
    def test_validate_xlink_title_descriptive_text(self):
        """Test descriptive text does not require @xlink:title."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="uri" xlink:href="https://www.scielo.br/">
                        SciELO Brasil
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        results = filter_results(validator.validate_xlink_title_when_generic())
        
        # Descriptive text should not yield results
        self.assertEqual(len(results), 0)
    
    # ========== TESTS: MULTIPLE EXT-LINKS ==========
    
    def test_validate_multiple_ext_links(self):
        """Test validation of multiple ext-links."""
        xml_content = """
        <article xmlns:xlink="http://www.w3.org/1999/xlink">
            <body>
                <p>
                    <ext-link ext-link-type="uri" xlink:href="https://www.scielo.br/">
                        SciELO Brasil
                    </ext-link>
                </p>
                <p>
                    <ext-link xlink:href="www.example.com">
                        Example
                    </ext-link>
                </p>
                <p>
                    <ext-link ext-link-type="website" xlink:href="https://example.org/">
                        click here
                    </ext-link>
                </p>
            </body>
        </article>
        """
        xmltree = etree.fromstring(xml_content)
        validator = ExtLinkValidation(xmltree)
        
        # Check all validations
        type_presence_results = filter_results(validator.validate_ext_link_type_presence())
        href_presence_results = filter_results(validator.validate_xlink_href_presence())
        href_format_results = filter_results(validator.validate_xlink_href_format())
        type_value_results = filter_results(validator.validate_ext_link_type_value())
        text_results = filter_results(validator.validate_descriptive_text())
        
        # First ext-link is valid
        # Second ext-link: missing @ext-link-type, invalid URL format
        # Third ext-link: invalid @ext-link-type value, generic text
        
        self.assertEqual(len(type_presence_results), 3)  # All checked
        self.assertEqual(len([r for r in type_presence_results if r["response"] != "OK"]), 1)  # 1 error
        
        self.assertEqual(len(href_format_results), 3)  # All 3 have href
        self.assertEqual(len([r for r in href_format_results if r["response"] != "OK"]), 1)  # 1 error
        
        self.assertEqual(len(type_value_results), 2)  # Only 2 have type
        self.assertEqual(len([r for r in type_value_results if r["response"] != "OK"]), 1)  # 1 error
        
        self.assertEqual(len(text_results), 1)  # Only 1 generic text
        self.assertEqual(text_results[0]["response"], "WARNING")


if __name__ == "__main__":
    unittest.main()
