"""
Validations for the <permissions> element according to SPS 1.10 specification.

This module implements validations for the <permissions> element and its
children (<license>, <license-p>, copyright elements), which define
conditions under which content may be used, accessed, and distributed.

Reference: https://docs.google.com/document/d/1GTv4Inc2LS_AXY-ToHT3HmO66UT0VAHWJNOIqzBNSgA/edit?tab=t.0#heading=h.permissions
"""

import re

from packtools.sps.validation.utils import build_response


XLINK_HREF = "{http://www.w3.org/1999/xlink}href"
XML_LANG = "{http://www.w3.org/XML/1998/namespace}lang"

# Default valid CC-BY URL patterns
DEFAULT_VALID_LICENSE_URL_PATTERNS = [
    "https://creativecommons.org/licenses/by/",
    "http://creativecommons.org/licenses/by/",
]

# Default language-to-deed mapping
DEFAULT_LANG_TO_DEED = {
    "pt": "deed.pt",
    "en": "deed.en",
    "es": "deed.es",
}


class PermissionsValidation:
    """
    Validates the <permissions> element according to SPS 1.10 rules.

    Validation rules implemented:
    1. Presence of <permissions> in <article-meta>
    2. Uniqueness of <permissions> in <article-meta>
    3. Presence of <license> in <permissions>
    4. Presence of @license-type="open-access" in <license>
    5. Presence of @xlink:href in <license>
    6. Presence of @xml:lang in <license>
    7. Presence of <license-p> in <license>
    8. Valid CC-BY URL in @xlink:href
    9. Consistency between @xml:lang and @xlink:href
    10. Copyright structure validation
    """

    def __init__(self, xmltree, params=None):
        self.xmltree = xmltree
        self.params = params or {}

        # Extract article-level parent info
        root = xmltree.find(".")
        self._parent = {
            "parent": root.tag if root is not None else None,
            "parent_id": root.get("id") if root is not None else None,
            "parent_article_type": root.get("article-type") if root is not None else None,
            "parent_lang": root.get(XML_LANG) if root is not None else None,
        }

    def validate(self):
        """Run all permission validations and yield results."""
        yield from self.validate_permissions_presence()
        yield from self.validate_permissions_uniqueness()
        yield from self.validate_license_presence()
        yield from self.validate_license_type()
        yield from self.validate_xlink_href_presence()
        yield from self.validate_xml_lang_presence()
        yield from self.validate_license_p_presence()
        yield from self.validate_license_url()
        yield from self.validate_lang_link_consistency()
        yield from self.validate_copyright_structure()

    def _get_permissions_nodes(self):
        """Get all <permissions> nodes within <article-meta>."""
        return self.xmltree.xpath(".//front/article-meta/permissions")

    def _get_license_nodes(self):
        """Get all <license> nodes within <permissions> in <article-meta>."""
        return self.xmltree.xpath(".//front/article-meta/permissions/license")

    def validate_permissions_presence(self):
        """Rule 1: Validate that <permissions> is present in <article-meta>."""
        error_level = self.params.get("permissions_presence_error_level", "CRITICAL")
        permissions = self._get_permissions_nodes()
        is_valid = len(permissions) > 0

        yield build_response(
            title="Permissions presence",
            parent=self._parent,
            item="article-meta",
            sub_item="permissions",
            validation_type="exist",
            is_valid=is_valid,
            expected="<permissions> element in <article-meta>",
            obtained="<permissions>" if is_valid else None,
            advice="Add <permissions> element to <article-meta> with a Creative Commons license declaration",
            data={"permissions_count": len(permissions)},
            error_level=error_level,
        )

    def validate_permissions_uniqueness(self):
        """Rule 2: Validate that <permissions> appears exactly once in <article-meta>."""
        error_level = self.params.get("permissions_uniqueness_error_level", "ERROR")
        permissions = self._get_permissions_nodes()
        count = len(permissions)

        if count <= 1:
            # No issue if 0 (handled by presence check) or 1
            return

        yield build_response(
            title="Permissions uniqueness",
            parent=self._parent,
            item="article-meta",
            sub_item="permissions",
            validation_type="value",
            is_valid=False,
            expected="exactly 1 <permissions> element",
            obtained=f"{count} <permissions> elements",
            advice="Remove duplicate <permissions> elements. Only one <permissions> should exist in <article-meta>",
            data={"permissions_count": count},
            error_level=error_level,
        )

    def validate_license_presence(self):
        """Rule 3: Validate that <license> is present in <permissions>."""
        error_level = self.params.get("license_presence_error_level", "CRITICAL")
        permissions = self._get_permissions_nodes()
        if not permissions:
            return

        for perm_node in permissions:
            licenses = perm_node.findall("license")
            is_valid = len(licenses) > 0

            yield build_response(
                title="License presence",
                parent=self._parent,
                item="permissions",
                sub_item="license",
                validation_type="exist",
                is_valid=is_valid,
                expected="<license> element in <permissions>",
                obtained="<license>" if is_valid else None,
                advice="Add <license> element to <permissions> with Creative Commons CC-BY attributes",
                data={"license_count": len(licenses)},
                error_level=error_level,
            )

    def validate_license_type(self):
        """Rule 4: Validate that @license-type='open-access' is present in <license>."""
        error_level = self.params.get("license_type_error_level", "CRITICAL")
        expected_type = self.params.get("expected_license_type", "open-access")
        license_nodes = self._get_license_nodes()

        for license_node in license_nodes:
            obtained_type = license_node.get("license-type")
            is_valid = obtained_type == expected_type

            yield build_response(
                title="License type",
                parent=self._parent,
                item="license",
                sub_item="@license-type",
                validation_type="value",
                is_valid=is_valid,
                expected=expected_type,
                obtained=obtained_type,
                advice=f'Set license-type="{expected_type}" in <license> element',
                data={
                    "license_type": obtained_type,
                    "lang": license_node.get(XML_LANG),
                },
                error_level=error_level,
            )

    def validate_xlink_href_presence(self):
        """Rule 5: Validate that @xlink:href is present in <license>."""
        error_level = self.params.get("xlink_href_presence_error_level", "CRITICAL")
        license_nodes = self._get_license_nodes()

        for license_node in license_nodes:
            href = license_node.get(XLINK_HREF)
            is_valid = bool(href)

            yield build_response(
                title="License xlink:href presence",
                parent=self._parent,
                item="license",
                sub_item="@xlink:href",
                validation_type="exist",
                is_valid=is_valid,
                expected="@xlink:href attribute in <license>",
                obtained=href,
                advice="Add xlink:href attribute with a valid Creative Commons CC-BY URL to <license>",
                data={
                    "xlink_href": href,
                    "lang": license_node.get(XML_LANG),
                },
                error_level=error_level,
            )

    def validate_xml_lang_presence(self):
        """Rule 6: Validate that @xml:lang is present in <license>."""
        error_level = self.params.get("xml_lang_presence_error_level", "CRITICAL")
        license_nodes = self._get_license_nodes()

        for license_node in license_nodes:
            lang = license_node.get(XML_LANG)
            is_valid = bool(lang)

            yield build_response(
                title="License xml:lang presence",
                parent=self._parent,
                item="license",
                sub_item="@xml:lang",
                validation_type="exist",
                is_valid=is_valid,
                expected="@xml:lang attribute in <license>",
                obtained=lang,
                advice="Add xml:lang attribute to <license> element indicating the language of the license text",
                data={
                    "xml_lang": lang,
                    "xlink_href": license_node.get(XLINK_HREF),
                },
                error_level=error_level,
            )

    def validate_license_p_presence(self):
        """Rule 7: Validate that <license-p> is present in <license>."""
        error_level = self.params.get("license_p_presence_error_level", "CRITICAL")
        license_nodes = self._get_license_nodes()

        for license_node in license_nodes:
            license_p = license_node.find("license-p")
            is_valid = license_p is not None

            yield build_response(
                title="License text presence",
                parent=self._parent,
                item="license",
                sub_item="license-p",
                validation_type="exist",
                is_valid=is_valid,
                expected="<license-p> element in <license>",
                obtained="<license-p>" if is_valid else None,
                advice="Add <license-p> element with the license text to <license>",
                data={
                    "has_license_p": is_valid,
                    "lang": license_node.get(XML_LANG),
                },
                error_level=error_level,
            )

    def validate_license_url(self):
        """Rule 8: Validate that @xlink:href is a valid CC-BY URL."""
        error_level = self.params.get("license_url_error_level", "ERROR")
        valid_patterns = self.params.get(
            "valid_license_url_patterns", DEFAULT_VALID_LICENSE_URL_PATTERNS
        )
        license_nodes = self._get_license_nodes()

        for license_node in license_nodes:
            href = license_node.get(XLINK_HREF)
            if not href:
                # Missing href is handled by validate_xlink_href_presence
                continue

            is_valid = any(href.startswith(pattern) for pattern in valid_patterns)

            yield build_response(
                title="License URL",
                parent=self._parent,
                item="license",
                sub_item="@xlink:href",
                validation_type="value",
                is_valid=is_valid,
                expected=f"a Creative Commons CC-BY URL starting with one of {valid_patterns}",
                obtained=href,
                advice=f"Use a valid Creative Commons CC-BY 4.0 URL, e.g. https://creativecommons.org/licenses/by/4.0/",
                data={
                    "xlink_href": href,
                    "lang": license_node.get(XML_LANG),
                },
                error_level=error_level,
            )

    def validate_lang_link_consistency(self):
        """Rule 9: Validate consistency between @xml:lang and @xlink:href."""
        error_level = self.params.get("lang_link_consistency_error_level", "ERROR")
        lang_to_deed = self.params.get("lang_to_deed", DEFAULT_LANG_TO_DEED)
        license_nodes = self._get_license_nodes()

        for license_node in license_nodes:
            lang = license_node.get(XML_LANG)
            href = license_node.get(XLINK_HREF)
            if not lang or not href:
                # Missing attributes are handled by other validations
                continue

            expected_deed = lang_to_deed.get(lang)
            if expected_deed is None:
                # Language not in the mapping, skip consistency check
                continue

            is_valid = href.endswith(expected_deed) or href.endswith(expected_deed + "/")

            yield build_response(
                title="License language and URL consistency",
                parent=self._parent,
                item="license",
                sub_item="@xml:lang and @xlink:href",
                validation_type="value",
                is_valid=is_valid,
                expected=f"URL ending with '{expected_deed}' for language '{lang}'",
                obtained=href,
                advice=f"For xml:lang=\"{lang}\", use a URL ending with '{expected_deed}', "
                       f"e.g. https://creativecommons.org/licenses/by/4.0/{expected_deed}",
                data={
                    "xml_lang": lang,
                    "xlink_href": href,
                    "expected_deed": expected_deed,
                },
                error_level=error_level,
            )

    def validate_copyright_structure(self):
        """Rule 10: Validate copyright structure when <copyright-statement> is present."""
        error_level = self.params.get("copyright_structure_error_level", "WARNING")
        permissions = self._get_permissions_nodes()

        for perm_node in permissions:
            statement = perm_node.find("copyright-statement")
            if statement is None:
                # Copyright is optional; skip if not present
                continue

            statement_text = statement.text or ""
            copyright_year = perm_node.find("copyright-year")

            # Check if statement mentions a year (4 consecutive digits)
            year_match = re.search(r"\b(\d{4})\b", statement_text)
            if year_match and copyright_year is None:
                yield build_response(
                    title="Copyright year",
                    parent=self._parent,
                    item="permissions",
                    sub_item="copyright-year",
                    validation_type="exist",
                    is_valid=False,
                    expected="<copyright-year> when year is mentioned in <copyright-statement>",
                    obtained=None,
                    advice=f"Add <copyright-year>{year_match.group(1)}</copyright-year> to <permissions> "
                           f"since the copyright statement mentions the year '{year_match.group(1)}'",
                    data={
                        "copyright_statement": statement_text,
                        "mentioned_year": year_match.group(1),
                    },
                    error_level=error_level,
                )
