import unittest

from packtools.sps.utils import xml_utils
from packtools.sps.formats.am import record


class RecordTest(unittest.TestCase):
    def setUp(self):
        self.xml_tree = xml_utils.get_xml_tree(
            "tests/sps/formats/am/examples/S0104-11692025000100300.xml"
        )
        self.data = record.data(self.xml_tree)

    def test_field_v30(self):
        expected = {"v30": [{"_": "Rev. Latino-Am. Enfermagem"}]}
        obtained = record.field_v30(self.data)
        self.assertDictEqual(expected, obtained)

    def test_field_v31(self):
        expected = {'v31': [{'_': '33'}]}
        obtained = record.field_v31(self.data)
        self.assertDictEqual(expected, obtained)

    def test_code(self):
        expected = {'code': 'S0104-11692025000100300'}
        obtained = record.field_code(self.data)
        self.assertDictEqual(expected, obtained)

    def test_field_v121(self):
        expected = {'v121': [{'_': '00300'}]}
        obtained = record.field_v121(self.data)
        self.assertDictEqual(expected, obtained)

    def test_field_v10(self):
        obtained = record.field_v10(self.data)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v10", obtained)
        self.assertGreater(len(obtained["v10"]), 0)

        author = obtained["v10"][0]
        expected_keys = {"k", "n", "1", "s", "r", "_"}
        self.assertTrue(expected_keys.issubset(author.keys()))

        self.assertTrue(author["k"].startswith("0000-"))  # ORCID
        self.assertTrue(author["n"])  # Nome
        self.assertTrue(author["s"])  # Sobrenome

    def test_field_v10_includes_specific_author(self):
        obtained = record.field_v10(self.data)["v10"]
        author = next((a for a in obtained if a["k"] == "0000-0002-4201-0624"), None)
        self.assertIsNotNone(author)
        self.assertEqual(author["n"], "Janaina Recanello")
        self.assertEqual(author["s"], "Begui")
        self.assertEqual(author["1"], "aff1")
        self.assertEqual(author["r"], "Study concept and design")


if __name__ == "__main__":
    unittest.main()
