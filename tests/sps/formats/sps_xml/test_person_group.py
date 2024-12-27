import unittest
from lxml import etree as ET
from packtools.sps.formats.sps_xml.person_group import build_person_group


class TestBuildPersonGroupAuthor(unittest.TestCase):
    def test_build_person_group_author(self):
        data = [
            {
                "person-group-type": "author",
                "persons": [
                    {
                        "surname": "Einstein",
                        "given-names": "Albert",
                        "prefix": "Prof.",
                        "suffix": "Neto"
                    }
                ],
            }
        ]
        expected_xml_str = (
            '<person-group person-group-type="author">'
            '<name>'
            '<surname>Einstein</surname>'
            '<given-names>Albert</given-names>'
            '<prefix>Prof.</prefix>'
            '<suffix>Neto</suffix>'
            '</name>'
            '</person-group>'
        )
        for person_group_elem in build_person_group(data):
            generated_xml_str = ET.tostring(person_group_elem, encoding="unicode", method="xml")
            self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_person_group_author_None(self):
        data = [
            {
                "person-group-type": None
            }
        ]

        with self.assertRaises(ValueError) as e:
            list(build_person_group(data))
        self.assertEqual(str(e.exception), "person-group-type is required")


class TestBuildPersonGroupCollab(unittest.TestCase):
    def test_build_person_group_collab(self):
        data = [
            {
                "person-group-type": "author",
                "collab": ["Instituto Brasil Leitor"]
            }
        ]

        expected_xml_str = (
            '<person-group person-group-type="author">'
            '<collab>Instituto Brasil Leitor</collab>'
            '</person-group>'
        )
        for person_group_elem in build_person_group(data):
            generated_xml_str = ET.tostring(person_group_elem, encoding="unicode", method="xml")
            self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_person_group_collab_None(self):
        data = [
            {
                "person-group-type": "author",
                "collab": None
            }
        ]

        expected_xml_str = (
            '<person-group person-group-type="author"/>'
        )
        for person_group_elem in build_person_group(data):
            generated_xml_str = ET.tostring(person_group_elem, encoding="unicode", method="xml")
            self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())


class TestBuildPersonGroupRole(unittest.TestCase):
    def test_build_person_group_role(self):
        data = [
            {
                "person-group-type": "author",
                "role": ["Pesquisador"]
            }
        ]

        expected_xml_str = (
            '<person-group person-group-type="author">'
            '<role>Pesquisador</role>'
            '</person-group>'
        )
        for person_group_elem in build_person_group(data):
            generated_xml_str = ET.tostring(person_group_elem, encoding="unicode", method="xml")
            self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())

    def test_build_person_group_role_None(self):
        data = [
            {
                "person-group-type": "author",
                "role": None
            }
        ]

        expected_xml_str = (
            '<person-group person-group-type="author"/>'
        )
        for person_group_elem in build_person_group(data):
            generated_xml_str = ET.tostring(person_group_elem, encoding="unicode", method="xml")
            self.assertEqual(generated_xml_str.strip(), expected_xml_str.strip())
