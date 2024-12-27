import unittest
from lxml import etree as ET
from packtools.sps.formats.sps_xml.kwd_group import build_kwd_group


class TestBuildKwdGroup(unittest.TestCase):
    def test_build_kwd_group(self):
        data = {
            "kwd-lang": "pt",
            "kwd-title": "Palavra-chave",
            "kwds": [
                "Broncoscopia",
            ]
        }
        expected_xml_str = (
            '<kwd-group xml:lang="pt">'
            '<title>Palavra-chave</title>'
            '<kwd>Broncoscopia</kwd>'
            '</kwd-group>'
        )
        kwd_group_elem = build_kwd_group(data)
        generated_xml_str = ET.tostring(kwd_group_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_kwd_group_None(self):
        data = {
            "kwd-lang": None,
            "kwd-title": "Palavra-chave",
            "kwds": [
                "Broncoscopia",
            ]
        }
        with self.assertRaises(ValueError) as e:
            build_kwd_group(data)
        self.assertEqual(str(e.exception), "kwd-lang is required")


class TestBuildKwdGroupTitle(unittest.TestCase):
    def test_build_kwd_group_title(self):
        data = {
            "kwd-lang": "pt",
            "kwd-title": "Palavra-chave",
            "kwds": [
                "Broncoscopia",
            ]
        }
        expected_xml_str = (
            '<kwd-group xml:lang="pt">'
            '<title>Palavra-chave</title>'
            '<kwd>Broncoscopia</kwd>'
            '</kwd-group>'
        )
        kwd_group_elem = build_kwd_group(data)
        generated_xml_str = ET.tostring(kwd_group_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_kwd_group_title_None(self):
        data = {
            "kwd-lang": "pt",
            "kwd-title": None,
            "kwds": [
                "Broncoscopia",
            ]
        }
        with self.assertRaises(ValueError) as e:
            build_kwd_group(data)
        self.assertEqual(str(e.exception), "kwd-title is required")


class TestBuildKwdGroupKwds(unittest.TestCase):
    def test_build_kwd_group_kwds(self):
        data = {
            "kwd-lang": "pt",
            "kwd-title": "Palavra-chave",
            "kwds": [
                "Broncoscopia",
            ]
        }
        expected_xml_str = (
            '<kwd-group xml:lang="pt">'
            '<title>Palavra-chave</title>'
            '<kwd>Broncoscopia</kwd>'
            '</kwd-group>'
        )
        kwd_group_elem = build_kwd_group(data)
        generated_xml_str = ET.tostring(kwd_group_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_kwd_group_kwds_None(self):
        data = {
            "kwd-lang": "pt",
            "kwd-title": "Palavra-chave",
            "kwds": None
        }
        with self.assertRaises(ValueError) as e:
            build_kwd_group(data)
        self.assertEqual(str(e.exception), "kwds must not be an empty list")
