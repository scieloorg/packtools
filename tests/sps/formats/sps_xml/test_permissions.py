import unittest
import xml.etree.ElementTree as ET
from packtools.sps.formats.sps_xml.permissions import build_permissions


class TestBuildPermissionsCopyrightStatement(unittest.TestCase):
    def test_build_permissions_copyright_statement(self):
        data = {
            "copyright-statement": "Copyright © 2014 SciELO",
            "licenses": [
                {
                    "license-type": "open-access",
                    "xlink:href": "http://creativecommons.org/licenses/by-nc-sa/4.0/",
                    "xml:lang": "pt",
                    "license-p": "This is an article published in open access under a Creative Commons license"
                }
            ]
        }
        expected_xml_str = (
            '<permissions>'
            '<copyright-statement>Copyright © 2014 SciELO</copyright-statement>'
            '<license license-type="open-access" xlink:href="http://creativecommons.org/licenses/by-nc-sa/4.0/" xml:lang="pt">'
            'This is an article published in open access under a Creative Commons license'
            '</license>'
            '</permissions>'
        )
        permissions_elem = build_permissions(data)
        generated_xml_str = ET.tostring(permissions_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_permissions_copyright_statement_None(self):
        data = {
            "copyright-statement": None,
            "licenses": [
                {
                    "license-type": "open-access",
                    "xlink:href": "http://creativecommons.org/licenses/by-nc-sa/4.0/",
                    "xml:lang": "pt",
                    "license-p": "This is an article published in open access under a Creative Commons license"
                }
            ]
        }
        expected_xml_str = (
            '<permissions>'
            '<license license-type="open-access" xlink:href="http://creativecommons.org/licenses/by-nc-sa/4.0/" xml:lang="pt">'
            'This is an article published in open access under a Creative Commons license'
            '</license>'
            '</permissions>'
        )
        permissions_elem = build_permissions(data)
        generated_xml_str = ET.tostring(permissions_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildPermissionsCopyrightYear(unittest.TestCase):
    def test_build_permissions_copyright_year(self):
        data = {
            "copyright-year": "2014",
            "licenses": [
                {
                    "license-type": "open-access",
                    "xlink:href": "http://creativecommons.org/licenses/by-nc-sa/4.0/",
                    "xml:lang": "pt",
                    "license-p": "This is an article published in open access under a Creative Commons license"
                }
            ]
        }
        expected_xml_str = (
            '<permissions>'
            '<copyright-year>2014</copyright-year>'
            '<license license-type="open-access" xlink:href="http://creativecommons.org/licenses/by-nc-sa/4.0/" xml:lang="pt">'
            'This is an article published in open access under a Creative Commons license'
            '</license>'
            '</permissions>'
        )
        permissions_elem = build_permissions(data)
        generated_xml_str = ET.tostring(permissions_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_permissions_copyright_year_None(self):
        data = {
            "copyright-year": None,
            "licenses": [
                {
                    "license-type": "open-access",
                    "xlink:href": "http://creativecommons.org/licenses/by-nc-sa/4.0/",
                    "xml:lang": "pt",
                    "license-p": "This is an article published in open access under a Creative Commons license"
                }
            ]
        }
        expected_xml_str = (
            '<permissions>'
            '<license license-type="open-access" xlink:href="http://creativecommons.org/licenses/by-nc-sa/4.0/" xml:lang="pt">'
            'This is an article published in open access under a Creative Commons license'
            '</license>'
            '</permissions>'
        )
        permissions_elem = build_permissions(data)
        generated_xml_str = ET.tostring(permissions_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildPermissionsCopyrightHolder(unittest.TestCase):
    def test_build_permissions_copyright_holder(self):
        data = {
            "copyright-holder": "SciELO",
            "licenses": [
                {
                    "license-type": "open-access",
                    "xlink:href": "http://creativecommons.org/licenses/by-nc-sa/4.0/",
                    "xml:lang": "pt",
                    "license-p": "This is an article published in open access under a Creative Commons license"
                }
            ]
        }
        expected_xml_str = (
            '<permissions>'
            '<copyright-holder>SciELO</copyright-holder>'
            '<license license-type="open-access" xlink:href="http://creativecommons.org/licenses/by-nc-sa/4.0/" xml:lang="pt">'
            'This is an article published in open access under a Creative Commons license'
            '</license>'
            '</permissions>'
        )
        permissions_elem = build_permissions(data)
        generated_xml_str = ET.tostring(permissions_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_permissions_copyright_holder_None(self):
        data = {
            "copyright-holder": None,
            "licenses": [
                {
                    "license-type": "open-access",
                    "xlink:href": "http://creativecommons.org/licenses/by-nc-sa/4.0/",
                    "xml:lang": "pt",
                    "license-p": "This is an article published in open access under a Creative Commons license"
                }
            ]
        }
        expected_xml_str = (
            '<permissions>'
            '<license license-type="open-access" xlink:href="http://creativecommons.org/licenses/by-nc-sa/4.0/" xml:lang="pt">'
            'This is an article published in open access under a Creative Commons license'
            '</license>'
            '</permissions>'
        )
        permissions_elem = build_permissions(data)
        generated_xml_str = ET.tostring(permissions_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildPermissionsLicenses(unittest.TestCase):
    def test_build_permissions_licenses(self):
        data = {
            "licenses": [
                {
                    "license-type": "open-access",
                    "xlink:href": "http://creativecommons.org/licenses/by-nc-sa/4.0/",
                    "xml:lang": "pt",
                    "license-p": "This is an article published in open access under a Creative Commons license"
                }
            ]
        }
        expected_xml_str = (
            '<permissions>'
            '<license license-type="open-access" '
            'xlink:href="http://creativecommons.org/licenses/by-nc-sa/4.0/" '
            'xml:lang="pt">This is an article published in open access under a Creative Commons license'
            '</license>'
            '</permissions>'
        )
        permissions_elem = build_permissions(data)
        generated_xml_str = ET.tostring(permissions_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_permissions_licenses_None(self):
        data = {
            "licenses": None
        }
        with self.assertRaises(TypeError) as e:
            build_permissions(data)
        self.assertEqual(str(e.exception), "licenses must be a list")

    def test_build_permissions_licenses_required_attributes(self):
        # vale para os demais atributos, exceto "license-p"
        data = {
            "licenses": [
                {
                    "xlink:href": "http://creativecommons.org/licenses/by-nc-sa/4.0/",
                    "xml:lang": "pt",
                    "license-p": "This is an article published in open access under a Creative Commons license"
                }
            ]
        }
        with self.assertRaises(ValueError) as e:
            build_permissions(data)
        self.assertEqual(str(e.exception), "'license-type' is required")
