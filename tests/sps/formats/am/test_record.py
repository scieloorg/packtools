import unittest

from packtools.sps.utils import xml_utils
from packtools.sps.formats.am import record, am


class RecordTest(unittest.TestCase):
    def setUp(self):
        self.xml_tree = xml_utils.get_xml_tree(
            "tests/sps/formats/am/examples/S0104-11692025000100300.xml"
        )

    def test_field_v30(self):
        expected = {"v30": [{"_": "Rev. Latino-Am. Enfermagem"}]}
        obtained = am.get_journal(self.xml_tree)
        self.assertDictEqual(expected, obtained)

    def test_field_v31(self):
        expected = {'v31': [{'_': '33'}]}
        obtained = am.get_articlemeta_issue(self.xml_tree)
        self.assertLessEqual(expected.items(), obtained.items())

    def test_code(self):
        expected = {'code': 'S0104-11692025000100300'}
        obtained = am.get_ids(self.xml_tree)
        self.assertDictEqual(expected, obtained)

    def test_field_v121(self):
        expected = {'v121': [{'_': '00300'}]}
        obtained = am.get_articlemeta_issue(self.xml_tree)
        self.assertLessEqual(expected.items(), obtained.items())

    def test_field_v10(self):
        obtained = am.get_contribs(self.xml_tree)
        print(obtained)
        self.assertIsInstance(obtained, dict)
        self.assertIn("v10", obtained)
        self.assertGreater(len(obtained["v10"]), 0)

        author = obtained["v10"][0]
        expected_keys = {"k", "n", "1", "s", "r", "_"}
        self.assertTrue(expected_keys.issubset(author.keys()))

    def test_field_v10_includes_specific_author(self):
        obtained = am.get_contribs(self.xml_tree)
        author = next((a for a in obtained["v10"] if a["k"] == "0000-0002-4201-0624"), None)
        self.assertIsNotNone(author)
        self.assertEqual(author["n"], "Janaina Recanello")
        self.assertEqual(author["s"], "Begui")
        self.assertEqual(author["1"], "aff1")
        self.assertEqual(author["r"], "ND")


if __name__ == "__main__":
    unittest.main()
