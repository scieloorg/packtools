from unittest import TestCase

from lxml import etree

from packtools.sps.validation.permissions import PermissionsValidation


def _make_xmltree(permissions_xml="", article_type="research-article", lang="en"):
    """Helper to build a minimal article XML tree with the given permissions block."""
    return etree.fromstring(
        f"""<article xmlns:xlink="http://www.w3.org/1999/xlink"
                     xmlns:mml="http://www.w3.org/1998/Math/MathML"
                     dtd-version="1.0"
                     article-type="{article_type}"
                     xml:lang="{lang}">
            <front>
                <article-meta>
                    {permissions_xml}
                </article-meta>
            </front>
        </article>"""
    )


VALID_PERMISSIONS_EN = """
<permissions>
    <license license-type="open-access"
             xlink:href="https://creativecommons.org/licenses/by/4.0/deed.en"
             xml:lang="en">
        <license-p>This is an open-access article distributed under the terms of the Creative Commons Attribution License</license-p>
    </license>
</permissions>
"""

VALID_PERMISSIONS_PT = """
<permissions>
    <license license-type="open-access"
             xlink:href="https://creativecommons.org/licenses/by/4.0/deed.pt"
             xml:lang="pt">
        <license-p>Este é um artigo de acesso aberto</license-p>
    </license>
</permissions>
"""

VALID_PERMISSIONS_WITH_COPYRIGHT = """
<permissions>
    <copyright-statement>Copyright © 2025, the authors</copyright-statement>
    <copyright-year>2025</copyright-year>
    <copyright-holder>the authors</copyright-holder>
    <license license-type="open-access"
             xlink:href="https://creativecommons.org/licenses/by/4.0/deed.en"
             xml:lang="en">
        <license-p>This is an open-access article</license-p>
    </license>
</permissions>
"""


class PermissionsPresenceTest(TestCase):
    """Tests for Rule 1: <permissions> must be present in <article-meta>."""

    def test_permissions_present(self):
        xmltree = _make_xmltree(VALID_PERMISSIONS_EN)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_permissions_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
        self.assertEqual(results[0]["title"], "Permissions presence")

    def test_permissions_missing(self):
        xmltree = _make_xmltree("")
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_permissions_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")
        self.assertIsNotNone(results[0]["advice"])


class PermissionsUniquenessTest(TestCase):
    """Tests for Rule 2: <permissions> must appear exactly once."""

    def test_single_permissions(self):
        xmltree = _make_xmltree(VALID_PERMISSIONS_EN)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_permissions_uniqueness())
        self.assertEqual(len(results), 0)  # No error yielded when exactly one

    def test_duplicate_permissions(self):
        xml = """
        <permissions>
            <license license-type="open-access"
                     xlink:href="https://creativecommons.org/licenses/by/4.0/deed.en"
                     xml:lang="en">
                <license-p>text</license-p>
            </license>
        </permissions>
        <permissions>
            <license license-type="open-access"
                     xlink:href="https://creativecommons.org/licenses/by/4.0/deed.pt"
                     xml:lang="pt">
                <license-p>texto</license-p>
            </license>
        </permissions>
        """
        xmltree = _make_xmltree(xml)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_permissions_uniqueness())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")

    def test_no_permissions(self):
        xmltree = _make_xmltree("")
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_permissions_uniqueness())
        self.assertEqual(len(results), 0)  # Handled by presence check


class LicensePresenceTest(TestCase):
    """Tests for Rule 3: <license> must be present in <permissions>."""

    def test_license_present(self):
        xmltree = _make_xmltree(VALID_PERMISSIONS_EN)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_license_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_license_missing(self):
        xml = "<permissions></permissions>"
        xmltree = _make_xmltree(xml)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_license_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")

    def test_no_permissions(self):
        xmltree = _make_xmltree("")
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_license_presence())
        self.assertEqual(len(results), 0)  # No permissions, nothing to check


class LicenseTypeTest(TestCase):
    """Tests for Rule 4: @license-type must be 'open-access'."""

    def test_license_type_open_access(self):
        xmltree = _make_xmltree(VALID_PERMISSIONS_EN)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_license_type())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")
        self.assertEqual(results[0]["got_value"], "open-access")

    def test_license_type_wrong(self):
        xml = """
        <permissions>
            <license license-type="subscription"
                     xlink:href="https://creativecommons.org/licenses/by/4.0/deed.en"
                     xml:lang="en">
                <license-p>text</license-p>
            </license>
        </permissions>
        """
        xmltree = _make_xmltree(xml)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_license_type())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")
        self.assertEqual(results[0]["got_value"], "subscription")

    def test_license_type_missing(self):
        xml = """
        <permissions>
            <license xlink:href="https://creativecommons.org/licenses/by/4.0/deed.en"
                     xml:lang="en">
                <license-p>text</license-p>
            </license>
        </permissions>
        """
        xmltree = _make_xmltree(xml)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_license_type())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")
        self.assertIsNone(results[0]["got_value"])


class XlinkHrefPresenceTest(TestCase):
    """Tests for Rule 5: @xlink:href must be present in <license>."""

    def test_xlink_href_present(self):
        xmltree = _make_xmltree(VALID_PERMISSIONS_EN)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_xlink_href_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_xlink_href_missing(self):
        xml = """
        <permissions>
            <license license-type="open-access" xml:lang="en">
                <license-p>text</license-p>
            </license>
        </permissions>
        """
        xmltree = _make_xmltree(xml)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_xlink_href_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")


class XmlLangPresenceTest(TestCase):
    """Tests for Rule 6: @xml:lang must be present in <license>."""

    def test_xml_lang_present(self):
        xmltree = _make_xmltree(VALID_PERMISSIONS_EN)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_xml_lang_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_xml_lang_missing(self):
        xml = """
        <permissions>
            <license license-type="open-access"
                     xlink:href="https://creativecommons.org/licenses/by/4.0/deed.en">
                <license-p>text</license-p>
            </license>
        </permissions>
        """
        xmltree = _make_xmltree(xml)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_xml_lang_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")


class LicensePPresenceTest(TestCase):
    """Tests for Rule 7: <license-p> must be present in <license>."""

    def test_license_p_present(self):
        xmltree = _make_xmltree(VALID_PERMISSIONS_EN)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_license_p_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_license_p_missing(self):
        xml = """
        <permissions>
            <license license-type="open-access"
                     xlink:href="https://creativecommons.org/licenses/by/4.0/deed.en"
                     xml:lang="en">
            </license>
        </permissions>
        """
        xmltree = _make_xmltree(xml)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_license_p_presence())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "CRITICAL")


class LicenseUrlTest(TestCase):
    """Tests for Rule 8: @xlink:href must be a valid CC-BY URL."""

    def test_valid_https_url(self):
        xmltree = _make_xmltree(VALID_PERMISSIONS_EN)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_license_url())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_valid_http_url(self):
        xml = """
        <permissions>
            <license license-type="open-access"
                     xlink:href="http://creativecommons.org/licenses/by/4.0/"
                     xml:lang="en">
                <license-p>text</license-p>
            </license>
        </permissions>
        """
        xmltree = _make_xmltree(xml)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_license_url())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_invalid_url(self):
        xml = """
        <permissions>
            <license license-type="open-access"
                     xlink:href="https://example.com/license"
                     xml:lang="en">
                <license-p>text</license-p>
            </license>
        </permissions>
        """
        xmltree = _make_xmltree(xml)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_license_url())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")

    def test_non_by_cc_url(self):
        xml = """
        <permissions>
            <license license-type="open-access"
                     xlink:href="https://creativecommons.org/licenses/by-nc/4.0/"
                     xml:lang="en">
                <license-p>text</license-p>
            </license>
        </permissions>
        """
        xmltree = _make_xmltree(xml)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_license_url())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")

    def test_missing_href_skipped(self):
        xml = """
        <permissions>
            <license license-type="open-access" xml:lang="en">
                <license-p>text</license-p>
            </license>
        </permissions>
        """
        xmltree = _make_xmltree(xml)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_license_url())
        self.assertEqual(len(results), 0)  # Skipped, handled by href presence check


class LangLinkConsistencyTest(TestCase):
    """Tests for Rule 9: @xml:lang must match the language in @xlink:href."""

    def test_consistent_en(self):
        xmltree = _make_xmltree(VALID_PERMISSIONS_EN)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_lang_link_consistency())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_consistent_pt(self):
        xmltree = _make_xmltree(VALID_PERMISSIONS_PT)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_lang_link_consistency())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "OK")

    def test_inconsistent_lang_and_link(self):
        xml = """
        <permissions>
            <license license-type="open-access"
                     xlink:href="https://creativecommons.org/licenses/by/4.0/deed.pt"
                     xml:lang="en">
                <license-p>text</license-p>
            </license>
        </permissions>
        """
        xmltree = _make_xmltree(xml)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_lang_link_consistency())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")

    def test_url_without_deed_suffix(self):
        xml = """
        <permissions>
            <license license-type="open-access"
                     xlink:href="https://creativecommons.org/licenses/by/4.0/"
                     xml:lang="en">
                <license-p>text</license-p>
            </license>
        </permissions>
        """
        xmltree = _make_xmltree(xml)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_lang_link_consistency())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "ERROR")

    def test_missing_lang_skipped(self):
        xml = """
        <permissions>
            <license license-type="open-access"
                     xlink:href="https://creativecommons.org/licenses/by/4.0/deed.en">
                <license-p>text</license-p>
            </license>
        </permissions>
        """
        xmltree = _make_xmltree(xml)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_lang_link_consistency())
        self.assertEqual(len(results), 0)

    def test_unknown_lang_skipped(self):
        xml = """
        <permissions>
            <license license-type="open-access"
                     xlink:href="https://creativecommons.org/licenses/by/4.0/deed.fr"
                     xml:lang="fr">
                <license-p>text</license-p>
            </license>
        </permissions>
        """
        xmltree = _make_xmltree(xml)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_lang_link_consistency())
        self.assertEqual(len(results), 0)


class CopyrightStructureTest(TestCase):
    """Tests for Rule 10: Validate copyright structure when present."""

    def test_copyright_with_year_element(self):
        xmltree = _make_xmltree(VALID_PERMISSIONS_WITH_COPYRIGHT)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_copyright_structure())
        self.assertEqual(len(results), 0)  # No warning, structure is complete

    def test_copyright_statement_mentions_year_but_missing_element(self):
        xml = """
        <permissions>
            <copyright-statement>Copyright © 2025, the authors</copyright-statement>
            <license license-type="open-access"
                     xlink:href="https://creativecommons.org/licenses/by/4.0/deed.en"
                     xml:lang="en">
                <license-p>text</license-p>
            </license>
        </permissions>
        """
        xmltree = _make_xmltree(xml)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_copyright_structure())
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["response"], "WARNING")
        self.assertIn("2025", results[0]["advice"])

    def test_copyright_statement_without_year_no_warning(self):
        xml = """
        <permissions>
            <copyright-statement>Copyright the authors</copyright-statement>
            <license license-type="open-access"
                     xlink:href="https://creativecommons.org/licenses/by/4.0/deed.en"
                     xml:lang="en">
                <license-p>text</license-p>
            </license>
        </permissions>
        """
        xmltree = _make_xmltree(xml)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_copyright_structure())
        self.assertEqual(len(results), 0)

    def test_no_copyright_no_warning(self):
        xmltree = _make_xmltree(VALID_PERMISSIONS_EN)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate_copyright_structure())
        self.assertEqual(len(results), 0)


class FullValidateTest(TestCase):
    """Tests for the full validate() method with valid and invalid XML."""

    def test_valid_xml_all_pass(self):
        xmltree = _make_xmltree(VALID_PERMISSIONS_EN)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate())
        for result in results:
            self.assertEqual(
                result["response"],
                "OK",
                f"Validation '{result['title']}' failed: {result.get('advice')}",
            )

    def test_valid_xml_with_copyright_all_pass(self):
        xmltree = _make_xmltree(VALID_PERMISSIONS_WITH_COPYRIGHT)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate())
        for result in results:
            self.assertEqual(
                result["response"],
                "OK",
                f"Validation '{result['title']}' failed: {result.get('advice')}",
            )

    def test_empty_article_meta_yields_critical(self):
        xmltree = _make_xmltree("")
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate())
        # Should have at least the permissions presence check
        self.assertTrue(len(results) >= 1)
        self.assertEqual(results[0]["response"], "CRITICAL")
        self.assertEqual(results[0]["title"], "Permissions presence")

    def test_multiple_licenses(self):
        xml = """
        <permissions>
            <license license-type="open-access"
                     xlink:href="https://creativecommons.org/licenses/by/4.0/deed.en"
                     xml:lang="en">
                <license-p>English license text</license-p>
            </license>
            <license license-type="open-access"
                     xlink:href="https://creativecommons.org/licenses/by/4.0/deed.pt"
                     xml:lang="pt">
                <license-p>Texto de licença em português</license-p>
            </license>
        </permissions>
        """
        xmltree = _make_xmltree(xml)
        validator = PermissionsValidation(xmltree)
        results = list(validator.validate())
        for result in results:
            self.assertEqual(
                result["response"],
                "OK",
                f"Validation '{result['title']}' failed: {result.get('advice')}",
            )

    def test_custom_error_levels(self):
        xmltree = _make_xmltree("")
        params = {"permissions_presence_error_level": "WARNING"}
        validator = PermissionsValidation(xmltree, params)
        results = list(validator.validate_permissions_presence())
        self.assertEqual(results[0]["response"], "WARNING")


class ResponseStructureTest(TestCase):
    """Tests verifying that response dictionaries have correct structure."""

    def setUp(self):
        self.xmltree = _make_xmltree(VALID_PERMISSIONS_EN)
        self.validator = PermissionsValidation(self.xmltree)
        self.expected_keys = {
            "title",
            "parent",
            "parent_id",
            "parent_article_type",
            "parent_lang",
            "item",
            "sub_item",
            "validation_type",
            "response",
            "expected_value",
            "got_value",
            "message",
            "msg_text",
            "msg_params",
            "advice",
            "adv_text",
            "adv_params",
            "data",
        }

    def test_response_has_expected_keys(self):
        results = list(self.validator.validate())
        self.assertTrue(len(results) > 0)
        for result in results:
            self.assertEqual(set(result.keys()), self.expected_keys)

    def test_parent_info(self):
        results = list(self.validator.validate())
        for result in results:
            self.assertEqual(result["parent"], "article")
            self.assertEqual(result["parent_article_type"], "research-article")
            self.assertEqual(result["parent_lang"], "en")
