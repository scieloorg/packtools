import unittest
import xml.etree.ElementTree as ET
from packtools.sps.formats.sps_xml.person_group import build_person_group


class TestBuildPersonGroupAuthor(unittest.TestCase):
    def test_build_person_group_author(self):
        data = {
            "author": [
                {
                    "surname": "Einstein",
                    "given_names": "Albert",
                    "prefix": "Prof.",
                    "suffix": "Neto"
                }
            ]
        }
        expected_xml_str = (
            '<person-group person-group-type="author">'
            '<name>'
            '<surname>Einstein</surname>'
            '<given_names>Albert</given_names>'
            '<prefix>Prof.</prefix>'
            '<suffix>Neto</suffix>'
            '</name>'
            '</person-group>'
        )
        person_group_elem = build_person_group(data)
        generated_xml_str = ET.tostring(person_group_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_person_group_author_None(self):
        data = {
            "author": None
        }

        with self.assertRaises(ValueError) as e:
            build_person_group(data)
        self.assertEqual(str(e.exception), "person group type is required")


class TestBuildPersonGroupCollab(unittest.TestCase):
    def test_build_person_group_collab(self):
        data = {
            "author": [
                {
                    "surname": "Einstein",
                }
            ],
            "collab": ["Instituto Brasil Leitor"],
        }
        expected_xml_str = (
            '<person-group person-group-type="author">'
            '<name>'
            '<surname>Einstein</surname>'
            '</name>'
            '<collab>Instituto Brasil Leitor</collab>'
            '</person-group>'
        )
        person_group_elem = build_person_group(data)
        generated_xml_str = ET.tostring(person_group_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_person_group_collab_None(self):
        data = {
            "author": [
                {
                    "surname": "Einstein",
                }
            ],
            "collab": None
        }
        expected_xml_str = (
            '<person-group person-group-type="author">'
            '<name>'
            '<surname>Einstein</surname>'
            '</name>'
            '</person-group>'
        )
        person_group_elem = build_person_group(data)
        generated_xml_str = ET.tostring(person_group_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildPersonGroupRole(unittest.TestCase):
    def test_build_person_group_role(self):
        data = {
            "author": [
                {
                    "surname": "Einstein",
                }
            ],
            "role": ["Pesquisador"]
        }
        expected_xml_str = (
            '<person-group person-group-type="author">'
            '<name>'
            '<surname>Einstein</surname>'
            '</name>'
            '<role>Pesquisador</role>'
            '</person-group>'
        )
        person_group_elem = build_person_group(data)
        generated_xml_str = ET.tostring(person_group_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_person_group_role_None(self):
        data = {
            "author": [
                {
                    "surname": "Einstein",
                }
            ],
            "role": None
        }
        expected_xml_str = (
            '<person-group person-group-type="author">'
            '<name>'
            '<surname>Einstein</surname>'
            '</name>'
            '</person-group>'
        )
        person_group_elem = build_person_group(data)
        generated_xml_str = ET.tostring(person_group_elem, encoding="unicode", method="xml")
        self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())
